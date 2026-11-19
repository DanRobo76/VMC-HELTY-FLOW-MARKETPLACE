"""Prove della 9.0.0b32: testi e commenti corretti dalla verifica profonda 1:1 (licenza, nome VMC)."""

from __future__ import annotations

from pathlib import Path

from custom_components.vmc_master import trasforma

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8")


def test_licenza_con_il_nome_dell_integrazione() -> None:
    """La riga della licenza nomina l'integrazione (una sola per tutte le VMC), non la VMC."""
    for nome in ("vmc_master.yaml", "vmc_master_automazione.txt", "vmc_master_scheda_manuale_interfaccia.txt",
                 "vmc_master_script_cambio_ip.sh", "vmc_master_script_cambio_nome.sh"):
        riscritto = trasforma.rinomina(_testo(nome), "prova")
        assert riscritto.count("L'INTEGRAZIONE VMC MASTER") == 2, nome
        assert "INTEGRAZIONE VMC PROVA" not in riscritto, nome
        assert ("vmc_prova" in riscritto) == ("vmc_master" in _testo(nome)), nome


def test_script_cambio_nome() -> None:
    script = _testo("vmc_master_script_cambio_nome.sh")
    assert "RELEASE [VER. 9.0.0b32]" in script[:1000]
    assert "NE AMMETTE FINO A 12, LA SCHEDA 10" in script
    assert "pattern: '^[A-Za-z0-9_-]{0,10}$'" in _testo("vmc_master.yaml")
