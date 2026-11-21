"""Prove della b36, fetta «allerte»: scelte del proprietario sull'audit 1:1 della b34 (1, 2, 6 e 7 del brief).

- C3-2: una velocità scelta dall'utente negli 8 s di attesa della fine degli Inquinanti veniva sovrascritta dal
  ripristino della memoria: ora resta, le memorie Inquinanti si spengono e il ramo si ferma, come la protezione del PdR.
  Esclusa l'opzione Free (ha la sua ripresa); con Congelamento o Δ Temp. accesi comportamento di prima.
- C4-4: con [Set Velocità Umidità di Avvio] su Velocità 0 e la Free sospesa l'avvio dell'Umidità mandava la VMC a
  Velocità 1 (nota 3): ora vale il Set 0 (la VMC resta ferma, memoria Velocità 0) e a fine Umidità la ripresa Free non
  viene annullata. Lo stesso nei 2 rami TeVsTi e nella fine Inquinanti in Free (R8): Velocità 0 invece della nota 3.
- C4-3: i trigger del PdR con la ripresa Free in attesa (154/156 e gemelli con gli Inquinanti, guardia e Countdown)
  valevano con qualsiasi velocità: ora solo con la VMC a Velocità 0, in Free o a Velocità 1 dell'Umidità (gemelli: 0, 1
  o Free) e, senza Inquinanti, senza una memoria PdR di velocità già accesa.
- C4-5: interruttore Umidità spento durante l'allerta con la VMC OFF-Line, Non disponibile o in ripristino dopo un
  Black-Out: l'interruttore si riaccendeva; ora resta spento e si spengono solo l'allerta e le memorie Umidità, senza
  comando alla VMC (come il ramo del PdR con la VMC non disponibile).
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest
from homeassistant.core import Context, HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.script import Script

from tests.test_b35_allerte import (
    BLACK_OUT,
    COMANDI,
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
    MEMORIE_DELTA,
    MEMORIE_PDR,
    PARTENZA,
    PDR_FREE,
    SCONSIGLIATO,
    SPIA_CO2,
    SPIA_DELTA,
    SPIA_U0,
    SPIA_UMIDITA,
    SUFFISSI,
    V1_PDR,
    _automazione,
    _copia_guardia,
    _copie_countdown,
    _imposta,
    _norm,
    _ramo,
    _rami,
    _render,
    _spente,
    _testo,
    _trigger,
)

SPIA_GELO = "input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia"
MEMORIE_GELO = [f"input_boolean.vmc_master_spia_velocita_{s}_congelamento" for s in SUFFISSI]
BLACK_OUT_RILEVATO = "binary_sensor.vmc_master_black_out_rilevato"
SET_UMIDITA = "input_select.vmc_master_speed_umidita"
INT_UMIDITA = "input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita"
SPIA_U0_MANTENUTA = "input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0"
SPIA_U_FREE = "input_boolean.vmc_master_spia_umidita_velocita_freecooling"
MEMORIE_UMIDITA = [SPIA_U0, SPIA_U0_MANTENUTA] + [
    f"input_boolean.vmc_master_spia_umidita_velocita_{s}" for s in SUFFISSI[1:]]
CALENDARIO = [f"input_boolean.vmc_master_spia_calendario_{g}_{n}"
              for g in ("lunedi", "martedi", "mercoledi", "giovedi", "venerdi", "sabato", "domenica") for n in (1, 2)]
TID_INTERRUTTORE_UMIDITA = " Disattivazione Umidità Limite, precedentemente Armato ed Attivato"
PDR_FREE_INQ = {
    "PdR Spia Free Heating OFF e Spia FreeCooling ON -> Imposta Velocità 1 se Spia Inquinanti ON": "Cooling",
    "PdR Spia Free Heating ON e Spia FreeCooling OFF -> Imposta Velocità 1 se Spia Inquinanti ON": "Heating",
}
VELOCITA = {"Velocità 0": "velocita_0", "Velocità 1": "velocita_1", "Velocità 2": "velocita_2",
            "Velocità 3": "velocita_3", "Velocità 4": "velocita_4", "Notturna": "notturna",
            "Iperventilazione": "iperventilazione"}


async def _esegui(hass: HomeAssistant, sequenza: list[dict[str, Any]], stati: dict[str, str], attesa: float = 1.5,
                  variabili: dict[str, Any] | None = None) -> list[str]:
    """Come in test_b35_allerte, con le variabili della corsa (per esempio «trigger»)."""
    comandi: list[str] = []

    def _entita(call: ServiceCall) -> list[str]:
        valore = call.data.get("entity_id", [])
        if isinstance(valore, str):
            valore = [v.strip() for v in valore.split(",") if v.strip()]
        return list(valore)

    async def _accendi(call: ServiceCall) -> None:
        for entita in _entita(call):
            hass.states.async_set(entita, "on")

    async def _spegni(call: ServiceCall) -> None:
        for entita in _entita(call):
            hass.states.async_set(entita, "off")

    async def _comando(call: ServiceCall) -> None:
        comandi.append(call.service)

    async def _niente(call: ServiceCall) -> None:
        return None

    hass.services.async_register("input_boolean", "turn_on", _accendi)
    hass.services.async_register("input_boolean", "turn_off", _spegni)
    hass.services.async_register("homeassistant", "update_entity", _niente)
    for nome in COMANDI:
        hass.services.async_register("shell_command", f"vmc_master_{nome}", _comando)
    _imposta(hass, stati)
    script = Script(hass, cv.SCRIPT_SCHEMA(sequenza), "Prova b36", "test_b36_allerte")
    corsa = hass.async_create_task(script.async_run(run_variables=variabili, context=Context()))
    finite, _ = await asyncio.wait({corsa}, timeout=attesa)
    if not finite:
        await script.async_stop()
    await asyncio.gather(corsa, return_exceptions=True)
    await hass.async_block_till_done()
    return comandi


def _stato(hass: HomeAssistant, entita: str) -> str:
    return hass.states.get(entita).state


# ------------------------------------------------------------------------------------------------ C3-2
def _passi_fine_inquinanti() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    sequenza = _ramo("inquinanti_co2_voc_off")["sequence"]
    (k,) = [k for k, passo in enumerate(sequenza) if "vel_ripristino_inquinanti" in passo.get("variables", {})]
    return sequenza[k], sequenza[k + 1], sequenza[k + 2]


def test_c3_2_protezione_prima_del_ripristino() -> None:
    """Dopo lo spegnimento della spia: velocità letta e velocità del ripristino, poi la protezione che spegne le
    memorie Inquinanti e ferma il ramo, poi il «choose» del ripristino di prima."""
    sequenza = _ramo("inquinanti_co2_voc_off")["sequence"]
    variabili, protezione, ripristino = _passi_fine_inquinanti()
    assert sequenza[0]["target"]["entity_id"] == SPIA_CO2 and sequenza.index(variabili) == 1
    assert variabili["variables"]["vel_fine_inquinanti"] == "{{ states('" + LETTURA + "') }}"
    assert "choose" in ripristino and len(ripristino["choose"]) == 8
    condizione = protezione["if"][0]["value_template"]
    for pezzo in (f"is_state('{SPIA_GELO}', 'off')", f"is_state('{SPIA_DELTA}', 'off')",
                  "vel_ripristino_inquinanti != ''", "vel_fine_inquinanti != vel_ripristino_inquinanti",
                  "not (vel_ripristino_inquinanti == 'Velocità 0' and vel_fine_inquinanti == 'Velocità 1')",
                  f"not (vel_fine_inquinanti == 'Velocità 1' and is_state('{V1_PDR}', 'on'))"):
        assert pezzo in condizione, pezzo
    allora = protezione["then"]
    assert set(allora[0]["target"]["entity_id"]) == {SPIA_CO2, PARTENZA, V1_PDR, *MEMORIE_CO2}
    assert set(allora[1]["then"][0]["target"]["entity_id"]) == set(MEMORIE_PDR)
    assert "stop" in allora[-1]
    assert not any("shell_command" in str(passo) for passo in allora)


def _memorie_co2(**accese: str) -> dict[str, str]:
    return {**_spente(MEMORIE_CO2), PARTENZA: "off", V1_PDR: "off", FREE_C: "off", FREE_H: "off", **accese}


@pytest.mark.parametrize(
    ("memorie", "attesa"),
    [
        ({"input_boolean.vmc_master_spia_velocita_0_co2_o_voc": "on"}, "Velocità 0"),
        ({PARTENZA: "on", "input_boolean.vmc_master_spia_velocita_2_co2_o_voc": "on"}, "Velocità 0"),
        ({"input_boolean.vmc_master_spia_velocita_1_co2_o_voc": "on"}, "Velocità 1"),
        ({"input_boolean.vmc_master_spia_velocita_1_co2_o_voc": "on", V1_PDR: "on"}, ""),
        ({"input_boolean.vmc_master_spia_velocita_1_co2_o_voc": "on", FREE_C: "on"}, ""),  # opzione Free
        ({"input_boolean.vmc_master_spia_velocita_2_co2_o_voc": "on", FREE_H: "on"}, "Velocità 2"),
        ({"input_boolean.vmc_master_spia_velocita_3_co2_o_voc": "on"}, "Velocità 3"),
        ({"input_boolean.vmc_master_spia_velocita_4_co2_o_voc": "on"}, "Velocità 4"),
        ({"input_boolean.vmc_master_spia_velocita_notturna_co2_o_voc": "on"}, "Notturna"),
        ({"input_boolean.vmc_master_spia_velocita_iperventilazione_co2_o_voc": "on"}, "Iperventilazione"),
        ({"input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc": "on"}, ""),  # opzione Free
        ({}, ""),
    ],
)
async def test_c3_2_velocita_del_ripristino_come_le_opzioni(hass: HomeAssistant, memorie: dict[str, str],
                                                            attesa: str) -> None:
    variabili, _, ripristino = _passi_fine_inquinanti()
    _imposta(hass, _memorie_co2(**memorie))
    assert _render(hass, variabili["variables"]["vel_ripristino_inquinanti"]) == attesa
    # stessa scelta del «choose» del ripristino: la prima opzione valida e' quella della velocita' calcolata
    valide = [k for k, opzione in enumerate(ripristino["choose"])
              if all(_render(hass, c["value_template"]) for c in opzione["conditions"])]
    ordine = ["Velocità 0", "Velocità 1", "Velocità 2", "Velocità 3", "Velocità 4", "Notturna", "Iperventilazione"]
    if attesa:
        assert valide[0] == ordine.index(attesa)
    else:
        assert not valide or valide[0] == 7


@pytest.mark.parametrize(
    ("ripristino", "letta", "altri", "protetta"),
    [
        ("Velocità 2", "Velocità 3", {}, True),
        ("Velocità 2", "Velocità 0", {}, True),
        ("Velocità 2", "Free Cooling", {}, True),
        ("Velocità 0", "Velocità 2", {}, True),
        ("Velocità 2", "Velocità 2", {}, False),  # nessun cambio: ripristino di prima (stessa velocita')
        ("Velocità 0", "Velocità 1", {}, False),  # Velocita' 1 degli Inquinanti partiti da ferma
        ("Velocità 2", "Velocità 1", {V1_PDR: "on"}, False),  # Velocita' 1 imposta da un altro ramo
        ("Velocità 2", "Velocità 1", {}, True),
        ("", "Velocità 3", {}, False),  # opzione Free: ha la sua ripresa
        ("Velocità 2", "Non disponibile", {}, False),
        ("Velocità 2", "Velocità 3", {SPIA_GELO: "on"}, False),
        ("Velocità 2", "Velocità 3", {SPIA_DELTA: "on"}, False),
    ],
)
async def test_c3_2_quando_vale_la_protezione(hass: HomeAssistant, ripristino: str, letta: str,
                                              altri: dict[str, str], protetta: bool) -> None:
    _, protezione, _ = _passi_fine_inquinanti()
    _imposta(hass, {SPIA_GELO: "off", SPIA_DELTA: "off", V1_PDR: "off", **altri})
    variabili = {"vel_ripristino_inquinanti": ripristino, "vel_fine_inquinanti": letta}
    assert _render(hass, protezione["if"][0]["value_template"], variabili) is protetta


def _stati_fine_inquinanti(**altri: str) -> dict[str, str]:
    stati = {SPIA_CO2: "on", SPIA_GELO: "off", SPIA_DELTA: "off", BLACK_OUT_RILEVATO: "off", SPIA_UMIDITA: "off",
             **_memorie_co2(), **_spente(MEMORIE_PDR), **_spente(BLACK_OUT)}
    stati.update(altri)
    return stati


async def test_c3_2_velocita_scelta_nell_attesa_resta(hass: HomeAssistant) -> None:
    """Allerta partita a Velocità 2, l'utente sceglie la Velocità 3 negli 8 s di attesa: nessun comando, memorie
    Inquinanti e spia spente (le memorie PdR restano, la VMC non era ferma)."""
    stati = _stati_fine_inquinanti(**{"input_boolean.vmc_master_spia_velocita_2_co2_o_voc": "on",
                                      "input_boolean.vmc_master_spia_velocita_3_un_solo_avvio": "on",
                                      LETTURA: "Velocità 3"})
    comandi = await _esegui(hass, _ramo("inquinanti_co2_voc_off")["sequence"], stati)
    assert comandi == []
    assert all(_stato(hass, e) == "off" for e in (SPIA_CO2, PARTENZA, V1_PDR, *MEMORIE_CO2))
    assert _stato(hass, "input_boolean.vmc_master_spia_velocita_3_un_solo_avvio") == "on"


async def test_c3_2_partita_da_ferma_velocita_scelta_resta(hass: HomeAssistant) -> None:
    """Allerta partita da Velocità 0 e Velocità 2 scelta nell'attesa: resta, spente anche le memorie PdR (O5)."""
    stati = _stati_fine_inquinanti(**{PARTENZA: "on", "input_boolean.vmc_master_spia_velocita_1_co2_o_voc": "on",
                                      "input_boolean.vmc_master_spia_velocita_0_un_solo_avvio": "on",
                                      LETTURA: "Velocità 2"})
    comandi = await _esegui(hass, _ramo("inquinanti_co2_voc_off")["sequence"], stati)
    assert comandi == []
    assert all(_stato(hass, e) == "off" for e in (SPIA_CO2, PARTENZA, *MEMORIE_CO2, *MEMORIE_PDR))


