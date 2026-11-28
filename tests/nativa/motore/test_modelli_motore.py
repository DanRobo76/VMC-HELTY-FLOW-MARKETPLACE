"""Ogni modello del package tradotto in Python si comporta come in Home Assistant.

Banco a caso: a ogni giro le entità citate nei modelli prendono stati e attributi (a caso,
oppure valori realistici letti dal package: ``valori_package.py``), l'orologio un istante a
caso, e ogni modello si rende con variabili (``trigger``, ``repeat`` e le variabili del
package, a caso o realistiche) da Home Assistant e dalla funzione tradotta. Per ogni resa
si confrontano:

- il testo: ``Template.async_render(parse_result=False)`` / ``Contesto.testo`` (stesso
  testo, o errore con lo stesso messaggio in tutti e due);
- il risultato interpretato: ``Template.async_render`` / ``ModelloHA.async_render`` e
  ``Contesto.resa_complessa``: stesso tipo Python (anche dentro liste, tuple, insiemi e
  dizionari: ``True`` non è ``1``, ``1.0`` non è ``1``, le liste di Home Assistant non sono
  ``list``) e stesso valore (``nan`` uguale a ``nan``), stesso testo scritto;
- la ``RenderInfo`` di ``async_render_to_info``, con e senza interpretazione: entità,
  domini, ``all_states``, ``all_states_lifecycle``, ``domains_lifecycle``, ``has_time``,
  ``rate_limit``, ``is_static``, i filtri scelti (``filter``, ``filter_lifecycle``, provati
  sulle entità lette, su una entità per dominio del package e su entità di altri domini)
  e l'errore (classe e messaggio): sono quello che ascoltano i trigger ``template`` e i
  ``wait_template``;
- l'esito come condizione ``template``: ``condition.async_template`` di Home Assistant /
  ``Contesto.condizione``: stesso booleano, o ``ConditionError`` con lo stesso messaggio.

Oltre ai giri a caso c'è un giro «mirato»: per ogni modello, ogni valore di ogni suo
confronto (``trigger.id == '...'``, ``states('x') == '...'``, ``x | float > 25``...) almeno
una volta, e alcuni scenari scritti a mano (``SCENARI``). ``VMC_GIRI`` cambia il numero
dei giri a caso (50), ``VMC_SEME`` il seme dei numeri a caso.
"""

from __future__ import annotations

import logging
import math
import os
import random
import re
from collections import Counter
from collections.abc import Callable, Iterator
from datetime import UTC, datetime, timedelta
from functools import partial
from typing import Any

import pytest
from freezegun.api import FrozenDateTimeFactory
from homeassistant.core import Context, Event, HomeAssistant, State, valid_entity_id
from homeassistant.exceptions import ConditionError, TemplateError
from homeassistant.helpers import condition
from homeassistant.helpers.template import (
    ResultWrapper,
    Template,
    TemplateEnvironment,
    render_complex,
)
from homeassistant.helpers.template.render_info import RenderInfo
from homeassistant.util import dt as dt_util

from custom_components.vmc_master.nativa.motore import jinja as J
from custom_components.vmc_master.nativa.motore.contesto import Contesto, ModelloHA
from custom_components.vmc_master.nativa.motore.esecuzione import Modello
from custom_components.vmc_master.trasforma import rinomina

from . import valori_package as P
from .generato import modelli as M
from .traduci import traduzione
from .traduci_jinja import Traduttore

GIRI = int(os.environ.get("VMC_GIRI", "50"))
SEME = int(os.environ.get("VMC_SEME", "20261125"))
VARIANTI = 2
ATTRIBUTO = re.compile(r"state_attr\(\s*'([a-z0-9_.]+)'\s*,\s*'([a-z0-9_]+)'")
_INDIRIZZO = re.compile(r" at 0x[0-9a-fA-F]+")
BOOLEANI = {
    "input_boolean",
    "binary_sensor",
    "switch",
    "automation",
    "script",
    "fan",
    "light",
}
NUMERI = [
    0,
    1,
    2,
    3,
    4,
    5,
    7,
    10,
    12.3,
    15,
    18,
    21.5,
    25,
    30,
    45.7,
    60,
    80,
    100,
    450,
    1200,
    -5,
]
# Entità di altri domini (per provare i filtri della RenderInfo).
ALTRE = ["sensor.altro", "light.altra", "media_player.altro", "zone.home"]
# Entità di un'installazione vera che i modelli cercano tra tutti gli stati (sensori per
# classe, meteo, lettori multimediali, l'IP delle altre VMC), con i loro attributi.
INSTALLAZIONE: dict[str, dict[str, Any]] = {
    "sensor.temperatura_salotto": {"device_class": "temperature"},
    "sensor.umidita_bagno": {"device_class": "humidity"},
    "sensor.co2_cucina": {"device_class": "carbon_dioxide"},
    "sensor.vmc_master_temperatura_esterna_selezionata": {
        "device_class": "temperature"
    },
    "weather.casa": {"temperature": 12.5, "humidity": 70},
    "weather.spento": {},
    "media_player.salotto": {"friendly_name": "Salotto"},
    "sensor.vmc_cucina_ip": {"restored": False},
    "sensor.vmc_bagno_ip": {"restored": True},
}
# Scenari scritti a mano per i rami che i valori dei confronti non raggiungono da soli:
# un pezzo del testo del modello, stati (stato, attributi) e variabili.
SCENARI: list[tuple[str, dict[str, tuple[str, dict[str, Any]]], dict[str, Any]]] = [
    # l'IP scelto è già di un'altra VMC (sensore non ripristinato con lo stesso IP)
    (
        "selectattr('entity_id', 'search', '^sensor\\.vmc_[a-z]+_ip$')",
        {"sensor.vmc_cucina_ip": (" 192.168.1.60", {"restored": False})},
        {"ip": "192.168.1.60"},
    ),
    # comandi ancora «in viaggio» (indici dei comandi tra le ultime 8 scritture)
    (
        "{%- if loop.index0 in in_viaggio -%}",
        {
            "input_text.vmc_master_ultimi_comandi_automazione": (
                "100|105|90|0|120|80|70|60",
                {},
            )
        },
        {"in_viaggio": [0, 2, 5], "indice": 1, "ts_scelta": 95.0},
    ),
]
# Valori scritti a mano per le entità e le variabili con un formato (indirizzi IP, nomi).
IP = [
    "192.168.1.50",
    "192.168.1.60",
    "10.0.0.7",
    "10.0.0.256",
    "127.0.0.1",
    "169.254.1.1",
    "",
]
FATTI: dict[P.Soggetto, list[Any]] = {
    ("stato", "input_text.vmc_master_ip_insert"): [*IP, " 192.168.1.60 "],
    ("stato", "sensor.vmc_master_ip"): IP,
    ("stato", "sensor.vmc_cucina_ip"): IP,
    ("stato", "sensor.vmc_bagno_ip"): IP,
    ("stato", "input_text.vmc_master_nome_da_inserire"): [
        "cucina",
        "Bagno-2",
        "",
        "x" * 11,
    ],
    ("var", "ip"): IP,
}


