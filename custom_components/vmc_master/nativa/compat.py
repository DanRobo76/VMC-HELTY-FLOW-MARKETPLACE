"""Le funzioni e i filtri dei modelli di Home Assistant usati dal package, rifatti uguali.

Servono a portare in Python i modelli del package senza cambiare nemmeno un caso limite:
``| float(0)``, ``| int(0)``, ``| round(1)``, ``is_number`` e la scrittura dei valori nel
testo (``{{ x }}``) si comportano come in Home Assistant 2026.11.
"""

from __future__ import annotations

import math
from typing import Any


def fl(valore: Any, predefinito: Any) -> Any:
    """``valore | float(predefinito)``."""
    try:
        return float(valore)
    except (ValueError, TypeError):
        return predefinito


def it(valore: Any, predefinito: Any, base: int = 10) -> Any:
    """``valore | int(predefinito)`` (come jinja2 do_int, usato da Home Assistant)."""
    try:
        if isinstance(valore, str):
            return int(valore, base)
        return int(valore)
    except (TypeError, ValueError):
        try:
            return int(float(valore))
        except (TypeError, ValueError, OverflowError):
            return predefinito


def rnd(valore: Any, precisione: int = 0, predefinito: Any = None) -> Any:
    """``valore | round(precisione)`` (metodo «common» di Home Assistant)."""
    try:
        risultato = round(float(valore), precisione)
        return int(risultato) if precisione == 0 else risultato
    except (ValueError, TypeError):
        if predefinito is None:
            raise
        return predefinito


def is_number(valore: Any) -> bool:
    """``valore | is_number``."""
    try:
        numero = float(valore)
    except (ValueError, TypeError):
        return False
    return math.isfinite(numero)


def testo(valore: Any) -> str:
    """Come ``{{ valore }}`` scrive un valore nel testo del modello."""
    return str(valore)
