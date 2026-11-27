"""Gli aiutanti di oggi a confronto con i domini di domani (fase 4), con Home Assistant.

Ogni prova mette nello stesso Home Assistant un aiutante del package (``input_boolean``,
``input_number``, ``input_select``, ``input_text``, ``input_datetime``, ``timer``) e
l'entità minima del dominio che lo sostituisce (``aiutanti_nativi.py``), fa le stesse
cose a tutti e due e dice dove lo stato, gli attributi, gli errori, il contesto e il
ripristino sono uguali e dove no. È la prova delle righe della tabella di compatibilità
del resoconto della fase 4.
"""

from __future__ import annotations

from datetime import UTC, datetime, time, timedelta
from typing import Any

import probatio
import pytest
from freezegun.api import FrozenDateTimeFactory
from homeassistant.const import EVENT_CALL_SERVICE, EVENT_STATE_CHANGED
from homeassistant.core import Context, Event, HomeAssistant, State, callback
from homeassistant.exceptions import ServiceNotFound, ServiceValidationError
from homeassistant.helpers import restore_state
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.json import json_bytes
from homeassistant.setup import async_setup_component
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import (
    MockUser,
    async_fire_time_changed,
)

import custom_components.vmc_master  # noqa: F401  (si prova anche da solo)

from .aiutanti_nativi import (
    InterruttoreNativo,
    NumeroNativo,
    OraNativa,
    PulsanteNativo,
    ScadenzaNativa,
    SceltaNativa,
    ScritturaNativa,
    SpiaNativa,
    TestoNativo,
    aggiungi,
)

T0 = datetime(2026, 11, 25, 10, 0, 0, tzinfo=UTC)
NUMERO = {"min": 0, "max": 10000000000000000000000, "step": 0.0001}
SCELTA = {"options": ["Velocità 0", "Velocità 1", "Notturna"]}
ORA = {"has_date": False, "has_time": True}


async def _prepara(
    hass: HomeAssistant, vecchi: dict[str, dict[str, Any]], nativi: list[Entity]
) -> None:
    assert await async_setup_component(hass, "homeassistant", {})
    for dominio, voci in vecchi.items():
        assert await async_setup_component(hass, dominio, {dominio: voci})
    await aggiungi(hass, nativi)
    await hass.async_block_till_done()


def _stato(hass: HomeAssistant, entita: str) -> str:
    stato = hass.states.get(entita)
    assert stato is not None, entita
    return stato.state


def _attributi(hass: HomeAssistant, entita: str) -> set[str]:
    stato = hass.states.get(entita)
    assert stato is not None, entita
    return set(stato.attributes)


async def _chiama(
    hass: HomeAssistant, servizio: str, entita: str | list[str], **dati: Any
) -> Context:
    contesto = Context()
    dominio, nome = servizio.split(".")
    await hass.services.async_call(
        dominio, nome, {"entity_id": entita, **dati}, blocking=True, context=contesto
    )
    return contesto


def _ricorda(
    hass: HomeAssistant, stati: list[tuple[str, str, dict[str, Any] | None]]
) -> None:
    """Mette nella memoria del ripristino gli ultimi stati di «prima del riavvio».

    Nel 2026.11 la memoria è per voce del registro delle entità: uno stato salvato
    per entity_id passa alla voce del registro quando l'entità viene creata. (Il
    ``mock_restore_cache`` del plugin di prova scrive ancora ``last_states``, che
    questa versione non legge più: qui si riempie la memoria vera.)
    """
    memoria = restore_state.async_get(hass)
    for entita, stato, dati in stati:
        in_piu = None if dati is None else restore_state.RestoredExtraData(dati)
        memoria.last_states_by_entity_id[entita] = restore_state.StoredState(
            State(entita, stato), in_piu, T0
        )


def _cambi(hass: HomeAssistant) -> list[tuple[str, str]]:
    """Registra i cambi di stato: (entity_id, nuovo stato)."""
    visti: list[tuple[str, str]] = []

    @callback
    def annota(evento: Event) -> None:
        visti.append((evento.data["entity_id"], evento.data["new_state"].state))

    hass.bus.async_listen(EVENT_STATE_CHANGED, annota)
    return visti


