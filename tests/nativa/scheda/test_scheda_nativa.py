"""La scheda «VMC Master» tradotta ai nomi delle entità native (fase 4).

- la scheda tradotta, l'elenco delle modifiche e i totali sono quelli che scrive oggi il
  traduttore (con ``VMC_RIGENERA=1`` il test li riscrive);
- ogni entità della scheda tradotta esiste domani, nessuna voce interna o tolta resta, ogni
  entità di oggi che la scheda usava ha il suo nome di domani; le righe delle voci tolte
  (b46: il campo «Cambia IP VMC») escono intere;
- ogni azione chiama un servizio che Home Assistant ha per il dominio delle sue entità, con
  dati che lo schema del servizio accetta;
- oltre a nomi, servizi, righe dei timer (con il loro colore), condizioni dei timer, voci
  dell'elenco, chiavi dei tipi, ramo delle entità escluse dal Recorder e testi aggiornati
  (``TESTI``) non cambia niente (seconda traduzione indipendente, sulla struttura); i testi
  aggiornati cambiano solo le loro righe e nessun testo parla più del package, degli
  aiutanti, delle automazioni, degli script, delle esclusioni dal Recorder o dei tempi di
  attesa modificabili; i link vanno al repository nuovo (VMC-HELTY-FLOW-MASTER);
- con gli stati di oggi e quelli delle entità native nella stessa situazione ogni condizione
  della scheda dà lo stesso risultato e ogni modello Jinja lo stesso testo, a parte i testi
  aggiornati (tranne l'elenco di «Pulisci cronologia», che perde le voci interne).
"""

from __future__ import annotations

import difflib
import json
import os
import re
import shutil
import subprocess
from collections import Counter
from collections.abc import Mapping
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest
import yaml
from homeassistant.core import HomeAssistant
from homeassistant.helpers.template import Template
from homeassistant.setup import async_setup_component

from custom_components.vmc_master.nativa.entita import nome_visibile
from custom_components.vmc_master.nativa.tabelle import IMPOSTAZIONI
from custom_components.vmc_master.trasforma import adatta_link_repository, per_vmc

from . import nativi
from .traduci_scheda import (
    CHIAVI_TIPI,
    COMANDO,
    COMMENTI,
    CONTO_ALLA_ROVESCIA,
    PREMI,
    RAMO_ESCLUSE,
    RIGA_CONTO,
    SERVIZI,
    TESTI,
    Commento,
    Mappa,
    NonTraducibile,
    Testo,
    file_generati,
    mappa_fase_1,
    modello_testo,
    scheda_master,
    tolte_fase_1,
    traduci,
)

JS = (
    Path(__file__).resolve().parents[3]
    / "custom_components/vmc_master/frontend/vmc-master-card.js"
)
DOMINI_DI_DOMANI = (
    "binary_sensor",
    "button",
    "number",
    "select",
    "sensor",
    "switch",
    "text",
    "time",
)
SOLO_DI_OGGI = (
    "automation",
    "input_boolean",
    "input_datetime",
    "input_number",
    "input_select",
    "input_text",
    "script",
    COMANDO,
    "timer",
)
_NOME = re.compile(r"(?<![A-Za-z0-9_.])([a-z_]+)\.([a-z0-9_]*)")
# Domini che il frontend accende e spegne con un tocco (const.ts, DOMAINS_TOGGLE)
DOMINI_TOGGLE = {
    "fan",
    "input_boolean",
    "light",
    "switch",
    "group",
    "automation",
    "humidifier",
    "valve",
}
SERVIZI_DI_DOMANI = {*SERVIZI.values(), PREMI}


@pytest.fixture(scope="module")
def traduzione():
    return traduci()


@pytest.fixture(scope="module")
def schede(traduzione):
    """(scheda di oggi, scheda tradotta) come configurazioni."""
    return yaml.safe_load(scheda_master()), yaml.safe_load(traduzione.testo)


def _stringhe(config: Any):
    if isinstance(config, Mapping):
        for valore in config.values():
            yield from _stringhe(valore)
    elif isinstance(config, list):
        for valore in config:
            yield from _stringhe(valore)
    elif isinstance(config, str):
        yield config


# I testi aggiornati cercati nei testi già letti (YAML o modelli): fra due parole uno o più
# spazi o a capo (anche fra due capoversi, «\n» nel testo)
_TESTI = [
    (re.compile(r"\s+".join(re.escape(p) for p in t.prima.split())), t) for t in TESTI
]
# Il sensore che oggi la scheda legge per le entità escluse dal Recorder: domani la scheda
# non lo legge più (nessuna entità è esclusa dal Recorder, vedi «esclusioni»)
SENSORE_ESCLUSE = "sensor.vmc_master_entita_escluse_recorder"


def _testi_nuovi(testo: str, trovati: Counter[str] | None = None) -> str:
    """Il testo con i testi aggiornati (conta in ``trovati`` quelli trovati)."""
    for modello, t in _TESTI:
        testo, quanti = modello.subn(lambda _t, dopo=t.dopo: dopo, testo)
        if trovati is not None:
            trovati[t.prima] += quanti
    return testo


def _nomi(config: Any, domini) -> Counter[str]:
    """Nomi «dominio.oggetto» (interi o pezzi) dei ``domini`` nei testi della scheda."""
    return Counter(
        t.group(0)
        for s in _stringhe(config)
        for t in _NOME.finditer(s)
        if t.group(1) in domini
    )


# ------------------------------------------------------------------ file generati
def test_scheda_tradotta_aggiornata(traduzione) -> None:
    """Scheda tradotta, modifiche e totali sono quelli che scrive oggi il traduttore."""
    vecchi = []
    for percorso, testo in file_generati(traduzione):
        if os.environ.get("VMC_RIGENERA"):
            percorso.write_text(testo, encoding="utf-8", newline="")
        attuale = (
            percorso.read_text(encoding="utf-8", newline="")
            if percorso.exists()
            else None
        )
        if attuale != testo:
            vecchi.append(percorso.name)
    assert not vecchi, f"da rigenerare (VMC_RIGENERA=1): {vecchi}"


def test_scheda_tradotta_per_ogni_vmc(traduzione) -> None:
    """La scheda tradotta passa da per_vmc come quella di oggi: per la Master non cambia
    (le sezioni Clona e Installa non ci sono più), per un'altra VMC cambiano nome e IP."""
    assert per_vmc(traduzione.testo, "master", "192.168.1.160") == traduzione.testo
    sala = yaml.safe_load(
        adatta_link_repository(per_vmc(traduzione.testo, "sala", "192.168.1.161"))
    )
    nomi = _nomi(sala, DOMINI_DI_DOMANI + SOLO_DI_OGGI)
    assert not [n for n in nomi if "vmc_master" in n]
    interi = {n for n in nomi if not n.endswith("_")} - SERVIZI_DI_DOMANI
    assert interi <= nativi.insieme_nativo("sala")