async def test_c3_2_partita_da_ferma_velocita_1_degli_inquinanti_torna_a_0(hass: HomeAssistant) -> None:
    stati = _stati_fine_inquinanti(**{PARTENZA: "on", LETTURA: "Velocità 1"})
    comandi = await _esegui(hass, _ramo("inquinanti_co2_voc_off")["sequence"], stati, attesa=0.5)
    assert comandi[:1] == ["vmc_master_velocita_0"]


@pytest.mark.parametrize(
    "altri",
    [
        {LETTURA: "Velocità 2"},  # nessun cambio
        {LETTURA: "Velocità 1", V1_PDR: "on"},  # Velocita' 1 imposta da un altro ramo durante gli Inquinanti
    ],
)
async def test_c3_2_senza_scelta_ripristino_come_prima(hass: HomeAssistant, altri: dict[str, str]) -> None:
    stati = _stati_fine_inquinanti(**{"input_boolean.vmc_master_spia_velocita_2_co2_o_voc": "on", **altri})
    comandi = await _esegui(hass, _ramo("inquinanti_co2_voc_off")["sequence"], stati, attesa=0.5)
    assert comandi[:1] == ["vmc_master_velocita_2"]


async def test_c3_2_opzione_free_esclusa(hass: HomeAssistant) -> None:
    stati = _stati_fine_inquinanti(**{"input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc": "on",
                                      LETTURA: "Velocità 3"})
    comandi = await _esegui(hass, _ramo("inquinanti_co2_voc_off")["sequence"], stati, attesa=0.5)
    assert comandi[:1] in (["vmc_master_freecooling"], ["vmc_master_velocita_0"], ["vmc_master_velocita_1"])


