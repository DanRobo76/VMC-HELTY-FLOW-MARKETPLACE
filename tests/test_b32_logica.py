"""Prove della 9.0.0b32: correzioni della logica trovate dalla verifica profonda 1:1 e confermate dalle prove
dinamiche (simulatore con Home Assistant reale)."""

from __future__ import annotations

import re
from pathlib import Path

from homeassistant.util import yaml as hay

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"


def _automazione() -> str:
    return (PKG / "vmc_master_automazione.txt").read_text(encoding="utf-8")


def test_automazione_valida_e_versione() -> None:
    dati = hay.load_yaml(str(PKG / "vmc_master_automazione.txt"))
    assert dati
    versione = re.search(r"AUTOMAZIONE VMC HELTY FLOW PLUS RELEASE \[VER\. 9\.0\.0b(\d+)\]", _automazione()[:1000])
    assert versione and int(versione.group(1)) >= 32


def test_delta_temp_non_cancella_il_ritorno_a_velocita_0_degli_inquinanti() -> None:
    """A1-2: Inquinanti partiti da Velocita' 0 e Δ Temp. scattato prima della memoria Inquinanti (8 s a Velocita' 1):
    a fine Δ la regola 03-11-2026 non deve trattare la Velocita' 1 come scelta dell'utente, cosi' a fine Inquinanti
    la VMC torna a Velocita' 0 (Foglio A28)."""
    testo = _automazione()
    i = testo.index("durante Δ Temp. -> diventa la memoria degli Inquinanti (regola 03-11-2026; non se la Velocità 1")
    condizione = testo[i : testo.index("then:", i)]
    assert "not is_state('input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0', 'on')" in condizione
    assert "not is_state('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr', 'on')" in condizione
    # le altre 13 regole (Congelamento e Δ con memorie 0, 2, 3, 4, Notturna, Iperventilazione) restano come prima
    assert testo.count("(regola 03-11-2026)") == 13


def test_fine_umidita_con_inquinanti_anche_con_avvio_free() -> None:
    """A3-1: con [Velocita' Umidita' di Avvio] = «Free Cool./Heat.» la lettura della VMC e' «Free Cooling» (o
    «Velocita' 1» con le allerte Free), mai uguale all'opzione: a fine Umidita' con Inquinanti la VMC deve scendere a
    Velocita' 1 e a fine Inquinanti a Velocita' 0 (Foglio A21, NOTE 2). Trigger, condizione e 2 copie del countdown."""
    nuova = ("(states('input_select.vmc_master_speed_umidita') == 'Free Cool./Heat.' and "
             "states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') in ['Free Cooling', 'Velocità 1'])")
    assert _automazione().count(nuova) == 2
    assert (PKG / "vmc_master.yaml").read_text(encoding="utf-8").count(nuova) == 2
    opzioni = hay.load_yaml(str(PKG / "vmc_master.yaml"))["input_select"]["vmc_master_speed_umidita"]["options"]
    assert "Free Cool./Heat." in opzioni


def test_velocita_0_scelta_durante_l_umidita_resta() -> None:
    """A3-3: con la Velocita' 0 scelta dall'utente durante l'Umidita' (spia «mantenuta» accesa), un ritorno a 0 dopo
    gli Inquinanti o dopo un tocco breve non rimanda la velocita' di avvio dell'Umidita'."""
    testo = _automazione()
    i = testo.index("rimanda la velocità di avvio dell'opzione 175, la memoria resta (correzione U3)")
    condizione = testo[i : testo.index("then:", i)]
    assert "is_state('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0', 'off')" in condizione


def test_la_fascia_spegne_la_memoria_del_black_out() -> None:
    """A4-1: Black-Out rilevato fuori fascia e corrente tornata dentro una fascia: la fascia comanda la VMC e spegne le
    8 spie velocita' del Black-Out, che altrimenti restavano accese per tutta la fascia (bloccando le allerte e
    nascondendo la scheda completa)."""
    script = hay.load_yaml(str(PKG / "vmc_master.yaml"))["script"]
    spie = {f"input_boolean.vmc_master_spia_velocita_{v}" for v in
            ("0", "1", "2", "3", "4", "notturna", "iperventilazione", "freecooling")}
    for nome in ("vmc_master_calendario_fascia_1_on", "vmc_master_calendario_fascia_2_on"):
        primo = script[nome]["sequence"][0]
        assert primo["action"] == "input_boolean.turn_off", nome
        assert set(primo["target"]["entity_id"]) == spie, nome
        assert "delay" in script[nome]["sequence"][1], nome


