"""Le attivazioni del motore (``attivazioni.py``) come i trigger di Home Assistant.

Come in ``test_seguire.py`` ogni prova fa girare gli stessi passi due volte, con un Home
Assistant nuovo e lo stesso orologio fermo: una con ``async_initialize_triggers`` e le
piattaforme di Home Assistant, una con ``inizializza_attivazioni`` e le piattaforme
riportate nel motore. Il registro (azioni chiamate con le variabili ``trigger``, il
contesto e l'istante; messaggi di ``log_cb`` e dei registri) deve essere identico.

- Entità vere: le configurazioni validate da Home Assistant
  (``async_validate_trigger_config``), cioè come le ha il motore.
- Valori interni: le configurazioni scritte come nel codice tradotto, sui valori della
  sorgente finta (con il motore) o su entità vere (con Home Assistant).
- Il trigger dei timer del motore (``altri``: ``timer.attacca_trigger_timer``, come lo
  aggancia il motore, ed ``evento_anche_su``) e le attivazioni del codice tradotto
  (``generato_fase4``) con la memoria interna vera: confronto con
  ``_inizializza_come_ha``, il codice del motore fino alla 9.0.0b45
  (``timer.inizializza_trigger``: ``async_initialize_triggers`` con le parti interne di
  Home Assistant e il trigger ``event`` di Home Assistant anche sul bus dei timer del
  motore), qui come riferimento.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Callable, Mapping
from datetime import timedelta
from types import SimpleNamespace
from typing import Any

import probatio
import pytest
from freezegun.api import FrozenDateTimeFactory
from homeassistant.components.homeassistant.triggers import event as trigger_evento
from homeassistant.const import CONF_ALIAS, CONF_ENABLED, CONF_ID, CONF_PLATFORM
from homeassistant.core import (
    CALLBACK_TYPE,
    Context,
    Event,
    EventStateChangedData,
    HomeAssistant,
    callback,
)
from homeassistant.exceptions import HomeAssistantError, TemplateError
from homeassistant.helpers.event import (
    _TRACK_STATE_CHANGE_DATA,
    _async_dispatch_entity_id_event,
    async_track_template,
)
from homeassistant.helpers.template import Template
from homeassistant.helpers.trigger import (
    TriggerData,
    TriggerInfo,
    _async_attach_trigger_cls,
    _async_get_trigger_platform,
    _async_is_legacy_trigger,
    _trigger_action_wrapper,
    async_initialize_triggers,
    async_validate_trigger_config,
    get_relative_description_key,
)
from homeassistant.util.async_ import create_eager_task

from custom_components.vmc_master.nativa.motore.attivazioni import (
    PIATTAFORME,
    evento_anche_su,
    inizializza_attivazioni,
)
from custom_components.vmc_master.nativa.motore.contesto import Contesto
from custom_components.vmc_master.nativa.motore.generato_fase4 import (
    motore as codice_fase4,
)
from custom_components.vmc_master.nativa.motore.memoria_interna import MemoriaInterna
from custom_components.vmc_master.nativa.motore.seguire import (
    cambi_interni,
    segui_modello,
)
from custom_components.vmc_master.nativa.motore.timer import (
    TRIGGER,
    attacca_trigger_timer,
    bus_del_motore,
)

from .test_seguire import (  # noqa: F401
    Banco,
    ModelloProva,
    confronta,
    corsa,
    etichette,
    ordine_dei_timer,
    tempi_casuali,
)

pytestmark = pytest.mark.usefixtures("tempi_casuali", "ordine_dei_timer")

HA = SimpleNamespace(nome="ha", inizializza=async_initialize_triggers)
MIO = SimpleNamespace(nome="mio", inizializza=inizializza_attivazioni)


# --- il riferimento: il codice del motore fino alla 9.0.0b45 ----------------------------


class _HassDelMotore:
    """Quello che il trigger ``event`` di Home Assistant usa di ``hass``, con il bus dei
    timer del motore al posto del bus di Home Assistant."""

    def __init__(self, hass: HomeAssistant) -> None:
        self.loop = hass.loop
        self.async_run_hass_job = hass.async_run_hass_job
        self.bus = bus_del_motore(hass)


async def _attacca_trigger_timer_ha(
    hass: HomeAssistant,
    conf: Mapping[str, Any],
    action: Callable[..., Any],
    info: TriggerInfo,
    platform: Any,
) -> CALLBACK_TYPE:
    """Il trigger ``event`` di Home Assistant (lo stesso codice) due volte: sul bus di
    Home Assistant, come lo attacca Home Assistant (``platform``: la piattaforma dei
    trigger ``event``); poi sul bus dei timer del motore."""
    conf_evento = {**conf, CONF_PLATFORM: "event"}
    togli = [
        await platform.async_attach_trigger(hass, conf_evento, action, info),
        await trigger_evento.async_attach_trigger(
            _HassDelMotore(hass),  # type: ignore[arg-type]
            conf_evento,
            action,
            info,
        ),
    ]

    @callback
    def togli_tutto() -> None:
        for una in togli:
            una()

    return togli_tutto


async def _inizializza_come_ha(
    hass: HomeAssistant,
    trigger_config: list[Mapping[str, Any]],
    action: Callable[..., Any],
    domain: str,
    name: str,
    log_cb: Callable[..., Any],
    variables: Any = None,
    *,
    did_not_trigger: Any = None,
) -> CALLBACK_TYPE | None:
    """``helpers.trigger.async_initialize_triggers`` (le stesse righe) con i trigger dei
    timer del motore (``TRIGGER``): stessi id, indici e ordine degli altri trigger (il
    ``timer.inizializza_trigger`` del motore fino alla 9.0.0b45)."""
    triggers: list[asyncio.Task[CALLBACK_TYPE]] = []
    for idx, conf in enumerate(trigger_config):
        if CONF_ENABLED in conf:
            enabled = conf[CONF_ENABLED]
            if hasattr(enabled, "async_render"):
                try:
                    enabled = enabled.async_render(variables, limited=True)
                except TemplateError as err:
                    log_cb(logging.ERROR, f"Error rendering enabled template: {err}")
                    continue
            if not enabled:
                continue

        trigger_key: str = conf[CONF_PLATFORM]
        # un trigger dei timer del motore è un trigger «event» di Home Assistant
        timer_del_motore = trigger_key == TRIGGER
        if timer_del_motore:
            trigger_key = "event"
        platform_domain, platform = await _async_get_trigger_platform(hass, trigger_key)
        trigger_id = conf.get(CONF_ID, f"{idx}")
        trigger_idx = f"{idx}"
        trigger_alias = conf.get(CONF_ALIAS)
        trigger_data = TriggerData(id=trigger_id, idx=trigger_idx, alias=trigger_alias)
        info = TriggerInfo(
            domain=domain,
            name=name,
            variables=variables,
            trigger_data=trigger_data,
        )

        if not await _async_is_legacy_trigger(hass, platform, trigger_key):
            if timer_del_motore:
                raise HomeAssistantError("il trigger event non è più un trigger legacy")
            trigger_descriptors = await platform.async_get_triggers(hass)
            relative_trigger_key = get_relative_description_key(
                platform_domain, trigger_key
            )
            trigger_cls = trigger_descriptors[relative_trigger_key]
            coro = _async_attach_trigger_cls(
                hass,
                trigger_cls,
                trigger_key,
                conf,  # type: ignore[arg-type]
                action,
                info,
                did_not_trigger,
            )
        else:
            action_wrapper = _trigger_action_wrapper(hass, action, conf)  # type: ignore[arg-type]
            if timer_del_motore:
                coro = _attacca_trigger_timer_ha(
                    hass, conf, action_wrapper, info, platform
                )
            else:
                coro = platform.async_attach_trigger(hass, conf, action_wrapper, info)

        triggers.append(create_eager_task(coro))

    attach_results = await asyncio.gather(*triggers, return_exceptions=True)
    removes: list[Callable[[], None]] = []

    for result in attach_results:
        if isinstance(result, HomeAssistantError):
            log_cb(logging.ERROR, f"Got error '{result}' when setting up triggers for")
        elif isinstance(result, Exception):
            log_cb(logging.ERROR, "Error setting up trigger", exc_info=result)
        elif isinstance(result, BaseException):
            raise result from None
        elif result is None:
            log_cb(  # type: ignore[unreachable]
                logging.ERROR, "Unknown error while setting up trigger (empty result)"
            )
        else:
            removes.append(result)

    if not removes:
        return None

    log_cb(logging.INFO, "Initialized trigger")

    @callback
    def remove_triggers() -> None:
        for remove in removes:
            remove()

    return remove_triggers


def _azione(b: Banco, nome: str = "azione") -> Callable[..., Any]:
    """L'azione di un'automazione (una coroutine, come ``_async_trigger_if_enabled``)."""

    async def azione(run_variables: dict[str, Any], context: Context | None = None) -> None:
        b.annota(nome, run_variables, context)

    return azione


def _azione_callback(b: Banco, nome: str) -> Callable[..., Any]:
    @callback
    def azione(run_variables: dict[str, Any], context: Context | None = None) -> None:
        b.annota(nome, run_variables, context)

    return azione


def _log_cb(b: Banco, nome: str = "log_cb") -> Callable[..., None]:
    def log_cb(livello: int, messaggio: str, **argomenti: Any) -> None:
        errore = argomenti.get("exc_info")
        b.annota(
            nome,
            livello,
            messaggio,
            None if errore is None else (type(errore).__name__, str(errore)),
        )

    return log_cb


def _prepara_validate(
    grezze: list[dict[str, Any]], *, azione_callback: bool = False
) -> Callable[[Banco], Any]:
    """Aggancia le configurazioni ``grezze`` validate da Home Assistant (come le ha il
    motore) con ``async_initialize_triggers`` o con ``inizializza_attivazioni``."""

    async def prepara(b: Banco) -> None:
        conf = await async_validate_trigger_config(b.hass, grezze)
        azione = _azione_callback(b, "azione") if azione_callback else _azione(b)
        b.oggetti["togli"] = await b.F.inizializza(
            b.hass,
            conf,
            azione,
            "automation",
            "prova",
            _log_cb(b),
            variables={"this": None},
        )
        b.annota("agganciati", b.oggetti["togli"] is not None)

    return prepara


async def come_home_assistant(
    freezer: FrozenDateTimeFactory,
    prepara: Callable[[Banco], Any],
    passi: list[tuple[Any, ...]],
    **argomenti: Any,
) -> list[Any]:
    interni = argomenti.pop("interni", ())
    atteso = await corsa(freezer, HA, prepara, passi, **argomenti)
    ottenuto = await corsa(freezer, MIO, prepara, passi, interni=interni, **argomenti)
    confronta(atteso, ottenuto)
    return atteso


def _stacca(b: Banco) -> None:
    b.oggetti.pop("togli")()


# --- entità vere ----------------------------------------------------------------------------

STATO: list[dict[str, Any]] = [
    {"platform": "state", "entity_id": "sensor.a", "to": "on", "id": "a_on", "alias": "A"},
    {"platform": "state", "entity_id": ["sensor.a", "sensor.b"]},
    {
        "platform": "state",
        "entity_id": "sensor.a",
        "from": ["off", "x"],
        "to": "on",
        "for": "00:00:05",
    },
    {
        "platform": "state",
        "entity_id": "sensor.b",
        "not_from": ["unavailable", "unknown"],
        "not_to": ["unavailable", "unknown"],
    },
    {"platform": "state", "entity_id": "sensor.a", "attribute": "livello", "to": 3},
    {"platform": "state", "entity_id": "sensor.a", "attribute": "livello"},
    {"platform": "state", "entity_id": "sensor.a", "from": "on", "for": {"seconds": "{{ 2 + 1 }}"}},
    {"platform": "state", "entity_id": "sensor.b", "to": "on", "for": 0},
    {"platform": "state", "entity_id": "sensor.b", "to": "on", "for": "{{ 'xx' }}"},
    {"platform": "state", "entity_id": "sensor.b", "to": None},
    {
        "platform": "state",
        "entity_id": ["sensor.a", "sensor.b"],
        "to": "on",
        "for": {"seconds": "{{ 4 if trigger.entity_id == 'sensor.a' else 2 }}"},
    },
]

PASSI_STATO: list[tuple[Any, ...]] = [
    ("stato", "sensor.a", "on"),
    ("stato", "sensor.b", "on", {"x": 1}),
    ("attendi", 1),
    ("stato", "sensor.a", "on", {"livello": 3}),
    ("stato", "sensor.a", "on", {"livello": 4}),
    ("attendi", 2.5),
    ("stato", "sensor.b", "off"),
    ("attendi", 2),
    ("stato", "sensor.a", "off"),
    ("stato", "sensor.a", "on", None, Context(id="dato", user_id="utente")),
    ("attendi", 1),
    ("stato", "sensor.a", "x"),
    ("stato", "sensor.a", "on"),
    ("attendi", 6),
    ("stato", "sensor.a", "off"),
    ("attendi", 1),
    ("stato", "sensor.a", "y"),
    ("attendi", 3),
    ("togli", "sensor.b"),
    ("stato", "sensor.b", "on"),
    ("attendi", 3),
    ("chiama", _stacca),
    ("stato", "sensor.a", "off"),
    ("attendi", 6),
]


async def test_state_entita_vere(freezer: FrozenDateTimeFactory) -> None:
    """Il trigger ``state``: to/from/not_from/not_to, attributo, ``for`` fisso, da modello
    (anche con ``trigger.entity_id``), zero e sbagliato, cambi che annullano l'attesa,
    entità tolta e ritornata, stacco."""
    registro = await come_home_assistant(
        freezer,
        _prepara_validate(STATO),
        PASSI_STATO,
        iniziali=[("sensor.a", "off"), ("sensor.b", "off")],
    )
    assert len(etichette(registro, "azione")) > 10
    assert etichette(registro, "messaggio")


MODELLO: list[dict[str, Any]] = [
    {"platform": "template", "value_template": "{{ is_state('sensor.a', 'on') }}", "id": "m"},
    {
        "platform": "template",
        "value_template": "{{ states('sensor.b') | int(0) > 5 }}",
        "for": {"seconds": "{{ states('sensor.c') | int(2) }}"},
    },
    {
        "platform": "template",
        "value_template": "{{ states('sensor.b') | int(0) > 7 }}",
        "for": "00:00:03",
    },
    {"platform": "template", "value_template": "{{ now().minute % 2 == 1 }}"},
    {"platform": "template", "value_template": "{{ states('sensor.d') | int > 1 }}"},
    {
        "platform": "template",
        "value_template": "{{ this is none and is_state('sensor.a', 'on') }}",
        "alias": "con this",
    },
    {
        "platform": "template",
        "value_template": "{{ is_state('sensor.a', 'on') }}",
        "for": {"seconds": "{{ 'no' }}"},
    },
]

PASSI_MODELLO: list[tuple[Any, ...]] = [
    ("stato", "sensor.a", "on"),
    ("stato", "sensor.b", "6"),
    ("attendi", 1),
    ("stato", "sensor.b", "8"),
    ("attendi", 1.5),
    ("stato", "sensor.b", "9"),
    ("attendi", 3),
    ("stato", "sensor.d", "5"),
    ("stato", "sensor.d", "testo"),
    ("stato", "sensor.d", "0"),
    ("stato", "sensor.d", "2"),
    ("stato", "sensor.a", "off"),
    ("stato", "sensor.a", "on"),
    ("stato", "sensor.c", "1"),
    ("stato", "sensor.b", "0"),
    ("stato", "sensor.b", "6"),
    ("attendi", 70),
    ("stato", "sensor.b", "0"),
    ("attendi", 60),
]


async def test_template_entita_vere(freezer: FrozenDateTimeFactory) -> None:
    """Il trigger ``template``: armato solo se prima falso, ``for`` da modello e fisso
    annullato da un cambio, ``now()``, errori all'avvio e dopo, ``this``, ``for``
    sbagliato."""
    registro = await come_home_assistant(
        freezer,
        _prepara_validate(MODELLO),
        PASSI_MODELLO,
        iniziali=[("sensor.a", "off"), ("sensor.b", "0")],
    )
    assert len(etichette(registro, "azione")) >= 5


EVENTO: list[dict[str, Any]] = [
    {"platform": "event", "event_type": "prova", "event_data": {"x": 1}},
    {"platform": "event", "event_type": ["prova", "altra"], "context": {"user_id": ["u1", "u2"]}},
    {"platform": "event", "event_type": "prova", "event_data": {"nido": {"a": 1}}},
    {"platform": "event", "event_type": "{{ 'state_reported' }}"},
    {"platform": "event", "event_type": "{{ 'prova' if this is none else 'no' }}"},
    {"platform": "event", "event_type": "prova", "context": {"user_id": "u1"}, "id": "u1"},
]

PASSI_EVENTO: list[tuple[Any, ...]] = [
    ("evento", "prova", {"x": 1, "y": 2}),
    ("evento", "prova", {"x": 2}, Context(user_id="u1")),
    ("evento", "altra", None, Context(user_id="u2")),
    ("evento", "altra", None, Context(user_id="u3")),
    ("evento", "prova", {"nido": {"a": 1, "b": 2}}),
    ("evento", "prova", {"nido": {"a": 2}}),
    ("chiama", _stacca),
    ("evento", "prova", {"x": 1}),
]


async def test_event_entita_vere(freezer: FrozenDateTimeFactory) -> None:
    """Il trigger ``event``: dati (semplici e annidati), contesto (uno o più utenti), tipi
    da modello, ``state_reported`` rifiutato all'aggancio (``log_cb``)."""
    registro = await come_home_assistant(
        freezer, _prepara_validate(EVENTO), PASSI_EVENTO
    )
    assert etichette(registro, "log_cb")


