"""Banco differenziale casuale del package intero: Home Assistant e motore tradotto.

Completa i 17.264 scenari fissi del simulatore: qui una sequenza casuale di eventi
(generata una volta dal seme ``VMC_SEME``, ``VMC_PASSI`` passi) gira due volte nello
stesso processo, con lo stesso orologio fermo:

1. con le integrazioni ``automation`` e ``script`` di Home Assistant che leggono i file
   del package come li scrive l'integrazione per la Master (``installatore.genera_file``)
   e come li legge Home Assistant (``parse_yaml``);
2. con il motore tradotto (il codice di ``generato/``: le automazioni come logiche
   dell'integrazione, gli script come entità ``script`` con ``fase3.MotoreFase3``).

Il resto del package è lo stesso nelle due corse: gli aiutanti veri (``input_*`` e
``timer``, con stati ripristinati a caso all'avvio), i sensori modello veri
(integrazione ``template`` con la configurazione del package) e, al posto dei sensori
che leggono la VMC (``tcp``, ``command_line``, ``rest``), entità di comodo scritte dal
banco con lo stato di una VMC finta (velocità, alimentazione, sensori ambientali). I
servizi con effetti esterni (``shell_command``, ``notify``, ``tts``,
``media_player``, ``recorder``, ``homeassistant.update_entity`` e
``homeassistant.restart``, ``vmc_master.verifica_ip``) sono finti: annotano dominio,
servizio, dati e istante; i comandi di velocità arrivano alla VMC finta, gli
aggiornamenti forzati dei sensori della VMC la rileggono, gli altri aggiornamenti
forzati restano quelli veri. Le notifiche persistenti sono quelle vere, annotate a ogni
cambio.

Gli eventi: cambi degli aiutanti come dalla scheda (con un utente, a volte più tocchi
nello stesso istante), letture della VMC (stato di ventilazione, CO2, VOC, umidità,
temperature, ``unavailable``, Black-Out e ripartenza, telecomando), sensori esterni,
script e comandi di velocità chiamati dalla scheda, timer e il tempo che passa (pochi
decimi di secondo o salti di molti minuti, che attraversano i trigger a orario). Il
tempo avanza da un timer all'altro (un microsecondo dopo l'istante in cui scade, come
con un orologio vero). Se nello stesso istante arrivano più di ``LIMITE_ISTANTE`` eventi
(automazioni che si richiamano a vicenda senza fine) la corsa finisce lì: anche il
motore deve entrare nel ciclo allo stesso evento. (Fino alla 9.0.0b45 il banco spegneva
e riaccendeva tutte le automazioni, come un utente, e la sequenza continuava: le logiche
del motore non hanno ``automation.turn_off`` e ``automation.turn_on``, né
``automation.trigger``, che non è più tra i passi.)

Gli stati delle logiche del motore (``automation.*``, fuori dalla macchina degli stati)
entrano nel registro nel punto del bus dei loro state_changed
(``fase3.osserva_logiche``). Si confrontano, in quest'ordine: le chiamate ai servizi
finti, i cambi di stato di tutte le entità e delle logiche, stato e attributi finali di
automazioni e script (``last_triggered``, ``current``...), le notifiche persistenti e
infine il registro completo degli eventi, senza ``automation_triggered`` (le logiche non
lo hanno); i contesti diventano numeri d'ordine (si confronta chi ha causato cosa). Il
rapporto di copertura (automazioni avviate, dagli ``automation_triggered`` di Home
Assistant, e script avviati, con i conteggi esatti) si stampa e, con
``VMC_RAPPORTO=<file>``, si scrive in JSON.

    VMC_PASSI=2000 VMC_SEME=7 pytest tests/nativa/motore/test_pacchetto_casuale.py -s
"""

from __future__ import annotations

import asyncio
import concurrent.futures
import difflib
import functools
import gc
import heapq
import itertools
import json
import logging
import math
import os
import random
import re
import shlex
import sys
import types
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime, time, timedelta
from functools import lru_cache
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pytest
from freezegun.api import FrozenDateTimeFactory
from homeassistant.components import persistent_notification as pn
from homeassistant.components.homeassistant.services import SCHEMA_UPDATE_ENTITY
from homeassistant.const import EVENT_CALL_SERVICE, EVENT_STATE_CHANGED, MATCH_ALL
from homeassistant.core import (
    Context,
    CoreState,
    Event,
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
    State,
    SupportsResponse,
    callback,
)
from homeassistant.core_config import _CUSTOMIZE_CONFIG_SCHEMA, DATA_CUSTOMIZE
from homeassistant.helpers.entity_component import async_update_entity
from homeassistant.helpers.entity_values import EntityValues
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.setup import async_setup_component
from homeassistant.util import dt as dt_util
from homeassistant.util import slugify
from homeassistant.util.yaml.loader import parse_yaml
from pytest_homeassistant_custom_component.common import async_test_home_assistant

from custom_components.vmc_master.const import NOME_MASTER
from custom_components.vmc_master.installatore import genera_file
from custom_components.vmc_master.nativa.client import ErroreVMC
from custom_components.vmc_master.nativa.motore.definizioni import (
    COMANDO_NOME,
    COMANDO_VMC,
)
from custom_components.vmc_master.nativa.motore.ha import Motore
from custom_components.vmc_master.nativa.motore.interni import nome_valido
from custom_components.vmc_master.nativa.motore.memoria_interna import MemoriaInterna
from custom_components.vmc_master.nativa.motore.stati_logiche import stati_logiche
from custom_components.vmc_master.nativa.motore.timer import (
    EVENTI_TIMER,
    bus_del_motore,
)

from . import generato
from .banco_memoria import (
    AGGIORNA,
    DOMINI_INTERNI,
    IDS_INTERNI,
    Smistatore,
    modelli_entita_con_memoria,
    salvati_da_stati,
    senza_interni,
    servizi_misti,
)
from .fase3 import MotoreFase3, osserva_logiche, personalizzato
from .nel_canale import CoppiaContesto, ordine_esterno, rinumera_ovunque, voce_interna
from .test_avvio_motore import _ripristina
from .test_semantica import _carica, _gira
from .traduci import (
    _comando,
    leggi_comandi,
    leggi_package,
    traduci_configurazione,
)

VMC_PASSI = int(os.environ.get("VMC_PASSI", "300"))
VMC_SEME = int(os.environ.get("VMC_SEME", "1"))
VMC_RAPPORTO = os.environ.get("VMC_RAPPORTO")
# Eventi nello stesso istante oltre i quali il banco interrompe un ciclo senza fine; nelle
# corse senza cicli il massimo è di qualche centinaio (all'avvio)
LIMITE_ISTANTE = 5000

FUSO = ZoneInfo("Europe/Rome")
# IP e versione con cui l'integrazione scrive il package (e che la VMC finta risponde)
IP = "192.168.1.160"
VERSIONE = "9.0.0b42"
AIUTANTI = (
    "input_boolean",
    "input_number",
    "input_text",
    "input_select",
    "input_datetime",
    "timer",
)
# I sensori che leggono la VMC (tcp, command_line, rest): entità di comodo del banco.
STATO = "sensor.vmc_master_status_ventola"
SENSORI = "sensor.vmc_master_sensori"
NOME = "sensor.vmc_master_nome"
LAN = "sensor.vmc_master_lan"
PING = "sensor.vmc_master_status_ip"
REPOSITORY = "sensor.vmc_master_versione_repository"
DI_COMODO = (STATO, SENSORI, NOME, LAN, PING, REPOSITORY)
# Intervalli di lettura dei sensori della VMC nel package (scan_interval).
LETTURE = {STATO: 5, PING: 10, SENSORI: 1227, NOME: 43227, LAN: 57641}
# Entità esterne che la scheda può scegliere (elenchi degli script «Aggiorna Elenco»).
ESTERNE: dict[str, dict[str, Any]] = {
    "sensor.temperatura_esterna_prova": {
        "device_class": "temperature",
        "unit_of_measurement": "°C",
    },
    "sensor.temperatura_interna_prova": {
        "device_class": "temperature",
        "unit_of_measurement": "°C",
    },
    "sensor.umidita_esterna_prova": {
        "device_class": "humidity",
        "unit_of_measurement": "%",
    },
    "sensor.umidita_interna_prova": {
        "device_class": "humidity",
        "unit_of_measurement": "%",
    },
    "sensor.co2_prova": {
        "device_class": "carbon_dioxide",
        "unit_of_measurement": "ppm",
    },
}
METEO = "weather.casa_prova"
LETTORI = ("media_player.soggiorno_prova", "media_player.cucina_prova")
TELEFONO = "telefono_prova"
# Comandi di velocità (shell_command) e codice della velocità nella lettura VMGO.
VELOCITA = {
    "vmc_master_velocita_0": 0,
    "vmc_master_velocita_1": 1,
    "vmc_master_velocita_2": 2,
    "vmc_master_velocita_3": 3,
    "vmc_master_velocita_4": 4,
    "vmc_master_iperventilazione": 5,
    "vmc_master_notturna": 6,
    "vmc_master_freecooling": 7,
}
# Servizi finti oltre a shell_command.* (homeassistant.update_entity a parte).
FINTI = (
    ("homeassistant", "restart"),
    ("tts", "google_translate_say"),
    ("tts", "clear_cache"),
    ("media_player", "volume_set"),
    ("recorder", "purge_entities"),
    ("vmc_master", "verifica_ip"),
    ("notify", f"mobile_app_{TELEFONO}"),
)


@lru_cache(maxsize=1)
def _testi() -> dict[str, str]:
    """I file del package della Master come li scrive l'integrazione."""
    return genera_file(NOME_MASTER, IP, VERSIONE)


@lru_cache(maxsize=1)
def _package() -> dict[str, Any]:
    """Il package della Master (``vmc_master.yaml``) letto come lo legge Home Assistant;
    in ``automation`` anche l'Automazione VMC Master (``vmc_master_automazione.yaml``),
    per ultima come la carica Home Assistant (``packages: !include_dir_named`` legge i file
    in ordine di nome, prima ``vmc_master.yaml``). Le automazioni e gli script della corsa di Home Assistant vengono da qui,
    non da ``leggi_package`` (che legge il motore tradotto): il confronto prova anche
    che il traduttore legge il package come lo installa l'integrazione."""
    package = parse_yaml(_testi()[f"vmc_{NOME_MASTER}.yaml"])
    principale = parse_yaml(_testi()[f"vmc_{NOME_MASTER}_automazione.yaml"])
    package["automation"] = [*package["automation"], *principale["automation"]]
    return package


@lru_cache(maxsize=1)
def _automazioni() -> tuple[str, ...]:
    """Gli entity_id delle automazioni del package (dal nome, come li crea Home
    Assistant)."""
    return tuple(
        sorted(f"automation.{slugify(a['alias'])}" for a in _package()["automation"])
    )


@lru_cache(maxsize=1)
def _testo_package() -> str:
    return "".join(
        _testi()[f"vmc_{NOME_MASTER}{coda}.yaml"] for coda in ("", "_automazione")
    )


