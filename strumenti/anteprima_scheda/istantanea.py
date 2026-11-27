"""Stati delle entità della VMC Master dal simulatore (per i test e l'anteprima della scheda).

Legge la riga ``__avvio__`` di un file dei risultati del simulatore (``strumenti/simulatore``,
variante ``identica``: il package YAML di oggi) e scrive lo stato di tutte le entità della VMC
al fork (dopo l'avvio e 300 s di riscaldamento, VMC finta in linea), con gli attributi:

    python istantanea.py <risultati.jsonl> [uscita.json]

Uscita predefinita: ``tests/nativa/scheda/stati_package.json`` (una entità per riga).
Il sensore della versione del repository (``platform: rest``) nel simulatore non c'è.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RADICE / "strumenti/simulatore"))

import tracce

USCITA = RADICE / "tests/nativa/scheda/stati_package.json"


def leggi(percorso: Path) -> dict[str, list]:
    """entity_id -> [stato, attributi] al fork della riga ``__avvio__``."""
    with percorso.open(encoding="utf-8") as flusso:
        riga = json.loads(flusso.readline())
    if riga.get("id") != "__avvio__":
        raise SystemExit(f"{percorso}: la prima riga non è __avvio__")
    dati = tracce.decomprimi(riga)
    return {e: [s, dati["attr"][a]] for e, s, a in dati["finale"]}


def scrivi(stati: dict[str, list], uscita: Path, origine: str) -> None:
    """Una entità per riga, in ordine di entity_id (diff leggibili)."""
    righe = [
        f"  {json.dumps(e, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False, sort_keys=True)}"
        for e, v in sorted(stati.items())
    ]
    testo = (
        "{\n"
        + f'  "__origine__": {json.dumps(origine, ensure_ascii=False)},\n'
        + ",\n".join(righe)
        + "\n}\n"
    )
    uscita.write_text(testo, encoding="utf-8")


if __name__ == "__main__":
    risultati = Path(sys.argv[1])
    uscita = Path(sys.argv[2]) if len(sys.argv) > 2 else USCITA
    stati = leggi(risultati)
    origine = f"simulatore, riga __avvio__ (stato al fork) di {risultati.name}, variante identica"
    sorgente = risultati.parent / "cfg_A/SORGENTE.json"
    if sorgente.exists():
        dati = json.loads(sorgente.read_text(encoding="utf-8"))
        origine += f", package {dati['versione']} (md5 vmc_master.yaml {dati['md5_sorgenti']['vmc_master.yaml']})"
    scrivi(stati, uscita, origine)
    print(f"{len(stati)} entità -> {uscita}")
