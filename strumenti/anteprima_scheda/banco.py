"""Anteprima della scheda «VMC Master»: oggi (package) e tradotta (entità native), affiancate.

Avvio, dalla radice del worktree, in primo piano:

    timeout 600 /home/user/hav/bin/python strumenti/anteprima_scheda/banco.py

Prepara ``anteprima/ha`` (cartella di configurazione nuova a ogni avvio) e avvia Home Assistant
in questo processo (solo 127.0.0.1, porta 8471) con:

- gli aiutanti del package di oggi presi tali e quali da ``vmc_master.yaml`` (input_*, timer);
  gli script come segnaposto (stesso nome, icona, modo e campi: lanciano solo l'evento
  ``vmc_anteprima_script``) e i comandi di shell come segnaposto (``true``);
- i sostituti delle entità native (``sostituti_vmc``) con gli entity_id di domani;
- sensori, sensori binari e automazioni come nello stato del simulatore (stati_package.json);
- due plance YAML: ``scheda-oggi`` (la scheda che l'integrazione serve oggi) e
  ``scheda-nativa`` (``scheda_nativa.txt``, passata da per_vmc come oggi).

Poi controlla che i sostituti abbiano gli stati e gli attributi «di domani» (nativi.py),
porta Home Assistant in ogni scena, fa fotografare a ``scatta.js`` le due plance e le confronta
pixel per pixel; prova due tocchi veri nel browser e infine ogni azione della scheda tradotta
contro quella di oggi (stesso effetto sugli aiutanti, sugli script e sui comandi di shell).
Risultati in ``anteprima/risultati.json`` (immagini in ``anteprima/scene``).
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from collections import Counter
from collections.abc import Iterator, Mapping
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import unquote

import numpy as np
import yaml
from PIL import Image

Image.MAX_IMAGE_PIXELS = None  # le schede aperte sono alte decine di migliaia di pixel

RADICE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RADICE))

from custom_components.vmc_master.installatore import genera_file
from custom_components.vmc_master.trasforma import (
    adatta_link_repository,
    per_vmc,
)
from tests.nativa.scheda import nativi
from tests.nativa.scheda.traduci_scheda import (
    FASE_1,
    SCHEDA,
    TESTI,
    USCITA,
    _leggi_csv,
    mappa_fase_1,
)

QUI = Path(__file__).resolve().parent
ANTEPRIMA = RADICE / "anteprima"
CONFIG = ANTEPRIMA / "ha"
SCENE_DIR = ANTEPRIMA / "scene"
# Le immagini della scheda puntano al repository su GitHub, irraggiungibile da qui: scatta.js
# le serve dalla cartella IMMAGINI, dove si estraggono dal repository locale (sola lettura)
IMMAGINI = ANTEPRIMA / "immagini"
REPOSITORY_IMMAGINI = Path("/home/user/vmc-helty-flow-marketplace")
VERSIONE_IMMAGINI = "origin/main"
INDIRIZZO_IMMAGINI = (
    "https://raw.githubusercontent.com/DanRobo76/VMC-HELTY-FLOW-MARKETPLACE/main/"
)
PORTA = 8471
BASE = f"http://127.0.0.1:{PORTA}"
UTENTE, PAROLA = "prova", "prova12345"
NOME, IP, VERSIONE = "master", "192.168.1.160", "9.0.0b42"
# Ora del simulatore nello stato al fork (stessa ora dei test dei modelli)
ORA_ISTANTANEA = datetime.fromisoformat("2026-01-15T09:05:00+00:00")
# I timer delle scene partono con 600 s in più: restano attivi per tutta la scena e il
# browser, con l'orologio fermo a partenza + 600 s - 0,5 s, mostra proprio i secondi voluti
MARGINE = 600
AIUTANTI = (
    "input_boolean",
    "input_number",
    "input_select",
    "input_text",
    "input_datetime",
)
EVENTO_SCRIPT = "vmc_anteprima_script"


# ---------------------------------------------------------------------------------- scene
@dataclass
class Scena:
    """Una situazione della scheda: interruttori accesi, timer attivi (secondi alla fine),
    numeri e sensori cambiati rispetto allo stato di base, riquadri <details> da aprire."""

    nome: str
    accesi: tuple[str, ...] = ()
    timer: Mapping[str, int] = field(default_factory=dict)
    numeri: Mapping[str, float] = field(default_factory=dict)
    sensori: Mapping[str, str] = field(default_factory=dict)
    apri: bool = False


# Il titolo di ogni scena, per chi guarda le fotografie
TITOLI = {
    "01_principale": "Vista principale",
    "02_principale_led_blu_velocita_2": "Vista principale con LED blu e Velocità 2",
    "03_telecomando": "Telecomando",
    "04_sensori": "Sensori",
    "05_prossime_letture": "Sensori con le prossime letture",
    "06_calendario": "Calendario",
    "07_opzioni": "Opzioni, con i conti alla rovescia dei pulsanti",
    "08_opzioni_scelta_sensori": "Opzioni - Scelta dei sensori",
    "09_opzioni_elementi_chimici": "Opzioni - Elementi chimici",
    "10_opzioni_punto_di_rugiada": "Opzioni - Punto di rugiada",
    "11_opzioni_calendario": "Opzioni - Calendario",
    "12_opzioni_free_heating_cooling": "Opzioni - Free Heating / Free Cooling",
    "13_audio": "Opzioni - Audio",
    "14_pulisci_cronologia": "Opzioni - Pulisci cronologia",
    "15_avvisi": "Avvisi",
    "16_avvisi_grafici": "Avvisi con i grafici",
    "17_informazioni": "Informazioni, con tutte le voci aperte",
    "18_riallineamento_1_attesa": "Riallineamento dopo il riavvio: 1° gruppo in attesa",
    "19_riallineamento_1_fermo": "Riallineamento dopo il riavvio: 1° gruppo fermo",
    "20_riallineamento_2_attesa": "Riallineamento dopo il riavvio: 2° gruppo in attesa",
    "21_riallineamento_3_fermo": "Riallineamento dopo il riavvio: 3° gruppo fermo",
    "22_riallineamento_4": "Riallineamento dopo il riavvio completato",
    "23_tempi_attesa": "Tempi di attesa",
    "24_tutti_i_timer": "Tutti i conti alla rovescia in corso",
    "25_tutti_i_timer_prossime_letture": (
        "Tutti i conti alla rovescia in corso, con le prossime letture"
    ),
}

_OPZ = "opzioni_offset_sensori"
_TIMER_SCRIPT = {
    "countdown_script_agg_sensori": 95,
    "countdown_script_panic_button": 47,
    "countdown_script_inizializzazione": 125,
    "countdown_script_reset_filtro": 33,
}
SCENE = (
    Scena("01_principale"),
    Scena(
        "02_principale_led_blu_velocita_2",
        sensori={
            "sensor.vmc_master_stato_led_interfaccia": "blu",
            "sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia": (
                "Velocità 2"
            ),
        },
    ),
    Scena("03_telecomando", accesi=("opzioni_vmc",)),
    Scena("04_sensori", accesi=("opzioni_monitoraggio_sensori",)),
    Scena(
        "05_prossime_letture",
        accesi=("opzioni_monitoraggio_sensori", "opzione_finestra_prossime_letture"),
    ),
    Scena("06_calendario", accesi=("opzioni_interruttore_calendario",)),
    Scena("07_opzioni", accesi=(_OPZ,), timer=_TIMER_SCRIPT),
    Scena("08_opzioni_scelta_sensori", accesi=(_OPZ, "opzioni_scelta_sensori")),
    Scena("09_opzioni_elementi_chimici", accesi=(_OPZ, "opzioni_elementi_chimici")),
    Scena("10_opzioni_punto_di_rugiada", accesi=(_OPZ, "opzioni_punto_di_rugiada")),
    Scena(
        "11_opzioni_calendario",
        accesi=(_OPZ, "opzioni_calendario_main", "opzioni_calendario"),
    ),
    Scena(
        "12_opzioni_free_heating_cooling",
        accesi=(_OPZ, "opzioni_free_heating_o_free_cooling"),
    ),
    Scena("13_audio", accesi=(_OPZ, "opzione_finestra_audio")),
    Scena(
        "14_pulisci_cronologia", accesi=(_OPZ, "conferma_pulizia_cronologia"), apri=True
    ),
    Scena("15_avvisi", accesi=("opzioni_avvisi",)),
    Scena("16_avvisi_grafici", accesi=("opzioni_avvisi", "opzioni_avvisi_grafici")),
    Scena("17_informazioni", accesi=("opzioni_lettura_sensori",), apri=True),
    Scena(
        "18_riallineamento_1_attesa",
        numeri={"fase_riallineamento_al_riavvio": 1.0},
        timer={"countdown_avvio_home_assistant": 75},
    ),
    Scena("19_riallineamento_1_fermo", numeri={"fase_riallineamento_al_riavvio": 1.0}),
    Scena(
        "20_riallineamento_2_attesa",
        numeri={"fase_riallineamento_al_riavvio": 2.0},
        timer={"countdown_fase_allerte": 52},
    ),
    Scena("21_riallineamento_3_fermo", numeri={"fase_riallineamento_al_riavvio": 3.0}),
    Scena("22_riallineamento_4", numeri={"fase_riallineamento_al_riavvio": 4.0}),
    Scena("23_tempi_attesa", accesi=("opzione_finestra_tempi_attesa",)),
    Scena("24_tutti_i_timer", timer={"*": 0}),
    Scena(
        "25_tutti_i_timer_prossime_letture",
        accesi=("opzioni_monitoraggio_sensori", "opzione_finestra_prossime_letture"),
        timer={"*": 0},
    ),
)


# ------------------------------------------------------------------------ configurazione
def config_scheda(testo: str) -> Any:
    """La configurazione della scheda come la serve l'integrazione (VmcSchedaView)."""
    return yaml.safe_load(adatta_link_repository(per_vmc(testo, NOME, IP)))