@functools.cache
def _letterali(entita: str) -> tuple[str, ...]:
    """I valori con cui il package confronta lo stato di ``entita`` (``==``, ``!=``,
    ``in [...]``, ``is_state``): i valori «interessanti» da provare."""
    testo = _testo_package()
    e = re.escape(entita)
    valori: set[str] = set()
    filtri = r"\s*(?:\|\s*(?:trim|lower|string)\s*)*"
    for m in re.finditer(
        rf"states\(\s*['\"]{e}['\"]\s*\){filtri}(?:==|!=)\s*['\"]([^'\"]*)['\"]", testo
    ):
        valori.add(m.group(1))
    for m in re.finditer(
        rf"states\(\s*['\"]{e}['\"]\s*\){filtri}(?:not\s+)?in\s*\[([^\]]*)\]", testo
    ):
        valori.update(re.findall(r"['\"]([^'\"]*)['\"]", m.group(1)))
    for m in re.finditer(
        rf"is_state\(\s*['\"]{e}['\"]\s*,\s*(\[[^\]]*\]|['\"][^'\"]*['\"])", testo
    ):
        valori.update(re.findall(r"['\"]([^'\"]*)['\"]", m.group(1)))
    return tuple(sorted(valori))


# --- i timer del package nel motore (fase 4) ------------------------------------------------

# I timer del package letti da Home Assistant fuori dal motore: il sensore modello
# «Velocità Registrata» (nell'integrazione nativa è un modello di StatoVMC, che riceve i
# timer del motore). Con i timer del motore il banco li scrive nella macchina degli stati
# nel punto in cui li scriverebbe Home Assistant, perché il sensore modello vero li legga.
SPECCHIO = (
    "timer.vmc_master_countdown_free_heating_annullamento",
    "timer.vmc_master_countdown_free_cooling_annullamento",
)
_TRADOTTO_CON_TIMER: dict[str, Any] = {}


def _del_package(evento: Event) -> bool:
    """Un evento dei timer del package: un loro cambio di stato, un loro evento
    (``timer.started``...) o la chiamata a un servizio dei timer."""
    dati = evento.data
    if evento.event_type == EVENT_STATE_CHANGED:
        return dati["entity_id"].startswith("timer.vmc_master_")
    if evento.event_type in EVENTI_TIMER:
        return str(dati.get("entity_id", "")).startswith("timer.vmc_master_")
    if evento.event_type == "call_service":
        return dati.get("domain") == "timer"
    return False


async def _motore_con_timer(hass: HomeAssistant) -> Any:
    """Il package tradotto con ``timer_motore`` (una volta per processo): il modulo con
    ``crea``."""
    if "motore" not in _TRADOTTO_CON_TIMER:
        automazioni, script = leggi_package()
        modelli, motore = await traduci_configurazione(
            hass,
            automazioni,
            script,
            nome_modelli="pacchetto_timer_modelli",
            timer_motore=True,
        )
        _carica("pacchetto_timer_modelli", modelli)
        _TRADOTTO_CON_TIMER["motore"] = _carica("pacchetto_timer_motore", motore)
    assert f"{generato.__name__}.pacchetto_timer_motore" in __import__("sys").modules
    return _TRADOTTO_CON_TIMER["motore"]


def _stato_timer(stato: State, norma: Callable[[Any], Any]) -> tuple[Any, ...]:
    return (
        stato.entity_id,
        stato.state,
        norma(dict(stato.attributes)),
        norma(stato.last_changed),
        norma(stato.last_updated),
        norma(stato.context),
    )


# --- la VMC finta -----------------------------------------------------------------------


@dataclass
class VmcFinta:
    """La VMC vista dai sensori di comodo: velocità (codice VMGO 0-7), alimentazione,
    letture ambientali grezze (decimi; le temperature negative in complemento a 2)."""

    velocita: int = 1
    accesa: bool = True
    disturbo: bool = False
    t_interna: int = 210
    t_esterna: int = 100
    umidita: int = 500
    co2: int = 600
    voc: int = 50

    def stato(self) -> str:
        if not self.accesa or self.disturbo:
            return "unavailable"
        return f"VMGO,{self.velocita:05d}" + ",00000" * 13

    def sensori(self) -> str:
        if not self.accesa or self.disturbo:
            return "unavailable"
        campi = [
            self.t_interna % 65536,
            self.t_esterna % 65536,
            self.umidita,
            self.co2,
            *[0] * 6,
            self.voc,
            0,
            0,
            0,
        ]
        return "VMGI," + ",".join(f"{v:05d}" for v in campi)

    def lettura(self, entita: str) -> str:
        if entita == STATO:
            return self.stato()
        if entita == SENSORI:
            return self.sensori()
        if entita == PING:
            return "ON-Line" if self.accesa else "OFF-Line"
        if not self.accesa or self.disturbo:
            return "unavailable"
        if entita == NOME:
            return "VMNM Master"
        if entita == LAN:
            return "VMSL," + IP.replace(".", ",")
        return f"v.{VERSIONE}"


# --- la sequenza casuale ------------------------------------------------------------------


@dataclass
class Prova:
    """Una sequenza casuale: istante iniziale, stati ripristinati, passi."""

    seme: int
    inizio: datetime
    ripristino: list[State]
    vmc: VmcFinta
    passi: list[tuple[Any, ...]] = field(default_factory=list)


def _numero(conf: dict[str, Any], valore: float) -> float:
    minimo, massimo = float(conf.get("min", 0)), float(conf.get("max", 100))
    passo = float(conf.get("step", 1))
    valore = min(massimo, max(minimo, valore))
    return round(round((valore - minimo) / passo) * passo + minimo, 6)