def _letterali(analisi: dict[str, P.Analisi]) -> tuple[list[str], list[Any]]:
    """I testi e i numeri scritti nei modelli e quelli dei loro confronti (candidati per
    stati e variabili)."""
    testi: set[str] = set()
    numeri: set[Any] = set()
    for voce in analisi.values():
        testi |= voce.testi
        numeri |= voce.numeri
        for valori in voce.candidati.values():
            for valore in valori:
                if isinstance(valore, str) and len(valore) < 80:
                    testi.add(valore)
                elif isinstance(valore, (int, float)) and not isinstance(valore, bool):
                    numeri.add(valore)
    return sorted(testi), sorted(numeri)


class Banco:
    """Stati e variabili per i modelli del package: a caso e realistici."""

    def __init__(
        self,
        hass: HomeAssistant,
        sorgenti: list[str],
        package: P.Package,
        modelli: dict[str, Template],
    ) -> None:
        self.hass = hass
        self.rng = random.Random(SEME)
        self.package = package
        self.modelli = modelli
        globali = set(TemplateEnvironment(hass).globals)
        self.analisi = {s: P.analizza(s) for s in sorgenti}
        for voce in self.analisi.values():
            voce.nomi -= globali
        testo = "\n".join(sorgenti)
        self.entita = sorted(
            e
            for e in set(P.ENTITA.findall(testo))
            | set(package.definizioni)
            | set(INSTALLAZIONE)
            if valid_entity_id(e) and not e.endswith("_")
        )
        self.attributi: dict[str, set[str]] = {}
        for entita, nome in ATTRIBUTO.findall(testo):
            self.attributi.setdefault(entita, set()).add(nome)
        self.testi, numeri = _letterali(self.analisi)
        self.numeri = sorted({*NUMERI, *numeri}, key=float)
        # Valori di ogni soggetto in tutti i modelli (gli stati di un'entità confrontati
        # da qualsiasi modello, gli id dei trigger, i campi di una variabile...).
        self.globali: dict[P.Soggetto, list[Any]] = {}
        for voce in self.analisi.values():
            for soggetto, valori in voce.candidati.items():
                for valore in valori:
                    _aggiungi(self.globali.setdefault(soggetto, []), valore)
        for soggetto in list(self.globali):
            if soggetto[0] == "stato":
                self.globali[soggetto] = [
                    v for v in self.globali[soggetto] if not isinstance(v, (list, dict))
                ]
        for entita, config in package.definizioni.items():
            for opzione in config.get("options") or []:
                _aggiungi(self.globali.setdefault(("stato", entita), []), opzione)
        for soggetto, valori in FATTI.items():
            for valore in valori:
                _aggiungi(self.globali.setdefault(soggetto, []), valore)
        # Gli stati delle entità sì/no: anche l'altro valore.
        for voce in self.analisi.values():
            for soggetto in list(voce.candidati):
                if soggetto[0] == "stato" and soggetto[1].split(".", 1)[0] in BOOLEANI:
                    voce.aggiungi(soggetto, "on")
                    voce.aggiungi(soggetto, "off")
        # I trigger del package per id: (automazione, indice).
        self.trigger_per_id: dict[str, list[tuple[int, int]]] = {}
        for automazione, trigger in enumerate(package.trigger):
            for indice, config in enumerate(trigger):
                self.trigger_per_id.setdefault(
                    str(config.get("id", indice)), []
                ).append((automazione, indice))
        self._cache_soggetti: dict[str, Any] = {}
        # Valori realistici delle variabili e degli aiutanti: resi a ogni giro.
        self.realistici: dict[str, list[Any]] = {}
        self.scritti: dict[str, list[Any]] = {}
        self.elementi: list[Any] = []

    # --- valori a caso -------------------------------------------------------------------

    def valore(self) -> Any:
        r = self.rng.random()
        if r < 0.35:
            return self.rng.choice(self.testi)
        if r < 0.7:
            return self.rng.choice(self.numeri)
        if r < 0.8:
            return self.rng.choice([True, False])
        if r < 0.85:
            return None
        if r < 0.92:
            return str(self.rng.choice(self.numeri))
        return self.rng.sample(self.testi, 3)

    def stato(self, entity_id: str) -> str:
        rng = self.rng
        dominio = entity_id.split(".", 1)[0]
        if rng.random() < 0.08:
            return rng.choice(["unavailable", "unknown"])
        r = rng.random()
        if r < 0.4 and (valori := self.globali.get(("stato", entity_id))):
            return str(rng.choice(valori))
        if r < 0.55 and (valori := self.scritti.get(entity_id)):
            return str(rng.choice(valori))
        definizione = self.package.definizioni.get(entity_id, {})
        if dominio in BOOLEANI:
            return rng.choice(["on", "off"])
        if dominio == "input_select" and definizione.get("options"):
            return str(rng.choice(definizione["options"]))
        if dominio in ("input_number", "number", "counter"):
            if definizione and rng.random() < 0.5:
                minimo = float(definizione.get("min", 0))
                massimo = min(float(definizione.get("max", 100)), minimo + 1000)
                passo = float(definizione.get("step", 1))
                return str(
                    round(
                        minimo
                        + passo * rng.randrange(int((massimo - minimo) / passo) + 1),
                        6,
                    )
                )
            return str(float(rng.choice(self.numeri)))
        if dominio == "timer":
            return rng.choice(["idle", "active", "paused"])
        if dominio == "input_datetime":
            if definizione.get("has_date") and not definizione.get("has_time"):
                return rng.choice(["2026-11-25", "2026-01-01"])
            return rng.choice(
                ["2026-11-25 08:30:00", "2026-01-01 00:00:00", "07:15:00", "22:00:00"]
            )
        if entity_id in self.package.numerici and rng.random() < 0.6:
            return str(rng.choice([*self.numeri, 0.0, 19.4, 55.0, 850]))
        r = rng.random()
        if r < 0.45:
            return rng.choice(self.testi)
        if r < 0.85:
            return str(rng.choice(self.numeri))
        return rng.choice(["", "on", "off", "None", "2026-11-25T09:00:00+00:00"])

    def attributi_di(self, entity_id: str) -> dict[str, Any]:
        rng = self.rng
        attributi: dict[str, Any] = {}
        for nome in sorted(self.attributi.get(entity_id, ())):
            valori = self.globali.get(("attributo", entity_id, nome))
            attributi[nome] = (
                rng.choice(valori) if valori and rng.random() < 0.5 else self.valore()
            )
        dominio = entity_id.split(".", 1)[0]
        adesso = dt_util.utcnow()
        if dominio == "timer" and rng.random() < 0.8:
            durata = timedelta(seconds=rng.choice([0, 5, 59, 60, 300, 3600, 5400]))
            attributi.setdefault("duration", str(durata))
            attributi.setdefault("remaining", str(durata / 2))
            attributi.setdefault(
                "finishes_at",
                (
                    adesso + timedelta(seconds=rng.choice([-30, 0, 1, 7, 90, 1800]))
                ).isoformat(),
            )
        if dominio == "input_datetime":
            definizione = self.package.definizioni.get(entity_id, {})
            attributi.update(
                has_date=bool(definizione.get("has_date")),
                has_time=bool(definizione.get("has_time", True)),
                hour=rng.randrange(24),
                minute=rng.choice([0, 15, 30, 59]),
                second=0,
                timestamp=rng.choice([0, 27000, 79200, 1764059400.0]),
            )
        if rng.random() < 0.5:
            attributi["friendly_name"] = rng.choice(self.testi)
        if entity_id in INSTALLAZIONE and rng.random() < 0.9:
            attributi.update(INSTALLAZIONE[entity_id])
        return attributi

    def giro(self, freezer: FrozenDateTimeFactory) -> None:
        """Nuovi stati per tutte le entità, un nuovo istante, nuovi valori realistici."""
        rng = self.rng
        freezer.move_to(
            datetime(2026, 1, 1, tzinfo=UTC)
            + timedelta(days=rng.randrange(365), seconds=rng.randrange(86400))
        )
        for entity_id in self.entita:
            self.hass.states.async_set(
                entity_id, self.stato(entity_id), self.attributi_di(entity_id)
            )
        self._realistici()

    def _rendi(self, valore: Any, V: dict[str, Any]) -> Any:
        """Un valore del package come lo rende Home Assistant (``render_complex``)."""
        return render_complex(self._come_template(valore), V)

    def _come_template(self, valore: Any) -> Any:
        if P.e_modello(valore):
            return self.modelli[valore.strip()]
        if isinstance(valore, list):
            return [self._come_template(v) for v in valore]
        if isinstance(valore, dict):
            return {k: self._come_template(v) for k, v in valore.items()}
        return valore

    def _realistici(self) -> None:
        """Le variabili e gli aiutanti come li assegna il package, resi da Home Assistant
        con gli stati del giro (in ordine: una variabile vede le precedenti)."""
        visti: dict[str, Any] = {}
        for gruppo, archivio in (
            (self.package.variabili, self.realistici),
            (self.package.scritture, self.scritti),
            (self.package.per_ogni, None),
        ):
            for assegnazione in gruppo:
                V = self._variabili_base(assegnazione.automazione, visti)
                try:
                    valore = self._rendi(assegnazione.valore, V)
                except TemplateError:
                    continue
                if archivio is None:
                    for elemento in valore if isinstance(valore, list) else []:
                        _aggiungi(self.elementi, elemento, 40)
                    continue
                if archivio is self.realistici:
                    visti[assegnazione.nome] = valore
                _aggiungi(archivio.setdefault(assegnazione.nome, []), valore, 12)

    def _variabili_base(
        self, automazione: int | None, visti: dict[str, Any]
    ) -> dict[str, Any]:
        V = dict(visti)
        if automazione is not None and self.package.trigger[automazione]:
            indice = self.rng.randrange(len(self.package.trigger[automazione]))
            V["trigger"] = self.trigger_reale(automazione, indice)
        return V

    # --- trigger -------------------------------------------------------------------------

    def _stato_trigger(self, entity_id: str, voluto: Any) -> State:
        stato = voluto if isinstance(voluto, str) else self.stato(entity_id)
        attuale = self.hass.states.get(entity_id)
        return State(entity_id, stato, attuale.attributes if attuale else None)

    def trigger_reale(self, automazione: int, indice: int) -> dict[str, Any]:
        """Le variabili di un trigger dell'automazione come le crea Home Assistant."""
        config = self.package.trigger[automazione][indice]
        piattaforma = config["trigger"]
        trigger: dict[str, Any] = {
            "id": str(config.get("id", indice)),
            "idx": str(indice),
            "alias": config.get("alias"),
            "platform": piattaforma,
        }
        if piattaforma in ("state", "template"):
            if piattaforma == "state":
                entita = P.lista(config.get("entity_id"))
            else:
                entita = P.ENTITA.findall(str(config.get("value_template", "")))
            entity_id = self.rng.choice(entita) if entita else None
            trigger["entity_id"] = entity_id
            if entity_id is None:
                trigger.update(from_state=None, to_state=None)
            else:
                prima = config.get("from")
                dopo = config.get("to")
                trigger["from_state"] = (
                    None
                    if self.rng.random() < 0.1
                    else self._stato_trigger(
                        entity_id, P.lista(prima)[0] if prima else None
                    )
                )
                trigger["to_state"] = self._stato_trigger(
                    entity_id, P.lista(dopo)[0] if dopo else None
                )
            trigger["for"] = None
            if piattaforma == "state":
                trigger["attribute"] = config.get("attribute")
            trigger["description"] = f"{piattaforma} of {entity_id}"
        elif piattaforma == "event":
            dati = dict(config.get("event_data") or {})
            if config.get("event_type") == "timer.finished":
                timer = [e for e in self.entita if e.startswith("timer.")]
                dati["entity_id"] = self.rng.choice(timer)
            trigger["event"] = Event(
                config.get("event_type", "evento"),
                dati,
                context=Context(user_id=self.rng.choice([None, "utente"])),
            )
            trigger["description"] = f"event '{config.get('event_type')}'"
        elif piattaforma == "homeassistant":
            trigger["event"] = config.get("event", "start")
            trigger["description"] = "Home Assistant starting"
        else:
            trigger["now"] = dt_util.now()
            trigger["description"] = piattaforma
            if piattaforma == "time":
                trigger["entity_id"] = None
        return trigger

    def trigger_casuale(self) -> dict[str, Any]:
        rng = self.rng
        entity_id = rng.choice(self.entita)
        return {
            "platform": rng.choice(
                ["state", "template", "event", "time", "homeassistant"]
            ),
            "id": rng.choice(self.testi),
            "idx": str(rng.randrange(5)),
            "alias": None,
            "entity_id": entity_id,
            "from_state": State(entity_id, self.stato(entity_id)),
            "to_state": self.hass.states.get(entity_id),
            "for": None,
            "description": "prova",
        }

    # --- variabili di un modello ---------------------------------------------------------

    def candidati(self, sorgente: str, soggetto: P.Soggetto) -> list[Any]:
        """I valori di un soggetto: prima quelli del modello, poi quelli di tutti."""
        propri = self.analisi[sorgente].candidati.get(soggetto)
        if propri and self.rng.random() < 0.7:
            return propri
        return self.globali.get(soggetto) or propri or []

    def scegli(
        self,
        sorgente: str,
        soggetto: P.Soggetto,
        forzato: tuple[P.Soggetto, Any] | None,
    ) -> tuple[bool, Any]:
        """Il valore di un soggetto confrontato dal modello: quello forzato, uno dei
        valori dei confronti, oppure nessuno (resta quello a caso: l'altro ramo)."""
        if forzato is not None and forzato[0] == soggetto:
            return True, forzato[1]
        if self.rng.random() < 0.4:
            return False, None
        valori = self.candidati(sorgente, soggetto)
        if not valori or self.rng.random() < 1 / (len(valori) + 2):
            return False, None
        return True, self.rng.choice(valori)

    def mira_stati(
        self, sorgente: str, forzato: tuple[P.Soggetto, Any] | None = None
    ) -> None:
        """Gli stati e gli attributi confrontati dal modello presi tra i valori dei suoi
        confronti (``scegli``; ``forzato`` sempre)."""
        nuovi: dict[str, tuple[str | None, dict[str, Any]]] = {}
        for soggetto, radice in self._soggetti(sorgente)[0]:
            scelto, valore = self.scegli(sorgente, soggetto, forzato)
            if not scelto:
                continue
            if soggetto[0] == "parte":
                valore = self._parte(soggetto, valore)
            stato, attributi = nuovi.get(radice[1], (None, {}))
            if radice[0] == "stato":
                stato = str(valore)
            else:
                attributi[radice[2]] = valore
            nuovi[radice[1]] = (stato, attributi)
        for entity_id, (stato, attributi) in nuovi.items():
            if not valid_entity_id(entity_id):
                continue
            attuale = self.hass.states.get(entity_id)
            self.hass.states.async_set(
                entity_id,
                stato if stato is not None else (attuale.state if attuale else "on"),
                {**(attuale.attributes if attuale else {}), **attributi},
            )

    def _soggetti(
        self, sorgente: str
    ) -> tuple[
        list[tuple[P.Soggetto, P.Soggetto]], list[tuple[P.Soggetto, P.Soggetto]]
    ]:
        """I soggetti dei confronti del modello con la loro radice (uno stato o un
        attributo; una variabile): quelli dentro un ``split`` hanno la radice fuori."""
        if (fatti := self._cache_soggetti.get(sorgente)) is None:
            stati: list[tuple[P.Soggetto, P.Soggetto]] = []
            variabili: list[tuple[P.Soggetto, P.Soggetto]] = []
            for soggetto in self.analisi[sorgente].candidati:
                radice = soggetto
                while radice[0] == "parte":
                    radice = radice[1]
                if radice[0] in ("stato", "attributo"):
                    stati.append((soggetto, radice))
                elif radice[0] == "var":
                    variabili.append((soggetto, radice))
            fatti = self._cache_soggetti[sorgente] = (stati, variabili)
        return fatti

    def _parte(self, soggetto: P.Soggetto, valore: Any) -> str:
        """Un testo con ``valore`` al posto ``indice`` dopo ``split(separatore)``."""
        _parte, _radice, separatore, indice = soggetto
        if indice < 0:
            parti = ["0"] * (-indice - 1)
            return separatore.join(
                [str(self.rng.choice(self.testi)), str(valore), *parti]
            )
        parti = [
            str(self.rng.choice(["0", "1", *self.testi[:5]])) for _ in range(indice)
        ]
        coda = [
            str(self.rng.choice(["0", "scheda", ""]))
            for _ in range(self.rng.randrange(3))
        ]
        return separatore.join([*parti, str(valore), *coda])

    def variabili(
        self, sorgente: str, forzato: tuple[P.Soggetto, Any] | None = None
    ) -> dict[str, Any]:
        """Le variabili per una resa del modello: a caso, realistiche (come le assegna il
        package, i trigger della sua automazione) o prese dai suoi confronti."""
        rng = self.rng
        analisi = self.analisi[sorgente]
        V: dict[str, Any] = {"context": Context()}
        automazioni = sorted(self.package.automazioni_di.get(sorgente, ()))
        reale = False
        if "trigger" in analisi.nomi:
            r = rng.random()
            per_id = [
                voce
                for identificativo in analisi.candidati.get(
                    ("var", "trigger", "id"), []
                )
                for voce in self.trigger_per_id.get(identificativo, [])
                if voce[0] in automazioni
            ]
            if forzato is not None and forzato[0] == ("var", "trigger", "id"):
                # un id dei trigger della sua automazione: quel trigger
                per_id = [
                    voce
                    for voce in self.trigger_per_id.get(forzato[1], [])
                    if voce[0] in automazioni
                ]
                r = 0 if per_id else 1
            if per_id and r < 0.35:
                V["trigger"] = self.trigger_reale(*rng.choice(per_id))
                reale = True
            elif automazioni and r < 0.6:
                automazione = rng.choice(automazioni)
                indice = rng.randrange(len(self.package.trigger[automazione]))
                V["trigger"] = self.trigger_reale(automazione, indice)
            elif r < 0.9 or sorgente not in self.package.negli_script:
                V["trigger"] = self.trigger_casuale()
        if "repeat" in analisi.nomi:
            V["repeat"] = {
                "index": (indice := rng.randint(1, 6)),
                "first": indice == 1,
                "last": rng.random() < 0.3,
            }
            if self.elementi and rng.random() < 0.8:
                V["repeat"]["item"] = rng.choice(self.elementi)
        for nome in sorted(analisi.nomi - {"trigger", "repeat"}):
            r = rng.random()
            if r < 0.08:
                continue
            # realistiche (come le assegna il package), dai valori scritti a mano, a caso
            if (r < 0.45 and (valori := self.realistici.get(nome))) or (
                r < 0.6 and (valori := self.globali.get(("var", nome)))
            ):
                V[nome] = rng.choice(valori)
            else:
                V[nome] = self.valore()
        # i percorsi delle variabili confrontati dal modello
        for soggetto, radice in self._soggetti(sorgente)[1]:
            if radice[1] not in V and radice[1] != "trigger":
                continue
            if reale and radice[:3] in (
                ("var", "trigger", "id"),
                ("var", "trigger", "platform"),
            ):
                continue  # il trigger vero della sua automazione resta com'è
            scelto, valore = self.scegli(sorgente, soggetto, forzato)
            if not scelto:
                continue
            if soggetto[0] == "parte":
                valore = self._parte(soggetto, valore)
            self._imposta(V, radice[1:], valore)
        return V

    def _imposta(
        self, V: dict[str, Any], percorso: tuple[Any, ...], valore: Any
    ) -> None:
        """``V[a][b][c] = valore``, creando dizionari, liste e stati dove servono."""
        nome, *resto = percorso
        if not resto:
            V[nome] = valore
            return
        if nome == "trigger":
            trigger = V.setdefault("trigger", self.trigger_casuale())
            chiave, *coda = resto
            if chiave in ("to_state", "from_state") and coda:
                entity_id = trigger.get("entity_id") or self.rng.choice(self.entita)
                vecchio = trigger.get(chiave)
                if coda == ["state"]:
                    trigger[chiave] = State(
                        entity_id, str(valore), vecchio.attributes if vecchio else None
                    )
                elif coda[0] == "attributes" and len(coda) == 2:
                    attributi = dict(vecchio.attributes) if vecchio else {}
                    attributi[coda[1]] = valore
                    trigger[chiave] = State(
                        entity_id, vecchio.state if vecchio else "on", attributi
                    )
                return
            if chiave == "event" and coda:
                vecchio = trigger.get("event")
                dati = dict(vecchio.data) if isinstance(vecchio, Event) else {}
                utente = None
                if coda[0] == "data" and len(coda) == 2:
                    dati[coda[1]] = valore
                elif coda[:2] == ["context", "user_id"]:
                    utente = valore
                trigger["event"] = Event(
                    "call_service", dati, context=Context(user_id=utente)
                )
                return
            self._annida(trigger, resto, valore)
            return
        contenitore = V.get(nome)
        if isinstance(resto[0], int):
            contenitore = list(contenitore) if isinstance(contenitore, list) else []
        elif not isinstance(contenitore, dict):
            contenitore = {}
        else:
            contenitore = dict(contenitore)
        V[nome] = contenitore
        self._annida(contenitore, resto, valore)

    def _annida(self, contenitore: Any, percorso: list[Any], valore: Any) -> None:
        chiave, *resto = percorso
        if resto:
            # una copia: i valori realistici restano come li ha resi Home Assistant
            figlio = contenitore.get(chiave) if isinstance(contenitore, dict) else None
            if isinstance(resto[0], int):
                figlio = list(figlio) if isinstance(figlio, list) else []
            else:
                figlio = dict(figlio) if isinstance(figlio, dict) else {}
            self._annida(figlio, resto, valore)
            valore = figlio
        if isinstance(contenitore, dict):
            contenitore[chiave] = valore
        elif isinstance(chiave, int) and isinstance(contenitore, list):
            posto = max(chiave, 0)
            while len(contenitore) <= posto:
                contenitore.append(str(self.rng.choice(["0", "1", *self.testi[:3]])))
            contenitore[posto] = valore

    def mirati(self, sorgente: str) -> Iterator[tuple[P.Soggetto, Any]]:
        """Ogni valore di ogni confronto del modello (il giro mirato)."""
        for soggetto, valori in self.analisi[sorgente].candidati.items():
            if soggetto[0] in ("stato", "attributo", "var", "parte"):
                for valore in valori:
                    yield soggetto, valore


