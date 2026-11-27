"""Come Home Assistant trasforma il testo reso da un template di sensore nel suo stato.

Un solo posto per le regole che tutti i modelli devono seguire:

- ``interpreta``: il testo reso diventa un valore (``_parse_result``): ``21.30`` il numero
  21.3, ``None`` nessun valore, ``True`` un booleano; liste, dizionari, insiemi e tuple si
  confrontano per valore ma si scrivono come sono stati resi; ogni altro testo resta testo;
- ``scrivi``: lo stato scritto per un valore: decimali con al più 15 cifre significative,
  nessun valore = ``unknown``, uno stato più lungo di 255 caratteri = ``unknown``;
- ``stato_numerico``: per i sensori con unità di misura o classe lo stato è un numero,
  altrimenti ``unknown``;
- ``uguali``: lo stato di un template cambia solo se il nuovo risultato è diverso (``!=``)
  dal precedente: dopo ``100.0`` un risultato ``100`` lascia scritto ``100.0``.
"""

from __future__ import annotations

import ast
import math
import re
from typing import Any

# Stesse costanti di homeassistant.helpers.template (_IS_NUMERIC, dal 2026.11 con
# re.ASCII: «٣» o «１２» restano testo) e helpers.entity (FLOAT_PRECISION), e lunghezza
# massima di uno stato.
NUMERO_SEMPLICE = re.compile(r"^[+-]?(?!0\d)\d*(?:\.\d*)?$", re.ASCII)
PRECISIONE = 15
LUNGHEZZA_MASSIMA = 255
SCONOSCIUTO = "unknown"


class _Errore:
    """Risultato di un template andato in errore (TemplateError)."""

    def __repr__(self) -> str:
        return "ERRORE"


ERRORE: Any = _Errore()


class Contenitore:
    """Lista, dizionario, insieme o tupla resi: si confronta per valore, si scrive com'è reso."""

    __slots__ = ("testo", "valore")

    def __init__(self, valore: Any, testo_reso: str) -> None:
        self.valore = valore
        self.testo = testo_reso

    def __eq__(self, altro: object) -> bool:
        return bool(self.valore == (altro.valore if isinstance(altro, Contenitore) else altro))

    __hash__ = None  # type: ignore[assignment]


def interpreta(resa: str) -> Any:
    """Il risultato del template come lo interpreta Home Assistant (``parse_result``)."""
    resa = resa.strip()
    if NUMERO_SEMPLICE.match(resa):
        try:
            return float(resa) if "." in resa else int(resa)
        except ValueError:
            pass
    try:
        valore = ast.literal_eval(resa)
    except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
        return resa  # RecursionError: dal 2026.11 (un testo lunghissimo come «1+1+1...»)
    if isinstance(valore, (dict, list, set, tuple)):
        return Contenitore(valore, resa)
    if isinstance(valore, (str, complex)):
        return resa  # testo e numeri complessi restano scritti come sono stati resi
    if isinstance(valore, (int, float)) and not isinstance(valore, bool):
        return valore if NUMERO_SEMPLICE.match(resa) else resa  # 1e3, 1_000 restano testo
    return valore


def scrivi(valore: Any) -> str:
    """Lo stato scritto da Home Assistant per un valore."""
    if valore is None:
        return SCONOSCIUTO
    if type(valore) is str:
        testo = valore
    elif isinstance(valore, Contenitore):
        testo = valore.testo
    elif isinstance(valore, float):
        testo = f"{valore:.{PRECISIONE}}"
    else:
        testo = str(valore)
    return SCONOSCIUTO if len(testo) > LUNGHEZZA_MASSIMA else testo


def stato_testo(risultato: Any) -> str:
    """Stato di un sensore senza unità di misura."""
    return scrivi(risultato)


def stato_numerico(risultato: Any) -> str:
    """Stato di un sensore con unità di misura (o classe): un numero, altrimenti ``unknown``.

    Un valore infinito o ``nan`` Home Assistant non lo scrive affatto (resta lo stato di
    prima, con un errore nel registro): qui diventa ``unknown``.
    """
    valore = risultato
    if valore is None or isinstance(valore, bool):
        return SCONOSCIUTO
    if not isinstance(valore, (int, float)):
        try:
            valore = float(valore)
        except Exception:  # noqa: BLE001  (come Coerce(float): ogni errore vale «non numerico»)
            return SCONOSCIUTO
    if not math.isfinite(valore):
        return SCONOSCIUTO
    return scrivi(valore)


def come_stato(resa: str) -> str:
    """Stato di un sensore senza unità per il testo reso dal template."""
    return stato_testo(interpreta(resa))


def come_stato_numerico(resa: str) -> str:
    """Stato di un sensore con unità per il testo reso dal template."""
    return stato_numerico(interpreta(resa))


def uguali(prima: Any, dopo: Any) -> bool:
    """Come Home Assistant: due errori sono uguali; gli altri risultati si confrontano con ``==``."""
    if prima is ERRORE or dopo is ERRORE:
        return prima is dopo
    try:
        return bool(prima == dopo)
    except Exception:  # noqa: BLE001
        return False
