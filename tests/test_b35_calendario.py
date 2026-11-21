"""Prove della 9.0.0b35, fetta CALENDARIO (rilievi C1-1, C1-4 e C5-1 dell'audit 1:1 della b34).

C1-1 a: alla fine della Fascia il ciclo della Velocita' 0 esce per la lettura persa (TCP assente da 32 s) prima che il
Black-Out venga rilevato (il ping va OFF-Line dopo il TCP e il sensore Black-Out aspetta altri 32 s): la memoria
Velocita' 0 non si accendeva e al ritorno della corrente «Black-Out a Velocita' X» ripristinava la velocita' della
Fascia finita. Ora la memoria si accende anche con la VMC OFF-Line e la lettura persa.
C1-1 b: con la VMC ON-Line ma la velocita' illeggibile (porta 5001 muta) nessuno rimandava la Velocita' 0: ora i 14 rami
«Off» accendono la Spia Comando non eseguito del Calendario (come lo script della Fascia all'inizio) e il ramo del
ritorno della VMC, a Fascia finita, ripete la Velocita' 0 con lo stesso ciclo dei rami «Off», solo se la velocita' non
e' cambiata da quando la spia si e' accesa e senza Congelamento/Δ Temp. in corso. Nessun tempo nuovo.
C1-4: «Calendario in transizione» (fine Congelamento e fine Δ Temp.) vede anche una fascia di un altro giorno ancora
accesa (finita prima della mezzanotte durante l'allerta).
C5-1: i testi dicono la causa vera (velocita' che non si legge, non «non esegue i comandi») e il nuovo caso della fine
della Fascia.

Le prove dinamiche eseguono i passi veri dell'automazione con un piccolo esecutore (condizioni rese da Home Assistant,
spie scritte negli stati, cicli registrati con gli stati all'uscita)."""

from __future__ import annotations

import re
import time
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest
from homeassistant.util import dt as dt_util
from homeassistant.util import yaml as hay

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"
TCP = "sensor.vmc_master_status_ventola"
IP = "sensor.vmc_master_status_ip_interfaccia"
LETTURA = "sensor.vmc_master_status_ventola_lettura_codice_interpretato"
LETTURA_INTERFACCIA = "sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia"
BO = "binary_sensor.vmc_master_black_out_rilevato"
ATTESA = "input_number.vmc_master_attesa_blackout_rilevazione"
FASE = "input_number.vmc_master_fase_riallineamento_al_riavvio"
SPIA_CNE = "input_boolean.vmc_master_spia_calendario_comando_non_eseguito"
SPIA_BO = "input_boolean.vmc_master_spia_calendario_black_out"
SPIA_V0 = "input_boolean.vmc_master_spia_velocita_0"
INTERRUTTORE = "input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario"
GELO = "input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia"
DELTA = "input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia"
GIORNI = ("lunedi", "martedi", "mercoledi", "giovedi", "venerdi", "sabato", "domenica")
SPIE_VELOCITA = [f"input_boolean.vmc_master_spia_velocita_{v}"
                 for v in ("1", "2", "3", "4", "notturna", "iperventilazione", "freecooling")]
LETTURA_PERSA = (f"(is_state('{TCP}', 'unavailable') and (now() - states.{TCP}.last_changed).total_seconds() >= "
                 f"states('{ATTESA}') | int(32))")
BLACK_OUT = f"is_state('{BO}', 'on')"
MEMORIA = (f"{{{{ ({BLACK_OUT} or (is_state('{IP}', 'OFF-Line') and {LETTURA_PERSA})) "
           f"and states('{LETTURA}') != 'Velocità 0' }}}}")
SPIA = (f"{{{{ {LETTURA_PERSA} and is_state('{IP}', 'ON-Line') and not {BLACK_OUT} "
        f"and states('{LETTURA}') != 'Velocità 0' }}}}")


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8")


def _automazione() -> dict[str, Any]:
    return hay.load_yaml(str(PKG / "vmc_master_automazione.txt"))


def _pacchetto() -> dict[str, Any]:
    return hay.load_yaml(str(PKG / "vmc_master.yaml"))