def test_conteggi_delle_modifiche(traduzione) -> None:
    """Numero esatto di modifiche per tipo (vedi modifiche_scheda_totali.txt)."""
    per_tipo = Counter(m.tipo for m in traduzione.modifiche)
    assert per_tipo == {
        "nome": 1922,
        "elenco": 122,
        "servizio": 66,
        "condizione timer": 62,
        "riga conto alla rovescia": 39,
        "colore riga conto alla rovescia": 39,
        "comando": 23,
        "testo": 67,
        "riga tolta": 27,
        "esclusioni": 20,
        "frammento": 12,
        "chiave tipi": 5,
        "intestazione": 2,
    }
    assert sum(per_tipo.values()) == 2406


# ------------------------------------------------------------------------ i testi
# Parole dei testi della scheda che domani non sono più vere: il package e i suoi file, i
# domini degli aiutanti, le automazioni e gli script (domani c'è l'integrazione, con spie,
# interruttori e pulsanti), le esclusioni dal Recorder, il ricaricamento dello YAML, i tempi
# di attesa (e le spie) da non modificare e riportati ai valori originali (domani nessuno li
# può modificare), il repository di prima (domani VMC-HELTY-FLOW-MASTER).
TESTI_NON_PIU_VERI = {
    "package": re.compile(r"\b[Pp]ackage\b"),
    "file vmc_master.yaml": re.compile(r"vmc_master\.yaml"),
    "dominio di un aiutante": re.compile(
        r"\(input_(?:boolean|datetime|number|select|text)\)"
    ),
    "booleane": re.compile(r"\bBooleans?\b|[Vv]ariabili [Bb]ooleane"),
    "scan_interval": re.compile(r"scan_interval"),
    "automazione": re.compile(r"\b[Aa]utomazion[ei]\b"),
    "script": re.compile(r"\b[Ss]cript\b(?!\.)"),
    "ricarica dello YAML": re.compile(r"Strumenti → YAML"),
    "esclusioni dal Recorder": re.compile(
        r"sezione «recorder»|vmc_master_backup|non registrano storico"
    ),
    "entità escluse dal Recorder": re.compile(
        r"escluse dal Recorder|entita_escluse_recorder"
    ),
    "da non modificare": re.compile(
        r"non vanno modificat|[Vv]alori\s+[Oo]riginali|li riporta comunque"
    ),
    "repository di prima": re.compile(
        r"VMC-HELTY-FLOW-MARKETPLACE|github\.com/DanRobo76/VMC-HELTY-FLOW(?![-\w])"
    ),
}
# Restano, perché domani non si vedono: le etichette dei tipi «automation» e «script» del
# modello di «Pulisci cronologia» (domani nell'elenco non ci sono automazioni né script)
TESTI_AMMESSI = ("'automation': 'Automazioni'", "'script': 'Script'")


def _testi_non_piu_veri(config: Any) -> Counter[str]:
    trovati: Counter[str] = Counter()
    for testo in _stringhe(config):
        for ammesso in TESTI_AMMESSI:
            testo = testo.replace(ammesso, "")
        for nome, modello in TESTI_NON_PIU_VERI.items():
            trovati[nome] += len(modello.findall(testo))
    return +trovati


def test_nessun_testo_non_piu_vero(schede) -> None:
    """Nessun testo della scheda tradotta parla ancora del package, dei suoi file, degli
    aiutanti, delle automazioni, degli script, delle esclusioni dal Recorder, dei tempi di
    attesa da non modificare o del repository di prima."""
    oggi, domani = schede
    assert _testi_non_piu_veri(oggi) == {
        "package": 19,
        "automazione": 17,
        "script": 10,
        "da non modificare": 7,
        "dominio di un aiutante": 6,
        "booleane": 4,
        "esclusioni dal Recorder": 4,
        "file vmc_master.yaml": 3,
        "entità escluse dal Recorder": 2,
        "repository di prima": 2,
        "scan_interval": 1,
        "ricarica dello YAML": 1,
    }
    assert _testi_non_piu_veri(domani) == {}


# Il repository di prima, cercato anche nei commenti dell'intestazione del file
_REPOSITORY_DI_PRIMA = TESTI_NON_PIU_VERI["repository di prima"]
_IMMAGINI = "https://raw.githubusercontent.com/DanRobo76/VMC-HELTY-FLOW/main/"


def _intestazione(testo: str) -> list[str]:
    """Le righe di commento prima della scheda."""
    righe = testo.split("\r\n")
    return righe[: next(i for i, r in enumerate(righe) if not r.startswith("#"))]


def test_link_al_repository_nuovo(traduzione) -> None:
    """Nel file della scheda tradotta, commenti compresi, ogni link al repository
    dell'integrazione va a VMC-HELTY-FLOW-MASTER (il proprietario rinomina
    VMC-HELTY-FLOW-MARKETPLACE): copyright dell'intestazione, pagina del Marketplace e
    GitHub in Informazioni. I 75 indirizzi delle immagini restano quelli (mai spostare
    file: le schede installate puntano a percorsi fissi). L'intestazione resta una cornice di «#» larga
    uguale; dalla 9.0.0b46 cambia anche la versione della scheda nativa (riga 3)."""
    oggi, domani = scheda_master(), traduzione.testo
    assert len(_REPOSITORY_DI_PRIMA.findall(oggi)) == 3
    assert _REPOSITORY_DI_PRIMA.findall(domani) == []
    assert domani.count("VMC-HELTY-FLOW-MASTER") == 3
    assert oggi.count(_IMMAGINI) == domani.count(_IMMAGINI) == 75
    righe_oggi, righe_domani = _intestazione(oggi), _intestazione(domani)
    assert len(righe_oggi) == len(righe_domani) == 39
    assert [len(r) for r in righe_domani] == [len(r) for r in righe_oggi]
    assert [i for i, (a, b) in enumerate(zip(righe_oggi, righe_domani)) if a != b] == [
        2,
        10,
    ]
    assert "RELEASE [VER. 9.0.0b47]" in righe_domani[2]
    assert righe_domani[10].startswith(
        f"# Copyright © 2023-2026 Ing. Danilo Robotti {COMMENTI[0].dopo} "
    )