# --- input_boolean -> switch / binary_sensor ------------------------------------------------


async def test_acceso_spento(hass: HomeAssistant) -> None:
    """Stato on/off identico; ``editable`` c'è solo nell'aiutante; una spia
    (binary_sensor) non ha servizi: la scrive solo chi la possiede."""
    interruttore = InterruttoreNativo("switch.a", {"name": "A"})
    spia = SpiaNativa("binary_sensor.a", {"name": "A"})
    await _prepara(hass, {"input_boolean": {"a": {"name": "A"}}}, [interruttore, spia])
    tutte = ("input_boolean.a", "switch.a", "binary_sensor.a")
    assert [_stato(hass, e) for e in tutte] == ["off", "off", "off"]

    await _chiama(hass, "input_boolean.turn_on", "input_boolean.a")
    await _chiama(hass, "switch.turn_on", "switch.a")
    spia.imposta(True)
    assert [_stato(hass, e) for e in tutte] == ["on", "on", "on"]

    assert _attributi(hass, "input_boolean.a") == {"editable", "friendly_name"}
    assert _attributi(hass, "switch.a") == {"friendly_name"}
    assert _attributi(hass, "binary_sensor.a") == {"friendly_name"}

    # toggle c'è in tutti e due i domini con servizi; il binary_sensor non ne ha
    for servizio in ("turn_on", "turn_off", "toggle"):
        assert hass.services.has_service("input_boolean", servizio)
        assert hass.services.has_service("switch", servizio)
        assert not hass.services.has_service("binary_sensor", servizio)
    with pytest.raises(ServiceNotFound):
        await _chiama(hass, "binary_sensor.turn_off", "binary_sensor.a")
    # homeassistant.turn_off sceglie il servizio dal dominio: sulla spia non fa nulla
    await _chiama(hass, "homeassistant.turn_off", "input_boolean.a")
    await _chiama(hass, "homeassistant.turn_off", "switch.a")
    await _chiama(hass, "homeassistant.turn_off", "binary_sensor.a")
    assert [_stato(hass, e) for e in tutte] == ["off", "off", "on"]


async def test_ordine_delle_scritture_di_una_chiamata(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory
) -> None:
    """Una chiamata con più entità (il package ne fa con decine di spie) le scrive
    tutte nello stesso istante e con lo stesso contesto, ma NON nell'ordine
    dell'elenco: Home Assistant le prende da un insieme (``helpers/service.py``), cioè
    in un ordine che cambia a ogni avvio. Vale per ``input_boolean`` e per ``switch``.
    Chi confronta due registri non deve guardare l'ordine dentro una chiamata."""
    freezer.move_to(T0)
    nomi = [f"spia_{numero:02d}" for numero in range(12)]
    await _prepara(
        hass,
        {"input_boolean": {nome: {} for nome in nomi}},
        [InterruttoreNativo(f"switch.{nome}") for nome in nomi],
    )
    visti: list[tuple[str, str, datetime]] = []

    @callback
    def annota(evento: Event) -> None:
        nuovo = evento.data["new_state"]
        visti.append((nuovo.entity_id, evento.context.id, nuovo.last_changed))

    hass.bus.async_listen(EVENT_STATE_CHANGED, annota)
    for dominio in ("input_boolean", "switch"):
        visti.clear()
        elenco = [f"{dominio}.{nome}" for nome in nomi]
        contesto = await _chiama(hass, f"{dominio}.turn_on", elenco)
        ordine = [entita for entita, _, _ in visti]
        assert sorted(ordine) == elenco
        assert ordine != elenco  # 12 entità: per caso in ordine una volta su 12!
        assert {(c, quando) for _, c, quando in visti} == {(contesto.id, T0)}


# --- input_number -> number -------------------------------------------------------------------


