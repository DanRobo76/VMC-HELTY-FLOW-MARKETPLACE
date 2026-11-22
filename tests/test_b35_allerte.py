"""Prove della b35, fetta «allerte»: correzioni dell'audit 1:1 della b34 (rapporti degli agenti 3, 4 e 5).

- C3-3: spegnendo l'interruttore degli Inquinanti nei primi 8 s di un'allerta partita con la VMC in moto (spia
  dell'allerta accesa, nessuna memoria ancora) la VMC non andava subito a Velocità 0 e la memoria che arrivava dopo
  poteva fermarla dopo una scelta dell'utente (Foglio A27, TIMING 0): il trigger guarda anche la spia dell'allerta e la
  memoria Velocità 1 Inquinanti/PdR.
- C3-1: Δ Temp., una velocità scelta negli ultimi 4 s dell'allerta (o nei 4 s di attesa della fine) non veniva
  memorizzata e il ripristino rimandava la velocità di prima (Foglio D6): ora resta la velocità scelta, come per il PdR.
- C4-1: con la Free sospesa e il PdR superato la ripresa Free (24 s) faceva ripartire la VMC in Free per ~16 s (Foglio
  F6, F15, F19, G6): la ripresa senza Inquinanti attende la fine dell'allerta PdR e, con la ripresa in attesa e le
  condizioni gia' favorevoli, il PdR memorizza la Free (la VMC resta ferma e l'Umidita' non parte).
- C4-2: il ripristino Free a fine PdR non aveva il controllo «Umidita' partita da Velocita' 0 e gia' finita».
- C3-4: ramo «Spia Velocità Free Heating/Cooling CO₂ e/o VOC», opzione «spie Free OFF»: l'«until» del ciclo delle spie
  controllava 2 spie che il ciclo non spegne.
- C5-2: descrizione dell'automazione e voce 17 senza l'eccezione del Foglio A21 (prima un'altra velocita' tenuta 4 s,
  poi Velocita' 0: la VMC resta ferma anche a fine Umidita'); testi aggiornati anche per C3-1 e C4-1.
"""

from __future__ import annotations

import asyncio
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

import pytest
from homeassistant.core import Context, HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.script import Script
from homeassistant.helpers.template import Template
from homeassistant.util import yaml as hay

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"
LETTURA = "sensor.vmc_master_status_ventola_lettura_codice_interpretato"
LETTURA_I = "sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia"
IP = "sensor.vmc_master_status_ip_interfaccia"
FASE = "input_number.vmc_master_fase_riallineamento_al_riavvio"
SPIA_CO2 = "input_boolean.vmc_master_spia_co2_o_voc"
PARTENZA = "input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0"
V1_PDR = "input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr"
INT_CO2 = "input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc"
INT_PDR = "input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr"
CONFRONTO = "sensor.vmc_master_punto_di_rugiada_verifica_confronto"
SCONSIGLIATO = "Se ne sconsiglia l'impiego"
FREE = "sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi"
FREE_C = "input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling"
FREE_H = "input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating"
SPIA_DELTA = "input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia"
SPIA_UMIDITA = "input_boolean.vmc_master_umidita_verifica_soglia_valore_spia"
SPIA_U0 = "input_boolean.vmc_master_spia_umidita_velocita_0"
ALLERTA_UMIDITA = "sensor.vmc_master_alert_monitoraggio_umidita"
SUFFISSI = ("0", "1", "2", "3", "4", "notturna", "iperventilazione", "freecooling")
MEMORIE_CO2 = [f"input_boolean.vmc_master_spia_velocita_{s}_co2_o_voc" for s in SUFFISSI]
MEMORIE_DELTA = [f"input_boolean.vmc_master_spia_velocita_{s}_delta_temp_verifica_soglia_valore" for s in SUFFISSI]
MEMORIE_PDR = [f"input_boolean.vmc_master_spia_velocita_{s}_un_solo_avvio" for s in SUFFISSI]
BLACK_OUT = [f"input_boolean.vmc_master_spia_velocita_{s}" for s in SUFFISSI]
SPIA_BO_CALENDARIO = "input_boolean.vmc_master_spia_calendario_black_out"
COMANDI = ("velocita_0", "velocita_1", "velocita_2", "velocita_3", "velocita_4", "notturna", "iperventilazione",
           "freecooling")