# --------------------------------------------------------------------- le tabelle
def test_tabelle_della_fase_1() -> None:
    """Le due tabelle della fase 1 coincidono; 219 voci su 326 (aiutanti e script) restano
    entità, 105 diventano interne e 2 sono tolte; i 16 comandi di shell: 12 pulsanti, 3
    interni e 1 tolto; 13 delle 14 automazioni diventano il motore, 1 è tolta; 1 sensore è
    tolto (b46: il campo «Cambia IP VMC» e chi lo serve)."""
    mappa, tolte = mappa_fase_1(), tolte_fase_1()
    tipi = Counter()
    for oggi, domani in mappa.items():
        dominio = oggi.split(".", 1)[0]
        stato = "tolta" if oggi in tolte else "entità" if domani else "interna"
        if domani is None:
            assert stato != "entità"
        if dominio in ("sensor", "binary_sensor"):
            assert domani == oggi or stato == "tolta"
            tipi[("sensore", stato)] += stato == "tolta"
            continue
        gruppo = (
            "comando"
            if dominio == COMANDO
            else "automazione"
            if dominio == "automation"
            else "voce"
        )
        tipi[(gruppo, stato)] += 1
        if domani is not None:
            assert domani.split(".", 1)[1] == oggi.split(".", 1)[1], oggi
    assert +tipi == {
        ("voce", "entità"): 219,
        ("voce", "interna"): 105,
        ("voce", "tolta"): 2,
        ("comando", "entità"): 12,
        ("comando", "interna"): 3,
        ("comando", "tolta"): 1,
        ("automazione", "interna"): 13,
        ("automazione", "tolta"): 1,
        ("sensore", "tolta"): 1,
    }
    assert tolte == {
        "automation.vmc_master_cambio_ip_vmc_riavvio_di_h_a",
        "input_text.vmc_master_ip_insert",
        "input_text.vmc_master_ip_insert_esito",
        "sensor.vmc_master_verifica_ip_inserito",
        "shell_command.vmc_master_aggiorna_indirizzo_ip",
    }


# ----------------------------------------------------------- entità della scheda
def test_entita_della_scheda_tradotta_esistono(schede) -> None:
    """Ogni nome della scheda tradotta è un'entità nativa (o l'inizio di entità native dello
    stesso dominio); nessun nome di oggi e nessuna voce interna restano."""
    _oggi, domani = schede
    nativo = nativi.insieme_nativo()
    nomi = _nomi(domani, DOMINI_DI_DOMANI + SOLO_DI_OGGI)
    assert not [n for n in nomi if n.split(".", 1)[0] in SOLO_DI_OGGI]
    assert not set(nomi) & nativi.interne()
    interi = {n for n in nomi if n in nativo}
    pezzi = set(nomi) - interi - SERVIZI_DI_DOMANI
    for pezzo in pezzi:
        assert [e for e in nativo if e.startswith(pezzo)], pezzo
    assert pezzi == {
        "binary_sensor.vmc_master_spia_calendario_",
        "time.vmc_master_accensione_",
        "time.vmc_master_spegnimento_",
        "sensor.vmc_",
        "sensor.vmc_master_",
    }
    # 366 entità native diverse: 136 sensori della fase 2 e 230 di aiutanti, script e comandi
    # (non il sensore delle entità escluse dal Recorder, che la scheda non legge più)
    assert len(interi) == 366
    assert SENSORE_ESCLUSE in nativo and SENSORE_ESCLUSE not in interi
    assert Counter(e.split(".", 1)[0] for e in interi) == {
        "sensor": 157,
        "binary_sensor": 92,
        "switch": 37,
        "time": 30,
        "button": 25,
        "select": 14,
        "number": 10,
        "text": 1,
    }


def test_nessuna_entita_persa(schede) -> None:
    """Ogni entità che la scheda di oggi usa fuori dall'elenco di «Pulisci cronologia» è
    usata, con il nome di domani, dalla scheda tradotta, e viceversa; tranne il sensore delle
    entità escluse dal Recorder, che leggeva solo il ramo tolto («esclusioni»)."""
    oggi, domani = schede
    mappa = mappa_fase_1()
    nomi_oggi = {
        n for n in _nomi(oggi, SOLO_DI_OGGI + ("sensor", "binary_sensor")) if n in mappa
    }
    assert mappa["input_select.vmc_master_entita_escluse_recorder"] == SENSORE_ESCLUSE
    attesi = {mappa[n] for n in nomi_oggi if mappa[n] is not None} - {SENSORE_ESCLUSE}
    trovati = {
        n for n in _nomi(domani, DOMINI_DI_DOMANI) if n in nativi.insieme_nativo()
    }
    assert trovati == attesi
    assert (
        len(nomi_oggi - set(SERVIZI)) == 489 - 0
    )  # come le righe di traduzione_scheda.csv
    assert {n for n in nomi_oggi if mappa[n] is None} == nativi.interne() - {
        e for e in nativi.interne() if e.startswith(COMANDO)
    }


# ----------------------------------------------------------------------- servizi
def _azioni(config: Any):
    if isinstance(config, Mapping):
        if "perform_action" in config or "service" in config:
            yield config
        for valore in config.values():
            yield from _azioni(valore)
    elif isinstance(config, list):
        for valore in config:
            yield from _azioni(valore)


def _bersagli(azione: Mapping[str, Any]) -> list[str]:
    bersagli = []
    for chiave in ("target", "data"):
        valore = (azione.get(chiave) or {}).get("entity_id")
        if valore:
            bersagli += valore if isinstance(valore, list) else [valore]
    return bersagli


async def test_servizi_delle_azioni_esistono(hass: HomeAssistant, schede) -> None:
    """Ogni azione della scheda tradotta chiama un servizio di Home Assistant del dominio di
    tutte le sue entità, e lo schema del servizio accetta bersaglio e dati."""
    assert await async_setup_component(hass, "homeassistant", {})
    for dominio in ("switch", "button", "number", "select", "text", "time"):
        assert await async_setup_component(hass, dominio, {})
    _oggi, domani = schede
    nativo = nativi.insieme_nativo()
    conteggio = Counter()
    for azione in _azioni(domani):
        assert "service" not in azione
        dominio, servizio = azione["perform_action"].split(".", 1)
        assert hass.services.has_service(dominio, servizio), azione["perform_action"]
        bersagli = _bersagli(azione)
        assert bersagli and all(
            b in nativo and b.split(".", 1)[0] == dominio for b in bersagli
        ), azione
        schema = hass.services.async_services_for_domain(dominio)[servizio].schema
        schema({**(azione.get("data") or {}), **(azione.get("target") or {})})
        conteggio[azione["perform_action"]] += 1
    assert conteggio == {
        "switch.toggle": 48,
        "button.press": 39,
        "switch.turn_on": 1,
        "switch.turn_off": 1,
    }


