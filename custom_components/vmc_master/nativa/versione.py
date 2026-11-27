"""Versione dell'integrazione, letta una volta sola da manifest.json.

Il package della beta la scriveva nel sensore «Package Ver.» quando veniva generato
(``trasforma.adatta_versione`` con ``integrazione.version``). La versione nativa mostra la
stessa nel sensore «Versione»: il modello Python (``modelli/stato_vmc.py``) e il sensore
template tradotto (``motore/generato_fase4/sensori.py``) la prendono da qui.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Final


def _leggi_versione() -> str:
    manifest = Path(__file__).resolve().parents[1] / "manifest.json"
    return str(json.loads(manifest.read_text(encoding="utf-8"))["version"])


VERSIONE_INTEGRAZIONE: Final = _leggi_versione()