TID_C33 = " Disattivazione VMC per Inquinanti CO2 e/o VOC, precedentemente Armato ed Attivato"
RIPRESA = {"Rip. Free Heating No TeVsTi ": "Heating", "Rip. Free Cooling No TeVsTi ": "Cooling"}
PDR_FREE = {"PdR Spia Free Heating OFF e Spia FreeCooling ON -> Imposta Velocità 0": "Cooling",
            "PdR Spia Free Heating ON e Spia FreeCooling OFF -> Imposta Velocità 0": "Heating"}
RIGA_PDR = ("and not (states('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr') == 'on' and "
            "states('sensor.vmc_master_punto_di_rugiada_verifica_confronto') == \"Se ne sconsiglia l'impiego\")")


def _norm(testo: str) -> str:
    return re.sub(r"\s+", " ", testo).strip()


@lru_cache
def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8").replace("\r\n", "\n")


@lru_cache
def _automazione() -> dict[str, Any]:
    return hay.load_yaml(str(PKG / "vmc_master_automazione.txt"))


def _rami() -> list[dict[str, Any]]:
    return [r for b in _automazione()["actions"] if "choose" in b for r in b["choose"]]


def _ramo(tid: str) -> dict[str, Any]:
    trovati = []
    for ramo in _rami():
        ident = ramo["conditions"][0].get("id")
        if tid in ([ident] if isinstance(ident, str) else ident or []):
            trovati.append(ramo)
    assert len(trovati) == 1, tid
    return trovati[0]


def _trigger(tid: str) -> dict[str, Any]:
    (trigger,) = [t for t in _automazione()["triggers"] if t.get("id") == tid]
    return trigger


def _copia_guardia(tid: str) -> str:
    righe = _testo("vmc_master_automazione.txt").split("\n")
    testa = re.compile(r"\{%-? (el)?if trigger\.id == ['\"]" + re.escape(tid) + r"['\"] -?%\}")
    (inizio,) = [k for k, r in enumerate(righe) if testa.fullmatch(r.strip())]
    rientro = len(righe[inizio]) - len(righe[inizio].lstrip())
    fine = next(k for k in range(inizio + 1, len(righe))
                if len(righe[k]) - len(righe[k].lstrip()) == rientro
                and re.match(r"\{%-? (elif|else|endif)\b", righe[k].strip()))
    return "\n".join(righe[inizio + 1 : fine])


def _copie_countdown(tid: str) -> tuple[str, str]:
    """Le 2 copie (ON e OFF) del trigger nell'automazione «Countdown Attese» del package."""
    pacchetto = hay.load_yaml(str(PKG / "vmc_master.yaml"))
    countdown = next(a for a in pacchetto["automation"] if a.get("id") == "vmc_master_countdown_attese_automazione")
    righe = _testo("vmc_master.yaml").split("\n")
    (testa,) = [k for k, r in enumerate(righe) if r.startswith("      - trigger: template") and f"# {tid.strip()} (ATTESA:" in r]
    id_on = righe[testa + 1].split("id: ", 1)[1].strip().strip('"')
    assert id_on.startswith("ON|")
    copie = {t["id"]: t["value_template"] for t in countdown["triggers"] if t.get("id") in (id_on, "OFF|" + id_on[3:])}
    return copie[id_on], copie["OFF|" + id_on[3:]]


def _render(hass: HomeAssistant, modello: str, variabili: dict[str, Any] | None = None) -> Any:
    return Template(modello, hass).async_render(variabili or {})


def _imposta(hass: HomeAssistant, stati: dict[str, str]) -> None:
    # b39: i trigger delle allerte chiedono spenta anche la Spia Black-Out del Calendario (dopo un Black-Out in Fascia
    # aspettano il ritorno della Fascia): chi dichiara spente le 8 spie del Black-Out dichiara «nessun Black-Out», quindi
    # anche quella del Calendario, salvo se la imposta
    if SPIA_BO_CALENDARIO not in stati and any(stati.get(e) == "off" for e in BLACK_OUT):
        stati = {**stati, SPIA_BO_CALENDARIO: "off"}
    for entita, stato in stati.items():
        hass.states.async_set(entita, stato)


