"""Prove della b36, Velocità 1 scelta dall'utente dopo il ritorno della corrente e prima del ripristino (Foglio A23).

Il blocco in testa agli 8 rami «Black-Out Off» riconosce una scelta dalla lettura cambiata, ma non la Velocità 1: dopo
un Black-Out la VMC può riaccendersi da sola a Velocità 1 e allora la lettura non cambia. Il ramo «Black-Out Scelta
Vel. 1» la riconosce al momento della scelta:
- dal Telecomando o dalla scheda: il comando shell_command.vmc_master_velocita_1 inviato da un utente (evento
  call_service con context.user_id), con la VMC già a Velocità 1;
- da qualsiasi parte (anche dall'App): la lettura grezza della VMC che passa a 00001 da un'altra velocità letta (la
  ripartenza della VMC dopo un Black-Out arriva invece da una lettura fallita, unavailable).
Con la VMC ON-Line e il ripristino di una velocità diversa dalla Velocità 1 in attesa: nessun comando, spie del
Black-Out spente (il ripristino non avviene) e memorie Inquinanti azzerate con CO2 o VOC in allerta, come nel blocco
degli 8 rami. Resta irriconoscibile solo la Velocità 1 scelta dall'App con la VMC già a Velocità 1.
"""

from __future__ import annotations

from typing import Any

import pytest
from homeassistant.core import Context, Event, HomeAssistant, State
from homeassistant.helpers import config_validation as cv

from tests.test_b35_allerte import BLACK_OUT, FASE, IP, LETTURA, PKG, _automazione, _ramo, _render, _spente
from tests.test_b36_allerte import CALENDARIO, _esegui, _stato

TID = "Black-Out Scelta Vel. 1"
GREZZA = "sensor.vmc_master_status_ventola"
SPIA_CO2 = "input_boolean.vmc_master_spia_co2_o_voc"
CO2 = "sensor.vmc_master_alert_monitoraggio_co2"
VOC = "sensor.vmc_master_alert_monitoraggio_voc"
MEMORIE_INQ = [f"input_boolean.vmc_master_spia_velocita_{s}_co2_o_voc" for s in
               ("0", "1", "2", "3", "4", "notturna", "iperventilazione", "freecooling")]
STOP = "Velocità 1 scelta dall'utente dopo il ritorno della corrente mantenuta (nessun ripristino)"
CODICI = {"Velocità 0": "00000", "Velocità 1": "00001", "Velocità 2": "00002", "Velocità 3": "00003",
          "Velocità 4": "00004", "Iperventilazione": "00005", "Notturna": "00006", "Free Cooling": "00007"}


def _grezza(codice: str) -> str:
    return "VMGO," + codice + ",00000" * 14


def _evento(utente: str | None) -> dict[str, Any]:
    evento = Event("call_service", {"domain": "shell_command", "service": "vmc_master_velocita_1", "service_data": {}},
                   context=Context(user_id=utente))
    return {"trigger": {"platform": "event", "id": TID, "event": evento}}


def _cambio(da: str, a: str) -> dict[str, Any]:
    return {"trigger": {"platform": "state", "id": TID, "entity_id": GREZZA,
                        "from_state": State(GREZZA, da), "to_state": State(GREZZA, a)}}


def _stati(memoria: str = "3", letta: str = "Velocità 1", **altri: str) -> dict[str, str]:
    stati = {IP: "ON-Line", LETTURA: letta, FASE: "0", **_spente(BLACK_OUT), **_spente(CALENDARIO),
             f"input_boolean.vmc_master_spia_velocita_{memoria}": "on", SPIA_CO2: "off", CO2: "Nessuna Allerta",
             VOC: "Nessuna Allerta", **_spente(MEMORIE_INQ)}
    stati.update(altri)
    return stati


def _condizione() -> str:
    (condizione,) = _ramo(TID)["sequence"][0]["if"]
    assert condizione["condition"] == "template"
    return condizione["value_template"]


