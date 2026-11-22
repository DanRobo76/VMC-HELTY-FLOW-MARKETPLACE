"""Prove della 9.0.0b34, aggiunta chiesta dal proprietario dopo B1-1: quando la VMC risponde al ping ma la sua
velocita' non si legge, il Calendario smette di ripetere il comando della Fascia dopo il tempo di rilevazione del
Black-Out (B1-1) e accende la Spia Comando non eseguito del Calendario; appena la VMC torna a rispondere la Fascia
riparte (stesso script della Fascia), salvo se nel frattempo la velocita' e' cambiata (per esempio con il
telecomando): il controllo e' nello script, dopo i suoi 5 s, perche' al ritorno della VMC le letture derivate dal
sensore TCP possono non essere ancora aggiornate (visto sul vero Home Assistant del simulatore). La spia si spegne all'avvio di ogni Fascia e a fine Fascia (azzeramento delle spie); dalla b36 resta accesa dopo un
riavvio di Home Assistant (niente initial: false, E1 della verifica dei riavvii) e il comando viene ripetuto a
riallineamento finito, sempre salvo se la velocita' e' cambiata (la decisione B1-4 resta: nessuna Fascia rilanciata
senza un comando in sospeso)."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import pytest
from homeassistant.util import yaml as hay

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"
SPIA = "input_boolean.vmc_master_spia_calendario_comando_non_eseguito"
SPIA_BO = "input_boolean.vmc_master_spia_calendario_black_out"
TCP = "sensor.vmc_master_status_ventola"
IP = "sensor.vmc_master_status_ip_interfaccia"
LETTURA = "sensor.vmc_master_status_ventola_lettura_codice_interpretato"
LETTURA_INTERFACCIA = "sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia"
LETT = f"states.{LETTURA}"
ATTESA = "input_number.vmc_master_attesa_blackout_rilevazione"
FASE = "input_number.vmc_master_fase_riallineamento_al_riavvio"
INTERRUTTORE = "input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario"
FASCE = ("vmc_master_calendario_fascia_1_on", "vmc_master_calendario_fascia_2_on")
LETTURA_PERSA = (f"(is_state('{TCP}', 'unavailable') and (now() - states.{TCP}.last_changed).total_seconds() >= "
                 f"states('{ATTESA}') | int(32))")
GIORNI = ("lunedi", "martedi", "mercoledi", "giovedi", "venerdi", "sabato", "domenica")


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8")


def _pacchetto() -> dict[str, Any]:
    return hay.load_yaml(str(PKG / "vmc_master.yaml"))


def _automazione() -> dict[str, Any]:
    return hay.load_yaml(str(PKG / "vmc_master_automazione.txt"))


def _trigger() -> dict[str, Any]:
    (trigger,) = [t for t in _automazione()["triggers"] if t.get("id") == "calendario_ritorno_comando"]
    return trigger


def _ramo() -> dict[str, Any]:
    rami = [r for b in _automazione()["actions"] if "choose" in b for r in b["choose"]
            if r["conditions"][0].get("id") == "calendario_ritorno_comando"]
    assert len(rami) == 1
    return rami[0]


def _render(hass, modello: str, variabili: dict[str, Any] | None = None) -> str:
    from homeassistant.helpers.template import Template

    return Template(modello, hass).async_render(variabili or {}, parse_result=False).strip()


# ------------------------------------------------------------------------------------------------ la spia
def test_spia_definita_ripristinata_al_riavvio_e_negli_elenchi() -> None:
    spia = _pacchetto()["input_boolean"]["vmc_master_spia_calendario_comando_non_eseguito"]
    assert spia == {"name": "Spia Comando non eseguito all'interno del Calendario", "icon": "mdi:memory"}
    pacchetto = _testo("vmc_master.yaml")
    escluse = pacchetto[pacchetto.index("&vmc_master_entita_escluse_recorder"):]
    assert SPIA in escluse[: escluse.index("\n\n")]
    for script in ("\n  vmc_master_azzera_booleans:", '\n    alias: "VMC Master - Pulisci cronologia Entità"'):
        corpo = pacchetto[pacchetto.index(script):]
        assert SPIA in corpo[: corpo.index("\n  vmc_master_", 10)], script
    scheda = _testo("vmc_master_scheda_manuale_interfaccia.txt")
    elenco = scheda[scheda.index("{%- set elenco = ["):]
    assert f"'{SPIA}'," in elenco[: elenco.index("] -%}")]


def test_fine_fascia_spegne_la_spia() -> None:
    """Lo script di fine Fascia azzera tutte le spie (anche questa) con vmc_master_azzera_booleans."""
    script = _pacchetto()["script"]
    assert script["vmc_master_calendario_fascia_1_o_2_off"]["sequence"][0]["action"] == "script.vmc_master_azzera_booleans"
    spente = [p for p in script["vmc_master_azzera_booleans"]["sequence"]
              if p.get("action") == "input_boolean.turn_off" and SPIA in str(p)]
    assert spente


# ------------------------------------------------------------------------------------------------ script di Fascia
@pytest.mark.parametrize("nome", FASCE)
def test_script_di_fascia_spegne_e_riaccende_la_spia(nome: str) -> None:
    sequenza = _pacchetto()["script"][nome]["sequence"]
    assert sequenza[1]["action"] == "input_boolean.turn_off" and sequenza[1]["target"] == {"entity_id": SPIA}
    ultimo = sequenza[-1]
    (condizione,) = ultimo["if"]
    assert condizione["value_template"] == (
        f"{{{{ {LETTURA_PERSA} and is_state('{IP}', 'ON-Line') and is_state('{SPIA_BO}', 'off') }}}}")
    assert ultimo["then"] == [{"action": "input_boolean.turn_on", "target": {"entity_id": SPIA}}]
    assert "else" not in ultimo
    # controllo del ritorno subito dopo i 5 s e la velocita' prima del comando, prima di qualsiasi comando
    assert sequenza[2]["delay"]["seconds"] == 5 and "variables" in sequenza[3]
    assert sequenza[4] == {
        "alias": sequenza[4]["alias"], "condition": "template",
        "value_template": ("{{ (comando_non_eseguito_dalle | default(0) | float(0)) == 0 or "
                           f"({LETT} is not none and as_timestamp({LETT}.last_changed, 0) <= "
                           "comando_non_eseguito_dalle | float(0)) }}")}
    assert "choose" in sequenza[5]


@pytest.mark.parametrize(
    ("stato_tcp", "secondi_fa", "ip", "bo", "atteso"),
    [
        ("unavailable", 40, "ON-Line", "off", "True"),  # lettura persa da 40 s con il ping OK: comando non eseguito
        ("unavailable", 10, "ON-Line", "off", "False"),  # disturbo breve
        ("00002", 40, "ON-Line", "off", "False"),  # lettura valida (comando confermato)
        ("unavailable", 40, "OFF-Line", "off", "False"),  # Black-Out: lo gestisce la Spia Black-Out del Calendario
        ("unavailable", 40, "ON-Line", "on", "False"),
    ],
)
async def test_condizione_dell_ultimo_passo(hass, stato_tcp, secondi_fa, ip, bo, atteso) -> None:
    hass.states.async_set(ATTESA, "32.0")
    hass.states.async_set(TCP, stato_tcp, timestamp=time.time() - secondi_fa)
    hass.states.async_set(IP, ip)
    hass.states.async_set(SPIA_BO, bo)
    modello = _pacchetto()["script"][FASCE[0]]["sequence"][-1]["if"][0]["value_template"]
    assert _render(hass, modello) == atteso


# ------------------------------------------------------------------------------------------------ trigger
def test_trigger_senza_attesa_e_con_la_copia_in_evento_ancora_valido() -> None:
    trigger = _trigger()
    assert trigger["trigger"] == "template" and "for" not in trigger
    testo = _testo("vmc_master_automazione.txt")
    copia = testo[testo.index("{%- elif trigger.id == 'calendario_ritorno_comando' -%}\n"):]
    copia = copia[copia.index("\n") + 1: copia.index("      {%- elif trigger.id == ")]
    assert " ".join(copia.split()) == " ".join(trigger["value_template"].split())


@pytest.mark.parametrize(
    ("spia", "tcp", "fase", "atteso"),
    [
        ("on", "VMGO,00000", "0.0", "True"),  # la VMC torna a rispondere
        ("on", "unavailable", "0.0", "False"),  # ancora muta
        ("on", "unknown", "0.0", "False"),
        ("off", "VMGO,00000", "0.0", "False"),  # nessun comando della Fascia in sospeso
        ("on", "VMGO,00000", "2.0", "False"),  # riallineamento al riavvio in corso
        ("on", "VMGO,00000", "4.0", "True"),
    ],
)
async def test_condizione_del_trigger(hass, spia, tcp, fase, atteso) -> None:
    for allerta in ("input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia",
                    "input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia"):
        hass.states.async_set(allerta, "off")  # b36 (C1-3): il ritorno aspetta la fine di Congelamento e Δ Temp.
    hass.states.async_set(SPIA, spia)
    hass.states.async_set(TCP, tcp)
    hass.states.async_set(FASE, fase)
    assert _render(hass, _trigger()["value_template"]) == atteso


# ------------------------------------------------------------------------------------------------ ramo
def test_ramo_spegne_la_spia_e_rilancia_lo_script_della_fascia_accesa() -> None:
    passi = _ramo()["sequence"]
    assert passi[0]["variables"] == {"comando_non_eseguito_dalle": (
        f"{{{{ as_timestamp(states.{SPIA}.last_changed, 0) if states.{SPIA} is not none else 0 }}}}")}
    assert passi[1]["action"] == "input_boolean.turn_off" and passi[1]["target"] == {"entity_id": SPIA}
    assert passi[2]["condition"] == "template"
    (scelta,) = passi[3:]
    # b35 (C1-1): la terza opzione ripete la Velocita' 0 di fine Fascia; b36 (C1-5): la quarta la Velocita' 1 dello
    # spegnimento del Calendario con gli Inquinanti
    assert len(scelta["choose"]) == 4
    for n, opzione in zip((1, 2), scelta["choose"]):
        modello = " ".join(opzione["conditions"][0]["value_template"].split())
        assert modello == "{{ " + " or ".join(
            f"states('input_boolean.vmc_master_spia_calendario_{g}_{n}') == 'on'" for g in GIORNI) + " }}"
        # b36 (C1-5): l'interruttore del Calendario serve solo per far ripartire la Fascia
        assert opzione["conditions"][1] == {"alias": "Interruttore del Calendario acceso", "condition": "state",
                                            "entity_id": INTERRUTTORE, "state": "on"}
        (chiamata,) = opzione["sequence"]
        assert chiamata["action"] == f"script.vmc_master_calendario_fascia_{n}_on"
        assert chiamata["data"] == {"comando_non_eseguito_dalle": "{{ comando_non_eseguito_dalle }}"}
    assert "default" not in scelta
    assert "shell_command." not in str(scelta["choose"][:2]) and "shell_command." not in str(passi[:3])


@pytest.mark.parametrize(
    ("interruttore", "ip", "bo", "interfaccia", "atteso"),
    [
        ("on", "ON-Line", "off", "Velocità 0", "True"),
        # b36 (C1-5): con il Calendario spento la Fascia non riparte (condizione nelle opzioni della Fascia), ma la
        # Velocita' 0 (o 1) dello spegnimento del Calendario si ripete
        ("off", "ON-Line", "off", "Velocità 0", "True"),
        ("on", "OFF-Line", "off", "Velocità 0", "False"),
        ("on", "ON-Line", "on", "Velocità 0", "False"),  # Black-Out in Fascia: riparte con la Spia Black-Out
        ("on", "ON-Line", "off", "Non disponibile", "False"),
    ],
)
async def test_condizioni_del_ramo(hass, interruttore, ip, bo, interfaccia, atteso) -> None:
    hass.states.async_set(INTERRUTTORE, interruttore)
    hass.states.async_set(IP, ip)
    hass.states.async_set(SPIA_BO, bo)
    hass.states.async_set(LETTURA_INTERFACCIA, interfaccia)
    assert _render(hass, _ramo()["sequence"][2]["value_template"]) == atteso


@pytest.mark.parametrize(
    ("lettura_cambiata_fa", "atteso"),  # controllo nello script della Fascia (dopo i 5 s)
    [
        (600, "True"),  # velocita' invariata da prima del comando non eseguito: la Fascia riparte
        (5, "False"),  # cambiata dopo (per esempio con il telecomando): si rispetta
    ],
)
async def test_velocita_cambiata_nel_frattempo(hass, lettura_cambiata_fa, atteso) -> None:
    ora = time.time()
    hass.states.async_set(SPIA, "on", timestamp=ora - 60)
    hass.states.async_set(LETTURA, "Velocità 0", timestamp=ora - lettura_cambiata_fa)
    dalle = _render(hass, _ramo()["sequence"][0]["variables"]["comando_non_eseguito_dalle"])
    assert abs(float(dalle) - (ora - 60)) < 1
    controllo = _pacchetto()["script"][FASCE[1]]["sequence"][4]["value_template"]
    assert _render(hass, controllo, {"comando_non_eseguito_dalle": float(dalle)}) == atteso
    assert _render(hass, controllo, {"comando_non_eseguito_dalle": dalle}) == atteso  # anche come testo


async def test_chiamate_normali_e_senza_spia(hass) -> None:
    """Le altre 18 chiamate degli script di Fascia non passano la variabile: il controllo e' sempre vero."""
    controllo = _pacchetto()["script"][FASCE[0]]["sequence"][4]["value_template"]
    hass.states.async_set(LETTURA, "Velocità 2")
    assert _render(hass, controllo) == "True"
    assert _render(hass, _ramo()["sequence"][0]["variables"]["comando_non_eseguito_dalle"]) == "0"
    assert _render(hass, controllo, {"comando_non_eseguito_dalle": 0}) == "True"