class Generatore:
    """Genera la sequenza dal seme: tutto quello che è casuale si decide qui, prima delle
    corse, così le due corse ricevono esattamente gli stessi passi."""

    def __init__(self, seme: int) -> None:
        self.rng = random.Random(seme)
        self.seme = seme
        pkg = _package()
        self.pkg = pkg
        self.booleani = sorted(pkg["input_boolean"])
        self.opzioni = [
            b
            for b in self.booleani
            if not b.startswith("vmc_master_spia")
            and "verifica_soglia" not in b
            and b != "vmc_master_attese_inizializzate"
        ]
        self.numeri = sorted(pkg["input_number"])
        self.selezioni = sorted(pkg["input_select"])
        self.testi = sorted(pkg["input_text"])
        self.orari = sorted(pkg["input_datetime"])
        self.timer = sorted(pkg["timer"])
        self.script = sorted(pkg["script"])

    # --- valori -----------------------------------------------------------------------

    def valore_numero(self, nome: str) -> float:
        conf = self.pkg["input_number"][nome]
        r = self.rng
        minimo, massimo = float(conf.get("min", 0)), float(conf.get("max", 100))
        if nome.startswith("vmc_master_attesa_"):
            # attese brevi (si vedono finire) e qualche attesa lunga
            return _numero(conf, r.choice([1, 2, 3, 5, 8, 10, 15, 30, 60, 120, 300]))
        if nome.startswith("vmc_master_offset_"):
            return _numero(conf, r.choice([0, 0, 0, r.uniform(minimo, massimo) / 10]))
        if nome.startswith("vmc_master_aria_scambiata"):
            return _numero(conf, r.choice([0, r.uniform(0, 5000), 1e6]))
        scelta = r.random()
        if scelta < 0.15:
            return _numero(conf, minimo)
        if scelta < 0.3:
            return _numero(conf, massimo)
        return _numero(conf, r.uniform(minimo, min(massimo, minimo + 1000)))

    def valore_testo(self, nome: str) -> str:
        r = self.rng
        candidati = [*_letterali(f"input_text.{nome}"), ""]
        if nome.startswith("vmc_master_last_"):
            candidati += [*ESTERNE, METEO, *LETTORI, TELEFONO]
        if nome.startswith("vmc_master_countdown_"):
            candidati += [str(r.randint(0, 300)), "0", "-"]
        if nome == "vmc_master_ip_insert":
            candidati += ["192.168.1.160", "192.168.1.77", "10.0.0.300", "abc"]
        if nome == "vmc_master_nome_da_inserire":
            candidati += ["Sala", "Camera_2", "x" * 10]
        if nome in (
            "vmc_master_ultimi_comandi_automazione",
            "vmc_master_ultime_letture_velocita",
        ):
            candidati.append("|".join("0" for _ in range(8)))
        valore = r.choice(candidati)
        massimo = int(self.pkg["input_text"][nome].get("max", 100))
        return valore[:massimo]

    def valore_orario(self, adesso: datetime) -> str:
        """Un orario vicino a ``adesso`` (ora locale: i calendari scattano davvero) o a
        caso."""
        r = self.rng
        if r.random() < 0.6:
            locale = adesso.astimezone(FUSO) + timedelta(minutes=r.randint(-3, 20))
            return locale.strftime("%H:%M:00")
        return f"{r.randint(0, 23):02d}:{r.choice([0, 15, 30, 45, r.randint(0, 59)]):02d}:00"

    def stato_ripristinato(self, dominio: str, nome: str, adesso: datetime) -> State:
        r = self.rng
        conf = self.pkg[dominio][nome] or {}
        entita = f"{dominio}.{nome}"
        if dominio == "input_boolean":
            acceso = r.random() < (0.15 if nome.startswith("vmc_master_spia") else 0.5)
            return State(entita, "on" if acceso else "off")
        if dominio == "input_number":
            return State(entita, str(self.valore_numero(nome)))
        if dominio == "input_text":
            return State(entita, self.valore_testo(nome))
        if dominio == "input_select":
            return State(entita, r.choice(list(conf.get("options", []))))
        return State(entita, self.valore_orario(adesso))

    # --- la prova ------------------------------------------------------------------------

    def prova(self, passi: int) -> Prova:
        r = self.rng
        # giorno a caso dell'anno (giorno della settimana e mese contano: calendario,
        # free heating/cooling); a volte poco prima di mezzanotte o delle 8 (trigger time)
        giorno = datetime(2026, 1, 1, tzinfo=FUSO) + timedelta(days=r.randint(0, 364))
        scelta = r.random()
        if scelta < 0.25:
            ora = time(23, r.randint(50, 59), r.randint(0, 59))
        elif scelta < 0.45:
            ora = time(7, r.randint(50, 59), r.randint(0, 59))
        else:
            ora = time(r.randint(0, 23), r.randint(0, 59), r.randint(0, 59))
        inizio = datetime.combine(giorno.date(), ora, tzinfo=FUSO).astimezone(UTC)
        ripristino = []
        for dominio in ("input_boolean", "input_number", "input_text", "input_select"):
            for nome, conf in self.pkg[dominio].items():
                if isinstance(conf, dict) and "initial" in conf:
                    continue
                ripristino.append(self.stato_ripristinato(dominio, nome, inizio))
        for nome in self.orari:
            ripristino.append(self.stato_ripristinato("input_datetime", nome, inizio))
        vmc = VmcFinta(
            velocita=r.choice([0, 1, 1, 2, 3, 4, 5, 6, 7]),
            accesa=r.random() < 0.9,
            t_interna=r.randint(150, 280),
            t_esterna=r.randint(-80, 380),
            umidita=r.randint(300, 900),
            co2=r.randint(400, 2000),
            voc=r.randint(0, 600),
        )
        prova = Prova(self.seme, inizio, ripristino, vmc)
        adesso = inizio
        tipi: list[tuple[float, Callable[[datetime], Any]]] = [
            (26, self.passo_tempo),
            (12, self.passo_booleano),
            (5, self.passo_numero),
            (4, self.passo_selezione),
            (3, self.passo_orario),
            (2, self.passo_testo),
            (10, self.passo_vmc),
            (2, self.passo_interruzione),
            (1, self.passo_raffica),
            (8, self.passo_ambiente),
            (4, self.passo_esterni),
            (6, self.passo_comando),
            (8, self.passo_script),
            (2, self.passo_timer),
        ]
        pesi = [p for p, _ in tipi]
        while len(prova.passi) < passi:
            (genera,) = r.choices([g for _, g in tipi], weights=pesi)
            generati = genera(adesso)
            for passo in generati if isinstance(generati, list) else [generati]:
                if passo[0] == "attendi":
                    adesso += timedelta(microseconds=passo[1])
                prova.passi.append(passo)
        del prova.passi[passi:]
        return prova

    # --- i passi -------------------------------------------------------------------------

    def passo_tempo(self, _adesso: datetime) -> tuple[Any, ...]:
        """Il tempo passa (microsecondi): pochi decimi, qualche secondo o minuto, salti
        fino a 20 minuti."""
        r = self.rng
        scelta = r.random()
        if scelta < 0.4:
            secondi = r.choice([0.1, 0.2, 0.5, 1, 1.5])
        elif scelta < 0.7:
            secondi = r.uniform(1, 12)
        elif scelta < 0.92:
            secondi = r.uniform(12, 150)
        else:
            secondi = r.uniform(150, 1200)
        return ("attendi", round(secondi * 1_000_000))

    def passo_booleano(self, _adesso: datetime) -> tuple[Any, ...]:
        r = self.rng
        nome = r.choice(self.opzioni if r.random() < 0.75 else self.booleani)
        servizio = r.choice(["turn_on", "turn_off", "toggle"])
        return (
            "servizio",
            "input_boolean",
            servizio,
            {"entity_id": f"input_boolean.{nome}"},
        )

    def passo_raffica(self, _adesso: datetime) -> tuple[Any, ...]:
        """Due-quattro finestre della scheda aperte (o chiuse) nello stesso istante,
        come tocchi veloci mentre l'Automazione VMC Master (mode: queued) è occupata."""
        r = self.rng
        finestre = [
            b
            for b in self.booleani
            if b.startswith(("vmc_master_opzion", "vmc_master_conferma"))
        ]
        return (
            "raffica",
            [
                (
                    "input_boolean",
                    "turn_on" if r.random() < 0.8 else "turn_off",
                    {"entity_id": f"input_boolean.{nome}"},
                )
                for nome in r.sample(finestre, r.randint(2, 4))
            ],
        )

    def passo_numero(self, _adesso: datetime) -> tuple[Any, ...]:
        nome = self.rng.choice(self.numeri)
        return (
            "servizio",
            "input_number",
            "set_value",
            {"entity_id": f"input_number.{nome}", "value": self.valore_numero(nome)},
        )

    def passo_selezione(self, _adesso: datetime) -> tuple[Any, ...]:
        r = self.rng
        nome = r.choice(self.selezioni)
        entita = f"input_select.{nome}"
        opzioni = list(self.pkg["input_select"][nome].get("options", []))
        if nome == "vmc_master_selected_notification_device" and r.random() < 0.5:
            return (
                "servizio",
                "input_select",
                "set_options",
                {"entity_id": entita, "options": [*opzioni, TELEFONO]},
            )
        if "selected" in nome:
            opzioni += [
                *ESTERNE,
                METEO,
                *LETTORI,
                TELEFONO,
                "sensor.vmc_master_temp_esterna_status_senza_offset",
                "sensor.vmc_master_co2_status_senza_offset",
            ]
        return (
            "servizio",
            "input_select",
            "select_option",
            {"entity_id": entita, "option": r.choice(opzioni)},
        )

    def passo_orario(self, adesso: datetime) -> tuple[Any, ...]:
        nome = self.rng.choice(self.orari)
        return (
            "servizio",
            "input_datetime",
            "set_datetime",
            {"entity_id": f"input_datetime.{nome}", "time": self.valore_orario(adesso)},
        )

    def passo_testo(self, _adesso: datetime) -> tuple[Any, ...]:
        nome = self.rng.choice(self.testi)
        return (
            "servizio",
            "input_text",
            "set_value",
            {"entity_id": f"input_text.{nome}", "value": self.valore_testo(nome)},
        )

    def passo_vmc(self, _adesso: datetime) -> tuple[Any, ...]:
        """La VMC: telecomando (velocità cambiata e subito letta), Black-Out e
        ripartenza, disturbo del Wi-Fi (letture unavailable), lettura forzata."""
        r = self.rng
        scelta = r.random()
        if scelta < 0.45:
            return ("vmc", "velocita", r.choice([0, 1, 2, 3, 4, 5, 6, 7]))
        if scelta < 0.6:
            return ("vmc", "accesa", r.random() < 0.6)
        if scelta < 0.75:
            return ("vmc", "disturbo", r.random() < 0.5)
        if scelta < 0.9:
            return ("vmc", "leggi", r.choice(list(LETTURE)))
        # una lettura strana scritta così com'è (codice sconosciuto, vuota, unknown)
        return (
            "lettura",
            STATO,
            r.choice(
                ["VMGO,00009" + ",00000" * 13, "", "unknown", "VMGO", "unavailable"]
            ),
            {},
        )

    def passo_interruzione(self, _adesso: datetime) -> list[tuple[Any, ...]]:
        """Un'interruzione breve della lettura della VMC: corrente via per pochi secondi
        (la VMC riparte a Velocità 1; il ping la vede spenta solo se capita in mezzo)
        o disturbo del Wi-Fi, poi la velocità letta subito."""
        r = self.rng
        campo, spenta, riaccesa = r.choice(
            [
                ("accesa", False, True),
                ("accesa", False, True),
                ("disturbo", True, False),
            ]
        )
        return [
            ("vmc", campo, spenta),
            ("vmc", "leggi", STATO),
            ("attendi", round(r.uniform(0.5, 15) * 1_000_000)),
            ("vmc", campo, riaccesa),
            ("vmc", "leggi", STATO),
        ]

    def passo_ambiente(self, _adesso: datetime) -> tuple[Any, ...]:
        """Letture ambientali della VMC (decimi): CO2, VOC, umidità, temperature."""
        r = self.rng
        campo = r.choice(["co2", "voc", "umidita", "t_interna", "t_esterna"])
        valore = {
            "co2": lambda: r.choice([r.randint(350, 900), r.randint(900, 2500), 5000]),
            "voc": lambda: r.choice([r.randint(0, 150), r.randint(150, 1000)]),
            "umidita": lambda: r.choice([r.randint(200, 600), r.randint(600, 1000)]),
            "t_interna": lambda: r.randint(100, 320),
            "t_esterna": lambda: r.choice([r.randint(-150, 50), r.randint(50, 400)]),
        }[campo]()
        return ("ambiente", campo, valore, r.random() < 0.8)

    def passo_esterni(self, _adesso: datetime) -> tuple[Any, ...]:
        r = self.rng
        scelta = r.random()
        if scelta < 0.6:
            entita = r.choice(list(ESTERNE))
            if "temperatura" in entita:
                valore = str(round(r.uniform(-10, 35), 1))
            elif "umidita" in entita:
                valore = str(round(r.uniform(15, 100), 1))
            else:
                valore = str(r.randint(350, 2500))
            if r.random() < 0.1:
                valore = r.choice(["unavailable", "unknown"])
            return ("lettura", entita, valore, ESTERNE[entita])
        if scelta < 0.8:
            return (
                "lettura",
                METEO,
                r.choice(["sunny", "rainy", "unavailable"]),
                {
                    "temperature": round(r.uniform(-5, 35), 1),
                    "humidity": r.randint(20, 100),
                },
            )
        return (
            "lettura",
            r.choice(LETTORI),
            r.choice(["idle", "playing", "off", "unavailable"]),
            {},
        )

    def passo_comando(self, _adesso: datetime) -> tuple[Any, ...]:
        """Un tasto di velocità della scheda (shell_command chiamato da un utente)."""
        r = self.rng
        nomi = list(VELOCITA)
        if r.random() < 0.15:
            nomi = [
                "vmc_master_sensori_on",
                "vmc_master_sensori_off",
                "vmc_master_pannello_led_on",
                "vmc_master_pannello_led_off",
            ]
        return ("chiama", "shell_command", r.choice(nomi), {}, True)

    def passo_script(self, _adesso: datetime) -> tuple[Any, ...]:
        r = self.rng
        nome = r.choice(self.script)
        dati: dict[str, Any] = {}
        if nome == "vmc_master_azzera_booleans" and r.random() < 0.5:
            dati = {"mantieni_pannelli": r.choice([True, False])}
        if r.random() < 0.5:
            return (
                "chiama",
                "script",
                "turn_on",
                {
                    "entity_id": f"script.{nome}",
                    **({"variables": dati} if dati else {}),
                },
                True,
            )
        return ("chiama", "script", nome, dati, True)

    def passo_timer(self, _adesso: datetime) -> tuple[Any, ...]:
        r = self.rng
        nome = r.choice(self.timer)
        servizio = r.choice(["start", "start", "cancel", "finish", "pause"])
        dati: dict[str, Any] = {"entity_id": f"timer.{nome}"}
        if servizio == "start" and r.random() < 0.7:
            dati["duration"] = r.choice([1, 2, 5, 10, 30, 70])
        return ("servizio", "timer", servizio, dati)


# --- una corsa ---------------------------------------------------------------------------


class Normalizzatore:
    """Valori del registro senza ciò che cambia da una corsa all'altra: istanti in
    secondi dall'inizio (al microsecondo), contesti come numeri d'ordine."""

    def __init__(self, inizio: datetime) -> None:
        self.inizio = inizio
        self.contesti: dict[str | None, int | None] = {None: None}

    def contesto(self, identificativo: str | None) -> int | None:
        return self.contesti.setdefault(identificativo, len(self.contesti) - 1)

    def __call__(self, valore: Any) -> Any:
        if isinstance(valore, datetime):
            return round((valore - self.inizio).total_seconds(), 6)
        if isinstance(valore, Context):
            return CoppiaContesto(
                (self.contesto(valore.id), self.contesto(valore.parent_id))
            )
        if isinstance(valore, State):
            return (
                valore.entity_id,
                valore.state,
                self(dict(valore.attributes)),
                self(valore.last_changed),
            )
        if isinstance(valore, dict):
            return {
                str(k): self(v)
                for k, v in sorted(valore.items(), key=lambda kv: str(kv[0]))
                if k != "run_id"
            }
        if isinstance(valore, (list, tuple, set, frozenset)):
            voci = [self(v) for v in valore]
            return (
                sorted(voci, key=repr) if isinstance(valore, (set, frozenset)) else voci
            )
        if isinstance(valore, (str, int, float, bool)) or valore is None:
            return valore
        return repr(valore)


class CicloInfinito(Exception):
    """Troppi eventi nello stesso istante: automazioni e script si richiamano a vicenda
    senza fine e senza far passare il tempo."""