def test_due_trigger_senza_tempi() -> None:
    """Due trigger con lo stesso id, nessun «for»: l'evento del comando Velocità 1 e il cambio della lettura grezza
    tra due letture valide (non da/verso unavailable o unknown). Non sono template: la guardia li lascia passare."""
    trigger = [t for t in _automazione()["triggers"] if t.get("id") == TID]
    assert len(trigger) == 2
    evento, cambio = trigger
    assert evento["trigger"] == "event" and evento["event_type"] == "call_service"
    assert evento["event_data"] == {"domain": "shell_command", "service": "vmc_master_velocita_1"}
    assert cambio["trigger"] == "state" and cambio["entity_id"] == GREZZA
    assert cambio["not_from"] == ["unavailable", "unknown"] and cambio["not_to"] == ["unavailable", "unknown"]
    assert all("for" not in t for t in trigger)
    guardia = _automazione()["actions"][0]
    assert guardia["value_template"].startswith("{%- if trigger.platform != 'template' -%}\ntrue")


def test_ramo_senza_comandi_ne_attese() -> None:
    (passo,) = _ramo(TID)["sequence"]
    inquinanti, spegni, stop = passo["then"]
    assert sorted(inquinanti["then"][0]["target"]["entity_id"]) == sorted(MEMORIE_INQ)
    assert spegni["action"] == "input_boolean.turn_off" and sorted(spegni["target"]["entity_id"]) == sorted(
        BLACK_OUT + ["input_boolean.vmc_master_spia_calendario_black_out"])
    assert stop == {"stop": STOP}
    testo = str(passo)
    for parola in ("delay", "wait_template", "timeout", "'for'", "shell_command", "repeat"):
        assert parola not in testo, parola


async def test_ramo_valido_per_home_assistant(hass: HomeAssistant) -> None:
    cv.SCRIPT_SCHEMA(_ramo(TID)["sequence"])


def test_file_lf() -> None:
    dati = (PKG / "vmc_master_automazione.txt").read_bytes()
    assert b"\r" not in dati
    assert dati.decode("utf-8").count(f"- stop: {STOP}\n") == 1


@pytest.mark.parametrize("memoria", ["0", "2", "3", "4", "notturna", "iperventilazione", "freecooling"])
async def test_telecomando_o_scheda_con_la_vmc_gia_a_velocita_1(hass: HomeAssistant, memoria: str) -> None:
    _imposta_e = _stati(memoria)
    for e, s in _imposta_e.items():
        hass.states.async_set(e, s)
    assert _render(hass, _condizione(), _evento("utente")) is True


@pytest.mark.parametrize(
    ("utente", "altri", "atteso"),
    [
        ("utente", {}, True),
        (None, {}, False),  # comando dell'automazione (nessun utente)
        ("utente", {LETTURA: "Velocità 3"}, False),  # VMC non ancora a Velocità 1: decide il cambio della lettura
        ("utente", {"input_boolean.vmc_master_spia_velocita_1": "on"}, False),  # ripristino della Velocità 1
        ("utente", {"input_boolean.vmc_master_spia_velocita_3": "off"}, False),  # nessun ripristino in attesa
        ("utente", {IP: "OFF-Line"}, False),
        ("utente", {"input_boolean.vmc_master_spia_calendario_lunedi_1": "on"}, False),  # Fascia del Calendario
        ("utente", {FASE: "1"}, False),  # riallineamento al riavvio
        ("utente", {FASE: "4"}, True),
    ],
)
async def test_quando_vale_il_comando(hass: HomeAssistant, utente: str | None, altri: dict[str, str],
                                      atteso: bool) -> None:
    for e, s in _stati(**altri).items():
        hass.states.async_set(e, s)
    assert _render(hass, _condizione(), _evento(utente)) is atteso