def test_scelta_durante_la_sospensione_free_con_umidita_annulla_la_ripresa() -> None:
    """A3-2: con la Free sospesa e un'allerta Umidita' in corso (VMC a Velocita' 1, Nota 3) una velocita' scelta
    dall'utente e mantenuta 20 secondi annulla la ripresa in Free (Foglio A29), come senza Umidita'. Trigger,
    condizione e 2 copie del Countdown Attese."""
    nuova = ("and (states('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia') == 'off' or "
             "states('sensor.vmc_master_status_ventola_lettura_codice_interpretato') != 'Velocità 1')")
    assert _automazione().count(nuova) == 2
    assert (PKG / "vmc_master.yaml").read_text(encoding="utf-8").count(nuova) == 2


def test_velocita_scelta_negli_ultimi_secondi_del_pdr_resta() -> None:
    """A2-1: una velocita' scelta durante l'allerta PdR e non ancora memorizzata (allerta finita prima dei 16 s, 12 s
    con Inquinanti) resta a fine allerta (Foglio F6): 8 rami senza Inquinanti (memoria 0, 1, 2, 3, 4, Notturna,
    Iperventilazione, Free) e 5 con Inquinanti (2, 3, 4, Notturna, Iperventilazione; il ramo 1 non invia comandi)."""
    testo = _automazione()
    assert testo.count("- stop: Velocità scelta dall'utente durante l'allerta PdR mantenuta") == 13
    rami = {}
    righe = testo.split("\n")
    for i, riga in enumerate(righe):
        if "- stop: Velocità scelta dall'utente durante l'allerta PdR mantenuta" in riga:
            j = max(k for k in range(i) if "vel_prima_del_comando not in [" in righe[k])
            escluse = righe[j].split("not in [", 1)[1].split("]", 1)[0]
            k = max(k for k in range(j) if " Rip. " in righe[k] and ("id: " in righe[k] or righe[k].strip().startswith("- Rip.")))
            rami[righe[k].split("Rip. ", 1)[1].strip()] = escluse
    assert len(rami) == 13
    assert rami["Vel. 0 No PdR -> Spia PdR Velocità 0 OFF"].startswith("'Velocità 0', 'Non disponibile'")
    assert rami["Vel. 2 No PdR"].startswith("'Velocità 0', 'Velocità 2', 'Non disponibile'")
    assert rami["Free Cool./Heat. No PdR"].startswith("'Velocità 0', 'Free Cooling', 'Non disponibile'")
    assert rami["Vel. 3 No PdR  se Spia Inquinanti ON"].startswith("'Velocità 0', 'Velocità 1', 'Velocità 3', 'Non")


def test_ripristino_free_dopo_black_out_manda_sempre_un_comando() -> None:
    """A4-3: «Black-Out Off Free Cool./Heat.» con Inquinanti appena rilevati (memoria della Velocita' 1 degli
    Inquinanti ancora spenta) e Free programmato non mandava nessun comando: ora il default manda la Velocita' 1 con
    gli Inquinanti in corso, altrimenti Free Cool./Heat. (Foglio A23). Dalla b34 (B1-2) il comando sta nel ciclo
    di conferma (secondo passo, dopo la memoria della velocita' prima del comando)."""
    dati = hay.load_yaml(str(PKG / "vmc_master_automazione.txt"))
    rami = [r for blocco in dati["actions"] if "choose" in blocco for r in blocco["choose"]]
    ramo = next(r for r in rami if r["conditions"][0].get("id") == "Black-Out Off Free Cool./Heat.")
    scelta = next(passo for passo in ramo["sequence"] if "choose" in passo)
    assert len(scelta["choose"]) == 4
    interno = scelta["default"][0]
    assert interno["choose"][0]["conditions"][0]["entity_id"] == "input_boolean.vmc_master_spia_co2_o_voc"
    assert interno["choose"][0]["sequence"][1]["repeat"]["sequence"][0]["action"] == "shell_command.vmc_master_velocita_1"
    assert interno["default"][1]["repeat"]["sequence"][0]["action"] == "shell_command.vmc_master_freecooling"
