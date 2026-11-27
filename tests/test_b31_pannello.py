"""Prove della 9.0.0b31: pannello «Riattivazione delle Allerte» in cima alla scheda e riga «0»
del 3° gruppo raggiungibile (il timer da 140 s finisce nello stesso secondo del countdown di
gruppo, la fase 4 arriva poco dopo)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from homeassistant.util import yaml as hay

from custom_components.vmc_master import _configurazione_scheda

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"
FILE = "vmc_master_scheda_manuale_interfaccia.txt"
FASE = "input_number.vmc_master_fase_riallineamento_al_riavvio"
T60 = "timer.vmc_master_countdown_avvio_home_assistant"
T140 = "timer.vmc_master_countdown_riattivazione_allerte"
T40 = "timer.vmc_master_countdown_fase_allerte"
STATO = "sensor.vmc_master_status_ip_interfaccia"
TITOLO = "Riattivazione delle Allerte"
INIZIO_INSTALLA = "# >>> INIZIO SEZIONE INSTALLA VMC"
FINE_INSTALLA = "# >>> FINE SEZIONE INSTALLA VMC"


def _testo() -> str:
    return (PKG / FILE).read_text(encoding="utf-8")


def _scheda() -> dict:
    return hay.load_yaml(str(PKG / FILE))


def _ridotta(carta: dict) -> bool:
    return "ferma_off_line" in str(carta.get("card", {}).get("header"))


# ------------------------------------------------------------------ posizione
def test_pannello_prima_carta() -> None:
    carte = _scheda()["cards"]
    assert carte[0]["card"]["title"] == TITOLO
    assert _ridotta(carte[1])
    assert sum(c.get("card", {}).get("title") == TITOLO for c in carte) == 1


def test_sezioni_installa_al_loro_posto() -> None:
    righe = _testo().splitlines()
    inizio = righe.index("cards:")
    assert righe[inizio - 1] == "type: vertical-stack"
    assert righe[inizio + 1] == "  - type: conditional"
    pannello = next(i for i, r in enumerate(righe) if r == f"      title: {TITOLO}")
    installa = [i for i, r in enumerate(righe) if r.startswith((INIZIO_INSTALLA, FINE_INSTALLA))]
    # il pannello viene prima di tutte le sezioni solo Master, che restano dopo la scheda ridotta
    assert pannello < installa[0]
    ridotta = next(i for i, r in enumerate(righe) if "ferma_off_line.webp" in r)
    assert pannello < ridotta < installa[0]


@pytest.mark.parametrize("nome", ["master", "soggiorno"])
def test_pannello_prima_carta_per_ogni_vmc(nome: str) -> None:
    _configurazione_scheda.cache_clear()
    # la scheda della beta (servita finche' la VMC aspetta il passaggio)
    carte = _configurazione_scheda(nome, "192.168.1.170", nativa=False)["cards"]
    assert carte[0]["card"]["title"] == TITOLO
    assert f"timer.vmc_{nome}_countdown_riattivazione_allerte" in str(carte[0]["conditions"])
    assert _ridotta(carte[1])
    # sezioni solo Master tolte: niente Finestra Prima Installazione VMC
    assert "installa_vmc" not in str(carte)
    assert "Prima Installazione VMC" not in str(carte)


# ------------------------------------------------------------------ condizioni
def test_condizioni_del_pannello() -> None:
    assert _scheda()["cards"][0]["conditions"] == [
        {
            "condition": "or",
            "conditions": [
                {"condition": "state", "entity": T140, "state": "active"},
                {"condition": "state", "entity": FASE, "state": "3.0"},
            ],
        },
        {"condition": "state", "entity": STATO, "state": "ON-Line"},
    ]


def _vera(c: dict, stati: dict) -> bool:
    """Condizione di una carta o riga conditional (state, state_not, or, and)."""
    if c.get("condition") == "or":
        return any(_vera(x, stati) for x in c["conditions"])
    if c.get("condition") == "and":
        return all(_vera(x, stati) for x in c["conditions"])
    if "state_not" in c:
        esclusi = c["state_not"] if isinstance(c["state_not"], list) else [c["state_not"]]
        return stati.get(c["entity"]) not in esclusi
    attesi = c["state"] if isinstance(c["state"], list) else [c["state"]]
    return stati.get(c["entity"]) in attesi


def _mostrato(stati: dict) -> list[str] | None:
    """Righe del pannello con gli stati dati; None se il pannello e' nascosto."""
    carta = _scheda()["cards"][0]
    if not all(_vera(c, stati) for c in carta["conditions"]):
        return None
    out = []
    for r in carta["card"]["entities"]:
        if r.get("type") == "conditional":
            if not all(_vera(c, stati) for c in r["conditions"]):
                continue
            r = r["row"]
        if r.get("type") == "section":
            continue
        if r.get("type") == "text":
            out.append(f"{r['name']} | {r['text']}")
        else:
            out.append(f"{r['name']} | {'countdown' if stati.get(r['entity']) == 'active' else 'Inattivo'}")
    return out


