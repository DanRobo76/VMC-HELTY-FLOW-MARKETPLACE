"""La memoria interna del motore (fase 4): i 68 valori con stato che non sono entità.

Oggi 68 aiutanti del package (32 ``input_number``, 35 ``input_text``, 1
``input_boolean``) servono solo alle automazioni: contatori dell'aria scambiata, tempi
di attesa, conti alla rovescia, ultime scelte. Un'integrazione del catalogo non può
escludere le proprie entità dal registro di Home Assistant (e un contatore dell'aria
cambia ogni secondo mentre la VMC gira): domani questi valori non sono entità e stanno
qui, una memoria per VMC, salvata con ``Store``. Le chiavi sono quelle di ``StatoVMC``
(l'entity_id di oggi senza «vmc_<nome>_», per esempio ``input_number.attesa_avvisi``).

Le regole sono quelle degli aiutanti di oggi (Home Assistant 2026.11):

- ogni valore è uno ``State`` di Home Assistant con l'entity_id di oggi, con stato,
  attributi, ``last_changed``, ``last_updated``, ``last_reported`` e contesto calcolati
  come ``StateMachine.async_set_internal`` (stesso stato e stessi attributi: cambia solo
  ``last_reported``); un numero si scrive come un float (``"5.0"``);
- le scritture sono i servizi degli aiutanti (``input_number.set_value``,
  ``input_text.set_value``, ``input_boolean.turn_on``/``turn_off``/``toggle``) con lo
  stesso schema, gli stessi limiti, gli stessi errori e gli stessi avvisi, eseguiti da
  ``entity_service_call`` di Home Assistant su questi valori: contesto della chiamata,
  ordine dei bersagli e un compito per bersaglio come per le entità; manca solo
  l'evento ``call_service`` (che il registro salverebbe);
- le letture dei modelli del motore passano da ``hass_modelli``: lo stesso motore dei
  modelli di Home Assistant su una macchina degli stati che vede anche questi valori,
  così ``states()``, ``is_state()``, ``state_attr()``, ``states.d.o``, ``has_value``,
  ``expand``, ``last_changed``... e le letture annotate (``RenderInfo``) per trigger e
  attese sono quelle di sempre;
- ogni scrittura si annuncia nello stesso punto del bus in cui Home Assistant manda
  ``state_changed`` (o ``state_reported``, o ``call_service`` per la chiamata): un
  evento ``state_reported`` con un marchio, che non arriva agli ascoltatori di tutti
  gli eventi (registro compreso) e che nessun trigger ``event`` può ascoltare. Chi lo
  riceve consegna il cambio a chi segue l'entità come un'entità vera (trigger ``state``
  e ``template``, attese, modelli: le iscrizioni di ``seguire.CambiInterni``, di cui la
  memoria è una sorgente), poi allo ``StatoVMC`` e a chi ascolta la memoria. Così istanti e ordine restano quelli
  degli aiutanti, anche quando la scrittura avviene mentre il bus consegna un altro
  evento (la consegna si accoda come quella di ``state_changed``).

All'avvio i valori si ripristinano con le regole degli aiutanti (``ripristina``): con
``initial`` non si ripristina nulla (i 5 testi che oggi ripartono vuoti), un numero
fuori dai limiti torna al minimo, un testo di lunghezza sbagliata resta «unknown».
"""

from __future__ import annotations

import logging
import re
import time
from collections import ChainMap
from collections.abc import Callable, Iterable, Iterator, Mapping
from itertools import chain
from typing import TYPE_CHECKING, Any

import probatio
from homeassistant.components import input_boolean, input_number, input_text
from homeassistant.const import (
    EVENT_HOMEASSISTANT_STOP,
    EVENT_STATE_CHANGED,
    EVENT_STATE_REPORTED,
    MAX_LENGTH_STATE_STATE,
    STATE_OFF,
    STATE_ON,
    STATE_UNKNOWN,
)
from homeassistant.core import (
    CALLBACK_TYPE,
    Context,
    Event,
    EventOrigin,
    HassJob,
    HassJobType,
    HomeAssistant,
    ServiceCall,
    State,
    callback,
    get_hassjob_callable_job_type,
)
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity import CONTEXT_RECENT_TIME_SECONDS, FLOAT_PRECISION
from homeassistant.helpers.service import entity_service_call
from homeassistant.helpers.storage import Store
from homeassistant.util import dt as dt_util
from homeassistant.util.ulid import ulid_at_time

from ...trasforma import rinomina
from ..tabelle import IMPOSTAZIONI
from .seguire import cambi_interni
from .stati_logiche import stati_logiche

if TYPE_CHECKING:
    from ..stato import StatoVMC

_LOGGER = logging.getLogger(__name__)

