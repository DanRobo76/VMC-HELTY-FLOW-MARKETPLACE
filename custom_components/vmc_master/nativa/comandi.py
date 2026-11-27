"""Impostazioni native: gli aiutanti visibili del package come entità native (fase 4).

Come entita.py per i sensori, ogni entità è una vista su StatoVMC: il valore sta in
StatoVMC con la chiave di oggi (entity_id senza «vmc_<nome>_», es. «input_boolean.x»),
così i modelli che leggono le impostazioni continuano a funzionare. Il dominio di domani
viene dalla colonna «Domani» della fase 1 (tabelle.DOMANI): l'oggetto dopo il punto non
cambia, cambia solo il dominio.

- 37 input_boolean -> switch, 77 input_boolean -> binary_sensor (le spie: le scrive solo
  il motore), 10 input_number -> number, 14 input_select -> select, 2 input_text -> text,
  30 input_datetime -> time, 1 input_number + 1 input_select + 1 input_text -> sensor.

Ogni entità rifà quello che fa l'aiutante di oggi: stesso valore iniziale, stesso
ripristino dopo un riavvio, stesso testo dello stato (numeri come float: «5.0»; ora
«HH:MM:SS»), stesse scritture. Le scritture del motore passano da ``ScritturaComandi``,
che rifà i servizi degli aiutanti (stessi schemi, stessi errori, stessi tempi e contesti
di ``helpers/service.py``) sulle entità native; l'utente usa i servizi del dominio nativo
(switch.turn_on, number.set_value, select.select_option, text.set_value, time.set_value).
"""

from __future__ import annotations

import datetime as dt
import logging
import re
from collections import Counter
from collections.abc import Callable, Iterable, Mapping
from functools import partial
from typing import TYPE_CHECKING, Any

import probatio
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.number import NumberMode, RestoreNumber
from homeassistant.components.select import SelectEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.components.text import TextEntity, TextMode
from homeassistant.components.time import TimeEntity
from homeassistant.const import ATTR_ENTITY_ID, STATE_ON
from homeassistant.core import (
    Context,
    HassJob,
    HomeAssistant,
    ServiceCall,
    State,
    callback,
)
from homeassistant.exceptions import ServiceNotFound, ServiceValidationError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity import FLOAT_PRECISION, Entity
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.service import entity_service_call
from homeassistant.util import dt as dt_util

from .entita import nome_visibile
from .stato import SCONOSCIUTO, Cambi, StatoVMC
from .tabelle import DOMANI, IMPOSTAZIONI, ORDINE_AIUTANTI

if TYPE_CHECKING:
    from .motore.memoria_interna import MemoriaInterna

_LOGGER = logging.getLogger(__name__)

DOMINI_AIUTANTI = (
    "input_boolean",
    "input_number",
    "input_select",
    "input_text",
    "input_datetime",
)
"""I tipi di aiutante di oggi che diventano entità native (i timer non sono qui)."""

FORMATO_ORA = "%H:%M:%S"
"""Il testo dello stato di un input_datetime con la sola ora."""


def chiavi_comandi() -> list[str]:
    """Le chiavi delle impostazioni che domani sono entità native (non interne)."""
    return [
        chiave
        for chiave in IMPOSTAZIONI
        if chiave.split(".", 1)[0] in DOMINI_AIUTANTI and DOMANI[chiave] != "interna"
    ]


def testo_numero(valore: float) -> str:
    """Il testo dello stato di un numero float, come lo scrive Home Assistant («5.0»)."""
    return f"{valore:.{FLOAT_PRECISION}}"


def _numero(testo: str | None) -> float | None:
    if testo is None or testo == SCONOSCIUTO:
        return None
    try:
        return float(testo)
    except ValueError:
        return None