async def test_c3_2_con_delta_acceso_come_prima(hass: HomeAssistant) -> None:
    """Δ Temp. acceso: la protezione non vale, l'opzione «Δ ON» spegne solo le memorie (nessun comando) e la
    memoria Inquinanti della Velocità 2 non viene spenta dalla protezione con le altre."""
    stati = _stati_fine_inquinanti(**{"input_boolean.vmc_master_spia_velocita_2_co2_o_voc": "on",
                                      SPIA_DELTA: "on", LETTURA: "Velocità 3"})
    _, protezione, _ = _passi_fine_inquinanti()
    _imposta(hass, stati)
    assert _render(hass, protezione["if"][0]["value_template"],
                   {"vel_ripristino_inquinanti": "Velocità 2", "vel_fine_inquinanti": "Velocità 3"}) is False


async def test_c3_2_ramo_valido_per_home_assistant(hass: HomeAssistant) -> None:
    cv.SCRIPT_SCHEMA(_ramo("inquinanti_co2_voc_off")["sequence"])


# ------------------------------------------------------------------------------------------------ C4-4
def _stati_avvio_umidita(**altri: str) -> dict[str, str]:
    stati = {LETTURA: "Velocità 0", LETTURA_I: "Velocità 0", SPIA_UMIDITA: "off", FREE_C: "on", FREE_H: "off",
             SET_UMIDITA: "Velocità 0", BLACK_OUT_RILEVATO: "off", **_spente(MEMORIE_UMIDITA),
             FREE: "Allerta Free Cooling Programmato (Riscaldamento Arrestato)"}
    stati.update(altri)
    return stati


