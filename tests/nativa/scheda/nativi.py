"""Le entità native che la scheda tradotta può usare e i loro stati «come domani».

- ``insieme_nativo``: le entità della VMC Master che domani esistono: gli aiutanti, gli script
  e i comandi di shell che restano visibili (colonna «Domani» di ``aiutanti_fase1.csv``, non
  «interna» né «tolta») e i sensori e sensori binari nativi della fase 2
  (``tabelle.SENSORI``);
- ``stati_nativi``: dagli stati di oggi (aiutanti del package) gli stati che avranno le entità
  native nella stessa situazione, con gli attributi che Home Assistant scrive per il loro
  dominio (``NumberEntity``: min, max, step, mode; ``SelectEntity``: options; ``TextEntity``:
  min, max, pattern, mode; ``TimeEntity``, ``SwitchEntity``, ``ButtonEntity``: nessuno; il
  sensore di un timer: classe timestamp, stato = ora di fine o ``unknown``). L'anteprima della
  scheda controlla che le entità vere di Home Assistant scrivano proprio questi attributi.
- ``vero`` / ``condizioni``: le condizioni della plancia (``conditional``, ``visibility``)
  valutate come il frontend 20261028 (``validate-condition.ts``).
"""

from __future__ import annotations

import json
import math
from collections.abc import Iterator, Mapping
from pathlib import Path
from typing import Any

from custom_components.vmc_master.nativa.tabelle import SENSORI

from .traduci_scheda import FASE_1, TOLTA, _leggi_csv, mappa_fase_1

STATI_PACKAGE = Path(__file__).with_name("stati_package.json")
NOME = "master"
Stati = dict[str, tuple[str, dict[str, Any]]]

_BASE = ("friendly_name", "icon")


def insieme_nativo(nome: str = NOME) -> set[str]:
    """Le entità che domani ci sono per la VMC ``nome``."""
    domani = {
        riga["Domani"].replace("vmc_master_", f"vmc_{nome}_", 1)
        for riga in _leggi_csv(FASE_1)
        if not riga["Domani"].startswith("interna") and riga["Domani"] != TOLTA
    }
    sensori = {
        f"{chiave.split('.', 1)[0]}.vmc_{nome}_{chiave.split('.', 1)[1]}"
        for chiave in SENSORI
    }
    return domani | sensori


def interne() -> set[str]:
    """Le voci di oggi che domani non sono entità (stato interno del motore, o tolte)."""
    return {oggi for oggi, domani in mappa_fase_1().items() if domani is None}


def leggi_stati() -> Stati:
    """Gli stati di oggi (simulatore, VMC Master in linea dopo il riscaldamento)."""
    dati = json.loads(STATI_PACKAGE.read_text(encoding="utf-8"))
    dati.pop("__origine__")
    return {e: (v[0], v[1]) for e, v in dati.items()}


def _numero(stato: str) -> str:
    try:
        return str(float(stato))
    except ValueError:
        return stato


def stato_nativo(
    vecchia: str,
    nuova: str,
    stato: str,
    attributi: Mapping[str, Any],
    mappa: Mapping[str, str | None],
) -> tuple[str, dict[str, Any]]:
    """Lo stato dell'entità nativa ``nuova`` quando quella di oggi ``vecchia`` vale ``stato``."""
    oggi, domani = vecchia.split(".", 1)[0], nuova.split(".", 1)[0]
    base = {k: attributi[k] for k in _BASE if k in attributi}
    if oggi == domani:
        return stato, dict(attributi)
    if oggi == "input_boolean":
        return stato, base
    if oggi == "input_number":
        unita = (
            {"unit_of_measurement": attributi["unit_of_measurement"]}
            if "unit_of_measurement" in attributi
            else {}
        )
        if domani == "number":
            limiti = {k: float(attributi[k]) for k in ("min", "max", "step")}
            return _numero(stato), {
                **limiti,
                "mode": attributi["mode"],
                **unita,
                **base,
            }
        return _numero(stato), {**unita, **base}
    if oggi == "input_select":
        if domani == "select":
            return stato, {"options": list(attributi["options"]), **base}
        return (mappa.get(stato) or stato), base
    if oggi == "input_text":
        if domani == "text":
            return stato, {
                k: attributi[k] for k in ("min", "max", "pattern", "mode")
            } | base
        return stato, base
    if oggi == "input_datetime":
        return stato, base
    if oggi == "timer":
        fine = attributi.get("finishes_at") if stato == "active" else None
        return (fine or "unknown"), {"device_class": "timestamp", **base}
    if oggi == "script":
        return "unknown", base
    raise ValueError(f"{vecchia} -> {nuova}: dominio non previsto")


