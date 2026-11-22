"""Prove della b36 (A2-1 completato, controllo d6): velocità scelta dall'utente poco prima della fine del PdR negli
ultimi 2 rami di ripristino che non la guardavano.

Il ripristino di fine PdR parte dopo il «for» del trigger (16 s, 12 s con gli Inquinanti) senza guardare la lettura,
mentre la scelta fatta durante l'allerta diventa memoria solo dopo un'altra attesa: una velocità scelta poco prima della
fine veniva sovrascritta dal ripristino. Dalla b32 (A2-1) 13 rami lo evitano; mancavano:
- «Rip. Free Cool./Heat. No PdR se Spia Inquinanti ON»: il controllo sta in ciascuno dei 3 casi che mandano il comando
  Free Cooling (Free non sospesa, «Nessuna Allerta Free Cooling Programmato», «Nessuna Allerta Free Heating
  Programmato»); non contano come scelta la Velocità 0 (PdR), la Velocità 1 (Inquinanti) e Free Cooling (la Free
  Heating si legge «Free Cooling»); i 2 casi con la Free sospesa non mandano comandi;
- «Rip. Vel. 0 No PdR» (memoria Velocità 1 Inquinanti/PdR accesa, Inquinanti finiti): non contano come scelta la
  Velocità 0 e la Velocità 1 (quella degli Inquinanti, che non si distingue da una scelta).
Con una scelta: nessun comando, memorie spente (nessun altro ripristino riparte), stop come i rami gemelli. Senza
scelta: ripristino di prima (Foglio Logiche F6, A28; regole C3-1, C3-2, A2-1).
"""

from __future__ import annotations

from typing import Any

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from tests.test_b35_allerte import (
    BLACK_OUT,
    CONFRONTO,
    FASE,
    FREE,
    FREE_C,
    FREE_H,
    INT_CO2,
    INT_PDR,
    IP,
    LETTURA,
    LETTURA_I,
    MEMORIE_CO2,
    MEMORIE_PDR,
    PARTENZA,
    SPIA_CO2,
    SPIA_DELTA,
    V1_PDR,
    _automazione,
    _imposta,
    _ramo,
    _render,
    _spente,
)
from tests.test_b36_allerte import _esegui, _stato

FREE_INQ = "Rip. Free Cool./Heat. No PdR se Spia Inquinanti ON"
VEL_0 = "Rip. Vel. 0 No PdR"
STOP = "Velocità scelta dall'utente durante l'allerta PdR mantenuta"
SPIA_GELO = "input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia"
BLACK_OUT_RILEVATO = "binary_sensor.vmc_master_black_out_rilevato"
MEMORIA_FREE = "input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio"
ESCLUSE_FREE = ["Velocità 0", "Velocità 1", "Free Cooling", "Non disponibile", "unknown", "unavailable", ""]
ESCLUSE_VEL_0 = ["Velocità 0", "Velocità 1", "Non disponibile", "unknown", "unavailable", ""]
SCELTE = ["Velocità 2", "Velocità 3", "Velocità 4", "Notturna", "Iperventilazione"]
# casi del choose «Verifica Tipo di Allerte» che mandano il comando Free Cooling: spie «per programmazione» e avviso Free
CASI_CON_COMANDO = {
    "free_non_sospesa": {FREE_C: "off", FREE_H: "off", FREE: "Allerta Raffrescamento in atto, Presenza di Inquinanti"},
    "nessuna_allerta_free_cooling": {FREE_C: "on", FREE_H: "off",
                                     FREE: "Nessuna Allerta Free Cooling Programmato, Presenza di Inquinanti"},
    "nessuna_allerta_free_heating": {FREE_C: "off", FREE_H: "on",
                                     FREE: "Nessuna Allerta Free Heating Programmato, Presenza di Inquinanti"},
}
CASI_SENZA_COMANDO = {
    "free_cooling_sospesa": {FREE_C: "on", FREE_H: "off",
                             FREE: "Allerta Free Cooling Programmato (Riscaldamento Arrestato, Presenza di Inquinanti)"},
    "free_heating_sospesa": {FREE_C: "off", FREE_H: "on",
                             FREE: "Allerta Free Heating Programmato (Raffrescamento Arrestato, Presenza di Inquinanti)"},
}