def _senza_azione(config: Any, dentro_pulsanti: bool = False):
    """Schede e righe con un'entità e senza tap_action (tocco predefinito del frontend)."""
    if isinstance(config, Mapping):
        tipo = config.get("type")
        if (
            isinstance(config.get("entity"), str)
            and "tap_action" not in config
            and (tipo == "button" or dentro_pulsanti)
        ):
            yield config["entity"]
        for chiave, valore in config.items():
            yield from _senza_azione(valore, tipo == "buttons" and chiave == "entities")
    elif isinstance(config, list):
        for valore in config:
            yield from _senza_azione(valore, dentro_pulsanti)


def test_tocco_predefinito_uguale(schede) -> None:
    """Pulsanti senza tap_action: il tocco predefinito (accendi/spegni o informazioni) dipende
    dal dominio; ogni entità di domani fa la stessa cosa di quella di oggi."""
    oggi, domani = schede
    mappa = mappa_fase_1()
    prima, dopo = list(_senza_azione(oggi)), list(_senza_azione(domani))
    assert [mappa.get(e, e) for e in prima] == dopo
    # 156 pulsanti, tutti di input_boolean che domani sono switch (tocco: accendi/spegni)
    assert Counter(e.split(".", 1)[0] for e in dopo) == {"switch": 156}
    for vecchia, nuova in zip(prima, dopo, strict=True):
        assert (vecchia.split(".", 1)[0] in DOMINI_TOGGLE) == (
            nuova.split(".", 1)[0] in DOMINI_TOGGLE
        )


# ---------------------------------------------- nient'altro cambia (seconda traduzione)
def _riga_tolta(config: Any, tolte: frozenset[str]) -> bool:
    """La riga di una voce tolta o una riga ``conditional`` con una condizione su una voce
    tolta (escono intere dalla scheda tradotta)."""
    if not isinstance(config, Mapping):
        return False
    if config.get("entity") in tolte:
        return True
    return config.get("type") == "conditional" and any(
        _riga_tolta(c, tolte) for c in config.get("conditions") or []
    )


def _traduci_struttura(config: Any, mappa: Mappa) -> Any:
    """La stessa traduzione fatta sulla configurazione (non sul testo)."""
    removibili = {n for n, d in mappa.entita.items() if d is None}
    trovati: Counter[str] = Counter()

    def nome(testo: str) -> str:
        def sostituisci(t: re.Match[str]) -> str:
            n = t.group(0)
            if (
                t.group(1) not in SOLO_DI_OGGI + ("sensor", "binary_sensor")
                or n in SERVIZI
            ):
                return n
            if n in mappa.entita:
                return mappa.entita[n] or n
            return mappa.frammento(n)

        if "{%- set elenco = [" in testo:
            righe = testo.split("\n")
            testo = "\n".join(
                r
                for r in righe
                if not (
                    re.fullmatch(r"\s*'([a-z_.0-9]+)',?", r)
                    and r.strip(" ',") in removibili
                )
            )
        if "{%- set tipi = {" in testo:
            for vecchio, nuovo in CHIAVI_TIPI.items():
                testo = testo.replace(f"'{vecchio}': ", f"'{nuovo}': ", 1)
        if RAMO_ESCLUSE[0] in testo:
            # il ramo delle entità escluse dal Recorder (nel testo ripiegato le sue righe
            # sono unite da spazi) e il suo «endif», l'ultimo pezzo del modello
            testo, tolti = re.subn(
                re.escape(RAMO_ESCLUSE[0]) + r".*?\{%- else -%\}\s*",
                "",
                testo,
                flags=re.DOTALL,
            )
            testo, chiusi = re.subn(r"\s*\{%- endif -%\}\Z", "", testo)
            assert (tolti, chiusi) == (1, 1)
        return _NOME.sub(sostituisci, _testi_nuovi(testo, trovati))

    def visita(nodo: Any, colore: str | None = None) -> Any:
        if isinstance(nodo, list):
            return [visita(x, colore) for x in nodo if not _riga_tolta(x, mappa.tolte)]
        if isinstance(nodo, str):
            return nome(nodo)
        if not isinstance(nodo, Mapping):
            return nodo
        if nodo.get("type") == "entities":
            colore = _colore_della_scheda(nodo)
        nuovo = {k: visita(v, colore) for k, v in nodo.items()}
        entita = nodo.get("entity")
        if isinstance(entita, str) and entita.startswith("timer."):
            if "condition" in nodo:
                stato = nuovo.pop("state")
                chiave, valore = CONTO_ALLA_ROVESCIA[stato].split(": ", 1)
                nuovo[chiave] = yaml.safe_load(valore)
            else:
                nuovo["type"] = RIGA_CONTO
                nuovo["color"] = colore
        servizio = nodo.get("perform_action")
        if servizio in SERVIZI:
            nuovo["perform_action"] = SERVIZI[servizio]
        elif isinstance(servizio, str) and servizio.startswith(f"{COMANDO}."):
            nuovo["perform_action"] = PREMI
            nuovo["target"] = {"entity_id": mappa.entita[servizio]}
        return nuovo

    tradotta = visita(config)
    assert trovati == {t.prima: t.volte for t in TESTI}
    return tradotta


def _colore_della_scheda(scheda: Mapping[str, Any]) -> str:
    """Il colore che la scheda entities dà alle sue righe (frontend 20261028:
    ``{color: "state", ...config}``, con ``state_color: false`` che diventa ``none``)."""
    if "color" in scheda:
        return scheda["color"]
    return "none" if scheda.get("state_color") is False else "state"


def _righe_dei_timer(oggi: Any, domani: Any, colore: str | None = None):
    """(riga di oggi, riga tradotta, colore che la scheda dà alla riga di oggi) per ogni riga
    di un timer. Il frontend passa il colore della scheda alle righe senza «type» o con un
    tipo suo, mai a quelle con un tipo ``custom:``: la riga tradotta lo deve avere scritto."""
    if isinstance(oggi, Mapping):
        if oggi.get("type") == "entities":
            colore = _colore_della_scheda(oggi)
        entita = oggi.get("entity")
        if (
            isinstance(entita, str)
            and entita.startswith("timer.")
            and "condition" not in oggi
        ):
            yield oggi, domani, colore
            return
        for chiave, valore in oggi.items():
            if (
                chiave in domani
            ):  # le condizioni dei timer cambiano «state» in «state_not»
                yield from _righe_dei_timer(valore, domani[chiave], colore)
    elif isinstance(oggi, list):
        tenute = [a for a in oggi if not _riga_tolta(a, tolte_fase_1())]
        for a, b in zip(tenute, domani, strict=True):
            yield from _righe_dei_timer(a, b, colore)


