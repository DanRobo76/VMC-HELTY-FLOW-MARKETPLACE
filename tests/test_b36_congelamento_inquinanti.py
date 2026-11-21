"""Prove della b36, gemello di A1-2 (b32 106d73e) nella fine del Congelamento.

A1-2 aveva escluso dalla «regola 03-11-2026» del ramo Velocità 1 di fine Δ Temp. la Velocità 1 avviata dagli Inquinanti
partiti da Velocità 0 (memoria «Partenza e Ritorno a Velocità 0» o memoria Velocità 1 Inquinanti/PdR accesa): senza
l'esclusione la regola la trattava come una scelta dell'utente, spegneva il ritorno a Velocità 0 e a fine Inquinanti la
VMC restava a Velocità 1 (Foglio A28 NOTA 1). Il ramo gemello di fine Congelamento non aveva l'esclusione.

Simulatore (Home Assistant 2026.11.2, /home/user/simfull/cong/cong_inq.py): con la 67a5bcf il difetto non si vede, perché
il Congelamento ON a Velocità 1 con gli Inquinanti in corso accende già la memoria Velocità 1 Inquinanti e tiene la
Partenza da Velocità 0 («Verifica Spia Richiamo Inquinanti»), quindi a fine Congelamento la regola non scatta; forzando
lo stato che il Δ Temp. ON lascia prima della memoria Inquinanti (memoria Velocità 1 spenta) la VMC finiva a Velocità 1.
Il ramo di fine Congelamento ora ha la stessa esclusione del Δ Temp.: le due regole sono identiche per ogni velocità.
"""

from __future__ import annotations

from typing import Any

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from tests.test_b35_allerte import (
    FREE_C,
    FREE_H,
    IP,
    LETTURA,
    MEMORIE_CO2,
    MEMORIE_DELTA,
    MEMORIE_PDR,
    PARTENZA,
    SPIA_CO2,
    SPIA_DELTA,
    SUFFISSI,
    V1_PDR,
    _ramo,
    _rami,
    _spente,
)
from tests.test_b36_allerte import BLACK_OUT_RILEVATO, CALENDARIO, MEMORIE_GELO, SPIA_GELO, _esegui, _stato

COMANDO_NON_ESEGUITO = "input_boolean.vmc_master_spia_calendario_comando_non_eseguito"
INT_CALENDARIO = "input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario"
M1 = "input_boolean.vmc_master_spia_velocita_1_co2_o_voc"
M2 = "input_boolean.vmc_master_spia_velocita_2_co2_o_voc"
REGOLA = "Inquinanti in corso e velocità scelta dall'utente durante"
ESCLUSIONE = ("and not is_state('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0', 'on') "
              "and not is_state('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr', 'on')")
# allerta -> (id del trigger di fine allerta, spia dell'allerta, memorie di velocità dell'allerta, nome della memoria)
ALLERTE = {
    "Congelamento": ("Congelamento OFF", SPIA_GELO, MEMORIE_GELO, "input_boolean.vmc_master_spia_velocita_{}_congelamento"),
    "Δ Temp.": ("delta_temp_OFF", SPIA_DELTA, MEMORIE_DELTA,
                "input_boolean.vmc_master_spia_velocita_{}_delta_temp_verifica_soglia_valore"),
}


def _opzioni_ripristino(allerta: str) -> dict[str, dict[str, Any]]:
    """Le 8 opzioni del choose «Ripristino Velocità» di fine allerta, per suffisso della velocità memorizzata."""
    tid, _, _, memoria = ALLERTE[allerta]
    (ripristino,) = [p for p in _ramo(tid)["sequence"] if p.get("alias") == "Ripristino Velocità"]
    opzioni = {}
    for opzione in ripristino["choose"]:
        (suffisso,) = [s for s in SUFFISSI if memoria.format(s) in opzione["conditions"][0]["value_template"]]
        opzioni[suffisso] = opzione
    assert sorted(opzioni) == sorted(SUFFISSI)
    return opzioni


