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
    "freecooling": "Free Cool./Heat.",
}
SPIE = [f"input_boolean.vmc_master_spia_velocita_{k}" for k in VELOCITA]
OFF = {"condition": "state", "entity": STATO, "state": "OFF-Line"}


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8")


def _righe_ridotta() -> list:
    scheda = hay.load_yaml(str(PKG / "vmc_master_scheda_manuale_interfaccia.txt"))
    # la scheda ridotta e' quella con l'intestazione «ferma_off_line» (dalla b31 la prima carta
    # e' il pannello «Riattivazione delle Allerte»)
    ridotte = [c for c in scheda["cards"] if "ferma_off_line" in str(c.get("card", {}).get("header"))]
    assert len(ridotte) == 1
    return ridotte[0]["card"]["entities"]


def _dopo_ripristino() -> list:
    righe = _righe_ridotta()
    i = next(k for k, r in enumerate(righe) if r.get("row", {}).get("entity") == RIP)
    # subito sotto il countdown c'e' «Ripristino Velocità: conferma in corso» (prove in test_b31_ridotta)
    assert righe[i + 1]["row"].get("text") == "conferma in corso"
    i += 1
    fine = next(k for k, r in enumerate(righe) if r.get("entity") == "script.vmc_master_upgrade_sensors")
    return righe[i + 1 : fine]


def test_righe_nuove_sotto_il_ripristino() -> None:
    righe = _dopo_ripristino()
    # b39: + comando di un'allerta non eseguito in Fascia + comando del Calendario in attesa della fine di Congelamento/Δ
    assert len(righe) == 3 + len(VELOCITA) + 1 + 1 + 1 + 1
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
    assert len(righe[3:-4]) == len(VELOCITA)
    for riga, (chiave, testo) in zip(righe[3:-4], VELOCITA.items()):
        assert riga["conditions"] == [
            {"condition": "state", "entity": f"input_boolean.vmc_master_spia_velocita_{chiave}", "state": "on"}
        ]
        assert riga["row"] == {"type": "text", "name": "Velocità salvata", "text": testo, "icon": "mdi:fan"}

    # 4) Black-Out durante una fascia del Calendario
    assert righe[-4]["conditions"] == [OFF, {"condition": "state", "entity": CAL, "state": "on"}]
    assert righe[-4]["row"]["label"].startswith("Black-Out durante la fascia del Calendario: ")
    # b39: con Congelamento/Δ in corso la Fascia riparte alla fine dell'allerta
    assert righe[-4]["row"]["label"].endswith("(se nel frattempo la fascia è finita, si arresta; con un'allerta "
                                              "Congelamento o Δ Temp. in corso riparte alla fine dell'allerta). Non "
                                              "serve fare nulla.")
    on_line = {"condition": "state", "entity": "sensor.vmc_master_status_ip_interfaccia", "state": "ON-Line"}
    non_letta = {"condition": "or", "conditions": [
        {"condition": "state", "entity": "sensor.vmc_master_status_ventola", "state": "unavailable"},
        {"condition": "state", "entity": "sensor.vmc_master_status_ventola", "state": "unknown"}]}
    spia_cal = {"condition": "state", "entity": "input_boolean.vmc_master_spia_calendario_comando_non_eseguito",
                "state": "on"}

    # 5) b34: comando della fascia non eseguito (VMC ON-Line ma velocità illeggibile); b35 (C5-1, C1-1): la causa vera e
    # anche la Velocità 0 di fine fascia
    # b39: solo con la velocità davvero non leggibile (con la velocità leggibile e Congelamento/Δ c'è la riga sotto)
    assert righe[-3]["conditions"] == [on_line, spia_cal, non_letta]
    assert righe[-3]["row"]["label"].startswith("La VMC risponde in rete ma la sua velocità non si legge: ")
    assert "Velocità 0 di fine fascia" in righe[-3]["row"]["label"]
    # b36 (C1-3): con Congelamento/Δ in corso il comando riparte alla fine dell'allerta
    assert righe[-3]["row"]["label"].endswith("salvo se nel frattempo la velocità è cambiata; con un'allerta Congelamento "
                                              "o Δ Temp. in corso il comando riparte alla fine dell'allerta, al posto "
                                              "della velocità memorizzata dall'allerta. Non serve fare nulla.")
    # b39: velocità leggibile, comando del Calendario in attesa della fine di Congelamento/Δ (anche dopo un Black-Out in
    # Fascia con l'allerta in corso)
    assert righe[-2]["conditions"] == [
        on_line, spia_cal,
        {"condition": "state", "entity": "sensor.vmc_master_status_ventola", "state_not": "unavailable"},
        {"condition": "state", "entity": "sensor.vmc_master_status_ventola", "state_not": "unknown"},
        {"condition": "or", "conditions": [
            {"condition": "state", "entity": "input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia",
             "state": "on"},
            {"condition": "state", "entity": "input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia",
             "state": "on"}]},
    ]
    assert righe[-2]["row"]["label"] == (
        "Allerta Congelamento o Δ Temp. in corso: il comando del Calendario (velocità della fascia, Velocità 0 di fine "
        "fascia o comando dato spegnendo l'interruttore del Calendario durante la fascia) riparte alla fine "
        "dell'allerta, al posto della velocità memorizzata dall'allerta. Non serve fare nulla.")

    # 6) b39: comando di un'allerta (o del suo ripristino) non eseguito durante una fascia, finche' non viene ripetuto
    testo = "input_text.vmc_master_comando_non_eseguito"
    assert righe[-1]["conditions"] == [
        {"condition": "state", "entity": "sensor.vmc_master_status_ip_interfaccia", "state": "ON-Line"},
        {"condition": "state", "entity": testo, "state_not": ""},
        {"condition": "state", "entity": testo, "state_not": "unknown"},
        {"condition": "state", "entity": testo, "state_not": "unavailable"},
        non_letta,
    ]
    assert righe[-1]["row"]["label"] == (
        "La VMC risponde in rete ma la sua velocità non si legge: il comando di un'allerta (o del suo ripristino) dato "
        "durante la fascia del Calendario non è confermato. Appena la velocità torna leggibile il comando riparte, salvo "
        "se nel frattempo la velocità è cambiata. Non serve fare nulla.")


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
    assert "«Velocità salvata»" in nota
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
    """La scheda e' cambiata nella b31: la sua VER. e' almeno 9.0.0b31."""
    versione = re.search(r"RELEASE \[VER\. 9\.0\.0b(\d+)\]", _testo("vmc_master_scheda_manuale_interfaccia.txt")[:2000])
    assert versione and int(versione.group(1)) >= 31


def test_ip_salvato_nascosto_con_il_campo_vuoto() -> None:
    """Dopo il riavvio il sensore di verifica ripristina per un attimo il valore di prima: con il campo
    vuoto (initial "") la riga «IP salvato…» non deve ricomparire."""
    righe = _testo("vmc_master_scheda_manuale_interfaccia.txt").splitlines()
    etichette = [k for k, r in enumerate(righe) if r.strip().startswith("label: IP salvato.")]
    assert len(etichette) == 3
    for k in etichette:
        inizio = max(j for j in range(k) if righe[j].strip() == "conditions:")
        blocco = [r.strip() for r in righe[inizio:k]]
        i = blocco.index("entity: input_text.vmc_master_ip_insert")
        assert blocco[i - 1] == "- condition: state" and blocco[i + 1] == "state_not: ''"