def test_colore_delle_righe_conto_alla_rovescia(schede) -> None:
    """Ogni riga conto alla rovescia ha scritto il colore che oggi la scheda entities dà alla
    riga del timer (icona colorata quando il timer è attivo)."""
    oggi, domani = schede
    righe = list(_righe_dei_timer(oggi, domani))
    assert len(righe) == 39
    assert Counter(colore for _o, _d, colore in righe) == {"state": 30, "none": 9}
    for riga_oggi, riga_domani, colore in righe:
        assert "color" not in riga_oggi and "state_color" not in riga_oggi
        assert riga_domani["type"] == RIGA_CONTO
        assert riga_domani["color"] == colore


def test_solo_nomi_e_servizi_cambiati(schede) -> None:
    """La traduzione del testo è uguale alla traduzione fatta sulla struttura: testi,
    disposizione e stili restano identici."""
    oggi, domani = schede
    assert _traduci_struttura(oggi, Mappa(mappa_fase_1(), tolte_fase_1())) == domani


def test_righe_cambiate_solo_dalle_modifiche() -> None:
    """Righe tolte, aggiunte e cambiate: esattamente quelle delle modifiche (i testi a
    parte, vedi il test che segue)."""
    traduzione = traduci(testi=())
    prima = scheda_master().split("\r\n")
    dopo = traduzione.testo.split("\r\n")
    tolte, aggiunte = Counter(), Counter()
    for riga in difflib.ndiff(prima, dopo):
        if riga.startswith("- "):
            tolte[riga[2:]] += 1
        elif riga.startswith("+ "):
            aggiunte[riga[2:]] += 1
    tolte_intere = ("elenco", "esclusioni", "riga tolta")
    righe_toccate = {m.riga for m in traduzione.modifiche if m.tipo not in tolte_intere}
    elenco = [m for m in traduzione.modifiche if m.tipo == "elenco"]
    esclusioni = [m for m in traduzione.modifiche if m.tipo == "esclusioni"]
    righe_tolte = [m for m in traduzione.modifiche if m.tipo == "riga tolta"]
    # ogni riga toccata da una modifica è tolta e rimessa cambiata; tolte anche le voci
    # dell'elenco, le 20 righe del ramo delle entità escluse dal Recorder, i 17
    # «target: {}» dei comandi e le 237 righe del campo «Cambia IP VMC» (3 volte 79: la riga
    # del campo e le 8 righe condizionali dei suoi esiti); aggiunte le 39 righe «type:» e le
    # 39 righe «color:» delle righe dei timer e, per i 23 comandi, 23 «target:» e 23
    # «entity_id:»
    assert len(elenco) == 122 and len(esclusioni) == 20 and len(righe_tolte) == 27
    assert Counter(m.posto for m in righe_tolte) == {"riga": 3, "riga condizionale": 24}
    assert not righe_toccate & set(range(556, 635))
    assert [m.prima for m in esclusioni][:3] == list(RAMO_ESCLUSE)
    assert [m.prima for m in esclusioni][-2:] == ["{%- else -%}", "{%- endif -%}"]
    assert not righe_toccate & {m.riga for m in esclusioni}
    assert sum(tolte.values()) == len(righe_toccate) + 122 + 20 + 17 + 237
    assert Counter(m.prima for m in esclusioni) <= Counter(
        r.strip() for r in tolte.elements()
    )
    assert tolte[next(r for r in tolte if r.strip() == "target: {}")] == 17
    assert sum(aggiunte.values()) == len(righe_toccate) + 39 + 39 + 23 + 23
    nuove = Counter(r.strip() for r in aggiunte.elements())
    assert nuove[f"type: {RIGA_CONTO}"] == 39 and nuove["target:"] >= 23
    assert nuove["color: state"] == 30 and nuove["color: none"] == 9
    assert len(dopo) == len(prima) - 122 - 20 - 237 + 39 + 39 + 6 + 23


def test_righe_cambiate_dai_testi(traduzione) -> None:
    """I testi aggiornati cambiano solo le loro righe: ogni pezzo cambiato è fatto delle
    righe di uno o più testi di oggi e, rimesse le righe in fila, è il testo nuovo."""
    senza = traduci(testi=()).testo
    righe_senza = senza.split("\r\n")
    righe_con = traduzione.testo.split("\r\n")
    inizi = [0] + [i + 2 for i in range(len(senza)) if senza.startswith("\r\n", i)]
    coperte: set[int] = set()
    for t in TESTI:
        trovati = list(modello_testo(t.prima).finditer(senza))
        assert len(trovati) == t.volte, t.prima
        for trovato in trovati:
            a = sum(1 for inizio in inizi if inizio <= trovato.start()) - 1
            b = sum(1 for inizio in inizi if inizio < trovato.end()) - 1
            coperte.update(range(a, b + 1))
    pezzi = difflib.SequenceMatcher(None, righe_senza, righe_con, autojunk=False)
    corrispondenti: dict[int, int] = {}
    for tipo, i1, i2, j1, _j2 in pezzi.get_opcodes():
        if tipo == "equal":
            corrispondenti.update({i1 + k: j1 + k for k in range(i2 - i1)})
        else:
            # «delete»: un testo che domani sparisce (la nota di uno script senza pulsante)
            assert tipo in ("replace", "delete"), (tipo, i1, j1)
            assert set(range(i1, i2)) <= coperte
    # ogni gruppo di righe di testi di oggi, rimesso in fila, diventa il testo nuovo
    gruppi: list[list[int]] = []
    for riga in sorted(coperte):
        if gruppi and gruppi[-1][-1] == riga - 1:
            gruppi[-1].append(riga)
        else:
            gruppi.append([riga])
    for gruppo in gruppi:
        j1 = corrispondenti[gruppo[0] - 1] + 1
        j2 = corrispondenti[gruppo[-1] + 1]
        # con i suoi a capo e le righe vuote (un testo su due capoversi), spazi a parte
        vecchio = "\r\n".join(righe_senza[gruppo[0] : gruppo[-1] + 1])
        assert " ".join(_testi_nuovi(vecchio).split()) == " ".join(
            " ".join(righe_con[j1:j2]).split()
        )
    # 104 righe con testi di oggi (55 testi, alcuni su più righe, su più capoversi o sulla
    # stessa riga), in 44 gruppi di righe consecutive
    assert (len(coperte), len(gruppi)) == (117, 54)
    assert len(righe_con) == len(righe_senza) - 35