@dataclass
class Ritmo:
    """Gli eventi annotati nell'istante corrente."""

    istante: datetime | None = None
    eventi: int = 0

    def conta(self, istante: datetime) -> None:
        if istante != self.istante:
            self.istante = istante
            self.eventi = 0
        self.eventi += 1


async def _lavora(hass: HomeAssistant, ritmo: Ritmo) -> None:
    """Come ``_gira`` (il ciclo lavora finché ha qualcosa di pronto), ma si ferma con
    ``CicloInfinito`` se nello stesso istante arrivano più di ``LIMITE_ISTANTE`` eventi.
    Senza limite il ciclo non finirebbe e la memoria crescerebbe senza fine: Home
    Assistant tiene in cache le condizioni degli script con una chiave che contiene il
    numero di render dei loro modelli (``Script._async_get_condition``), cioè una chiave
    nuova (decine di kB per l'Automazione VMC Master) a ogni esecuzione."""
    loop = hass.loop
    while True:
        await asyncio.sleep(0)
        if ritmo.eventi > LIMITE_ISTANTE:
            raise CicloInfinito(ritmo.istante)
        fine = loop.time() + loop._clock_resolution  # type: ignore[attr-defined]
        if not loop._ready and not any(  # type: ignore[attr-defined]
            not h.cancelled() and h.when() < fine
            for h in loop._scheduled  # type: ignore[attr-defined]
        ):
            return


async def _avanza(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory, microsecondi: int, ritmo: Ritmo
) -> int:
    """Il tempo passa di ``microsecondi`` fermandosi a ogni timer che scade nel
    frattempo, come con un orologio vero: al primo microsecondo dopo l'istante del timer
    (asyncio lo esegue solo quando ``when < loop.time() + clock_resolution``, e la
    risoluzione è sotto la precisione di ``loop.time()``). Restituisce le fermate."""
    loop = hass.loop
    restano = microsecondi
    fermate = 0
    while True:
        await _lavora(hass, ritmo)
        if restano == 0:
            return fermate
        prossimo = min(
            (h.when() for h in loop._scheduled if not h.cancelled()), default=None
        )
        salto = restano
        if prossimo is not None:
            # dopo _lavora nessun timer è dovuto: prossimo >= loop.time()
            salto = min(restano, math.floor((prossimo - loop.time()) * 1e6) + 1)
        freezer.tick(timedelta(microseconds=salto))
        restano -= salto
        fermate += 1


class EsecutoreSincrono(concurrent.futures.Executor):
    """Un esecutore senza thread: il lavoro gira subito, dentro ``submit``, e il futuro
    è già finito; asyncio consegna il risultato al ciclo come un callback pronto,
    nell'ordine in cui i lavori sono stati chiesti. Con i thread l'istante reale in cui
    un lavoro finisce (per esempio l'import delle piattaforme dei sensori modello)
    cambierebbe l'ordine degli eventi da una corsa all'altra."""

    def submit(  # type: ignore[override]
        self, fn: Callable[..., Any], /, *args: Any, **kwargs: Any
    ) -> concurrent.futures.Future[Any]:
        futuro: concurrent.futures.Future[Any] = concurrent.futures.Future()
        try:
            risultato = fn(*args, **kwargs)
        except BaseException as err:  # noqa: BLE001 - come in un thread
            futuro.set_exception(err)
        else:
            futuro.set_result(risultato)
        return futuro


class TimerOrdinato(asyncio.TimerHandle):
    """Un timer del ciclo che, a parità di istante, scade nell'ordine in cui è stato
    creato.

    asyncio tiene i timer in uno heap ordinato solo per istante: due timer con lo stesso
    istante (per esempio le pause di due script partiti insieme) escono nell'ordine che
    dà la forma dello heap, cioè tutta la storia dei timer del ciclo, compresi quelli di
    altre istanze di Home Assistant di prova sullo stesso ciclo. È un ordine arbitrario
    (anche due corse identiche di Home Assistant lo vedono diverso): qui diventa l'ordine
    di creazione, uguale in tutte le corse che creano gli stessi timer nello stesso
    ordine."""

    __slots__ = ("_ordine",)
    _ordine: int

    def __lt__(self, altro: asyncio.TimerHandle) -> bool:  # type: ignore[override]
        # nella coda ci sono solo timer: quelli nati prima della corsa vengono prima
        return (self._when, self._ordine) < (
            altro._when,  # type: ignore[attr-defined]
            getattr(altro, "_ordine", -1),
        )


def _call_at_ordinato(
    loop: asyncio.AbstractEventLoop,
    contatore: itertools.count[int],
    when: float,
    callback: Callable[..., Any],
    *args: Any,
    context: Any = None,
) -> asyncio.TimerHandle:
    """``BaseEventLoop.call_at`` (senza debug) con un ``TimerOrdinato``."""
    loop._check_closed()  # type: ignore[attr-defined]
    timer = TimerOrdinato(when, callback, args, loop, context)
    timer._ordine = next(contatore)
    heapq.heappush(loop._scheduled, timer)  # type: ignore[attr-defined]
    timer._scheduled = True  # type: ignore[attr-defined]
    return timer


def _ciclo_pulito(loop: asyncio.AbstractEventLoop) -> None:
    """Toglie dalla coda dei timer del ciclo quelli annullati (della corsa precedente).

    Due timer con lo stesso istante scadono nell'ordine in cui li restituisce lo heap di
    asyncio, che dipende anche dai timer annullati ancora nello heap: senza pulizia la
    seconda corsa partirebbe da uno heap diverso e gli scadere allo stesso istante
    cambierebbero ordine (anche tra due corse identiche di Home Assistant)."""
    coda = loop._scheduled  # type: ignore[attr-defined]
    for handle in coda:
        if handle.cancelled():
            handle._scheduled = False  # type: ignore[attr-defined]
    coda[:] = [h for h in coda if not h.cancelled()]
    heapq.heapify(coda)
    loop._timer_cancelled_count = 0  # type: ignore[attr-defined]


async def _corsa(
    freezer: FrozenDateTimeFactory,
    prova: Prova,
    *,
    motore: bool,
    timer_motore: bool = False,
    fedeli: bool = False,
    codice: types.ModuleType | None = None,
    memoria: bool = False,
) -> dict[str, Any]:
    """Una corsa su un ciclo degli eventi reso deterministico e veloce, poi rimesso com'era.

    - Niente modalità di debug di asyncio (il plugin dei test la accende: a ogni
      callback e a ogni futuro annota da dove viene e la corsa diventa tre volte più
      lenta) e niente messaggi INFO (uno per ogni automazione avviata).
    - L'esecutore di default è ``EsecutoreSincrono``: il lavoro mandato ai thread
      finisce subito, non quando capita.
    - I timer nascono come ``TimerOrdinato``: a parità di istante scadono nell'ordine di
      creazione (la stessa regola della fixture ``ordine_dei_timer`` di
      test_semantica_tempi.py, senza tenere in vita un registro di tutti i timer).
    - La coda dei timer parte pulita e il garbage collector è spento: i distruttori
      (che chiudono generatori, cancellano timer...) non girano in momenti diversi
      nelle due corse. Con il garbage collector acceso già la corsa di Home Assistant da
      sola cambia (seme 1, 600 passi: 59.699 cambi di stato invece di 59.713); spento,
      la memoria cresce: con 2000 passi una corsa arriva a qualche GB.
    - Alla fine si cancellano i timer rimasti all'istanza di Home Assistant fermata."""
    loop = asyncio.get_running_loop()
    debug = loop.get_debug()
    esecutore = loop._default_executor  # type: ignore[attr-defined]
    radice = logging.getLogger()
    livello = radice.level
    # i messaggi INFO di ogni automazione avviata (una al secondo) rallentano la corsa
    radice.setLevel(max(livello, logging.WARNING))
    loop.set_debug(False)
    loop._default_executor = EsecutoreSincrono()  # type: ignore[attr-defined]
    loop.call_at = functools.partial(  # type: ignore[method-assign]
        _call_at_ordinato, loop, itertools.count()
    )
    _ciclo_pulito(loop)
    gc.collect()
    gc.disable()
    try:
        return await _corsa_ciclo(
            freezer,
            prova,
            motore=motore,
            timer_motore=timer_motore,
            fedeli=fedeli,
            codice=codice,
            memoria=memoria,
        )
    finally:
        gc.enable()
        radice.setLevel(livello)
        del loop.call_at  # type: ignore[method-assign]
        loop._default_executor = esecutore  # type: ignore[attr-defined]
        # i timer lasciati da Home Assistant fermato (per esempio quelli dei modelli
        # con now()) non devono scattare nella corsa dopo
        for handle in loop._scheduled:  # type: ignore[attr-defined]
            handle.cancel()
        _ciclo_pulito(loop)
        loop.set_debug(debug)