def _casi_free() -> list[dict[str, Any]]:
    (scelta,) = [p for p in _ramo(FREE_INQ)["sequence"] if "choose" in p]
    return scelta["choose"]


def _blocco(sequenza: list[dict[str, Any]]) -> tuple[int, dict[str, Any]]:
    """Il controllo della scelta dell'utente (if ... then stop) e la sua posizione nella sequenza."""
    (trovati,) = [[(i, p) for i, p in enumerate(sequenza) if "if" in p and {"stop": STOP} in p.get("then", [])]]
    assert len(trovati) == 1
    return trovati[0]


def _primo_comando(sequenza: list[dict[str, Any]]) -> int:
    return next(i for i, p in enumerate(sequenza) if "shell_command." in str(p))


def _escluse(passo: dict[str, Any]) -> list[str]:
    (condizione,) = passo["if"]
    testo = condizione["value_template"]
    assert testo.startswith("{{ vel_prima_del_comando not in [") and testo.endswith("] }}")
    return [v.strip().strip("'") for v in testo.split("[", 1)[1].rsplit("]", 1)[0].split(",")]


# ------------------------------------------------------------------------------------------------ struttura
def test_free_con_inquinanti_controllo_nei_3_casi_con_il_comando() -> None:
    """Ogni caso del choose che manda il comando Free Cooling ha il controllo dopo la memoria della velocità prima del
    comando e prima del ciclo di comando; i 2 casi con la Free sospesa non mandano comandi e non lo hanno."""
    casi = _casi_free()
    assert len(casi) == 5
    con_comando = [c for c in casi if "shell_command." in str(c["sequence"])]
    assert len(con_comando) == 3
    for caso in con_comando:
        seq = caso["sequence"]
        i, passo = _blocco(seq)
        assert "vel_prima_del_comando" in seq[i - 1]["variables"]
        assert i < _primo_comando(seq)
        assert _escluse(passo) == ESCLUSE_FREE
        (spegni,) = [p for p in passo["then"] if p.get("action") == "input_boolean.turn_off"]
        assert sorted(spegni["target"]["entity_id"]) == sorted(MEMORIE_PDR + [FREE_C, FREE_H])
    for caso in casi:
        if caso not in con_comando:
            assert STOP not in str(caso["sequence"])


def test_velocita_0_controllo_prima_del_comando() -> None:
    """«Rip. Vel. 0 No PdR»: controllo dopo la memoria della velocità prima del comando e prima del ciclo; spegne la
    memoria Velocità 1 Inquinanti/PdR e le 8 memorie PdR, le stesse che il ripristino spegne nel ciclo."""
    seq = _ramo(VEL_0)["sequence"]
    i, passo = _blocco(seq)
    assert i == 1 and "vel_prima_del_comando" in seq[0]["variables"]
    assert i < _primo_comando(seq)
    assert _escluse(passo) == ESCLUSE_VEL_0
    (spegni,) = [p for p in passo["then"] if p.get("action") == "input_boolean.turn_off"]
    assert sorted(spegni["target"]["entity_id"]) == sorted([V1_PDR] + MEMORIE_PDR)
    nel_ciclo = [e for p in seq[i + 1]["repeat"]["sequence"] if p.get("action") == "input_boolean.turn_off"
                 for e in ([p["target"]["entity_id"]] if isinstance(p["target"]["entity_id"], str)
                           else p["target"]["entity_id"])]
    assert sorted(nel_ciclo) == sorted(spegni["target"]["entity_id"])


async def test_rami_validi_per_home_assistant(hass: HomeAssistant) -> None:
    for tid in (FREE_INQ, VEL_0):
        cv.SCRIPT_SCHEMA(_ramo(tid)["sequence"])