ORA: list[dict[str, Any]] = [
    {"platform": "time", "at": "02:00:30"},
    {"platform": "time", "at": ["02:00:40", "input_datetime.ora"], "id": "due"},
    {"platform": "time", "at": {"entity_id": "sensor.istante", "offset": "-00:00:10"}},
    {"platform": "time", "at": "02:01:00", "weekday": "wed"},
    {"platform": "time", "at": "02:01:00", "weekday": "thu"},
    {"platform": "time", "at": "02:01:00", "weekday": ["mon", "tue"]},
    {"platform": "time", "at": "input_datetime.data"},
    {"platform": "time_pattern", "seconds": "/20"},
    {"platform": "time_pattern", "minutes": "/1"},
    {"platform": "time_pattern", "hours": "2", "minutes": "1"},
]

ORA_INIZIALI: list[tuple[Any, ...]] = [
    (
        "input_datetime.ora",
        "02:00:50",
        {"has_date": False, "has_time": True, "hour": 2, "minute": 0, "second": 50},
    ),
    (
        "input_datetime.data",
        "2026-11-25 02:01:30",
        {
            "has_date": True,
            "has_time": True,
            "year": 2026,
            "month": 11,
            "day": 25,
            "hour": 2,
            "minute": 1,
            "second": 30,
        },
    ),
    ("sensor.istante", "2026-11-25T10:01:20+00:00", {"device_class": "timestamp"}),
]