def _aggiungi(voci: list[Any], valore: Any, massimo: int | None = None) -> None:
    """Aggiunge un valore se non c'è già (stesso tipo e valore); al massimo ``massimo``."""
    try:
        if any(type(v) is type(valore) and v == valore for v in voci):
            return
    except Exception:  # noqa: BLE001
        return
    voci.append(valore)
    if massimo is not None and len(voci) > massimo:
        del voci[0]


# --- Confronti --------------------------------------------------------------------------


def forma(valore: Any) -> Any:
    """Forma confrontabile di un risultato: tipo esatto e valore, anche dentro liste,
    tuple, insiemi e dizionari; per le liste di Home Assistant anche il testo scritto."""
    tipo = type(valore)
    testo = str(valore) if isinstance(valore, ResultWrapper) else None
    if isinstance(valore, float):
        return (tipo, "nan" if math.isnan(valore) else repr(valore))
    if isinstance(valore, (list, tuple)):
        return (tipo, testo, tuple(forma(v) for v in valore))
    if isinstance(valore, dict):
        return (tipo, testo, tuple((forma(k), forma(v)) for k, v in valore.items()))
    if isinstance(valore, (set, frozenset)):
        return (tipo, testo, frozenset(forma(v) for v in valore))
    if isinstance(valore, (str, int, bool, type(None), complex)):
        return (tipo, valore)
    return (tipo, _INDIRIZZO.sub(" at 0x…", repr(valore)))