@pytest.mark.parametrize(
    ("da", "a", "atteso"),
    [
        ("Velocità 3", "Velocità 1", True),  # VMC ripartita alla velocità di prima, poi Velocità 1 (anche dall'App)
        ("Velocità 0", "Velocità 1", True),  # VMC rimasta ferma, poi Velocità 1
        ("Free Cooling", "Velocità 1", True),
        ("Velocità 2", "Velocità 1", True),
        ("Velocità 1", "Velocità 3", False),
        ("Velocità 3", "Velocità 2", False),  # le altre velocità le riconosce il blocco degli 8 rami
    ],
)
async def test_quando_vale_il_cambio_della_lettura(hass: HomeAssistant, da: str, a: str, atteso: bool) -> None:
    for e, s in _stati().items():
        hass.states.async_set(e, s)
    assert _render(hass, _condizione(), _cambio(_grezza(CODICI[da]), _grezza(CODICI[a]))) is atteso


async def test_cambio_della_lettura_con_altri_campi(hass: HomeAssistant) -> None:
    """Stessa Velocità 1 con un altro campo cambiato: non è una scelta."""
    for e, s in _stati().items():
        hass.states.async_set(e, s)
    da = _grezza("00001")
    a = "VMGO,00001,00001" + ",00000" * 13
    assert _render(hass, _condizione(), _cambio(da, a)) is False


async def test_scelta_resta_nessun_comando(hass: HomeAssistant) -> None:
    comandi = await _esegui(hass, _ramo(TID)["sequence"], _stati("4"), attesa=0.5, variabili=_evento("utente"))
    assert comandi == []
    assert all(_stato(hass, e) == "off" for e in BLACK_OUT)


async def test_comando_dell_automazione_non_tocca_niente(hass: HomeAssistant) -> None:
    comandi = await _esegui(hass, _ramo(TID)["sequence"], _stati("4"), attesa=0.5, variabili=_evento(None))
    assert comandi == []
    assert _stato(hass, "input_boolean.vmc_master_spia_velocita_4") == "on"


async def test_inquinanti_in_allerta_azzera_le_memorie(hass: HomeAssistant) -> None:
    stati = _stati("3", **{SPIA_CO2: "on", CO2: "Allerta", "input_boolean.vmc_master_spia_velocita_3_co2_o_voc": "on"})
    comandi = await _esegui(hass, _ramo(TID)["sequence"], stati, attesa=0.5,
                            variabili=_cambio(_grezza("00003"), _grezza("00001")))
    assert comandi == []
    assert all(_stato(hass, e) == "off" for e in MEMORIE_INQ + BLACK_OUT)
    assert _stato(hass, SPIA_CO2) == "on"


async def test_inquinanti_rientrati_memorie_restano(hass: HomeAssistant) -> None:
    stati = _stati("3", **{SPIA_CO2: "on", "input_boolean.vmc_master_spia_velocita_3_co2_o_voc": "on"})
    await _esegui(hass, _ramo(TID)["sequence"], stati, attesa=0.5, variabili=_evento("utente"))
    assert _stato(hass, "input_boolean.vmc_master_spia_velocita_3_co2_o_voc") == "on"
    assert all(_stato(hass, e) == "off" for e in BLACK_OUT)


# ------------------------------------------------------------------ ritorno della Fascia del Calendario dopo un Black-Out
SPIA_BO_CAL = "input_boolean.vmc_master_spia_calendario_black_out"
INT_CAL = "input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario"
LETTURA_INT = "sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia"
STOP_CAL = "Velocità scelta dall'utente dopo il ritorno della corrente mantenuta (la Fascia non riparte)"


