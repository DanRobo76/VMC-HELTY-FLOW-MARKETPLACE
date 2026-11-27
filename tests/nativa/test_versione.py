"""Il sensore «Versione» mostra la versione dell'integrazione (manifest.json).

Il package della beta la scriveva quando veniva generato (adatta_versione con
integrazione.version). Le due implementazioni native (modello Python e sensore template
tradotto) devono leggere la stessa fonte, anche quando le tabelle vengono da un package
di un'altra versione (tabelle.VERSIONE_PACKAGE).
"""

from __future__ import annotations

import json
from pathlib import Path

from custom_components.vmc_master.nativa.modelli.stato_vmc import versione_corrente
from custom_components.vmc_master.nativa.versione import VERSIONE_INTEGRAZIONE

_RADICE = Path(__file__).resolve().parents[2] / "custom_components" / "vmc_master"


def test_versione_dal_manifest() -> None:
    manifest = json.loads((_RADICE / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["version"] == VERSIONE_INTEGRAZIONE


def test_modello_python_mostra_la_versione_dell_integrazione() -> None:
    assert versione_corrente(None) == f"v.{VERSIONE_INTEGRAZIONE}"


def test_sensore_tradotto_mostra_la_versione_dell_integrazione() -> None:
    sorgente = (
        _RADICE / "nativa" / "motore" / "generato_fase4" / "sensori.py"
    ).read_text(encoding="utf-8")
    assert "VERSIONE_PACKAGE" not in sorgente
    assert sorgente.count("c.statico('v.' + VERSIONE_INTEGRAZIONE)") == 1