class ComandoVMC(Entity):
    """Parte comune: identità dalla tabella, valore in StatoVMC.

    Una scrittura passa da StatoVMC; l'entità scrive il suo stato prima dei sensori che
    la leggono (ascolto con ``prima``), come l'aiutante cambia prima dei template. Se il
    valore non cambia lo stato si riscrive lo stesso (Home Assistant manda allora
    ``state_reported``, come per l'aiutante).
    """

    _attr_should_poll = False

    def __init__(self, stato: StatoVMC, chiave: str) -> None:
        """Entità per la chiave (es. «input_boolean.notifica_audio») della VMC di ``stato``."""
        voce = IMPOSTAZIONI[chiave]
        oggetto = chiave.split(".", 1)[1]
        self._stato = stato
        self._chiave = chiave
        self._voce = voce
        self.entity_id = f"{DOMANI[chiave]}.vmc_{stato.nome}_{oggetto}"
        self._attr_unique_id = f"vmc_{stato.nome}_{oggetto}"
        self._attr_name = (
            nome_visibile(voce["name"], stato.nome) if "name" in voce else None
        )
        self._attr_icon = voce.get("icon")

    @property
    def chiave(self) -> str:
        """Chiave dell'impostazione in StatoVMC (entity_id di oggi senza «vmc_<nome>_»)."""
        return self._chiave

    @property
    def dominio_di_oggi(self) -> str:
        """Il dominio dell'aiutante di oggi (es. «input_boolean»)."""
        return self._chiave.split(".", 1)[0]

    async def async_added_to_hass(self) -> None:
        """Valore iniziale (o ripristinato) in StatoVMC, poi segue i cambi della chiave."""
        await super().async_added_to_hass()
        self._stato.imposta({self._chiave: await self._valore_iniziale()})
        self.async_on_remove(self._stato.ascolta(self._cambi, prima=True))

    async def _valore_iniziale(self) -> str | tuple[str, Mapping[str, Any]]:
        """Il valore all'avvio, come l'aiutante di oggi (``initial``, ripristino...)."""
        raise NotImplementedError

    async def _ultimo_stato(self) -> State | None:
        """L'ultimo stato da riprendere: quello conservato da Home Assistant oppure, se
        non c'è (prima partenza dopo il passaggio dalla beta), il valore dell'aiutante
        della beta passato in StatoVMC. Le regole del ripristino sono le stesse."""
        stato = await self.async_get_last_state()  # type: ignore[attr-defined]
        if stato is None:
            stato = self._stato.passati.get(self._chiave)
        return stato

    @callback
    def _cambi(self, cambi: Cambi) -> None:
        if self._chiave in cambi:
            self.async_write_ha_state()

    @callback
    def _scrivi(self, valore: str | tuple[str, Mapping[str, Any]]) -> None:
        """Scrive il valore in StatoVMC e lo stato in Home Assistant (anche se uguale);
        i sensori che lo leggono prendono il contesto della scrittura (quello della chiamata,
        che ``entity_service_call`` ha appena dato all'entità), come i template di oggi
        prendono quello del cambio dell'aiutante."""
        if self._chiave not in self._stato.imposta(
            {self._chiave: valore}, self._context
        ):
            self.async_write_ha_state()

    def _testo(self) -> str | None:
        return self._stato.stato(self._chiave)


# --- input_boolean -> switch / binary_sensor -------------------------------------------------


class _AccesoSpento(ComandoVMC, RestoreEntity):
    """Acceso/spento come ``input_boolean``: ``initial``, altrimenti l'ultimo stato,
    altrimenti spento."""

    async def _valore_iniziale(self) -> str:
        iniziale = self._voce.get("initial")
        if iniziale is not None:
            return STATE_ON if iniziale else "off"
        stato = await self._ultimo_stato()
        return STATE_ON if stato is not None and stato.state == STATE_ON else "off"

    @property
    def is_on(self) -> bool:
        """Acceso se il valore in StatoVMC è «on»."""
        return self._testo() == STATE_ON

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Accende (input_boolean.turn_on)."""
        self._scrivi(STATE_ON)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Spegne (input_boolean.turn_off)."""
        self._scrivi("off")


