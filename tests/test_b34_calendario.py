"""Prove della 9.0.0b34, Calendario e Countdown (rilievi B1-1, B1-3, B1-4, B1-5, B1-6, B1-7 della verifica profonda
della b33).

B1-1: il ciclo «ripeti finche' la VMC conferma» del Calendario non finiva se la VMC risponde al ping ma la porta 5001
non risponde (velocita' letta sempre quella di prima, nessun OFF-Line): l'automazione principale (in coda) restava
ferma. Ora tutti i cicli del Calendario (360 negli script di Fascia, 14 nei rami «Off») escono anche quando la lettura
della velocita' (sensore TCP, «unavailable» a ogni lettura fallita) manca da quanto dura la rilevazione del Black-Out.
Nessun tempo nuovo: si usa la stessa attesa della rilevazione del Black-Out."""

from __future__ import annotations

import time
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
from homeassistant.util import yaml as hay

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"
FASCE = ("vmc_master_calendario_fascia_1_on", "vmc_master_calendario_fascia_2_on")
TCP = "sensor.vmc_master_status_ventola"
LETTURA = "sensor.vmc_master_status_ventola_lettura_codice_interpretato"
ATTESA = "input_number.vmc_master_attesa_blackout_rilevazione"
LETTURA_PERSA = (f"(is_state('{TCP}', 'unavailable') and (now() - states.{TCP}.last_changed).total_seconds() >= "
                 f"states('{ATTESA}') | int(32))")


def _pacchetto() -> dict[str, Any]:
    return hay.load_yaml(str(PKG / "vmc_master.yaml"))


def _automazione() -> dict[str, Any]:
    return hay.load_yaml(str(PKG / "vmc_master_automazione.txt"))


def _cicli(nodo: Any) -> Iterator[dict[str, Any]]:
    if isinstance(nodo, dict):
        if "repeat" in nodo:
            yield nodo["repeat"]
        for valore in nodo.values():
            yield from _cicli(valore)
    elif isinstance(nodo, list):
        for valore in nodo:
            yield from _cicli(valore)


def _cicli_calendario() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """I cicli degli script di Fascia e quelli dei rami «Off» (1°/2° giorno Off) dell'automazione."""
    script = _pacchetto()["script"]
    fasce = [c for nome in FASCE for c in _cicli(script[nome]["sequence"])]
    rami = [r for b in _automazione()["actions"] if "choose" in b for r in b["choose"]]
    off = [c for r in rami
           if isinstance(r["conditions"][0].get("id"), str) and r["conditions"][0]["id"].endswith(" Off")
           and r["conditions"][0]["id"][:2] in ("1°", "2°")
           for c in _cicli(r["sequence"])]
    return fasce, off


# ------------------------------------------------------------------------------------------------------------ B1-1
def test_b1_1_tutti_i_cicli_del_calendario_escono_con_la_lettura_persa() -> None:
    fasce, off = _cicli_calendario()
    assert len(fasce) == 360 and len(off) == 14
    for ciclo in fasce + off:
        (fine,) = ciclo["until"]
        assert fine["value_template"].endswith(f" or {LETTURA_PERSA} }}}}"), fine["value_template"][-200:]
        assert "lettura della velocità persa per il tempo di rilevazione del Black-Out" in fine["alias"]
    # nessun altro ciclo ha la nuova uscita: 360 nel package, 14 nell'automazione, in tutto 374
    pacchetto = (PKG / "vmc_master.yaml").read_text(encoding="utf-8")
    automazione = (PKG / "vmc_master_automazione.txt").read_text(encoding="utf-8")
    assert pacchetto.count(LETTURA_PERSA) == 360
    assert automazione.count(LETTURA_PERSA) == 14