PASSI_ORA: list[tuple[Any, ...]] = [
    ("attendi", 55),
    (
        "stato",
        "input_datetime.ora",
        "02:01:40",
        {"has_date": False, "has_time": True, "hour": 2, "minute": 1, "second": 40},
    ),
    ("stato", "sensor.istante", "2026-11-25T10:01:50+00:00", {"device_class": "timestamp"}),
    ("attendi", 70),
    ("chiama", _stacca),
    ("attendi", 30),
]


async def test_time_e_time_pattern_entita_vere(freezer: FrozenDateTimeFactory) -> None:
    """I trigger ``time`` (ora fissa, entità ``input_datetime`` con e senza data, sensore
    con un istante e uno scarto, giorni della settimana) e ``time_pattern``."""
    registro = await come_home_assistant(
        freezer, _prepara_validate(ORA), PASSI_ORA, iniziali=ORA_INIZIALI
    )
    assert len(etichette(registro, "azione")) > 10


AVVIO: list[dict[str, Any]] = [
    {"platform": "homeassistant", "event": "start", "id": "avvio"},
    {"platform": "homeassistant", "event": "shutdown"},
    {"platform": "state", "entity_id": "sensor.a"},
]


async def test_homeassistant_entita_vere(freezer: FrozenDateTimeFactory) -> None:
    """Il trigger ``homeassistant``: ``start`` all'avvio (agganciato prima),
    ``shutdown`` alla chiusura."""
    registro = await come_home_assistant(
        freezer,
        _prepara_validate(AVVIO),
        [("stato", "sensor.a", "1"), ("avvia",), ("attendi", 1), ("ferma",)],
        avvio=True,
    )
    assert len(etichette(registro, "azione")) == 3