class InterruttoreVMC(_AccesoSpento, SwitchEntity):
    """Un ``input_boolean`` che la scheda comanda: domani è uno ``switch``."""


class SpiaVMC(_AccesoSpento, BinarySensorEntity):
    """Un ``input_boolean`` solo mostrato: domani è un ``binary_sensor``, scritto solo dal
    motore (``ScritturaComandi``: il dominio binary_sensor non ha servizi)."""


# --- input_number -> number / sensor ---------------------------------------------------------


class _Numero(ComandoVMC):
    """Valore numerico come ``input_number``: float, limiti float, ripristino.

    In StatoVMC c'è il testo dello stato («5.0»); l'entità tiene anche il float esatto
    scritto (0.1 + 0.2 resta 0.30000000000000004, come nell'aiutante).
    """

    def __init__(self, stato: StatoVMC, chiave: str) -> None:
        """Limiti e passo dalla tabella, float come li rende lo schema di input_number."""
        super().__init__(stato, chiave)
        # float come lo schema di input_number: un massimo intero oltre i 64 bit non si
        # potrebbe salvare nel registro delle entità
        self._minimo = float(self._voce["min"])
        self._massimo = float(self._voce["max"])
        self._passo = float(self._voce.get("step", 1))
        iniziale = self._voce.get("initial")
        self._iniziale = None if iniziale is None else float(iniziale)
        self._esatto: float | None = None

    def _valore_numerico(self) -> float | None:
        testo = self._testo()
        if self._esatto is not None and testo == testo_numero(self._esatto):
            return self._esatto
        return _numero(testo)

    async def _valore_iniziale(self) -> str:
        if self._iniziale is not None:
            valore: float | None = self._iniziale
        else:
            valore = await self._ultimo_numero()
        if valore is None or not self._minimo <= valore <= self._massimo:
            valore = self._minimo
        self._esatto = float(valore)
        return testo_numero(self._esatto)

    async def _ultimo_numero(self) -> float | None:
        """L'ultimo valore salvato (come InputNumber.async_added_to_hass)."""
        stato = await self._ultimo_stato()
        return None if stato is None else _numero(stato.state)

    async def async_set_native_value(self, value: float) -> None:
        """Nuovo valore (sempre float, come input_number)."""
        self._esatto = float(value)
        self._scrivi(testo_numero(self._esatto))


class NumeroVMC(_Numero, RestoreNumber):
    """Un ``input_number``: domani è un ``number``."""

    def __init__(self, stato: StatoVMC, chiave: str) -> None:
        """Limiti, passo, modo e unità dell'aiutante."""
        super().__init__(stato, chiave)
        self._attr_native_min_value = self._minimo
        self._attr_native_max_value = self._massimo
        self._attr_native_step = self._passo
        self._attr_mode = NumberMode(self._voce.get("mode", "slider"))
        self._attr_native_unit_of_measurement = self._voce.get("unit_of_measurement")

    @property
    def native_value(self) -> float | None:
        """Il valore in StatoVMC (float)."""
        return self._valore_numerico()

    async def _ultimo_numero(self) -> float | None:
        """Dai dati del numero; senza, dal testo dello stato (come input_number fino alla 2027.5)."""
        if (dati := await self.async_get_last_number_data()) is not None:
            return dati.native_value
        return await super()._ultimo_numero()


class SensoreNumeroVMC(_Numero, SensorEntity, RestoreEntity):
    """Un ``input_number`` che la scheda solo mostra: domani è un ``sensor``.

    Il motore lo scrive con ``input_number.set_value`` (stessi limiti e stesso errore).
    """

    @property
    def native_value(self) -> float | None:
        """Il valore in StatoVMC (float: lo stato è «0.0» come l'aiutante)."""
        return self._valore_numerico()

    @property
    def min_value(self) -> float:
        """Minimo (come NumberEntity.min_value, senza unità da convertire)."""
        return self._minimo

    @property
    def max_value(self) -> float:
        """Massimo."""
        return self._massimo

    native_min_value = min_value
    native_max_value = max_value

    def convert_to_native_value(self, value: float) -> float:
        """Nessuna conversione di unità."""
        return value


