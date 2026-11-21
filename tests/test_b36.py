"""Prove della 9.0.0b36: versioni dei file cambiati (scheda, automazione, manifest); gli script .sh non sono cambiati."""

from __future__ import annotations

import json
from pathlib import Path

PKG = Path(__file__).resolve().parents[1] / "custom_components" / "vmc_master" / "package"


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8")


def test_versioni_b36() -> None:
    assert "SCHEDA MANUALE INTERFACCIA VMC HELTY FLOW PLUS RELEASE [VER. 9.0.0b36]" in _testo(
        "vmc_master_scheda_manuale_interfaccia.txt")[:2000]
    assert "AUTOMAZIONE VMC HELTY FLOW PLUS RELEASE [VER. 9.0.0b36]" in _testo("vmc_master_automazione.txt")[:1000]
    manifest = json.loads((PKG.parent / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["version"] == "9.0.0b36"


def test_script_non_cambiati() -> None:
    """Regola del proprietario: la VER. di un file cambia solo quando cambia il file."""
    assert "RELEASE [VER. 9.0.0b31]" in _testo("vmc_master_script_cambio_ip.sh")[:1000]
    assert "RELEASE [VER. 9.0.0b32]" in _testo("vmc_master_script_cambio_nome.sh")[:1000]