async def test_c4_4_set_0_con_la_free_sospesa_la_vmc_resta_ferma(hass: HomeAssistant) -> None:
    comandi = await _esegui(hass, _ramo("spia_umidita_on")["sequence"], _stati_avvio_umidita(), attesa=0.5)
    assert comandi[:1] == ["vmc_master_velocita_0"]
    assert _stato(hass, SPIA_UMIDITA) == "on"
    assert _stato(hass, SPIA_U0) == "on" and _stato(hass, SPIA_U0_MANTENUTA) == "off"
    assert _stato(hass, SPIA_U_FREE) == "off"
    assert _stato(hass, FREE_C) == "on"  # la ripresa Free resta in attesa


@pytest.mark.parametrize("velocita", ["Velocità 1", "Velocità 2", "Free Cool./Heat."])
async def test_c4_4_altro_set_con_la_free_sospesa_velocita_1_come_prima(hass: HomeAssistant, velocita: str) -> None:
    comandi = await _esegui(hass, _ramo("spia_umidita_on")["sequence"],
                            _stati_avvio_umidita(**{SET_UMIDITA: velocita}), attesa=0.5)
    assert comandi[:1] == ["vmc_master_velocita_1"]
    assert _stato(hass, SPIA_U_FREE) == "on"


def _stati_fine_umidita(**altri: str) -> dict[str, str]:
    stati = {SPIA_UMIDITA: "on", **_spente(MEMORIE_UMIDITA), SPIA_U0: "on", FREE_C: "on", FREE_H: "off",
             SET_UMIDITA: "Velocità 0", LETTURA: "Velocità 0", BLACK_OUT_RILEVATO: "off"}
    stati.update(altri)
    return stati


@pytest.mark.parametrize(
    ("altri", "ripresa"),
    [
        ({}, "on"),  # Set 0, Velocita' 0 data dall'avvio: la ripresa Free resta in attesa
        ({SPIA_U0_MANTENUTA: "on"}, "off"),  # Velocita' 0 scelta dall'utente: annullata come prima
        ({SET_UMIDITA: "Velocità 2"}, "off"),  # come prima
    ],
)
async def test_c4_4_fine_umidita_e_ripresa_free(hass: HomeAssistant, altri: dict[str, str], ripresa: str) -> None:
    comandi = await _esegui(hass, _ramo("spia_umidita_off")["sequence"], _stati_fine_umidita(**altri), attesa=0.5)
    assert comandi[:1] == ["vmc_master_velocita_0"]
    assert _stato(hass, FREE_C) == ripresa
    assert all(_stato(hass, e) == "off" for e in (SPIA_UMIDITA, *MEMORIE_UMIDITA))


