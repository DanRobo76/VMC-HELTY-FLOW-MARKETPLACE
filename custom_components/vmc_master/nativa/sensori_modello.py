"""I sensori calcolati della VMC come entità dell'integrazione: sensori e sensori binari
con un modello.

Ognuno dei 120 sensori calcolati di una VMC (``motore/generato_fase4/sensori.py``) è una
configurazione come quella di un sensore template del package (stato, disponibilità,
icona, nome, unità...) con i modelli tradotti (``ModelloHA``, un ``Template``) al posto del
Jinja. Qui sono entità dell'integrazione (``SensorEntity``, ``BinarySensorEntity``) che si
comportano come i sensori template di Home Assistant senza trigger: stessa sequenza
all'avvio, stesso ordine dei modelli resi e degli attributi scritti, stato scritto subito,
durante la consegna dell'evento che li ha fatti ricalcolare, stessi errori, stessa
disponibilità, stesso ritardo ``delay_on``, stessi entity_id, unique_id e nomi (la
cronologia degli utenti resta). Il simulatore confronta istanti e ordine dei cambi con
il package.

I modelli si seguono con una funzione con la firma di
``homeassistant.helpers.event.async_track_template_result`` (parametro ``segui``): di norma
quella dell'integrazione (``motore.seguire.traccia_modelli``), che segue le entità come
Home Assistant e consegna anche i cambi dei valori interni del motore (memoria interna,
timer del motore).

Solo le chiavi che i 120 sensori usano: ``default_entity_id``, ``name``, ``unique_id``,
``state``, ``icon``, ``availability`` e, per i sensori, ``unit_of_measurement``,
``device_class``, ``state_class``; per i sensori binari ``delay_on``. Una configurazione
con altre chiavi non si accetta (``ValueError``): andrebbe portata prima.

Logica portata da Home Assistant 2026.11.2 (Apache-2.0), file
``homeassistant/components/template/entity.py``, ``template_entity.py``, ``sensor.py``,
``binary_sensor.py`` e ``validators.py``, ridotta alle chiavi qui sopra.
"""

from __future__ import annotations

import contextlib
import logging
from collections.abc import Awaitable, Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import timedelta
from typing import Any, Protocol

import probatio
from homeassistant.components.binary_sensor import (
    ENTITY_ID_FORMAT as FORMATO_BINARIO,
)
from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
)
from homeassistant.components.sensor import (
    ENTITY_ID_FORMAT as FORMATO_SENSORE,
)
from homeassistant.components.sensor import (
    NON_NUMERIC_DEVICE_CLASSES,
    RestoreSensor,
    SensorDeviceClass,
    SensorExtraStoredData,
)
from homeassistant.const import (
    ATTR_FRIENDLY_NAME,
    ATTR_ICON,
    STATE_ON,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
)
from homeassistant.core import (
    CALLBACK_TYPE,
    Event,
    EventStateChangedData,
    HomeAssistant,
    State,
    callback,
)
from homeassistant.exceptions import TemplateError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity import Entity, async_generate_entity_id
from homeassistant.helpers.event import (
    TrackTemplate,
    TrackTemplateResult,
    TrackTemplateResultListener,
    async_call_later,
)
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.start import async_at_start
from homeassistant.helpers.template import (
    Template,
    TemplateStateFromEntityId,
    result_as_boolean,
)
from homeassistant.helpers.typing import StateType
from homeassistant.util.enum import try_parse_enum

from .motore.seguire import traccia_modelli

_LOGGER = logging.getLogger(__name__)

CONF_AVAILABILITY = "availability"
CONF_DEFAULT_ENTITY_ID = "default_entity_id"
CONF_DELAY_ON = "delay_on"
CONF_DEVICE_CLASS = "device_class"
CONF_ICON = "icon"
CONF_NAME = "name"
CONF_STATE = "state"
CONF_STATE_CLASS = "state_class"
CONF_UNIQUE_ID = "unique_id"
CONF_UNIT_OF_MEASUREMENT = "unit_of_measurement"

