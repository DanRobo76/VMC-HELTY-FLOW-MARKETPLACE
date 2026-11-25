"""Prove della 9.0.0b40.

Regola 5 (approvata il 23-11-2026): «Se la VMC torna leggibile a Velocità 1 dopo un'interruzione (velocità non
leggibile), senza un comando mandato, è ripartita: si rimanda l'ultima velocità.»

Classe del difetto: la VMC riparte da sola a Velocità 1 dopo un taglio della corrente che il Black-Out non rileva
(VMC OFF-Line per meno di 32 Secondi, oppure tornata mentre Home Assistant era spento o nel 1° minuto del
riallineamento al riavvio): nessuna spia del Black-Out, quindi nessun ripristino, e la VMC restava a Velocità 1.
Correzione: l'«Ultima Lettura Valida Stato Ventola» annota nell'attributo «lettura_prima_dell_interruzione» la
lettura di prima (codice e ora in cui era iniziata) quando la nuova lettura arriva dopo letture fallite o all'avvio
di Home Assistant; «VMC Master - Ripartenza della VMC» accende la spia del Black-Out di quella velocità (durante una
Fascia la Spia Black-Out del Calendario) e il ripristino del Black-Out già esistente la rimanda [Foglio Logiche A23].
La verifica dinamica completa (HA vero, VMC simulata che riparte a Velocità 1) è nel simulatore (famiglie OF, OSC, HB)."""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.template import Template
from homeassistant.setup import async_setup_component
from homeassistant.util import dt as dt_util
from homeassistant.util import yaml as hay

PKG = Path(__file__).resolve().parents[1] / "custom_components" / "vmc_master" / "package"
ALIAS = "VMC Master - Ripartenza della VMC"
RIPARTENZA = "automation.vmc_master_ripartenza_della_vmc"
GREZZA = "sensor.vmc_master_status_ventola"
MEMORIZZATA = "sensor.vmc_master_status_ventola_memorizzata"
RILEVATO = "binary_sensor.vmc_master_black_out_rilevato"
COMANDI = "input_text.vmc_master_ultimi_comandi_automazione"
SCELTA = "input_text.vmc_master_ultima_scelta_utente"
NON_ESEGUITO = "input_text.vmc_master_comando_non_eseguito"
SPIA_CAL_BO = "input_boolean.vmc_master_spia_calendario_black_out"
SPIA_CAL_NON_ESEGUITO = "input_boolean.vmc_master_spia_calendario_comando_non_eseguito"
NOMI_SPIE = ["0", "1", "2", "3", "4", "iperventilazione", "notturna", "freecooling"]
SPIE = [f"input_boolean.vmc_master_spia_velocita_{n}" for n in NOMI_SPIE]
SPIA_DEL_CODICE = {0: SPIE[0], 2: SPIE[2], 3: SPIE[3], 4: SPIE[4], 5: SPIE[5], 6: SPIE[6], 7: SPIE[7]}
GIORNI = ["lunedi", "martedi", "mercoledi", "giovedi", "venerdi", "sabato", "domenica"]
SPIE_FASCE = [f"input_boolean.vmc_master_spia_calendario_{g}_{f}" for g in GIORNI for f in (1, 2)]


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8").replace("\r\n", "\n")


@lru_cache
def _package() -> dict:
    return hay.load_yaml(str(PKG / "vmc_master.yaml"))


@lru_cache
def _automazione() -> dict:
    return hay.load_yaml(str(PKG / "vmc_master_automazione.txt"))


def _ripartenza() -> dict:
    return next(a for a in _package()["automation"] if a["alias"] == ALIAS)


def _blocco_memorizzata() -> dict:
    return next(b for b in _package()["template"]
                if any(s.get("unique_id") == "vmc_master_status_ventola_memorizzata" for s in b.get("sensor", [])))


