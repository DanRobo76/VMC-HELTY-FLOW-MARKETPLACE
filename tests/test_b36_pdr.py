"""Prove della b36, memoria PdR nella ripartenza degli Inquinanti (verifica Black-Out con il simulatore, agente A).

Ramo «inquinanti_co2_voc_on», casi «Velocità 0 con PdR su Velocità X o Spia Inquinanti su Velocità X» (X = 2, 3, 4,
Notturna, Iperventilazione): oltre alla memoria Inquinanti accendevano la memoria PdR «un solo avvio» della stessa
velocità con il solo interruttore PdR acceso (correzione R4 della revisione del 03-06/11/2026, che aveva aggiunto la
condizione dell'interruttore a un'accensione prima senza condizioni). Il caso entra anche dalla sola memoria
Inquinanti, cioè quando il trigger riscatta con gli Inquinanti già in corso (ritorno della corrente dopo un Black-Out,
fine di Congelamento o Δ Temp., VMC di nuovo leggibile): senza un'allerta PdR la memoria PdR accesa faceva scattare
dopo 12 s «Rip. Vel. X No PdR se Spia Inquinanti ON», che rimandava la velocità X (comando inutile) e annullava la
velocità 0, 1 o 2 scelta dall'utente in quei 12 s (Foglio: Inquinanti, la velocità cambiata durante l'allerta viene
memorizzata e mantenuta; il ripristino dei 12 s è solo quello di fine allerta Lim. Δ PdR).
Ora la memoria PdR si accende solo con l'interruttore PdR acceso E l'allerta PdR in corso (Punto di Rugiada «Se ne
sconsiglia l'impiego», il contrario esatto della prima condizione di «Rip. Vel. X No PdR se Spia Inquinanti ON»),
nell'«if» e nell'«until» del ciclo delle spie. Con l'allerta PdR in corso (anche dopo il ritorno della corrente) resta
tutto come prima: la memoria PdR resta per la fine dell'allerta (Foglio F6, Lim. Δ PdR con Inquinanti).
"""

from __future__ import annotations

from typing import Any

import pytest
from homeassistant.core import HomeAssistant

from tests.test_b35_allerte import (
    BLACK_OUT,
    CONFRONTO,
    FASE,
    FREE_C,
    FREE_H,
    INT_PDR,
    IP,
    LETTURA,
    LETTURA_I,
    MEMORIE_CO2,
    MEMORIE_PDR,
    PARTENZA,
    SCONSIGLIATO,
    SPIA_CO2,
    SPIA_DELTA,
    V1_PDR,
    _norm,
    _ramo,
    _render,
    _spente,
    _trigger,
)
from tests.test_b36_allerte import _esegui, _stato

TID = "inquinanti_co2_voc_on"
CASI = ("2", "3", "4", "notturna", "iperventilazione")
LETTO = {"2": "Velocità 2", "3": "Velocità 3", "4": "Velocità 4", "notturna": "Notturna",
         "iperventilazione": "Iperventilazione"}
COMANDO = {"2": "vmc_master_velocita_2", "3": "vmc_master_velocita_3", "4": "vmc_master_velocita_4",
           "notturna": "vmc_master_notturna", "iperventilazione": "vmc_master_iperventilazione"}
RIPRISTINO = {"2": "Rip. Vel. 2 No PdR se Spia Inquinanti ON", "3": "Rip. Vel. 3 No PdR  se Spia Inquinanti ON",
              "4": "Rip. Vel. 4 No PdR se Spia Inquinanti ON", "notturna": "Rip. Notturno No PdR se Spia Inquinanti ON",
              "iperventilazione": "Rip. Iperventilazione No PdR se Spia Inquinanti ON"}
ALLERTA_PDR = "states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') == \"Se ne sconsiglia l'impiego\""
ATTESO_UNTIL = ("('on' if (is_state('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr', 'on') and "
                + ALLERTA_PDR + ") else 'off')")