async def _esegui(hass: HomeAssistant, sequenza: list[dict[str, Any]], stati: dict[str, str],
                  attesa: float = 1.5) -> list[str]:
    """Esegue una sequenza dell'automazione con servizi finti: gli input_boolean cambiano stato davvero, i comandi alla
    VMC vengono solo registrati. Se dopo «attesa» secondi la sequenza e' ancora in corso (ciclo di comando con le sue
    attese) viene fermata. Restituisce i comandi inviati."""
    comandi: list[str] = []

    def _entita(call: ServiceCall) -> list[str]:
        valore = call.data.get("entity_id", [])
        if isinstance(valore, str):
            valore = [v.strip() for v in valore.split(",") if v.strip()]
        return list(valore)

    async def _accendi(call: ServiceCall) -> None:
        for entita in _entita(call):
            hass.states.async_set(entita, "on")

    async def _spegni(call: ServiceCall) -> None:
        for entita in _entita(call):
            hass.states.async_set(entita, "off")

    async def _comando(call: ServiceCall) -> None:
        comandi.append(call.service)

    async def _niente(call: ServiceCall) -> None:
        return None

    hass.services.async_register("input_boolean", "turn_on", _accendi)
    hass.services.async_register("input_boolean", "turn_off", _spegni)
    hass.services.async_register("homeassistant", "update_entity", _niente)
    for nome in COMANDI:
        hass.services.async_register("shell_command", f"vmc_master_{nome}", _comando)
    _imposta(hass, stati)
    script = Script(hass, cv.SCRIPT_SCHEMA(sequenza), "Prova b35", "test_b35_allerte")
    corsa = hass.async_create_task(script.async_run(context=Context()))
    finite, _ = await asyncio.wait({corsa}, timeout=attesa)
    if not finite:
        await script.async_stop()
    await asyncio.gather(corsa, return_exceptions=True)
    await hass.async_block_till_done()
    return comandi


def _spente(lista: list[str]) -> dict[str, str]:
    return {e: "off" for e in lista}


# ------------------------------------------------------------------------------------------------ C3-3
def test_c3_3_trigger_e_guardia_guardano_la_spia_dell_allerta() -> None:
    """L'OR del trigger guarda anche la spia dell'allerta Inquinanti e la memoria Velocità 1 Inquinanti/PdR, come il
    trigger di fine Inquinanti; la copia nella guardia «Evento ancora valido» e' identica (il trigger non ha «for»)."""
    trigger = _trigger(TID_C33)
    assert "for" not in trigger
    modello = trigger["value_template"]
    for riga in ("states('input_boolean.vmc_master_spia_co2_o_voc') == 'on' or",
                 "states('input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr') == 'on' or"):
        assert modello.count(riga) == 1, riga
    assert _norm(_copia_guardia(TID_C33)) == _norm(modello)


def _stati_c33(**altri: str) -> dict[str, str]:
    stati = {INT_CO2: "off", IP: "ON-Line", LETTURA_I: "Velocità 2", LETTURA: "Velocità 2", SPIA_CO2: "off",
             PARTENZA: "off", V1_PDR: "off", **_spente(MEMORIE_CO2), **_spente(BLACK_OUT)}
    stati.update(altri)
    return stati


@pytest.mark.parametrize(
    ("altri", "atteso"),
    [
        ({SPIA_CO2: "on"}, True),  # primi 8 s dell'allerta con la VMC in moto: nessuna memoria ancora
        ({V1_PDR: "on"}, True),
        ({SPIA_CO2: "on", INT_CO2: "on"}, False),  # interruttore acceso: niente
        ({}, False),  # la funzione non comanda la VMC: la velocita' non cambia
        ({SPIA_CO2: "on", IP: "OFF-Line"}, False),
        ({"input_boolean.vmc_master_spia_velocita_2_co2_o_voc": "on"}, True),  # come prima
    ],
)
async def test_c3_3_trigger_reso(hass: HomeAssistant, altri: dict[str, str], atteso: bool) -> None:
    _imposta(hass, _stati_c33(**altri))
    assert _render(hass, _trigger(TID_C33)["value_template"]) is atteso
    assert _render(hass, _copia_guardia(TID_C33)) is atteso