# ------------------------------------------ stessi risultati con gli stati di domani
def _varianti(stati: nativi.Stati):
    """Gli stati del simulatore e varianti: ogni input_boolean invertito, ogni timer attivo
    o fermo, ogni fase del riallineamento, un comando non eseguito."""
    yield "base", stati
    for entita, (stato, attributi) in stati.items():
        dominio = entita.split(".", 1)[0]
        if dominio == "input_boolean":
            yield (
                entita,
                {**stati, entita: ("off" if stato == "on" else "on", attributi)},
            )
        elif dominio == "timer":
            if stato == "active":
                nuovi = {k: v for k, v in attributi.items() if k != "finishes_at"}
                yield entita, {**stati, entita: ("idle", nuovi)}
            else:
                yield (
                    entita,
                    {
                        **stati,
                        entita: (
                            "active",
                            {**attributi, "finishes_at": "2026-01-15T09:15:00+00:00"},
                        ),
                    },
                )
    fase = "input_number.vmc_master_fase_riallineamento_al_riavvio"
    for valore in ("1.0", "2.0", "3.0", "4.0"):
        yield f"fase {valore}", {**stati, fase: (valore, stati[fase][1])}
    comando = "input_text.vmc_master_comando_non_eseguito"
    yield "comando", {**stati, comando: ("Velocità 2", stati[comando][1])}


def test_condizioni_uguali(schede) -> None:
    """Ogni condizione della scheda (schede e righe conditional, visibility) dà lo stesso
    risultato con gli stati di oggi e con quelli delle entità native, in 155 situazioni
    (tranne le 24 righe condizionali del campo «Cambia IP VMC», che escono)."""
    oggi, domani = schede
    tolte = tolte_fase_1()
    tutte_oggi = list(nativi.condizioni(oggi))
    elenchi_oggi = [e for e in tutte_oggi if not any(_riga_tolta(c, tolte) for c in e)]
    elenchi_domani = list(nativi.condizioni(domani))
    assert len(tutte_oggi) == 162
    assert len(elenchi_oggi) == len(elenchi_domani) == 138
    stati = nativi.leggi_stati()
    situazioni = 0
    for nome, variante in _varianti(stati):
        prima = {**variante}
        dopo = {
            **{
                e: v
                for e, v in variante.items()
                if e.split(".", 1)[0] in ("sensor", "binary_sensor")
            },
            **nativi.stati_nativi(variante),
        }
        for elenco_oggi, elenco_domani in zip(
            elenchi_oggi, elenchi_domani, strict=True
        ):
            esito_oggi = all(nativi.vero(c, prima) for c in elenco_oggi)
            esito_domani = all(nativi.vero(c, dopo) for c in elenco_domani)
            assert esito_oggi == esito_domani, (nome, elenco_oggi)
        situazioni += 1
    assert situazioni == 155


async def _carica(hass: HomeAssistant, stati: nativi.Stati) -> None:
    for entita in list(hass.states.async_entity_ids()):
        hass.states.async_remove(entita)
    for entita, (stato, attributi) in stati.items():
        hass.states.async_set(entita, stato, attributi)
    await hass.async_block_till_done()


async def test_modelli_uguali(hass: HomeAssistant, schede, freezer) -> None:
    """Ogni modello Jinja della scheda dà lo stesso testo con gli stati di oggi e con quelli
    delle entità native, a parte i testi aggiornati (tutti tranne l'elenco di «Pulisci
    cronologia»), in 4 situazioni."""
    freezer.move_to(datetime.fromisoformat("2026-01-15T10:05:00+01:00"))
    oggi, domani = schede
    modelli_oggi, modelli_domani = (
        list(nativi.modelli(oggi)),
        list(nativi.modelli(domani)),
    )
    assert len(modelli_oggi) == len(modelli_domani) == 13
    stati = nativi.leggi_stati()
    accesi = {
        e: ("on", a) for e, (s, a) in stati.items() if e.startswith("input_boolean.")
    }
    attivi = {
        e: ("active", {**a, "finishes_at": "2026-01-15T09:15:00+00:00"})
        for e, (s, a) in stati.items()
        if e.startswith("timer.")
    }
    situazioni = {
        "base": stati,
        "spie accese": {**stati, **accesi},
        "timer attivi": {**stati, **attivi},
        "tutto": {**stati, **accesi, **attivi},
    }
    elenchi = 0
    for nome, variante in situazioni.items():
        await _carica(hass, variante)
        testi_oggi = [
            Template(m, hass).async_render(parse_result=False) for m in modelli_oggi
        ]
        await _carica(
            hass,
            {
                **{
                    e: v
                    for e, v in variante.items()
                    if e.split(".", 1)[0] in ("sensor", "binary_sensor")
                },
                **nativi.stati_nativi(variante),
            },
        )
        testi_domani = [
            Template(m, hass).async_render(parse_result=False) for m in modelli_domani
        ]
        for modello, prima, dopo in zip(
            modelli_oggi, testi_oggi, testi_domani, strict=True
        ):
            if "{%- set elenco = [" in modello:
                elenchi += 1
                continue
            assert _testi_nuovi(prima) == dopo, (nome, modello[:200])
    assert elenchi == 4


async def test_elenco_pulisci_cronologia(hass: HomeAssistant, schede) -> None:
    """L'elenco di «Pulisci cronologia» tradotto: 353 voci (475 di oggi meno le 122 interne,
    del motore o tolte). Il riquadro mostra sempre il ramo senza esclusioni (domani tutte le entità
    sono registrate: un'integrazione del catalogo non può escluderne dal Recorder), anche se
    il sensore delle entità escluse ha l'attributo «options» con l'elenco del package, come
    lo scrive oggi ``comandi.SensoreSceltaVMC`` (con quel ramo il riquadro direbbe 267
    entità registrate e 86 escluse)."""
    oggi, domani = schede
    elenco = next(m for m in nativi.modelli(domani) if "{%- set elenco = [" in m)
    elenco_oggi = next(m for m in nativi.modelli(oggi) if "{%- set elenco = [" in m)
    voci = re.findall(r"^\s*'([a-z_]+\.[a-z0-9_]+)',?$", elenco, re.MULTILINE)
    voci_oggi = re.findall(r"^\s*'([a-z_]+\.[a-z0-9_]+)',?$", elenco_oggi, re.MULTILINE)
    assert (len(voci_oggi), len(voci)) == (475, 353)
    mappa = mappa_fase_1()
    assert voci == [mappa[v] for v in voci_oggi if mappa[v] is not None]
    stati = nativi.leggi_stati()
    await _carica(
        hass,
        {
            **{
                e: v
                for e, v in stati.items()
                if e.split(".", 1)[0] in ("sensor", "binary_sensor")
            },
            **nativi.stati_nativi(stati),
        },
    )
    testo = Template(elenco, hass).async_render(parse_result=False)
    assert "Vuoi cancellare la cronologia di 353 entità della VMC «Master»?" in testo
    assert "escluse" not in testo and "registrate" not in testo
    assert "Elenco completo delle 353 entità" in testo
    assert SENSORE_ESCLUSE not in elenco
    # il sensore nativo con l'attributo «options» (l'elenco del package, coi nomi di oggi)
    opzioni = [
        nome_visibile(o, "master")
        for o in IMPOSTAZIONI["input_select.entita_escluse_recorder"]["options"]
    ]
    assert len(opzioni) == 423
    stato = hass.states.get(SENSORE_ESCLUSE)
    hass.states.async_set(
        SENSORE_ESCLUSE, stato.state, {**stato.attributes, "options": opzioni}
    )
    await hass.async_block_till_done()
    assert Template(elenco, hass).async_render(parse_result=False) == testo
    # le voci dell'elenco che il ramo tolto avrebbe chiamato escluse
    assert Counter(v.split(".", 1)[0] for v in voci if v in opzioni) == {
        "sensor": 71,
        "binary_sensor": 15,
    }
    righe = dict(
        re.findall(r"<tr><td[^>]*>([^<]+)</td><td[^>]*>(\d+)</td></tr>", testo)
    )
    assert righe == {
        "Sensori binari": "92",
        "Pulsanti": "12",
        "Interruttori": "37",
        "Orari": "30",
        "Valori numerici": "10",
        "Selettori": "14",
        "Testi": "1",
        "Sensori": "157",
    }