# ------------------------------------------------------------------------------------------------ comportamento
def _stati_free(caso: dict[str, str], letta: str) -> dict[str, str]:
    """Fine PdR con Inquinanti, VMC partita da Free Cool./Heat. (memoria PdR Free accesa), velocità letta «letta»."""
    return {LETTURA: letta, LETTURA_I: letta, BLACK_OUT_RILEVATO: "off", **_spente(MEMORIE_PDR), MEMORIA_FREE: "on",
            SPIA_CO2: "on", V1_PDR: "off", **caso}


def _stati_vel_0(letta: str) -> dict[str, str]:
    """Fine PdR e fine Inquinanti con la memoria Velocità 1 Inquinanti/PdR accesa, velocità letta «letta»."""
    return {LETTURA: letta, LETTURA_I: letta, BLACK_OUT_RILEVATO: "off", **_spente(MEMORIE_PDR), V1_PDR: "on",
            SPIA_CO2: "off", PARTENZA: "off"}


@pytest.mark.parametrize("caso", list(CASI_CON_COMANDO))
@pytest.mark.parametrize("letta", SCELTE)
async def test_free_con_inquinanti_scelta_resta(hass: HomeAssistant, caso: str, letta: str) -> None:
    """Velocità scelta poco prima della fine del PdR (non ancora memorizzata): nessun comando, memorie PdR e spie «per
    programmazione» spente."""
    comandi = await _esegui(hass, _ramo(FREE_INQ)["sequence"], _stati_free(CASI_CON_COMANDO[caso], letta))
    assert comandi == []
    assert all(_stato(hass, e) == "off" for e in MEMORIE_PDR + [FREE_C, FREE_H])


@pytest.mark.parametrize("caso", list(CASI_CON_COMANDO))
@pytest.mark.parametrize("letta", ["Velocità 0", "Velocità 1", "Free Cooling", "Non disponibile"])
async def test_free_con_inquinanti_senza_scelta_ripristina(hass: HomeAssistant, caso: str, letta: str) -> None:
    """VMC ferma dal PdR, a Velocità 1 degli Inquinanti, già in Free (anche Free Heating, letta «Free Cooling») o non
    leggibile: il ripristino manda Free Cooling come prima."""
    comandi = await _esegui(hass, _ramo(FREE_INQ)["sequence"], _stati_free(CASI_CON_COMANDO[caso], letta), attesa=1.0)
    assert comandi[:1] == ["vmc_master_freecooling"]


@pytest.mark.parametrize("caso", list(CASI_SENZA_COMANDO))
@pytest.mark.parametrize("letta", ["Velocità 0", "Velocità 3"])
async def test_free_con_inquinanti_free_sospesa_come_prima(hass: HomeAssistant, caso: str, letta: str) -> None:
    """Free sospesa da un'allerta: nessun comando (la VMC resta dov'è) e memorie PdR spente; le spie «per
    programmazione» restano per la ripresa Free, con o senza una scelta."""
    comandi = await _esegui(hass, _ramo(FREE_INQ)["sequence"], _stati_free(CASI_SENZA_COMANDO[caso], letta))
    assert comandi == []
    assert all(_stato(hass, e) == "off" for e in MEMORIE_PDR)
    assert {_stato(hass, FREE_C), _stato(hass, FREE_H)} == {"on", "off"}


@pytest.mark.parametrize("letta", SCELTE + ["Free Cooling"])
async def test_velocita_0_scelta_resta(hass: HomeAssistant, letta: str) -> None:
    """Velocità scelta (anche Free Cool./Heat.) poco prima della fine: nessun comando Velocità 0, memoria Velocità 1
    Inquinanti/PdR e memorie PdR spente."""
    comandi = await _esegui(hass, _ramo(VEL_0)["sequence"], _stati_vel_0(letta))
    assert comandi == []
    assert all(_stato(hass, e) == "off" for e in [V1_PDR] + MEMORIE_PDR)