# I 68 valori interni (colonna «Domani» della fase 1: «interna (stato del motore)»),
# per dominio e nell'ordine del package: l'ordine conta per le scritture a più
# bersagli, che Home Assistant esegue nell'ordine dell'insieme dei bersagli costruito
# dall'elenco delle entità del dominio.
INTERNI: tuple[str, ...] = (
    "input_boolean.spia_umidita_mantenuta_velocita_0",
    "input_number.aria_scambiata_v1",
    "input_number.aria_scambiata_v2",
    "input_number.aria_scambiata_v3",
    "input_number.aria_scambiata_v4",
    "input_number.aria_scambiata_iperventilazione",
    "input_number.aria_scambiata_notte",
    "input_number.aria_scambiata_freecooling",
    "input_number.aria_scambiata_ricomincio",
    "input_number.attesa_pdr_cambio",
    "input_number.attesa_pdr_cambio_inquinanti",
    "input_number.attesa_pdr_ripristino",
    "input_number.attesa_pdr_ripristino_inquinanti",
    "input_number.attesa_free_sospensione",
    "input_number.attesa_free_sospensione_inquinanti",
    "input_number.attesa_free_ripristino",
    "input_number.attesa_free_ripristino_inquinanti",
    "input_number.attesa_blackout_rilevazione",
    "input_number.attesa_blackout_ripristino",
    "input_number.attesa_calendario_inizio",
    "input_number.attesa_calendario_fine",
    "input_number.attesa_avvisi",
    "input_number.attesa_inquinanti_avvio",
    "input_number.attesa_inquinanti_avvio_spia_pdr",
    "input_number.attesa_inquinanti_fine",
    "input_number.attesa_inquinanti_memoria",
    "input_number.attesa_free_annullamento",
    "input_number.attesa_umidita_avvio",
    "input_number.attesa_umidita_fine",
    "input_number.attesa_umidita_memoria",
    "input_number.attesa_delta_avvio",
    "input_number.attesa_delta_fine",
    "input_number.attesa_delta_memoria",
    "input_text.ip_insert_esito",
    "input_text.last_temp_external_entity",
    "input_text.last_temp_internal_entity",
    "input_text.last_humidity_external_entity",
    "input_text.last_humidity_internal_entity",
    "input_text.last_co2_internal_entity",
    "input_text.last_notification_device",
    "input_text.tempo_mancante_reset",
    "input_text.velocita_precedente",
    "input_text.last_media_player_entity",
    "input_text.countdown_pdr_cambio",
    "input_text.countdown_pdr_ripristino",
    "input_text.countdown_free_heating_annullamento",
    "input_text.countdown_free_heating_sospensione",
    "input_text.countdown_free_heating_ripristino",
    "input_text.countdown_free_cooling_annullamento",
    "input_text.countdown_free_cooling_sospensione",
    "input_text.countdown_free_cooling_ripristino",
    "input_text.countdown_inquinanti_avvio",
    "input_text.countdown_inquinanti_fine",
    "input_text.countdown_inquinanti_memoria",
    "input_text.countdown_umidita_avvio",
    "input_text.countdown_umidita_fine",
    "input_text.countdown_umidita_memoria",
    "input_text.countdown_delta_avvio",
    "input_text.countdown_delta_fine",
    "input_text.countdown_delta_memoria",
    "input_text.countdown_blackout_rilevazione",
    "input_text.countdown_blackout_ripristino",
    "input_text.countdown_calendario_inizio",
    "input_text.countdown_calendario_fine",
    "input_text.countdown_avvisi",
    "input_text.ultima_scelta_utente",
    "input_text.ultimi_comandi_automazione",
    "input_text.ultime_letture_velocita",
)

# Archivio di una VMC (``.storage/vmc_master.memoria_interna.<nome>``).
CHIAVE_ARCHIVIO = "vmc_master.memoria_interna.{nome}"
VERSIONE_ARCHIVIO = 1
# Dopo un cambio la memoria si salva entro questo ritardo (s): come gli aiutanti di
# oggi, che Home Assistant salva ogni 15 minuti (restore_state) e alla chiusura.
RITARDO_SALVATAGGIO = 900

# La chiave del marchio negli eventi che annunciano una scrittura.
_MARCHIO = "vmc_master_memoria_interna"

_SCHEMI_CONFIG: dict[str, Any] = {
    "input_boolean": input_boolean.CONFIG_SCHEMA,
    "input_number": input_number.CONFIG_SCHEMA,
    "input_text": input_text.CONFIG_SCHEMA,
}


# --- i valori ------------------------------------------------------------------------------