@pytest.mark.parametrize(
    ("valore", "testo"),
    [
        (0, "0.0"),
        (12, "12.0"),
        (12.5, "12.5"),
        (0.1 + 0.2, "0.3"),
        (1234567.8912, "1234567.8912"),
        (10000000000000000000000, "1e+22"),
    ],
)
async def test_numero_stesso_testo_dello_stato(
    hass: HomeAssistant, valore: float, testo: str
) -> None:
    """Lo stato di un ``number`` che tiene un float è scritto come ``input_number``
    (nel 2026.11 ``input_number`` È un ``NumberEntity``): «12.0», mai «12»."""
    await _prepara(
        hass, {"input_number": {"n": NUMERO}}, [NumeroNativo("number.n", NUMERO)]
    )
    await _chiama(hass, "input_number.set_value", "input_number.n", value=valore)
    await _chiama(hass, "number.set_value", "number.n", value=valore)
    assert _stato(hass, "input_number.n") == testo
    assert _stato(hass, "number.n") == testo


async def test_numero_fuori_intervallo_e_attributi(hass: HomeAssistant) -> None:
    """Fuori da min/max nessuno dei due taglia il valore: tutti e due rifiutano, ma con
    un errore diverso. ``initial`` ed ``editable`` ci sono solo nell'aiutante;
    ``increment``/``decrement`` anche."""
    config = {"min": 1, "max": 300, "step": 1, "mode": "box", "initial": 5}
    await _prepara(
        hass, {"input_number": {"n": config}}, [NumeroNativo("number.n", config)]
    )
    with pytest.raises(probatio.Invalid) as vecchio:
        await _chiama(hass, "input_number.set_value", "input_number.n", value=301)
    assert not isinstance(vecchio.value, ServiceValidationError)
    with pytest.raises(ServiceValidationError):
        await _chiama(hass, "number.set_value", "number.n", value=301)
    assert _stato(hass, "input_number.n") == _stato(hass, "number.n") == "5.0"

    # «5.0» solo perché il valore nativo è un float: con un intero lo stato è «5»
    intero = NumeroNativo("number.intero", config)
    intero._attr_native_value = 5
    await aggiungi(hass, [intero])
    assert _stato(hass, "number.intero") == "5"

    comuni = {"min", "max", "step", "mode"}
    assert _attributi(hass, "input_number.n") == comuni | {"initial", "editable"}
    assert _attributi(hass, "number.n") == comuni
    for servizio in ("increment", "decrement"):
        assert hass.services.has_service("input_number", servizio)
        assert not hass.services.has_service("number", servizio)


def test_numero_limiti_interi_oltre_i_64_bit() -> None:
    """Il package ha un ``input_number`` con ``max: 10000000000000000000000`` (lo YAML
    lo legge come intero): l'aiutante lo rende float nello schema. Un ``number`` nativo
    che lo tenesse intero non potrebbe salvare le sue capacità nel registro delle
    entità (JSON di Home Assistant: interi fino a 64 bit)."""
    assert isinstance(NUMERO["max"], int)
    with pytest.raises(TypeError, match="Integer exceeds 64-bit range"):
        json_bytes({"max": NUMERO["max"]})
    assert json_bytes({"max": float(NUMERO["max"])}) == b'{"max":1e+22}'


# --- input_select -> select -------------------------------------------------------------------


async def test_scelta(hass: HomeAssistant) -> None:
    """Stessa opzione come stato, stesso errore per un'opzione che non c'è (nessuno dei
    due cambia stato). ``set_options`` c'è solo in ``input_select``."""
    await _prepara(
        hass, {"input_select": {"s": SCELTA}}, [SceltaNativa("select.s", SCELTA)]
    )
    assert _stato(hass, "input_select.s") == _stato(hass, "select.s") == "Velocità 0"
    for servizio, entita in (
        ("input_select", "input_select.s"),
        ("select", "select.s"),
    ):
        await _chiama(hass, f"{servizio}.select_option", entita, option="Notturna")
        with pytest.raises(ServiceValidationError):
            await _chiama(hass, f"{servizio}.select_option", entita, option="Boh")
        assert _stato(hass, entita) == "Notturna"
        for nome in ("select_first", "select_last", "select_next", "select_previous"):
            assert hass.services.has_service(servizio, nome)
    assert hass.services.has_service("input_select", "set_options")
    assert not hass.services.has_service("select", "set_options")
    assert _attributi(hass, "input_select.s") == {"options", "editable"}
    assert _attributi(hass, "select.s") == {"options"}
    # set_options cambia anche lo stato se l'opzione corrente sparisce
    await _chiama(hass, "input_select.set_options", "input_select.s", options=["x"])
    assert _stato(hass, "input_select.s") == "x"