def test_c4_4_annullamento_prima_dello_spegnimento_delle_memorie() -> None:
    """La condizione legge la memoria della Velocità 0 mantenuta: va valutata prima che il passo successivo la spenga."""
    opzione = _ramo("spia_umidita_off")["sequence"][1]["choose"][0]
    assert opzione["sequence"][0]["alias"].startswith("Memoria Velocità 0 -> annulla la ripresa della Free sospesa")
    assert SPIA_U0_MANTENUTA in opzione["sequence"][1]["target"]["entity_id"]


async def test_c4_4_rami_validi_per_home_assistant(hass: HomeAssistant) -> None:
    for tid in ("spia_umidita_on", "spia_umidita_off"):
        cv.SCRIPT_SCHEMA(_ramo(tid)["sequence"])


# ------------------------------------------------------------------------------------------------ C4-3
RIGA_VEL = (f"(states('{LETTURA}') in ['Velocità 0', 'Free Cooling'] or (states('{SPIA_UMIDITA}') == 'on' and "
            f"states('{LETTURA}') == 'Velocità 1'))")
RIGA_VEL_INQ = f"states('{LETTURA}') in ['Velocità 0', 'Velocità 1', 'Free Cooling'] and"


def test_c4_3_condizioni_in_tutte_le_copie() -> None:
    aut = _testo("vmc_master_automazione.txt")
    pacchetto = _testo("vmc_master.yaml")
    # stessa condizione delle 2 riprese Free senza Inquinanti (4 copie gia' nella b35) + 2 trigger del PdR
    assert aut.count(RIGA_VEL) == 8 and pacchetto.count(RIGA_VEL) == 8
    assert aut.count(RIGA_VEL_INQ) == 4 and pacchetto.count(RIGA_VEL_INQ) == 4
    for tid in [*PDR_FREE, *PDR_FREE_INQ]:
        modello = _norm(_trigger(tid)["value_template"])
        assert _norm(_copia_guardia(tid)) == modello, tid
        accesa, spenta = _copie_countdown(tid)
        assert _norm(accesa) == modello, tid
        assert modello in _norm(spenta), tid
    for tid in PDR_FREE:
        assert _trigger(tid)["value_template"].count(RIGA_VEL) == 1
        assert "Nessuna Allerta Free" in _trigger(tid)["value_template"]  # estensione C4-1 della b35 mantenuta
    for tid in PDR_FREE_INQ:
        assert _trigger(tid)["value_template"].count(RIGA_VEL_INQ) == 1


def _stati_pdr_free(tipo: str, **altri: str) -> dict[str, str]:
    stati = {FREE: (f"Allerta Free {tipo} Programmato (Riscaldamento Arrestato)" if tipo == "Cooling"
                    else f"Allerta Free {tipo} Programmato (Raffrescamento Arrestato)"),
             FREE_C: "on" if tipo == "Cooling" else "off", FREE_H: "on" if tipo == "Heating" else "off",
             SPIA_CO2: "off", LETTURA: "Velocità 0", LETTURA_I: "Velocità 0", SPIA_UMIDITA: "off",
             SPIA_GELO: "off", SPIA_DELTA: "off", IP: "ON-Line", FASE: "0", INT_PDR: "on", CONFRONTO: SCONSIGLIATO,
             "sensor.vmc_master_alert_monitoraggio_co2": "Nessuna Allerta",
             "sensor.vmc_master_alert_monitoraggio_voc": "Nessuna Allerta", INT_CO2: "on",
             **_spente(BLACK_OUT), **_spente(MEMORIE_PDR)}
    stati.update(altri)
    return stati


def _rendi_tutte(hass: HomeAssistant, tid: str) -> bool:
    esito = _render(hass, _trigger(tid)["value_template"])
    assert _render(hass, _copia_guardia(tid)) is esito
    accesa, spenta = _copie_countdown(tid)
    assert _render(hass, accesa) is esito
    assert _render(hass, spenta) is (not esito)
    return esito