async def test_c3_3_ramo_spegne_spia_e_memorie_e_ferma_la_vmc(hass: HomeAssistant) -> None:
    """Il ramo dell'interruttore spento (Congelamento e Δ Temp. spenti) spegne anche la spia dell'allerta e la memoria
    Velocità 1 Inquinanti/PdR e porta la VMC a Velocità 0; con Congelamento o Δ Temp. riaccende l'interruttore."""
    ramo = _ramo(TID_C33)
    opzioni = ramo["sequence"][0]["choose"]
    ciclo = opzioni[0]["sequence"][1]["repeat"]["sequence"]
    spente = ciclo[0]["target"]["entity_id"]
    assert ciclo[0]["action"] == "input_boolean.turn_off"
    assert SPIA_CO2 in spente and V1_PDR in spente and PARTENZA in spente
    assert set(MEMORIE_CO2) <= set(spente) and set(MEMORIE_PDR) <= set(spente)
    assert ciclo[1]["action"] == "shell_command.vmc_master_velocita_0"
    assert opzioni[1]["sequence"][0]["action"] == "input_boolean.turn_on"
    comandi = await _esegui(hass, ramo["sequence"], {
        "input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia": "off", SPIA_DELTA: "off",
        INT_CO2: "off", SPIA_CO2: "on", LETTURA: "Velocità 2"}, attesa=0.5)
    assert comandi[:1] == ["vmc_master_velocita_0"]
    assert hass.states.get(SPIA_CO2).state == "off"


# ------------------------------------------------------------------------------------------------ C3-1
def test_c3_1_protezione_nel_ramo_di_fine_delta() -> None:
    """Dopo il blocco «Calendario in transizione» e prima del ripristino: con una velocita' valida diversa dalla
    Velocità 1 (scelta non ancora memorizzata) spegne le memorie Δ Temp. come il ripristino e si ferma."""
    ramo = _ramo("delta_temp_OFF")
    passi = ramo["sequence"]
    assert passi[0]["alias"].startswith("Calendario in transizione")
    assert set(passi[1]["variables"]) == {"vel_fine_delta", "memoria_inquinanti_fine_delta"}
    protezione = passi[2]
    assert "[Foglio Logiche D6]" in protezione["alias"]
    assert protezione["if"][0]["value_template"] == (
        "{{ vel_fine_delta in ['Velocità 0', 'Velocità 2', 'Velocità 3', 'Velocità 4', 'Notturna', 'Iperventilazione', "
        "'Free Cooling'] }}")
    inquinanti, memorie, fermo = protezione["then"]
    assert set(memorie["target"]["entity_id"]) == {SPIA_DELTA, *MEMORIE_DELTA}
    assert fermo == {"stop": "Velocità scelta dall'utente durante l'allerta Δ Temp. mantenuta"}
    # stesse memorie spente dalle opzioni del ripristino
    for opzione in passi[3]["choose"]:
        spente = [p for p in opzione["sequence"] if p.get("action") == "input_boolean.turn_off" and "data" in p]
        assert spente[0]["target"]["entity_id"] == memorie["target"]["entity_id"]
    assert "is_state('input_boolean.vmc_master_spia_co2_o_voc', 'on')" in inquinanti["if"][0]["value_template"]
    assert passi[3]["alias"] == "Ripristino Velocità"


@pytest.mark.parametrize(
    ("velocita", "memoria"),
    [("Velocità 0", "0"), ("Velocità 2", "2"), ("Velocità 3", "3"), ("Velocità 4", "4"), ("Notturna", "notturna"),
     ("Iperventilazione", "iperventilazione"), ("Free Cooling", "freecooling"), ("Velocità 1", None),
     ("Non disponibile", None)],
)
async def test_c3_1_memoria_inquinanti_della_velocita_scelta(hass: HomeAssistant, velocita: str,
                                                             memoria: str | None) -> None:
    passi = _ramo("delta_temp_OFF")["sequence"]
    modello = passi[1]["variables"]["memoria_inquinanti_fine_delta"]
    risultato = _render(hass, modello, {"vel_fine_delta": velocita})
    assert risultato == (f"input_boolean.vmc_master_spia_velocita_{memoria}_co2_o_voc" if memoria else "")
    assert _render(hass, passi[2]["if"][0]["value_template"], {"vel_fine_delta": velocita}) is (memoria is not None)
    if memoria:
        spente = _render(hass, passi[2]["then"][0]["then"][1]["target"]["entity_id"],
                         {"memoria_inquinanti_fine_delta": risultato})
        assert spente.split(",") == [m for m in MEMORIE_CO2 if m != risultato] + [PARTENZA, V1_PDR]