async def _corsa_ciclo(
    freezer: FrozenDateTimeFactory,
    prova: Prova,
    *,
    motore: bool,
    timer_motore: bool = False,
    fedeli: bool = False,
    codice: types.ModuleType | None = None,
    memoria: bool = False,
) -> dict[str, Any]:
    """La corsa. Fase 4: con ``timer_motore`` i timer del package sono fuori dal registro
    degli eventi: i loro cambi di stato, i loro eventi e le chiamate ai loro servizi
    vanno nel registro dei timer (``dei_timer``) o, le chiamate ai servizi dei timer, da
    nessuna parte; con il motore (``motore``) il package è tradotto con
    ``timer_motore`` e i timer sono quelli del motore. Con ``fedeli`` i comandi di shell
    finti durano come quelli veri (``_COMANDI_FEDELI``) e il registro non ha gli eventi
    che con gli script e i comandi dentro il motore non ci sono più (li conta
    ``esito["tolti"]``). ``codice`` è il codice del motore tradotto con gli script e i
    comandi dentro il motore (``comandi=``), anche insieme a ``timer_motore``.

    Con ``memoria`` (fase 4) i 67 valori interni sono fuori dal registro: i loro cambi
    di stato e le chiamate con soli valori interni vanno in ``interni`` e
    ``chiamate_interne`` (``banco_memoria.Smistatore``), ``homeassistant.update_entity``
    è senza di loro; con il motore ``codice`` è tradotto anche con ``interni=INTERNI`` e
    i valori interni sono nella memoria interna, ripristinati da ``prova.ripristino``."""
    freezer.move_to(prova.inizio)
    norma = Normalizzatore(prova.inizio)
    pkg = _package()
    vmc = VmcFinta(**vars(prova.vmc))
    registro: list[Any] = []
    chiamate: list[Any] = []
    notifiche: list[Any] = []
    fine_chiamate: list[Any] = []
    dei_timer: list[Any] = []
    esito: dict[str, Any] = {
        "registro": registro,
        "chiamate": chiamate,
        "notifiche": notifiche,
        "fine_chiamate": fine_chiamate,
    }
    annota_attivo = False
    ritmo = Ritmo()
    con_timer_del_motore = motore and timer_motore
    esito["tolti"] = Counter()
    avviate: list[tuple[str, str]] = []
    esito["automazioni_avviate"] = avviate
    m: Motore | None = None
    # fase 4, memoria interna: lo smistatore scrive nello stesso registro
    smistatore: Smistatore | None = None
    interni = set(IDS_INTERNI) if memoria else set()
    if memoria:
        smistatore = Smistatore(IDS_INTERNI, norma, ritmo.conta)
        smistatore.registro = registro
    memoria_interna: MemoriaInterna | None = None

    async with async_test_home_assistant(initial_state=CoreState.not_running) as hass:
        hass.import_executor = EsecutoreSincrono()
        await hass.config.async_set_time_zone(str(FUSO))
        _ripristina(hass, prova.ripristino)
        hass.data[DATA_CUSTOMIZE] = EntityValues(
            _CUSTOMIZE_CONFIG_SCHEMA(pkg["homeassistant"])["customize"], {}, {}
        )
        utente = await hass.auth.async_create_user("Utente scheda")

        @callback
        def annota(evento: Event) -> None:
            if not annota_attivo:
                return
            if evento.event_type == "automation_triggered":
                # solo con Home Assistant (le logiche del motore non hanno l'evento):
                # fuori dal registro, per il rapporto di copertura
                avviate.append(
                    (evento.data["entity_id"], str(evento.data.get("source")))
                )
                return
            if timer_motore and _del_package(evento):
                # con i timer del motore: nella corsa di Home Assistant i cambi di stato
                # e gli eventi dei timer vanno nel registro dei timer (le chiamate ai
                # loro servizi da nessuna parte); in quella del motore ci sono solo i
                # cambi di stato di SPECCHIO, già annotati dal motore
                if not motore and evento.event_type != "call_service":
                    ritmo.conta(evento.time_fired)
                    if evento.event_type == EVENT_STATE_CHANGED:
                        dei_timer.append(("stato", evento.data["new_state"]))
                    else:
                        dei_timer.append(
                            (
                                "evento",
                                evento.time_fired,
                                evento.event_type,
                                dict(evento.data),
                                evento.context,
                            )
                        )
                return
            if fedeli and (tolto := _tolto(evento)) is not None:
                esito["tolti"][tolto] += 1
                return
            if smistatore is not None:
                smistatore.evento(evento)
                return
            ritmo.conta(evento.time_fired)
            dati = evento.data
            if evento.event_type == EVENT_STATE_CHANGED:
                dati = {"entity_id": dati["entity_id"], "new_state": dati["new_state"]}
            registro.append(
                (
                    norma(evento.time_fired),
                    evento.event_type,
                    norma(dict(dati)),
                    norma(evento.context),
                )
            )

        hass.bus.async_listen(MATCH_ALL, annota)
        smetti = osserva_logiche(hass, annota) if motore else None
        assert await async_setup_component(hass, "homeassistant", {})
        assert await async_setup_component(hass, "persistent_notification", {})
        for dominio in AIUTANTI:
            if dominio == "timer" and con_timer_del_motore:
                continue
            voci = pkg[dominio]
            if memoria and motore and dominio in DOMINI_INTERNI:
                voci = {
                    o: v for o, v in voci.items() if f"{dominio}.{o}" not in interni
                }
            assert await async_setup_component(hass, dominio, {dominio: voci})
        if memoria and motore:
            assert smistatore is not None
            memoria_interna = MemoriaInterna(hass, NOME_MASTER)
            memoria_interna.ripristina(salvati_da_stati(prova.ripristino))
            memoria_interna.ascolta_cambi(
                lambda evento: smistatore.cambio(evento) if annota_attivo else None
            )
            memoria_interna.ascolta_chiamate(
                lambda *voce: smistatore.chiamata(*voce) if annota_attivo else None
            )
            servizi_misti(
                hass,
                memoria_interna,
                [f"input_boolean.{o}" for o in pkg["input_boolean"]],
            )

        @callback
        def notificato(tipo: Any, voci: dict[str, Any]) -> None:
            notifiche.append(
                (
                    norma(dt_util.utcnow()),
                    str(tipo),
                    norma({k: dict(v) for k, v in voci.items()}),
                )
            )

        pn.async_register_callback(hass, notificato)

        def annota_chiamata(chiamata: ServiceCall) -> None:
            dati = dict(chiamata.data)
            if memoria and (chiamata.domain, chiamata.service) == AGGIORNA:
                # con la memoria interna il motore toglie i valori interni
                dati = senza_interni(
                    {
                        "domain": chiamata.domain,
                        "service": chiamata.service,
                        "service_data": dati,
                    },
                    interni,
                )["service_data"]
            chiamate.append(
                (
                    norma(dt_util.utcnow()),
                    chiamata.domain,
                    chiamata.service,
                    norma(dati),
                    norma(chiamata.context),
                )
            )

        def leggi(entita: str) -> None:
            """Una lettura del sensore di comodo dalla VMC finta."""
            hass.states.async_set(
                entita, vmc.lettura(entita), {"friendly_name": entita}
            )

        async def finto(chiamata: ServiceCall) -> None:
            annota_chiamata(chiamata)

        async def nc(codice: int | None) -> bool:
            """Fase 4: un comando che arriva alla VMC finta (come ``comando``)."""
            if not vmc.accesa:
                await asyncio.sleep(3)
                return False
            await asyncio.sleep(0.05)
            if codice is not None:

                def applica() -> None:
                    if vmc.accesa:
                        vmc.velocita = codice

                hass.loop.call_later(0.5, applica)
            return True

        async def comando_fedele(chiamata: ServiceCall) -> None:
            """Fase 4: lo shell_command come quello vero. I comandi per la VMC come
            ``comando``; il cambio del nome arriva alla VMC solo con un nome valido
            (come il file .sh, vedi test_comandi_vmc.py); il cambio dell'IP, un nome
            non valido e la pulizia dei file .sh finiscono subito (un processo che non
            dura)."""
            tipo = _COMANDI_FEDELI[chiamata.service]
            if tipo == COMANDO_VMC:
                await nc(VELOCITA.get(chiamata.service))
            elif tipo == COMANDO_NOME:
                stato = hass.states.get("input_text.vmc_master_nome_da_inserire")
                valore = stato.state if stato is not None else "unknown"
                pulito = valore.replace('"', "").replace("\\", "")
                if nome_valido(shlex.split(f'"{pulito}"')) is not None:
                    await nc(None)

        async def comando(chiamata: ServiceCall) -> None:
            """shell_command: il comando dura un attimo (o il timeout di nc con la VMC
            spenta) e la VMC cambia velocità mezzo secondo dopo."""
            annota_chiamata(chiamata)
            if fedeli:
                await comando_fedele(chiamata)
                return
            codice = VELOCITA.get(chiamata.service)
            if not vmc.accesa:
                await asyncio.sleep(3)
                return
            await asyncio.sleep(0.05)
            if codice is not None:

                def applica() -> None:
                    if vmc.accesa:
                        vmc.velocita = codice

                hass.loop.call_later(0.5, applica)

        async def aggiorna(chiamata: ServiceCall) -> None:
            """homeassistant.update_entity: i sensori della VMC si rileggono dalla VMC
            finta, le altre entità si aggiornano davvero."""
            annota_chiamata(chiamata)
            for entita in chiamata.data["entity_id"]:
                if entita in DI_COMODO:
                    leggi(entita)
                else:
                    await async_update_entity(hass, entita)

        async def statistiche(chiamata: ServiceCall) -> ServiceResponse:
            annota_chiamata(chiamata)
            return {"statistics": {}}

        for nome in pkg["shell_command"]:
            hass.services.async_register("shell_command", nome, comando)
        for dominio, servizio in FINTI:
            hass.services.async_register(dominio, servizio, finto)
        hass.services.async_register(
            "homeassistant", "update_entity", aggiorna, schema=SCHEMA_UPDATE_ENTITY
        )
        hass.services.async_register(
            "recorder",
            "get_statistics",
            statistiche,
            supports_response=SupportsResponse.ONLY,
        )
        for entita in DI_COMODO:
            leggi(entita)
        for entita, attributi in ESTERNE.items():
            hass.states.async_set(entita, "20", attributi)
        hass.states.async_set(METEO, "sunny", {"temperature": 12.5, "humidity": 60})
        for entita in LETTORI:
            hass.states.async_set(entita, "idle")
        for entita, secondi in LETTURE.items():
            async_track_time_interval(
                hass,
                lambda _istante, entita=entita: leggi(entita),
                timedelta(seconds=secondi),
                cancel_on_shutdown=True,
            )
        assert await async_setup_component(
            hass, "template", {"template": pkg["template"]}
        )
        await hass.async_block_till_done()
        if motore and (codice is not None or timer_motore):
            # fase 4: il codice tradotto con gli script e i comandi dentro il motore
            # (``codice``), con i timer del motore (``timer_motore``), o con tutti e due
            if codice is None:
                codice = await _motore_con_timer(hass)
            argomenti: dict[str, Any] = {}
            if timer_motore:
                argomenti["timer"] = pkg["timer"]
            if getattr(codice, "comandi", None) is not None:
                # fase 4: script e comandi dentro il motore, i comandi alla VMC finta
                per_testo = {
                    _comando(riga)[1]: nome
                    for nome, riga in pkg["shell_command"].items()
                }

                async def invia(testo: str) -> str:
                    if not await nc(VELOCITA.get(per_testo.get(testo, ""))):
                        raise ErroreVMC("VMC spenta")
                    return ""

                argomenti.update(comandi=codice.comandi, invia=invia)
            if memoria_interna is not None:
                assert modelli_entita_con_memoria(hass, memoria_interna)
            # il codice di generato/ (senza comandi) con gli script come entità
            fase3 = getattr(codice, "comandi", None) is None
            m = (MotoreFase3 if fase3 else Motore)(hass, memoria=memoria_interna)
            await m.avvia(crea=codice.crea, **argomenti)
            if m.c.comandi is not None:

                @callback
                def comandato(evento: Event) -> None:
                    """La chiamata di un comando, annotata come la annota ``comando``."""
                    chiamate.append(
                        (
                            norma(dt_util.utcnow()),
                            "shell_command",
                            evento.data["service"],
                            norma(dict(evento.data["service_data"])),
                            norma(evento.context),
                        )
                    )

                m.c.comandi.ascolta(comandato)
            if timer_motore:
                assert m.c.timer is not None

                @callback
                def scritto(t: Any) -> None:
                    stato = t.stato_ha
                    if annota_attivo:
                        ritmo.conta(stato.last_updated)
                        dei_timer.append(("stato", stato))
                    if t.entity_id in SPECCHIO:
                        hass.states.async_set_internal(
                            t.entity_id,
                            stato.state,
                            stato.attributes,
                            True,
                            stato.context,
                            None,
                            stato.last_updated_timestamp,
                        )

                @callback
                def evento_del_motore(evento: Event) -> None:
                    if annota_attivo:
                        ritmo.conta(evento.time_fired)
                        dei_timer.append(
                            (
                                "evento",
                                evento.time_fired,
                                evento.event_type,
                                dict(evento.data),
                                evento.context,
                            )
                        )

                for t in m.c.timer.timer.values():
                    if t.entity_id in SPECCHIO:
                        scritto(t)
                m.c.timer.ascolta(scritto)
                for tipo in sorted(EVENTI_TIMER):
                    bus_del_motore(hass).async_listen(tipo, evento_del_motore)
        elif motore:
            assert not memoria, "con la memoria interna serve il codice tradotto"
            m = MotoreFase3(hass)
            await m.avvia()
        else:
            assert await async_setup_component(
                hass, "script", {"script": pkg["script"]}
            )
            assert await async_setup_component(
                hass, "automation", {"automation": pkg["automation"]}
            )
        await hass.async_block_till_done()
        annota_attivo = True
        compiti: list[asyncio.Future[Any]] = []
        esito["fermate"] = 0
        esito["cicli_infiniti"] = []

        async def _chiama(
            indice: int, dominio: str, servizio: str, dati: Any, con_utente: bool
        ) -> None:
            """Una chiamata della scheda (o di un altro script) che il banco non aspetta:
            si annota quando finisce e come."""
            contesto = Context(user_id=utente.id if con_utente else None)
            try:
                if m is not None and m.c.interni is not None and dominio == "script":
                    # fase 4: lo script del motore, come la chiamata del servizio
                    assert m.c.interni is not None
                    await m.c.interni.chiama(servizio, dati, {}, contesto)
                elif (
                    m is not None
                    and m.c.comandi is not None
                    and dominio == "shell_command"
                ):
                    assert m.c.comandi is not None
                    await m.c.comandi.esegui(servizio, dati, {}, contesto)
                else:
                    await hass.services.async_call(
                        dominio, servizio, dati, blocking=True, context=contesto
                    )
            except BaseException as err:
                fine_chiamate.append(
                    (norma(dt_util.utcnow()), indice, type(err).__name__)
                )
                if isinstance(err, asyncio.CancelledError):
                    raise
                return
            fine_chiamate.append((norma(dt_util.utcnow()), indice))

        async def passo_singolo(indice: int, passo: tuple[Any, ...]) -> None:
            tipo = passo[0]
            if tipo == "attendi":
                esito["fermate"] += await _avanza(hass, freezer, passo[1], ritmo)
                return
            if tipo == "servizio":
                _, dominio, servizio, dati = passo
                try:
                    if dominio == "timer" and m is not None and m.c.timer is not None:
                        # la scheda e i timer del motore
                        await m.c.timer.servizio(
                            servizio, dict(dati), None, Context(user_id=utente.id)
                        )
                    else:
                        await hass.services.async_call(
                            dominio,
                            servizio,
                            dati,
                            blocking=True,
                            context=Context(user_id=utente.id),
                        )
                except Exception as err:  # noqa: BLE001
                    registro.append(
                        (norma(dt_util.utcnow()), "errore", indice, repr(err))
                    )
            elif tipo == "chiama":
                _, dominio, servizio, dati, con_utente = passo
                compiti.append(
                    asyncio.ensure_future(
                        _chiama(indice, dominio, servizio, dati, con_utente)
                    )
                )
            elif tipo == "raffica":
                # più tocchi nello stesso istante, senza aspettare l'uno l'altro
                for dominio, servizio, dati in passo[1]:
                    compiti.append(
                        asyncio.ensure_future(
                            _chiama(indice, dominio, servizio, dati, True)
                        )
                    )
            elif tipo == "lettura":
                _, entita, stato, attributi = passo
                hass.states.async_set(entita, stato, attributi)
            elif tipo == "vmc":
                _, campo, valore = passo
                if campo == "leggi":
                    leggi(valore)
                elif campo == "velocita":
                    if vmc.accesa:
                        vmc.velocita = valore
                        leggi(STATO)
                elif campo == "accesa":
                    if valore and not vmc.accesa and vmc.velocita != 0:
                        # dopo un Black-Out la VMC riparte a velocità 1 (se non era ferma)
                        vmc.velocita = 1
                    vmc.accesa = valore
                else:
                    vmc.disturbo = valore
            elif tipo == "ambiente":
                _, campo, valore, subito = passo
                setattr(vmc, campo, valore)
                if subito:
                    leggi(SENSORI)
            await _lavora(hass, ritmo)

        async def esegui() -> None:
            registro.append(("avvio",))
            avvio = asyncio.ensure_future(hass.async_start())
            while not avvio.done():
                await _avanza(hass, freezer, 100_000, ritmo)
            registro.append(("avviato",))

            for indice, passo in enumerate(prova.passi):
                await passo_singolo(indice, passo)
            # coda: le esecuzioni in corso finiscono (o restano in attesa) per un minuto
            esito["fermate"] += await _avanza(hass, freezer, 60_000_000, ritmo)

        try:
            await esegui()
        except CicloInfinito:
            # un ciclo senza fine (le logiche del motore non si spengono e riaccendono
            # come le automazioni): Home Assistant e il motore devono fermarsi allo stesso
            # evento e si confronta quello che è successo fino a lì
            esito["cicli_infiniti"].append(norma(ritmo.istante))
            esito["corsa_interrotta"] = norma(ritmo.istante)
            registro.append((norma(ritmo.istante), "corsa interrotta", ritmo.eventi))
        registro.append(("fine",))
        annota_attivo = False

        logiche = [
            s
            for s in (personalizzato(hass, v) for v in stati_logiche(hass).stati.values())
            if s is not None
        ]
        esito["stati"] = sorted(
            (s.entity_id, s.state, norma(dict(s.attributes)), norma(s.last_changed))
            for s in [*hass.states.async_all(), *logiche]
            if not (timer_motore and s.entity_id.startswith("timer.vmc_master_"))
            and not (fedeli and s.entity_id.startswith("script."))
            and s.entity_id not in interni
        )
        if smistatore is not None:
            assert not (memoria_interna and any(hass.states.get(e) for e in interni))
            esito["interni"] = smistatore.interni_cambi
            esito["chiamate_interne"] = smistatore.chiamate_interne
            esito["sequenza"] = smistatore.sequenza
            esito["update_senza_interni"] = smistatore.update_senza_interni
            esito["stati_interni"] = [
                (
                    s.entity_id,
                    s.state,
                    norma(dict(s.attributes)),
                    norma(s.last_changed),
                    norma(s.last_updated),
                )
                for e in IDS_INTERNI
                if (
                    s := (
                        memoria_interna.stato(e)
                        if memoria_interna is not None
                        else hass.states.get(e)
                    )
                )
                is not None
            ]
        if timer_motore:
            finali = (
                [t.stato_ha for t in m.c.timer.timer.values()]
                if m is not None and m.c.timer is not None
                else [
                    s
                    for s in hass.states.async_all("timer")
                    if s.entity_id.startswith("timer.vmc_master_")
                ]
            )
            # il registro dei timer, con i contesti numerati dopo quelli del registro
            esito["dei_timer"] = [
                ("stato", _stato_timer(v[1], norma)) if v[0] == "stato" else norma(v)
                for v in dei_timer
            ]
            esito["timer_finali"] = sorted(_stato_timer(s, norma) for s in finali)
        esito["automazioni_script"] = [
            voce
            for voce in esito["stati"]
            if voce[0].startswith(("automation.", "script."))
        ]
        esito["notifiche_finali"] = norma(
            {k: dict(v) for k, v in pn._async_get_or_create_notifications(hass).items()}
        )
        if m is not None:
            # le logiche si fermano (e con loro gli script interni)
            assert smetti is not None
            smetti()
            await m.ferma()
        else:
            await hass.services.async_call(
                "automation", "turn_off", {"entity_id": "all"}, blocking=True
            )
        if m is None or m.c.interni is None:
            await hass.services.async_call(
                "script", "turn_off", {"entity_id": "all"}, blocking=True
            )
        if m is not None and m.c.timer is not None:
            await m.c.timer.servizio("cancel", {"entity_id": "all"}, None, Context())
        else:
            await hass.services.async_call(
                "timer", "cancel", {"entity_id": "all"}, blocking=True
            )
        await _gira(hass)
        await hass.async_stop(force=True)
        freezer.tick(timedelta(seconds=61))
        await _gira(hass)
        for compito in compiti:
            if not compito.done():
                compito.cancel()
        await asyncio.gather(*compiti, return_exceptions=True)
    return esito