class _Valore:
    """Un valore interno come lo vede ``entity_service_call``: le parti di ``Entity``
    che usa (disponibilità, contesto, richiesta della chiamata, tipo dei metodi)."""

    should_poll = False
    available = True
    dominio = ""

    def __init__(
        self, memoria: MemoriaInterna, chiave: str, config: Mapping[str, Any]
    ) -> None:
        self._memoria = memoria
        self.chiave = chiave
        self.entity_id = memoria.entity_id(chiave)
        nome = config.get("name")
        if nome is not None and memoria.nome != "master":
            nome = rinomina(nome, memoria.nome)
        self.nome: str | None = nome
        self.icona: str | None = config.get("icon")
        self._contesto: Context | None = None
        self._contesto_impostato: float | None = None

    # --- come Entity --------------------------------------------------------------------

    @callback
    def async_set_context(self, context: Context) -> None:
        """Il contesto della chiamata in corso (come ``Entity.async_set_context``)."""
        self._contesto = context
        self._contesto_impostato = time.time()

    async def async_request_call[T](self, coro: Any) -> T:
        """Come ``Entity.async_request_call`` senza aggiornamenti in parallelo."""
        return await coro  # type: ignore[no-any-return]

    def get_hassjob_type(self, function_name: str) -> HassJobType:
        """Il tipo del metodo di un servizio (come ``Entity.get_hassjob_type``)."""
        return get_hassjob_callable_job_type(getattr(self, function_name))

    # --- stato --------------------------------------------------------------------------

    def calcola(self) -> tuple[str, dict[str, Any]]:
        """Stato e attributi come li scrive l'aiutante di oggi."""
        raise NotImplementedError

    def _attributi_comuni(self, attributi: dict[str, Any]) -> dict[str, Any]:
        """Icona e nome dopo gli attributi propri (come ``Entity``)."""
        if self.icona is not None:
            attributi["icon"] = self.icona
        if self.nome:
            attributi["friendly_name"] = self.nome
        return attributi

    def ripristina(self, salvato: Any) -> None:
        """Il valore all'avvio dal valore salvato (o None), come l'aiutante."""
        raise NotImplementedError

    def salvato(self) -> Any:
        """Il valore da salvare."""
        raise NotImplementedError

    @callback
    def _scrivi(self) -> None:
        """Come ``Entity._async_write_ha_state``: un contesto vecchio di più di 5 s non
        vale più."""
        stato, attributi = self.calcola()
        adesso = time.time()
        if (
            self._contesto_impostato is not None
            and adesso - self._contesto_impostato > CONTEXT_RECENT_TIME_SECONDS
        ):
            self._contesto = None
            self._contesto_impostato = None
        self._memoria._imposta(self, stato, attributi, self._contesto, adesso)


class _Numero(_Valore):
    """Un ``input_number`` di oggi (senza classe di dispositivo: nessuna conversione)."""

    dominio = "input_number"

    def __init__(
        self, memoria: MemoriaInterna, chiave: str, config: Mapping[str, Any]
    ) -> None:
        super().__init__(memoria, chiave, config)
        self.minimo: float = config["min"]
        self.massimo: float = config["max"]
        self.passo: float = config["step"]
        self.modo: str = config["mode"]
        self.unita: str | None = config.get("unit_of_measurement")
        self.iniziale: float | None = config.get("initial")
        self.valore: float | None = self.iniziale

    # come NumberEntity, per il servizio set_value
    @property
    def min_value(self) -> float:
        return self.minimo

    @property
    def max_value(self) -> float:
        return self.massimo

    @property
    def native_min_value(self) -> float:
        return self.minimo

    @property
    def native_max_value(self) -> float:
        return self.massimo

    def convert_to_native_value(self, value: float) -> float:
        return value

    async def async_set_native_value(self, value: float) -> None:
        """Come ``InputNumber.async_set_native_value``."""
        self.valore = float(value)
        self._scrivi()

    def calcola(self) -> tuple[str, dict[str, Any]]:
        stato = (
            STATE_UNKNOWN
            if self.valore is None
            else f"{self.valore:.{FLOAT_PRECISION}}"
        )
        attributi: dict[str, Any] = {
            "min": self.minimo,
            "max": self.massimo,
            "step": self.passo,
            "mode": self.modo,
            "initial": self.iniziale,
            "editable": False,
        }
        if self.unita is not None:
            attributi["unit_of_measurement"] = self.unita
        return stato, self._attributi_comuni(attributi)

    def ripristina(self, salvato: Any) -> None:
        """Come ``InputNumber.async_added_to_hass``: con ``initial`` nessun ripristino,
        un valore fuori dai limiti (o nessuno) diventa il minimo."""
        self.valore = self.iniziale
        if self.valore is not None:
            return
        valore = (
            float(salvato)
            if isinstance(salvato, (int, float)) and not isinstance(salvato, bool)
            else None
        )
        if valore is not None and self.minimo <= valore <= self.massimo:
            self.valore = valore
        else:
            self.valore = self.minimo

    def salvato(self) -> Any:
        return self.valore


