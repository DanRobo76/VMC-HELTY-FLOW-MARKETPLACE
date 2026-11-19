"""Prove della 9.0.0b30: pannello «Riattivazione delle Allerte» con un countdown per gruppo,
uno dopo l'altro (60 s, poi 40 s, poi 40 s)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from homeassistant.util import yaml as hay

from custom_components.vmc_master.trasforma import per_vmc

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"
FASE = "input_number.vmc_master_fase_riallineamento_al_riavvio"
T60 = "timer.vmc_master_countdown_avvio_home_assistant"
T140 = "timer.vmc_master_countdown_riattivazione_allerte"
T40 = "timer.vmc_master_countdown_fase_allerte"


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8")


def _riallineamento() -> dict:
    pacchetto = hay.load_yaml(str(PKG / "vmc_master.yaml"))
    return next(a for a in pacchetto["automation"] if a.get("id") == "vmc_master_riallineamento_allerte_al_riavvio")


def _pannello() -> dict:
    scheda = hay.load_yaml(str(PKG / "vmc_master_scheda_manuale_interfaccia.txt"))
    return next(c for c in scheda["cards"] if T140 in str(c.get("conditions")))["card"]


# ------------------------------------------------------------------ timer nuovo
def test_timer_di_gruppo() -> None:
    timer = hay.load_yaml(str(PKG / "vmc_master.yaml"))["timer"]["vmc_master_countdown_fase_allerte"]
    assert timer == {"name": "Riattivazione Gruppo di Allerte", "duration": "00:00:40", "icon": "mdi:timer-sand"}
    # niente restore: dopo un riavvio a meta' sequenza non torna un countdown vecchio


def test_timer_di_gruppo_escluso_e_ripulito() -> None:
    pacchetto = _testo("vmc_master.yaml")
    escluse = pacchetto[pacchetto.index("&vmc_master_entita_escluse_recorder") :]
    assert T40 in escluse[: escluse.index("\n\n")]
    corpo = pacchetto[pacchetto.index('\n    alias: "VMC Master - Pulisci cronologia Entità"') :]
    assert T40 in corpo[: corpo.index("\n    alias:", 10)]
    scheda = _testo("vmc_master_scheda_manuale_interfaccia.txt")
    assert f"'{T40}'," in scheda  # elenco del pannello Pulisci cronologia


def _conta_configurazione(entita: str) -> int:
    """Regola dell'intestazione: la riga di definizione conta 1, non si contano i commenti
    ne' la sezione recorder:."""
    modello = re.compile(re.escape(entita) + r"(?![A-Za-z0-9_])")
    n, recorder = 1, False
    for riga in _testo("vmc_master.yaml").splitlines():
        if riga.startswith("recorder:"):
            recorder = True
            continue
        if recorder and riga[:1] not in ("", " ", "#"):
            recorder = False
        if recorder or riga.lstrip().startswith("#"):
            continue
        n += len(modello.findall(riga.split("#", 1)[0]))
    return n


@pytest.mark.parametrize("entita", [T40, T60, T140, FASE])
def test_richiami_aggiornati(entita: str) -> None:
    modello = re.compile(re.escape(entita) + r"(?![A-Za-z0-9_])")
    oggetto = entita.split(".", 1)[1]
    commento = re.search(rf"\n  {oggetto}: +# (.+)", _testo("vmc_master.yaml")).group(1)
    attesi = (
        f"[CONFIGURAZIONE, {_conta_configurazione(entita)} RICHIAMI] "
        f"[INTERFACCIA, {len(modello.findall(_testo('vmc_master_scheda_manuale_interfaccia.txt')))} RICHIAMI] "
        f"[AUTOMAZIONE, {len(modello.findall(_testo('vmc_master_automazione.txt')))} RICHIAMI]"
    )
    assert commento.startswith(attesi), (commento[:120], attesi)


# ------------------------------------------------------------------ automazione
def test_countdown_di_gruppo_avviati_prima_delle_fasi() -> None:
    azioni = _riallineamento()["actions"]
    # all'inizio nessun countdown di gruppo rimasto da un riallineamento interrotto
    primo_ritardo = next(i for i, a in enumerate(azioni) if "delay" in a)
    assert any(
        a.get("action") == "timer.cancel" and a["target"]["entity_id"] == T40 for a in azioni[:primo_ritardo]
    )
    for valore in (2, 3):
        i = next(
            i for i, a in enumerate(azioni)
            if a.get("action") == "input_number.set_value" and a["data"]["value"] == valore
        )
        avvio = azioni[i - 1]
        assert avvio["action"] == "timer.start" and avvio["target"]["entity_id"] == T40
        assert avvio["data"] == {"duration": "00:00:40"}
        # 40 s = stacco fino alla fase successiva
        assert azioni[i + 1] == {"delay": {"seconds": 40}}