def _nome_filtro(filtro: Callable[[str], bool]) -> str:
    return getattr(filtro, "__name__", repr(filtro))


def forma_info(info: RenderInfo, entita: list[str]) -> dict[str, Any]:
    """Tutto quello che trigger e attese leggono da una ``RenderInfo``."""
    errore = info.exception
    return {
        "risultato": None if errore is not None else forma(info._result),
        "errore": None
        if errore is None
        else (type(errore), _INDIRIZZO.sub(" at 0x…", str(errore))),
        "entities": frozenset(info.entities),
        "domains": frozenset(info.domains),
        "domains_lifecycle": frozenset(info.domains_lifecycle),
        "all_states": info.all_states,
        "all_states_lifecycle": info.all_states_lifecycle,
        "has_time": info.has_time,
        "rate_limit": info.rate_limit,
        "is_static": info.is_static,
        "filter": _nome_filtro(info.filter),
        "filter_lifecycle": _nome_filtro(info.filter_lifecycle),
        "filtrate": frozenset(e for e in entita if info.filter(e)),
        "filtrate_lifecycle": frozenset(e for e in entita if info.filter_lifecycle(e)),
    }


class _Registrato(Template):
    """Un ``Template`` di Home Assistant che tiene l'ultima ``RenderInfo`` (quella della
    condizione ``template``, che Home Assistant non restituisce)."""

    __slots__ = ("info",)

    def async_render_to_info(self, *args: Any, **kwargs: Any) -> RenderInfo:
        self.info = super().async_render_to_info(*args, **kwargs)
        return self.info