# ------------------------------------------------------------- riga conto alla rovescia
PROVA_RIGA = r"""
const classi = {};
globalThis.window = globalThis;
globalThis.HTMLElement = class extends EventTarget {
  replaceChildren(...figli) { this.figli = figli; }
};
globalThis.CustomEvent = class extends Event { constructor(t, o) { super(t, o); this.detail = o && o.detail; } };
globalThis.customElements = { get: (n) => classi[n], define: (n, c) => { classi[n] = c; } };
const creati = [];
window.loadCardHelpers = async () => ({ createRowElement: (config) => {
  const riga = new EventTarget(); riga.config = config; riga.setConfig = (c) => { riga.config = c; }; creati.push(riga); return riga;
} });
await import(new URL("./scheda.mjs", import.meta.url).href);
const Riga = classi["vmc-master-conto-alla-rovescia"];
const riga = new Riga();
riga.setConfig({ type: "custom:vmc-master-conto-alla-rovescia", entity: "sensor.vmc_master_lettura_ping", color: "state", name: "Ping", icon: "mdi:x", secondary_info: "last-updated" });
await new Promise((r) => setTimeout(r, 0));
const sensore = (stato) => ({ entity_id: "sensor.vmc_master_lettura_ping", state: stato,
  attributes: { device_class: "timestamp", friendly_name: "Prossima Lettura", icon: "mdi:timer-sync-outline" },
  last_changed: "2026-01-15T09:05:00+00:00", last_updated: "2026-01-15T09:05:01+00:00", context: { id: "c" } });
const esiti = {};
for (const [nome, stato] of [["attivo", "2026-01-15T09:05:10+00:00"], ["fermo", "unknown"], ["non disponibile", "unavailable"]]) {
  const s = sensore(stato);
  riga.hass = { states: { [s.entity_id]: s, "sensor.altro": { state: "1" } }, localize: "L" };
  const hass = creati[0].hass;
  esiti[nome] = { config: creati[0].config, stato: hass.states["timer.vmc_master_lettura_ping"], altro: hass.states["sensor.altro"], localize: hass.localize,
                  stessoOggetto: (riga.hass = { states: { [s.entity_id]: s }, localize: "L" }, creati[0].hass.states["timer.vmc_master_lettura_ping"] === hass.states["timer.vmc_master_lettura_ping"]) };
}
const aperti = [];
riga.addEventListener("hass-more-info", (e) => aperti.push(e.detail.entityId));
creati[0].dispatchEvent = undefined;
riga.dispatchEvent(new CustomEvent("hass-more-info", { detail: { entityId: "timer.vmc_master_lettura_ping" }, bubbles: true }));
esiti.informazioni = aperti;
console.log(JSON.stringify(esiti));
"""


def test_riga_conto_alla_rovescia(tmp_path: Path) -> None:
    """La riga della scheda costruisce dal sensore con l'ora di fine lo stato «timer» per la
    riga del timer di Home Assistant (attivo, fermo, non disponibile) e apre le informazioni
    del sensore."""
    node = shutil.which("node")
    if node is None:
        pytest.skip("node non installato")
    shutil.copyfile(JS, tmp_path / "scheda.mjs")
    (tmp_path / "prova.mjs").write_text(PROVA_RIGA, encoding="utf-8")
    uscita = subprocess.run(
        [node, str(tmp_path / "prova.mjs")],
        capture_output=True,
        text=True,
        check=True,
        timeout=60,
    )
    esiti = json.loads(uscita.stdout)
    config = {
        "entity": "timer.vmc_master_lettura_ping",
        "color": "state",
        "name": "Ping",
        "icon": "mdi:x",
        "secondary_info": "last-updated",
    }
    attributi = {"friendly_name": "Prossima Lettura", "icon": "mdi:timer-sync-outline"}
    tempi = {
        "last_changed": "2026-01-15T09:05:00+00:00",
        "last_updated": "2026-01-15T09:05:01+00:00",
        "context": {"id": "c"},
        "entity_id": "timer.vmc_master_lettura_ping",
    }
    assert esiti["attivo"]["config"] == config
    assert esiti["attivo"]["stato"] == {
        **tempi,
        "state": "active",
        "attributes": {
            **attributi,
            "remaining": "0:00:10",
            "finishes_at": "2026-01-15T09:05:10.000Z",
        },
    }
    assert esiti["fermo"]["stato"] == {
        **tempi,
        "state": "idle",
        "attributes": {**attributi, "remaining": "0:00:00"},
    }
    assert esiti["non disponibile"]["stato"]["state"] == "unavailable"
    for esito in ("attivo", "fermo", "non disponibile"):
        assert (
            esiti[esito]["altro"] == {"state": "1"} and esiti[esito]["localize"] == "L"
        )
        assert esiti[esito]["stessoOggetto"] is True
    assert esiti["informazioni"] == ["sensor.vmc_master_lettura_ping"]


# ------------------------------------------------------------------ tipo «testo»
def test_testo_aggiornato_va_a_capo_come_prima() -> None:
    """Un testo su più righe di un testo ripiegato («>») va a capo con lo stesso rientro,
    con il resto della sua ultima riga e senza superare la riga più lunga di prima."""
    scheda = "a: >\r\n  uno due tre\r\n  quattro cinque\r\nb: x\r\n"
    tradotta = traduci(scheda, Mappa({}), (Testo("due tre quattro", "2 3 4"),), ())
    assert tradotta.testo == "a: >\r\n  uno 2 3 4\r\n  cinque\r\nb: x\r\n"
    assert yaml.safe_load(tradotta.testo) == {"a": "uno 2 3 4 cinque\n", "b": "x"}
    assert [(m.riga, m.colonna, m.tipo, m.posto) for m in tradotta.modifiche] == [
        (2, 7, "testo", "a")
    ]
    # su una riga sola il testo nuovo resta dov'era, anche fra virgolette
    tradotta = traduci('a: "uno due"\r\n', Mappa({}), (Testo("due", "l'altro"),), ())
    assert tradotta.testo == 'a: "uno l\'altro"\r\n'