# --- input_text -> text -----------------------------------------------------------------------


async def test_testo(hass: HomeAssistant, caplog: pytest.LogCaptureFixture) -> None:
    """Stesso testo come stato (anche vuoto, e «unknown» senza valore iniziale). Un
    testo troppo lungo: ``input_text`` avvisa nel registro e la chiamata riesce,
    ``text`` solleva un errore."""
    config = {"max": 10}
    await _prepara(hass, {"input_text": {"t": config}}, [TestoNativo("text.t", config)])
    assert _stato(hass, "input_text.t") == _stato(hass, "text.t") == "unknown"
    for valore in ("abc", ""):
        await _chiama(hass, "input_text.set_value", "input_text.t", value=valore)
        await _chiama(hass, "text.set_value", "text.t", value=valore)
        assert _stato(hass, "input_text.t") == _stato(hass, "text.t") == valore

    await _chiama(hass, "input_text.set_value", "input_text.t", value="x" * 11)
    assert "Invalid value: xxxxxxxxxxx (length range 0 - 10)" in caplog.text
    with pytest.raises(ServiceValidationError):
        await _chiama(hass, "text.set_value", "text.t", value="x" * 11)
    assert _stato(hass, "input_text.t") == _stato(hass, "text.t") == ""

    comuni = {"min", "max", "pattern", "mode"}
    assert _attributi(hass, "input_text.t") == comuni | {"editable"}
    assert _attributi(hass, "text.t") == comuni


# --- input_datetime (solo ora) -> time --------------------------------------------------------


async def test_ora(hass: HomeAssistant) -> None:
    """Stesso stato «HH:MM:SS». Gli attributi dell'aiutante (``timestamp``, ``hour``...)
    non ci sono nel ``time``; ``time.set_value`` accetta solo ``time``."""
    await _prepara(hass, {"input_datetime": {"o": ORA}}, [OraNativa("time.o")])
    assert _stato(hass, "input_datetime.o") == _stato(hass, "time.o") == "00:00:00"
    for valore, atteso in (("07:30:00", "07:30:00"), ("21:05", "21:05:00")):
        await _chiama(
            hass, "input_datetime.set_datetime", "input_datetime.o", time=valore
        )
        await _chiama(hass, "time.set_value", "time.o", time=valore)
        assert _stato(hass, "input_datetime.o") == _stato(hass, "time.o") == atteso

    assert _attributi(hass, "input_datetime.o") == {
        "has_date",
        "has_time",
        "editable",
        "hour",
        "minute",
        "second",
        "timestamp",
    }
    assert _attributi(hass, "time.o") == set()

    # set_datetime con timestamp (secondi dall'epoca, letti nell'ora locale): solo
    # l'aiutante; il package usa sempre e solo ``time:``
    await _chiama(
        hass, "input_datetime.set_datetime", "input_datetime.o", timestamp=3600 * 5
    )
    locale = dt_util.as_local(datetime.fromtimestamp(3600 * 5, UTC))
    assert _stato(hass, "input_datetime.o") == locale.strftime("%H:%M:%S")
    with pytest.raises(probatio.Invalid):
        await _chiama(hass, "time.set_value", "time.o", timestamp=3600 * 5)