def _stati_fine_delta(**altri: str) -> dict[str, str]:
    stati = {SPIA_DELTA: "on", **_spente(MEMORIE_DELTA), "input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore": "on",
             SPIA_CO2: "off", PARTENZA: "off", V1_PDR: "off", **_spente(MEMORIE_CO2), IP: "ON-Line",
             "input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario": "off", "binary_sensor.vmc_master_black_out_rilevato": "off"}
    stati.update(altri)
    return stati


async def test_c3_1_velocita_scelta_negli_ultimi_secondi_resta(hass: HomeAssistant) -> None:
    """VMC a Velocità 2 prima del Δ (memoria 2), l'utente sceglie Velocità 3 a fine allerta: nessun comando, la VMC
    resta a Velocità 3 e le memorie del Δ si spengono (prima veniva rimandata la Velocità 2)."""
    comandi = await _esegui(hass, _ramo("delta_temp_OFF")["sequence"], _stati_fine_delta(**{LETTURA: "Velocità 3"}))
    assert comandi == []
    assert hass.states.get(LETTURA).state == "Velocità 3"
    assert all(hass.states.get(e).state == "off" for e in [SPIA_DELTA, *MEMORIE_DELTA])


async def test_c3_1_con_inquinanti_la_scelta_diventa_la_memoria_inquinanti(hass: HomeAssistant) -> None:
    """Con gli Inquinanti in corso la velocita' scelta diventa la memoria degli Inquinanti (D6: la logica Inquinanti
    riparte dalla velocita' scelta), come nelle opzioni del ripristino."""
    comandi = await _esegui(hass, _ramo("delta_temp_OFF")["sequence"], _stati_fine_delta(**{
        LETTURA: "Velocità 3", SPIA_CO2: "on", PARTENZA: "on",
        "input_boolean.vmc_master_spia_velocita_1_co2_o_voc": "on"}))
    assert comandi == []
    accese = {e for e in [*MEMORIE_CO2, PARTENZA, V1_PDR] if hass.states.get(e).state == "on"}
    assert accese == {"input_boolean.vmc_master_spia_velocita_3_co2_o_voc"}
    assert hass.states.get(SPIA_CO2).state == "on"


async def test_c3_1_velocita_0_scelta_con_inquinanti(hass: HomeAssistant) -> None:
    """Velocità 0 scelta a fine allerta con gli Inquinanti in corso: la VMC resta ferma e la memoria Inquinanti diventa
    la Velocità 0 (gli Inquinanti ancora presenti la riavviano a Velocità 1 dopo 8 s, A27), non la velocita' di prima."""
    comandi = await _esegui(hass, _ramo("delta_temp_OFF")["sequence"], _stati_fine_delta(**{
        LETTURA: "Velocità 0", SPIA_CO2: "on", "input_boolean.vmc_master_spia_velocita_2_co2_o_voc": "on"}))
    assert comandi == []
    accese = {e for e in [*MEMORIE_CO2, PARTENZA, V1_PDR] if hass.states.get(e).state == "on"}
    assert accese == {"input_boolean.vmc_master_spia_velocita_0_co2_o_voc"}


async def test_c3_1_velocita_1_ripristina_la_memoria(hass: HomeAssistant) -> None:
    """Con la VMC a Velocità 1 (tenuta dal Δ, o scelta: non cambia la memoria) il ripristino resta quello di prima."""
    comandi = await _esegui(hass, _ramo("delta_temp_OFF")["sequence"], _stati_fine_delta(**{LETTURA: "Velocità 1"}),
                            attesa=0.5)
    assert comandi[:1] == ["vmc_master_velocita_2"]


