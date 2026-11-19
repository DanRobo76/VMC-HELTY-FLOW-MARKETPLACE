"""Prove della 9.0.0b31 (scheda ridotta, VMC di nuovo ON-Line): il countdown dei 60 s dopo
l'avvio di Home Assistant compare solo nel pannello «Riattivazione delle Allerte»; nel
riquadro della VMC «Ripristino Velocità» dice «dopo il 1° gruppo» e, finito il countdown
del ripristino, «conferma della VMC in corso» (niente momenti senza countdown)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from homeassistant.util import yaml as hay

from custom_components.vmc_master.trasforma import per_vmc

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"
SCHEDA = "vmc_master_scheda_manuale_interfaccia.txt"
STATO = "sensor.vmc_master_status_ip_interfaccia"
FASE = "input_number.vmc_master_fase_riallineamento_al_riavvio"
T60 = "timer.vmc_master_countdown_avvio_home_assistant"
RIP = "timer.vmc_master_countdown_blackout_ripristino"
RIL = "timer.vmc_master_countdown_blackout_rilevazione"
SPIA = "input_boolean.vmc_master_spia_velocita_2"
ON = {"condition": "state", "entity": STATO, "state": "ON-Line"}
SEZIONE = (
    "VMC di nuovo ON-Line, ripristino della velocità in uso prima del Black-Out in corso... "
    "Non serve fare nulla, attendi la fine del countdown."
)
DOPO = "Ripristino Velocità | dopo il 1° gruppo"
CONFERMA = "Ripristino Velocità | conferma della VMC in corso"
COUNTDOWN = f"Ripristino Velocità tra | countdown {RIP}"
MEMORIZZATA = "Velocità memorizzata | Velocità 2"
NOMI_VMC = ("sala", "camera", "cucina")


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8")


def _righe_ridotta() -> list:
    scheda = hay.load_yaml(str(PKG / SCHEDA))
    ridotta = scheda["cards"][0]
    assert "ferma_off_line" in str(ridotta["card"]["header"])
    righe = ridotta["card"]["entities"]
    fine = next(k for k, r in enumerate(righe) if r.get("entity") == "script.vmc_master_upgrade_sensors")
    return righe[:fine]


def _vera(c: dict, stati: dict) -> bool:
    if c["condition"] == "or":
        return any(_vera(x, stati) for x in c["conditions"])
    if c["condition"] == "and":
        return all(_vera(x, stati) for x in c["conditions"])
    assert c["condition"] == "state"
    valore = stati.get(c["entity"])
    if "state_not" in c:
        esclusi = c["state_not"] if isinstance(c["state_not"], list) else [c["state_not"]]
        return valore not in esclusi
    attesi = c["state"] if isinstance(c["state"], list) else [c["state"]]
    return valore in attesi


def _visibili(stati: dict) -> list[str]:
    """Righe mostrate dalla scheda ridotta con gli stati dati (simula le conditional)."""
    out = []
    for r in _righe_ridotta():
        if r.get("type") == "conditional":
            if not all(_vera(c, stati) for c in r["conditions"]):
                continue
            r = r["row"]
        if r.get("type") == "section":
            out.append(r["label"])
        elif r.get("type") == "text":
            out.append(f"{r['name']} | {r['text']}")
        else:
            out.append(f"{r['name']} | {'countdown ' + r['entity'] if stati.get(r['entity']) == 'active' else 'Inattivo'}")
    return out


# ------------------------------------------------------------------ righe
def test_ordine_delle_righe() -> None:
    righe = _righe_ridotta()
    assert righe[0]["row"]["label"] == SEZIONE
    assert righe[1]["row"]["text"] == "dopo il 1° gruppo"
    assert righe[2]["row"]["entity"] == RIP
    assert righe[3]["row"]["text"] == "conferma della VMC in corso"
    assert righe[4]["row"]["label"].startswith("VMC OFF-Line: ")


def test_riga_dopo_il_primo_gruppo() -> None:
    riga = _righe_ridotta()[1]
    assert riga["type"] == "conditional"
    assert riga["conditions"] == [{"condition": "state", "entity": FASE, "state": "1.0"}, ON]
    assert riga["row"] == {
        "type": "text",
        "name": "Ripristino Velocità",
        "text": "dopo il 1° gruppo",
        "icon": "mdi:pause-circle-outline",
    }


def test_riga_conferma_della_vmc() -> None:
    riga = _righe_ridotta()[3]
    assert riga["type"] == "conditional"
    assert riga["conditions"] == [
        ON,
        {"condition": "state", "entity": FASE, "state_not": "1.0"},
        {"condition": "state", "entity": RIP, "state": "idle"},
    ]
    assert riga["row"] == {
        "type": "text",
        "name": "Ripristino Velocità",
        "text": "conferma della VMC in corso",
        "icon": "mdi:progress-clock",
    }


def test_countdown_dei_60_s_solo_nel_pannello() -> None:
    assert T60 not in str(_righe_ridotta())
    scheda = _testo(SCHEDA)
    assert 'name: "Avvio di Home Assistant"' not in scheda
    assert "«Avvio di Home Assistant»" not in scheda
    assert "Avvio di Home Assistant»" not in _testo("vmc_master.yaml")


# --------------------------------------------------------- ripristino passo per passo
BASE = {STATO: "ON-Line", SPIA: "on", RIL: "idle"}


@pytest.mark.parametrize(
    ("fase", "t60", "rip", "attese"),
    [
        # primi 60 s dopo l'avvio di Home Assistant: il ripristino aspetta il 1° gruppo
        ("1.0", "active", "idle", [SEZIONE, DOPO, MEMORIZZATA]),
        # timer dei 60 s finito, fase non ancora cambiata
        ("1.0", "idle", "idle", [SEZIONE, DOPO, MEMORIZZATA]),
        # fase 2: il ripristino parte (1 s prima che il countdown sia attivo)
        ("2.0", "idle", "idle", [SEZIONE, CONFERMA, MEMORIZZATA]),
        ("2.0", "idle", "active", [SEZIONE, COUNTDOWN, MEMORIZZATA]),
        # countdown finito: la VMC deve confermare la velocità
        ("2.0", "idle", "idle", [SEZIONE, CONFERMA, MEMORIZZATA]),
        ("3.0", "idle", "idle", [SEZIONE, CONFERMA, MEMORIZZATA]),
        ("4.0", "idle", "idle", [SEZIONE, CONFERMA, MEMORIZZATA]),
        # VMC di nuovo ON-Line senza riavvio di Home Assistant
        ("0.0", "idle", "active", [SEZIONE, COUNTDOWN, MEMORIZZATA]),
        ("0.0", "idle", "idle", [SEZIONE, CONFERMA, MEMORIZZATA]),
    ],
)
def test_ripristino_sempre_con_una_riga(fase: str, t60: str, rip: str, attese: list[str]) -> None:
    assert _visibili({**BASE, FASE: fase, T60: t60, RIP: rip}) == attese


@pytest.mark.parametrize("fase", ["0.0", "1.0", "2.0", "3.0", "4.0"])
def test_nessuna_riga_del_ripristino_off_line(fase: str) -> None:
    visibili = _visibili({**BASE, STATO: "OFF-Line", FASE: fase, T60: "active", RIP: "idle"})
    assert not [v for v in visibili if v.startswith("Ripristino Velocità")]
    assert MEMORIZZATA in visibili


def test_righe_per_le_altre_vmc() -> None:
    scheda = per_vmc(_testo(SCHEDA), "prova", "192.168.1.250")
    assert "timer.vmc_master_" not in scheda
    assert scheda.count(FASE.replace("master", "prova")) == _testo(SCHEDA).count(FASE)


# ------------------------------------------------------------------ testi
def _nota(scheda: str, titolo: str) -> str:
    i = scheda.index(titolo)
    return re.sub(r"\s+", " ", scheda[i : scheda.index("<br>", i)])


def test_nota_vmc_di_nuovo_on_line() -> None:
    nota = _nota(_testo(SCHEDA), "<strong>Nota VMC di nuovo ON-Line</strong>")
    assert "«Velocità memorizzata»" in nota
    assert "«Ripristino Velocità tra» (32 secondi)" in nota
    assert "«Ripristino Velocità» indica «dopo il 1° gruppo», fino alla riattivazione del 1° gruppo di allerte" in nota
    assert "(vedere la Nota Avvio di Home Assistant)" in nota
    assert "per pochi secondi compare «conferma della VMC in corso», poi la scheda completa." in nota
    assert "60 secondi" not in nota
    assert not any(re.search(rf"\b{n}\b", nota, re.IGNORECASE) for n in NOMI_VMC)


def test_dopo_il_collegamento() -> None:
    scheda = re.sub(r"\s+", " ", _testo(SCHEDA))
    i = scheda.index("<b>Dopo il collegamento.</b>")
    paragrafo = scheda[i : scheda.index("<br>", i)]
    assert "«Ripristino Velocità: dopo il 1° gruppo»" in paragrafo
    assert "«Ripristino Velocità tra» (32 secondi)" in paragrafo
    assert "per pochi secondi «conferma della VMC in corso»" in paragrafo
    assert "60 secondi" not in paragrafo
    assert not any(re.search(rf"\b{n}\b", paragrafo, re.IGNORECASE) for n in NOMI_VMC)


def test_descrizione_del_riallineamento() -> None:
    pacchetto = hay.load_yaml(str(PKG / "vmc_master.yaml"))
    automazione = next(a for a in pacchetto["automation"] if a.get("id") == "vmc_master_riallineamento_allerte_al_riavvio")
    descrizione = re.sub(r"\s+", " ", automazione["description"]).strip()
    assert descrizione.endswith(
        "Dopo un Black-Out il riquadro della VMC mostra «Ripristino Velocità: dopo il 1° gruppo» finché il 1° gruppo "
        "non si riattiva: solo allora parte il ripristino della velocità."
    )
    assert "Avvio di Home Assistant" not in descrizione
    assert not re.search(r"\b(timer|input_number|input_boolean|sensor|automation|script)\.", descrizione)
    assert "vmc_master_clona_" not in descrizione
    assert not re.search(r"\b\d{1,3}(\.\d{1,3}){3}\b", descrizione)
    assert "master" not in descrizione


def test_commento_del_timer_dei_60_s() -> None:
    commento = re.search(r"\n  vmc_master_countdown_avvio_home_assistant: +# (.+)", _testo("vmc_master.yaml")).group(1)
    assert "E' ANCHE IL COUNTDOWN" not in commento
    assert "E' MOSTRATO SOLO COME COUNTDOWN DEL 1° GRUPPO DI ALLERTE" in commento


@pytest.mark.parametrize("nome", [SCHEDA, "vmc_master.yaml"])
def test_fine_riga_crlf(nome: str) -> None:
    dati = (PKG / nome).read_bytes()
    assert dati.count(b"\n") == dati.count(b"\r\n")