@pytest.mark.parametrize("tid", list(PDR_FREE))
@pytest.mark.parametrize(
    ("altri", "atteso"),
    [
        ({}, True),
        ({LETTURA: "Free Cooling"}, True),
        ({LETTURA: "Velocità 1", SPIA_UMIDITA: "on"}, True),  # Velocita' 1 dell'Umidita'
        ({LETTURA: "Velocità 1"}, False),  # velocita' scelta: valgono i trigger PdR della velocita'
        ({LETTURA: "Velocità 2"}, False),
        ({LETTURA: "Iperventilazione"}, False),
        ({"input_boolean.vmc_master_spia_velocita_2_un_solo_avvio": "on"}, False),  # PdR Vel. 2 gia' memorizzato
        ({"input_boolean.vmc_master_spia_velocita_1_un_solo_avvio": "on"}, False),
        ({"input_boolean.vmc_master_spia_velocita_1_un_solo_avvio": "on", SPIA_UMIDITA: "on"}, True),
        ({"input_boolean.vmc_master_spia_velocita_0_un_solo_avvio": "on"}, True),
        ({FREE: "Nessuna Allerta Free {tipo} Programmato"}, True),  # estensione C4-1 della b35
        ({FREE: "Nessuna Allerta Free {tipo} Programmato", LETTURA: "Velocità 2"}, False),
    ],
)
async def test_c4_3_trigger_pdr_free_solo_a_0_in_free_o_a_1_dell_umidita(hass: HomeAssistant, tid: str,
                                                                        altri: dict[str, str], atteso: bool) -> None:
    tipo = PDR_FREE[tid]
    altri = {k: v.format(tipo=tipo) for k, v in altri.items()}
    _imposta(hass, _stati_pdr_free(tipo, **altri))
    assert _rendi_tutte(hass, tid) is atteso


@pytest.mark.parametrize("tid", list(PDR_FREE_INQ))
@pytest.mark.parametrize(
    ("letta", "atteso"),
    [("Velocità 1", True), ("Velocità 0", True), ("Free Cooling", True), ("Velocità 2", False),
     ("Notturna", False)],
)
async def test_c4_3_gemelli_con_inquinanti(hass: HomeAssistant, tid: str, letta: str, atteso: bool) -> None:
    tipo = PDR_FREE_INQ[tid]
    _imposta(hass, _stati_pdr_free(tipo, **{"sensor.vmc_master_alert_monitoraggio_co2": "Allerta", SPIA_CO2: "on",
                                            "input_boolean.vmc_master_spia_velocita_1_co2_o_voc": "on",
                                            LETTURA: letta, LETTURA_I: letta}))
    assert _rendi_tutte(hass, tid) is atteso


async def test_c4_3_fine_pdr_torna_la_velocita_scelta_anche_con_la_ripresa_free(hass: HomeAssistant) -> None:
    """Velocità 2 scelta con la ripresa Free in attesa: il PdR della Velocità 2 la memorizza; alla fine il ramo
    «Rip. Vel. 2» rimanda la Velocità 2 e annulla la ripresa Free (Foglio F6)."""
    stati = {**_spente(MEMORIE_PDR), "input_boolean.vmc_master_spia_velocita_2_un_solo_avvio": "on",
             FREE_C: "on", FREE_H: "off", LETTURA: "Velocità 0", SPIA_UMIDITA: "off", SPIA_U0: "off",
             BLACK_OUT_RILEVATO: "off", SPIA_GELO: "off", SPIA_DELTA: "off", SPIA_CO2: "off"}
    comandi = await _esegui(hass, _ramo("Rip. Vel. 2 No PdR")["sequence"], stati, attesa=0.5)
    assert comandi[:1] == ["vmc_master_velocita_2"]
    assert _stato(hass, FREE_C) == "off" and _stato(hass, FREE_H) == "off"


# ------------------------------------------------------------------------------------------------ C4-5
def _rami_interruttore_umidita() -> list[dict[str, Any]]:
    return [r for r in _rami() if r["conditions"][0].get("id") in ([TID_INTERRUTTORE_UMIDITA],
                                                                   TID_INTERRUTTORE_UMIDITA)]


def test_c4_5_due_rami_che_si_escludono() -> None:
    nuovo, vecchio = _rami_interruttore_umidita()
    assert len(nuovo["conditions"]) == 2 and len(vecchio["conditions"]) == 2
    vmc_non_usabile = nuovo["conditions"][1]["value_template"]
    assert _norm(vecchio["conditions"][1]["value_template"]) == _norm(
        "{{ not (" + vmc_non_usabile.strip()[3:-3].strip() + ") }}")
    assert not any("shell_command" in str(passo) for passo in nuovo["sequence"])
    # stesse condizioni del ramo con la VMC ON-Line, senza ON-Line e senza le memorie del Black-Out
    se = nuovo["sequence"][0]
    for entita in (*MEMORIE_CO2, *MEMORIE_PDR, *MEMORIE_GELO, *MEMORIE_DELTA, FREE_C, FREE_H, *CALENDARIO, PARTENZA,
                   V1_PDR, SPIA_CO2):
        assert f"states('{entita}') == 'off'" in se["if"][0]["value_template"], entita
    assert set(se["then"][0]["target"]["entity_id"]) == {SPIA_UMIDITA, *MEMORIE_UMIDITA}
    assert se["else"][0]["target"]["entity_id"] == INT_UMIDITA


@pytest.mark.parametrize(
    ("altri", "nuovo"),
    [
        ({IP: "OFF-Line"}, True),
        ({LETTURA_I: "Non disponibile"}, True),
        ({"input_boolean.vmc_master_spia_velocita_2": "on"}, True),  # in ripristino dopo un Black-Out
        ({}, False),
        ({IP: "OFF-Line", SPIA_UMIDITA: "off"}, False),  # nessuna allerta Umidita': ramo di prima (non fa nulla)
    ],
)
async def test_c4_5_condizioni_dei_due_rami(hass: HomeAssistant, altri: dict[str, str], nuovo: bool) -> None:
    ramo_nuovo, ramo_vecchio = _rami_interruttore_umidita()
    _imposta(hass, {SPIA_UMIDITA: "on", IP: "ON-Line", LETTURA_I: "Velocità 1", **_spente(BLACK_OUT), **altri})
    assert _render(hass, ramo_nuovo["conditions"][1]["value_template"]) is nuovo
    assert _render(hass, ramo_vecchio["conditions"][1]["value_template"]) is (not nuovo)