def test_testo_aggiornato_su_due_capoversi() -> None:
    """Un testo con «\\n» prende due capoversi (nel file la riga vuota fra i due): il testo
    nuovo li sostituisce tutti e due, a capo come prima."""
    scheda = "a: >\r\n  uno due\r\n\r\n  tre quattro\r\nb: x\r\n"
    assert yaml.safe_load(scheda) == {"a": "uno due\ntre quattro\n", "b": "x"}
    tradotta = traduci(scheda, Mappa({}), (Testo("due\ntre", "2 3"),), ())
    assert tradotta.testo == "a: >\r\n  uno 2 3\r\n  quattro\r\nb: x\r\n"
    assert yaml.safe_load(tradotta.testo) == {"a": "uno 2 3 quattro\n", "b": "x"}
    # senza «\\n» il testo non salta la riga vuota
    with pytest.raises(NonTraducibile, match="trovato 0 volte"):
        traduci(scheda, Mappa({}), (Testo("due tre", "2 3"),), ())


def test_commento_dell_intestazione() -> None:
    """Un testo di ``COMMENTI`` cambia una volta nelle righe di commento prima della
    scheda; la cornice di «#» resta allineata."""
    scheda = "###########\r\n# a (x)   #\r\n###########\r\nb: (x)\r\n"
    tradotta = traduci(scheda, Mappa({}), (), (Commento("(x)", "(xyz)"),))
    assert tradotta.testo == "###########\r\n# a (xyz) #\r\n###########\r\nb: (x)\r\n"
    tradotta = traduci(scheda, Mappa({}), (), (Commento("(x)", ""),))
    assert tradotta.testo == "###########\r\n# a       #\r\n###########\r\nb: (x)\r\n"
    assert [(m.riga, m.colonna, m.tipo, m.posto) for m in tradotta.modifiche] == [
        (2, 5, "intestazione", "commento")
    ]


@pytest.mark.parametrize(
    ("scheda", "commento", "motivo"),
    [
        ("# a #\r\nb: (x)\r\n", Commento("(x)", "(y)"), "trovato 0 volte"),
        ("# (x) (x) #\r\nb: c\r\n", Commento("(x)", "(y)"), "trovato 2 volte"),
        ("# a (x) #\r\nb: c\r\n", Commento("(x)", "(xyz)"), "cornice"),
        ("# a (x) b #\r\nb: c\r\n", Commento("(x)", "(y)"), "cornice"),
    ],
)
def test_commento_non_aggiornabile(
    scheda: str, commento: Commento, motivo: str
) -> None:
    """Un testo di ``COMMENTI`` fuori dall'intestazione, trovato più volte, troppo lungo per
    la cornice o non alla fine della riga ferma la traduzione."""
    with pytest.raises(NonTraducibile, match=motivo):
        traduci(scheda, Mappa({}), (), (commento,))


_ELENCO = "a: >-\r\n  {%- set elenco = [\r\n    'sensor.x'\r\n  ] -%}\r\n"
_RAMO = "".join(f"  {r}\r\n" for r in RAMO_ESCLUSE)


def test_ramo_delle_entita_escluse() -> None:
    """Dal modello di «Pulisci cronologia» esce il ramo per le entità escluse dal Recorder,
    con il suo «endif»: resta il ramo «else»."""
    scheda = f"{_ELENCO}{_RAMO}  A\r\n  {{%- else -%}}\r\n  B\r\n  {{%- endif -%}}\r\nb: x\r\n"
    tradotta = traduci(scheda, Mappa({"sensor.x": "sensor.x"}), (), ())
    assert tradotta.testo == f"{_ELENCO}  B\r\nb: x\r\n"
    assert [(m.riga, m.tipo, m.prima) for m in tradotta.modifiche] == [
        (5, "esclusioni", RAMO_ESCLUSE[0]),
        (6, "esclusioni", RAMO_ESCLUSE[1]),
        (7, "esclusioni", RAMO_ESCLUSE[2]),
        (8, "esclusioni", "A"),
        (9, "esclusioni", "{%- else -%}"),
        (11, "esclusioni", "{%- endif -%}"),
    ]


@pytest.mark.parametrize(
    ("ramo", "motivo"),
    [
        ("  B\r\n", "non trovato"),
        (
            _RAMO.replace("is not none", "is none")
            + "  {%- else -%}\r\n  {%- endif -%}\r\n",
            "non previsto",
        ),
        (_RAMO + "  {%- endif -%}\r\n", "non unici"),
        (_RAMO + "  {%- endif -%}\r\n  {%- else -%}\r\n", "fuori ordine"),
        (_RAMO + "  {%- else -%}\r\n  {%- endif -%}\r\n  B\r\n", "non alla fine"),
    ],
)
def test_ramo_delle_entita_escluse_non_previsto(ramo: str, motivo: str) -> None:
    """Un modello di «Pulisci cronologia» senza il ramo delle entità escluse, con un ramo
    diverso o con «else» ed «endif» non come oggi ferma la traduzione."""
    with pytest.raises(NonTraducibile, match=motivo):
        traduci(f"{_ELENCO}{ramo}b: x\r\n", Mappa({"sensor.x": "sensor.x"}), (), ())


@pytest.mark.parametrize(
    ("scheda", "testo", "motivo"),
    [
        ("a: |\r\n  uno due\r\n  tre\r\n", Testo("due tre", "2 3"), "fuori da un"),
        ("a: >\r\n  x\r\n    due\r\n    tre\r\n", Testo("due tre", "2 3"), "rientrate"),
        ("a: >\r\n  due tre\r\n", Testo("due", "2", 2), "trovato 1 volte"),
        ("a: 'uno due'\r\n", Testo("due", "2"), "escape"),
    ],
)
def test_testo_non_aggiornabile(scheda: str, testo: Testo, motivo: str) -> None:
    """Un testo su più righe fuori da un «>» o su righe più rientrate (dove gli a capo
    restano), trovato un numero di volte diverso o da scrivere con escape ferma la
    traduzione."""
    with pytest.raises(NonTraducibile, match=motivo):
        traduci(scheda, Mappa({}), (testo,), ())