# ------------------------------------------------------------------------------------------------ testi
def test_descrizioni_e_scheda() -> None:
    script = _pacchetto()["script"]
    for nome in FASCE:
        testo = " ".join(script[nome]["description"].split())
        assert "e quando la VMC torna a rispondere dopo un comando non eseguito" in testo
        assert ("si accende la Spia Comando non eseguito del Calendario e, appena la VMC torna a rispondere, la Fascia "
                "riparte, salvo se nel frattempo la velocità è cambiata, per esempio con il telecomando") in testo
        assert "(anche la Spia Comando non eseguito si spegne)" in testo
        for vietata in ("vmc_master", "master", "input_", "sensor.", "999.999"):
            assert vietata not in testo
    # b35 (C5-1): la causa vera (la velocita' non si legge) e il caso della fine della Fascia (C1-1)
    # b36 (C1-3, C1-5): l'attesa della fine di Congelamento/Δ e il comando dello spegnimento del Calendario
    frase = ("se invece la VMC risponde al ping ma la sua velocità non si legge (porta 5001), dopo 32 Secondi la Fascia "
             "smette di ripetere il comando e, appena la velocità torna leggibile, la Fascia riparte, salvo se nel "
             "frattempo la Velocità è cambiata (per esempio con il Telecomando); lo stesso vale per la Velocità 0 di fine "
             "Fascia e per il comando dato spegnendo l'interruttore del Calendario durante una Fascia (Velocità 0, o "
             "Velocità 1 con Inquinanti): appena la velocità torna leggibile il comando viene ripetuto, anche con "
             "l'interruttore del Calendario spento, salvo se nel frattempo la Velocità è cambiata; "
             "lo stesso vale per il comando di un'allerta (o del suo ripristino) dato durante una Fascia: dopo 32 "
             "Secondi la ripetizione si ferma e, appena la velocità torna leggibile, il comando viene ripetuto, "
             "salvo se nel frattempo la Velocità è cambiata (se anche il comando del Calendario non è stato "
             "eseguito, prima riparte la Fascia); "
             "con un'allerta "
             "Congelamento o Δ Temp. in corso il comando del Calendario aspetta la fine dell'allerta: a fine allerta, "
             "appena la velocità è leggibile, la Fascia riparte con la sua Velocità (o si ripete la Velocità 0, o 1, in "
             "sospeso) al posto della Velocità memorizzata dall'allerta, salvo se si sceglie un'altra Velocità dopo la "
             "fine dell'allerta; se invece la corrente manca proprio mentre la Fascia finisce o mentre si spegne "
             "l'interruttore del Calendario, al ritorno della corrente la VMC si arresta dopo 32 Secondi (o va a Velocità "
             "1, se l'interruttore è stato spento con Inquinanti presenti);")
    assert frase in " ".join(_automazione()["description"].split())
    assert frase + "<br>" in " ".join(_testo("vmc_master_scheda_manuale_interfaccia.txt").split())