# ------------------------------------------------------------------ struttura
def test_ripartenza_struttura() -> None:
    """Tre trigger (lettura valida memorizzata che cambia, Black-Out Rilevato che si spegne, avvio di Home Assistant),
    cinque condizioni con il loro alias, nessun comando mandato dall'automazione nuova: accende solo una spia."""
    auto = _ripartenza()
    assert auto["id"] == "vmc_master_ripartenza_della_vmc"
    assert auto["mode"] == "queued"
    assert auto["triggers"] == [
        {"trigger": "state", "entity_id": MEMORIZZATA, "not_to": ["unavailable", "unknown"]},
        {"trigger": "state", "entity_id": RILEVATO, "to": "off"},
        {"trigger": "homeassistant", "event": "start"},
    ]
    condizioni = auto["conditions"]
    assert len(condizioni) == 5 and all(c["condition"] == "template" and c["alias"] for c in condizioni)
    testo = str(auto["actions"])
    assert "shell_command" not in testo and "script." not in testo
    assert "input_number.vmc_master_attesa_blackout_ripristino" in condizioni[0]["value_template"]
    # nessuna costante di tempo nuova: solo il tempo di ripristino del Black-Out già esistente
    assert not re.search(r"\b(delay|for|timeout)\b", str(auto["actions"]) + str(auto["triggers"]))


def test_ripartenza_spie_e_ripristini_esistenti() -> None:
    """Ogni spia accesa ha il suo ripristino «Black-Out Off» nell'Automazione VMC Master (stessa spia, con la VMC
    ON-Line per il tempo di ripristino); con la Spia di una Fascia accesa (tutte le 14) si accende la Spia Black-Out
    del Calendario, che fa ripartire la Fascia."""
    fascia, fuori = _ripartenza()["actions"][0]["choose"]
    for spia in SPIE_FASCE:
        assert f"states('{spia}') == 'on'" in fascia["conditions"][0]["value_template"], spia
    assert fascia["sequence"] == [{"action": "input_boolean.turn_on", "target": {"entity_id": SPIA_CAL_BO}}]
    mappa = eval(re.search(r"\{\{ (\{.*\})\[codice_prima\] \}\}",  # noqa: S307
                           fuori["sequence"][0]["target"]["entity_id"]).group(1))
    assert mappa == SPIA_DEL_CODICE
    assert fuori["sequence"][0]["action"] == "input_boolean.turn_on"
    ripristini = [t for t in _automazione()["triggers"]
                  if t.get("trigger") == "template" and str(t.get("id", "")).startswith("Black-Out Off")]
    for spia in mappa.values():
        (trigger,) = [t for t in ripristini if f"states('{spia}') == \"on\"" in t["value_template"]]
        assert "ON-Line" in trigger["value_template"]
        assert "attesa_blackout_ripristino" in trigger["for"]["seconds"]
    ritorno = next(t for t in _automazione()["triggers"] if t.get("id") == "calendario_ritorno_da_black_out")
    assert f"states('{SPIA_CAL_BO}') == 'on'" in ritorno["value_template"]


def test_ripartenza_copie_gemelle() -> None:
    """Automazione nuova esclusa dal recorder, nello script e nel pannello «Pulisci cronologia», icona mdi:hvac;
    descrizione senza entity_id, IP, 'vmc_master_clona_' e «master» minuscolo; un solo alias."""
    pkg = _package()
    scheda = _testo("vmc_master_scheda_manuale_interfaccia.txt")
    pulizia = next(s for s in pkg["script"].values() if s.get("alias") == "VMC Master - Pulisci cronologia Entità")
    elenco = scheda[scheda.index("{%- set elenco = [") :]
    elenco = elenco[: elenco.index("] -%}")]
    assert RIPARTENZA in pkg["recorder"]["exclude"]["entities"]
    assert RIPARTENZA in pulizia["sequence"][0]["data"]["entity_id"]
    assert f"'{RIPARTENZA}'" in elenco
    assert pkg["homeassistant"]["customize"][RIPARTENZA]["icon"] == "mdi:hvac"
    descrizione = _ripartenza()["description"]
    assert not re.search(r"\b[a-z_]+\.vmc_[a-z0-9_]+", descrizione)
    assert "vmc_master_clona_" not in descrizione and not re.search(r"\d+\.\d+\.\d+\.\d+", descrizione)
    assert not re.search(r"\bmaster\b", descrizione)
    assert _testo("vmc_master.yaml").count(f'alias: "{ALIAS}"') == 1
    # la memorizzata resta esclusa dal recorder: l'attributo nuovo non scrive nel database
    assert MEMORIZZATA in pkg["recorder"]["exclude"]["entities"]