class _Testo(_Valore):
    """Un ``input_text`` di oggi."""

    dominio = "input_text"

    def __init__(
        self, memoria: MemoriaInterna, chiave: str, config: Mapping[str, Any]
    ) -> None:
        super().__init__(memoria, chiave, config)
        self.minimo: int = config["min"]
        self.massimo: int = config["max"]
        self.modo: str = config["mode"]
        self.pattern: str | None = config.get("pattern")
        self._pattern = None if self.pattern is None else re.compile(self.pattern)
        self.unita: str | None = config.get("unit_of_measurement")
        self.iniziale: str | None = config.get("initial")
        self.valore: str | None = self.iniziale

    async def async_set_value(self, value: str) -> None:
        """Come ``InputText.async_set_value``: un testo non valido si annota e si
        ignora."""
        if len(value) < self.minimo or len(value) > self.massimo:
            _LOGGER.warning(
                "Invalid value: %s (length range %s - %s)",
                value,
                self.minimo,
                self.massimo,
            )
            return
        if self._pattern is not None and not self._pattern.match(value):
            _LOGGER.warning(
                "Invalid value: %s (does not match pattern %s)", value, self.pattern
            )
            return
        self.valore = value
        self._scrivi()

    def calcola(self) -> tuple[str, dict[str, Any]]:
        stato = STATE_UNKNOWN if self.valore is None else self.valore
        attributi: dict[str, Any] = {
            "mode": self.modo,
            "min": max(self.minimo, 0),
            "max": min(self.massimo, MAX_LENGTH_STATE_STATE),
            "pattern": self.pattern,
            "editable": False,
        }
        if self.unita is not None:
            attributi["unit_of_measurement"] = self.unita
        return stato, self._attributi_comuni(attributi)

    def ripristina(self, salvato: Any) -> None:
        """Come ``InputText.async_added_to_hass``: con ``initial`` nessun ripristino,
        un testo di lunghezza sbagliata (o nessuno) lascia il valore sconosciuto."""
        self.valore = self.iniziale
        if self.valore is not None:
            return
        if isinstance(salvato, str) and self.minimo <= len(salvato) <= self.massimo:
            self.valore = salvato

    def salvato(self) -> Any:
        return self.valore


class _Interruttore(_Valore):
    """Un ``input_boolean`` di oggi."""

    dominio = "input_boolean"

    def __init__(
        self, memoria: MemoriaInterna, chiave: str, config: Mapping[str, Any]
    ) -> None:
        super().__init__(memoria, chiave, config)
        self.iniziale: bool | None = config.get("initial")
        self.is_on: bool = bool(self.iniziale)

    async def async_turn_on(self, **kwargs: Any) -> None:
        self.is_on = True
        self._scrivi()

    async def async_turn_off(self, **kwargs: Any) -> None:
        self.is_on = False
        self._scrivi()

    async def async_toggle(self, **kwargs: Any) -> None:
        """Come ``ToggleEntity.async_toggle``."""
        if self.is_on:
            await self.async_turn_off(**kwargs)
        else:
            await self.async_turn_on(**kwargs)

    def calcola(self) -> tuple[str, dict[str, Any]]:
        stato = STATE_ON if self.is_on else STATE_OFF
        return stato, self._attributi_comuni({"editable": False})

    def ripristina(self, salvato: Any) -> None:
        """Come ``InputBoolean.async_added_to_hass``: con ``initial`` nessun
        ripristino, altrimenti acceso solo se era acceso."""
        if self.iniziale is not None:
            self.is_on = self.iniziale
            return
        self.is_on = salvato is True

    def salvato(self) -> Any:
        return self.is_on


_TIPI: dict[str, type[_Valore]] = {
    "input_boolean": _Interruttore,
    "input_number": _Numero,
    "input_text": _Testo,
}


async def _imposta_numero(entity: _Numero, service_call: ServiceCall) -> None:
    """Come ``input_number.services._async_set_value``."""
    value = service_call.data["value"]
    if value < entity.min_value or value > entity.max_value:
        raise probatio.Invalid(
            f"Invalid value for {entity.entity_id}: {value} (range "
            f"{entity.min_value} - {entity.max_value})"
        )
    native_value = entity.convert_to_native_value(value)
    await entity.async_set_native_value(
        min(max(native_value, entity.native_min_value), entity.native_max_value)
    )


# I servizi degli aiutanti sui valori interni: (schema, funzione) come li registrano
# input_number, input_text e input_boolean (schema da entity service, funzione o nome
# del metodo).
SERVIZI: dict[tuple[str, str], tuple[Any, str | HassJob[..., Any]]] = {
    ("input_number", "set_value"): (
        cv.make_entity_service_schema(
            {probatio.Required("value"): probatio.Coerce(float)}
        ),
        HassJob(_imposta_numero),
    ),
    ("input_text", "set_value"): (
        cv.make_entity_service_schema({probatio.Required("value"): cv.string}),
        "async_set_value",
    ),
    ("input_boolean", "turn_on"): (
        cv.make_entity_service_schema(None),
        "async_turn_on",
    ),
    ("input_boolean", "turn_off"): (
        cv.make_entity_service_schema(None),
        "async_turn_off",
    ),
    ("input_boolean", "toggle"): (cv.make_entity_service_schema(None), "async_toggle"),
}