ABILITATI: list[dict[str, Any]] = [
    {"platform": "state", "entity_id": "sensor.a", "enabled": False, "id": "spento"},
    {"platform": "state", "entity_id": "sensor.a", "enabled": "{{ this is none }}"},
    {"platform": "state", "entity_id": "sensor.a", "enabled": "{{ 1 / 0 }}"},
    {"platform": "state", "entity_id": "sensor.a", "enabled": "{{ this is not none }}"},
    {
        "platform": "state",
        "entity_id": "sensor.a",
        "variables": {"extra": "{{ trigger.to_state.state }}-x", "fisso": 3},
    },
    {"platform": "state", "entity_id": "sensor.a", "alias": "con alias", "id": "mio_id"},
]


@pytest.mark.parametrize("azione_callback", [False, True], ids=["coroutine", "callback"])
async def test_enabled_variables_id_alias(
    freezer: FrozenDateTimeFactory, azione_callback: bool
) -> None:
    """``enabled`` (anche da modello, anche sbagliato), ``variables`` del trigger con
    un'azione coroutine o callback, ``id`` (l'indice se manca), ``idx``, ``alias``."""
    registro = await come_home_assistant(
        freezer,
        _prepara_validate(ABILITATI, azione_callback=azione_callback),
        [("stato", "sensor.a", "1"), ("stato", "sensor.a", "2")],
    )
    assert etichette(registro, "log_cb")