def test_b1_1_il_sensore_letto_e_quello_tcp() -> None:
    """La condizione legge il sensore TCP della porta 5001 (che da HA 2026.x diventa «unavailable» a ogni lettura
    fallita), non la sua copia «memorizzata» che conserva l'ultimo valore."""
    tcp = next(s for s in _pacchetto()["sensor"] if s.get("name") == "vmc_master_status_ventola")
    assert tcp["platform"] == "tcp" and tcp["port"] == 5001 and tcp["payload"] == "VMGH?"


def _until_fascia() -> str:
    fasce, _ = _cicli_calendario()
    return next(c["until"][0]["value_template"] for c in fasce
                if c["sequence"][0]["action"] == "shell_command.vmc_master_velocita_2")


@pytest.mark.parametrize(
    ("stato_tcp", "secondi_fa", "attesa", "atteso"),
    [
        (None, 0, "32.0", "False"),  # sensore TCP inesistente: nessun errore
        ("0102", 100, "32.0", "False"),  # lettura valida
        ("unavailable", 10, "32.0", "False"),  # lettura persa da poco (disturbo): si continua a ripetere
        ("unavailable", 40, "32.0", "True"),  # lettura persa da almeno 32 s: il ciclo finisce
        ("unavailable", 40, "60.0", "False"),  # stessa attesa della rilevazione del Black-Out
        ("unavailable", 40, "unknown", "True"),  # attesa non disponibile: riserva 32 s
        ("unknown", 40, "32.0", "False"),
    ],
)
async def test_b1_1_uscita_dal_ciclo(hass, stato_tcp, secondi_fa, attesa, atteso) -> None:
    from homeassistant.helpers.template import Template

    hass.states.async_set(LETTURA, "Velocità 0")
    hass.states.async_set("sensor.vmc_master_status_ip_interfaccia", "ON-Line")
    hass.states.async_set("binary_sensor.vmc_master_black_out_rilevato", "off")
    hass.states.async_set(ATTESA, attesa)
    if stato_tcp is not None:
        hass.states.async_set(TCP, stato_tcp, timestamp=time.time() - secondi_fa)
    reso = Template(_until_fascia(), hass).async_render({"vel_prima_del_comando": "Velocità 0"}, parse_result=False)
    assert reso == atteso


# ------------------------------------------------------------------------- simulazione dei choose degli script di Fascia
PDR_STATI = ("Se ne sconsiglia l'impiego", "Si può impiegare", "Non disponibile")
INT_PDR = "input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr"
INT_INQ = "input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc"
CO2 = "sensor.vmc_master_alert_monitoraggio_co2"
VOC = "sensor.vmc_master_alert_monitoraggio_voc"
MESE = "sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling"
SPIA_FREE = "sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi"


def _vera(hass, condizione: dict[str, Any]) -> bool:
    from homeassistant.helpers.template import Template

    tipo = condizione["condition"]
    if tipo == "template":
        reso = Template(condizione["value_template"], hass).async_render({}, parse_result=False).strip()
        assert reso in ("True", "False"), reso
        return reso == "True"
    if tipo == "state":
        return hass.states.get(condizione["entity_id"]).state == condizione["state"]
    if tipo == "and":
        return all(_vera(hass, c) for c in condizione["conditions"])
    assert tipo == "or", tipo
    return any(_vera(hass, c) for c in condizione["conditions"])


def _esegui(hass, passi: list[dict[str, Any]], esito: dict[str, Any]) -> dict[str, Any]:
    """Segue il percorso dello script (primo ramo vero di ogni choose, poi il default se c'e'): comando mandato
    (primo passo del ciclo) e memorie accese. Nessun comando = None."""
    for passo in passi:
        if "choose" in passo:
            ramo = next((o for o in passo["choose"] if all(_vera(hass, c) for c in o["conditions"])), None)
            if ramo is not None:
                _esegui(hass, ramo["sequence"], esito)
            elif "default" in passo:
                _esegui(hass, passo["default"], esito)
        elif "repeat" in passo:
            assert esito["comando"] is None
            esito["comando"] = passo["repeat"]["sequence"][0]["action"].removeprefix("shell_command.vmc_master_")
        elif passo.get("action") == "input_boolean.turn_on":
            bersaglio = passo["target"]["entity_id"]
            esito["accese"] |= {bersaglio} if isinstance(bersaglio, str) else set(bersaglio)
    return esito