def _stati_interruttore(**altri: str) -> dict[str, str]:
    stati = {INT_UMIDITA: "off", SPIA_UMIDITA: "on", **_spente(MEMORIE_UMIDITA), SPIA_U0: "on", IP: "OFF-Line",
             LETTURA_I: "Non disponibile", LETTURA: "Non disponibile", BLACK_OUT_RILEVATO: "off", SPIA_CO2: "off",
             PARTENZA: "off", V1_PDR: "off", FREE_C: "off", FREE_H: "off", **_spente(MEMORIE_CO2),
             **_spente(MEMORIE_PDR), **_spente(MEMORIE_GELO), **_spente(MEMORIE_DELTA), **_spente(BLACK_OUT),
             **_spente(CALENDARIO)}
    stati.update(altri)
    return stati


async def _interruttore_spento(hass: HomeAssistant, stati: dict[str, str]) -> list[str]:
    """Esegue il «choose» con i due rami dell'interruttore Umidità, come l'automazione al suo trigger."""
    sequenza = [{"choose": _rami_interruttore_umidita()}]
    variabili = {"trigger": {"id": TID_INTERRUTTORE_UMIDITA, "entity_id": INT_UMIDITA, "platform": "state"}}
    return await _esegui(hass, sequenza, stati, attesa=1.0, variabili=variabili)


@pytest.mark.parametrize("altri", [{}, {IP: "ON-Line", LETTURA_I: "Velocità 1"} | {
    "input_boolean.vmc_master_spia_velocita_1": "on"}])
async def test_c4_5_vmc_non_disponibile_spegne_solo_l_allerta(hass: HomeAssistant, altri: dict[str, str]) -> None:
    comandi = await _interruttore_spento(hass, _stati_interruttore(**altri))
    assert comandi == []
    assert all(_stato(hass, e) == "off" for e in (SPIA_UMIDITA, *MEMORIE_UMIDITA))
    assert _stato(hass, INT_UMIDITA) == "off"


@pytest.mark.parametrize("altri", [{SPIA_CO2: "on"}, {FREE_C: "on"},
                                   {"input_boolean.vmc_master_spia_velocita_2_un_solo_avvio": "on"},
                                   {"input_boolean.vmc_master_spia_calendario_lunedi_1": "on"}])
async def test_c4_5_con_altre_allerte_l_interruttore_si_riaccende(hass: HomeAssistant, altri: dict[str, str]) -> None:
    comandi = await _interruttore_spento(hass, _stati_interruttore(**altri))
    assert comandi == []
    assert _stato(hass, INT_UMIDITA) == "on"
    assert _stato(hass, SPIA_UMIDITA) == "on" and _stato(hass, SPIA_U0) == "on"


async def test_c4_5_vmc_on_line_ramo_di_prima(hass: HomeAssistant) -> None:
    comandi = await _interruttore_spento(hass, _stati_interruttore(**{IP: "ON-Line", LETTURA_I: "Velocità 1",
                                                                       LETTURA: "Velocità 1"}))
    assert comandi[:1] == ["vmc_master_velocita_0"]
    assert _stato(hass, SPIA_UMIDITA) == "off" and _stato(hass, INT_UMIDITA) == "off"


async def test_c4_5_rami_validi_per_home_assistant(hass: HomeAssistant) -> None:
    for ramo in _rami_interruttore_umidita():
        cv.SCRIPT_SCHEMA(ramo["sequence"])
    assert len(_automazione()["actions"][1]["choose"]) == 196


# ------------------------------------------------------------------------------------------------ C4-4 ovunque
# Il Set 0 vale anche nei 2 rami TeVsTi (Free sospesa con l'Umidità in corso) e nella fine Inquinanti in Free (R8):
# Velocità 0 con il ciclo del ramo e memoria Umidità «avviata da Velocità 0», come all'avvio con la Free sospesa.
TEVSTI = {"TeVsTi Free-Heating -> Imposta Velocità 0": FREE_H, "TeVsTi Free-Cooling -> Imposta Velocità 0": FREE_C}


def _stati_tevsti(**altri: str) -> dict[str, str]:
    stati = {SPIA_UMIDITA: "on", **_spente(MEMORIE_UMIDITA), SPIA_U_FREE: "on", FREE_C: "off", FREE_H: "off",
             SET_UMIDITA: "Velocità 0", LETTURA: "Free Cooling", BLACK_OUT_RILEVATO: "off"}
    stati.update(altri)
    return stati