async def test_nessun_trigger_agganciato(freezer: FrozenDateTimeFactory) -> None:
    """Tutti spenti: None, senza «Initialized trigger»."""
    registro = await come_home_assistant(
        freezer,
        _prepara_validate([{"platform": "state", "entity_id": "sensor.a", "enabled": False}]),
        [("stato", "sensor.a", "1")],
    )
    assert ["agganciati", [False]] in [list(r[1:]) for r in registro]


async def test_piattaforma_sconosciuta(hass: HomeAssistant) -> None:
    """Un trigger che nessuna piattaforma conosce: lo stesso errore di Home Assistant.
    Una piattaforma di Home Assistant che il motore non usa non c'è."""
    conf = [{"platform": "nessuna", "entity_id": ["sensor.a"]}]
    with pytest.raises(probatio.Invalid) as da_ha:
        await async_initialize_triggers(hass, conf, _nulla, "automation", "x", _nulla)
    with pytest.raises(probatio.Invalid) as dal_motore:
        await inizializza_attivazioni(hass, conf, _nulla, "automation", "x", _nulla)
    assert str(dal_motore.value) == str(da_ha.value)
    assert set(PIATTAFORME) == {
        "state",
        "template",
        "event",
        "homeassistant",
        "time",
        "time_pattern",
    }
    with pytest.raises(probatio.Invalid):
        await inizializza_attivazioni(
            hass,
            [{"platform": "numeric_state", "entity_id": ["sensor.a"], "above": 1}],
            _nulla,
            "automation",
            "x",
            _nulla,
        )


def _nulla(*_: Any, **__: Any) -> None:
    return None


# --- valori interni -------------------------------------------------------------------------


def _conf_interne(hass: HomeAssistant) -> list[dict[str, Any]]:
    """Configurazioni come nel codice tradotto, su valori interni (e un'entità vera)."""

    def acceso(leggi: Callable[[str], str], V: dict[str, Any]) -> str:
        return str(leggi("input_boolean.c") == "on")

    def soglia(leggi: Callable[[str], str], V: dict[str, Any]) -> str:
        try:
            return str(float(leggi("input_number.n")) > 5)
        except ValueError:
            return "False"

    def attesa(leggi: Callable[[str], str], V: dict[str, Any]) -> str:
        return leggi("input_number.attesa")

    def doppio(leggi: Callable[[str], str], V: dict[str, Any]) -> str:
        return str(
            leggi("input_boolean.c") == "on" and leggi("sensor.vero") == "on"
        )

    return [
        {"entity_id": ["input_boolean.c"], "to": "on", "id": "c_on", "platform": "state"},
        {"entity_id": ["input_boolean.c"], "platform": "state"},
        {
            "entity_id": ["input_boolean.c", "sensor.vero"],
            "from": "off",
            "to": "on",
            "for": timedelta(seconds=5),
            "id": "per5",
            "platform": "state",
        },
        {
            "entity_id": ["input_number.n"],
            "not_to": ["unknown", "unavailable"],
            "for": {"seconds": ModelloProva(hass, "attesa_stato", attesa)},
            "platform": "state",
        },
        {"value_template": ModelloProva(hass, "acceso", acceso), "id": "m", "platform": "template"},
        {
            "alias": "soglia con attesa",
            "value_template": ModelloProva(hass, "soglia", soglia),
            "id": "soglia",
            "for": {"seconds": ModelloProva(hass, "attesa", attesa)},
            "platform": "template",
        },
        {"value_template": ModelloProva(hass, "doppio", doppio), "platform": "template"},
        {"at": ["input_datetime.ora"], "platform": "time"},
        {"entity_id": ["input_boolean.c"], "to": "on", "id": "ultimo", "platform": "state"},
    ]


