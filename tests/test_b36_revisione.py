"""Prove della b36, rilievi della revisione indipendente.

- B1: con la Spia Comando non eseguito del Calendario accesa, senza fascia, la Spia Inquinanti accesa e l'interruttore
  «VMC ON/OFF in Funzione del Calendario» spento, a fine allerta l'automazione porta la VMC a Velocità 1 (fino al
  rientro degli Inquinanti) anche con la memoria della partenza da Velocità 0 spenta: le schede Congelamento e Δ Temp.
  devono annunciare la Velocità 1, non la Velocità 0.
"""

from __future__ import annotations

import pytest

from tests.test_b36_testi import CNE, _norm, _render, _schede_gelo_delta

SPIA_INQ = "input_boolean.vmc_master_spia_co2_o_voc"
PARTENZA_0 = "input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0"
INTERRUTTORE_CAL = "input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario"
V1 = "LA VMC ANDRÀ ALLA <strong>VELOCITÀ 1 (INQUINANTI PRESENTI)</strong>"
V0 = "LA VMC ANDRÀ ALLA <strong>VELOCITÀ 0</strong>"


@pytest.mark.parametrize(
    ("interruttore", "inquinanti", "partenza_0", "atteso"),
    [
        ("off", "on", "off", V1),
        ("off", "on", "on", V1),
        ("on", "on", "on", V1),
        ("on", "on", "off", V0),
        ("off", "off", "off", V0),
        ("off", "off", "on", V0),
    ],
)
async def test_annuncio_comando_in_sospeso_come_l_automazione(hass, interruttore: str, inquinanti: str,
                                                               partenza_0: str, atteso: str) -> None:
    """Stessa condizione del ramo dell'automazione «Spia Inquinanti accesa con la memoria della partenza da Velocità 0
    accesa oppure con l'interruttore del Calendario spento»."""
    from homeassistant.util import dt as dt_util

    giorno = ["lunedi", "martedi", "mercoledi", "giovedi", "venerdi", "sabato", "domenica"][dt_util.now().weekday()]
    hass.states.async_set(CNE, "on")
    hass.states.async_set(f"input_boolean.vmc_master_spia_calendario_{giorno}_1", "off")
    hass.states.async_set(f"input_boolean.vmc_master_spia_calendario_{giorno}_2", "off")
    hass.states.async_set(INTERRUTTORE_CAL, interruttore)
    hass.states.async_set(SPIA_INQ, inquinanti)
    hass.states.async_set(PARTENZA_0, partenza_0)
    schede = _schede_gelo_delta()
    assert len(schede) == 2
    for testa, annunci in schede:
        assert annunci
        for annuncio in annunci:
            testo = _norm(_render(hass, testa + annuncio, {"spia_velocita_2": "on"}))
            assert atteso in testo, testo


def test_condizione_dell_automazione_invariata() -> None:
    """La condizione che l'annuncio copia è ancora quella dell'automazione."""
    from pathlib import Path

    aut = (Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"
           / "vmc_master_automazione.txt").read_text(encoding="utf-8")
    assert (f"{{{{ states('{SPIA_INQ}') == 'on'\n"
            f"                      and (states('{PARTENZA_0}') == 'on'\n"
            f"                      or states('{INTERRUTTORE_CAL}') == 'off') }}}}") in aut