async def test_ora_con_le_frazioni_di_secondo(hass: HomeAssistant) -> None:
    """Il testo dello stato potrebbe differire solo con le frazioni di secondo
    (``strftime`` le taglia, ``isoformat`` le scrive), ma dai servizi non ci si
    arriva: tutti e due rifiutano un'ora con le frazioni."""
    await _prepara(hass, {"input_datetime": {"o": ORA}}, [OraNativa("time.o")])
    with pytest.raises(probatio.Invalid):
        await _chiama(
            hass, "input_datetime.set_datetime", "input_datetime.o", time="07:30:15.5"
        )
    with pytest.raises(probatio.Invalid):
        await _chiama(hass, "time.set_value", "time.o", time="07:30:15.5")
    assert _stato(hass, "input_datetime.o") == _stato(hass, "time.o") == "00:00:00"
    # scritto da chi lo possiede con le frazioni, il ``time`` le mostra
    ora = OraNativa("time.frazioni")
    ora._attr_native_value = time(7, 30, 15, 500000)
    await aggiungi(hass, [ora])
    assert _stato(hass, "time.frazioni") == "07:30:15.500000"


# --- timer -> sensore con l'istante di fine ---------------------------------------------------


async def test_timer_e_sensore_della_scadenza(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory
) -> None:
    """Un timer ha stato idle/active/paused, attributi, servizi ed eventi propri; un
    sensore «timestamp» ha per stato l'istante di fine e nient'altro."""
    freezer.move_to(T0 + timedelta(seconds=0.4))
    scadenza = ScadenzaNativa("sensor.t")
    await _prepara(hass, {"timer": {"t": {"duration": "00:01:00"}}}, [scadenza])
    eventi: list[tuple[str, dict[str, Any]]] = []
    for nome in ("started", "restarted", "cancelled", "finished", "paused"):
        hass.bus.async_listen(
            f"timer.{nome}", lambda e: eventi.append((e.event_type, dict(e.data)))
        )
    assert _stato(hass, "timer.t") == "idle"
    assert _stato(hass, "sensor.t") == "unknown"

    await _chiama(hass, "timer.start", "timer.t", duration=10)
    scadenza.imposta(T0 + timedelta(seconds=10))
    timer = hass.states.get("timer.t")
    assert timer is not None
    assert timer.state == "active"
    # il timer parte dal secondo intero: finisce 0,4 s prima di «adesso + 10 s»
    assert timer.attributes["finishes_at"] == "2026-11-25T10:00:10+00:00"
    assert timer.attributes["duration"] == "0:00:10"
    assert timer.attributes["remaining"] == "0:00:10"
    assert set(timer.attributes) == {
        "duration",
        "editable",
        "last_transition",
        "finishes_at",
        "remaining",
    }
    assert _stato(hass, "sensor.t") == "2026-11-25T10:00:10+00:00"
    assert _attributi(hass, "sensor.t") == {"device_class"}

    freezer.move_to(T0 + timedelta(seconds=10))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()
    assert _stato(hass, "timer.t") == "idle"
    assert [nome for nome, _ in eventi] == ["timer.started", "timer.finished"]
    assert eventi[1][1] == {
        "entity_id": "timer.t",
        "finished_at": "2026-11-25T10:00:10+00:00",
    }
    # il sensore resta sull'istante passato finché chi lo possiede non lo cambia
    assert _stato(hass, "sensor.t") == "2026-11-25T10:00:10+00:00"

    # annullare un timer fermo non scrive lo stato e non manda eventi
    cambi = _cambi(hass)
    await _chiama(hass, "timer.cancel", "timer.t")
    assert cambi == []
    assert len(eventi) == 2
    for servizio in ("start", "pause", "cancel", "finish", "change"):
        assert hass.services.has_service("timer", servizio)
    assert not hass.services.async_services_for_domain("sensor")