async def _prepara_interne(b: Banco) -> None:
    b.oggetti["togli"] = await b.F.inizializza(
        b.hass,
        _conf_interne(b.hass),
        _azione(b),
        "automation",
        "interna",
        _log_cb(b),
        variables={"this": None},
    )


INIZIALI_INTERNE: list[tuple[Any, ...]] = [
    ("input_boolean.c", "off"),
    ("input_number.n", "0.0"),
    ("input_number.attesa", "3"),
    ("sensor.vero", "off"),
    (
        "input_datetime.ora",
        "02:00:20",
        {"has_date": False, "has_time": True, "hour": 2, "minute": 0, "second": 20},
    ),
]

PASSI_INTERNI: list[tuple[Any, ...]] = [
    ("stato", "input_boolean.c", "on"),
    ("stato", "sensor.vero", "on"),
    ("attendi", 2),
    ("stato", "input_boolean.c", "off"),
    ("stato", "input_boolean.c", "on", None, Context(id="scelta", user_id="utente")),
    ("stato", "input_number.n", "6.0"),
    ("attendi", 2),
    ("stato", "input_number.n", "7.0"),
    ("attendi", 2),
    ("stato", "input_number.n", "4.0"),
    ("stato", "input_number.attesa", "1"),
    ("stato", "input_number.n", "8.0"),
    ("attendi", 6),
    (
        "stato",
        "input_datetime.ora",
        "02:00:30",
        {"has_date": False, "has_time": True, "hour": 2, "minute": 0, "second": 30},
    ),
    ("attendi", 20),
    ("stato", "input_boolean.c", "off"),
    ("stato", "input_number.n", "unknown"),
    ("chiama", _stacca),
    ("stato", "input_boolean.c", "on"),
    ("attendi", 6),
]


async def test_valori_interni_come_entita(freezer: FrozenDateTimeFactory) -> None:
    """Trigger ``state``, ``template`` e ``time`` su valori interni (con il motore) come
    sulle stesse entità vere (con Home Assistant): stessi trigger nello stesso ordine
    (l'ordine delle iscrizioni), stesse variabili e stessi contesti, ``for`` fisso e da
    modello annullato da un cambio intermedio, ora letta da un valore interno."""
    registro = await come_home_assistant(
        freezer,
        _prepara_interne,
        PASSI_INTERNI,
        interni=("input_boolean.c", "input_number.n", "input_number.attesa", "input_datetime.ora"),
        iniziali=INIZIALI_INTERNE,
    )
    trigger = [r[2][0]["trigger"] for r in etichette(registro, "azione")]
    # l'ordine delle iscrizioni: c_on, il trigger 1, il modello «m», poi «ultimo»
    assert [t["id"] for t in trigger[:4]] == ["c_on", "1", "m", "ultimo"]
    assert any(t["id"] == "per5" for t in trigger)
    assert any(t["id"] == "soglia" for t in trigger)
    assert any(t["platform"] == "time" for t in trigger)


# --- il trigger dei timer del motore (altri) ------------------------------------------------


async def _prepara_timer(b: Banco) -> None:
    """Il trigger dei timer del motore come lo aggancia il motore
    (``timer.attacca_trigger_timer``)."""
    await _prepara_timer_con(b, attacca_trigger_timer)


async def _prepara_timer_anche_su(b: Banco) -> None:
    """Il trigger dei timer del motore con ``evento_anche_su(bus_del_motore(hass))``."""
    await _prepara_timer_con(b, evento_anche_su(bus_del_motore(b.hass)))


async def _prepara_timer_con(b: Banco, piattaforma: Any) -> None:
    hass = b.hass
    conf = [
        {"event_type": [Template("timer.finished", hass)], "id": "scaduto", "platform": TRIGGER},
        {
            "event_type": [Template("timer.started", hass), Template("timer.cancelled", hass)],
            "event_data": {"entity_id": "timer.a"},
            "platform": TRIGGER,
        },
        {"entity_id": ["sensor.a"], "platform": "state"},
    ]
    argomenti = {"variables": {"this": None}}
    if b.mio:
        togli = await inizializza_attivazioni(
            hass,
            conf,
            _azione(b),
            "automation",
            "timer",
            _log_cb(b),
            altri={TRIGGER: piattaforma},
            **argomenti,
        )
    else:
        # il riferimento: le parti interne di Home Assistant
        togli = await _inizializza_come_ha(
            hass, conf, _azione(b), "automation", "timer", _log_cb(b), **argomenti
        )
    b.oggetti["togli"] = togli


