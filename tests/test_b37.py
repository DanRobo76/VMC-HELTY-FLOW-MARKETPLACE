"""Prove della 9.0.0b37: versioni dei file cambiati (scheda e manifest); automazione e script .sh non sono cambiati.

La b37 contiene solo la correzione dell'Offset CO₂/VOC (si somma sempre al valore letto, anche con la sonda della VMC
assente): cambiano vmc_master.yaml (senza VER., la sua versione la scrive l'integrazione), la scheda e il manifest."""

from __future__ import annotations

import json
from pathlib import Path

PKG = Path(__file__).resolve().parents[1] / "custom_components" / "vmc_master" / "package"


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8")


def test_versioni_b37() -> None:
    assert "SCHEDA MANUALE INTERFACCIA VMC HELTY FLOW PLUS RELEASE [VER. 9.0.0b37]" in _testo(
        "vmc_master_scheda_manuale_interfaccia.txt")[:2000]
    manifest = json.loads((PKG.parent / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["version"] == "9.0.0b37"


def test_file_non_cambiati() -> None:
    """Regola del proprietario: la VER. di un file cambia solo quando cambia il file."""
    assert "AUTOMAZIONE VMC HELTY FLOW PLUS RELEASE [VER. 9.0.0b36]" in _testo("vmc_master_automazione.txt")[:1000]
    assert "RELEASE [VER. 9.0.0b31]" in _testo("vmc_master_script_cambio_ip.sh")[:1000]
    assert "RELEASE [VER. 9.0.0b32]" in _testo("vmc_master_script_cambio_nome.sh")[:1000]


def test_package_senza_ver() -> None:
    """vmc_master.yaml non ha una VER. nell'intestazione: rimanda al sensore della versione, scritto dall'integrazione."""
    intestazione = _testo("vmc_master.yaml")[:2000]
    assert "[VER." not in intestazione
    assert "RELEASE [VEDERE VALORE INSERITO NEL SENSORE vmc_master_versione_corrente]" in intestazione