# --- input_select -> select / sensor ---------------------------------------------------------


class _Scelta(ComandoVMC, RestoreEntity):
    """Scelta fra opzioni come ``input_select``: le opzioni stanno negli attributi della
    voce in StatoVMC (``set_options`` le cambia)."""

    def __init__(self, stato: StatoVMC, chiave: str) -> None:
        """Opzioni dalla tabella (col nome della VMC)."""
        super().__init__(stato, chiave)
        self._opzioni_iniziali = [
            nome_visibile(o, stato.nome) for o in self._voce["options"]
        ]

    def _opzioni(self) -> list[str]:
        voce = self._stato.voce(self._chiave)
        if voce is not None and "options" in voce.attributi:
            return list(voce.attributi["options"])
        return list(self._opzioni_iniziali)

    async def _valore_iniziale(self) -> tuple[str, Mapping[str, Any]]:
        opzioni = self._opzioni_iniziali
        scelta = self._voce.get("initial")
        if scelta is None:
            stato = await self._ultimo_stato()
            scelta = (
                stato.state
                if stato is not None and stato.state in opzioni
                else opzioni[0]
            )
        return scelta, {"options": list(opzioni)}


class SceltaVMC(_Scelta, SelectEntity):
    """Un ``input_select``: domani è un ``select``."""

    @property
    def options(self) -> list[str]:
        """Le opzioni in StatoVMC."""
        return self._opzioni()

    @property
    def current_option(self) -> str | None:
        """L'opzione in StatoVMC."""
        return self._testo()

    async def async_select_option(self, option: str) -> None:
        """Sceglie un'opzione; un'opzione che non c'è dà l'errore di input_select."""
        opzioni = self._opzioni()
        if option not in opzioni:
            raise ServiceValidationError(
                translation_domain="input_select",
                translation_key="invalid_option",
                translation_placeholders={
                    "entity_id": self.entity_id,
                    "option": option,
                    "options": ", ".join(opzioni),
                },
            )
        self._scrivi((option, {"options": opzioni}))

    async def async_set_options(self, options: list[str]) -> None:
        """Nuove opzioni (input_select.set_options, solo per il motore)."""
        if duplicati := [
            opzione for opzione, quante in Counter(options).items() if quante > 1
        ]:
            raise ServiceValidationError(
                translation_domain="input_select",
                translation_key="duplicate_options",
                translation_placeholders={
                    "entity_id": self.entity_id,
                    "duplicates": ", ".join(duplicati),
                },
            )
        scelta = self._testo()
        if scelta not in options:
            _LOGGER.warning(
                "Current option: %s no longer valid (possible options: %s)",
                scelta,
                ", ".join(options),
            )
            scelta = options[0]
        assert scelta is not None
        self._scrivi((scelta, {"options": list(options)}))


class SensoreSceltaVMC(_Scelta, SensorEntity):
    """Un ``input_select`` che nessuno cambia (l'elenco delle entità escluse dal registro):
    domani è un ``sensor`` con lo stesso stato e lo stesso attributo ``options``."""

    @property
    def native_value(self) -> str | None:
        """L'opzione in StatoVMC."""
        return self._testo()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """L'attributo ``options`` dell'aiutante (lo legge la scheda)."""
        return {"options": self._opzioni()}


# --- input_text -> text / sensor -------------------------------------------------------------