@pytest.mark.parametrize(("altri", "atteso"), [
    ({SPIA_BO_CAL: "on", "input_boolean.vmc_master_spia_calendario_martedi_2": "on"}, True),
    ({SPIA_BO_CAL: "on", "input_boolean.vmc_master_spia_calendario_martedi_2": "on", FASE: "2"}, False),
    ({SPIA_BO_CAL: "on"}, False),  # nessuna Fascia accesa
    ({"input_boolean.vmc_master_spia_calendario_martedi_2": "on"}, False),  # nessun ritorno della Fascia in attesa
])
async def test_velocita_1_nel_ritorno_della_fascia(hass: HomeAssistant, altri: dict[str, str], atteso: bool) -> None:
    stati = _stati(**altri)
    stati["input_boolean.vmc_master_spia_velocita_3"] = "off"  # nelle Fasce la rilevazione del Black-Out non è attiva
    stati.setdefault(SPIA_BO_CAL, "off")
    for e, s in stati.items():
        hass.states.async_set(e, s)
    assert _render(hass, _condizione(), _evento("utente")) is atteso


async def test_velocita_1_nel_ritorno_della_fascia_spegne_la_spia(hass: HomeAssistant) -> None:
    stati = _stati(**{SPIA_BO_CAL: "on", "input_boolean.vmc_master_spia_calendario_lunedi_1": "on"})
    stati["input_boolean.vmc_master_spia_velocita_3"] = "off"
    comandi = await _esegui(hass, _ramo(TID)["sequence"], stati, attesa=0.5,
                            variabili=_cambio(_grezza("00003"), _grezza("00001")))
    assert comandi == []
    assert _stato(hass, SPIA_BO_CAL) == "off"


def _blocco_fascia() -> dict[str, Any]:
    sequenza = _ramo("calendario_ritorno_da_black_out")["sequence"]
    (blocco,) = [p for p in sequenza if "if" in p and "then" in p and p["then"] == [{"stop": STOP_CAL}]]
    assert sequenza.index(blocco) == 2 and "choose" in sequenza[3]
    return blocco


def test_scelta_nel_ritorno_della_fascia_come_negli_8_rami() -> None:
    """Stessa condizione dei rami «Black-Out Off» (blocco gemello), solo nel ritorno normale: non nel ritorno durante
    il riallineamento al riavvio, dove le letture rinascono all'avvio di Home Assistant."""
    from tests.test_b36_scelta import CONDIZIONE
    (condizione,) = _blocco_fascia()["if"]
    assert " ".join(condizione["value_template"].split()) == " ".join(CONDIZIONE.split())
    assert STOP_CAL not in str(_ramo("calendario_ritorno_da_black_out_riallineamento"))


@pytest.mark.parametrize(("letta", "cambiata", "fascia_riparte"), [
    ("Velocità 3", 10.0, False),  # scelta dopo il ritorno: resta
    ("Velocità 1", 10.0, True),  # ripartenza della VMC da sola (o Velocità 1: la riconosce l'altro ramo)
    ("Velocità 2", 120.0, True),  # lettura di prima del Black-Out (VMC ripartita alla velocità di prima)
])
async def test_ritorno_della_fascia(hass: HomeAssistant, letta: str, cambiata: float, fascia_riparte: bool) -> None:
    import time
    adesso = time.time()
    chiamati: list[str] = []

    async def _script(call: Any) -> None:
        chiamati.append(call.service)

    hass.services.async_register("script", "vmc_master_calendario_fascia_1_on", _script)
    hass.services.async_register("script", "vmc_master_calendario_fascia_2_on", _script)
    stati = {SPIA_BO_CAL: "on", INT_CAL: "on", LETTURA_INT: letta, **_spente(CALENDARIO),
             "input_boolean.vmc_master_spia_calendario_mercoledi_1": "on"}
    hass.states.async_set(IP, "ON-Line", timestamp=adesso - 32)
    hass.states.async_set(LETTURA, letta, timestamp=adesso - cambiata)
    comandi = await _esegui(hass, _ramo("calendario_ritorno_da_black_out")["sequence"], stati, attesa=0.5)
    assert comandi == []
    assert chiamati == (["vmc_master_calendario_fascia_1_on"] if fascia_riparte else [])
    assert _stato(hass, SPIA_BO_CAL) == "off"