@pytest.mark.parametrize("letta", ["Velocità 1", "Velocità 0", "Non disponibile"])
async def test_velocita_0_senza_scelta_ripristina(hass: HomeAssistant, letta: str) -> None:
    """VMC a Velocità 1 degli Inquinanti (o già ferma, o non leggibile): il ripristino manda Velocità 0 come prima e
    spegne le memorie."""
    comandi = await _esegui(hass, _ramo(VEL_0)["sequence"], _stati_vel_0(letta), attesa=1.0)
    assert comandi[:1] == ["vmc_master_velocita_0"]
    assert all(_stato(hass, e) == "off" for e in [V1_PDR] + MEMORIE_PDR)


# ------------------------------------------------------------------------------------------------ dopo lo stop
def _trigger_di_ripristino() -> list[dict[str, Any]]:
    """Trigger di fine PdR e di ripresa Free («Rip. ...») e di fine Inquinanti."""
    return [t for t in _automazione()["triggers"]
            if str(t.get("id", "")).startswith("Rip. ") or t.get("id") == "inquinanti_co2_voc_off"]


def _stati_comuni(letta: str) -> dict[str, str]:
    return {CONFRONTO: "Si può impiegare", INT_PDR: "on", INT_CO2: "on", IP: "ON-Line", FASE: "0", SPIA_GELO: "off",
            SPIA_DELTA: "off", "sensor.vmc_master_alert_monitoraggio_co2": "Nessuna Allerta",
            "sensor.vmc_master_alert_monitoraggio_voc": "Nessuna Allerta", **_spente(BLACK_OUT),
            **_spente(MEMORIE_CO2), LETTURA: letta, LETTURA_I: letta}


@pytest.mark.parametrize("letta", ["Velocità 3", "Notturna"])
async def test_velocita_0_dopo_lo_stop_nessun_altro_ripristino(hass: HomeAssistant, letta: str) -> None:
    """Dopo lo stop di «Rip. Vel. 0 No PdR» nessun trigger di ripristino (fine PdR, ripresa Free, fine Inquinanti) è
    vero: la velocità scelta non viene sovrascritta da un altro ramo. Prima dello stop il trigger del ramo è vero."""
    _imposta(hass, {**_stati_comuni(letta), FREE_C: "off", FREE_H: "off"})
    trigger = {t["id"]: t for t in _trigger_di_ripristino()}
    _imposta(hass, _stati_vel_0(letta))
    assert _render(hass, trigger[VEL_0]["value_template"]) is True
    await _esegui(hass, _ramo(VEL_0)["sequence"], _stati_vel_0(letta))
    veri = [tid for tid, t in trigger.items() if _render(hass, t["value_template"]) is True]
    assert veri == []


@pytest.mark.parametrize("caso", list(CASI_CON_COMANDO))
async def test_free_con_inquinanti_dopo_lo_stop_nessun_altro_ripristino(hass: HomeAssistant, caso: str) -> None:
    """Dopo lo stop di «Rip. Free Cool./Heat. No PdR se Spia Inquinanti ON» (Inquinanti ancora in corso) nessun trigger
    di ripristino è vero; prima dello stop il trigger del ramo è vero."""
    _imposta(hass, {**_stati_comuni("Velocità 3"), "sensor.vmc_master_alert_monitoraggio_voc": "Allerta"})
    trigger = {t["id"]: t for t in _trigger_di_ripristino()}
    _imposta(hass, _stati_free(CASI_CON_COMANDO[caso], "Velocità 3"))
    assert _render(hass, trigger[FREE_INQ]["value_template"]) is True
    await _esegui(hass, _ramo(FREE_INQ)["sequence"], _stati_free(CASI_CON_COMANDO[caso], "Velocità 3"))
    veri = [tid for tid, t in trigger.items() if _render(hass, t["value_template"]) is True]
    assert veri == []