@pytest.mark.parametrize(("durata", "stesso"), [(3, True), (10, False)])
async def test_timer_contesto_alla_scadenza(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory, durata: int, stesso: bool
) -> None:
    """Il cambio di stato alla scadenza porta il contesto di chi ha avviato il timer
    solo se scade entro 5 secondi (``CONTEXT_RECENT_TIME_SECONDS``); dopo, un contesto
    nuovo. L'evento ``timer.finished`` ha sempre un contesto suo."""
    freezer.move_to(T0)
    await _prepara(hass, {"timer": {"t": {}}}, [])
    contesti: list[Context] = []
    hass.bus.async_listen("timer.finished", lambda e: contesti.append(e.context))
    avvio = await _chiama(hass, "timer.start", "timer.t", duration=durata)
    assert hass.states.get("timer.t").context is avvio
    freezer.move_to(T0 + timedelta(seconds=durata))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()
    fine = hass.states.get("timer.t")
    assert fine.state == "idle"
    assert (fine.context.id == avvio.id) is stesso
    assert len(contesti) == 1
    assert contesti[0].id != avvio.id


# --- scritture uguali, contesto, ripristino ---------------------------------------------------


async def test_scrivere_lo_stesso_valore_non_cambia_lo_stato(
    hass: HomeAssistant,
) -> None:
    """Riscrivere il valore che c'è già non manda ``state_changed``: vale per gli
    aiutanti e per le entità native (lo decide la macchina degli stati). Fa eccezione
    il timer, che riparte."""
    interruttore = InterruttoreNativo("switch.a")
    spia = SpiaNativa("binary_sensor.a")
    nativi = [
        interruttore,
        spia,
        NumeroNativo("number.n", NUMERO),
        SceltaNativa("select.s", SCELTA),
        TestoNativo("text.t", {"initial": ""}),
        OraNativa("time.o"),
    ]
    vecchi = {
        "input_boolean": {"a": {}},
        "input_number": {"n": NUMERO},
        "input_select": {"s": SCELTA},
        "input_text": {"t": {"initial": ""}},
        "input_datetime": {"o": ORA},
        "timer": {"t": {"duration": 30}},
    }
    await _prepara(hass, vecchi, nativi)
    scrittura = ScritturaNativa(hass, [interruttore, spia])
    chiamate = [
        ("input_boolean.turn_off", "input_boolean.a", {}),
        ("switch.turn_off", "switch.a", {}),
        ("nativa_prova.turn_off", "binary_sensor.a", {}),
        ("input_number.set_value", "input_number.n", {"value": 0}),
        ("number.set_value", "number.n", {"value": 0}),
        ("input_select.select_option", "input_select.s", {"option": "Velocità 0"}),
        ("select.select_option", "select.s", {"option": "Velocità 0"}),
        ("input_text.set_value", "input_text.t", {"value": ""}),
        ("text.set_value", "text.t", {"value": ""}),
        ("input_datetime.set_datetime", "input_datetime.o", {"time": "00:00:00"}),
        ("time.set_value", "time.o", {"time": "00:00:00"}),
    ]
    cambi = _cambi(hass)
    for servizio, entita, dati in chiamate:
        await _chiama(hass, servizio, entita, **dati)
        await _chiama(hass, "homeassistant.update_entity", entita)
    assert cambi == []
    assert scrittura.mancanti == []

    await _chiama(hass, "timer.start", "timer.t")
    await _chiama(hass, "timer.start", "timer.t")
    assert cambi == [("timer.t", "active"), ("timer.t", "active")]
    await _chiama(hass, "timer.cancel", "timer.t")