def test_c3_1_congelamento_senza_lo_stesso_buco() -> None:
    """Nel Congelamento la memoria della velocita' scelta e la fine allerta hanno TIMING 0 (nessun «for»): non c'e' una
    finestra in cui la scelta non sia ancora memorizzata, quindi il ramo «Congelamento OFF» non ha bisogno della
    stessa protezione."""
    trigger = [t for t in _automazione()["triggers"]
               if str(t.get("id", "")).endswith("_congelamento") and str(t["id"]).startswith("spia_velocita_")]
    assert len(trigger) == 8
    assert all("for" not in t for t in trigger)
    assert "for" not in _trigger("Congelamento OFF")


async def test_c3_1_rami_cambiati_validi_per_home_assistant(hass: HomeAssistant) -> None:
    for tid in (TID_C33, "delta_temp_OFF", "Rip. Free Cool./Heat. No PdR", "spia_velocita_freecooling_inquinanti_co2_voc"):
        cv.SCRIPT_SCHEMA(_ramo(tid)["sequence"])


# ------------------------------------------------------------------------------------------------ C4-1
def test_c4_1_condizione_in_tutte_le_copie() -> None:
    aut = _testo("vmc_master_automazione.txt")
    pacchetto = _testo("vmc_master.yaml")
    assert aut.count(RIGA_PDR) == 4 and pacchetto.count(RIGA_PDR) == 4  # 2 trigger: trigger + guardia, ON + OFF
    for tid in [*RIPRESA, *PDR_FREE]:
        modello = _norm(_trigger(tid)["value_template"])
        assert _norm(_copia_guardia(tid)) == modello, tid
        accesa, spenta = _copie_countdown(tid)
        assert _norm(accesa) == modello, tid
        assert modello in _norm(spenta), tid
    for tid in RIPRESA:
        assert _trigger(tid)["value_template"].count(RIGA_PDR) == 1
    for tid, tipo in PDR_FREE.items():
        nuova = (f"(states('{FREE}') in ['Nessuna Allerta Free {tipo} Programmato', 'Nessuna Allerta Free {tipo} "
                 f"Programmato, Presenza di Inquinanti'] and states('{LETTURA}') == 'Velocità 0')")
        assert _norm(_trigger(tid)["value_template"]).count(nuova) == 1, tid
    # il ramo dei trigger 154/156 e' quello del PdR in Free (memoria PdR Free e Velocità 0)
    for tid in PDR_FREE:
        assert "input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio" in str(_ramo(tid)["sequence"])


def _stati_ripresa(tipo: str, **altri: str) -> dict[str, str]:
    stati = {FREE: f"Nessuna Allerta Free {tipo} Programmato", FREE_C: "off", FREE_H: "off",
             ("input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_free"
              + tipo.lower()): "on",
             SPIA_CO2: "off", LETTURA: "Velocità 0", LETTURA_I: "Velocità 0", SPIA_UMIDITA: "off",
             "input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia": "off", SPIA_DELTA: "off",
             IP: "ON-Line", FASE: "0", INT_PDR: "on", CONFRONTO: SCONSIGLIATO, **_spente(BLACK_OUT)}
    stati.update(altri)
    return stati


@pytest.mark.parametrize("tid", list(RIPRESA))
@pytest.mark.parametrize(
    ("altri", "atteso"),
    [
        ({}, False),  # PdR superato con l'interruttore PdR acceso: la ripresa aspetta la fine dell'allerta
        ({INT_PDR: "off"}, True),
        ({CONFRONTO: "Se ne consiglia l'impiego"}, True),
        ({CONFRONTO: "[Non Calcolabile]"}, True),
        ({INT_PDR: "off", LETTURA: "Velocità 2"}, False),  # come prima: velocita' scelta dall'utente
    ],
)
async def test_c4_1_ripresa_free_solo_senza_pdr(hass: HomeAssistant, tid: str, altri: dict[str, str],
                                                atteso: bool) -> None:
    _imposta(hass, _stati_ripresa(RIPRESA[tid], **altri))
    assert _render(hass, _trigger(tid)["value_template"]) is atteso
    assert _render(hass, _copia_guardia(tid)) is atteso
    accesa, spenta = _copie_countdown(tid)
    assert _render(hass, accesa) is atteso
    assert _render(hass, spenta) is (not atteso)