# le chiavi di tutti i sensori calcolati, poi quelle dei sensori e dei sensori binari
CHIAVI_COMUNI = frozenset(
    {
        CONF_DEFAULT_ENTITY_ID,
        CONF_NAME,
        CONF_UNIQUE_ID,
        CONF_STATE,
        CONF_ICON,
        CONF_AVAILABILITY,
    }
)
CHIAVI_SENSORE = CHIAVI_COMUNI | {
    CONF_UNIT_OF_MEASUREMENT,
    CONF_DEVICE_CLASS,
    CONF_STATE_CLASS,
}
CHIAVI_BINARIO = CHIAVI_COMUNI | {CONF_DELAY_ON}

# classi dei sensori con lo stato come data o istante: Home Assistant lo converte, qui non
# è portato (nessuno dei 120 sensori le usa)
_CLASSI_CON_DATA = (
    SensorDeviceClass.DATE,
    SensorDeviceClass.TIMESTAMP,
    SensorDeviceClass.UPTIME,
)

# nessun dato in più da ripristinare (sensori binari)
_NESSUN_DATO = object()


class Seguiti(Protocol):
    """I modelli seguiti (come ``TrackTemplateResultInfo``): ricalcolo e fine."""

    def async_refresh(self) -> None: ...

    def async_remove(self) -> None: ...


class Seguire(Protocol):
    """Come seguire i modelli: la firma di ``async_track_template_result``."""

    def __call__(
        self,
        hass: HomeAssistant,
        track_templates: Sequence[TrackTemplate],
        action: TrackTemplateResultListener,
        strict: bool = False,
        log_fn: Callable[[int, str], None] | None = None,
        has_super_template: bool = False,
    ) -> Seguiti: ...


class _StatoFittizio(State):
    """``this`` dei modelli resi nel costruttore, prima che l'entità abbia uno stato (come
    ``DummyState`` di Home Assistant)."""

    def __init__(self) -> None:
        super().__init__("unknown.unknown", STATE_UNKNOWN)
        self.entity_id = None  # type: ignore[assignment]

    @property  # type: ignore[override]
    def name(self) -> str:
        return "<None>"


def _errore_di_validazione(
    risultato: Any,
    modello: Template,
    attributo: str,
    entity_id: str | None,
    errore: probatio.Invalid,
) -> None:
    """Un risultato che il validatore di un attributo non accetta (come
    ``log_validation_error``)."""
    logging.getLogger(
        f"{__name__}.{entity_id.split('.', maxsplit=1)[0]}" if entity_id else __name__
    ).error(
        (
            "Error validating template result '%s' "
            "from template '%s' "
            "for attribute '%s' in entity %s "
            "validation message '%s'"
        ),
        risultato,
        modello,
        attributo,
        entity_id,
        errore.msg,
    )


@dataclass
class ModelloDellEntita:
    """Un modello della configurazione e l'attributo che scrive (``EntityTemplate``)."""

    attributo: str
    modello: Template
    validatore: Callable[[Any], Any] | None
    aggiorna: Callable[[Any], None] | None
    none_su_errore: bool


class AttributoDelModello:
    """Il risultato di un modello in un attributo dell'entità (``_TemplateAttribute``)."""

    def __init__(
        self,
        entita: Entity,
        attributo: str,
        modello: Template,
        validatore: Callable[[Any], Any] | None = None,
        aggiorna: Callable[[Any], None] | None = None,
        none_su_errore: bool = False,
    ) -> None:
        self._entita = entita
        self.attributo = attributo
        self.modello = modello
        self.validatore = validatore
        self.aggiorna = aggiorna
        self.none_su_errore = none_su_errore

    @callback
    def prepara(self) -> None:
        """Senza ``aggiorna`` il risultato va nell'attributo, che deve esserci."""
        if self.aggiorna:
            return
        if not hasattr(self._entita, self.attributo):
            raise AttributeError(f"Attribute '{self.attributo}' does not exist.")
        self.aggiorna = self._scrivi

    @callback
    def _scrivi(self, risultato: Any) -> None:
        valore = None if isinstance(risultato, TemplateError) else risultato
        setattr(self._entita, self.attributo, valore)

    @callback
    def risultato(
        self,
        evento: Event[EventStateChangedData] | None,
        modello: Template,
        ultimo: Any,
        risultato: Any,
    ) -> None:
        """Un nuovo risultato del modello (``handle_result``)."""
        if isinstance(risultato, TemplateError):
            _LOGGER.error(
                (
                    "TemplateError('%s') "
                    "while processing template '%s' "
                    "for attribute '%s' in entity '%s'"
                ),
                risultato,
                self.modello,
                self.attributo,
                self._entita.entity_id,
            )
            if self.none_su_errore:
                self._scrivi(risultato)
            else:
                assert self.aggiorna
                self.aggiorna(risultato)
            return

        if not self.validatore:
            assert self.aggiorna
            self.aggiorna(risultato)
            return

        try:
            validato = self.validatore(risultato)
        except probatio.Invalid as errore:
            _errore_di_validazione(
                risultato, self.modello, self.attributo, self._entita.entity_id, errore
            )
            assert self.aggiorna
            self.aggiorna(None)
            return

        assert self.aggiorna
        self.aggiorna(validato)