# --- le letture dei modelli ------------------------------------------------------------------


class _Unione(Mapping[str, State]):
    """Gli stati di Home Assistant seguiti dai valori interni: quello che il motore dei
    modelli scorre per ``states`` di un dominio o di tutti (``_state_generator`` scorre
    ``states._states.values()`` della macchina degli stati che gli si dà). Gli stati di
    Home Assistant con le funzioni pubbliche della macchina degli stati, nello stesso
    ordine."""

    __slots__ = ("_interni", "_veri")

    def __init__(self, veri: Any, interni: Mapping[str, State]) -> None:
        self._veri = veri
        self._interni = interni

    def __getitem__(self, chiave: str) -> State:
        if (stato := self._interni.get(chiave)) is not None:
            return stato
        if (stato := self._veri.get(chiave)) is not None and stato.entity_id == chiave:
            return stato  # type: ignore[no-any-return]
        raise KeyError(chiave)

    def __iter__(self) -> Iterator[str]:
        return chain(self._veri.async_entity_ids(), self._interni)

    def __len__(self) -> int:
        return self._veri.async_entity_ids_count() + len(self._interni)  # type: ignore[no-any-return]

    def values(self) -> Any:
        return [*self._veri.async_all(), *self._interni.values()]


class StatiConMemoria:
    """La macchina degli stati come la vedono i modelli del motore: gli stati di Home
    Assistant più i valori interni, che nella macchina degli stati non ci sono.

    Ha le parti che usa il motore dei modelli (``get``, ``async_all``,
    ``async_entity_ids_count``, ``_states``); il resto è quello della macchina degli
    stati. Scorrendo un dominio o tutti gli stati i valori interni vengono dopo gli
    altri (oggi sono mescolati nell'ordine di creazione): nessun modello del package
    scorre i domini degli aiutanti o tutti gli stati."""

    __slots__ = ("_interni", "_veri")

    def __init__(self, veri: Any, interni: Mapping[str, State]) -> None:
        self._veri = veri
        self._interni = interni

    def get(self, entity_id: str) -> State | None:
        """Come ``StateMachine.get`` (anche con le maiuscole)."""
        if (stato := self._interni.get(entity_id)) is not None:
            return stato
        if (stato := self._veri.get(entity_id)) is not None:
            return stato
        return self._interni.get(entity_id.lower())

    def is_state(self, entity_id: str, state: str) -> bool:
        return (stato := self.get(entity_id)) is not None and stato.state == state

    def _interni_di(self, domain_filter: str | Iterable[str] | None) -> list[State]:
        if domain_filter is None:
            return list(self._interni.values())
        domini = (
            {domain_filter.lower()}
            if isinstance(domain_filter, str)
            else {d.lower() for d in domain_filter}
        )
        return [s for s in self._interni.values() if s.domain in domini]

    def async_all(
        self, domain_filter: str | Iterable[str] | None = None
    ) -> list[State]:
        return [*self._veri.async_all(domain_filter), *self._interni_di(domain_filter)]

    def async_entity_ids(
        self, domain_filter: str | Iterable[str] | None = None
    ) -> list[str]:
        return [
            *self._veri.async_entity_ids(domain_filter),
            *(s.entity_id for s in self._interni_di(domain_filter)),
        ]

    def async_entity_ids_count(self, domain_filter: str | None = None) -> int:
        return self._veri.async_entity_ids_count(domain_filter) + len(
            self._interni_di(domain_filter)
        )

    @property
    def _states(self) -> Mapping[str, State]:
        # il nome che il motore dei modelli di Home Assistant legge (``_state_generator``)
        return _Unione(self._veri, self._interni)

    def __getattr__(self, nome: str) -> Any:
        return getattr(self._veri, nome)


class HassConMemoria:
    """``hass`` come lo vedono i modelli del motore: tutto quello di Home Assistant,
    con la macchina degli stati che vede anche i valori interni."""

    __slots__ = ("_hass", "states")

    def __init__(self, hass: HomeAssistant, stati: StatiConMemoria) -> None:
        self._hass = hass
        self.states = stati

    def __getattr__(self, nome: str) -> Any:
        return getattr(self._hass, nome)


# --- la memoria --------------------------------------------------------------------------


class _Annuncio:
    """Il marchio di un evento che annuncia una scrittura (o una chiamata)."""

    __slots__ = ("dati", "memoria", "nuovo", "tipo", "valore", "vecchio")

    def __init__(
        self,
        memoria: MemoriaInterna,
        tipo: str,
        valore: _Valore | None = None,
        vecchio: State | None = None,
        nuovo: State | None = None,
        dati: tuple[str, str, Mapping[str, Any]] | None = None,
    ) -> None:
        self.memoria = memoria
        self.tipo = tipo
        self.valore = valore
        self.vecchio = vecchio
        self.nuovo = nuovo
        self.dati = dati


Cambio = Callable[[Event[Any]], None]
Chiamata = Callable[[float, str, str, Mapping[str, Any], Context | None], None]