def _lancia(tipo: str, dati: dict[str, Any]) -> Callable[[Banco], None]:
    def lancia(b: Banco) -> None:
        bus_del_motore(b.hass).lancia(tipo, dati)

    return lancia


@pytest.mark.parametrize("prepara", [_prepara_timer, _prepara_timer_anche_su])
async def test_trigger_dei_timer_del_motore(
    freezer: FrozenDateTimeFactory, prepara: Callable[[Banco], Any]
) -> None:
    """``altri`` con ``timer.attacca_trigger_timer`` (come il motore) e con
    ``evento_anche_su(bus_del_motore(hass))`` come ``_inizializza_come_ha``: gli eventi
    dei timer del motore e quelli dello stesso tipo sul bus di Home Assistant, stessi
    dati, ordine e variabili."""
    registro = await come_home_assistant(
        freezer,
        prepara,
        [
            ("chiama", _lancia("timer.finished", {"entity_id": "timer.a"})),
            ("evento", "timer.finished", {"entity_id": "timer.b"}),
            ("chiama", _lancia("timer.started", {"entity_id": "timer.a"})),
            ("chiama", _lancia("timer.started", {"entity_id": "timer.b"})),
            ("chiama", _lancia("timer.cancelled", {"entity_id": "timer.a"})),
            ("stato", "sensor.a", "1"),
            ("chiama", _stacca),
            ("chiama", _lancia("timer.finished", {"entity_id": "timer.a"})),
        ],
    )
    assert len(etichette(registro, "azione")) == 5


# --- la memoria interna vera e il codice tradotto ------------------------------------------


def _con_memoria(b: Banco, memoria: MemoriaInterna) -> None:
    """Con il motore la memoria consegna i suoi cambi a ``CambiInterni`` (ne è una
    sorgente); con Home Assistant li consegna anche come la memoria fino alla 9.0.0b45,
    nel dizionario privato di Home Assistant (a chi segue l'entità con
    ``async_track_state_change_event``), qui come riferimento."""
    assert cambi_interni(b.hass).sorgente_di(memoria.entity_ids[0]) is memoria
    if b.mio:
        return

    @callback
    def a_home_assistant(cambio: Event[EventStateChangedData]) -> None:
        if (seguiti := b.hass.data.get(_TRACK_STATE_CHANGE_DATA)) is not None:
            _async_dispatch_entity_id_event(b.hass, seguiti.callbacks, cambio)

    memoria.ascolta_cambi(a_home_assistant)


def _scrivi_memoria(dominio: str, servizio: str, dati: dict[str, Any]) -> Any:
    async def scrivi(b: Banco) -> None:
        memoria: MemoriaInterna = b.oggetti["memoria"]
        await memoria.async_chiama(dominio, servizio, dati, Context(id=f"{servizio}{dati}"))

    return scrivi


ATTESA = "input_number.vmc_master_attesa_avvisi"
RESET = "input_text.vmc_master_tempo_mancante_reset"
SPIA = "input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0"


def _attesa(valore: float) -> tuple[Any, ...]:
    """Passo: ``input_number.set_value`` sul valore interno dell'attesa degli avvisi."""
    dati = {"entity_id": ATTESA, "value": valore}
    return ("chiama", _scrivi_memoria("input_number", "set_value", dati))


def _reset(valore: str) -> tuple[Any, ...]:
    """Passo: ``input_text.set_value`` sul valore interno del reset del conto."""
    dati = {"entity_id": RESET, "value": valore}
    return ("chiama", _scrivi_memoria("input_text", "set_value", dati))


def _spia(servizio: str) -> tuple[Any, ...]:
    """Passo: ``input_boolean.<servizio>`` sulla spia interna."""
    return ("chiama", _scrivi_memoria("input_boolean", servizio, {"entity_id": SPIA}))


