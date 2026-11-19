"""Prove della 9.0.0b31: countdown della rilevazione del Black-Out e velocità memorizzata
nella scheda ridotta (VMC OFF-Line)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from homeassistant.util import yaml as hay

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"
STATO = "sensor.vmc_master_status_ip_interfaccia"
RIL = "timer.vmc_master_countdown_blackout_rilevazione"
RIP = "timer.vmc_master_countdown_blackout_ripristino"
CAL = "input_boolean.vmc_master_spia_calendario_black_out"
VELOCITA = {
    "0": "Velocità 0",
    "1": "Velocità 1",
    "2": "Velocità 2",
    "3": "Velocità 3",
    "4": "Velocità 4",
    "notturna": "Notturna",
    "iperventilazione": "Iperventilazione",
    "freecooling": "Free Heating/Cooling",
}
SPIE = [f"input_boolean.vmc_master_spia_velocita_{k}" for k in VELOCITA]
OFF = {"condition": "state", "entity": STATO, "state": "OFF-Line"}


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8")


def _righe_ridotta() -> list:
    scheda = hay.load_yaml(str(PKG / "vmc_master_scheda_manuale_interfaccia.txt"))
    ridotta = scheda["cards"][0]
    assert "ferma_off_line" in str(ridotta["card"]["header"])
    return ridotta["card"]["entities"]


def _dopo_ripristino() -> list:
    righe = _righe_ridotta()
    i = next(k for k, r in enumerate(righe) if r.get("row", {}).get("entity") == RIP)
    fine = next(k for k, r in enumerate(righe) if r.get("entity") == "script.vmc_master_upgrade_sensors")
    return righe[i + 1 : fine]


def test_righe_nuove_sotto_il_ripristino() -> None:
    righe = _dopo_ripristino()
    assert len(righe) == 3 + len(VELOCITA) + 1
    assert all(r["type"] == "conditional" for r in righe)
    attivo = {"condition": "state", "entity": RIL, "state": "active"}

    # 1) messaggio e countdown della rilevazione, solo OFF-Line e con il countdown in corso
    assert righe[0]["conditions"] == [OFF, attivo]
    assert righe[0]["row"] == {
        "type": "section",
        "label": "VMC OFF-Line: se non torna entro il countdown viene considerata in Black-Out. Non serve fare nulla.",
    }
    assert righe[1]["conditions"] == [OFF, attivo]
    assert righe[1]["row"] == {"entity": RIL, "name": "Rilevazione Black-Out tra", "icon": "mdi:timer-sand"}

    # 2) Black-Out rilevato: una qualsiasi spia della velocità accesa
    assert righe[2]["conditions"][0] == OFF
    oppure = righe[2]["conditions"][1]
    assert oppure["condition"] == "or"
    assert [c["entity"] for c in oppure["conditions"]] == SPIE
    assert all(c["state"] == "on" for c in oppure["conditions"])
    assert righe[2]["row"]["label"].startswith("Black-Out rilevato: ")

    # 3) velocità memorizzata: una riga per spia, anche con la VMC di nuovo ON-Line (ripristino)
    for riga, (chiave, testo) in zip(righe[3:-1], VELOCITA.items()):
        assert riga["conditions"] == [
            {"condition": "state", "entity": f"input_boolean.vmc_master_spia_velocita_{chiave}", "state": "on"}
        ]
        assert riga["row"] == {"type": "text", "name": "Velocità memorizzata", "text": testo, "icon": "mdi:fan"}

    # 4) Black-Out durante una fascia del Calendario
    assert righe[-1]["conditions"] == [OFF, {"condition": "state", "entity": CAL, "state": "on"}]
    assert righe[-1]["row"]["label"].startswith("Black-Out durante la fascia del Calendario: ")


def test_testi_brevi_e_senza_entita() -> None:
    for riga in _dopo_ripristino():
        etichetta = riga["row"].get("label", "")
        assert not re.search(r"\b(timer|input_boolean|sensor)\.", etichetta)
        assert "master" not in etichetta


def test_countdown_avviato_anche_nella_fascia_del_calendario() -> None:
    """Il testo della prima riga vale in tutti e due i casi: il countdown parte anche in fascia."""
    pacchetto = hay.load_yaml(str(PKG / "vmc_master.yaml"))
    countdown = next(a for a in pacchetto["automation"] if a.get("id") == "vmc_master_countdown_attese_automazione")
    ids = {t["id"] for t in countdown["triggers"]}
    assert "ON|blackout_rilevazione|blackout_rilevazione|Black-Out Velocità 2 rilevato" in ids
    assert "ON|blackout_rilevazione|blackout_rilevazione|Calendario - Black-Out durante una Fascia rilevato" in ids


def test_nota_informazioni() -> None:
    scheda = _testo("vmc_master_scheda_manuale_interfaccia.txt")
    i = scheda.index("<strong>Nota VMC OFF-Line</strong>")
    assert i < scheda.index("<strong>Nota VMC di nuovo ON-Line</strong>")
    nota = re.sub(r"\s+", " ", scheda[i : scheda.index("<br>", i)])
    assert "«Rilevazione Black-Out tra» (32 secondi)" in nota
    assert "«Velocità memorizzata»" in nota
    assert "Fascia del Calendario" in nota


def _commento(entita: str) -> str:
    pacchetto = _testo("vmc_master.yaml")
    dominio, oggetto = entita.split(".", 1)
    if dominio == "sensor":
        return re.search(rf"default_entity_id: {re.escape(entita)} +# (.+)", pacchetto).group(1)
    sezione = pacchetto.index(f"\n{dominio}:")
    return re.compile(rf"\n  {oggetto}: +# (.+)").search(pacchetto, sezione).group(1)


@pytest.mark.parametrize("entita", [STATO, RIL, CAL, *SPIE])
def test_richiami_interfaccia(entita: str) -> None:
    modello = re.compile(re.escape(entita) + r"(?![A-Za-z0-9_])")
    n = len(modello.findall(_testo("vmc_master_scheda_manuale_interfaccia.txt")))
    atteso = f"[INTERFACCIA, {n} RICHIAM{'O' if n == 1 else 'I'}]"
    assert atteso in _commento(entita), (_commento(entita)[:120], atteso)


def test_versione_della_scheda() -> None:
    assert "RELEASE [VER. 9.0.0b31]" in _testo("vmc_master_scheda_manuale_interfaccia.txt")[:2000]
