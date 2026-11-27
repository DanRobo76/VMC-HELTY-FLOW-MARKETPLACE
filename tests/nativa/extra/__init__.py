"""Valori in piu' per il banco di confronto, uno per gruppo di modelli.

Ogni modulo di questa cartella puo' definire:
- ``INGRESSI``: entity_id letti dai modelli che il banco non trova da solo;
- ``EXTRA``: {entity_id: [valori]} da aggiungere ai candidati di un ingresso;
- ``UN_SOLO_RISULTATO``: {chiave: motivo} modelli che danno sempre lo stesso risultato;
- ``SCENARI``: {nome: {entity_id: valore}} combinazioni da imporre insieme in alcuni giri,
  per i casi che i cambi a caso non raggiungono (es. una ventina di spie tutte «off»).
"""

from __future__ import annotations

import importlib
import pkgutil

INGRESSI: set[str] = set()
EXTRA: dict[str, set[str]] = {}
UN_SOLO_RISULTATO: dict[str, str] = {}
SCENARI: dict[str, dict[str, str]] = {}

for _info in pkgutil.iter_modules(__path__):
    _m = importlib.import_module(f"{__name__}.{_info.name}")
    INGRESSI |= set(getattr(_m, "INGRESSI", ()))
    for _eid, _valori in getattr(_m, "EXTRA", {}).items():
        EXTRA.setdefault(_eid, set()).update(_valori)
    UN_SOLO_RISULTATO.update(getattr(_m, "UN_SOLO_RISULTATO", {}))
    for _nome, _scenario in getattr(_m, "SCENARI", {}).items():
        if _nome in SCENARI:
            raise ValueError(f"scenario con lo stesso nome in due gruppi: {_nome}")
        SCENARI[_nome] = dict(_scenario)