SPIA_GELO = "input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia"
SPIA_SI_PUO = "Si può impiegare"


def _casi() -> dict[str, tuple[dict[str, Any], dict[str, Any], str]]:
    """Per ogni velocità: il caso del «choose», il passo «if» della memoria PdR e l'«until» del ciclo delle spie."""
    (scelta,) = [passo for passo in _ramo(TID)["sequence"] if "choose" in passo]
    casi = {}
    for opzione in scelta["choose"]:
        ripeti = opzione["sequence"][0].get("repeat")
        passi = [p for p in (ripeti or {}).get("sequence", []) if "if" in p]
        if not passi:
            continue
        (passo,) = passi
        memoria = passo["then"][0]["target"]["entity_id"]
        suffisso = memoria.removeprefix("input_boolean.vmc_master_spia_velocita_").removesuffix("_un_solo_avvio")
        casi[suffisso] = (opzione, passo, ripeti["until"][0]["value_template"])
    return casi


def test_memoria_pdr_solo_con_interruttore_e_allerta_pdr_in_corso() -> None:
    casi = _casi()
    assert set(casi) == set(CASI)
    for suffisso, (_, passo, until) in casi.items():
        memoria = f"input_boolean.vmc_master_spia_velocita_{suffisso}_un_solo_avvio"
        assert passo["then"][0] == {"action": "input_boolean.turn_on", "target": {"entity_id": memoria}}
        assert passo["else"][0] == {"action": "input_boolean.turn_off", "target": {"entity_id": memoria}}
        condizioni = passo["if"]
        assert len(condizioni) == 2
        assert condizioni[0] == {"condition": "state", "entity_id": INT_PDR, "state": "on"}
        assert condizioni[1]["condition"] == "template"
        assert _norm(condizioni[1]["value_template"]) == "{{ " + ALLERTA_PDR + " }}"
        # l'«until» chiede la stessa memoria dell'«if» (altrimenti il ciclo delle spie non finisce)
        testo = _norm(until)
        assert testo.count(f"states('{memoria}')== " + ATTESO_UNTIL) == 1, suffisso
        assert "('on' if is_state('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr', 'on') else 'off')" not in testo


def _stati(caso: str, **altri: str) -> dict[str, str]:
    """Inquinanti che ripartono già in corso dopo il ritorno della corrente: memoria Inquinanti della velocità X, VMC
    tornata alla velocità X, nessuna memoria PdR, interruttore PdR acceso, Punto di Rugiada senza allerta."""
    stati = {IP: "ON-Line", LETTURA: LETTO[caso], LETTURA_I: LETTO[caso], FASE: "0", **_spente(BLACK_OUT),
             SPIA_CO2: "on", **_spente(MEMORIE_CO2), f"input_boolean.vmc_master_spia_velocita_{caso}_co2_o_voc": "on",
             **_spente(MEMORIE_PDR), INT_PDR: "on", CONFRONTO: SPIA_SI_PUO, PARTENZA: "off", V1_PDR: "off",
             FREE_C: "off", FREE_H: "off", SPIA_GELO: "off", SPIA_DELTA: "off",
             "binary_sensor.vmc_master_black_out_rilevato": "off"}
    stati.update(altri)
    return stati


@pytest.mark.parametrize("caso", CASI)
async def test_ripartenza_senza_allerta_pdr_non_accende_la_memoria_pdr(hass: HomeAssistant, caso: str) -> None:
    """Il difetto: senza allerta PdR la memoria PdR resta spenta e «Rip. Vel. X No PdR se Spia Inquinanti ON» non
    scatta; la VMC va comunque alla velocità della memoria Inquinanti (come prima)."""
    comandi = await _esegui(hass, _ramo(TID)["sequence"], _stati(caso))
    assert comandi[:1] == [COMANDO[caso]]
    assert _stato(hass, f"input_boolean.vmc_master_spia_velocita_{caso}_co2_o_voc") == "on"
    assert _stato(hass, f"input_boolean.vmc_master_spia_velocita_{caso}_un_solo_avvio") == "off"
    assert _render(hass, _trigger(RIPRISTINO[caso])["value_template"]) is False