def _rami(dati: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Rami dei choose di primo livello, per id del trigger (anche gli id in elenco)."""
    rami: dict[str, dict[str, Any]] = {}
    for blocco in dati["actions"]:
        for ramo in blocco.get("choose", []):
            ident = ramo["conditions"][0].get("id")
            for nome in [ident] if isinstance(ident, str) else ident or []:
                rami[nome] = ramo
    return rami


def _rami_off(dati: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rami = {i: r for i, r in _rami(dati).items() if i.endswith(" Off") and i[:2] in ("1°", "2°")}
    assert len(rami) == 14
    return rami


def _render(hass, modello: str, variabili: dict[str, Any] | None = None) -> str:
    from homeassistant.helpers.template import Template

    return Template(modello, hass).async_render(variabili or {}, parse_result=False).strip()


# ------------------------------------------------------------------------------------------------ piccolo esecutore
def _vera(hass, condizione: dict[str, Any], variabili: dict[str, Any]) -> bool:
    tipo = condizione["condition"]
    if tipo == "template":
        reso = _render(hass, condizione["value_template"], variabili)
        assert reso in ("True", "False"), reso
        return reso == "True"
    if tipo == "state":
        stato = hass.states.get(condizione["entity_id"])
        return stato is not None and stato.state == condizione["state"]
    if tipo == "and":
        return all(_vera(hass, c, variabili) for c in condizione["conditions"])
    assert tipo == "or", tipo
    return any(_vera(hass, c, variabili) for c in condizione["conditions"])


def _esegui(hass, passi: list[dict[str, Any]], variabili: dict[str, Any], esito: dict[str, list[Any]],
            al_ciclo: Callable[[], None] | None = None) -> bool:
    """Esegue i passi; False se una condizione (o uno stop) ferma la sequenza. Un ciclo registra il comando, poi
    al_ciclo porta gli stati a quelli dell'uscita e si registra se l'until e' vero."""
    for passo in passi:
        if "variables" in passo:
            for nome, modello in passo["variables"].items():
                variabili[nome] = _render(hass, modello, variabili)
        elif "condition" in passo:
            if not _vera(hass, passo, variabili):
                return False
        elif "if" in passo:
            if all(_vera(hass, c, variabili) for c in passo["if"]):
                if not _esegui(hass, passo["then"], variabili, esito, al_ciclo):
                    return False
            elif "else" in passo and not _esegui(hass, passo["else"], variabili, esito, al_ciclo):
                return False
        elif "choose" in passo:
            opzione = next((o for o in passo["choose"] if all(_vera(hass, c, variabili) for c in o["conditions"])),
                           None)
            sequenza = opzione["sequence"] if opzione is not None else passo.get("default", [])
            if not _esegui(hass, sequenza, variabili, esito, al_ciclo):
                return False
        elif "repeat" in passo:
            esito["comandi"].append(passo["repeat"]["sequence"][0]["action"].removeprefix("shell_command.vmc_master_"))
            if al_ciclo is not None:
                al_ciclo()
            esito["uscita"].append(_vera(hass, passo["repeat"]["until"][0], variabili))
        elif "stop" in passo:
            return False
        elif "wait_template" in passo:
            continue
        elif passo.get("action") in ("input_boolean.turn_on", "input_boolean.turn_off"):
            stato = passo["action"].removeprefix("input_boolean.turn_")
            bersagli = passo["target"]["entity_id"]
            for entita in [bersagli] if isinstance(bersagli, str) else bersagli:
                attuale = hass.states.get(entita)
                if attuale is None or attuale.state != stato:
                    hass.states.async_set(entita, stato)
        elif passo.get("action") == "script.vmc_master_calendario_fascia_1_o_2_off":
            azzera = _pacchetto()["script"]["vmc_master_azzera_booleans"]["sequence"]
            _esegui(hass, azzera, {"mantieni_pannelli": True}, esito)
        else:
            esito["altro"].append(passo.get("action"))
    return True


def _nuovo_esito() -> dict[str, list[Any]]:
    return {"comandi": [], "uscita": [], "altro": []}


def _stato_base(hass) -> None:
    """Fuori dalla Fascia, VMC ON-Line e leggibile a Velocita' 1 (quella della Fascia), tutte le spie spente."""
    for entita in set(re.findall(r"input_boolean\.vmc_master_[a-z0-9_]+", _testo("vmc_master_automazione.txt"))):
        if not entita.endswith("_"):  # i nomi composti nei template («..._spia_calendario_' ~ g»)
            hass.states.async_set(entita, "off")
    vecchio = time.time() - 600
    for entita, stato in {
        INTERRUTTORE: "on", "input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc": "on",
        IP: "ON-Line", BO: "off", ATTESA: "32.0", FASE: "0.0", TCP: "VMGO,00001", LETTURA_INTERFACCIA: "Velocità 1",
        "sensor.vmc_master_alert_monitoraggio_co2": "Nessuna Allerta",
        "sensor.vmc_master_alert_monitoraggio_voc": "Nessuna Allerta",
        "sensor.vmc_master_status_accensione_vmc_tramite_calendario": "Disabilitata",
        "sensor.vmc_master_status_spegnimento_vmc_tramite_calendario": "Disabilitata",
        "sensor.vmc_master_status_accensione_vmc_tramite_calendario_2": "Disabilitata",
        "sensor.vmc_master_status_spegnimento_vmc_tramite_calendario_2": "Disabilitata",
    }.items():
        hass.states.async_set(entita, stato, timestamp=vecchio)
    hass.states.async_set(LETTURA, "Velocità 1", timestamp=vecchio)


def _fine_fascia(hass, ramo: str, ip: str, tcp: str = "unavailable", lettura: str = "Velocità 1") -> dict[str, list[Any]]:
    """Esegue un ramo «Off» con gli stati dell'uscita dal ciclo (TCP «unavailable» da 36 s = lettura persa)."""
    _stato_base(hass)
    hass.states.async_set(LETTURA, lettura, timestamp=time.time() - 600)
    giorno, fascia = ramo.split()[1].lower().replace("ì", "i"), ramo[0]
    hass.states.async_set(f"input_boolean.vmc_master_spia_calendario_{giorno}_{fascia}", "on")
    hass.states.async_set(TCP, tcp, timestamp=time.time() - 36)
    hass.states.async_set(IP, ip)
    esito = _nuovo_esito()
    assert _esegui(hass, _rami_off(_automazione())[ramo]["sequence"], {}, esito)
    assert esito["comandi"] == ["velocita_0"] and esito["uscita"] == [True]
    return esito


# ------------------------------------------------------------------------------------------------ C1-1 a (struttura)
def test_c1_1a_14_rami_off_memorizzano_la_velocita_0_anche_con_la_vmc_off_line() -> None:
    for ident, ramo in _rami_off(_automazione()).items():
        passi = ramo["sequence"]
        i = next(k for k, p in enumerate(passi) if "repeat" in p)
        assert passi[i + 1]["action"] == "script.vmc_master_calendario_fascia_1_o_2_off", ident
        memoria, spia = passi[i + 2], passi[i + 3]
        assert memoria["alias"].startswith("Black-Out prima della conferma -> memorizza la Velocità 0"), ident
        assert "anche con la VMC già OFF-Line ma il Black-Out non ancora rilevato" in memoria["alias"], ident
        assert memoria["if"] == [{"condition": "template", "value_template": MEMORIA}], ident
        assert memoria["then"][0] == {"data": {}, "target": {"entity_id": SPIA_V0}, "action": "input_boolean.turn_on"}
        assert memoria["then"][1]["target"]["entity_id"] == SPIE_VELOCITA
        assert spia["if"] == [{"condition": "template", "value_template": SPIA}], ident
        assert spia["then"] == [{"action": "input_boolean.turn_on", "target": {"entity_id": SPIA_CNE}}], ident
        assert "Fuori dal Calendario hanno effetto tutte le verifiche" in passi[i + 4]["alias"], ident
        assert len(passi) == i + 5, ident


@pytest.mark.parametrize(
    ("bo", "ip", "tcp", "secondi", "lettura", "atteso"),
    [
        ("off", "OFF-Line", "unavailable", 36, "Velocità 1", "True"),  # C1-1 a: uscita per lettura persa, ping gia' OFF-Line
        ("on", "OFF-Line", "unavailable", 36, "Velocità 1", "True"),  # Black-Out rilevato (come nella b34)
        ("off", "OFF-Line", "unavailable", 36, "Velocità 0", "False"),  # Velocita' 0 gia' confermata
        ("off", "ON-Line", "unavailable", 36, "Velocità 1", "False"),  # porta 5001 muta: Spia Comando non eseguito
        ("off", "OFF-Line", "VMGO,00003", 1, "Velocità 3", "False"),  # scelta dell'utente con un ping perso: nessuna memoria
        ("off", "OFF-Line", "unavailable", 10, "Velocità 1", "False"),  # ciclo non uscito per la lettura persa
    ],
)
async def test_c1_1a_condizione_della_memoria(hass, bo, ip, tcp, secondi, lettura, atteso) -> None:
    hass.states.async_set(ATTESA, "32.0")
    hass.states.async_set(BO, bo)
    hass.states.async_set(IP, ip)
    hass.states.async_set(TCP, tcp, timestamp=time.time() - secondi)
    hass.states.async_set(LETTURA, lettura)
    assert _render(hass, MEMORIA) == atteso


# ------------------------------------------------------------------------------------------------ C1-1 a (dinamica)
@pytest.mark.parametrize("ramo", ["1° Lunedì Off", "2° Domenica Off"])
async def test_c1_1a_black_out_a_fine_fascia_al_ritorno_velocita_0(hass, ramo: str) -> None:
    """Black-Out mentre la Fascia finisce: il ciclo esce per la lettura persa con la VMC gia' OFF-Line ma il Black-Out
    non ancora rilevato -> memoria Velocita' 0; «Black-Out a Velocita' X» non puo' scattare (e il sensore Black-Out
    resta spento); al ritorno della corrente «Black-Out Off Vel. 0» rimanda la Velocita' 0."""
    dati = _automazione()
    trigger = {t["id"]: t for t in dati["triggers"] if isinstance(t.get("id"), str)}
    rilevazione = [i for i in trigger if i.startswith("Black-Out") and not i.startswith("Black-Out Off")]
    assert len(rilevazione) == 11
    sensore = next(b for blocco in _pacchetto()["template"] for b in blocco.get("binary_sensor", [])
                   if b.get("default_entity_id") == BO)
    # senza la memoria (b34) «Black-Out a Velocita' 1» e il sensore Black-Out scatterebbero
    _stato_base(hass)
    hass.states.async_set(IP, "OFF-Line")
    assert _render(hass, trigger["Black-Out a Velocità 1"]["value_template"]) == "True"
    assert _render(hass, sensore["state"]) == "True"

    _fine_fascia(hass, ramo, "OFF-Line")
    assert hass.states.get(SPIA_V0).state == "on"
    assert all(hass.states.get(s).state == "off" for s in SPIE_VELOCITA)
    assert hass.states.get(SPIA_CNE).state == "off"
    for ident in rilevazione:
        assert _render(hass, trigger[ident]["value_template"]) == "False", ident
    assert _render(hass, sensore["state"]) == "False"
    # ritorno della corrente: la VMC si riaccende alla velocita' della Fascia finita
    hass.states.async_set(IP, "ON-Line")
    hass.states.async_set(TCP, "VMGO,00001")
    ripristino = [i for i in trigger if i.startswith("Black-Out Off")]
    assert [i for i in ripristino if _render(hass, trigger[i]["value_template"]) == "True"] == ["Black-Out Off Vel. 0"]
    esito = _nuovo_esito()
    _esegui(hass, _rami(dati)["Black-Out Off Vel. 0"]["sequence"], {}, esito,
            al_ciclo=lambda: hass.states.async_set(LETTURA, "Velocità 0"))
    assert esito["comandi"] == ["velocita_0"] and esito["uscita"] == [True]
    assert hass.states.get(SPIA_V0).state == "off"


# ------------------------------------------------------------------------------------------------ C1-1 b (rami «Off»)
@pytest.mark.parametrize(
    ("ip", "tcp", "lettura", "spia_cne", "memoria_0"),
    [
        ("ON-Line", "unavailable", "Velocità 1", "on", "off"),  # porta 5001 muta: Spia Comando non eseguito
        ("ON-Line", "unavailable", "Velocità 0", "off", "off"),  # velocita' memorizzata gia' a 0: nulla da ripetere
        ("OFF-Line", "unavailable", "Velocità 1", "off", "on"),  # Black-Out (C1-1 a)
    ],
)
async def test_c1_1b_fine_fascia_con_la_velocita_illeggibile(hass, ip, tcp, lettura, spia_cne, memoria_0) -> None:
    _fine_fascia(hass, "1° Martedì Off", ip, tcp, lettura)
    assert hass.states.get(SPIA_CNE).state == spia_cne
    assert hass.states.get(SPIA_V0).state == memoria_0


@pytest.mark.parametrize(("tcp", "lettura"), [("VMGO,00000", "Velocità 0"), ("VMGO,00003", "Velocità 3")])
async def test_c1_1b_ciclo_uscito_per_velocita_raggiunta_o_scelta_nessuna_spia(hass, tcp, lettura) -> None:
    _stato_base(hass)
    hass.states.async_set("input_boolean.vmc_master_spia_calendario_giovedi_2", "on")
    esito = _nuovo_esito()

    def uscita() -> None:
        hass.states.async_set(TCP, tcp)
        hass.states.async_set(LETTURA, lettura)

    assert _esegui(hass, _rami_off(_automazione())["2° Giovedì Off"]["sequence"], {}, esito, al_ciclo=uscita)
    assert esito["comandi"] == ["velocita_0"] and esito["uscita"] == [True]
    assert hass.states.get(SPIA_CNE).state == "off" and hass.states.get(SPIA_V0).state == "off"


# ------------------------------------------------------------------------------------------------ C1-1 b (ritorno)
def _ramo_ritorno() -> dict[str, Any]:
    return _rami(_automazione())["calendario_ritorno_comando"]


def _ritorno(hass, tcp: str = "VMGO,00001", lettura: str = "Velocità 1", lettura_fa: float = 600, spia_fa: float = 60,
             **stati: str) -> tuple[dict[str, list[Any]], dict[str, Any]]:
    """La VMC torna leggibile a Fascia finita con la Spia Comando non eseguito accesa da spia_fa secondi."""
    _stato_base(hass)
    ora = time.time()
    hass.states.async_set(SPIA_CNE, "on", timestamp=ora - spia_fa)
    hass.states.async_set(LETTURA, "Velocità 2", timestamp=ora - lettura_fa - 1)  # ultimo cambio: lettura_fa secondi fa
    hass.states.async_set(LETTURA, lettura, timestamp=ora - lettura_fa)
    hass.states.async_set(TCP, tcp)
    for entita, stato in stati.items():
        hass.states.async_set(entita, stato)
    (trigger,) = [t for t in _automazione()["triggers"] if t.get("id") == "calendario_ritorno_comando"]
    assert _render(hass, trigger["value_template"]) == "True"
    return _nuovo_esito(), {}


async def test_c1_1b_ritorno_della_vmc_a_fascia_finita_ripete_la_velocita_0(hass) -> None:
    esito, variabili = _ritorno(hass)

    def vmc_esegue() -> None:
        hass.states.async_set(TCP, "VMGO,00000")
        hass.states.async_set(LETTURA, "Velocità 0")

    _esegui(hass, _ramo_ritorno()["sequence"], variabili, esito, al_ciclo=vmc_esegue)
    assert esito["comandi"] == ["velocita_0"] and esito["uscita"] == [True] and esito["altro"] == []
    assert float(variabili["comando_non_eseguito_dalle"]) > 0
    assert hass.states.get(SPIA_CNE).state == "off" and hass.states.get(SPIA_V0).state == "off"


@pytest.mark.parametrize(
    ("caso", "argomenti"),
    [
        # telecomando durante il silenzio, letture derivate non ancora aggiornate: la lettura appena tornata e' diversa
        ("velocità cambiata, lettura derivata vecchia", {"tcp": "VMGO,00003"}),
        # telecomando durante il silenzio, letture derivate gia' aggiornate (cambiate dopo l'accensione della spia)
        ("velocità cambiata, lettura derivata nuova", {"tcp": "VMGO,00003", "lettura": "Velocità 3", "lettura_fa": 1}),
        ("velocità tornata uguale dopo la spia", {"lettura_fa": 10}),
        ("Congelamento in corso", {GELO: "on"}),
        ("Δ Temp. in corso", {DELTA: "on"}),
        ("interruttore del Calendario spento", {INTERRUTTORE: "off"}),
        ("VMC OFF-Line", {IP: "OFF-Line"}),
        ("Black-Out del Calendario", {SPIA_BO: "on"}),
    ],
)
async def test_c1_1b_ritorno_della_vmc_a_fascia_finita_nessun_comando(hass, caso, argomenti) -> None:
    stati = {k: v for k, v in argomenti.items() if "." in k}
    altri = {k: v for k, v in argomenti.items() if "." not in k}
    esito, variabili = _ritorno(hass, **altri, **stati)
    _esegui(hass, _ramo_ritorno()["sequence"], variabili, esito)
    assert esito["comandi"] == [] and esito["altro"] == [], caso
    assert hass.states.get(SPIA_CNE).state == "off", caso


async def test_c1_1b_ritorno_con_una_fascia_accesa_riparte_la_fascia(hass) -> None:
    """Il caso della b34 non cambia: con la spia di una Fascia accesa riparte lo script della Fascia."""
    esito, variabili = _ritorno(hass, **{"input_boolean.vmc_master_spia_calendario_mercoledi_2": "on"})
    _esegui(hass, _ramo_ritorno()["sequence"], variabili, esito)
    assert esito["comandi"] == [] and esito["altro"] == ["script.vmc_master_calendario_fascia_2_on"]


@pytest.mark.parametrize(
    ("tcp", "ip", "lettura", "spia_cne", "memoria_0"),
    [
        ("unavailable", "ON-Line", "Velocità 1", "on", "off"),  # di nuovo illeggibile: spia di nuovo accesa
        ("unavailable", "OFF-Line", "Velocità 1", "off", "on"),  # Black-Out durante la ripetizione: memoria Velocita' 0
        ("VMGO,00002", "ON-Line", "Velocità 2", "off", "off"),  # scelta dell'utente durante la ripetizione
    ],
)
async def test_c1_1b_ritorno_dopo_il_ciclo(hass, tcp, ip, lettura, spia_cne, memoria_0) -> None:
    esito, variabili = _ritorno(hass)

    def uscita() -> None:
        hass.states.async_set(TCP, tcp, timestamp=time.time() - 36)
        hass.states.async_set(IP, ip)
        hass.states.async_set(LETTURA, lettura)

    _esegui(hass, _ramo_ritorno()["sequence"], variabili, esito, al_ciclo=uscita)
    assert esito["comandi"] == ["velocita_0"] and esito["uscita"] == [True]
    assert hass.states.get(SPIA_CNE).state == spia_cne
    assert hass.states.get(SPIA_V0).state == memoria_0


def test_c1_1b_struttura_del_ramo_del_ritorno() -> None:
    """Terza opzione del ramo: stesso ciclo, stessa memoria e stessa spia dei rami «Off»; nessuna chiamata di script;
    trigger e guardia invariati (nessun tempo nuovo)."""
    dati = _automazione()
    passi = _ramo_ritorno()["sequence"]
    (scelta,) = passi[3:]
    assert len(scelta["choose"]) == 3 and "default" not in scelta
    terza = scelta["choose"][2]
    assert " ".join(terza["conditions"][0]["value_template"].split()) == "{{ " + " and ".join(
        f"states('input_boolean.vmc_master_spia_calendario_{g}_{n}') == 'off'" for n in (1, 2) for g in GIORNI) + " }}"
    assert " ".join(terza["conditions"][1]["value_template"].split()) == (
        f"{{{{ states('{GELO}') == 'off' and states('{DELTA}') == 'off' }}}}")
    controllo = " ".join(terza["conditions"][2]["value_template"].split())
    assert f"as_timestamp(states.{LETTURA}.last_changed, 0) <= comando_non_eseguito_dalle | float(0)" in controllo
    assert f"states('{TCP}').split(',')" in controllo
    off = _rami_off(dati)["1° Lunedì Off"]["sequence"]
    i = next(k for k, p in enumerate(off) if "repeat" in p)
    assert terza["sequence"] == [off[i - 1], off[i], off[i + 2], off[i + 3]]
    assert "script." not in str(terza) and "delay" not in str(terza["conditions"])
    (trigger,) = [t for t in dati["triggers"] if t.get("id") == "calendario_ritorno_comando"]
    assert "for" not in trigger


async def test_c1_1b_controllo_della_velocita_con_le_letture_dell_interfaccia(hass) -> None:
    """Il controllo decodifica la lettura appena tornata come il sensore della velocita' (stessi codici)."""
    controllo = _ramo_ritorno()["sequence"][3]["choose"][2]["conditions"][2]["value_template"]
    pacchetto = _testo("vmc_master.yaml")
    for codice, velocita in (("00000", "Velocità 0"), ("00004", "Velocità 4"), ("00005", "Iperventilazione"),
                             ("00006", "Notturna"), ("00007", "Free Cooling")):
        assert f"'{codice}': '{velocita}'" in pacchetto
        hass.states.async_set(TCP, f"VMGO,{codice},00001")
        hass.states.async_set(LETTURA, velocita, timestamp=time.time() - 100)
        assert _render(hass, controllo, {"comando_non_eseguito_dalle": time.time() - 50}) == "True"
        assert _render(hass, controllo, {"comando_non_eseguito_dalle": time.time() - 150}) == "False"
    for tcp in ("unavailable", "unknown", "VMGO"):
        hass.states.async_set(TCP, tcp)
        assert _render(hass, controllo, {"comando_non_eseguito_dalle": time.time()}) == "False"


# ------------------------------------------------------------------------------------------------ C1-4
def _transizioni() -> list[dict[str, Any]]:
    rami = _rami(_automazione())
    return [next(p for p in rami[i]["sequence"] if "Calendario in transizione" in p.get("alias", ""))
            for i in ("Congelamento OFF", "delta_temp_OFF")]


def test_c1_4_i_due_blocchi_restano_identici() -> None:
    gelo, delta = _transizioni()
    assert gelo["if"] == delta["if"]
    assert " ".join(gelo["alias"].split()).replace("Congelamento", "Δ Temp.") == " ".join(delta["alias"].split())
    assert "anche una fascia di un altro giorno finita prima della mezzanotte" in " ".join(gelo["alias"].split())
    assert gelo["then"][-1] == delta["then"][-1] == {"stop": "Ripresa lasciata al Calendario"}


@pytest.mark.parametrize(
    ("ora", "accese", "atteso"),
    [
        ((0, 10), ["sabato_2"], "True"),  # C1-4: fascia del sabato finita alle 23:30 durante l'allerta
        ((0, 10), ["sabato_1"], "True"),
        ((0, 10), ["venerdi_2"], "True"),
        ((0, 10), [], "False"),  # nessuna fascia: ripresa normale
        ((9, 0), ["domenica_1"], "False"),  # fascia di oggi ancora in corso: nessuna transizione
        ((11, 0), ["domenica_1"], "True"),  # fascia di oggi finita (come nella b34)
        ((9, 0), [], "True"),  # fascia di oggi iniziata durante l'allerta (come nella b34)
    ],
)
async def test_c1_4_fascia_di_un_altro_giorno_ancora_accesa(hass, freezer, ora, accese, atteso) -> None:
    freezer.move_to(datetime(2026, 11, 22, *ora, tzinfo=dt_util.get_default_time_zone()))  # domenica
    assert dt_util.now().weekday() == 6
    for g in GIORNI:
        for n in (1, 2):
            hass.states.async_set(f"input_boolean.vmc_master_spia_calendario_{g}_{n}", "off")
    for spia in accese:
        hass.states.async_set(f"input_boolean.vmc_master_spia_calendario_{spia}", "on")
    hass.states.async_set(INTERRUTTORE, "on")
    hass.states.async_set("sensor.vmc_master_status_accensione_vmc_tramite_calendario", "Domenica")
    hass.states.async_set("sensor.vmc_master_status_accensione_vmc_tramite_calendario_2", "Domenica")
    for chiave, valore in (("accensione_domenica", "08:00:00"), ("spegnimento_domenica", "10:00:00"),
                           ("accensione_domenica_2", "18:00:00"), ("spegnimento_domenica_2", "20:00:00")):
        hass.states.async_set(f"input_datetime.vmc_master_{chiave}", valore)
    for blocco in _transizioni():
        assert _render(hass, blocco["if"][0]["value_template"]) == atteso


# ------------------------------------------------------------------------------------------------ C5-1
# b36 (C1-3, C1-5): l'attesa della fine di Congelamento/Δ e il comando dello spegnimento del Calendario
FRASE = ("se invece la VMC risponde al ping ma la sua velocità non si legge (porta 5001), dopo 32 Secondi la Fascia "
         "smette di ripetere il comando e, appena la velocità torna leggibile, la Fascia riparte (con un'allerta "
         "Congelamento o Δ Temp. in corso aspetta la fine dell'allerta e poi riparte con la sua Velocità), salvo se nel "
         "frattempo la Velocità è cambiata (per esempio con il Telecomando); lo stesso vale per la Velocità 0 di fine "
         "Fascia e per il comando dato spegnendo l'interruttore del Calendario durante una Fascia (Velocità 0, o "
         "Velocità 1 con Inquinanti): appena la velocità torna leggibile il comando viene ripetuto, salvo se nel "
         "frattempo la Velocità è cambiata o è in corso un'allerta Congelamento o Δ Temp.; se invece la corrente manca "
         "proprio mentre la Fascia finisce, al ritorno della corrente la VMC si arresta dopo 32 Secondi;")


def test_c5_1_descrizione_e_voce_17() -> None:
    descrizione = " ".join(_automazione()["description"].split())
    scheda = " ".join(_testo("vmc_master_scheda_manuale_interfaccia.txt").split())
    assert FRASE in descrizione
    assert FRASE + "<br>" in scheda
    for testo in (descrizione, scheda):
        assert "non esegue i comandi" not in testo
        assert "non ha eseguito il comando" not in testo


def test_c5_1_riquadro_avvisi() -> None:
    scheda = _testo("vmc_master_scheda_manuale_interfaccia.txt")
    # b36 (C1-3, C1-5): il comando dello spegnimento del Calendario e l'attesa della fine di Congelamento/Δ
    riga = ('label: "La VMC risponde in rete ma la sua velocità non si legge: il comando del Calendario (velocità della '
            "fascia, Velocità 0 di fine fascia o comando dato spegnendo l'interruttore del Calendario durante la fascia) "
            "non è confermato. Appena la velocità torna leggibile il comando riparte, salvo se nel frattempo la velocità "
            "è cambiata; con un'allerta Congelamento o Δ Temp. in corso la velocità della fascia riparte alla fine "
            "dell'allerta, gli altri comandi non vengono ripetuti. Non serve fare nulla.\"")
    assert scheda.count(riga) == 1
    blocco = scheda[scheda.rindex("- type: conditional", 0, scheda.index(riga)): scheda.index(riga)]
    assert SPIA_CNE in blocco and "state: ON-Line" in blocco


def test_c5_1_descrizioni_degli_script_di_fascia() -> None:
    script = _pacchetto()["script"]
    uno, due = (" ".join(script[f"vmc_master_calendario_fascia_{n}_on"]["description"].split()) for n in (1, 2))
    assert uno.replace("1° Fascia", "2° Fascia") == due
    frase = ("Anche la Velocità 0 che l'Automazione manda alla fine della Fascia smette di essere ripetuta se la velocità "
             "non si legge: si accende la stessa Spia e, appena la VMC torna a rispondere, la Velocità 0 viene ripetuta, "
             "salvo se nel frattempo la velocità è cambiata o è in corso un'allerta Congelamento o Δ Temp.; se invece la "
             "VMC va OFF-Line prima di confermarla, la Velocità 0 viene memorizzata e rimandata al ritorno della corrente.")
    assert frase in uno
    for vietata in ("vmc_master", "master", "input_", "sensor.", "999.999"):
        assert vietata not in uno


def test_file_validi_e_fini_riga() -> None:
    for nome, crlf in (("vmc_master.yaml", True), ("vmc_master_scheda_manuale_interfaccia.txt", True),
                       ("vmc_master_automazione.txt", False)):
        dati = (PKG / nome).read_bytes()
        if crlf:
            assert dati.count(b"\r\n") == dati.count(b"\n"), nome
        else:
            assert b"\r" not in dati, nome
    assert _automazione()["mode"] == "queued"