async def _prepara_memoria_vera(b: Banco) -> None:
    hass = b.hass
    memoria = MemoriaInterna(
        hass,
        "master",
        ("input_number.attesa_avvisi", "input_text.tempo_mancante_reset",
         "input_boolean.spia_umidita_mantenuta_velocita_0"),
    )
    memoria.ripristina()
    b.oggetti["memoria"] = memoria
    _con_memoria(b, memoria)
    c = Contesto(hass, "master")
    c.usa_memoria(memoria)

    def oltre(c: Contesto, V: Any) -> str:
        return str(float(c.states(ATTESA)) > 10 and c.is_state(SPIA, "on"))

    def secondi(c: Contesto, V: Any) -> str:
        return str(int(float(c.states(ATTESA))) // 10)

    def azzerato(c: Contesto, V: Any) -> str:
        return str(c.is_state(RESET, "reset"))

    oltre.sorgente = "oltre"  # type: ignore[attr-defined]
    secondi.sorgente = "secondi"  # type: ignore[attr-defined]
    azzerato.sorgente = "azzerato"  # type: ignore[attr-defined]
    conf = [
        {"value_template": c.modello(oltre), "for": {"seconds": c.modello(secondi)},
         "id": "oltre", "platform": "template"},
        {"entity_id": [RESET], "to": "reset", "id": "reset", "platform": "state"},
        {"entity_id": [ATTESA], "platform": "state", "id": "ogni"},
        {"entity_id": [SPIA], "from": "off", "to": "on", "for": timedelta(seconds=2),
         "id": "spia", "platform": "state"},
    ]
    b.oggetti["togli"] = await b.F.inizializza(
        hass, conf, _azione(b), "automation", "memoria", _log_cb(b),
        variables={"this": None},
    )
    segui = segui_modello if b.mio else async_track_template

    @callback
    def attesa_finita(entity_id: Any, vecchio: Any, nuovo: Any) -> None:
        b.annota("attesa", entity_id, vecchio, nuovo)

    segui(hass, c.modello(azzerato), attesa_finita)


async def test_memoria_interna_vera(freezer: FrozenDateTimeFactory) -> None:
    """Con la ``MemoriaInterna`` vera e i ``ModelloHA`` del motore: trigger ``template``
    con ``for`` da modello, ``state`` (anche con ``for`` annullato) e un'attesa
    ``wait_template`` su valori interni scritti dai servizi degli aiutanti come oggi."""
    registro = await come_home_assistant(
        freezer,
        _prepara_memoria_vera,
        [
            _attesa(20),
            _spia("turn_on"),
            ("attendi", 1),
            _spia("turn_off"),
            _spia("turn_on"),
            ("attendi", 3),
            _reset("reset"),
            _attesa(20),
            _attesa(35),
            ("attendi", 4),
            _reset("x"),
            _reset("reset"),
            _attesa(5),
            _attesa(40),
            ("attendi", 3),
            _attesa(41),
            ("attendi", 5),
        ],
    )
    trigger = [r[2][0]["trigger"]["id"] for r in etichette(registro, "azione")]
    assert trigger.count("oltre") == 2
    assert trigger.count("reset") == 2
    assert trigger.count("spia") == 1
    assert len(etichette(registro, "attesa")) == 2


async def _prepara_fase4(b: Banco) -> None:
    """Tutte le automazioni del codice tradotto, con la memoria interna vera: con Home
    Assistant come le agganciava il motore fino alla 9.0.0b45 (``_inizializza_come_ha``),
    con il motore come le aggancia oggi (``inizializza_attivazioni`` con
    ``timer.attacca_trigger_timer``)."""
    hass = b.hass
    c = Contesto(hass, "master")
    automazioni, _ = codice_fase4.crea(c)
    assert c.memoria is not None
    b.oggetti["memoria"] = c.memoria
    _con_memoria(b, c.memoria)
    togli = []
    for automazione in automazioni:
        argomenti: dict[str, Any] = {"variables": {"this": None}}
        if b.mio:
            argomenti["altri"] = {TRIGGER: attacca_trigger_timer}
            inizializza = inizializza_attivazioni
        else:
            inizializza = _inizializza_come_ha
        uno = await inizializza(
            hass,
            list(automazione.trigger),
            _azione(b, automazione.alias),
            "automation",
            automazione.alias,
            _log_cb(b, f"log {automazione.alias}"),
            **argomenti,
        )
        b.annota("agganciata", automazione.alias, uno is not None)
        if uno is not None:
            togli.append(uno)

    def stacca(b: Banco) -> None:
        for uno in togli:
            uno()

    b.oggetti["stacca"] = stacca


async def test_attivazioni_del_codice_tradotto(freezer: FrozenDateTimeFactory) -> None:
    """Le configurazioni dei trigger come le scrive il codice tradotto (``generato_fase4``,
    13 automazioni, centinaia di trigger) con la memoria interna vera: stessi trigger, stessi
    messaggi e stesse azioni con il codice di oggi e con il motore, anche ai cambi dei
    valori interni e delle entità che i trigger seguono."""
    registro = await come_home_assistant(
        freezer,
        _prepara_fase4,
        [
            ("stato", "switch.vmc_master_opzioni_vmc", "on"),
            ("stato", "switch.vmc_master_opzioni_vmc", "off"),
            ("stato", "sensor.vmc_master_status_ip_interfaccia", "ON-Line"),
            ("stato", "sensor.vmc_master_status_ip_interfaccia", "OFF-Line"),
            ("stato", "sensor.vmc_master_status_ventola", "Velocità 2"),
            ("stato", "sensor.vmc_master_status_ventola", "Velocità 1"),
            _reset("reset"),
            _attesa(7),
            ("attendi", 2.5),
            ("chiama", lambda b: b.oggetti["stacca"](b)),
            ("stato", "switch.vmc_master_opzioni_vmc", "on"),
            ("attendi", 2),
        ],
        iniziali=[
            ("switch.vmc_master_opzioni_vmc", "off"),
            ("sensor.vmc_master_status_ip_interfaccia", "OFF-Line"),
            ("sensor.vmc_master_status_ventola", "Velocità 1"),
        ],
    )
    agganciate = {r[2][0]: r[2][1] for r in etichette(registro, "agganciata")}
    assert len(agganciate) == 13
    # i suoi trigger sono tutti agganci dei comandi (spenti qui)
    assert [nome for nome, si in agganciate.items() if not si] == [
        "VMC Master - Letture Ravvicinate"
    ]
    azioni = [r for r in registro if r[1].startswith(("VMC Master", "Automazione VMC"))]
    assert azioni

