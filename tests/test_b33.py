"""Prove della 9.0.0b33: versioni dei file cambiati (scheda, automazione, manifest)."""

from __future__ import annotations

import json
import re
from pathlib import Path

PKG = Path(__file__).resolve().parents[1] / "custom_components" / "vmc_master" / "package"


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8")


def test_versioni_b33() -> None:
    """Scheda, automazione e manifest sono cambiati nella b33: la loro versione e' almeno 9.0.0b33."""
    scheda = re.search(r"SCHEDA MANUALE INTERFACCIA VMC HELTY FLOW PLUS RELEASE \[VER\. 9\.0\.0b(\d+)\]",
                       _testo("vmc_master_scheda_manuale_interfaccia.txt")[:2000])
    assert scheda and int(scheda.group(1)) >= 33
    automazione = re.search(r"AUTOMAZIONE VMC HELTY FLOW PLUS RELEASE \[VER\. 9\.0\.0b(\d+)\]",
                            _testo("vmc_master_automazione.txt")[:1000])
    assert automazione and int(automazione.group(1)) >= 33
    manifest = json.loads((PKG.parent / "manifest.json").read_text(encoding="utf-8"))
    assert re.fullmatch(r"9\.0\.0b(\d+)", manifest["version"]) and int(manifest["version"].split("b")[1]) >= 33


def test_script_non_cambiati_restano_b32() -> None:
    """Regola del proprietario: la VER. di un file cambia solo quando cambia il file."""
    assert "RELEASE [VER. 9.0.0b32]" in _testo("vmc_master_script_cambio_nome.sh")[:1000]