def _esito(funzione: Callable[[], Any]) -> tuple[str, Any]:
    try:
        return ("valore", funzione())
    except ConditionError as err:
        return ("errore condizione", _INDIRIZZO.sub(" at 0x…", str(err)))
    except TemplateError as err:
        return ("errore", _INDIRIZZO.sub(" at 0x…", str(err)))


class Confronto:
    """Rende un modello con Home Assistant e con la funzione tradotta e confronta."""

    def __init__(
        self,
        hass: HomeAssistant,
        c: Contesto,
        modelli: dict[str, _Registrato],
        funzioni: dict[str, Any],
        nomi: dict[str, str],
        entita: list[str],
    ) -> None:
        self.hass = hass
        self.c = c
        self.modelli = modelli
        self.funzioni = funzioni
        self.nomi = nomi
        self.entita = entita
        self.tradotti = {s: c.modello(funzioni[s], s) for s in modelli}
        self.campione = list({e.split(".", 1)[0]: e for e in entita}.values())
        self.rese: Counter[str] = Counter()
        self.differenze: list[str] = []

    def _differenza(self, tipo: str, sorgente: str, atteso: Any, ottenuto: Any) -> None:
        self.rese[f"differenze {tipo}"] += 1
        if len(self.differenze) < 30:
            self.differenze.append(
                f"{self.nomi[sorgente]} ({tipo}): HA {atteso!r}\n  motore {ottenuto!r}\n"
                f"  {sorgente[:300]!r}"
            )

    def confronta(self, sorgente: str, V: dict[str, Any]) -> None:
        T = self.modelli[sorgente]
        f = self.funzioni[sorgente]
        m: ModelloHA = self.tradotti[sorgente]
        c = self.c
        # testo
        atteso = _esito(lambda: T.async_render(V, parse_result=False))
        ottenuto = _esito(lambda: c.testo(f, V))
        self.rese["testo"] += 1
        self.rese[f"testo: {atteso[0]}"] += 1
        if atteso != ottenuto:
            self._differenza("testo", sorgente, atteso, ottenuto)
        # risultato interpretato e RenderInfo (come i trigger template)
        info = T.async_render_to_info(V)
        mia = m.async_render_to_info(V)
        self.rese["interpretato"] += 1
        self.rese["render_info"] += 1
        atteso_info = forma_info(info, self._entita(info))
        if atteso_info != (ottenuto_info := forma_info(mia, self._entita(info))):
            self._differenza(
                "render_info",
                sorgente,
                {k: v for k, v in atteso_info.items() if ottenuto_info[k] != v},
                {k: v for k, v in ottenuto_info.items() if atteso_info[k] != v},
            )
        atteso_valore = (
            ("errore", str(info.exception)) if info.exception else forma(info._result)
        )
        for come, calcolo in (
            ("ModelloHA.async_render", lambda: m.async_render(V)),
            ("resa_complessa", lambda: c.resa_complessa(Modello(f), V)),
            ("resa_complessa in lista", lambda: c.resa_complessa([Modello(f)], V)[0]),
        ):
            try:
                ottenuto_valore = forma(calcolo())
            except TemplateError as err:
                ottenuto_valore = ("errore", str(err))
            if atteso_valore != ottenuto_valore:
                self._differenza(come, sorgente, atteso_valore, ottenuto_valore)
        # condizione template (con la sua RenderInfo, senza interpretazione)
        atteso = _esito(
            lambda: condition.async_template(self.hass, T, V, trace_result=False)
        )
        ottenuto = _esito(lambda: c.condizione(f, V))
        mia = m.async_render_to_info(V, parse_result=False)
        self.rese["condizione"] += 1
        self.rese["render_info"] += 1
        if atteso != ottenuto:
            self._differenza("condizione", sorgente, atteso, ottenuto)
        atteso_info = forma_info(T.info, self._entita(T.info))
        if atteso_info != (ottenuto_info := forma_info(mia, self._entita(T.info))):
            self._differenza(
                "render_info della condizione",
                sorgente,
                {k: v for k, v in atteso_info.items() if ottenuto_info[k] != v},
                {k: v for k, v in ottenuto_info.items() if atteso_info[k] != v},
            )

    def _entita(self, info: RenderInfo) -> list[str]:
        """Le entità su cui provare i filtri: quelle lette, di altri domini e alcune del
        package (una per dominio)."""
        return [*info.entities, *ALTRE, *self.campione]