def _stati_pdr_free(tipo: str, **altri: str) -> dict[str, str]:
    stati = _stati_ripresa(tipo, **{"sensor.vmc_master_alert_monitoraggio_co2": "Nessuna Allerta",
                                    "sensor.vmc_master_alert_monitoraggio_voc": "Nessuna Allerta", INT_CO2: "on"})
    stati.update(altri)
    return stati


@pytest.mark.parametrize("tid", list(PDR_FREE))
@pytest.mark.parametrize(
    ("altri", "atteso"),
    [
        ({}, True),  # ripresa in attesa con le condizioni gia' favorevoli e VMC ferma: il PdR memorizza la Free
        ({"stato": "Nessuna Allerta Free {tipo} Programmato, Presenza di Inquinanti", INT_CO2: "off"}, True),
        ({LETTURA: "Velocità 2"}, False),  # velocita' scelta dall'utente: la gestiscono i trigger del PdR
        ({INT_PDR: "off"}, False),
        ({CONFRONTO: "Se ne consiglia l'impiego"}, False),
    ],
)
async def test_c4_1_pdr_con_ripresa_in_attesa_e_free_favorevole(hass: HomeAssistant, tid: str,
                                                                 altri: dict[str, str], atteso: bool) -> None:
    tipo = PDR_FREE[tid]
    altri = dict(altri)
    stato = altri.pop("stato", None)
    _imposta(hass, _stati_pdr_free(tipo, **altri))
    if stato:
        hass.states.async_set(FREE, stato.format(tipo=tipo))
    assert _render(hass, _trigger(tid)["value_template"]) is atteso
    assert _render(hass, _copia_guardia(tid)) is atteso
    accesa, spenta = _copie_countdown(tid)
    assert _render(hass, accesa) is atteso
    assert _render(hass, spenta) is (not atteso)


@pytest.mark.parametrize("tid", list(PDR_FREE))
@pytest.mark.parametrize(("letta", "atteso"), [("Velocità 0", True), ("Velocità 2", False)])  # b36 C4-3: solo a 0
async def test_c4_1_pdr_free_sfavorevole_come_prima(hass: HomeAssistant, tid: str, letta: str, atteso: bool) -> None:
    tipo = PDR_FREE[tid]
    arrestato = ("Allerta Free Cooling Programmato (Riscaldamento Arrestato)" if tipo == "Cooling"
                 else "Allerta Free Heating Programmato (Raffrescamento Arrestato)")
    _imposta(hass, _stati_pdr_free(tipo, **{FREE: arrestato, LETTURA: letta}))
    assert _render(hass, _trigger(tid)["value_template"]) is atteso


# ------------------------------------------------------------------------------------------------ C4-2
def test_c4_2_ramo_free_con_il_controllo_dell_umidita() -> None:
    """Il ripristino Free a fine PdR ha in testa lo stesso controllo dei rami 44-48 e 50."""
    primo = _ramo("Rip. Free Cool./Heat. No PdR")["sequence"][0]
    gemello = _ramo("Rip. Vel. 2 No PdR")["sequence"][0]
    assert primo["if"] == gemello["if"]
    assert primo["then"] == gemello["then"]
    assert primo["alias"].startswith("Umidità partita da Velocità 0 e già finita mentre il PdR teneva ferma la VMC")


def _stati_fine_pdr_free(**altri: str) -> dict[str, str]:
    stati = {SPIA_UMIDITA: "on", SPIA_U0: "on", ALLERTA_UMIDITA: "Nessuna Allerta", **_spente(MEMORIE_PDR),
             "input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio": "on", FREE_C: "off", FREE_H: "off",
             LETTURA: "Velocità 0", "binary_sensor.vmc_master_black_out_rilevato": "off"}
    stati.update(altri)
    return stati