def _regola(opzione: dict[str, Any]) -> dict[str, Any] | None:
    passi = [p for p in opzione["sequence"] if str(p.get("alias", "")).startswith(REGOLA)]
    assert len(passi) <= 1
    return passi[0] if passi else None


def test_regola_03_11_2026_identica_a_fine_congelamento_e_a_fine_delta() -> None:
    """Per ogni velocità memorizzata la regola 03-11-2026 di fine Congelamento e quella di fine Δ Temp. hanno la stessa
    condizione e gli stessi passi (gemelli tra allerte, classe d7); la Velocità 0 non ha la regola in nessuna delle due
    (la memoria Inquinanti non può essere la Velocità 0, A28); solo la Velocità 1 esclude la Velocità 1 avviata dagli
    Inquinanti partiti da Velocità 0."""
    gelo, delta = _opzioni_ripristino("Congelamento"), _opzioni_ripristino("Δ Temp.")
    for suffisso in SUFFISSI:
        r_gelo, r_delta = _regola(gelo[suffisso]), _regola(delta[suffisso])
        if suffisso == "0":
            assert r_gelo is None and r_delta is None
            continue
        assert r_gelo["if"] == r_delta["if"], suffisso
        assert r_gelo["then"] == r_delta["then"], suffisso
        condizione = r_gelo["if"][0]["value_template"]
        assert f"not is_state('input_boolean.vmc_master_spia_velocita_{suffisso}_co2_o_voc', 'on')" in condizione
        assert (ESCLUSIONE in condizione) is (suffisso == "1"), suffisso
        assert r_gelo["alias"].replace("Congelamento", "Δ Temp.") == r_delta["alias"], suffisso


def _stati_fine(allerta: str, **altri: str) -> dict[str, str]:
    """Fine allerta con la memoria Velocità 1 dell'allerta accesa, VMC a Velocità 0 (Congelamento) o 1 (Δ Temp.)."""
    _, spia, memorie, memoria = ALLERTE[allerta]
    stati = {spia: "on", **_spente(memorie), memoria.format("1"): "on", **_spente(CALENDARIO),
             INT_CALENDARIO: "off", COMANDO_NON_ESEGUITO: "off", BLACK_OUT_RILEVATO: "off", IP: "ON-Line",
             LETTURA: "Velocità 0" if allerta == "Congelamento" else "Velocità 1",
             SPIA_CO2: "on", PARTENZA: "off", V1_PDR: "off", **_spente(MEMORIE_CO2)}
    stati.update(altri)
    return stati


@pytest.mark.parametrize("allerta", list(ALLERTE))
@pytest.mark.parametrize(
    "memorie",
    [{PARTENZA: "on", V1_PDR: "on"}, {PARTENZA: "on"}, {V1_PDR: "on"}],
    ids=["partenza+pdr", "partenza", "pdr"],
)
async def test_velocita_1_degli_inquinanti_partiti_da_0_resta_con_il_ritorno_a_0(
        hass: HomeAssistant, allerta: str, memorie: dict[str, str]) -> None:
    """Inquinanti partiti da Velocità 0 (VMC a Velocità 1, memoria Inquinanti non ancora data), allerta iniziata a
    Velocità 1 e finita prima del rientro: il ripristino rimanda la Velocità 1, ma la regola 03-11-2026 non la prende
    per una scelta dell'utente: le memorie della Partenza da Velocità 0 restano accese e la memoria Velocità 1 Inquinanti
    resta spenta, così a fine Inquinanti la VMC torna a Velocità 0 (Foglio A28 NOTA 1). Prima, a fine Congelamento, la
    regola le spegneva e accendeva la memoria Velocità 1: a fine Inquinanti la VMC restava a Velocità 1."""
    tid, spia, memorie_allerta, _ = ALLERTE[allerta]
    comandi = await _esegui(hass, _ramo(tid)["sequence"], _stati_fine(allerta, **memorie), attesa=0.5)
    assert comandi[:1] == ["vmc_master_velocita_1"]
    for entita, stato in memorie.items():
        assert _stato(hass, entita) == stato, entita
    assert _stato(hass, M1) == "off"
    assert _stato(hass, SPIA_CO2) == "on"
    assert all(_stato(hass, e) == "off" for e in [spia, *memorie_allerta])