async def test_il_cambio_porta_il_contesto_della_chiamata(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory
) -> None:
    """Lo stato scritto da un servizio porta il contesto della chiamata (utente e
    contesto genitore compresi): per l'aiutante, per lo switch e, se chi la scrive glielo
    passa, per la spia. Scritta SENZA contesto, la spia riusa per 5 secondi l'ultimo
    che le è stato dato: chi la scrive deve passarlo sempre."""
    freezer.move_to(T0)
    interruttore = InterruttoreNativo("switch.a")
    spia = SpiaNativa("binary_sensor.a")
    await _prepara(hass, {"input_boolean": {"a": {}}}, [interruttore, spia])
    ScritturaNativa(hass, [interruttore, spia])
    utente = MockUser(is_owner=True).add_to_hass(hass)
    for servizio, entita in (
        ("input_boolean.turn_on", "input_boolean.a"),
        ("switch.turn_on", "switch.a"),
        ("nativa_prova.turn_on", "binary_sensor.a"),
        ("nativa_prova.turn_off", "switch.a"),
    ):
        contesto = Context(user_id=utente.id, parent_id="genitore")
        dominio, nome = servizio.split(".")
        await hass.services.async_call(
            dominio, nome, {"entity_id": entita}, blocking=True, context=contesto
        )
        stato = hass.states.get(entita)
        assert stato is not None
        assert stato.context is contesto, servizio
    # scritta senza contesto entro 5 secondi (``CONTEXT_RECENT_TIME_SECONDS``): lo
    # stato porta ancora il contesto della chiamata di prima, che non c'entra
    ultimo = hass.states.get("binary_sensor.a").context
    freezer.move_to(T0 + timedelta(seconds=4.9))
    spia.imposta(False)
    assert hass.states.get("binary_sensor.a").context is ultimo
    # passati i 5 secondi ne prende uno nuovo, senza utente e senza genitore
    freezer.move_to(T0 + timedelta(seconds=10))
    spia.imposta(True)
    nuovo = hass.states.get("binary_sensor.a").context
    assert nuovo.id != ultimo.id
    assert (nuovo.user_id, nuovo.parent_id) == (None, None)


async def test_ripristino_dopo_il_riavvio(hass: HomeAssistant) -> None:
    """Dopo un riavvio: con ``initial`` vale ``initial``, senza vale l'ultimo stato, e
    senza ultimo stato il valore di partenza del dominio. Le entità native lo rifanno
    uguale (il numero con i suoi dati in più, come ``input_number``)."""
    numero = {"native_max_value": 100, "native_min_value": 0, "native_step": 1,
              "native_unit_of_measurement": None, "native_value": 7.0}  # fmt: skip
    fuori = dict(numero, native_value=500.0)
    _ricorda(
        hass,
        [
            ("input_number.n", "7.0", numero),
            ("number.n", "7.0", numero),
            ("input_number.fuori", "500.0", fuori),
            ("number.fuori", "500.0", fuori),
            ("input_boolean.a", "on", None),
            ("switch.a", "on", None),
            ("binary_sensor.a", "on", None),
            ("input_boolean.con_iniziale", "on", None),
            ("switch.con_iniziale", "on", None),
            ("input_select.s", "Notturna", None),
            ("select.s", "Notturna", None),
            ("input_select.sparita", "Non c'è più", None),
            ("select.sparita", "Non c'è più", None),
            ("input_text.t", "ciao", None),
            ("text.t", "ciao", None),
            ("input_datetime.o", "06:15:00", None),
            ("time.o", "06:15:00", None),
            ("timer.t", "active", None),
        ],
    )
    limiti = {"min": 0, "max": 100, "step": 1}
    vecchi = {
        "input_boolean": {"a": {}, "con_iniziale": {"initial": False}, "nuovo": {}},
        "input_number": {"n": limiti, "fuori": limiti, "nuovo": dict(limiti, min=2)},
        "input_select": {"s": SCELTA, "sparita": SCELTA},
        "input_text": {"t": {}, "nuovo": {}},
        "input_datetime": {"o": ORA, "nuova": ORA},
        "timer": {"t": {"duration": 30}},
    }
    nativi = [
        InterruttoreNativo("switch.a"),
        SpiaNativa("binary_sensor.a"),
        InterruttoreNativo("switch.con_iniziale", {"initial": False}),
        InterruttoreNativo("switch.nuovo"),
        NumeroNativo("number.n", limiti),
        NumeroNativo("number.fuori", limiti),
        NumeroNativo("number.nuovo", dict(limiti, min=2)),
        SceltaNativa("select.s", SCELTA),
        SceltaNativa("select.sparita", SCELTA),
        TestoNativo("text.t"),
        TestoNativo("text.nuovo"),
        OraNativa("time.o"),
        OraNativa("time.nuova"),
    ]
    await _prepara(hass, vecchi, nativi)
    attesi = {
        ("input_boolean.a", "switch.a", "binary_sensor.a"): "on",
        ("input_boolean.con_iniziale", "switch.con_iniziale"): "off",
        ("input_boolean.nuovo", "switch.nuovo"): "off",
        ("input_number.n", "number.n"): "7.0",
        ("input_number.fuori", "number.fuori"): "0.0",
        ("input_number.nuovo", "number.nuovo"): "2.0",
        ("input_select.s", "select.s"): "Notturna",
        ("input_select.sparita", "select.sparita"): "Velocità 0",
        ("input_text.t", "text.t"): "ciao",
        ("input_text.nuovo", "text.nuovo"): "unknown",
        ("input_datetime.o", "time.o"): "06:15:00",
        ("input_datetime.nuova", "time.nuova"): "00:00:00",
        ("timer.t",): "idle",  # nessun timer del package ha restore: true
    }
    for entita, atteso in attesi.items():
        assert {e: _stato(hass, e) for e in entita} == dict.fromkeys(entita, atteso)