def _imposta(hass, **stati: str) -> None:
    for entita, stato in stati.items():
        hass.states.async_set(entita, stato)


def _opzione_free(script: dict[str, Any], nome: str) -> list[dict[str, Any]]:
    (opzione,) = [o for o in script[nome]["sequence"][3]["choose"]
                  if o["conditions"][0]["conditions"][0]["state"] == "Free Cool./Heat."]
    return opzione["sequence"]


# ------------------------------------------------------------------------------------------------------------ B1-3
async def test_b1_3_allerte_free_cooling_on_legge_l_interruttore_pdr(hass) -> None:
    """Il ramo «Allerte Free Cooling ON» fa esattamente quello che fa il ramo gemello «Allerte Free Heating ON»
    (che ha lo strato degli interruttori PdR/Inquinanti), con la memoria della programmazione Free Cooling al posto
    di quella Free Heating: con l'interruttore PdR spento la memoria PdR non si accende piu'."""
    script = _pacchetto()["script"]
    memoria_pdr = "input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio"
    _imposta(hass, **{SPIA_FREE: "Allerta Free", "input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia": "off",
                      "input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia": "off"})
    prove = 0
    for nome in FASCE:
        passi = _opzione_free(script, nome)
        for int_pdr in ("on", "off"):
            for int_inq in ("on", "off"):
                for pdr in PDR_STATI:
                    for co2 in ("Allerta", "Nessuna Allerta"):
                        for voc in ("Allerta", "Nessuna Allerta"):
                            _imposta(hass, **{INT_PDR: int_pdr, INT_INQ: int_inq, CO2: co2, VOC: voc,
                                              "sensor.vmc_master_punto_di_rugiada_verifica_confronto": pdr})
                            _imposta(hass, **{MESE: "Free Cooling"})
                            cooling = _esegui(hass, passi, {"comando": None, "accese": set()})
                            _imposta(hass, **{MESE: "Free Heating"})
                            heating = _esegui(hass, passi, {"comando": None, "accese": set()})
                            gemello = {e.replace("_freeheating", "_freecooling") for e in heating["accese"]}
                            assert cooling["comando"] == heating["comando"] is not None
                            assert cooling["accese"] == gemello, (nome, int_pdr, int_inq, pdr, co2, voc)
                            if int_pdr == "off":
                                assert memoria_pdr not in cooling["accese"]
                            prove += 1
    assert prove == 2 * 2 * 2 * 3 * 2 * 2


# ------------------------------------------------------------------------------------------------------------ B1-6
VELOCITA_FASCIA = ("Velocità 0", "Velocità 1", "Velocità 2", "Velocità 3", "Velocità 4", "Notturna",
                   "Iperventilazione", "Free Cool./Heat.")
NON_ALLERTA = "not (states('sensor.vmc_master_alert_monitoraggio_co2') == 'Allerta' or " \
              "states('sensor.vmc_master_alert_monitoraggio_voc') == 'Allerta')"


def _casi(nodo: Any) -> Iterator[dict[str, Any]]:
    if isinstance(nodo, dict):
        if "choose" in nodo and any("alert_monitoraggio_co2" in str(o["conditions"]) for o in nodo["choose"]):
            yield nodo
        for valore in nodo.values():
            yield from _casi(valore)
    elif isinstance(nodo, list):
        for valore in nodo:
            yield from _casi(valore)