def _tolto(evento: Event) -> str | None:
    """Fase 4: il tipo di un evento che con gli script e i comandi dentro il motore non
    c'è più (None: resta)."""
    tipo, dati = evento.event_type, evento.data
    if tipo == EVENT_STATE_CHANGED and dati["entity_id"].startswith("script."):
        return "state_changed script"
    if tipo == EVENT_CALL_SERVICE and dati["domain"] in ("script", "shell_command"):
        return f"call_service {dati['domain']}"
    if tipo == "script_started":
        return tipo
    return None


# Fase 4: il tipo di ogni comando di shell del package (vmc, nome, ip, nessuno).
_COMANDI_FEDELI = {nome: _comando(riga)[0] for nome, riga in leggi_comandi().items()}


# --- confronto e copertura ---------------------------------------------------------------


def _confronta(atteso: list[Any], ottenuto: list[Any], cosa: str) -> str | None:
    if ottenuto == atteso:
        return None
    righe_attese = [repr(v) for v in atteso]
    righe_ottenute = [repr(v) for v in ottenuto]
    diff = list(
        difflib.unified_diff(
            righe_attese, righe_ottenute, "home_assistant", "motore", lineterm="", n=3
        )
    )
    return f"{cosa} diversi:\n" + "\n".join(diff[:80])


def copertura(esito: dict[str, Any]) -> dict[str, Any]:
    """Automazioni e script avviati (eventi automation_triggered della corsa di Home
    Assistant e script_started) e trigger diversi dell'Automazione VMC Master."""
    automazioni: Counter[str] = Counter()
    script: Counter[str] = Counter()
    trigger_principale: Counter[str] = Counter()
    for entita, origine in esito["automazioni_avviate"]:
        automazioni[entita] += 1
        if entita == AUTOMAZIONE_VMC:
            trigger_principale[origine] += 1
    for voce in esito["registro"]:
        if len(voce) > 2 and voce[1] == "script_started":
            script[voce[2]["entity_id"]] += 1
    tutte = _automazioni()
    tutti = [f"script.{s}" for s in _package()["script"]]
    return {
        "automazioni": {a: automazioni[a] for a in sorted(tutte)},
        "script": {s: script[s] for s in sorted(tutti)},
        "trigger_principale": dict(sorted(trigger_principale.items())),
        "chiamate": len(esito["chiamate"]),
        "eventi": sum(1 for v in esito["registro"] if len(v) > 2),
        "cambi_di_stato": sum(
            1 for v in esito["registro"] if len(v) > 2 and v[1] == EVENT_STATE_CHANGED
        ),
        "notifiche": len(esito["notifiche"]),
        "fermate": esito["fermate"],
        "cicli_infiniti": esito["cicli_infiniti"],
        "corsa_interrotta": esito.get("corsa_interrotta"),
    }


