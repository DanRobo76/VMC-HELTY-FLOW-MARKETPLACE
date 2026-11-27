"""Il codice generato della fase 4 è aggiornato rispetto al package e al traduttore.

Con ``VMC_RIGENERA=1`` il test riscrive ``motore/generato_fase4/`` (e toglie i moduli
che il traduttore non scrive più).
"""

from __future__ import annotations

import os

from homeassistant.core import HomeAssistant

from .traduci import contenuto
from .traduci_fase4 import GENERATO_FASE4, mappa_fase4, traduci_fase4


async def test_codice_generato_fase4_aggiornato(hass: HomeAssistant) -> None:
    """Ogni modulo di ``generato_fase4/`` è quello che scrive oggi il traduttore con
    tutte le opzioni della fase 4, e non ce ne sono altri."""
    moduli = await traduci_fase4(hass)
    if os.environ.get("VMC_RIGENERA"):
        GENERATO_FASE4.mkdir(exist_ok=True)
        for nome, testo in moduli.items():
            (GENERATO_FASE4 / nome).write_text(testo, encoding="utf-8")
        for percorso in GENERATO_FASE4.glob("*.py"):
            if percorso.name not in moduli:
                percorso.unlink()
    vecchi = []
    for nome, testo in moduli.items():
        percorso = GENERATO_FASE4 / nome
        if not percorso.exists() or contenuto(
            percorso.read_text(encoding="utf-8")
        ) != contenuto(testo):
            vecchi.append(nome)
    altri = sorted(p.name for p in GENERATO_FASE4.glob("*.py") if p.name not in moduli)
    assert not vecchi, f"da rigenerare (VMC_RIGENERA=1): {vecchi}"
    assert not altri, f"moduli che il traduttore non scrive più: {altri}"


def test_mappa_della_fase_4() -> None:
    """La mappa: i 172 aiutanti visibili (dalla b46 senza il campo «Cambia IP VMC»),
    stesso oggetto, nessun servizio cambiato."""
    mappa = mappa_fase4()
    domini: dict[str, int] = {}
    for vecchia, nuova in mappa.entita.items():
        assert vecchia.split(".", 1)[1] == nuova.split(".", 1)[1]
        coppia = f"{vecchia.split('.')[0]} -> {nuova.split('.')[0]}"
        domini[coppia] = domini.get(coppia, 0) + 1
    assert domini == {
        "input_boolean -> binary_sensor": 77,
        "input_boolean -> switch": 37,
        "input_datetime -> time": 30,
        "input_number -> number": 10,
        "input_number -> sensor": 1,
        "input_select -> select": 14,
        "input_select -> sensor": 1,
        "input_text -> sensor": 1,
        "input_text -> text": 1,
    }
    assert sum(domini.values()) == 172
    assert not mappa.servizi
