"""Prove della 9.0.0b32: correzioni della logica trovate dalla verifica profonda 1:1 e confermate dalle prove
dinamiche (simulatore con Home Assistant reale)."""

from __future__ import annotations

from pathlib import Path

from homeassistant.util import yaml as hay

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"


def _automazione() -> str:
    return (PKG / "vmc_master_automazione.txt").read_text(encoding="utf-8")


def test_automazione_valida_e_versione() -> None:
    dati = hay.load_yaml(str(PKG / "vmc_master_automazione.txt"))
    assert dati
    assert "AUTOMAZIONE VMC HELTY FLOW PLUS RELEASE [VER. 9.0.0b32]" in _automazione()[:1000]


def test_delta_temp_non_cancella_il_ritorno_a_velocita_0_degli_inquinanti() -> None:
    """A1-2: Inquinanti partiti da Velocita' 0 e Δ Temp. scattato prima della memoria Inquinanti (8 s a Velocita' 1):
    a fine Δ la regola 03-11-2026 non deve trattare la Velocita' 1 come scelta dell'utente, cosi' a fine Inquinanti
    la VMC torna a Velocita' 0 (Foglio A28)."""
    testo = _automazione()
    i = testo.index("durante Δ Temp. -> diventa la memoria degli Inquinanti (regola 03-11-2026; non se la Velocità 1")
    condizione = testo[i : testo.index("then:", i)]
    assert "not is_state('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0', 'on')" in condizione
    assert "not is_state('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr', 'on')" in condizione
    # le altre 13 regole (Congelamento e Δ con memorie 0, 2, 3, 4, Notturna, Iperventilazione) restano come prima
    assert testo.count("(regola 03-11-2026)") == 13