async def test_ripristino_senza_dati_in_piu(hass: HomeAssistant) -> None:
    """Uno stato salvato senza i dati del numero (un aiutante di prima): l'aiutante lo
    rilegge dal testo dello stato (fino alla 2027.5), il ``RestoreNumber`` nativo no:
    chi migra deve portare il valore."""
    _ricorda(hass, [("input_number.n", "7.0", None), ("number.n", "7.0", None)])
    limiti = {"min": 0, "max": 100, "step": 1}
    await _prepara(
        hass, {"input_number": {"n": limiti}}, [NumeroNativo("number.n", limiti)]
    )
    assert _stato(hass, "input_number.n") == "7.0"
    assert _stato(hass, "number.n") == "0.0"


async def test_ripristino_non_passa_da_un_dominio_all_altro(
    hass: HomeAssistant,
) -> None:
    """L'ultimo stato è legato all'entità che l'ha salvato: lo ``switch`` che prende il
    posto di un ``input_boolean`` acceso parte spento. Chi migra deve portare il
    valore (e, la prima volta, scriverlo con il suo contesto)."""
    _ricorda(hass, [("input_boolean.a", "on", None)])
    await _prepara(hass, {"input_boolean": {"a": {}}}, [InterruttoreNativo("switch.a")])
    assert _stato(hass, "input_boolean.a") == "on"
    assert _stato(hass, "switch.a") == "off"


# --- script / shell_command -> button ---------------------------------------------------------


async def test_comando_e_pulsante(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory
) -> None:
    """Un ``shell_command`` non ha entità né stato: chi lo ascolta (17 trigger del
    package) guarda l'evento ``call_service`` con dominio ``shell_command`` e il nome
    del comando. Premere un ``button`` manda ``call_service`` con dominio ``button``,
    servizio ``press`` e l'entità nei dati; lo stato del pulsante è l'istante della
    pressione e il contesto della chiamata arriva a chi lo riceve."""
    freezer.move_to(T0)
    pulsante = PulsanteNativo("button.velocita_1")
    assert await async_setup_component(
        hass, "shell_command", {"shell_command": {"velocita_1": "true"}}
    )
    await _prepara(hass, {}, [pulsante])
    assert _stato(hass, "button.velocita_1") == "unknown"
    assert hass.states.get("shell_command.velocita_1") is None
    chiamate: list[tuple[str, str, dict[str, Any]]] = []

    @callback
    def annota(evento: Event) -> None:
        dati = evento.data
        chiamate.append((dati["domain"], dati["service"], dict(dati["service_data"])))

    hass.bus.async_listen(EVENT_CALL_SERVICE, annota)
    await hass.services.async_call("shell_command", "velocita_1", {}, blocking=True)
    contesto = await _chiama(hass, "button.press", "button.velocita_1")
    assert chiamate == [
        ("shell_command", "velocita_1", {}),
        ("button", "press", {"entity_id": "button.velocita_1"}),
    ]
    assert pulsante.premute == [contesto]
    stato = hass.states.get("button.velocita_1")
    assert stato is not None
    assert stato.state == "2026-11-25T10:00:00+00:00"
    assert stato.context is contesto