@pytest.mark.parametrize("allerta", list(ALLERTE))
async def test_velocita_1_scelta_dall_utente_diventa_la_memoria_inquinanti(hass: HomeAssistant, allerta: str) -> None:
    """Regola 03-11-2026 invariata: Inquinanti in corso con la memoria Velocità 2 e Velocità 1 memorizzata dall'allerta
    (scelta dall'utente, nessuna Partenza da Velocità 0): a fine allerta la Velocità 1 diventa la memoria degli
    Inquinanti (Foglio C6, D6: la logica Inquinanti riparte dalla velocità scelta)."""
    tid = ALLERTE[allerta][0]
    comandi = await _esegui(hass, _ramo(tid)["sequence"], _stati_fine(allerta, **{M2: "on"}), attesa=0.5)
    assert comandi[:1] == ["vmc_master_velocita_1"]
    accese = {e for e in [*MEMORIE_CO2, PARTENZA, V1_PDR] if _stato(hass, e) == "on"}
    assert accese == {M1}


def _ramo_inizio_congelamento() -> dict[str, Any]:
    """Il ramo «Congelamento ON» (con i trigger delle velocità scelte durante il Congelamento, in OR)."""
    (ramo,) = [r for r in _rami() if r["conditions"][0].get("condition") == "or"
               and {"id": ["Congelamento ON"], "condition": "trigger"} in r["conditions"][0]["conditions"]]
    return ramo


def _stati_inizio_congelamento(**altri: str) -> dict[str, str]:
    stati = {SPIA_GELO: "off", **_spente(MEMORIE_GELO), LETTURA: "Velocità 1", IP: "ON-Line", BLACK_OUT_RILEVATO: "off",
             SPIA_CO2: "on", PARTENZA: "on", V1_PDR: "on", **_spente(MEMORIE_CO2), **_spente(MEMORIE_PDR),
             FREE_C: "off", FREE_H: "off"}
    stati.update(altri)
    return stati


async def test_congelamento_on_a_velocita_1_con_inquinanti_partiti_da_0(hass: HomeAssistant) -> None:
    """Perché con la 67a5bcf il simulatore non mostrava il difetto: il Congelamento ON a Velocità 1 con gli Inquinanti
    partiti da Velocità 0 (memoria Inquinanti non ancora data) accende la memoria Velocità 1 Inquinanti e tiene accese
    le memorie della Partenza da Velocità 0, poi porta la VMC a Velocità 0. Il Δ Temp. ON invece non tocca la memoria
    Inquinanti: per questo A1-2 si vedeva solo a fine Δ Temp."""
    comandi = await _esegui(hass, _ramo_inizio_congelamento()["sequence"], _stati_inizio_congelamento(), attesa=0.5,
                            variabili={"trigger": {"id": "Congelamento ON"}})
    assert comandi[:1] == ["vmc_master_velocita_0"]
    assert _stato(hass, "input_boolean.vmc_master_spia_velocita_1_congelamento") == "on"
    accese = {e for e in [*MEMORIE_CO2, PARTENZA, V1_PDR] if _stato(hass, e) == "on"}
    assert accese == {M1, PARTENZA, V1_PDR}


async def test_rami_validi_per_home_assistant(hass: HomeAssistant) -> None:
    for tid in ("Congelamento OFF", "delta_temp_OFF"):
        cv.SCRIPT_SCHEMA(_ramo(tid)["sequence"])