def _stampa_copertura(prova: Prova, dati: dict[str, Any]) -> None:
    passi = Counter(p[0] for p in prova.passi)
    virtuali = sum(p[1] for p in prova.passi if p[0] == "attendi") / 1e6
    print(
        f"\nseme {prova.seme}: {len(prova.passi)} passi {dict(passi)}, "
        f"inizio {prova.inizio.astimezone(FUSO).isoformat()}, "
        f"{virtuali:.0f} s virtuali (+60 di coda), {dati['fermate']} fermate; "
        f"confrontati: {dati['chiamate']} chiamate ai servizi finti, "
        f"{dati['cambi_di_stato']} cambi di stato, {dati['eventi']} eventi, "
        f"{dati['notifiche']} cambi delle notifiche"
    )
    for gruppo, titolo in (
        ("automazioni", "automazioni avviate"),
        ("script", "script avviati"),
    ):
        avviati = {k: v for k, v in dati[gruppo].items() if v}
        print(
            f"{titolo}: {len(avviati)}/{len(dati[gruppo])}: "
            + ", ".join(f"{k.split('.', 1)[1]}={v}" for k, v in avviati.items())
        )
    print(
        f"trigger diversi dell'Automazione VMC Master: {len(dati['trigger_principale'])}"
    )
    if dati["cicli_infiniti"]:
        print(
            f"CICLO INFINITO (più di {LIMITE_ISTANTE} eventi nello stesso istante) "
            f"a {dati['cicli_infiniti']} s"
        )
    if dati["corsa_interrotta"] is not None:
        print(f"CORSA INTERROTTA a {dati['corsa_interrotta']} s")


def confrontabile(esito: dict[str, Any]) -> dict[str, Any]:
    """Una corsa come si confronta (``nel_canale``): gli stati delle logiche (e gli
    annunci della memoria interna nella sequenza) non passano dal bus e possono passare
    prima degli eventi che Home Assistant tiene in coda; il registro e la sequenza con le
    voci esterne nel loro ordine e quelle interne nel loro, poi i contesti rinumerati in
    quest'ordine in tutti gli elenchi."""
    uscita = dict(esito)
    uscita["registro"] = ordine_esterno(esito["registro"], voce_interna)
    if "sequenza" in esito:
        uscita["sequenza"] = ordine_esterno(esito["sequenza"], voce_interna)
    chiavi = ["registro", *(k for k in uscita if k != "registro")]
    for chiave, valore in zip(
        chiavi, rinumera_ovunque(*(uscita[k] for k in chiavi)), strict=True
    ):
        uscita[chiave] = valore
    return uscita


def _confronta_corse(
    atteso: dict[str, Any], ottenuto: dict[str, Any], cosa: str
) -> None:
    """Home Assistant e motore, nell'ordine: chiamate ai servizi finti, cambi di stato,
    stati di automazioni e script, notifiche, fine delle chiamate del banco, stati finali
    e registro completo."""
    atteso, ottenuto = confrontabile(atteso), confrontabile(ottenuto)

    def cambi(esito: dict[str, Any]) -> list[Any]:
        return [
            v for v in esito["registro"] if len(v) > 2 and v[1] == EVENT_STATE_CHANGED
        ]

    for voce, chiave in (
        ("chiamate ai servizi finti", lambda e: e["chiamate"]),
        ("cambi di stato", cambi),
        ("stati di automazioni e script", lambda e: e["automazioni_script"]),
        ("notifiche persistenti", lambda e: e["notifiche"]),
        ("fine delle chiamate del banco", lambda e: e["fine_chiamate"]),
        ("stati finali", lambda e: e["stati"]),
        ("registri", lambda e: e["registro"]),
    ):
        if differenza := _confronta(chiave(atteso), chiave(ottenuto), voce):
            pytest.fail(f"{cosa}: {differenza}")
    assert ottenuto["notifiche_finali"] == atteso["notifiche_finali"]
    assert ottenuto["cicli_infiniti"] == atteso["cicli_infiniti"]
    assert ottenuto.get("corsa_interrotta") == atteso.get("corsa_interrotta")
    if "dei_timer" in atteso:
        for voce in ("dei_timer", "timer_finali"):
            if differenza := _confronta(atteso[voce], ottenuto[voce], voce):
                pytest.fail(f"{cosa}: {differenza}")
    if "stati_interni" in atteso:
        # fase 4, memoria interna: i cambi e le chiamate dei valori interni come quelli
        # della memoria, anche nell'ordine di tutto insieme
        for voce in ("interni", "chiamate_interne", "stati_interni", "sequenza"):
            if differenza := _confronta(atteso[voce], ottenuto[voce], voce):
                pytest.fail(f"{cosa}: {differenza}")