class EntitaModello(Entity):
    """La parte comune dei sensori calcolati: i modelli, come li segue e li scrive
    (``AbstractTemplateEntity`` e ``TemplateEntity`` di Home Assistant). Le classi delle
    entità la mettono prima delle classi di Home Assistant, con ``RestoreEntity`` dove
    la mettono i sensori template (stesso ordine delle classi)."""

    # da RestoreEntity, nelle classi delle entità
    async_get_last_state: Callable[[], Awaitable[State | None]]

    _formato_entity_id: str
    _chiavi: frozenset[str]
    # gli attributi che, se hanno già un valore, impediscono di ripristinare lo stato
    _proprieta_ripristinate: tuple[str, ...]

    _attr_available = True
    _attr_entity_picture = None
    _attr_icon = None
    _attr_should_poll = False

    def __init__(
        self,
        hass: HomeAssistant,
        config: Mapping[str, Any],
        unique_id: str | None,
        *,
        segui: Seguire = traccia_modelli,
    ) -> None:
        if altre := set(config) - self._chiavi:
            raise ValueError(
                f"{type(self).__name__}: chiavi della configurazione non gestite: "
                f"{sorted(altre)}"
            )
        if not isinstance(config.get(CONF_STATE), Template):
            raise TypeError(f"{type(self).__name__}: «{CONF_STATE}» senza modello")
        self.hass = hass
        self._config = config
        self._segui = segui
        self._modelli: dict[str, ModelloDellEntita] = {}
        self._attr_extra_state_attributes = {}

        if (default_entity_id := config.get(CONF_DEFAULT_ENTITY_ID)) is not None:
            _, _, oggetto = default_entity_id.partition(".")
            self.entity_id = async_generate_entity_id(
                self._formato_entity_id, oggetto, hass=self.hass
            )

        self._attributi: dict[Template, list[AttributoDelModello]] = {}
        self._seguiti: Seguiti | None = None
        self._pulizia_registrata = False
        self._autoriferimenti = 0
        self._attr_unique_id = unique_id
        self._modello_disponibilita: Template | None = config.get(CONF_AVAILABILITY)

        variabili = {"this": _StatoFittizio()}

        self._aggiungi_modello(
            CONF_AVAILABILITY, "_attr_available", aggiorna=self._aggiorna_disponibile
        )

        # nome e icona si rendono subito: il nome perché fa l'entity_id, l'icona perché
        # ci sia anche con l'entità non disponibile
        self._attr_name = None
        for opzione, attributo, validatore in (
            (CONF_ICON, "_attr_icon", probatio.Or(cv.whitespace, cv.icon)),
            (CONF_NAME, "_attr_name", cv.string),
        ):
            if modello := self._aggiungi_modello(
                opzione,
                attributo,
                validatore,
                aggiungi_se_statico=opzione != CONF_NAME,
            ):
                with contextlib.suppress(TemplateError):
                    setattr(
                        self,
                        attributo,
                        modello.async_render(variables=variabili, parse_result=False),
                    )

    # --- modelli della configurazione ------------------------------------------------------

    def _aggiungi_modello(
        self,
        opzione: str,
        attributo: str,
        validatore: Callable[[Any], Any] | None = None,
        aggiorna: Callable[[Any], None] | None = None,
        none_su_errore: bool = False,
        aggiungi_se_statico: bool = True,
    ) -> Template | None:
        """Il modello dell'opzione, se c'è, da seguire per l'attributo (``add_template``)."""
        if (modello := self._config.get(opzione)) and isinstance(modello, Template):
            if aggiungi_se_statico or not modello.is_static:
                self._modelli[opzione] = ModelloDellEntita(
                    attributo, modello, validatore, aggiorna, none_su_errore
                )
            return modello
        return None

    def _prepara_modello_dello_stato(
        self,
        attributo: str,
        validatore: Callable[[Any], Any] | None = None,
        aggiorna: Callable[[Any], None] | None = None,
    ) -> None:
        """Il modello dello stato (``setup_state_template``): un errore lo rende
        sconosciuto e, senza modello della disponibilità, l'entità non disponibile."""

        @callback
        def _aggiorna_stato(risultato: Any) -> None:
            if isinstance(risultato, TemplateError):
                setattr(self, attributo, None)
                if self._modello_disponibilita:
                    return
                self._attr_available = False
                return

            # di nuovo disponibile dopo un errore
            if not self._modello_disponibilita and not self._attr_available:
                self._attr_available = True

            stato = validatore(risultato) if validatore else risultato

            if aggiorna:
                aggiorna(stato)
            else:
                setattr(self, attributo, stato)

        self._aggiungi_modello(
            CONF_STATE, attributo, aggiorna=_aggiorna_stato, none_su_errore=False
        )

    @callback
    def _aggiorna_disponibile(self, risultato: Any) -> None:
        if isinstance(risultato, TemplateError):
            self._attr_available = True
            return
        self._attr_available = result_as_boolean(risultato)

    @callback
    def _prepara_attributi(self) -> None:
        """Un attributo per ogni modello, nell'ordine della configurazione
        (``_async_setup_templates``)."""
        for voce in self._modelli.values():
            if self.hass is None:
                raise ValueError("hass cannot be None")
            if voce.modello.hass is None:
                raise ValueError("template.hass cannot be None")
            self._attributi.setdefault(voce.modello, []).append(
                AttributoDelModello(
                    self,
                    voce.attributo,
                    voce.modello,
                    voce.validatore,
                    voce.aggiorna,
                    voce.none_su_errore,
                )
            )

    # --- come segue i modelli ----------------------------------------------------------------

    @callback
    def _risultati(
        self,
        evento: Event[EventStateChangedData] | None,
        aggiornamenti: list[TrackTemplateResult],
    ) -> None:
        """I nuovi risultati negli attributi, poi lo stato scritto subito
        (``_handle_results``)."""
        if evento:
            self.async_set_context(evento.context)

        entity_id = evento and evento.data["entity_id"]

        if entity_id and entity_id == self.entity_id:
            self._autoriferimenti += 1
        else:
            self._autoriferimenti = 0

        if self._autoriferimenti > len(self._attributi):
            for aggiornamento in aggiornamenti:
                _LOGGER.warning(
                    (
                        "Template loop detected while processing event: %s, skipping"
                        " template render for Template[%s]"
                    ),
                    evento,
                    aggiornamento.template.template,
                )
            return

        for aggiornamento in aggiornamenti:
            for attributo in self._attributi[aggiornamento.template]:
                attributo.risultato(
                    evento,
                    aggiornamento.template,
                    aggiornamento.last_result,
                    aggiornamento.result,
                )

        self.async_write_ha_state()

    @callback
    def _avvia_modelli(
        self,
        _hass: HomeAssistant | None,
        log_fn: Callable[[int, str], None] | None = None,
    ) -> None:
        """Comincia a seguire i modelli e li rende tutti (``_async_template_startup``): il
        modello della disponibilità per primo, gli altri nell'ordine della
        configurazione."""
        da_seguire: list[TrackTemplate] = []
        con_disponibilita = False

        variabili = {"this": TemplateStateFromEntityId(self.hass, self.entity_id)}

        for modello, attributi in self._attributi.items():
            seguito = TrackTemplate(modello, variabili)
            e_disponibilita = False
            for attributo in attributi:
                if attributo.attributo == "_attr_available":
                    con_disponibilita = True
                    e_disponibilita = True
                attributo.prepara()
            if e_disponibilita:
                da_seguire.insert(0, seguito)
            else:
                da_seguire.append(seguito)

        seguiti = self._segui(
            self.hass,
            da_seguire,
            self._risultati,
            log_fn=log_fn,
            has_super_template=con_disponibilita,
        )
        self._seguiti = seguiti
        # si riparte anche quando cambia l'entity_id: la pulizia si registra una volta
        if not self._pulizia_registrata:
            self._pulizia_registrata = True
            self.async_on_remove(self._smetti_di_seguire)
        seguiti.async_refresh()

    @callback
    def _smetti_di_seguire(self) -> None:
        self._pulizia_registrata = False
        if self._seguiti is not None:
            self._seguiti.async_remove()

    # --- ripristino ----------------------------------------------------------------------

    async def _ultimi_dati(self) -> Any:
        """I dati in più dell'ultimo stato (``_async_get_last_template_data``)."""
        return _NESSUN_DATO

    def _ripristina_stato(self, ultimo: State) -> bool:
        return True

    def _ripristina_dati(self, dati: Any) -> None:
        """I dati in più ripristinati (``restore_extra_data``)."""

    async def _ripristina(self) -> None:
        """Lo stato di prima del riavvio, se l'entità non ne ha già uno
        (``async_restore_last_state``)."""
        if (ultimo := await self.async_get_last_state()) is None:
            return

        dati = await self._ultimi_dati()

        if (
            dati is None
            or ultimo.state in (STATE_UNKNOWN, STATE_UNAVAILABLE)
            or any(getattr(self, a) is not None for a in self._proprieta_ripristinate)
        ):
            return

        if not self._ripristina_stato(ultimo):
            return

        # icona e nome della configurazione, poi gli attributi (nessun modello)
        for chiave, attributo_stato, attributo in (
            (CONF_ICON, ATTR_ICON, "_attr_icon"),
            (CONF_NAME, ATTR_FRIENDLY_NAME, "_attr_name"),
        ):
            if chiave not in self._config or attributo_stato not in ultimo.attributes:
                continue
            setattr(self, attributo, ultimo.attributes[attributo_stato])

        self._attr_extra_state_attributes = {}

        if dati is not _NESSUN_DATO:
            self._ripristina_dati(dati)

    # --- Home Assistant ----------------------------------------------------------------------

    async def async_added_to_hass(self) -> None:
        """I modelli si seguono all'avvio di Home Assistant (subito se è già avviato),
        poi lo stato di prima del riavvio."""
        await super().async_added_to_hass()
        self._prepara_attributi()
        async_at_start(self.hass, self._avvia_modelli)
        await self._ripristina()

    @callback
    def async_entity_id_changed(self, old_entity_id: str) -> None:
        """Nuovo entity_id: ``this`` dei modelli era il vecchio, si riparte. Lo stato si
        scrive prima: ``this.state`` deve esserci quando i modelli si rendono."""
        super().async_entity_id_changed(old_entity_id)
        self.async_write_ha_state()
        if self._seguiti is None:
            # non ancora partito: partirà con il nuovo entity_id
            return
        self._seguiti.async_remove()
        self._avvia_modelli(None)

    async def async_update(self) -> None:
        """Aggiornamento chiesto (``homeassistant.update_entity``): i modelli si
        ricalcolano."""
        assert self._seguiti
        self._seguiti.async_refresh()


