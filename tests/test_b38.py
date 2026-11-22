"""Prove della 9.0.0b38: velocità scelta dall'utente persa per i tempi di lettura o di esecuzione della VMC.

Classe del difetto (segnalazione del 22-11-2026: Velocità 0 premuta negli ultimi secondi dei 16 Secondi del Lim. Δ PdR,
VMC ferma ma «Velocità Registrata» Velocità 2): Home Assistant legge la velocità ogni 5 Secondi, quindi allo scadere di
un'attesa (trigger template con «for») la guardia «Evento ancora valido» poteva rivalutare il trigger con una lettura
vecchia. Correzioni:
- A: prima della guardia la velocità si rilegge; se l'ultimo comando mandato alla VMC (tasto della scheda o del
  Telecomando, o comando dell'automazione) non è ancora stato letto dopo l'invio si rilegge ogni 2 Secondi finché la VMC
  lo esegue (al massimo 12 Secondi dall'invio);
- B: «VMC Master - Registro Comandi e Scelte» annota le scelte dell'utente, l'ora dei comandi dell'automazione e l'ora
  in cui la lettura passa a ogni velocità;
- C: «VMC Master - Rimando della Scelta» rimanda la scelta cancellata da un comando dell'automazione in viaggio.
La verifica dinamica (HA vero, VMC simulata veloce e lenta) è nel simulatore (famiglia R e famiglie W/V)."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

from homeassistant.core import HomeAssistant
from homeassistant.helpers.template import Template, result_as_boolean
from homeassistant.util import dt as dt_util
from homeassistant.util import yaml as hay

PKG = Path(__file__).resolve().parents[1] / "custom_components" / "vmc_master" / "package"
GREZZA = "sensor.vmc_master_status_ventola"
SCELTA = "input_text.vmc_master_ultima_scelta_utente"
COMANDI = "input_text.vmc_master_ultimi_comandi_automazione"
LETTURE = "input_text.vmc_master_ultime_letture_velocita"
REGISTRO = "automation.vmc_master_registro_comandi_e_scelte"
RIMANDO = "automation.vmc_master_rimando_della_scelta"
CODICI = ["00000", "00001", "00002", "00003", "00004", "00005", "00006", "00007"]


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8").replace("\r\n", "\n")


@lru_cache
def _automazione() -> dict:
    return hay.load_yaml(str(PKG / "vmc_master_automazione.txt"))


@lru_cache
def _package() -> dict:
    return hay.load_yaml(str(PKG / "vmc_master.yaml"))


def _auto(alias: str) -> dict:
    return next(a for a in _package()["automation"] if a["alias"] == alias)


@lru_cache
def _servizi_velocita() -> dict[str, int]:
    """Tutti gli shell_command che mandano una velocità alla VMC (VMWH000000<n>) con il loro codice n."""
    servizi = {}
    for nome, comando in _package()["shell_command"].items():
        trovato = re.search(r"VMWH000000(\d)\\n", str(comando))
        if trovato:
            servizi[nome] = int(trovato.group(1))
    return servizi


# ------------------------------------------------------------------ versioni
def test_versioni_b38() -> None:
    """Automazione, scheda e manifest cambiano nella b38; gli script .sh no."""
    assert "AUTOMAZIONE VMC HELTY FLOW PLUS RELEASE [VER. 9.0.0b38]" in _testo("vmc_master_automazione.txt")[:1000]
    assert "SCHEDA MANUALE INTERFACCIA VMC HELTY FLOW PLUS RELEASE [VER. 9.0.0b38]" in _testo(
        "vmc_master_scheda_manuale_interfaccia.txt")[:2000]
    manifest = json.loads((PKG.parent / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["version"] == "9.0.0b38"
    assert "RELEASE [VER. 9.0.0b31]" in _testo("vmc_master_script_cambio_ip.sh")[:1000]
    assert "RELEASE [VER. 9.0.0b32]" in _testo("vmc_master_script_cambio_nome.sh")[:1000]


# ------------------------------------------------------------------ A: rilettura prima della guardia (tutta la classe)
def test_rilettura_prima_della_guardia_per_tutte_le_attese() -> None:
    """La rilettura è la prima azione e vale per OGNI trigger template con «for» (132, di cui 122 sulla velocità):
    la condizione non elenca trigger, quindi un'attesa nuova è coperta senza modifiche; subito dopo c'è la guardia."""
    azioni = _automazione()["actions"]
    rilettura, guardia = azioni[0], azioni[1]
    assert rilettura["alias"].startswith("Rilettura della velocità allo scadere di un'attesa")
    assert guardia["alias"].startswith("Evento ancora valido")
    condizione = rilettura["if"][0]["value_template"]
    assert "trigger.platform == 'template' and trigger.for is not none" in condizione
    assert "trigger.id" not in condizione
    assert "ON-Line" in condizione
    passi = rilettura["then"]
    assert passi[0]["action"] == "homeassistant.update_entity" and passi[0]["target"]["entity_id"] == GREZZA
    ciclo = passi[1]["repeat"]
    attesa = ciclo["while"][0]["value_template"]
    for pezzo in ("repeat.index <= 6", "scelta[2] == 'scheda'", "< 12", SCELTA, COMANDI, LETTURE,
                  "('0000' ~ ns.i) != letta", "r[ns.i] < ns.ts"):
        assert pezzo in attesa, pezzo
    assert ciclo["sequence"][0]["delay"]["seconds"] == 2
    assert ciclo["sequence"][1]["action"] == "homeassistant.update_entity"
    assert "sensor.vmc_master_status_ventola_memorizzata" in passi[2]["wait_template"]
    assert passi[2]["timeout"]["seconds"] == 2 and passi[2]["continue_on_timeout"] is True
    # ogni trigger template con «for» ha la sua copia nella guardia, che la rilettura precede
    con_for = [t for t in _automazione()["triggers"] if t.get("trigger") == "template" and "for" in t]
    assert len(con_for) == 132
    assert sum("status_ventola_lettura_codice_interpretato" in t["value_template"] for t in con_for) == 122
    for t in con_for:
        assert f"trigger.id == '{t['id']}'" in guardia["value_template"], t["id"]


# ------------------------------------------------------------------ B: registro dei comandi e delle scelte
def test_registro_copre_tutti_i_comandi_di_velocita() -> None:
    """Un trigger per OGNI shell_command di velocità (VMWH000000<n>), con il codice giusto nella mappa."""
    servizi = _servizi_velocita()
    assert sorted(servizi.values()) == list(range(8))
    registro = _auto("VMC Master - Registro Comandi e Scelte")
    assert registro["mode"] == "queued"
    eventi = [t for t in registro["triggers"] if t["trigger"] == "event"]
    assert sorted(t["event_data"]["service"] for t in eventi) == sorted(servizi)
    assert all(t["event_type"] == "call_service" and t["event_data"]["domain"] == "shell_command"
               and t["id"] == "comando" for t in eventi)
    (lettura,) = [t for t in registro["triggers"] if t["trigger"] == "state"]
    assert lettura["entity_id"] == GREZZA and lettura["id"] == "lettura"
    assert lettura["not_from"] == ["unavailable", "unknown"] and lettura["not_to"] == ["unavailable", "unknown"]
    mappa = eval(re.search(r"\{\{ (\{.*\}) \}\}", registro["variables"]["codici"]).group(1))  # noqa: S307
    assert mappa == servizi


def test_rimando_usa_gli_stessi_servizi() -> None:
    """Il servizio rimandato per il codice n è lo shell_command che manda VMWH000000<n>."""
    rimando = _auto("VMC Master - Rimando della Scelta")
    assert rimando["mode"] == "restart"
    assert rimando["triggers"] == [{"trigger": "state", "entity_id": SCELTA}]
    elenco = eval(re.search(r"\{\{ (\[.*\]) \}\}", rimando["variables"]["servizi"]).group(1))  # noqa: S307
    assert [_servizi_velocita()[s.split(".", 1)[1]] for s in elenco] == list(range(8))
    ciclo = rimando["actions"][-1]["repeat"]
    assert ciclo["sequence"][0]["action"] == "{{ servizi[indice] }}"
    fine = ciclo["until"][0]["value_template"]
    for pezzo in ("== codice", "binary_sensor.vmc_master_black_out_rilevato", "ON-Line", "ns.nuovo",
                  "repeat.index >= 5"):
        assert pezzo in fine, pezzo


def test_nuove_entita_nelle_copie_gemelle() -> None:
    """Helper e automazioni nuove: esclusi dal recorder, nello script e nel pannello «Pulisci cronologia», icona
    mdi:hvac per le automazioni; descrizioni senza entity_id, IP, 'vmc_master_clona_' e «master» minuscolo."""
    pkg = _package()
    testo = _testo("vmc_master.yaml")
    scheda = _testo("vmc_master_scheda_manuale_interfaccia.txt")
    escluse = pkg["recorder"]["exclude"]["entities"]
    pulizia = next(s for s in pkg["script"].values() if s.get("alias") == "VMC Master - Pulisci cronologia Entità")
    da_pulire = pulizia["sequence"][0]["data"]["entity_id"]
    elenco = scheda[scheda.index("{%- set elenco = [") :]
    elenco = elenco[: elenco.index("] -%}")]
    for entita in (SCELTA, COMANDI, LETTURE, REGISTRO, RIMANDO):
        assert entita in escluse and entita in da_pulire and f"'{entita}'" in elenco, entita
    for nome in ("vmc_master_ultima_scelta_utente", "vmc_master_ultimi_comandi_automazione",
                 "vmc_master_ultime_letture_velocita"):
        helper = pkg["input_text"][nome]
        assert helper["initial"] == "" and helper["max"] == 255
    for entita in (REGISTRO, RIMANDO):
        assert pkg["homeassistant"]["customize"][entita]["icon"] == "mdi:hvac"
    for alias in ("VMC Master - Registro Comandi e Scelte", "VMC Master - Rimando della Scelta"):
        descrizione = _auto(alias)["description"]
        assert not re.search(r"\b[a-z_]+\.vmc_[a-z0-9_]+", descrizione), alias
        assert "vmc_master_clona_" not in descrizione and not re.search(r"\d+\.\d+\.\d+\.\d+", descrizione)
        assert not re.search(r"\bmaster\b", descrizione), alias
    assert testo.count('alias: "VMC Master - Registro Comandi e Scelte"') == 1
    assert testo.count('alias: "VMC Master - Rimando della Scelta"') == 1


# ------------------------------------------------------------------ B e C: le regole dei template
async def test_registro_scelta_dall_app(hass: HomeAssistant) -> None:
    """Una lettura che cambia è una scelta dall'App solo senza un comando dell'automazione con quella velocità negli
    ultimi 20 Secondi e senza un tasto della scheda con quella velocità negli ultimi 20 Secondi."""
    registro = _auto("VMC Master - Registro Comandi e Scelte")
    condizione = Template(registro["actions"][1]["choose"][2]["conditions"][0]["value_template"], hass)

    class Stato:
        def __init__(self, s: str) -> None:
            self.state = s

    def scelta_app(da: str, a: str, comandi: list[float], scelta: list[str]) -> bool:
        trigger = {"id": "lettura", "from_state": Stato(f"VMGH,{da},0"), "to_state": Stato(f"VMGH,{a},0")}
        return result_as_boolean(
            condizione.async_render({"trigger": trigger, "ora": 1000.0, "comandi": comandi, "scelta": scelta}))

    zero = [0.0] * 8
    assert scelta_app("00002", "00004", zero, ["", "0", ""]) is True
    assert scelta_app("00002", "00002", zero, ["", "0", ""]) is False  # codice uguale
    comandi = list(zero)
    comandi[4] = 985.0  # comando dell'automazione di Velocità 4 15 s prima: è il suo comando
    assert scelta_app("00002", "00004", comandi, ["", "0", ""]) is False
    comandi[4] = 980.0  # 20 s prima: non è più il suo
    assert scelta_app("00002", "00004", comandi, ["", "0", ""]) is True
    assert scelta_app("00002", "00004", zero, ["00004", "990.0", "scheda"]) is False  # tasto della scheda già annotato
    assert scelta_app("00002", "00004", zero, ["00004", "990.0", "lettura"]) is True


async def test_rimando_comandi_in_viaggio(hass: HomeAssistant) -> None:
    """In viaggio: comandi dell'automazione con un'altra velocità mandati fino a 8 s prima della scelta dalla scheda
    (13 s prima della lettura per l'App), non dopo la scelta."""
    rimando = _auto("VMC Master - Rimando della Scelta")
    modello = Template(rimando["variables"]["in_viaggio"], hass)

    class Stato:
        def __init__(self, s: str) -> None:
            self.state = s

    def in_viaggio(comandi: list[float], scelta: str) -> list[int]:
        hass.states.async_set(COMANDI, "|".join(str(c) for c in comandi))
        codice, ts, _ = scelta.split("|")
        return modello.async_render({"trigger": {"to_state": Stato(scelta)}, "indice": int(codice),
                                     "ts_scelta": float(ts)})

    comandi = [0.0] * 8
    comandi[2] = 995.0
    assert in_viaggio(comandi, "00004|1000.0|scheda") == [2]
    assert in_viaggio(comandi, "00002|1000.0|scheda") == []  # stessa velocità della scelta
    comandi[2] = 991.0
    assert in_viaggio(comandi, "00004|1000.0|scheda") == []  # 9 s prima: già eseguito
    assert in_viaggio(comandi, "00004|1000.0|lettura") == [2]  # App: fino a 13 s prima della lettura
    comandi[2] = 1001.0
    assert in_viaggio(comandi, "00004|1000.0|scheda") == []  # mandato dopo la scelta: decisione dell'automazione


async def test_rilettura_aspetta_solo_un_comando_in_viaggio(hass: HomeAssistant) -> None:
    """Si aspetta solo se l'ultimo comando (dell'automazione o un tasto della scheda) è diverso dalla lettura, mandato da
    meno di 12 s e non ancora letto dopo l'invio; un comando già letto e poi cambiato dall'App non fa aspettare."""
    attesa = Template(_automazione()["actions"][0]["then"][1]["repeat"]["while"][0]["value_template"], hass)
    ora = dt_util.utcnow().timestamp()

    def aspetta(lettura: str, comandi: dict[int, float], letture: dict[int, float], scelta: str = "") -> bool:
        hass.states.async_set("sensor.vmc_master_status_ip_interfaccia", "ON-Line")
        hass.states.async_set(GREZZA, f"VMGH,{lettura},0")
        hass.states.async_set(COMANDI, "|".join(str(comandi.get(i, 0.0)) for i in range(8)))
        hass.states.async_set(LETTURE, "|".join(str(letture.get(i, 0.0)) for i in range(8)))
        hass.states.async_set(SCELTA, scelta)
        return result_as_boolean(attesa.async_render({"repeat": {"index": 1}}))

    assert aspetta("00002", {4: ora - 5}, {2: ora - 30, 4: ora - 60}) is True  # V4 in viaggio da 5 s
    assert aspetta("00004", {4: ora - 5}, {4: ora - 1}) is False  # già eseguito
    assert aspetta("00002", {4: ora - 5}, {4: ora - 4}) is False  # eseguito e poi cambiato dall'App
    assert aspetta("00002", {4: ora - 13}, {}) is False  # oltre 12 s dall'invio
    assert aspetta("00002", {}, {}, f"00000|{ora - 2}|scheda") is True  # tasto della scheda in viaggio
    assert aspetta("00002", {}, {}, f"00000|{ora - 2}|lettura") is False  # scelta dall'App: già eseguita
    assert aspetta("00002", {4: ora - 1}, {}, f"00000|{ora - 2}|scheda") is True  # l'ultimo è il comando V4
    hass.states.async_set("sensor.vmc_master_status_ip_interfaccia", "OFF-Line")
    assert result_as_boolean(attesa.async_render({"repeat": {"index": 1}})) is False


async def test_registro_ora_delle_letture(hass: HomeAssistant) -> None:
    """Ogni cambio della lettura annota l'ora per la nuova velocità."""
    registro = _auto("VMC Master - Registro Comandi e Scelte")
    passo = registro["actions"][0]
    condizione = Template(passo["if"][0]["value_template"], hass)
    valore = Template(passo["then"][0]["data"]["value"], hass)

    class Stato:
        def __init__(self, s: str) -> None:
            self.state = s

    trigger = {"id": "lettura", "from_state": Stato("VMGH,00002,0"), "to_state": Stato("VMGH,00004,0")}
    assert result_as_boolean(condizione.async_render({"trigger": trigger})) is True
    assert valore.async_render({"trigger": trigger, "ora": 1000.5, "letture": [1.0] * 8},
                               parse_result=False) == "1.0|1.0|1.0|1.0|1000.5|1.0|1.0|1.0"
    uguale = {"id": "lettura", "from_state": Stato("VMGH,00004,1"), "to_state": Stato("VMGH,00004,0")}
    assert result_as_boolean(condizione.async_render({"trigger": uguale})) is False