@pytest.mark.parametrize("caso", CASI)
async def test_ripartenza_con_allerta_pdr_in_corso_tiene_la_memoria_pdr(hass: HomeAssistant, caso: str) -> None:
    """Black-Out con Inquinanti e Lim. Δ PdR insieme, PdR ancora in corso al ritorno: come prima."""
    memoria = f"input_boolean.vmc_master_spia_velocita_{caso}_un_solo_avvio"
    comandi = await _esegui(hass, _ramo(TID)["sequence"], _stati(caso, **{CONFRONTO: SCONSIGLIATO, memoria: "on"}))
    assert comandi[:1] == [COMANDO[caso]]
    assert _stato(hass, memoria) == "on"


@pytest.mark.parametrize("caso", CASI)
async def test_inquinanti_durante_il_pdr_a_velocita_0_come_prima(hass: HomeAssistant, caso: str) -> None:
    """Inquinanti che arrivano durante un'allerta PdR iniziata alla velocità X (VMC ferma, memoria PdR X): la VMC va a X,
    la memoria Inquinanti diventa X e la memoria PdR resta per la fine dell'allerta (come prima)."""
    memoria = f"input_boolean.vmc_master_spia_velocita_{caso}_un_solo_avvio"
    stati = _stati(caso, **{CONFRONTO: SCONSIGLIATO, memoria: "on", LETTURA: "Velocità 0", LETTURA_I: "Velocità 0",
                            SPIA_CO2: "off", f"input_boolean.vmc_master_spia_velocita_{caso}_co2_o_voc": "off"})
    comandi = await _esegui(hass, _ramo(TID)["sequence"], stati)
    assert comandi[:1] == [COMANDO[caso]]
    assert _stato(hass, memoria) == "on"
    assert _stato(hass, f"input_boolean.vmc_master_spia_velocita_{caso}_co2_o_voc") == "on"


@pytest.mark.parametrize("caso", ["2", "iperventilazione"])
async def test_interruttore_pdr_spento_memoria_spenta_come_prima(hass: HomeAssistant, caso: str) -> None:
    """Correzione R4 invariata: con l'interruttore PdR spento la memoria PdR si spegne anche con l'allerta in corso."""
    memoria = f"input_boolean.vmc_master_spia_velocita_{caso}_un_solo_avvio"
    comandi = await _esegui(hass, _ramo(TID)["sequence"],
                            _stati(caso, **{CONFRONTO: SCONSIGLIATO, memoria: "on", INT_PDR: "off"}))
    assert comandi[:1] == [COMANDO[caso]]
    assert _stato(hass, memoria) == "off"


@pytest.mark.parametrize("caso", ["3", "notturna"])
async def test_pdr_appena_finito_con_la_vmc_ferma(hass: HomeAssistant, caso: str) -> None:
    """Allerta PdR appena finita (VMC ancora ferma, memoria PdR X, ripristino in attesa) e arrivo degli Inquinanti: la
    VMC va a X per gli Inquinanti; la memoria PdR si spegne, così il ripristino PdR dei 12 s non rimanda X."""
    memoria = f"input_boolean.vmc_master_spia_velocita_{caso}_un_solo_avvio"
    stati = _stati(caso, **{memoria: "on", LETTURA: "Velocità 0", LETTURA_I: "Velocità 0", SPIA_CO2: "off",
                            f"input_boolean.vmc_master_spia_velocita_{caso}_co2_o_voc": "off"})
    comandi = await _esegui(hass, _ramo(TID)["sequence"], stati)
    assert comandi[:1] == [COMANDO[caso]]
    assert _stato(hass, memoria) == "off"
    assert _stato(hass, f"input_boolean.vmc_master_spia_velocita_{caso}_co2_o_voc") == "on"