@pytest.mark.parametrize("tid", list(TEVSTI))
async def test_c4_4_tevsti_con_set_0_velocita_0(hass: HomeAssistant, tid: str) -> None:
    comandi = await _esegui(hass, _ramo(tid)["sequence"], _stati_tevsti(), attesa=0.5)
    assert comandi[:1] == ["vmc_master_velocita_0"]
    assert _stato(hass, TEVSTI[tid]) == "on"  # Free sospesa: la ripresa resta in attesa
    assert _stato(hass, SPIA_U0) == "on"
    assert all(_stato(hass, e) == "off" for e in MEMORIE_UMIDITA if e != SPIA_U0)


@pytest.mark.parametrize("tid", list(TEVSTI))
@pytest.mark.parametrize(
    ("altri", "comando"),
    [({SET_UMIDITA: "Velocità 2"}, "vmc_master_velocita_1"), ({SPIA_UMIDITA: "off"}, "vmc_master_velocita_0")],
)
async def test_c4_4_tevsti_altrimenti_come_prima(hass: HomeAssistant, tid: str, altri: dict[str, str],
                                                 comando: str) -> None:
    comandi = await _esegui(hass, _ramo(tid)["sequence"], _stati_tevsti(**altri), attesa=0.5)
    assert comandi[:1] == [comando]
    assert _stato(hass, SPIA_U_FREE) == "on" and _stato(hass, SPIA_U0) == "off"  # memorie Umidità non toccate


@pytest.mark.parametrize("tid", list(TEVSTI))
@pytest.mark.parametrize(
    ("valore_set", "letta", "fine"),
    [("Velocità 0", "Velocità 0", True), ("Velocità 0", "Velocità 1", False), ("Velocità 2", "Velocità 1", True),
     ("Velocità 2", "Velocità 0", False)],
)
async def test_c4_4_tevsti_fine_del_ciclo(hass: HomeAssistant, tid: str, valore_set: str, letta: str,
                                          fine: bool) -> None:
    ciclo = next(p for p in _ramo(tid)["sequence"] if "repeat" in p)
    _imposta(hass, {SPIA_UMIDITA: "on", SET_UMIDITA: valore_set, LETTURA: letta, BLACK_OUT_RILEVATO: "off"})
    assert _render(hass, ciclo["repeat"]["until"][0]["value_template"], {"vel_prima_del_comando": letta}) is fine


def _stati_r8(**altri: str) -> dict[str, str]:
    return _stati_fine_inquinanti(**{"input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc": "on",
                                     "input_boolean.vmc_master_spia_velocita_1_co2_o_voc": "on", FREE_C: "on",
                                     SPIA_UMIDITA: "on", SET_UMIDITA: "Velocità 0", LETTURA: "Velocità 1",
                                     **_spente(MEMORIE_UMIDITA), SPIA_U_FREE: "on", **altri})


async def test_c4_4_fine_inquinanti_in_free_con_set_0_velocita_0(hass: HomeAssistant) -> None:
    comandi = await _esegui(hass, _ramo("inquinanti_co2_voc_off")["sequence"], _stati_r8(), attesa=0.5)
    assert comandi[:1] == ["vmc_master_velocita_0"]
    assert _stato(hass, FREE_C) == "on"
    assert _stato(hass, SPIA_U0) == "on"
    assert all(_stato(hass, e) == "off" for e in MEMORIE_UMIDITA if e != SPIA_U0)


@pytest.mark.parametrize(
    ("altri", "comando"),
    [({SET_UMIDITA: "Velocità 2"}, "vmc_master_velocita_1"), ({SPIA_UMIDITA: "off"}, "vmc_master_velocita_0")],
)
async def test_c4_4_fine_inquinanti_in_free_altrimenti_come_prima(hass: HomeAssistant, altri: dict[str, str],
                                                                  comando: str) -> None:
    comandi = await _esegui(hass, _ramo("inquinanti_co2_voc_off")["sequence"], _stati_r8(**altri), attesa=0.5)
    assert comandi[:1] == [comando]
    assert _stato(hass, SPIA_U_FREE) == "on" and _stato(hass, SPIA_U0) == "off"


@pytest.mark.parametrize(("valore_set", "attesa"), [("Velocità 0", "Velocità 0"), ("Velocità 2", "Velocità 1")])
async def test_c4_4_fine_inquinanti_in_free_velocita_per_il_black_out(hass: HomeAssistant, valore_set: str,
                                                                      attesa: str) -> None:
    _, _, ripristino = _passi_fine_inquinanti()
    passi = ripristino["choose"][7]["sequence"][0]["choose"][0]["sequence"]  # Congelamento e Δ spenti
    fine = next(p for p in passi if "velocita_fine_allerta" in p.get("variables", {}))
    _imposta(hass, {SPIA_UMIDITA: "on", SET_UMIDITA: valore_set, FREE_C: "on", FREE_H: "off"})
    assert _render(hass, fine["variables"]["velocita_fine_allerta"]) == attesa


async def test_c4_4_ovunque_rami_validi_per_home_assistant(hass: HomeAssistant) -> None:
    for tid in (*TEVSTI, "inquinanti_co2_voc_off"):
        cv.SCRIPT_SCHEMA(_ramo(tid)["sequence"])