# ------------------------------------------------------------------ attributo della memorizzata
async def test_ripartenza_attributo_lettura_prima_dell_interruzione(hass: HomeAssistant) -> None:
    """«CODICE|ORA» della lettura di prima solo se la nuova lettura arriva dopo letture fallite (o senza stato
    precedente) o all'avvio di Home Assistant; vuoto se arriva da un'altra lettura valida o senza lettura di prima."""
    (sensore,) = _blocco_memorizzata()["sensor"]
    modello = Template(sensore["attributes"]["lettura_prima_dell_interruzione"], hass)
    hass.states.async_set(MEMORIZZATA, "VMGO,00003,00000")
    this = hass.states.get(MEMORIZZATA)
    inizio = round(this.last_changed.timestamp(), 1)

    class Stato:
        def __init__(self, s: str) -> None:
            self.state = s

    def valore(trigger: dict, stato=this) -> str:
        return modello.async_render({"trigger": trigger, "this": stato}, parse_result=False)

    for prima in ("unavailable", "unknown"):
        assert valore({"platform": "state", "from_state": Stato(prima)}) == f"00003|{inizio}"
    assert valore({"platform": "state", "from_state": None}) == f"00003|{inizio}"
    assert valore({"platform": "homeassistant"}) == f"00003|{inizio}"
    assert valore({"platform": "state", "from_state": Stato("VMGO,00003,00000")}) == ""
    hass.states.async_set(MEMORIZZATA, "unknown")
    assert valore({"platform": "homeassistant"}, hass.states.get(MEMORIZZATA)) == ""


# ------------------------------------------------------------------ automazione vera con la memorizzata vera
async def _prepara(hass: HomeAssistant, prima: str = "00003") -> None:
    """Memorizzata (template a trigger del package) e automazione nuova vere; aiutanti veri spenti o vuoti."""
    hass.states.async_set(GREZZA, f"VMGO,{prima},00000")
    hass.states.async_set(RILEVATO, "off")
    hass.states.async_set("sensor.vmc_master_status_ip_interfaccia", "ON-Line")
    booleani = {e.split(".", 1)[1]: {"initial": False} for e in SPIE + SPIE_FASCE + [SPIA_CAL_BO, SPIA_CAL_NON_ESEGUITO]}
    assert await async_setup_component(hass, "input_boolean", {"input_boolean": booleani})
    testi = {e.split(".", 1)[1]: {"initial": "", "max": 255} for e in (COMANDI, SCELTA, NON_ESEGUITO)}
    assert await async_setup_component(hass, "input_text", {"input_text": testi})
    assert await async_setup_component(hass, "input_number", {"input_number": {
        "vmc_master_attesa_blackout_ripristino": {"min": 0, "max": 600, "initial": 32}}})
    assert await async_setup_component(hass, "template", {"template": [_blocco_memorizzata()]})
    assert await async_setup_component(hass, "automation", {"automation": [_ripartenza()]})
    await hass.async_block_till_done()
    # prima lettura valida dopo il caricamento: la memorizzata parte dalla velocità «prima»
    hass.states.async_set(GREZZA, "unavailable")
    await hass.async_block_till_done()
    hass.states.async_set(GREZZA, f"VMGO,{prima},00001")
    await hass.async_block_till_done()
    assert hass.states.get(MEMORIZZATA).state.split(",")[1] == prima
    for spia in SPIE + [SPIA_CAL_BO]:  # la prima lettura (non Velocità 1) non accende niente
        assert hass.states.get(spia).state == "off"


