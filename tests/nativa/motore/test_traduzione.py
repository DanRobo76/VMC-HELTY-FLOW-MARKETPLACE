"""Il codice generato del motore è aggiornato rispetto al package e al traduttore.

Con ``VMC_RIGENERA=1`` il test riscrive ``motore/generato/`` (e toglie i moduli che il
traduttore non scrive più, per esempio una parte in meno).
"""

from __future__ import annotations

import os

from homeassistant.core import HomeAssistant

from .traduci import GENERATO, contenuto, traduci


async def test_codice_generato_aggiornato(hass: HomeAssistant) -> None:
    """Ogni modulo generato è quello che scrive oggi il traduttore, e non ce ne sono
    altri."""
    moduli = await traduci(hass)
    if os.environ.get("VMC_RIGENERA"):
        GENERATO.mkdir(exist_ok=True)
        for nome, testo in moduli.items():
            (GENERATO / nome).write_text(testo, encoding="utf-8")
        for percorso in GENERATO.glob("*.py"):
            if percorso.name not in moduli:
                percorso.unlink()
    vecchi = []
    for nome, testo in moduli.items():
        percorso = GENERATO / nome
        if not percorso.exists() or contenuto(
            percorso.read_text(encoding="utf-8")
        ) != contenuto(testo):
            vecchi.append(nome)
    altri = sorted(p.name for p in GENERATO.glob("*.py") if p.name not in moduli)
    assert not vecchi, f"da rigenerare (VMC_RIGENERA=1): {vecchi}"
    assert not altri, f"moduli che il traduttore non scrive più: {altri}"