def stati_nativi(stati: Stati, mappa: Mapping[str, str | None] | None = None) -> Stati:
    """Gli stati delle entità native che corrispondono agli stati di oggi ``stati``."""
    mappa = mappa_fase_1() if mappa is None else mappa
    uscita: Stati = {}
    for vecchia, (stato, attributi) in stati.items():
        nuova = mappa.get(vecchia)
        if nuova is None:
            continue
        uscita[nuova] = stato_nativo(vecchia, nuova, stato, attributi, mappa)
    return uscita


# --------------------------------------------------------------- condizioni della plancia
def _stato_di(stati: Mapping[str, tuple[str, Any]], entita: str | None) -> str | None:
    if entita and entita in stati:
        return stati[entita][0]
    return None


def vero(condizione: Mapping[str, Any], stati: Mapping[str, tuple[str, Any]]) -> bool:
    """Una condizione come la valuta il frontend (state, numeric_state, and, or)."""
    tipo = condizione.get("condition", "state")
    if tipo in ("and", "or"):
        figlie = condizione.get("conditions") or []
        esiti = [vero(c, stati) for c in figlie]
        return all(esiti) if tipo == "and" else any(esiti)
    if tipo == "state":
        stato = _stato_di(stati, condizione.get("entity"))
        stato = "unknown" if stato is None else stato
        valore = (
            condizione["state"]
            if "state" in condizione
            else condizione.get("state_not")
        )
        if valore is None:
            return False
        valori = list(valore) if isinstance(valore, list) else [valore]
        valori = [str(v) for v in valori]
        valori += [stati[v][0] for v in valori if v in stati]
        return (stato in valori) if "state" in condizione else (stato not in valori)
    if tipo == "numeric_state":
        stato = _stato_di(stati, condizione.get("entity"))
        try:
            numero = float(stato) if stato is not None else float("nan")
        except ValueError:
            return False
        if math.isnan(numero):
            return False
        sopra, sotto = condizione.get("above"), condizione.get("below")
        return (sopra is None or float(sopra) < numero) and (
            sotto is None or float(sotto) > numero
        )
    raise ValueError(f"condizione {tipo!r} non prevista")


def condizioni(config: Any) -> Iterator[list[Mapping[str, Any]]]:
    """Ogni elenco di condizioni della scheda (``conditions`` delle schede e righe
    ``conditional``, ``visibility``), nell'ordine in cui compaiono."""
    if isinstance(config, Mapping):
        if config.get("type") == "conditional":
            yield list(config.get("conditions") or [])
        if "visibility" in config:
            yield list(config["visibility"])
        for chiave, valore in config.items():
            if chiave not in ("conditions", "visibility"):
                yield from condizioni(valore)
    elif isinstance(config, list):
        for valore in config:
            yield from condizioni(valore)


def modelli(config: Any) -> Iterator[str]:
    """Ogni testo con Jinja della scheda, nell'ordine in cui compare."""
    if isinstance(config, Mapping):
        for valore in config.values():
            yield from modelli(valore)
    elif isinstance(config, list):
        for valore in config:
            yield from modelli(valore)
    elif isinstance(config, str) and ("{{" in config or "{%" in config):
        yield config