class SensoreModello(EntitaModello, RestoreSensor):
    """Un sensore calcolato della VMC (``StateSensorEntity`` di Home Assistant)."""

    _formato_entity_id = FORMATO_SENSORE
    _chiavi = CHIAVI_SENSORE
    _proprieta_ripristinate = ("_attr_native_value",)

    def __init__(
        self,
        hass: HomeAssistant,
        config: Mapping[str, Any],
        unique_id: str | None,
        *,
        segui: Seguire = traccia_modelli,
    ) -> None:
        if (
            try_parse_enum(SensorDeviceClass, config.get(CONF_DEVICE_CLASS))
            in _CLASSI_CON_DATA
        ):
            raise ValueError(
                f"{type(self).__name__}: classe «{config.get(CONF_DEVICE_CLASS)}» "
                "non gestita"
            )
        super().__init__(hass, config, unique_id, segui=segui)
        self._attr_native_unit_of_measurement = config.get(CONF_UNIT_OF_MEASUREMENT)
        self._attr_device_class = config.get(CONF_DEVICE_CLASS)
        self._attr_state_class = config.get(CONF_STATE_CLASS)
        self._attr_last_reset = None
        self._prepara_modello_dello_stato("_attr_native_value", self._valida_stato)

    def _numerico_atteso(self) -> bool:
        """Se lo stato deve essere un numero (come ``SensorEntity``): classe numerica e
        una tra classe di stato, unità, precisione o classe. Qui basta sapere se l'unità
        c'è: la correzione delle unità ambigue non toglie mai l'unità."""
        classe = try_parse_enum(SensorDeviceClass, self.device_class)
        if classe in NON_NUMERIC_DEVICE_CLASSES:
            return False
        if (
            self.state_class is not None
            or self.native_unit_of_measurement is not None
            or self.suggested_display_precision is not None
        ):
            return True
        return classe is not None

    def _valida_stato(self, risultato: Any) -> StateType:
        """Lo stato reso (``_validate_state``): un numero se il sensore è numerico."""
        if self._numerico_atteso():
            if not isinstance(risultato, bool) and isinstance(risultato, (int, float)):
                return risultato
            return self._numero(risultato)
        return risultato

    def _numero(self, risultato: Any) -> float | None:
        """Il risultato come numero, o None con un errore nel registro (``number``)."""
        if risultato is None:
            return None
        if type(risultato) is not bool:
            try:
                return probatio.Coerce(float)(risultato)
            except probatio.Invalid:
                pass
        _LOGGER.error(
            f"Received invalid {self.entity_id.split('.')[0]} {CONF_STATE}"
            f": {risultato} for entity {self.entity_id}, %s",
            "expected a number",
        )
        return None

    async def _ultimi_dati(self) -> Any:
        if (dati := await self.async_get_last_extra_data()) is None:
            return None
        return SensorExtraStoredData.from_dict(dati.as_dict())

    def _ripristina_dati(self, dati: SensorExtraStoredData) -> None:
        # l'unità no: è sempre quella della configurazione
        self._attr_native_value = dati.native_value