async def test_c4_2_umidita_finita_durante_il_pdr_nessuna_ripartenza_in_free(hass: HomeAssistant) -> None:
    comandi = await _esegui(hass, _ramo("Rip. Free Cool./Heat. No PdR")["sequence"], _stati_fine_pdr_free())
    assert comandi == []
    assert all(hass.states.get(e).state == "off" for e in MEMORIE_PDR)


async def test_c4_2_umidita_ancora_in_corso_ripristino_come_prima(hass: HomeAssistant) -> None:
    comandi = await _esegui(hass, _ramo("Rip. Free Cool./Heat. No PdR")["sequence"],
                            _stati_fine_pdr_free(**{ALLERTA_UMIDITA: "Allerta"}), attesa=0.5)
    assert comandi[:1] == ["vmc_master_freecooling"]


# ------------------------------------------------------------------------------------------------ C3-4
def test_c3_4_until_del_ciclo_delle_spie_solo_su_quello_che_spegne() -> None:
    opzione = _ramo("spia_velocita_freecooling_inquinanti_co2_voc")["sequence"][0]["choose"][0]
    ciclo = next(p["repeat"] for p in opzione["sequence"] if "repeat" in p)
    spente = set(ciclo["sequence"][0]["target"]["entity_id"])
    controllate = set(re.findall(r"states\('(input_boolean\.[a-z0-9_]+)'\)", ciclo["until"][0]["value_template"]))
    assert controllate <= spente
    assert FREE_C not in controllate and FREE_H not in controllate
    assert controllate == spente  # tutte le spie spente dal ciclo sono controllate


# ------------------------------------------------------------------------------------------------ C5-2 e testi
def _voce(testo: str, inizio: str) -> str:
    return _norm(testo.split("\n  - " + inizio, 1)[1].split(";\n\n", 1)[0])


@pytest.mark.parametrize("inizio", ["VMC Sensori Int. Δ Temp. > 23 [°C]: ", "Sup. Lim. Δ PdR: ", "Umidità: "])
def test_descrizione_e_voce_17_uguali(inizio: str) -> None:
    descrizione = _voce(_testo("vmc_master_automazione.txt"), inizio)
    assert "- " + inizio + descrizione + ";<br>" in _norm(_testo("vmc_master_scheda_manuale_interfaccia.txt"))


def test_c5_2_eccezione_a21_nella_descrizione_nella_voce_17_e_nella_tabella() -> None:
    eccezione = ("se invece prima si sceglie una Velocità diversa da quella di avvio e la si tiene almeno 4 Secondi, la "
                 "Velocità 0 scelta dopo viene memorizzata e la VMC resta ferma anche a fine Umidità")
    tabella = ("Se invece prima si è scelta una Velocità diversa da quella di avvio e la si è tenuta almeno 4 Secondi, "
               "la Velocità 0 viene memorizzata e la VMC resta ferma anche a fine Umidità")
    for nome in ("vmc_master_automazione.txt", "vmc_master_scheda_manuale_interfaccia.txt"):
        piatto = _norm(_testo(nome))
        assert piatto.count(eccezione) == 1, nome
        assert piatto.count(tabella) == 1, nome
    assert "Per fermarla si spegne l'interruttore dell'Umidità. " + tabella in _norm(_testo("vmc_master_automazione.txt"))


def test_testi_delta_e_pdr_aggiornati() -> None:
    for nome in ("vmc_master_automazione.txt", "vmc_master_scheda_manuale_interfaccia.txt"):
        piatto = _norm(_testo(nome))
        assert piatto.count("impostata a fine allerta (se l'allerta finisce prima che sia memorizzata, la Velocità "
                            "scelta resta)") == 1, nome
        assert piatto.count("impostata a fine allerta (se l'allerta finisce prima che sia memorizzata, resta la "
                            "Velocità scelta)") == 1, nome
        assert piatto.count("l'Umidità non la avvia fino al termine dell'allerta e un'eventuale ripresa in Free "
                            "Cool./Heat. in attesa riparte solo al termine dell'allerta") == 1, nome
    assert ("(dopo 24 secondi; 20 con Inquinanti). Con un'allerta Lim. Δ PdR in corso la ripresa attende il termine "
            "dell'allerta.") in _norm(_testo("vmc_master_scheda_manuale_interfaccia.txt"))