async def _ripartita(hass: HomeAssistant) -> None:
    """La lettura fallisce e torna a Velocità 1."""
    hass.states.async_set(GREZZA, "unavailable")
    await hass.async_block_till_done()
    hass.states.async_set(GREZZA, "VMGO,00001,00000")
    await hass.async_block_till_done()


def _accese(hass: HomeAssistant) -> list[str]:
    return [e for e in SPIE + [SPIA_CAL_BO] if hass.states.get(e).state == "on"]


async def _imposta(hass: HomeAssistant, entita: str, valore: str) -> None:
    dominio = entita.split(".", 1)[0]
    if dominio == "input_text":
        await hass.services.async_call("input_text", "set_value", {"entity_id": entita, "value": valore}, blocking=True)
    else:
        await hass.services.async_call(dominio, f"turn_{valore}", {"entity_id": entita}, blocking=True)


@pytest.mark.parametrize(("codice", "spia"), sorted(SPIA_DEL_CODICE.items()))
async def test_ripartenza_rimanda_la_velocita_di_prima(hass: HomeAssistant, codice: int, spia: str) -> None:
    """Velocità 0, 2, 3, 4, Iperventilazione, Notturna, Free Cool./Heat. letta, lettura fallita, poi Velocità 1 senza
    comandi: si accende la spia del Black-Out di quella velocità (e nessun'altra)."""
    await _prepara(hass, f"0000{codice}")
    await _ripartita(hass)
    assert _accese(hass) == [spia]


async def test_ripartenza_non_scatta_da_velocita_1_o_da_lettura_valida(hass: HomeAssistant) -> None:
    """Già a Velocità 1 prima dell'interruzione: niente. Velocità 3 -> Velocità 1 tra due letture valide (Telecomando,
    App o comando): niente, è una scelta o un comando, non una ripartenza."""
    await _prepara(hass, "00001")
    await _ripartita(hass)
    assert _accese(hass) == []
    hass.states.async_set(GREZZA, "VMGO,00003,00000")
    await hass.async_block_till_done()
    hass.states.async_set(GREZZA, "VMGO,00001,00000")
    await hass.async_block_till_done()
    assert _accese(hass) == []


@pytest.mark.parametrize(("comandi", "scelta", "scatta"), [
    ({1: 1.0}, "", False),
    ({2: 1.0}, "", False),
    ({0: 1.0}, "", False),
    ({3: 1.0}, "", True),
    ({1: -100.0, 2: -50.0}, "", True),
    ({}, "00001|{t}|scheda", False),
    ({}, "00002|{t}|scheda", False),
    ({}, "00003|{t}|scheda", True),
    ({}, "00002|{t}|lettura", True),
])
async def test_ripartenza_nessun_comando_mandato(hass: HomeAssistant, comandi: dict[int, float], scelta: str,
                                                  scatta: bool) -> None:
    """Un comando dell'automazione o un tasto della finestra Telecomando di un'altra velocità (Velocità 1 compresa)
    dopo l'ultima lettura di prima blocca la regola: la Velocità 1 è stata chiesta, o un altro comando è ancora in
    viaggio e ha il suo ciclo. Un comando della stessa velocità di prima (un ritorno a Velocità 3 perso nel taglio) e i
    comandi più vecchi della lettura di prima non la bloccano; le scelte «lettura» (App) sono già letture valide."""
    await _prepara(hass)
    inizio = round(hass.states.get(MEMORIZZATA).last_changed.timestamp(), 1)  # ora della lettura di prima
    await _imposta(hass, COMANDI, "|".join(str(round(inizio + comandi[i], 1)) if i in comandi else "0" for i in range(8)))
    if scelta:
        await _imposta(hass, SCELTA, scelta.format(t=round(inizio + 1, 1)))
    await _ripartita(hass)
    assert _accese(hass) == ([SPIE[3]] if scatta else [])