def _leggi_testo(percorso: Path) -> str:
    with percorso.open(encoding="utf-8", newline="") as flusso:
        return flusso.read()


CONFIGURAZIONE = f"""\
homeassistant:
  name: Anteprima scheda VMC
  time_zone: Europe/Rome
  language: it
  country: IT
  currency: EUR
  unit_system: metric
  latitude: 45.4642
  longitude: 9.19
  elevation: 120
  packages: !include_dir_named packages
frontend:
  extra_module_url:
    - /local/vmc-master-card.js?v=anteprima
http:
  server_host: 127.0.0.1
  server_port: {PORTA}
api:
websocket_api:
lovelace:
  dashboards:
    scheda-oggi:
      mode: yaml
      filename: scheda_oggi.yaml
      title: Scheda di oggi
      icon: mdi:fan
      show_in_sidebar: true
    scheda-nativa:
      mode: yaml
      filename: scheda_nativa.yaml
      title: Scheda nativa
      icon: mdi:fan-auto
      show_in_sidebar: true
recorder:
  commit_interval: 0
history:
sostituti_vmc:
logger:
  default: warning
"""


def aiutanti_di_oggi() -> dict[str, Any]:
    """Il package di oggi ridotto agli aiutanti (tali e quali) e ai segnaposto di script e
    comandi di shell."""
    package = yaml.safe_load(genera_file(NOME, IP, VERSIONE)[f"vmc_{NOME}.yaml"])
    uscita: dict[str, Any] = {
        dominio: package[dominio] for dominio in (*AIUTANTI, "timer")
    }
    uscita["script"] = {
        nome: {
            **{
                k: v
                for k, v in script.items()
                if k in ("alias", "icon", "mode", "max", "fields", "description")
            },
            "sequence": [{"event": EVENTO_SCRIPT, "event_data": {"script": nome}}],
        }
        for nome, script in package["script"].items()
    }
    uscita["shell_command"] = dict.fromkeys(package["shell_command"], "true")
    return uscita