@pytest.mark.parametrize("seme", [VMC_SEME])
async def test_pacchetto_casuale(
    seme: int, freezer: FrozenDateTimeFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Stessa sequenza casuale con Home Assistant e con il motore tradotto: stesse
    chiamate ai servizi, stessi cambi di stato, stessi stati finali di automazioni e
    script, stesse notifiche, stesso registro degli eventi."""
    # Home Assistant sposta i trigger time_pattern di una frazione di secondo a caso: in
    # entrambe le corse la stessa
    monkeypatch.setattr(
        "homeassistant.helpers.event.randint", lambda minimo, massimo: minimo
    )
    prova = Generatore(seme).prova(VMC_PASSI)
    atteso = await _corsa(freezer, prova, motore=False)
    ottenuto = await _corsa(freezer, prova, motore=True)
    dati = copertura(atteso)
    _stampa_copertura(prova, dati)
    if VMC_RAPPORTO:
        Path(VMC_RAPPORTO).write_text(
            json.dumps({"seme": seme, "passi": len(prova.passi), **dati}, indent=1),
            encoding="utf-8",
        )
    _confronta_corse(atteso, ottenuto, f"seme {seme}")


@pytest.mark.parametrize("seme", [VMC_SEME])
async def test_pacchetto_casuale_timer_del_motore(
    seme: int, freezer: FrozenDateTimeFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Fase 4, i timer del package nel motore: la stessa sequenza casuale con Home
    Assistant (i suoi timer) e con il package tradotto con ``timer_motore`` sul motore
    con i timer del motore. Stessi eventi, chiamate, stati e notifiche di
    ``test_pacchetto_casuale`` senza gli eventi dei timer del package (i loro cambi di
    stato, i loro eventi e le chiamate ai loro servizi, che con i timer del motore non ci
    sono più); le scritture e gli eventi dei timer si confrontano a parte, dal registro dei
    timer del motore, con gli stati finali dei timer."""
    monkeypatch.setattr(
        "homeassistant.helpers.event.randint", lambda minimo, massimo: minimo
    )
    prova = Generatore(seme).prova(VMC_PASSI)
    atteso = await _corsa(freezer, prova, motore=False, timer_motore=True)
    ottenuto = await _corsa(freezer, prova, motore=True, timer_motore=True)
    dati = copertura(atteso)
    _stampa_copertura(prova, dati)
    voci = Counter(v[0] if v[0] == "stato" else v[2] for v in atteso["dei_timer"])
    print(
        f"registro dei timer: {len(atteso['dei_timer'])} voci {dict(sorted(voci.items()))}"
    )
    _confronta_corse(atteso, ottenuto, f"seme {seme}, timer del motore")


# Le finestre della scheda: gli input_boolean che le aprono (gli interruttori di funzione
# «opzioni_accendi_spegni_*» non lo sono), come in tests/test_b42.py.
FINESTRA = re.compile(
    r"^input_boolean\.vmc_master_(opzioni_(?!accendi_spegni_)[a-z_]+"
    r"|opzione_finestra_[a-z_]+|conferma_pulizia_cronologia)$"
)
AUTOMAZIONE_VMC = "automation.automazione_vmc_master"
# Interruttore e Spia dell'allerta Umidità: accesi insieme dalla scheda, con l'umidità
# sotto la soglia l'allerta finisce e dopo 4 s l'Automazione VMC Master rimanda la velocità
# registrata (Notturna) con il ciclo di conferma: resta occupata 5,05 s (misurato).
UMIDITA = "input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita"
SPIA_UMIDITA = "input_boolean.vmc_master_umidita_verifica_soglia_valore_spia"


def _prova_finestre() -> Prova:
    """La prova delle finestre: tutti gli input_boolean spenti tranne Interruttore e Spia
    Umidità (l'allerta finisce all'avvio), il resto dello stato del seme 1, la VMC
    accesa."""
    prova = Generatore(1).prova(0)
    prova.vmc.accesa = True
    prova.ripristino = [
        State(s.entity_id, "on" if s.entity_id in (UMIDITA, SPIA_UMIDITA) else "off")
        if s.entity_id.startswith("input_boolean.")
        else s
        for s in prova.ripristino
    ]
    return prova


def _istantanee_finestre(
    esito: dict[str, Any],
) -> list[tuple[float, int, int, list[str]]]:
    """Per ogni raffica (tocchi delle finestre nello stesso istante, riconosciuti dalle
    chiamate input_boolean con una sola finestra): istante, esecuzioni dell'Automazione
    VMC Master in corso subito prima dei tocchi e alla fine del loro istante (attributo
    ``current``), finestre aperte 40 s dopo."""
    registro = esito["registro"]
    raffiche = sorted(
        {
            v[0]
            for v in registro
            if len(v) > 2
            and v[1] == EVENT_CALL_SERVICE
            and v[2]["domain"] == "input_boolean"
            and isinstance(v[2]["service_data"].get("entity_id"), str)
            and FINESTRA.match(v[2]["service_data"]["entity_id"])
        }
    )
    uscita = []
    for istante in raffiche:
        prima = dopo = 0
        aperte: dict[str, str] = {}
        for v in registro:
            if len(v) < 3 or v[1] != EVENT_STATE_CHANGED:
                continue
            if v[0] > istante + 40:
                break
            entita, nuovo = v[2]["entity_id"], v[2]["new_state"]
            if nuovo is None:
                continue
            if entita == AUTOMAZIONE_VMC:
                if v[0] < istante:
                    prima = nuovo[2].get("current", 0)
                elif v[0] == istante:
                    dopo = nuovo[2].get("current", 0)
            elif FINESTRA.match(entita):
                aperte[entita] = nuovo[1]
        uscita.append(
            (
                istante,
                prima,
                dopo,
                sorted(
                    e.removeprefix("input_boolean.vmc_master_")
                    for e, s in aperte.items()
                    if s == "on"
                ),
            )
        )
    return uscita


async def test_tre_finestre_aperte_insieme(
    freezer: FrozenDateTimeFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Con tutte le finestre della scheda chiuse, Avvisi, Audio e Telecomando aperte
    nello stesso istante (tocchi veloci). Fino alla b41 le esecuzioni in coda
    dell'Automazione VMC Master (mode: queued) aprivano ognuna la propria finestra e
    chiudevano le altre, ogni apertura o chiusura ne accodava un'altra e il ciclo non
    finiva più (Home Assistant e motore entravano nel ciclo allo stesso evento, a 60,1 s).
    Dalla b42 ogni ramo delle finestre si esegue solo se la sua finestra è ancora nello
    stato del trigger e chiude solo le finestre aperte prima di lui: nessun ciclo, resta
    aperta l'ultima toccata (Telecomando, che chiude anche Audio; l'automazione è libera),
    Home Assistant e motore uguali. Riduzione dei cicli trovati dal banco casuale (semi 3
    e 4, 2000 passi, sulla b41)."""
    monkeypatch.setattr(
        "homeassistant.helpers.event.randint", lambda minimo, massimo: minimo
    )
    prova = Generatore(1).prova(0)
    chiuse = (
        "input_boolean.vmc_master_opzion",
        "input_boolean.vmc_master_spia",
        "input_boolean.vmc_master_conferma",
    )
    prova.ripristino = [
        State(s.entity_id, "off") if s.entity_id.startswith(chiuse) else s
        for s in prova.ripristino
    ]
    prova.passi = [
        ("attendi", 60_000_000),
        (
            "raffica",
            [
                ("input_boolean", "turn_on", {"entity_id": f"input_boolean.{nome}"})
                for nome in (
                    "vmc_master_opzioni_avvisi",
                    "vmc_master_opzione_finestra_audio",
                    "vmc_master_opzioni_vmc",
                )
            ],
        ),
        ("attendi", 10_000_000),
    ]
    atteso = await _corsa(freezer, prova, motore=False)
    ottenuto = await _corsa(freezer, prova, motore=True)
    assert atteso["cicli_infiniti"] == []
    assert "corsa_interrotta" not in atteso
    assert _istantanee_finestre(atteso) == [(60.1, 0, 0, ["opzioni_vmc"])]
    _confronta_corse(atteso, ottenuto, "tre finestre aperte insieme")


# (nome, tocchi nello stesso istante, finestre aperte alla fine con l'Automazione VMC
# Master libera e con l'automazione occupata), misurate con Home Assistant 2026.11.2 sul
# package della b42 (regola b42: con l'automazione libera resta aperta l'ultima toccata,
# con l'automazione occupata tutti gli eventi vanno in coda con lo stesso last_changed e
# resta la prima elaborata, cioè la prima toccata)
FINESTRE_INSIEME: list[tuple[str, list[tuple[str, str]], list[str], list[str]]] = [
    (
        "Avvisi, Audio e Telecomando",
        [
            ("opzioni_avvisi", "on"),
            ("opzione_finestra_audio", "on"),
            ("opzioni_vmc", "on"),
        ],
        ["opzioni_vmc"],  # Telecomando chiude anche Audio
        ["opzione_finestra_audio", "opzioni_avvisi"],  # Avvisi non chiude Audio
    ),
    (
        "Telecomando, Audio e Avvisi",
        [
            ("opzioni_vmc", "on"),
            ("opzione_finestra_audio", "on"),
            ("opzioni_avvisi", "on"),
        ],
        ["opzione_finestra_audio", "opzioni_avvisi"],
        ["opzioni_vmc"],  # Telecomando chiude Audio e Avvisi, aperte insieme
    ),
    (
        "Avvisi e Telecomando",
        [("opzioni_avvisi", "on"), ("opzioni_vmc", "on")],
        ["opzioni_vmc"],
        ["opzioni_avvisi"],
    ),
    (
        "Telecomando e Avvisi",
        [("opzioni_vmc", "on"), ("opzioni_avvisi", "on")],
        ["opzioni_avvisi"],
        ["opzioni_vmc"],
    ),
    (
        "Opzioni e la sua sotto-finestra Audio",
        [("opzioni_offset_sensori", "on"), ("opzione_finestra_audio", "on")],
        ["opzione_finestra_audio", "opzioni_offset_sensori"],
        ["opzioni_offset_sensori"],  # « Opzioni On» chiude Audio aperta insieme
    ),
    (
        "Audio e Opzioni",
        [("opzione_finestra_audio", "on"), ("opzioni_offset_sensori", "on")],
        ["opzioni_offset_sensori"],  # « Opzioni On» chiude Audio, aperta prima
        ["opzioni_offset_sensori"],  # e anche aperta insieme
    ),
    (
        "Avvisi aperta, chiusa e riaperta",
        [
            ("opzioni_avvisi", "on"),
            ("opzioni_avvisi", "off"),
            ("opzioni_avvisi", "on"),
        ],
        ["opzioni_avvisi"],  # vince l'ultimo tocco
        ["opzioni_avvisi"],
    ),
]


@pytest.mark.parametrize("occupata", [False, True], ids=["libera", "occupata"])
async def test_finestre_toccate_insieme(
    occupata: bool, freezer: FrozenDateTimeFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Le 7 raffiche di FINESTRE_INSIEME (due finestre che si chiudono a vicenda nei due
    ordini, le tre di ``test_tre_finestre_aperte_insieme`` nei due ordini, una finestra
    aperta, chiusa e riaperta), una ogni 100 s con tutte le finestre chiuse prima, con
    l'Automazione VMC Master libera o occupata (un'esecuzione lunga vera in corso: il
    rinvio della velocità registrata con il ciclo di conferma dopo la fine dell'allerta
    Umidità, che parte 4 s dopo l'accensione di Interruttore e Spia Umidità; i tocchi
    arrivano 1 s dopo e vanno tutti in coda). Sulla b41 queste raffiche erano il ciclo senza
    fine; dalla b42: nessun ciclo, le finestre aperte attese e Home Assistant e motore
    uguali in tutto (chiamate, cambi di stato, registro)."""
    monkeypatch.setattr(
        "homeassistant.helpers.event.randint", lambda minimo, massimo: minimo
    )
    prova = _prova_finestre()
    finestre = sorted(
        f"input_boolean.{nome}"
        for nome in _package()["input_boolean"]
        if FINESTRA.match(f"input_boolean.{nome}")
    )
    prova.passi = [("attendi", 300_000_000)]  # dopo i comandi dell'avvio
    for _, tocchi, _, _ in FINESTRE_INSIEME:
        prova.passi.append(
            ("servizio", "input_boolean", "turn_off", {"entity_id": finestre})
        )
        if occupata:
            prova.passi.append(
                (
                    "servizio",
                    "input_boolean",
                    "turn_on",
                    {"entity_id": [UMIDITA, SPIA_UMIDITA]},
                )
            )
        prova.passi += [
            ("attendi", 5_000_000),
            (
                "raffica",
                [
                    (
                        "input_boolean",
                        f"turn_{verso}",
                        {"entity_id": f"input_boolean.vmc_master_{nome}"},
                    )
                    for nome, verso in tocchi
                ],
            ),
            ("attendi", 95_000_000),
        ]
    atteso = await _corsa(freezer, prova, motore=False)
    ottenuto = await _corsa(freezer, prova, motore=True)
    assert atteso["cicli_infiniti"] == []
    assert "corsa_interrotta" not in atteso
    istantanee = _istantanee_finestre(atteso)
    assert [i[0] for i in istantanee] == [305.1 + 100 * k for k in range(7)]
    for (nome, tocchi, libera, con_occupata), (_, prima, dopo, aperte) in zip(
        FINESTRE_INSIEME, istantanee, strict=True
    ):
        if occupata:
            # l'esecuzione lunga e dietro di lei in coda un evento per ogni tocco
            assert (prima, dopo) == (1, 1 + len(tocchi)), nome
            assert aperte == con_occupata, nome
        else:
            assert prima == 0, nome
            assert aperte == libera, nome
    _confronta_corse(atteso, ottenuto, f"finestre toccate insieme, occupata={occupata}")


@pytest.mark.parametrize("seme", [VMC_SEME])
async def test_pacchetto_casuale_script_interni(
    seme: int, freezer: FrozenDateTimeFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Fase 4: la stessa sequenza casuale con gli script e gli shell_command di Home
    Assistant e con gli script e i comandi dentro il motore (tradotti con
    ``comandi=...``): stesse chiamate (i comandi dall'aggancio diretto), stessi cambi di
    stato, stessi stati finali, stesse notifiche, stesso registro, tolti lo stato degli
    script, ``script_started`` e le chiamate ``script.*`` e ``shell_command.*``. I
    comandi finti durano come quelli veri in entrambe le corse."""
    monkeypatch.setattr(
        "homeassistant.helpers.event.randint", lambda minimo, massimo: minimo
    )
    nome = f"casuale_interni_{seme}"
    async with async_test_home_assistant() as hass:
        automazioni, script = leggi_package()
        testo_modelli, testo_motore = await traduci_configurazione(
            hass,
            automazioni,
            script,
            nome_modelli=f"{nome}_modelli",
            comandi=leggi_comandi(),
        )
        await hass.async_stop(force=True)
    moduli = [
        f"{generato.__name__}.{nome}_modelli",
        f"{generato.__name__}.{nome}_motore",
    ]
    try:
        _carica(f"{nome}_modelli", testo_modelli)
        codice = _carica(f"{nome}_motore", testo_motore)
        prova = Generatore(seme).prova(VMC_PASSI)
        atteso = await _corsa(freezer, prova, motore=False, fedeli=True)
        ottenuto = await _corsa(freezer, prova, motore=True, fedeli=True, codice=codice)
    finally:
        for modulo in moduli:
            sys.modules.pop(modulo, None)
    print(f"\neventi tolti (seme {seme}, {len(prova.passi)} passi): {atteso['tolti']}")
    assert ottenuto["tolti"] == Counter()
    assert sum(1 for c in atteso["chiamate"] if c[1] == "shell_command")
    _confronta_corse(atteso, ottenuto, f"seme {seme}, script interni")


@pytest.mark.parametrize("seme", [VMC_SEME])
async def test_pacchetto_casuale_script_interni_e_timer_del_motore(
    seme: int, freezer: FrozenDateTimeFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Fase 4, tutto insieme: il package tradotto con gli script e i comandi dentro il
    motore (``comandi=...``) e con i timer del motore (``timer_motore``) contro Home
    Assistant con i suoi script, shell_command e timer. Tolti gli eventi che non ci sono
    più (degli script, dei comandi e dei timer del package), stesse chiamate, stessi
    cambi di stato, stati finali, notifiche e registro; le scritture e gli eventi dei
    timer si confrontano dal registro dei timer del motore."""
    monkeypatch.setattr(
        "homeassistant.helpers.event.randint", lambda minimo, massimo: minimo
    )
    nome = f"casuale_interni_timer_{seme}"
    async with async_test_home_assistant() as hass:
        automazioni, script = leggi_package()
        testo_modelli, testo_motore = await traduci_configurazione(
            hass,
            automazioni,
            script,
            nome_modelli=f"{nome}_modelli",
            comandi=leggi_comandi(),
            timer_motore=True,
        )
        await hass.async_stop(force=True)
    moduli = [
        f"{generato.__name__}.{nome}_modelli",
        f"{generato.__name__}.{nome}_motore",
    ]
    try:
        _carica(f"{nome}_modelli", testo_modelli)
        codice = _carica(f"{nome}_motore", testo_motore)
        prova = Generatore(seme).prova(VMC_PASSI)
        atteso = await _corsa(
            freezer, prova, motore=False, timer_motore=True, fedeli=True
        )
        ottenuto = await _corsa(
            freezer, prova, motore=True, timer_motore=True, fedeli=True, codice=codice
        )
    finally:
        for modulo in moduli:
            sys.modules.pop(modulo, None)
    _stampa_copertura(prova, copertura(atteso))
    voci = Counter(v[0] if v[0] == "stato" else v[2] for v in atteso["dei_timer"])
    print(
        f"\neventi tolti (seme {seme}, {len(prova.passi)} passi): {atteso['tolti']}; "
        f"registro dei timer: {len(atteso['dei_timer'])} voci "
        f"{dict(sorted(voci.items()))}"
    )
    assert ottenuto["tolti"] == Counter()
    assert sum(1 for c in atteso["chiamate"] if c[1] == "shell_command")
    assert any(v[0] == "evento" for v in ottenuto["dei_timer"])
    _confronta_corse(
        atteso, ottenuto, f"seme {seme}, script interni e timer del motore"
    )