def test_b1_6_casi_senza_lacune() -> None:
    """In ogni scelta dei 4 casi i casi «nessuna allerta Inquinanti» valgono ogni volta che non c'e' un'allerta CO₂ o
    VOC (anche con i sensori «Non disponibile»): i 4 casi coprono tutti gli stati e non si sovrappongono (nessun
    caso gia' coperto cambia ramo). Il mese non disponibile vale come mese non programmato."""
    import re

    script = _pacchetto()["script"]
    for nome in FASCE:
        scelte = list(_casi(script[nome]["sequence"]))
        assert len(scelte) == 45, nome
        for scelta in scelte:
            testi = [re.sub(r"\s+", " ", o["conditions"][0]["value_template"]) for o in scelta["choose"]]
            assert len(testi) == 4 and not any("Nessuna Allerta" in t for t in testi)
            allerta = [t for t in testi if NON_ALLERTA not in t]
            assert len(allerta) == 2 and all(
                "(states('sensor.vmc_master_alert_monitoraggio_co2') == 'Allerta' or "
                "states('sensor.vmc_master_alert_monitoraggio_voc') == 'Allerta')" in t for t in allerta)
        mese = _opzione_free(script, nome)[1]["choose"][2]["conditions"][0]
        assert re.sub(r"\s+", " ", mese["value_template"]) == (
            f"{{{{ states('{MESE}') not in [\"Free Heating\", \"Free Cooling\"] }}}}")
        assert "default" not in script[nome]["sequence"][3]  # con Congelamento o Δ Temp. nessun comando


async def test_b1_6_sensori_non_disponibili_comando_come_senza_allerte(hass) -> None:
    """Per ogni Fascia, velocita', interruttore e stato dei sensori parte sempre un comando (in assenza di
    Congelamento e Δ Temp.); con CO₂/VOC «Non disponibile» lo stesso comando e le stesse memorie di «Nessuna
    Allerta», con il mese «Non disponibile» gli stessi di un mese non programmato (Foglio A25: senza allerte la
    VMC va alla velocita' della Fascia). Con il Congelamento in corso nessun comando."""
    import itertools

    script = _pacchetto()["script"]
    gelo = "input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia"
    _imposta(hass, **{gelo: "off", "input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia": "off"})
    inquinanti = ("Allerta", "Nessuna Allerta", "Non disponibile")
    prove = 0
    for nome in FASCE:
        selettore = f"sensor.vmc_master_speed_{nome[-4]}_fascia_calendario"
        for velocita in VELOCITA_FASCIA:
            free = velocita == "Free Cool./Heat."
            mesi = ("Free Heating", "Free Cooling", "Disabilitata", "Non disponibile") if free else ("Disabilitata",)
            spie = ("Allerta Free", "Nessuna Allerta Free Heating Programmato",
                    "Nessuna Allerta Free Cooling Programmato") if free else ("-",)
            for ip, ii, pdr, co2, voc, mese, spia in itertools.product(
                    ("on", "off"), ("on", "off"), PDR_STATI, inquinanti, inquinanti, mesi, spie):
                stati = {selettore: velocita, INT_PDR: ip, INT_INQ: ii, CO2: co2, VOC: voc, MESE: mese, SPIA_FREE: spia,
                         "sensor.vmc_master_punto_di_rugiada_verifica_confronto": pdr}
                _imposta(hass, **stati)
                esito = _esegui(hass, script[nome]["sequence"], {"comando": None, "accese": set()})
                assert esito["comando"] is not None, stati
                if "Non disponibile" in (co2, voc, mese):
                    _imposta(hass, **{CO2: co2.replace("Non disponibile", "Nessuna Allerta"),
                                      VOC: voc.replace("Non disponibile", "Nessuna Allerta"),
                                      MESE: mese.replace("Non disponibile", "Disabilitata")})
                    assert _esegui(hass, script[nome]["sequence"], {"comando": None, "accese": set()}) == esito, stati
                prove += 1
            _imposta(hass, **{gelo: "on"})
            assert _esegui(hass, script[nome]["sequence"], {"comando": None, "accese": set()})["comando"] is None
            _imposta(hass, **{gelo: "off"})
    assert prove == 2 * (7 * 2 * 2 * 3 * 3 * 3 + 2 * 2 * 3 * 3 * 3 * 4 * 3)