def voci_sostituti(mappa: Mapping[str, str | None]) -> list[dict[str, Any]]:
    """Un sostituto per ogni entità di oggi che domani ha un altro entity_id."""
    nomi = {r["Entità oggi"]: r["Nome"] for r in _leggi_csv(FASE_1)}
    voci = []
    for vecchia, nuova in mappa.items():
        if nuova is None or nuova == vecchia:
            continue
        oggetto = vecchia.split(".", 1)[1]
        voci.append(
            {
                "vecchia": vecchia,
                "nuova": nuova,
                "nome": nomi.get(vecchia) or oggetto.replace("_", " ").capitalize(),
            }
        )
    return voci


def prepara_cartella(mappa: Mapping[str, str | None]) -> tuple[Any, Any, list[dict]]:
    """Scrive la cartella di configurazione; restituisce le due schede e i sostituti."""
    shutil.rmtree(CONFIG, ignore_errors=True)
    (CONFIG / "packages").mkdir(parents=True)
    (CONFIG / "www").mkdir()
    (CONFIG / ".storage").mkdir()
    shutil.copytree(
        QUI / "sostituti_vmc",
        CONFIG / "custom_components/sostituti_vmc",
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    shutil.copy(
        RADICE / "custom_components/vmc_master/frontend/vmc-master-card.js",
        CONFIG / "www/vmc-master-card.js",
    )
    (CONFIG / "configuration.yaml").write_text(CONFIGURAZIONE, encoding="utf-8")
    (CONFIG / ".storage/onboarding").write_text(
        json.dumps(
            {
                "version": 4,
                "minor_version": 1,
                "key": "onboarding",
                "data": {"done": ["user", "core_config", "analytics", "integration"]},
            }
        ),
        encoding="utf-8",
    )
    (CONFIG / "packages/aiutanti_oggi.yaml").write_text(
        yaml.safe_dump(aiutanti_di_oggi(), allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    oggi = config_scheda(_leggi_testo(SCHEDA))
    nativa = config_scheda(_leggi_testo(USCITA))
    for nome, scheda in (("scheda_oggi", oggi), ("scheda_nativa", nativa)):
        plancia = {
            "title": nome,
            "views": [{"title": "VMC", "path": "vmc", "cards": [scheda]}],
        }
        (CONFIG / f"{nome}.yaml").write_text(
            yaml.safe_dump(plancia, allow_unicode=True, sort_keys=False, width=10**6),
            encoding="utf-8",
        )
    voci = voci_sostituti(mappa)
    (CONFIG / "sostituti_vmc.json").write_text(
        json.dumps({"voci": voci, "mappa": dict(mappa)}, ensure_ascii=False, indent=1),
        encoding="utf-8",
    )
    return oggi, nativa, voci


def indirizzi_immagini(config: Any) -> set[str]:
    """I percorsi nel repository delle immagini nominate dalla scheda (senza ?v=...)."""
    trovati: set[str] = set()
    modello = re.compile(
        re.escape(INDIRIZZO_IMMAGINI) + r"([^\"'?<>\s]+?\.(?:png|webp|jpe?g|gif|svg))"
    )

    def visita(nodo: Any) -> None:
        if isinstance(nodo, dict):
            for valore in nodo.values():
                visita(valore)
        elif isinstance(nodo, list):
            for valore in nodo:
                visita(valore)
        elif isinstance(nodo, str):
            trovati.update(unquote(m.group(1)) for m in modello.finditer(nodo))

    visita(config)
    return trovati


def prepara_immagini(*schede: Any) -> dict[str, Any]:
    """Estrae in IMMAGINI le immagini delle schede dal repository locale."""
    shutil.rmtree(IMMAGINI, ignore_errors=True)
    percorsi = sorted(set().union(*(indirizzi_immagini(s) for s in schede)))
    mancanti = []
    for percorso in percorsi:
        esito = subprocess.run(
            [
                "git",
                "-C",
                str(REPOSITORY_IMMAGINI),
                "cat-file",
                "blob",
                f"{VERSIONE_IMMAGINI}:{percorso}",
            ],
            capture_output=True,
            check=False,
        )
        if esito.returncode:
            mancanti.append(percorso)
            continue
        file = IMMAGINI / percorso
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_bytes(esito.stdout)
    return {
        "repository": f"{REPOSITORY_IMMAGINI} {VERSIONE_IMMAGINI}",
        "nominate": len(percorsi),
        "mancanti": mancanti,
    }


def sorgente_testo(testo: str) -> str:
    """Un testo di TESTI come lo mostra il browser (senza tag HTML), come espressione
    regolare per scatta.js; un'etichetta fra apici (tabella dei tipi di «Pulisci
    cronologia») è seguita dal suo numero."""
    etichetta = len(testo) > 1 and testo[0] == testo[-1] == "'"
    piano = re.sub(r"<[^>]+>", "", testo.strip("'") if etichetta else testo)
    return re.escape(piano) + (r"(?=\d)" if etichetta else "")


def prepara_testi_cercati() -> Path:
    """Il file con i testi aggiornati da cercare nelle due pagine (per la galleria)."""
    file = ANTEPRIMA / "testi_cercati.json"
    file.write_text(
        json.dumps(
            {
                "oggi": [sorgente_testo(t.prima) for t in TESTI],
                "nativa": [sorgente_testo(t.dopo) for t in TESTI],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return file


def testi_visti(scena: str) -> list[dict[str, Any]]:
    """I testi aggiornati che si vedono nella scena: per ognuno i rettangoli (px CSS) nella
    pagina di oggi (testo di oggi) e in quella nativa (testo nuovo)."""
    trovati = json.loads(
        (SCENE_DIR / f"{scena}_testi.json").read_text(encoding="utf-8")
    )
    return [
        {
            "testo": i,
            "prima": t.prima,
            "dopo": t.dopo,
            "oggi": trovati["oggi"][i],
            "nativa": trovati["nativa"][i],
        }
        for i, t in enumerate(TESTI)
        if trovati["oggi"][i] or trovati["nativa"][i]
    ]


# ------------------------------------------------------------------------- Home Assistant
async def avvia_ha():
    from homeassistant import bootstrap
    from homeassistant.runner import RuntimeConfig

    # Home Assistant cerca le integrazioni personalizzate nel pacchetto custom_components:
    # deve essere quello della cartella di configurazione (sostituti_vmc), non quello del
    # worktree importato per preparare la scheda
    for modulo in [m for m in sys.modules if m.split(".", 1)[0] == "custom_components"]:
        del sys.modules[modulo]
    sys.path.insert(0, str(CONFIG))

    hass = await bootstrap.async_setup_hass(
        RuntimeConfig(
            config_dir=str(CONFIG),
            verbose=False,
            log_rotate_days=None,
            log_file=str(CONFIG / "ha.log"),
            log_no_color=True,
            skip_pip=True,
            safe_mode=False,
            debug=False,
            open_ui=False,
        )
    )
    await crea_utente(hass)
    await hass.async_start()
    await hass.async_block_till_done()
    # La configurazione http nuova è «in prova»: senza conferma dopo 5 minuti Home
    # Assistant torna a quella stabile e si riavvia
    from homeassistant.components.http.config import DATA_STORE

    negozio = hass.data.get(DATA_STORE)
    if negozio is not None and negozio.pending is not None:
        await negozio.async_promote_pending()
    return hass


async def crea_utente(hass) -> None:
    fornitore = next(p for p in hass.auth.auth_providers if p.type == "homeassistant")
    await fornitore.async_initialize()
    await hass.async_add_executor_job(fornitore.data.add_auth, UTENTE, PAROLA)
    await fornitore.data.async_save()
    credenziali = await fornitore.async_get_or_create_credentials({"username": UTENTE})
    utente = await hass.auth.async_create_user(UTENTE, group_ids=["system-admin"])
    await hass.auth.async_link_user(utente, credenziali)


async def servizio(hass, dominio: str, nome: str, dati: dict[str, Any]) -> None:
    await hass.services.async_call(dominio, nome, dati, blocking=True)


async def imposta(hass, entita: str, stato: str, attributi: Mapping[str, Any]) -> None:
    """Porta un'entità di oggi allo stato dato (aiutanti con i loro servizi)."""
    dominio = entita.split(".", 1)[0]
    dati = {"entity_id": entita}
    if dominio == "input_boolean":
        await servizio(hass, dominio, "turn_on" if stato == "on" else "turn_off", dati)
    elif dominio == "input_number":
        await servizio(hass, dominio, "set_value", {**dati, "value": float(stato)})
    elif dominio == "input_text":
        await servizio(hass, dominio, "set_value", {**dati, "value": stato})
    elif dominio == "input_select":
        opzioni = list(attributi["options"])
        if list(hass.states.get(entita).attributes["options"]) != opzioni:
            await servizio(hass, dominio, "set_options", {**dati, "options": opzioni})
        await servizio(hass, dominio, "select_option", {**dati, "option": stato})
    elif dominio == "input_datetime":
        if attributi.get("has_date") and attributi.get("has_time"):
            await servizio(hass, dominio, "set_datetime", {**dati, "datetime": stato})
        elif attributi.get("has_date"):
            await servizio(hass, dominio, "set_datetime", {**dati, "date": stato})
        else:
            await servizio(hass, dominio, "set_datetime", {**dati, "time": stato})
    elif dominio in ("timer", "script"):
        return  # i timer li avvia ogni scena; gli script restano fermi
    else:
        hass.states.async_set(entita, stato, dict(attributi))


def timer_di_base(stati: nativi.Stati) -> dict[str, int]:
    """I timer attivi nello stato del simulatore e i secondi che mancavano alla fine."""
    return {
        e: int(
            (datetime.fromisoformat(a["finishes_at"]) - ORA_ISTANTANEA).total_seconds()
        )
        for e, (s, a) in stati.items()
        if e.startswith("timer.") and s == "active"
    }


async def applica_scena(hass, scena: Scena, stati: nativi.Stati) -> float:
    """Stato di base + la scena; restituisce l'ora (ms) a cui fermare l'orologio del browser."""
    cambiati = {f"input_boolean.vmc_{NOME}_{n}" for n in scena.accesi}
    cambiati |= {f"input_number.vmc_{NOME}_{n}" for n in scena.numeri}
    for entita, (stato, attributi) in stati.items():
        dominio = entita.split(".", 1)[0]
        if dominio in AIUTANTI and entita not in cambiati:
            if hass.states.get(entita).state != stato:
                await imposta(hass, entita, stato, attributi)
        elif dominio in ("sensor", "binary_sensor", "automation"):
            nuovo = scena.sensori.get(entita, stato)
            attuale = hass.states.get(entita)
            if attuale is None or attuale.state != nuovo:
                hass.states.async_set(entita, nuovo, dict(attributi))
    for nome in scena.accesi:
        await servizio(
            hass,
            "input_boolean",
            "turn_on",
            {"entity_id": f"input_boolean.vmc_{NOME}_{nome}"},
        )
    for nome, valore in scena.numeri.items():
        await servizio(
            hass,
            "input_number",
            "set_value",
            {"entity_id": f"input_number.vmc_{NOME}_{nome}", "value": valore},
        )
    tutti = sorted(e for e in stati if e.startswith("timer."))
    timer = timer_di_base(stati)
    if "*" in scena.timer:
        timer = {e: 37 + 61 * i for i, e in enumerate(tutti)}
    timer |= {f"timer.vmc_{NOME}_{n}": s for n, s in scena.timer.items() if n != "*"}
    for e in tutti:
        if e not in timer and hass.states.get(e).state != "idle":
            await servizio(hass, "timer", "cancel", {"entity_id": e})
    for _tentativo in range(5):
        # partenza appena dopo un secondo intero: tutti i timer partono nello stesso secondo
        await asyncio.sleep(1.02 - time.time() % 1)
        for e, secondi in timer.items():
            await servizio(
                hass, "timer", "start", {"entity_id": e, "duration": MARGINE + secondi}
            )
        partenze = {
            datetime.fromisoformat(
                hass.states.get(e).attributes["finishes_at"]
            ).timestamp()
            - MARGINE
            - secondi
            for e, secondi in timer.items()
        }
        if len(partenze) <= 1:
            break
    else:
        raise RuntimeError(f"{scena.nome}: i timer non partono nello stesso secondo")
    await hass.async_block_till_done()
    partenza = partenze.pop() if partenze else float(int(time.time()))
    return (partenza + MARGINE - 0.5) * 1000


def stati_attuali(hass, entita: Iterator[str]) -> nativi.Stati:
    uscita: nativi.Stati = {}
    for e in entita:
        stato = hass.states.get(e)
        if stato is not None:
            uscita[e] = (stato.state, dict(stato.attributes))
    return uscita


def verifica_sostituti(hass, voci: list[dict], mappa) -> list[str]:
    """I sostituti hanno gli stati e gli attributi che nativi.stati_nativi prevede."""
    vecchie = stati_attuali(hass, (v["vecchia"] for v in voci))
    attesi = nativi.stati_nativi(vecchie, mappa)
    differenze = []
    for voce in voci:
        nuova = voce["nuova"]
        if voce["vecchia"].startswith("shell_command."):
            continue
        stato = hass.states.get(nuova)
        atteso = attesi.get(nuova)
        reale = (stato.state, dict(stato.attributes)) if stato else None
        if reale != atteso:
            differenze.append(f"{nuova}: atteso {atteso!r}, reale {reale!r}")
    return differenze


_NOME = re.compile(
    r"(?<![A-Za-z0-9_.])((?:binary_sensor|button|number|select|sensor|switch|text|time|"
    r"input_boolean|input_number|input_select|input_text|input_datetime|timer|script|"
    r"automation)\.vmc_master_[a-z0-9_]*[a-z0-9])\b"
)
SERVIZI = {
    "switch.toggle",
    "switch.turn_on",
    "switch.turn_off",
    "input_boolean.toggle",
    "input_boolean.turn_on",
    "input_boolean.turn_off",
    "script.turn_on",
}


def entita_della_scheda(config: Any) -> set[str]:
    testo = json.dumps(config, ensure_ascii=False)
    return {m.group(1) for m in _NOME.finditer(testo)} - SERVIZI


def mancanti(hass, config: Any) -> list[str]:
    """Entità nominate dalla scheda che in questo Home Assistant non ci sono."""
    return sorted(e for e in entita_della_scheda(config) if hass.states.get(e) is None)


# ------------------------------------------------------------------------- azioni
def coppie_di_azioni(
    oggi: Any, nativa: Any, percorso: str = ""
) -> Iterator[tuple[str, dict, dict]]:
    """Le azioni che chiamano un servizio, a coppie (scheda di oggi, scheda tradotta),
    nella stessa posizione delle due configurazioni."""
    if isinstance(oggi, dict) and isinstance(nativa, dict):
        if "perform_action" in oggi or "service" in oggi:
            yield percorso, oggi, nativa
            return
        for chiave in oggi:
            if chiave in nativa:
                yield from coppie_di_azioni(
                    oggi[chiave], nativa[chiave], f"{percorso}/{chiave}"
                )
    elif isinstance(oggi, list) and isinstance(nativa, list):
        assert len(oggi) == len(nativa), percorso
        for i, (a, b) in enumerate(zip(oggi, nativa, strict=True)):
            yield from coppie_di_azioni(a, b, f"{percorso}/{i}")


class Registro:
    """Gli effetti di un'azione: aiutanti di oggi cambiati, script avviati, comandi lanciati."""

    def __init__(self, hass) -> None:
        self.voci: list[tuple[str, ...]] = []
        self.attivo = False
        hass.bus.async_listen("state_changed", self._stato)
        hass.bus.async_listen("call_service", self._servizio)
        hass.bus.async_listen(EVENTO_SCRIPT, self._script)

    def _stato(self, evento) -> None:
        nuovo = evento.data["new_state"]
        if (
            self.attivo
            and nuovo
            and evento.data["entity_id"].split(".", 1)[0] in AIUTANTI
        ):
            self.voci.append(("stato", evento.data["entity_id"], nuovo.state))

    def _servizio(self, evento) -> None:
        if self.attivo and evento.data["domain"] == "shell_command":
            self.voci.append(("comando", evento.data["service"]))

    def _script(self, evento) -> None:
        if self.attivo:
            self.voci.append(("script", evento.data["script"]))

    async def effetti(self, hass, azione: Mapping[str, Any]) -> Counter:
        nome = azione.get("perform_action") or azione["service"]
        dominio, servizio_ = nome.split(".", 1)
        dati = {**(azione.get("data") or {}), **(azione.get("target") or {})}
        self.voci, self.attivo = [], True
        await hass.services.async_call(dominio, servizio_, dati, blocking=True)
        await hass.async_block_till_done()
        await asyncio.sleep(0.05)
        await hass.async_block_till_done()
        self.attivo = False
        return Counter(self.voci)


async def prova_azioni(
    hass, oggi: Any, nativa: Any, stati: nativi.Stati
) -> dict[str, Any]:
    """Ogni azione della scheda tradotta ha lo stesso effetto di quella di oggi."""
    registro = Registro(hass)
    esito: dict[str, Any] = {
        "coppie": 0,
        "per_servizio": Counter(),
        "diverse": [],
        "senza_effetto": [],
    }
    for percorso, a, b in coppie_di_azioni(oggi, nativa):
        esito["coppie"] += 1
        esito["per_servizio"][
            f"{a.get('perform_action')} -> {b.get('perform_action')}"
        ] += 1
        effetti = []
        for azione in (a, b):
            effetti.append(await registro.effetti(hass, azione))
            for voce in effetti[-1]:
                if voce[0] == "stato":
                    await imposta(hass, voce[1], *stati[voce[1]])
            await hass.async_block_till_done()
        if effetti[0] != effetti[1]:
            esito["diverse"].append(
                {
                    "percorso": percorso,
                    "oggi": str(effetti[0]),
                    "nativa": str(effetti[1]),
                }
            )
        if not effetti[0]:
            esito["senza_effetto"].append(percorso)
    esito["per_servizio"] = dict(esito["per_servizio"])
    return esito


async def prova_interruttori(
    hass, voci: list[dict], stati: nativi.Stati
) -> dict[str, Any]:
    """Accendere e spegnere ogni switch sostituto (il tocco predefinito del frontend) cambia
    l'interruttore di oggi; ogni pulsante avvia il suo script o il suo comando."""
    registro = Registro(hass)
    esito = {"switch": 0, "button": 0, "diversi": []}
    for voce in voci:
        nuova, vecchia = voce["nuova"], voce["vecchia"]
        dominio = nuova.split(".", 1)[0]
        if dominio == "switch":
            esito["switch"] += 1
            for servizio_, atteso in (
                ("turn_on", "on"),
                ("turn_off", "off"),
                ("toggle", "on"),
            ):
                fatto = await registro.effetti(
                    hass,
                    {
                        "perform_action": f"switch.{servizio_}",
                        "target": {"entity_id": nuova},
                    },
                )
                if (
                    fatto != Counter({("stato", vecchia, atteso): 1})
                    and hass.states.get(vecchia).state != atteso
                ):
                    esito["diversi"].append(f"{nuova} {servizio_}: {fatto}")
            await imposta(hass, vecchia, *stati[vecchia])
            await hass.async_block_till_done()
        elif dominio == "button":
            esito["button"] += 1
            fatto = await registro.effetti(
                hass, {"perform_action": "button.press", "target": {"entity_id": nuova}}
            )
            tipo, oggetto = vecchia.split(".", 1)
            atteso = Counter(
                {("script" if tipo == "script" else "comando", oggetto): 1}
            )
            if fatto != atteso:
                esito["diversi"].append(f"{nuova}: {fatto}, atteso {atteso}")
    return esito


# ------------------------------------------------------------------------- immagini
def unisci(file: Path, pezzi: int) -> None:
    """Rimette insieme i pezzi della fotografia scattati da scatta.js."""
    immagini = [Image.open(f"{file}.{i}.png").convert("RGB") for i in range(pezzi)]
    tela = Image.new(
        "RGB", (immagini[0].width, sum(i.height for i in immagini)), "white"
    )
    y = 0
    for immagine in immagini:
        tela.paste(immagine, (0, y))
        y += immagine.height
    tela.save(file)
    for i in range(pezzi):
        Path(f"{file}.{i}.png").unlink()


def confronta(scena: str, pezzi_oggi: int, pezzi_nativa: int) -> dict[str, Any]:
    """Pixel diversi fra le due fotografie della scena; scrive la differenza e le due
    fotografie affiancate."""
    unisci(SCENE_DIR / f"{scena}_oggi.png", pezzi_oggi)
    unisci(SCENE_DIR / f"{scena}_nativa.png", pezzi_nativa)
    a = np.asarray(Image.open(SCENE_DIR / f"{scena}_oggi.png").convert("RGB")).astype(
        np.int16
    )
    b = np.asarray(Image.open(SCENE_DIR / f"{scena}_nativa.png").convert("RGB")).astype(
        np.int16
    )
    altezza = max(a.shape[0], b.shape[0])
    larghezza = max(a.shape[1], b.shape[1])

    def allarga(x):
        tela = np.full((altezza, larghezza, 3), 255, dtype=np.int16)
        tela[: x.shape[0], : x.shape[1]] = x
        return tela

    a2, b2 = allarga(a), allarga(b)
    diversi = np.any(a2 != b2, axis=2)
    n = int(diversi.sum())
    esito: dict[str, Any] = {
        "oggi": list(a.shape[1::-1]),
        "nativa": list(b.shape[1::-1]),
        "pixel_diversi": n,
        "su": altezza * larghezza,
    }
    if n:
        righe = np.where(diversi.any(axis=1))[0]
        colonne = np.where(diversi.any(axis=0))[0]
        esito["riquadro"] = [
            int(colonne[0]),
            int(righe[0]),
            int(colonne[-1]),
            int(righe[-1]),
        ]
        # fasce di righe diverse (in pixel CSS, cioè /2)
        fasce, inizio, prima = [], int(righe[0]), int(righe[0])
        for r in righe[1:]:
            if r > prima + 1:
                fasce.append([inizio // 2, prima // 2])
                inizio = int(r)
            prima = int(r)
        fasce.append([inizio // 2, prima // 2])
        esito["fasce_css"] = fasce[:40]
    differenza = (a2 * 0.25 + 191).astype(np.uint8)
    differenza[diversi] = (255, 0, 0)
    Image.fromarray(differenza).save(SCENE_DIR / f"{scena}_differenza.png")
    affiancate = np.full((altezza, larghezza * 3 + 40, 3), 255, dtype=np.uint8)
    affiancate[:, :larghezza] = a2
    affiancate[:, larghezza + 20 : 2 * larghezza + 20] = b2
    affiancate[:, 2 * larghezza + 40 :] = differenza
    Image.fromarray(affiancate).save(SCENE_DIR / f"{scena}_affiancate.png")
    return esito


# ------------------------------------------------------------------------- browser
class Browser:
    """scatta.js, comandato riga per riga su stdin/stdout."""

    async def apri(self) -> None:
        self.processo = await asyncio.create_subprocess_exec(
            "node",
            str(QUI / "scatta.js"),
            BASE,
            str(SCENE_DIR),
            UTENTE,
            PAROLA,
            str(IMMAGINI),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            env={**os.environ, "NODE_PATH": "/opt/node-tools/node_modules"},
        )
        await self.risposta("PRONTO", 120)

    async def risposta(self, attesa: str, secondi: float = 90) -> str:
        while True:
            riga = await asyncio.wait_for(self.processo.stdout.readline(), secondi)
            if not riga:
                raise RuntimeError("scatta.js si è chiuso")
            testo = riga.decode().strip()
            if testo.startswith(attesa):
                return testo
            print("  scatta.js:", testo, flush=True)

    async def comando(self, testo: str, attesa: str, secondi: float = 90) -> str:
        self.processo.stdin.write((testo + "\n").encode())
        await self.processo.stdin.drain()
        return await self.risposta(attesa, secondi)

    async def chiudi(self) -> None:
        self.processo.stdin.write(b"FINE\n")
        await self.processo.stdin.drain()
        await asyncio.wait_for(self.processo.wait(), 60)


async def prova_tocchi(
    hass, browser: Browser, stati: nativi.Stati
) -> list[dict[str, Any]]:
    """Tocchi veri nel browser, sulle due schede: un pulsante del piè di pagina (apre la
    finestra Telecomando) e il pulsante «Velocità 2» della finestra Telecomando."""
    registro = Registro(hass)
    esiti = []
    prove = (
        ("chip", "opzioni_vmc", "03_telecomando", None),
        ("nome", "Velocità 2", None, "03_telecomando"),
    )
    for tipo, valore, _dopo, prima in prove:
        for pagina, dominio in (("oggi", "input_boolean"), ("nativa", "switch")):
            await applica_scena(
                hass,
                next(s for s in SCENE if s.nome == (prima or "01_principale")),
                stati,
            )
            await asyncio.sleep(2.5)
            bersaglio = f"{dominio}.vmc_{NOME}_{valore}" if tipo == "chip" else valore
            registro.voci, registro.attivo = [], True
            risposta = await browser.comando(
                f"CLICCA {pagina} {tipo} {bersaglio}", "CLICCATO"
            )
            await asyncio.sleep(1.5)
            await hass.async_block_till_done()
            registro.attivo = False
            esiti.append(
                {
                    "pagina": pagina,
                    "tocco": f"{tipo} {bersaglio}",
                    "browser": risposta,
                    "effetti": sorted(map(list, registro.voci)),
                }
            )
    return esiti


# ------------------------------------------------------------------------- tutto
async def principale() -> int:
    """Tutte le scene e tutte le prove; con VMC_SCENE (espressione regolare sul nome) solo
    quelle scene, con VMC_PROVE=0 senza tocchi e azioni. I risultati delle scene si
    aggiungono a quelli già in risultati.json (un giro in due volte resta sotto i 10 minuti).
    """
    # con «timeout» il giro riceve SIGTERM: si ferma, ma scrive i risultati raccolti
    asyncio.get_running_loop().add_signal_handler(
        signal.SIGTERM, asyncio.current_task().cancel
    )
    mappa = mappa_fase_1()
    stati = nativi.leggi_stati()
    scene = [s for s in SCENE if re.match(os.environ.get("VMC_SCENE", ""), s.nome)]
    prove = os.environ.get("VMC_PROVE", "1") != "0"
    SCENE_DIR.mkdir(parents=True, exist_ok=True)
    for scena in scene:
        for vecchio in SCENE_DIR.glob(f"{scena.nome}_*.png"):
            vecchio.unlink()
    file_risultati = ANTEPRIMA / "risultati.json"
    precedenti = (
        json.loads(file_risultati.read_text(encoding="utf-8"))
        if file_risultati.exists()
        else {}
    )
    oggi, nativa, voci = prepara_cartella(mappa)
    immagini = prepara_immagini(oggi, nativa)
    testi_cercati = prepara_testi_cercati()
    print(
        f"cartella pronta: {len(voci)} sostituti, immagini {immagini['nominate']}"
        f" (mancanti {len(immagini['mancanti'])})",
        flush=True,
    )
    inizio = time.monotonic()
    hass = await avvia_ha()
    print(
        f"Home Assistant {hass.config.version if hasattr(hass.config, 'version') else ''} avviato in {time.monotonic() - inizio:.0f} s",
        flush=True,
    )
    risultati: dict[str, Any] = {
        **precedenti,
        "sostituti": len(voci),
        "immagini": immagini,
    }
    try:
        for entita, (stato, attributi) in stati.items():
            if entita.split(".", 1)[0] not in ("timer", "script"):
                await imposta(hass, entita, stato, attributi)
        await applica_scena(hass, SCENE[0], stati)
        await hass.async_block_till_done()
        differenze = verifica_sostituti(hass, voci, mappa)
        risultati["sostituti_diversi_da_nativi"] = differenze
        print(f"sostituti diversi da stati_nativi: {len(differenze)}", flush=True)
        for riga in differenze[:20]:
            print("  ", riga, flush=True)
        risultati["mancanti_oggi"] = mancanti(hass, oggi)
        risultati["mancanti_nativa"] = mancanti(hass, nativa)
        risultati["entita_oggi"] = len(entita_della_scheda(oggi))
        risultati["entita_nativa"] = len(entita_della_scheda(nativa))
        print(
            f"entità nominate: oggi {risultati['entita_oggi']} (mancanti {len(risultati['mancanti_oggi'])}), "
            f"nativa {risultati['entita_nativa']} (mancanti {len(risultati['mancanti_nativa'])})",
            flush=True,
        )
        browser = Browser()
        await browser.apri()
        risultati["scene"] = {
            nome: esito
            for nome, esito in precedenti.get("scene", {}).items()
            if nome in {s.nome for s in SCENE}
        }
        try:
            for scena in scene:
                orologio = await applica_scena(hass, scena, stati)
                fatto = await browser.comando(
                    f"SCENA {scena.nome} {orologio:.0f} {'apri' if scena.apri else '-'}"
                    f" {testi_cercati}",
                    "FATTO",
                    180,
                )
                _f, _n, pezzi_oggi, pezzi_nativa = fatto.split()
                esito = await hass.async_add_executor_job(
                    confronta, scena.nome, int(pezzi_oggi), int(pezzi_nativa)
                )
                esito["titolo"] = TITOLI[scena.nome]
                esito["testi"] = await hass.async_add_executor_job(
                    testi_visti, scena.nome
                )
                risultati["scene"][scena.nome] = esito
                print(
                    f"[{time.monotonic() - inizio:.0f} s] {scena.nome}: oggi {esito['oggi']} nativa {esito['nativa']} pixel diversi {esito['pixel_diversi']} testi aggiornati visti {len(esito['testi'])}"
                    + (
                        f" fasce {esito['fasce_css'][:6]}"
                        if esito["pixel_diversi"]
                        else ""
                    ),
                    flush=True,
                )
            if prove:
                risultati["tocchi"] = await prova_tocchi(hass, browser, stati)
                for t in risultati["tocchi"]:
                    print("tocco", t, flush=True)
        finally:
            await browser.chiudi()
        risultati["scene"] = dict(sorted(risultati["scene"].items()))
        if not prove:
            return 0
        await applica_scena(hass, SCENE[0], stati)
        risultati["azioni"] = await prova_azioni(hass, oggi, nativa, stati)
        print(
            f"azioni: {risultati['azioni']['coppie']} coppie, diverse {len(risultati['azioni']['diverse'])}, "
            f"senza effetto {len(risultati['azioni']['senza_effetto'])}; {risultati['azioni']['per_servizio']}",
            flush=True,
        )
        risultati["interruttori"] = await prova_interruttori(hass, voci, stati)
        print(f"sostituti comandati: {risultati['interruttori']}", flush=True)
    finally:
        await hass.async_add_executor_job(
            file_risultati.write_text,
            json.dumps(risultati, ensure_ascii=False, indent=1, default=str),
            "utf-8",
        )
        await hass.async_stop()
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(principale()))