class MemoriaInterna:
    """I valori interni di una VMC."""

    def __init__(
        self,
        hass: HomeAssistant,
        nome: str = "master",
        chiavi: Iterable[str] = INTERNI,
        *,
        impostazioni: Mapping[str, Mapping[str, Any]] = IMPOSTAZIONI,
        stato: StatoVMC | None = None,
    ) -> None:
        self.hass = hass
        self.nome = nome
        self.stato_vmc = stato
        self._valori: dict[str, _Valore] = {}
        self._per_dominio: dict[str, dict[str, _Valore]] = {}
        for chiave in chiavi:
            dominio, _, oggetto = chiave.partition(".")
            grezza = dict(impostazioni[chiave] or {})
            # la configurazione come la valida l'aiutante (predefiniti compresi)
            config = _SCHEMI_CONFIG[dominio]({dominio: {oggetto: grezza}})[dominio][
                oggetto
            ]
            valore = _TIPI[dominio](self, chiave, config or {})
            self._valori[valore.entity_id] = valore
            self._per_dominio.setdefault(dominio, {})[valore.entity_id] = valore
        self._stati: dict[str, State] = {}
        # i modelli del motore vedono anche gli stati delle logiche (le automazioni del
        # package, che non sono entità)
        self.stati_modelli = StatiConMemoria(
            hass.states, ChainMap(self._stati, stati_logiche(hass).stati)
        )
        self.hass_modelli = HassConMemoria(hass, self.stati_modelli)
        # chi segue un valore interno lo segue da qui (prima di ogni iscrizione)
        self._togli_sorgente: CALLBACK_TYPE | None = cambi_interni(hass).aggiungi(self)
        self._cambi: list[Cambio] = []
        self._chiamate: list[Chiamata] = []
        self._annulla: list[CALLBACK_TYPE] = []
        self._archivio: Store[dict[str, Any]] | None = None
        self._salva_da_solo = False
        self._salvataggio_in_attesa = False

    # --- nomi ----------------------------------------------------------------------------

    def entity_id(self, chiave: str) -> str:
        """entity_id di oggi per una chiave (come ``StatoVMC.entity_id``)."""
        dominio, oggetto = chiave.split(".", 1)
        return f"{dominio}.vmc_{self.nome}_{oggetto}"

    def __contains__(self, entity_id: object) -> bool:
        return entity_id in self._valori

    def contiene(self, entity_id: str) -> bool:
        """Se ``entity_id`` è un valore interno (per ``seguire.CambiInterni``)."""
        return entity_id in self._valori

    @property
    def entity_ids(self) -> list[str]:
        return list(self._valori)

    def chiavi(self) -> list[str]:
        return [v.chiave for v in self._valori.values()]

    def stato(self, entity_id: str) -> State | None:
        """Lo stato di un valore interno (per entity_id di oggi)."""
        return self._stati.get(entity_id)

    def stati(self) -> list[State]:
        return list(self._stati.values())

    @callback
    def riscrivi(self, entity_id: str) -> None:
        """Riscrive un valore interno com'è: come ``homeassistant.update_entity`` di oggi
        sull'aiutante (``async_update_ha_state``, che senza un aggiornamento proprio
        riscrive lo stato: ``state_reported``, con il contesto dell'ultima scrittura se
        recente)."""
        self._valori[entity_id]._scrivi()

    def valori_del_dominio(self, dominio: str) -> Mapping[str, Any]:
        """I valori di un dominio come entità per ``entity_service_call`` (per
        entity_id, nell'ordine del package)."""
        return self._per_dominio.get(dominio, {})

    # --- avvio e salvataggio --------------------------------------------------------------

    @callback
    def ripristina(self, salvati: Mapping[str, Any] | None = None) -> None:
        """I valori all'avvio dai valori salvati (per chiave), con le regole degli
        aiutanti, e l'ascolto degli annunci. Come gli aiutanti all'avvio, prima dei
        trigger ``homeassistant: start``."""
        salvati = salvati or {}
        adesso = time.time()
        istante = dt_util.utc_from_timestamp(adesso)
        for valore in self._valori.values():
            valore.ripristina(salvati.get(valore.chiave))
            stato, attributi = valore.calcola()
            self._stati[valore.entity_id] = State(
                valore.entity_id,
                stato,
                attributi,
                None,
                istante,
                istante,
                Context(id=ulid_at_time(adesso)),
                True,
                None,
                adesso,
            )
        if not self._annulla:
            self._annulla.append(
                self.hass.bus.async_listen(
                    EVENT_STATE_REPORTED, self._consegna, event_filter=self._mio
                )
            )
        if self.stato_vmc is not None:
            self.stato_vmc.imposta(
                {
                    v.chiave: (self._stati[e].state, dict(self._stati[e].attributes))
                    for e, v in self._valori.items()
                }
            )

    def salvati(self) -> dict[str, Any]:
        """I valori da salvare, per chiave (il valore dell'aiutante: numero, testo o
        acceso)."""
        return {v.chiave: v.salvato() for v in self._valori.values()}

    def _store(self) -> Store[dict[str, Any]]:
        if self._archivio is None:
            self._archivio = Store(
                self.hass, VERSIONE_ARCHIVIO, CHIAVE_ARCHIVIO.format(nome=self.nome)
            )
        return self._archivio

    async def async_carica(self) -> None:
        """Ripristina i valori dall'archivio della VMC, poi salva da sola: entro
        ``RITARDO_SALVATAGGIO`` dopo un cambio e alla chiusura (``homeassistant_stop``,
        quando Home Assistant salva gli stati degli aiutanti)."""
        dati = await self._store().async_load()
        valori = dati.get("valori") if isinstance(dati, dict) else None
        self.ripristina(valori if isinstance(valori, dict) else None)
        self._salva_da_solo = True
        self._annulla.append(
            self.hass.bus.async_listen_once(
                EVENT_HOMEASSISTANT_STOP, self._salva_alla_chiusura
            )
        )

    async def async_salva(self) -> None:
        """Salva subito i valori di adesso."""
        self._salvataggio_in_attesa = False
        await self._store().async_save({"valori": self.salvati()})

    async def _salva_alla_chiusura(self, _evento: Event[Any]) -> None:
        # come restore_state: i valori alla chiusura, poi più nulla
        self._salva_da_solo = False
        await self.async_salva()

    def _dati_da_salvare(self) -> dict[str, Any]:
        self._salvataggio_in_attesa = False
        return {"valori": self.salvati()}

    @callback
    def _programma_salvataggio(self) -> None:
        if not self._salva_da_solo or self._salvataggio_in_attesa:
            return
        self._salvataggio_in_attesa = True
        self._store().async_delay_save(self._dati_da_salvare, RITARDO_SALVATAGGIO)

    @callback
    def ferma(self) -> None:
        """Smette di ascoltare gli annunci e di salvare; nessuno segue più i valori."""
        self._salva_da_solo = False
        for annulla in self._annulla:
            annulla()
        self._annulla.clear()
        if self._togli_sorgente is not None:
            self._togli_sorgente()
            self._togli_sorgente = None

    # --- ascolto -------------------------------------------------------------------------

    @callback
    def ascolta_cambi(self, funzione: Cambio) -> CALLBACK_TYPE:
        """``funzione`` riceve ogni cambio come l'evento ``state_changed`` che oggi
        manda l'aiutante, nello stesso punto (dopo chi segue l'entità)."""
        self._cambi.append(funzione)
        return lambda: self._cambi.remove(funzione)

    @callback
    def ascolta_chiamate(self, funzione: Chiamata) -> CALLBACK_TYPE:
        """``funzione(istante, dominio, servizio, dati, contesto)`` riceve ogni
        chiamata ai valori interni nel punto in cui oggi Home Assistant manda
        ``call_service``."""
        self._chiamate.append(funzione)
        return lambda: self._chiamate.remove(funzione)

    # --- scritture -----------------------------------------------------------------------

    @staticmethod
    def gestisce(dominio: str, servizio: str) -> bool:
        """Se il servizio è uno di quelli degli aiutanti sui valori interni."""
        return (dominio, servizio) in SERVIZI

    @staticmethod
    def valida(dominio: str, servizio: str, dati: Mapping[str, Any]) -> dict[str, Any]:
        """I dati validati con lo schema del servizio dell'aiutante."""
        schema, _ = SERVIZI[dominio, servizio]
        try:
            return schema(dict(dati))  # type: ignore[no-any-return]
        except probatio.Invalid:
            _LOGGER.debug(
                "Invalid data for service call %s.%s: %s", dominio, servizio, dati
            )
            raise

    async def async_chiama(
        self,
        dominio: str,
        servizio: str,
        dati: Mapping[str, Any],
        contesto: Context,
        validati: dict[str, Any] | None = None,
    ) -> None:
        """Un servizio di un aiutante sui valori interni (come
        ``ServiceRegistry.async_call`` con ``blocking=True``, senza ``call_service``):
        ``dati`` sono i dati con il bersaglio, ``validati`` gli stessi già validati."""
        if validati is None:
            validati = self.valida(dominio, servizio, dati)
        _, funzione = SERVIZI[dominio, servizio]
        chiamata = ServiceCall(self.hass, dominio, servizio, validati, contesto)
        self.hass.bus.async_fire(
            EVENT_STATE_REPORTED,
            {
                "entity_id": "",
                _MARCHIO: _Annuncio(
                    self, "chiamata", dati=(dominio, servizio, dict(dati))
                ),
            },
            context=contesto,
        )
        await entity_service_call(
            self.hass, self._per_dominio.get(dominio, {}), funzione, chiamata
        )

    @callback
    def _imposta(
        self,
        valore: _Valore,
        nuovo: str,
        attributi: dict[str, Any],
        contesto: Context | None,
        timestamp: float,
    ) -> None:
        """Come ``StateMachine.async_set_internal``, con l'annuncio al posto
        dell'evento."""
        entity_id = valore.entity_id
        vecchio = self._stati[entity_id]
        stesso_stato = vecchio.state == nuovo
        stessi_attributi = vecchio.attributes == attributi
        adesso = dt_util.utc_from_timestamp(timestamp)
        if contesto is None:
            contesto = Context(id=ulid_at_time(timestamp))
        if stesso_stato and stessi_attributi:
            # come Home Assistant cambia solo ``last_reported`` (con uno State nuovo:
            # gli altri campi, contesto compreso, restano quelli del cambio)
            riportato = State(
                entity_id,
                vecchio.state,
                vecchio.attributes,
                vecchio.last_changed,
                adesso,
                vecchio.last_updated,
                vecchio.context,
                False,
                None,
                vecchio.last_updated_timestamp,
            )
            self._stati[entity_id] = riportato
            self.hass.bus.async_fire(
                EVENT_STATE_REPORTED,
                {
                    "entity_id": entity_id,
                    "last_reported": adesso,
                    "old_last_reported": vecchio.last_reported,
                    "new_state": riportato,
                    _MARCHIO: _Annuncio(self, "riportato", valore),
                },
                context=contesto,
                time_fired=timestamp,
            )
            return
        if stessi_attributi:
            attributi = vecchio.attributes  # type: ignore[assignment]
        if not stesso_stato and len(nuovo) > MAX_LENGTH_STATE_STATE:
            _LOGGER.error(
                "State %s for %s is longer than %s, falling back to %s",
                nuovo,
                entity_id,
                MAX_LENGTH_STATE_STATE,
                STATE_UNKNOWN,
            )
            nuovo = STATE_UNKNOWN
        stato = State(
            entity_id,
            nuovo,
            attributi,
            vecchio.last_changed if stesso_stato else None,
            adesso,
            adesso,
            contesto,
            False,
            None,
            timestamp,
        )
        vecchio.expire()
        self._stati[entity_id] = stato
        self._programma_salvataggio()
        # l'entity_id vuoto: nessuno che segue i «state_reported» di un'entità lo
        # prende per un rapporto
        self.hass.bus.async_fire(
            EVENT_STATE_REPORTED,
            {
                "entity_id": "",
                _MARCHIO: _Annuncio(self, "cambiato", valore, vecchio, stato),
            },
            context=contesto,
            time_fired=timestamp,
        )

    # --- annunci -------------------------------------------------------------------------

    @callback
    def _mio(self, dati: Mapping[str, Any]) -> bool:
        annuncio = dati.get(_MARCHIO)
        return annuncio is not None and annuncio.memoria is self

    @callback
    def _consegna(self, evento: Event[Any]) -> None:
        """Un annuncio arriva quando Home Assistant consegnerebbe ``state_changed``
        (o ``call_service``): a chi segue l'entità, allo StatoVMC, a chi ascolta."""
        annuncio: _Annuncio = evento.data[_MARCHIO]
        if annuncio.tipo == "chiamata":
            assert annuncio.dati is not None
            dominio, servizio, dati = annuncio.dati
            for funzione in list(self._chiamate):
                funzione(
                    evento.time_fired_timestamp,
                    dominio,
                    servizio,
                    dati,
                    evento.context,
                )
            return
        if annuncio.tipo != "cambiato":
            return
        valore = annuncio.valore
        nuovo = annuncio.nuovo
        assert valore is not None and nuovo is not None
        cambio: Event[Any] = Event(
            EVENT_STATE_CHANGED,
            {
                "entity_id": valore.entity_id,
                "old_state": annuncio.vecchio,
                "new_state": nuovo,
            },
            EventOrigin.local,
            evento.time_fired_timestamp,
            evento.context,
        )
        # chi segue l'entità come un'entità vera (seguire.CambiInterni)
        cambi_interni(self.hass).consegna(cambio)
        if self.stato_vmc is not None:
            # con il contesto della scrittura, come il template di oggi che rilegge
            # l'aiutante e prende il contesto del suo cambio
            self.stato_vmc.imposta(
                {valore.chiave: (nuovo.state, dict(nuovo.attributes))}, evento.context
            )
        for funzione in list(self._cambi):
            funzione(cambio)


def da_stato(chiave: str, stato: str | None) -> Any:
    """Il valore da salvare per una chiave dallo stato di un aiutante di oggi, come lo
    ripristina l'aiutante senza dati aggiuntivi (un numero dal testo dello stato, un
    interruttore acceso solo se «on»)."""
    if stato is None:
        return None
    dominio = chiave.partition(".")[0]
    if dominio == "input_number":
        try:
            return float(stato)
        except ValueError:
            return None
    if dominio == "input_boolean":
        return stato == STATE_ON
    return stato