def test_descrizione_del_riallineamento() -> None:
    descrizione = _riallineamento()["description"]
    assert "Tutte le allerte attive tra" not in descrizione
    assert "un countdown per gruppo, uno dopo l'altro" in re.sub(r"\s+", " ", descrizione)
    assert not re.search(r"\b(timer|input_number|sensor|automation)\.", descrizione)
    assert "master" not in descrizione


# ------------------------------------------------------------------ pannello
def _visibili(righe: list, stati: dict) -> list[str]:
    """Righe mostrate dal pannello con gli stati dati (simula le conditional della scheda)."""
    def vera(c: dict) -> bool:
        attesi = c["state"] if isinstance(c["state"], list) else [c["state"]]
        return stati.get(c["entity"]) in attesi

    out = []
    for r in righe:
        if r.get("type") == "conditional":
            if not all(vera(c) for c in r["conditions"]):
                continue
            r = r["row"]
        if r.get("type") == "section":
            out.append(r["label"])
        elif r.get("type") == "text":
            out.append(f"{r['name']} | {r['text']}")
        else:
            out.append(f"{r['name']} | {'countdown ' + r['entity'] if stati.get(r['entity']) == 'active' else 'Inattivo'}")
    return out


INTRO = "Home Assistant si è appena avviato: le allerte ripartono da sole, un gruppo dopo l'altro. Non serve fare nulla."
G1 = "1° gruppo: Black-Out, Congelamento, Diff. Temp."
G2 = "2° gruppo: Inquinanti"
G3 = "3° gruppo: Punto di Rugiada, Free Heating/Cooling, Calendario, Umidità"


@pytest.mark.parametrize(
    ("fase", "t60", "t40", "attese"),
    [
        ("1.0", "active", "idle", [INTRO, G1, f"Si riattivano tra | countdown {T60}", G2, "In attesa | dopo il 1° gruppo", G3, "In attesa | dopo il 2° gruppo"]),
        ("2.0", "idle", "active", [INTRO, G1, "Già attive | ✓", G2, f"Si riattiva tra | countdown {T40}", G3, "In attesa | dopo il 2° gruppo"]),
        ("3.0", "idle", "active", [INTRO, G1, "Già attive | ✓", G2, "Già attiva | ✓", G3, f"Si riattivano tra | countdown {T40}"]),
        # timer finito meno di 1 s prima del cambio di fase: la riga sparisce, mai «Inattivo»
        ("1.0", "idle", "idle", [INTRO, G1, G2, "In attesa | dopo il 1° gruppo", G3, "In attesa | dopo il 2° gruppo"]),
        ("2.0", "idle", "idle", [INTRO, G1, "Già attive | ✓", G2, G3, "In attesa | dopo il 2° gruppo"]),
    ],
)
def test_un_countdown_per_gruppo(fase: str, t60: str, t40: str, attese: list[str]) -> None:
    pannello = _pannello()
    assert pannello["title"] == "Riattivazione delle Allerte"
    assert _visibili(pannello["entities"], {FASE: fase, T60: t60, T40: t40}) == attese


def test_pannello_per_le_altre_vmc() -> None:
    scheda = per_vmc(_testo("vmc_master_scheda_manuale_interfaccia.txt"), "sala", "192.168.1.161")
    pacchetto = per_vmc(_testo("vmc_master.yaml"), "sala", "192.168.1.161")
    assert scheda.count(T40.replace("master", "sala")) == _testo("vmc_master_scheda_manuale_interfaccia.txt").count(T40)
    assert "  vmc_sala_countdown_fase_allerte:" in pacchetto
    assert "timer.vmc_master_" not in scheda


def test_testi_aggiornati() -> None:
    scheda = re.sub(r"\s+", " ", _testo("vmc_master_scheda_manuale_interfaccia.txt"))
    assert "Tutte le allerte attive tra" not in scheda
    assert "Tutte le allerte attive tra" not in _testo("vmc_master.yaml")
    assert "un countdown per gruppo, uno dopo l'altro: il gruppo in corso conta i secondi" in scheda
    # la riga «Avvio di Home Assistant» del riquadro della VMC resta (Black-Out, VMC nuova)
    assert 'name: "Avvio di Home Assistant"' in _testo("vmc_master_scheda_manuale_interfaccia.txt")
    assert "[VER. 9.0.0b30]" in _testo("vmc_master_scheda_manuale_interfaccia.txt")[:1000]