def _stati(fase: str, t60: str = "idle", t40: str = "idle", t140: str = "idle", stato: str = "ON-Line") -> dict:
    return {FASE: fase, T60: t60, T40: t40, T140: t140, STATO: stato}


def test_riga_zero_del_terzo_gruppo_raggiungibile() -> None:
    """Fase 3 e tutti i timer finiti (timer da 140 s e countdown di gruppo nello stesso secondo,
    fase 4 circa 0,7 s dopo): il pannello resta e il 3° gruppo mostra «0»."""
    righe = _mostrato(_stati("3.0"))
    assert righe == ["Già attive | ✓", "Già attiva | ✓", "Si riattivano tra | 0"]
    # la riga «0» del 3° gruppo e' compatibile con la condizione esterna
    carta = _scheda()["cards"][0]
    zero = [
        r for r in carta["card"]["entities"]
        if r.get("type") == "conditional" and r["row"].get("text") == "0"
        and {"condition": "state", "entity": FASE, "state": "3.0"} in r["conditions"]
    ]
    assert len(zero) == 1
    assert {"condition": "state", "entity": T40, "state": "idle"} in zero[0]["conditions"]


@pytest.mark.parametrize(
    ("stati", "atteso"),
    [
        # sequenza dell'automazione (60 s, poi 40 s, poi 40 s): come nella b30
        (_stati("1.0", t60="active", t140="active"), ["Si riattivano tra | countdown", "In attesa | dopo il 1° gruppo", "In attesa | dopo il 2° gruppo"]),
        (_stati("1.0", t140="active"), ["Si riattivano tra | 0", "In attesa | dopo il 1° gruppo", "In attesa | dopo il 2° gruppo"]),
        (_stati("2.0", t40="active", t140="active"), ["Già attive | ✓", "Si riattiva tra | countdown", "In attesa | dopo il 2° gruppo"]),
        (_stati("2.0", t140="active"), ["Già attive | ✓", "Si riattiva tra | 0", "In attesa | dopo il 2° gruppo"]),
        (_stati("3.0", t40="active", t140="active"), ["Già attive | ✓", "Già attiva | ✓", "Si riattivano tra | countdown"]),
        (_stati("3.0"), ["Già attive | ✓", "Già attiva | ✓", "Si riattivano tra | 0"]),
        # fase 4: tutte le allerte attive, il pannello sparisce
        (_stati("4.0"), None),
        (_stati("0.0"), None),
        # fasi 1-2 senza il timer da 140 s: nascosto come prima della b31
        (_stati("1.0"), None),
        (_stati("2.0"), None),
        # VMC non ON-Line: nascosto anche in fase 3
        (_stati("3.0", stato="OFF-Line"), None),
        (_stati("3.0", t40="active", t140="active", stato="OFF-Line"), None),
    ],
)
def test_sequenza(stati: dict, atteso: list[str] | None) -> None:
    assert _mostrato(stati) == atteso


# ------------------------------------------------------------------ informazioni
def test_nota_avvio_dice_in_cima() -> None:
    scheda = _testo()
    i = scheda.index("<strong>Nota Avvio di Home Assistant</strong>")
    nota = re.sub(r"\s+", " ", scheda[i : scheda.index("<br>", i)])
    assert "Il pannello «Riattivazione delle Allerte», in cima alla scheda, mostra" in nota
    assert nota.count("in cima") == 1
    assert not re.search(r"\b(sala|camera|cucina)\b", nota, re.IGNORECASE)
