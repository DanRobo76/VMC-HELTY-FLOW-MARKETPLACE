"""Prove della b36, verifica Black-Out (agente A): allerte Congelamento, Δ Temp., Inquinanti e Lim. Δ PdR con un Black-Out
e il ritorno della corrente (simulatore con Home Assistant vero, scenari bo_a.py).

- Ripristino «Black-Out Off Vel. 0» con un'allerta Lim. Δ PdR ancora in corso: i rami «PdR Velocità X ON» mandavano la
  VMC alla velocità memorizzata dal PdR (per esempio Velocità 2) e dopo 16 s il PdR la fermava di nuovo (circa 20 s alla
  velocità sbagliata, Velocità Registrata «Nessuna» nel frattempo). Ora quei rami valgono solo se l'allerta PdR non è più
  in corso (allerta finita durante il Black-Out o mentre stava finendo): con l'allerta in corso la VMC resta a Velocità 0
  e la memoria PdR resta per la fine dell'allerta.
"""

from __future__ import annotations

import pytest
from homeassistant.core import HomeAssistant

from tests.test_b35_allerte import (
    BLACK_OUT,
    CONFRONTO,
    FASE,
    INT_PDR,
    IP,
    LETTURA,
    LETTURA_I,
    MEMORIE_PDR,
    PARTENZA,
    SCONSIGLIATO,
    SPIA_CO2,
    SUFFISSI,
    V1_PDR,
    _ramo,
    _spente,
)
from tests.test_b36_allerte import _esegui, _stato

TID_BO_OFF_0 = "Black-Out Off Vel. 0"
SPIA_GELO = "input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia"
BLACK_OUT_RILEVATO = "binary_sensor.vmc_master_black_out_rilevato"
COMANDO = {"0": "vmc_master_velocita_0", "1": "vmc_master_velocita_1", "2": "vmc_master_velocita_2",
           "3": "vmc_master_velocita_3", "4": "vmc_master_velocita_4", "notturna": "vmc_master_notturna",
           "iperventilazione": "vmc_master_iperventilazione", "freecooling": "vmc_master_freecooling"}
NON_PIU_IN_CORSO = ("{{ not (states('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr') == 'on' "
                    "and states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') == \"Se ne sconsiglia l'impiego\") }}")


def _opzioni_pdr() -> list[dict]:
    opzioni = _ramo(TID_BO_OFF_0)["sequence"][1]["choose"]
    return [o for o in opzioni if "_un_solo_avvio')=='on'" in o["conditions"][0]["value_template"]]


def test_rami_pdr_del_ripristino_solo_con_l_allerta_pdr_finita() -> None:
    opzioni = _opzioni_pdr()
    assert len(opzioni) == len(SUFFISSI)
    for opzione in opzioni:
        assert len(opzione["conditions"]) == 2
        assert " ".join(opzione["conditions"][1]["value_template"].split()) == NON_PIU_IN_CORSO


def _stati(memoria: str, **altri: str) -> dict[str, str]:
    stati = {IP: "ON-Line", LETTURA: "Velocità 0", LETTURA_I: "Velocità 0", FASE: "0", BLACK_OUT_RILEVATO: "off",
             **_spente(BLACK_OUT), "input_boolean.vmc_master_spia_velocita_0": "on", **_spente(MEMORIE_PDR),
             f"input_boolean.vmc_master_spia_velocita_{memoria}_un_solo_avvio": "on", INT_PDR: "on",
             CONFRONTO: SCONSIGLIATO, SPIA_CO2: "off", PARTENZA: "off", V1_PDR: "off", SPIA_GELO: "off"}
    stati.update(altri)
    return stati


@pytest.mark.parametrize("memoria", [s for s in SUFFISSI if s != "0"])
async def test_pdr_ancora_in_corso_la_vmc_resta_ferma(hass: HomeAssistant, memoria: str) -> None:
    """Prima del ritorno la VMC era ferma per il PdR: il ripristino non manda la velocità della memoria PdR e lascia la
    memoria PdR accesa (Velocità Registrata = velocità di fine allerta)."""
    comandi = await _esegui(hass, _ramo(TID_BO_OFF_0)["sequence"], _stati(memoria), attesa=1.0)
    assert comandi == []
    assert _stato(hass, f"input_boolean.vmc_master_spia_velocita_{memoria}_un_solo_avvio") == "on"


async def test_pdr_ancora_in_corso_spie_del_black_out_spente_dopo_l_attesa(hass: HomeAssistant) -> None:
    """Senza comando il ramo aspetta i 12 s dell'attesa di conferma (come prima con la VMC già ferma), poi spegne le
    spie del Black-Out; la memoria PdR resta."""
    comandi = await _esegui(hass, _ramo(TID_BO_OFF_0)["sequence"], _stati("2"), attesa=13.5)
    assert comandi == []
    assert all(_stato(hass, e) == "off" for e in BLACK_OUT)
    assert _stato(hass, "input_boolean.vmc_master_spia_velocita_2_un_solo_avvio") == "on"


@pytest.mark.parametrize("altri", [{CONFRONTO: "Si può impiegare"}, {INT_PDR: "off"}])
@pytest.mark.parametrize("memoria", ["2", "notturna"])
async def test_pdr_finito_durante_il_black_out_ripristina_la_memoria(hass: HomeAssistant, memoria: str,
                                                                     altri: dict[str, str]) -> None:
    """Allerta finita durante il Black-Out (o mentre stava finendo): come prima, la VMC va alla velocità memorizzata."""
    comandi = await _esegui(hass, _ramo(TID_BO_OFF_0)["sequence"], _stati(memoria, **altri), attesa=1.0)
    assert comandi[:1] == [COMANDO[memoria]]


async def test_pdr_ancora_in_corso_vmc_non_ferma_va_a_velocita_0(hass: HomeAssistant) -> None:
    """Se alla riaccensione la VMC non è ferma, con il PdR in corso va a Velocità 0 (ramo senza memoria)."""
    comandi = await _esegui(hass, _ramo(TID_BO_OFF_0)["sequence"], _stati("3", **{LETTURA: "Velocità 1"}), attesa=1.0)
    assert comandi[:1] == ["vmc_master_velocita_0"]