class _Testo(ComandoVMC, RestoreEntity):
    """Testo come ``input_text``: lunghezza e modello controllati come nell'aiutante."""

    def __init__(self, stato: StatoVMC, chiave: str) -> None:
        """Lunghezze e modello dalla tabella (predefiniti di input_text: 0 e 100)."""
        super().__init__(stato, chiave)
        self._minimo = int(self._voce.get("min", 0))
        self._massimo = int(self._voce.get("max", 100))
        self._modello = self._voce.get("pattern")

    def _valore_testo(self) -> str | None:
        testo = self._testo()
        return None if testo == SCONOSCIUTO else testo

    async def _valore_iniziale(self) -> str:
        valore = self._voce.get("initial")
        if valore is None:
            stato = await self._ultimo_stato()
            vecchio = stato.state if stato else None
            if vecchio is not None and self._minimo <= len(vecchio) <= self._massimo:
                valore = vecchio
        return SCONOSCIUTO if valore is None else valore

    async def async_set_value(self, value: str) -> None:
        """Nuovo testo; fuori misura o fuori modello: avviso e nessun cambio (input_text)."""
        if len(value) < self._minimo or len(value) > self._massimo:
            _LOGGER.warning(
                "Invalid value: %s (length range %s - %s)",
                value,
                self._minimo,
                self._massimo,
            )
            return
        if self._modello is not None and not re.match(self._modello, value):
            _LOGGER.warning(
                "Invalid value: %s (does not match pattern %s)", value, self._modello
            )
            return
        self._scrivi(value)


class TestoVMC(_Testo, TextEntity):
    """Un ``input_text``: domani è un ``text``."""

    __test__ = False  # non è una classe di prove di pytest

    def __init__(self, stato: StatoVMC, chiave: str) -> None:
        """Lunghezze, modello e modo dell'aiutante."""
        super().__init__(stato, chiave)
        self._attr_native_min = self._minimo
        self._attr_native_max = self._massimo
        self._attr_pattern = self._modello
        self._attr_mode = TextMode(self._voce.get("mode", "text"))

    @property
    def native_value(self) -> str | None:
        """Il testo in StatoVMC."""
        return self._valore_testo()


class SensoreTestoVMC(_Testo, SensorEntity):
    """Un ``input_text`` che la scheda solo mostra: domani è un ``sensor``.

    Il motore lo scrive con ``input_text.set_value`` (stessi controlli).
    """

    @property
    def native_value(self) -> str | None:
        """Il testo in StatoVMC."""
        return self._valore_testo()


# --- input_datetime (solo ora) -> time -------------------------------------------------------


class OraVMC(ComandoVMC, TimeEntity, RestoreEntity):
    """Un ``input_datetime`` con la sola ora: domani è un ``time``.

    In StatoVMC c'è il testo «HH:MM:SS» dell'aiutante (senza frazioni di secondo).
    """

    @property
    def native_value(self) -> dt.time | None:
        """L'ora in StatoVMC."""
        testo = self._testo()
        return None if testo in (None, SCONOSCIUTO) else dt_util.parse_time(testo)

    async def _valore_iniziale(self) -> str:
        iniziale = self._voce.get("initial")
        if iniziale:
            ora = dt_util.parse_time(iniziale)
            assert ora is not None
            return ora.strftime(FORMATO_ORA)
        stato = await self._ultimo_stato()
        ora = None if stato is None else dt_util.parse_time(stato.state)
        return (ora or dt.time(0, 0, 0)).strftime(FORMATO_ORA)

    async def async_set_value(self, value: dt.time) -> None:
        """Nuova ora (time.set_value)."""
        self._scrivi(value.strftime(FORMATO_ORA))

    @callback
    def async_set_datetime(
        self,
        date: dt.date | None = None,
        time: dt.time | None = None,
        datetime: dt.datetime | None = None,
        timestamp: float | None = None,
    ) -> None:
        """input_datetime.set_datetime per un aiutante con la sola ora (solo il motore)."""
        if timestamp is not None:
            datetime = dt_util.as_local(dt_util.utc_from_timestamp(timestamp))
        if datetime:
            time = datetime.time()
        if not time:
            raise probatio.Invalid("Nothing to set")
        self._scrivi(time.strftime(FORMATO_ORA))