class BinarioModello(EntitaModello, BinarySensorEntity, RestoreEntity):
    """Un sensore binario calcolato della VMC (``StateBinarySensorEntity`` di Home
    Assistant), con il ritardo ``delay_on`` (anche reso da un modello)."""

    _formato_entity_id = FORMATO_BINARIO
    _chiavi = CHIAVI_BINARIO
    _proprieta_ripristinate = ("_attr_is_on",)

    def __init__(
        self,
        hass: HomeAssistant,
        config: Mapping[str, Any],
        unique_id: str | None,
        *,
        segui: Seguire = traccia_modelli,
    ) -> None:
        super().__init__(hass, config, unique_id, segui=segui)
        self._attr_device_class = None
        # «_delay_on» come in Home Assistant: è anche nei messaggi d'errore del modello
        self._delay_on: timedelta | None = None
        self._annulla_ritardo: CALLBACK_TYPE | None = None

        self._prepara_modello_dello_stato("_attr_is_on", aggiorna=self._aggiorna_stato)
        try:
            self._delay_on = cv.positive_time_period(config.get(CONF_DELAY_ON))
        except probatio.Invalid:
            self._aggiungi_modello(
                CONF_DELAY_ON,
                "_delay_on",
                cv.positive_time_period,
                none_su_errore=True,
            )
        # un ritardo in corso finisce con l'entità
        self.async_on_remove(self._ferma_ritardo)

    @callback
    def _ferma_ritardo(self) -> None:
        if self._annulla_ritardo:
            self._annulla_ritardo()

    def _ripristina_stato(self, ultimo: State) -> bool:
        self._attr_is_on = ultimo.state == STATE_ON
        return True

    @callback
    def _aggiorna_stato(self, risultato: Any) -> None:
        """Il nuovo stato, subito o dopo ``delay_on`` se diventa acceso; un nuovo
        risultato annulla il ritardo in corso."""
        if self._annulla_ritardo:
            self._annulla_ritardo()
            self._annulla_ritardo = None

        stato: bool | None = None
        if risultato is not None and not isinstance(risultato, TemplateError):
            stato = result_as_boolean(risultato)

        if stato == self._attr_is_on:
            return

        # senza ritardo (nessun «delay_off» nei sensori della VMC: spento è subito)
        if not stato or not self._delay_on:
            self._attr_is_on = stato
            return

        @callback
        def _scrivi_stato(_: Any) -> None:
            self._attr_is_on = stato
            self.async_write_ha_state()

        # con ritardo: annullato se il risultato cambia
        self._annulla_ritardo = async_call_later(
            self.hass, self._delay_on.total_seconds(), _scrivi_stato
        )