@pytest.fixture
def senza_avvisi() -> Iterator[None]:
    """Gli avvisi dell'indefinito di Home Assistant non vanno nel registro (non si
    confrontano, e sono decine di migliaia)."""
    registro = logging.getLogger("homeassistant.helpers.template")
    livello = registro.level
    registro.setLevel(logging.CRITICAL)
    yield
    registro.setLevel(livello)


async def test_modelli_come_home_assistant(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory, senza_avvisi: None
) -> None:
    """Stesso testo, risultato, RenderInfo ed esito di condizione per ogni modello."""
    package = P.leggi()
    sorgenti = sorted(set(package.automazioni_di) | package.negli_script)
    # Compilati prima della traduzione: la convalida del package trova il codice già
    # compilato (la cache dei modelli di Home Assistant li tiene finché vivono).
    modelli = {s: _Registrato(s, hass) for s in sorgenti}
    for modello in modelli.values():
        modello.ensure_valid()
    jinja, _generatore, _, _ = await traduzione(
        hass, package.automazioni, package.script
    )
    assert sorted(jinja.funzioni) == sorgenti
    # b42: 22 modelli nuovi (21 expand dei turn_off, la guardia dell'Esclusività); b44:
    # 1 nuovo (nessun avviso dei cellulari aprendo la finestra Opzioni)
    assert len(sorgenti) == 1033
    banco = Banco(hass, sorgenti, package, modelli)
    c = Contesto(hass)
    confronto = Confronto(
        hass,
        c,
        modelli,
        {s: getattr(M, jinja.funzioni[s]) for s in sorgenti},
        jinja.funzioni,
        banco.entita,
    )
    for _ in range(GIRI):
        banco.giro(freezer)
        for sorgente in sorgenti:
            for _ in range(VARIANTI):
                banco.mira_stati(sorgente)
                confronto.confronta(sorgente, banco.variabili(sorgente))
    # giro mirato: ogni valore di ogni confronto di ogni modello
    banco.giro(freezer)
    mirate = 0
    for sorgente in sorgenti:
        for forzato in banco.mirati(sorgente):
            banco.mira_stati(sorgente, forzato)
            confronto.confronta(sorgente, banco.variabili(sorgente, forzato))
            mirate += 1
    for pezzo, stati, variabili in SCENARI:
        scelti = [s for s in sorgenti if pezzo in s]
        assert scelti, pezzo
        for sorgente in scelti:
            for entity_id, (stato, attributi) in stati.items():
                hass.states.async_set(entity_id, stato, attributi)
            confronto.confronta(sorgente, banco.variabili(sorgente) | variabili)
            mirate += 1
    rese = confronto.rese
    print(f"\n{GIRI} giri, {mirate} rese mirate: {dict(sorted(rese.items()))}")
    # il banco deve rendere davvero (non solo errori)
    assert rese["testo: valore"] > rese["testo: errore"]
    assert not confronto.differenze, "\n".join(confronto.differenze)