# --- le entità di una VMC ----------------------------------------------------------------------

_CLASSI: dict[tuple[str, str], type[ComandoVMC]] = {
    ("input_boolean", "switch"): InterruttoreVMC,
    ("input_boolean", "binary_sensor"): SpiaVMC,
    ("input_number", "number"): NumeroVMC,
    ("input_number", "sensor"): SensoreNumeroVMC,
    ("input_select", "select"): SceltaVMC,
    ("input_select", "sensor"): SensoreSceltaVMC,
    ("input_text", "text"): TestoVMC,
    ("input_text", "sensor"): SensoreTestoVMC,
    ("input_datetime", "time"): OraVMC,
}


def crea_comandi(stato: StatoVMC) -> dict[str, list[ComandoVMC]]:
    """Le 173 entità delle impostazioni visibili della VMC, per dominio di domani."""
    entita: dict[str, list[ComandoVMC]] = {}
    for chiave in chiavi_comandi():
        dominio = DOMANI[chiave]
        classe = _CLASSI[(chiave.split(".", 1)[0], dominio)]
        entita.setdefault(dominio, []).append(classe(stato, chiave))
    return entita


# --- le scritture del motore -----------------------------------------------------------------


async def _imposta_numero(entita: Any, chiamata: ServiceCall) -> None:
    """input_number.set_value: fuori dai limiti l'errore di input_number, poi il valore."""
    valore = chiamata.data["value"]
    if valore < entita.min_value or valore > entita.max_value:
        raise probatio.Invalid(
            f"Invalid value for {entita.entity_id}: {valore} (range "
            f"{entita.min_value} - {entita.max_value})"
        )
    nativo = entita.convert_to_native_value(valore)
    await entita.async_set_native_value(
        min(max(nativo, entita.native_min_value), entita.native_max_value)
    )


def _controlla_data_ora(config: dict[str, Any]) -> dict[str, Any]:
    """Come input_datetime: data/ora, datetime e timestamp non vanno insieme."""
    data_o_ora = any(chiave in config for chiave in ("date", "time"))
    if sum([data_o_ora, "datetime" in config, "timestamp" in config]) > 1:
        raise probatio.Invalid(f"Cannot use together: {', '.join(config.keys())}")
    return config


SERVIZI_MOTORE: dict[str, tuple[Any, str | Callable[..., Any]]] = {
    "input_boolean.turn_on": (cv.make_entity_service_schema(None), "async_turn_on"),
    "input_boolean.turn_off": (cv.make_entity_service_schema(None), "async_turn_off"),
    "input_number.set_value": (
        cv.make_entity_service_schema(
            {probatio.Required("value"): probatio.Coerce(float)}
        ),
        _imposta_numero,
    ),
    "input_select.select_option": (
        cv.make_entity_service_schema({probatio.Required("option"): cv.string}),
        "async_select_option",
    ),
    "input_select.set_options": (
        cv.make_entity_service_schema(
            {
                probatio.Required("options"): probatio.All(
                    probatio.EnsureList(), probatio.NonEmpty(), [cv.string]
                )
            }
        ),
        "async_set_options",
    ),
    "input_text.set_value": (
        cv.make_entity_service_schema({probatio.Required("value"): cv.string}),
        "async_set_value",
    ),
    "input_datetime.set_datetime": (
        probatio.All(
            cv.make_entity_service_schema(
                {
                    probatio.Optional("date"): cv.date,
                    probatio.Optional("time"): cv.time,
                    probatio.Optional("datetime"): cv.datetime,
                    probatio.Optional("timestamp"): probatio.Coerce(float),
                }
            ),
            probatio.AtLeastOne("date", "time", "datetime", "timestamp"),
            _controlla_data_ora,
        ),
        "async_set_datetime",
    ),
}
"""I servizi degli aiutanti che il package chiama (inventario: nessun increment,
decrement, select_next...), con lo schema e il metodo dell'aiutante."""