@pytest.mark.parametrize(("entita", "valore"), [
    (SPIE[3], "on"), (SPIE[1], "on"), (SPIA_CAL_BO, "on"), (SPIA_CAL_NON_ESEGUITO, "on"),
    (NON_ESEGUITO, "00003|1000.0|Inquinanti"),
])
async def test_ripartenza_non_scatta_con_black_out_o_comando_non_eseguito(hass: HomeAssistant, entita: str,
                                                                         valore: str) -> None:
    """Black-Out già rilevato o ripristino in attesa (una spia accesa), Fascia già in ripartenza (Spia Black-Out del
    Calendario), Comando non eseguito in attesa: la regola non scatta, ci pensa il percorso già in corso."""
    await _prepara(hass)
    await _imposta(hass, entita, valore)
    prima = _accese(hass)
    await _ripartita(hass)
    assert _accese(hass) == prima


async def test_ripartenza_aspetta_la_fine_del_black_out_rilevato(hass: HomeAssistant, freezer) -> None:
    """Lettura a Velocità 1 con «Black-Out Rilevato» ancora acceso (VMC OFF-Line da 32 s ma rilevazione non avvenuta,
    per esempio nel 1° minuto dopo il riavvio): niente finché il Black-Out Rilevato si spegne; se si spegne entro il
    tempo di ripristino dalla lettura la regola scatta, dopo no (la lettura non è più recente)."""
    await _prepara(hass)
    hass.states.async_set(RILEVATO, "on")
    await _ripartita(hass)
    assert _accese(hass) == []
    freezer.tick(5)
    hass.states.async_set(RILEVATO, "off")
    await hass.async_block_till_done()
    assert _accese(hass) == [SPIE[3]]


async def test_ripartenza_black_out_rilevato_che_si_spegne_tardi(hass: HomeAssistant, freezer) -> None:
    """Black-Out Rilevato spento oltre il tempo di ripristino dopo la lettura a Velocità 1: niente."""
    await _prepara(hass)
    hass.states.async_set(RILEVATO, "on")
    await _ripartita(hass)
    freezer.tick(40)
    hass.states.async_set(RILEVATO, "off")
    await hass.async_block_till_done()
    assert _accese(hass) == []


@pytest.mark.parametrize("spia_fascia", [SPIE_FASCE[0], SPIE_FASCE[13]])
async def test_ripartenza_in_fascia_riparte_la_fascia(hass: HomeAssistant, spia_fascia: str) -> None:
    """Con la Spia di una Fascia accesa si accende la Spia Black-Out del Calendario (la Fascia riparte), non la spia
    della velocità, come per un Black-Out durante una Fascia [Foglio Logiche A23]."""
    await _prepara(hass)
    await _imposta(hass, spia_fascia, "on")
    await _ripartita(hass)
    assert _accese(hass) == [SPIA_CAL_BO]


async def test_ripartenza_all_avvio_di_home_assistant(hass: HomeAssistant) -> None:
    """All'avvio la memorizzata ripristinata (Velocità 3) passa alla lettura vera (Velocità 1) con il trigger
    «homeassistant start»: l'attributo segna l'interruzione e l'automazione, valutata all'avvio, accende la spia."""
    await _prepara(hass)
    (sensore,) = _blocco_memorizzata()["sensor"]
    this = hass.states.get(MEMORIZZATA)
    valore = Template(sensore["attributes"]["lettura_prima_dell_interruzione"], hass).async_render(
        {"trigger": {"platform": "homeassistant"}, "this": this}, parse_result=False)
    assert valore.startswith("00003|")
    hass.states.async_set(MEMORIZZATA, "VMGO,00001,00000", {"lettura_prima_dell_interruzione": valore})
    await hass.async_block_till_done()  # il trigger di stato scatta qui; all'avvio vero lo fa «homeassistant start»
    assert _accese(hass) == [SPIE[3]]
    await _imposta(hass, SPIE[3], "off")
    await hass.services.async_call("automation", "trigger", {"entity_id": RIPARTENZA, "skip_condition": False},
                                   blocking=True)
    await hass.async_block_till_done()
    assert _accese(hass) == [SPIE[3]]