# Modelli che danno un errore «senza predefinito» (``raise_no_default``): il messaggio di
# Home Assistant contiene il testo del modello che si sta rendendo (``template_cv``),
# anche per i filtri di Home Assistant che il codice tradotto chiama (``multiply``).
ERRORI_SENZA_PREDEFINITO = [
    "{{ states('sensor.vmc_master_temperatura') | float }}",
    "{{ states('input_text.vmc_master_x') | int + 1 }}",
    "{%- set v = states('sensor.vmc_master_y') -%}\n  {{ v | round(1) }} Master",
    "{{ as_timestamp(states('input_datetime.vmc_master_z')) }}",
    "{{ 'MASTER' | bool }}",
    "{{ strptime(states('sensor.vmc_master_ora'), '%H:%M') }}",
    "{{ states('sensor.vmc_master_portata') | multiply(2) }}",
    "{{ states('sensor.vmc_master_n') | log(10) }}",
    "{{ states('sensor.vmc_master_dati') | from_json }}",
]


async def test_errori_con_il_testo_del_modello(hass: HomeAssistant) -> None:
    """Un errore «senza predefinito» ha lo stesso messaggio di Home Assistant, con il
    testo del modello (rinominato per un'altra VMC), come testo, condizione e risultato."""
    ambiente = TemplateEnvironment(hass)
    traduttore = Traduttore(
        filtri_ha={n for n in ambiente.filters if not hasattr(J, f"f_{n}")},
        test_ha={n for n in ambiente.tests if not hasattr(J, f"t_{n}")},
        globali_ha=set(ambiente.globals),
    )
    nomi = [traduttore.funzione(s) for s in ERRORI_SENZA_PREDEFINITO]
    modulo: dict[str, Any] = {"J": J}
    exec("\n\n\n".join(traduttore.codice), modulo)  # noqa: S102
    confronti = 0
    for nome_vmc in ("master", "pippo"):
        c = Contesto(hass, nome_vmc)
        for sorgente, nome in zip(ERRORI_SENZA_PREDEFINITO, nomi, strict=True):
            funzione = modulo[nome]
            # il package di un'altra VMC è quello della master rinominato
            T = _Registrato(
                sorgente if nome_vmc == "master" else rinomina(sorgente, nome_vmc), hass
            )
            atteso = _esito(partial(T.async_render, parse_result=False))
            assert atteso[0] == "errore" and "no default was specified" in atteso[1]
            assert f"template '{T.template}'" in atteso[1]
            assert _esito(partial(c.testo, funzione, {})) == atteso, sorgente
            assert _esito(c.modello(funzione).async_render) == atteso
            assert _esito(partial(c.resa_complessa, Modello(funzione), {})) == atteso
            assert _esito(partial(c.condizione, funzione, {})) == _esito(
                partial(condition.async_template, hass, T, {})
            )
            confronti += 1
    assert confronti == 2 * len(ERRORI_SENZA_PREDEFINITO)