class _ComeAiutante:
    """Un'entità nativa vista con l'entity_id dell'aiutante di oggi.

    Serve solo a ``entity_service_call`` (``ScritturaComandi.chiama``): Home Assistant
    scrive più bersagli nell'ordine dell'insieme dei loro entity_id, quindi con i nomi di
    oggi l'ordine dei compiti (e dei cambi di stato) è quello degli aiutanti. Tutto il
    resto (metodi, contesto, disponibilità) è dell'entità nativa.
    """

    __slots__ = ("_entita", "entity_id")

    def __init__(self, entita: ComandoVMC, entity_id: str) -> None:
        self._entita = entita
        self.entity_id = entity_id

    def __getattr__(self, nome: str) -> Any:
        return getattr(self._entita, nome)


class ScritturaComandi:
    """Le scritture del motore sulle impostazioni native, come i servizi degli aiutanti.

    Ogni servizio di oggi (``SERVIZI_MOTORE``) vede solo le entità che oggi sono di quel
    tipo di aiutante (input_boolean.turn_on: interruttori e spie; input_number.set_value:
    numeri e il sensore numerico...), con lo stesso schema, lo stesso errore e la stessa
    forma di ``helpers/service.py`` (``entity_service_call``): il contesto della chiamata
    su ogni entità; un'entità sola scritta dentro la chiamata, più entità ognuna in un
    suo compito, nell'ordine di un insieme come in Home Assistant.

    Due vie, con gli stessi tempi: ``chiama`` (diretta, senza evento ``call_service``) e
    ``registra`` (servizi veri in un dominio scelto da chi la usa, con il loro evento).
    ``chiama`` risolve i bersagli con gli entity_id di oggi (``_ComeAiutante``): più
    bersagli si scrivono nello stesso ordine degli aiutanti (Home Assistant scrive
    l'intersezione fra l'insieme dei bersagli e le entità del dominio, che percorre
    nell'ordine in cui si sono aggiunte: qui le entità di ogni tipo di aiutante, valori
    interni compresi, sono nell'ordine del package, ``ORDINE_AIUTANTI``).

    Con ``memoria`` (fase 4, la memoria interna del motore) ogni servizio vede anche i
    valori interni del suo tipo di aiutante, con il loro entity_id di oggi: una chiamata
    con impostazioni native e valori interni insieme (il package spegne la spia interna
    con altre spie) li scrive tutti in una volta, come oggi Home Assistant con gli
    aiutanti.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        entita: Iterable[ComandoVMC],
        memoria: MemoriaInterna | None = None,
    ) -> None:
        """Scritture per le entità date (quelle aggiunte a Home Assistant) e, con
        ``memoria``, per i valori interni."""
        self.hass = hass
        self._memoria = memoria
        self._per_tipo: dict[str, dict[str, ComandoVMC]] = {}
        # entity_id di domani -> entity_id di oggi, per tipo di aiutante
        self._di_oggi: dict[str, dict[str, str]] = {}
        for voce in entita:
            tipo = voce.dominio_di_oggi
            self._per_tipo.setdefault(tipo, {})[voce.entity_id] = voce
            oggetto = voce.entity_id.split(".", 1)[1]
            self._di_oggi.setdefault(tipo, {})[voce.entity_id] = f"{tipo}.{oggetto}"
        self._in_ordine: dict[str, Callable[[], Mapping[str, Any]]] = {}
        self._funzioni = {
            servizio: funzione if isinstance(funzione, str) else HassJob(funzione)
            for servizio, (_, funzione) in SERVIZI_MOTORE.items()
        }

    def gestisce(self, dominio: str) -> bool:
        """Se ``dominio`` è un tipo di aiutante di oggi (i suoi servizi vengono qui)."""
        return dominio in DOMINI_AIUTANTI

    def _entita(self, tipo: str) -> Callable[[], Mapping[str, Entity]]:
        def aggiunte() -> Mapping[str, Entity]:
            entita: dict[str, Any] = {
                entity_id: voce
                for entity_id, voce in self._per_tipo.get(tipo, {}).items()
                if voce.hass is not None
            }
            if self._memoria is not None:
                entita.update(self._memoria.valori_del_dominio(tipo))
            return entita

        return aggiunte

    def _entita_di_oggi(self, tipo: str) -> Callable[[], Mapping[str, Any]]:
        if (pronte := self._in_ordine.get(tipo)) is not None:
            return pronte
        di_oggi = self._di_oggi.get(tipo, {})
        # (entity_id di oggi, entità o valore interno, se è un valore interno)
        tutte: list[tuple[str, Any, bool]] = [
            (di_oggi[entity_id], voce, False)
            for entity_id, voce in self._per_tipo.get(tipo, {}).items()
        ]
        if self._memoria is not None:
            # i valori interni hanno già l'entity_id di oggi
            tutte += [
                (entity_id, valore, True)
                for entity_id, valore in self._memoria.valori_del_dominio(tipo).items()
            ]
        posizione = {
            chiave: i for i, chiave in enumerate(ORDINE_AIUTANTI.get(tipo, ()))
        }
        tutte.sort(key=lambda voce: posizione.get(voce[1].chiave, len(posizione)))

        def aggiunte() -> Mapping[str, Any]:
            return {
                entity_id: voce if interno else _ComeAiutante(voce, entity_id)
                for entity_id, voce, interno in tutte
                if interno or voce.hass is not None
            }

        self._in_ordine[tipo] = aggiunte
        return aggiunte

    async def chiama(
        self,
        servizio: str,
        dati: Mapping[str, Any] | None,
        contesto: Context,
        bersaglio: Mapping[str, Any] | None = None,
    ) -> None:
        """``servizio`` di oggi (es. «input_boolean.turn_on») sulle entità native, come
        ``hass.services.async_call(..., blocking=True)`` (senza evento ``call_service``).

        I bersagli possono essere le entità di domani o gli aiutanti di oggi: si
        risolvono con i nomi di oggi, come farebbe Home Assistant con gli aiutanti."""
        dominio, _, nome = servizio.partition(".")
        if servizio not in SERVIZI_MOTORE:
            raise ServiceNotFound(dominio, nome)
        schema, _ = SERVIZI_MOTORE[servizio]
        valori = dict(dati or {})
        if bersaglio:
            valori.update(bersaglio)
        validati = schema(valori)
        if isinstance(entita := validati.get(ATTR_ENTITY_ID), list):
            di_oggi = self._di_oggi.get(dominio, {})
            validati[ATTR_ENTITY_ID] = [di_oggi.get(e, e) for e in entita]
        chiamata = ServiceCall(self.hass, dominio, nome, validati, contesto)
        await entity_service_call(
            self.hass,
            self._entita_di_oggi(dominio),
            self._funzioni[servizio],
            chiamata,
        )

    @callback
    def registra(self, dominio: str) -> dict[str, str]:
        """Registra i servizi in ``dominio`` («<dominio>.input_boolean_turn_on»...).

        Restituisce servizio di oggi -> servizio registrato (per la mappa dei nomi).
        """
        nomi: dict[str, str] = {}
        for servizio, (schema, _) in SERVIZI_MOTORE.items():
            nome = servizio.replace(".", "_")
            self.hass.services.async_register(
                dominio,
                nome,
                partial(
                    entity_service_call,
                    self.hass,
                    self._entita(servizio.split(".", 1)[0]),
                    self._funzioni[servizio],
                ),
                schema,
            )
            nomi[servizio] = f"{dominio}.{nome}"
        return nomi
