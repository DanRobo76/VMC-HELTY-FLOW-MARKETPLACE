"""L'inventario degli aiutanti (fase 4) è aggiornato e i suoi conti tornano.

Con ``VMC_RIGENERA=1`` il test riscrive i file ``inventario_aiutanti*``.
"""

from __future__ import annotations

import os
import re
from collections import Counter

from homeassistant.core import HomeAssistant

from .inventario_aiutanti import (
    DOMINI_SIMILI,
    QUI,
    Inventario,
    inventario,
    leggi_fase1,
    uscite,
)

_FATTO: list[Inventario] = []


async def _inventario(hass: HomeAssistant) -> Inventario:
    """L'inventario, calcolato una volta sola per processo."""
    if not _FATTO:
        _FATTO.append(await inventario(hass))
    return _FATTO[0]


async def test_inventario_aggiornato(hass: HomeAssistant) -> None:
    """I file dell'inventario sono quelli che lo script scrive oggi."""
    testi = uscite(await _inventario(hass))
    if os.environ.get("VMC_RIGENERA"):
        for nome, testo in testi.items():
            (QUI / nome).write_text(testo, encoding="utf-8")
    vecchi = [
        nome
        for nome, testo in testi.items()
        if not (QUI / nome).exists() or (QUI / nome).read_text("utf-8") != testo
    ]
    assert not vecchi, f"da rigenerare (VMC_RIGENERA=1): {vecchi}"


async def test_le_voci_sono_quelle_della_fase_1(hass: HomeAssistant) -> None:
    """Le 342 voci «da aiutante» del package sono quelle dell'inventario approvato."""
    inv = await _inventario(hass)
    fase1 = leggi_fase1()
    del_package = {e for e, tipo in inv.entita.items() if tipo in DOMINI_SIMILI}
    assert set(fase1) == del_package
    assert Counter(riga["Tipo oggi"] for riga in fase1.values()) == {
        "input_boolean": 115,
        "input_number": 43,
        "input_text": 38,
        "input_select": 15,
        "input_datetime": 30,
        "timer": 34,
        "script": 51,
        "shell_command": 16,
    }
    interne = [r for r in fase1.values() if r["Domani"].startswith("interna")]
    # con le 13 automazioni del motore fanno le 121 voci «interne»; dalla b46 3 voci sono
    # tolte (il campo «Cambia IP VMC», il suo esito e il comando che scriveva l'IP)
    assert len(interne) == 108
    assert sum(r["Domani"] == "tolta" for r in fase1.values()) == 3


async def test_i_conti_tornano_con_il_testo(hass: HomeAssistant) -> None:
    """Controllo indipendente: per ogni entità del package, le volte che il suo
    entity_id è scritto nei modelli (cercato nel testo, senza i commenti di Jinja) sono
    le letture più le citazioni come costante che l'inventario ha contato dall'albero."""
    inv = await _inventario(hass)
    contate: Counter[str] = Counter()
    for (entita, *_resto), quante in inv.letture.items():
        contate[entita] += quante
    for (entita, _posizione, dove), quante in inv.costanti.items():
        if dove != "costante nella configurazione":
            contate[entita] += quante
    nel_testo: Counter[str] = Counter()
    cerca = re.compile(r"(?<![A-Za-z0-9_])(?:states\.)?([a-z_]+\.[a-z0-9_]+)")
    for sorgente, posti in inv.posti.items():
        senza_commenti = re.sub(r"\{#.*?#\}", "", sorgente, flags=re.DOTALL)
        for trovato in cerca.finditer(senza_commenti.replace("\\.", ".")):
            if trovato.group(1) in inv.entita:
                nel_testo[trovato.group(1)] += posti
    assert nel_testo == contate
    assert sum(contate.values()) > 25000


async def test_i_totali_principali(hass: HomeAssistant) -> None:
    """I numeri che il resoconto della fase 4 cita."""
    inv = await _inventario(hass)
    assert {k: v for k, v in inv.trigger.items() if " " not in k} == {
        "template": 433,
        "state": 79,
        "event": 18,
        "homeassistant": 6,
        "time": 3,
        "time_pattern": 2,
    }
    assert len(inv.eventi) == 18
    assert Counter(evento[3] for evento in inv.eventi) == {
        "call_service": 17,
        "timer.finished": 1,
    }
    assert sum(inv.modelli.values()) == 3241
    assert len(inv.posti) == 1033
    # nessun timer si ripristina al riavvio, nessun servizio dei timer oltre start/cancel
    assert not any(timer.get("restore") for timer in inv.timer.values())
    assert {s for s in inv.servizi if s.startswith("timer.")} == {
        "timer.start",
        "timer.cancel",
    }
    # dei servizi degli aiutanti il package usa solo questi
    assert {s for s in inv.servizi if s.split(".")[0].startswith("input_")} == {
        "input_boolean.turn_on",
        "input_boolean.turn_off",
        "input_number.set_value",
        "input_select.select_option",
        "input_select.set_options",
        "input_text.set_value",
        "input_datetime.set_datetime",
    }
    # il contesto si legge solo dall'evento call_service; mai ``context`` né ``this``
    assert Counter(c[0] for c in inv.contesto) == {
        "last_changed": 1005,
        "context": 3,
        "last_reported": 1,
    }
    assert not any(
        catena.split(".")[0] in ("context", "this") for catena, _ in inv.radici
    )
