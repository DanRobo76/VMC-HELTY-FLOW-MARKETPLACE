"""Passaggio dalla beta (package) all'integrazione nativa, con la conferma dell'utente.

Chi ha la beta (9.0.0bN) ha per ogni VMC il package che la beta stessa ha scritto in
/config/packages/vmc_helty_flow/‹nome› (con il marcatore ``.vmc_master_integrazione.json``).
Dopo l'aggiornamento, al primo avvio il package è ancora caricato: le sue entità hanno gli
entity_id che le entità native vogliono, e le sue automazioni gli stessi id di quelle del
motore. Finché c'è, la VMC nativa non parte (``IN_ATTESA``) e la VMC continua con il
package com'era.

1. Ad avvio finito si leggono dal package ancora caricato i valori che servono alla VMC
   nativa (``leggi_valori``): le 173 impostazioni visibili (valore di partenza delle
   entità native, come il ripristino dopo un riavvio), i 68 valori interni (archivio della
   memoria interna del motore) e i 10 sensori con memoria. Si salvano nell'archivio
   dell'integrazione (``.storage``), niente in /config.
2. Una riparazione chiede di confermare la rimozione della cartella del package e dei
   suoi elementi del registro delle entità (``async_conferma``): solo dopo il clic
   dell'utente, e solo per le cartelle scritte dalla beta. Alla conferma i valori si
   rileggono (sono quelli di quel momento).
3. Dopo il riavvio la cartella non c'è più, gli entity_id sono liberi e nascono le entità
   native con gli stessi entity_id dei sensori (``valori_passati``): la cronologia dei
   sensori continua.

Una cartella senza marcatore è un'installazione fatta a mano: non si tocca mai
(``MANUALE``), e la VMC nativa non parte finché c'è.
"""

from __future__ import annotations

import json
import logging
import re
import shutil
from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Final

import yaml
from homeassistant.components.lovelace import LOVELACE_DATA
from homeassistant.const import EntityStateAttribute
from homeassistant.core import HomeAssistant, State, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.restore_state import STATE_EXPIRATION
from homeassistant.helpers.restore_state import async_get as memoria_ripristino
from homeassistant.helpers.storage import Store
from homeassistant.util import dt as dt_util

from .nativa.comandi import chiavi_comandi
from .nativa.memoria import IN_ORDINE as SENSORI_CON_MEMORIA
from .nativa.motore.memoria_interna import (
    CHIAVE_ARCHIVIO as CHIAVE_MEMORIA_INTERNA,
)
from .nativa.motore.memoria_interna import (
    VERSIONE_ARCHIVIO as VERSIONE_MEMORIA_INTERNA,
)
from .nativa.motore.memoria_interna import da_stato
from .nativa.tabelle import DOMANI
from .nativa.vmc import ATTRIBUTO_INTERRUZIONE

_LOGGER = logging.getLogger(__name__)

FILE_MARCATORE: Final = ".vmc_master_integrazione.json"
"""Il file che la beta scriveva nella cartella del package di ogni VMC."""

CHIAVE_ARCHIVIO: Final = "vmc_master.passaggio.{nome}"
VERSIONE_ARCHIVIO: Final = 1

# Situazione di una VMC all'avvio
NATIVA: Final = "nativa"
"""Niente della beta: la VMC nativa parte."""
IN_ATTESA: Final = "in_attesa"
"""C'è il package della beta (o i suoi elementi del registro): si aspetta la conferma."""
MANUALE: Final = "manuale"
"""C'è un'installazione fatta a mano: non si tocca e la VMC nativa non parte."""

# Stato del passaggio nell'archivio della VMC
LETTO: Final = "letto"
CONFERMATO: Final = "confermato"
APPLICATO: Final = "applicato"

# Le piattaforme degli elementi del package nel registro (dominio, piattaforma): tutte
# YAML, senza voce di configurazione
_PIATTAFORME_PACKAGE: Final = frozenset(
    {
        "input_boolean",
        "input_number",
        "input_text",
        "input_select",
        "input_datetime",
        "timer",
        "script",
        "automation",
        "template",
        "rest",
        "command_line",
        "tcp",
    }
)
# Domini YAML in cui l'unique_id di un'entità è la sua chiave (piattaforma = dominio)
_DOMINI_CON_CHIAVE: Final = (
    "counter",
    "input_boolean",
    "input_button",
    "input_datetime",
    "input_number",
    "input_select",
    "input_text",
    "schedule",
    "script",
    "timer",
)
# Integrazioni con un elenco di blocchi {dominio: entità} (piattaforma = integrazione)
_INTEGRAZIONI_A_BLOCCHI: Final = ("command_line", "rest", "template")


class _CaricatoreYaml(getattr(yaml, "CSafeLoader", yaml.SafeLoader)):  # type: ignore[misc]
    """Legge i file del package; i tag di Home Assistant (!secret, !include...) valgono None."""


_CaricatoreYaml.add_multi_constructor("!", lambda _loader, _suffisso, _nodo: None)


# --- la cartella del package ------------------------------------------------------------------


def cartella_package(config_dir: str, nome: str) -> Path:
    """La cartella del package della beta per la VMC ``nome`` (solo da leggere o, dopo la
    conferma dell'utente, da togliere)."""
    return Path(config_dir) / "packages" / "vmc_helty_flow" / nome


def esamina_cartella(config_dir: str, nome: str) -> str | None:
    """«beta» se c'è la cartella scritta dalla beta (con il marcatore), «manuale» se c'è
    una cartella con file ma senza marcatore, None se non c'è (o è vuota)."""
    cartella = cartella_package(config_dir, nome)
    if not cartella.is_dir():
        return None
    if (cartella / FILE_MARCATORE).is_file():
        return "beta"
    return "manuale" if any(cartella.iterdir()) else None


def _come_lista(valore: object) -> list[Any]:
    return valore if isinstance(valore, list) else [valore]


def _id_della_configurazione(
    configurazione: object, id_package: set[tuple[str, str, str]]
) -> None:
    """Aggiunge gli id delle entità di un file YAML come (dominio, piattaforma, unique_id),
    come li salva il registro delle entità (anche per le entità rinominate dall'utente)."""
    if not isinstance(configurazione, dict):
        return
    for dominio, valore in configurazione.items():
        if dominio == "automation":
            for automazione in _come_lista(valore):
                if isinstance(automazione, dict) and automazione.get("id") is not None:
                    id_package.add(("automation", "automation", str(automazione["id"])))
        elif dominio in _DOMINI_CON_CHIAVE:
            if isinstance(valore, dict):
                id_package.update((dominio, dominio, str(chiave)) for chiave in valore)
        elif dominio in _INTEGRAZIONI_A_BLOCCHI:
            for blocco in _come_lista(valore):
                if not isinstance(blocco, dict):
                    continue
                prefisso = blocco.get("unique_id") if dominio == "template" else None
                for dominio_entita, entita in blocco.items():
                    for voce in _come_lista(entita):
                        if isinstance(voce, dict) and voce.get("unique_id") is not None:
                            unique_id = str(voce["unique_id"])
                            if prefisso is not None:
                                unique_id = f"{prefisso}-{unique_id}"
                            id_package.add((str(dominio_entita), dominio, unique_id))
        else:
            # piattaforme in elenco (sensor: - platform: rest ... unique_id: ...)
            for voce in _come_lista(valore):
                if (
                    isinstance(voce, dict)
                    and voce.get("platform")
                    and voce.get("unique_id") is not None
                ):
                    id_package.add(
                        (dominio, str(voce["platform"]), str(voce["unique_id"]))
                    )


def _id_dei_testi(testi: Iterable[str]) -> set[tuple[str, str, str]]:
    id_package: set[tuple[str, str, str]] = set()
    for testo in testi:
        _id_della_configurazione(yaml.load(testo, Loader=_CaricatoreYaml), id_package)
    return id_package


@lru_cache(maxsize=8)
def _id_del_package_della_beta(nome: str) -> frozenset[tuple[str, str, str]]:
    """Gli id del package che la beta scriveva per la VMC ``nome`` (dal testo che generava,
    solo in memoria: gli unique_id non dipendono dall'IP)."""
    from .installatore import genera_file  # solo per la VMC senza cartella

    testi = [
        t for n, t in genera_file(nome, "0.0.0.0", "0").items() if n.endswith(".yaml")
    ]
    return frozenset(_id_dei_testi(testi))


def id_del_package(config_dir: str, nome: str) -> frozenset[tuple[str, str, str]]:
    """Gli id del registro (dominio, piattaforma, unique_id) del package della VMC: dai
    file YAML della cartella, se c'è e si legge, più quelli del package che la beta
    scriveva (cartella cambiata a mano o già tolta)."""
    id_package = set(_id_del_package_della_beta(nome))
    cartella = cartella_package(config_dir, nome)
    try:
        file_yaml = sorted(p for p in cartella.glob("*.yaml") if p.is_file())
        testi = [p.read_text(encoding="utf-8") for p in file_yaml]
        id_package |= _id_dei_testi(testi)
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as errore:
        _LOGGER.warning("File del package in %s non leggibili: %s", cartella, errore)
    return frozenset(id_package)


@callback
def possibili_voci_della_beta(hass: HomeAssistant, nome: str) -> bool:
    """Controllo veloce: nel registro c'è qualche elemento YAML (senza voce di
    configurazione) di una piattaforma del package con l'entity_id della VMC? Le automazioni
    non contano: quelle del motore nativo hanno gli stessi id di quelle del package."""
    prefisso = f"vmc_{nome}_"
    return any(
        voce.config_entry_id is None
        and voce.platform in _PIATTAFORME_PACKAGE
        and voce.platform != "automation"
        and voce.entity_id.split(".", 1)[1].startswith(prefisso)
        for voce in er.async_get(hass).entities.values()
    )


@callback
def voci_del_package(
    hass: HomeAssistant,
    id_package: Iterable[tuple[str, str, str]],
    *,
    anche_automazioni: bool = True,
) -> list[str]:
    """Gli entity_id degli elementi del registro del package (stessi dominio, piattaforma e
    unique_id, senza voce di configurazione: niente creato dall'utente, anche se si chiama
    «vmc_‹nome›_…»)."""
    ids = set(id_package)
    return sorted(
        voce.entity_id
        for voce in er.async_get(hass).entities.values()
        if voce.config_entry_id is None
        and (voce.domain, voce.platform, voce.unique_id) in ids
        and (anche_automazioni or voce.platform != "automation")
    )


# --- i valori della beta ----------------------------------------------------------------------


def entity_id_di_oggi(chiave: str, nome: str) -> str:
    """L'entity_id dell'elemento del package per una chiave («input_boolean.x»)."""
    dominio, oggetto = chiave.split(".", 1)
    return f"{dominio}.vmc_{nome}_{oggetto}"


def entity_id_di_domani(chiave: str, nome: str) -> str | None:
    """L'entity_id nativo di una voce del package (None se è interna al motore)."""
    dominio = DOMANI[chiave]
    if dominio == "interna":
        return None
    return f"{dominio}.vmc_{nome}_{chiave.split('.', 1)[1]}"


@callback
def stato_della_beta(hass: HomeAssistant, entity_id: str) -> State | None:
    """Lo stato di un elemento del package: quello vivo (package caricato) oppure, se
    l'elemento non è caricato ma è ancora nel registro, l'ultimo che Home Assistant ha
    conservato per il ripristino (lo stesso che il package avrebbe ripreso al riavvio)."""
    stato = hass.states.get(entity_id)
    if stato is not None and not stato.attributes.get(EntityStateAttribute.RESTORED):
        return stato
    conservato = memoria_ripristino(hass).async_get_stored_state(entity_id)
    return None if conservato is None else conservato.state


@dataclass
class Letti:
    """I valori letti dal package di una VMC."""

    impostazioni: dict[str, str] = field(default_factory=dict)
    """Le impostazioni visibili: chiave -> stato (il valore di partenza dell'entità nativa)."""
    interni: dict[str, Any] = field(default_factory=dict)
    """I valori interni: chiave -> valore come lo salva la memoria interna."""
    memorie: dict[str, dict[str, Any]] = field(default_factory=dict)
    """I sensori con memoria: chiave -> {"state", "attributes"}."""
    non_letti: list[str] = field(default_factory=list)
    """Le chiavi senza un valore da leggere (partono come una VMC nuova)."""
    timer_attivi: list[str] = field(default_factory=list)
    """I timer attivi o in pausa al momento della lettura (non passano: vedi ``leggi_valori``)."""
    caricato: bool = False
    """Se il package era caricato (allora dopo la conferma serve un riavvio)."""

    def come_dati(self) -> dict[str, Any]:
        return {
            "impostazioni": self.impostazioni,
            "interni": self.interni,
            "memorie": self.memorie,
            "non_letti": self.non_letti,
            "timer_attivi": self.timer_attivi,
        }


@callback
def leggi_valori(hass: HomeAssistant, nome: str) -> Letti:
    """I valori del package della VMC ``nome`` che servono alla VMC nativa.

    - le 173 impostazioni visibili: lo stato dell'aiutante, che l'entità nativa riprende
      con le regole dell'aiutante (``initial`` vince, numero fuori dai limiti al minimo,
      opzione che non c'è alla prima...), come dopo un riavvio della beta;
    - i 68 valori interni: il valore come lo salva la memoria interna (``da_stato``);
    - i 10 sensori con memoria: stato e attributo dell'ultima lettura prima
      dell'interruzione.

    I 34 timer non passano: nessun timer del package ha ``restore``, quindi dopo il
    riavvio del passaggio ripartono fermi come dopo ogni riavvio della beta (si annotano
    solo quelli attivi). Script e comandi di shell non hanno valori.
    """
    letti = Letti()
    visibili = set(chiavi_comandi())
    for chiave in DOMANI:
        dominio = chiave.split(".", 1)[0]
        if dominio in ("script", "shell_command"):
            continue
        entity_id = entity_id_di_oggi(chiave, nome)
        stato = stato_della_beta(hass, entity_id)
        vivo = hass.states.get(entity_id)
        if vivo is not None and not vivo.attributes.get(EntityStateAttribute.RESTORED):
            letti.caricato = True
        if dominio == "timer":
            if stato is not None and stato.state in ("active", "paused"):
                letti.timer_attivi.append(chiave)
            continue
        if stato is None:
            letti.non_letti.append(chiave)
        elif chiave in visibili:
            letti.impostazioni[chiave] = stato.state
        else:  # le altre voci (tranne script, comandi e timer) sono i valori interni
            letti.interni[chiave] = da_stato(chiave, stato.state)
    for chiave in SENSORI_CON_MEMORIA:
        stato = stato_della_beta(hass, entity_id_di_oggi(chiave, nome))
        if stato is None:
            letti.non_letti.append(chiave)
            continue
        attributi = {}
        if ATTRIBUTO_INTERRUZIONE in stato.attributes:
            attributi[ATTRIBUTO_INTERRUZIONE] = stato.attributes[ATTRIBUTO_INTERRUZIONE]
        letti.memorie[chiave] = {"state": stato.state, "attributes": attributi}
    return letti


def valori_passati(dati: Mapping[str, Any], nome: str) -> dict[str, State]:
    """Gli stati passati alla VMC nativa (chiave -> State con l'entity_id nativo): le
    impostazioni visibili e i sensori con memoria salvati alla conferma. Le entità native
    li usano solo se Home Assistant non ha un loro stato conservato."""
    passati: dict[str, State] = {}
    for chiave, stato in (dati.get("impostazioni") or {}).items():
        entity_id = entity_id_di_domani(chiave, nome) if chiave in DOMANI else None
        if entity_id is not None and isinstance(stato, str):
            passati[chiave] = State(entity_id, stato, validate_entity_id=False)
    for chiave, voce in (dati.get("memorie") or {}).items():
        if isinstance(voce, dict) and isinstance(voce.get("state"), str):
            passati[chiave] = State(
                entity_id_di_oggi(chiave, nome),
                voce["state"],
                dict(voce.get("attributes") or {}),
                validate_entity_id=False,
            )
    return passati


# --- l'archivio ---------------------------------------------------------------------------------


def archivio(hass: HomeAssistant, nome: str) -> Store[dict[str, Any]]:
    """L'archivio del passaggio della VMC ``nome`` (``.storage``)."""
    return Store(hass, VERSIONE_ARCHIVIO, CHIAVE_ARCHIVIO.format(nome=nome))


async def async_salva_letti(
    hass: HomeAssistant, nome: str, letti: Letti, stato: str = LETTO
) -> None:
    """Salva i valori letti; alla conferma anche i valori interni nell'archivio della
    memoria interna del motore (lo legge all'avvio della VMC nativa)."""
    await archivio(hass, nome).async_save(
        {"stato": stato, "letto": dt_util.utcnow().isoformat(), **letti.come_dati()}
    )
    if stato == CONFERMATO:
        await Store(
            hass,
            VERSIONE_MEMORIA_INTERNA,
            CHIAVE_MEMORIA_INTERNA.format(nome=nome),
        ).async_save({"valori": letti.interni})


async def async_applicato(
    hass: HomeAssistant, nome: str, dati: Mapping[str, Any]
) -> None:
    """La VMC nativa è partita con i valori passati e Home Assistant li ha già conservati:
    nell'archivio restano solo i conteggi."""
    await archivio(hass, nome).async_save(
        {
            "stato": APPLICATO,
            "letto": dati.get("letto"),
            "applicato": dt_util.utcnow().isoformat(),
            "conteggi": {
                parte: len(dati.get(parte) or ())
                for parte in ("impostazioni", "interni", "memorie", "non_letti")
            },
        }
    )


def _memoria_interna(hass: HomeAssistant, nome: str) -> Store[dict[str, Any]]:
    return Store(
        hass, VERSIONE_MEMORIA_INTERNA, CHIAVE_MEMORIA_INTERNA.format(nome=nome)
    )


async def async_togli_archivi(hass: HomeAssistant, nome: str) -> None:
    """VMC eliminata: via il suo archivio del passaggio. La memoria interna resta, con
    l'istante dell'eliminazione: come Home Assistant con le entità tolte con la voce
    (stessa voce del registro e stesso stato se tornano entro ``STATE_EXPIRATION``), e
    come gli aiutanti della beta, una VMC aggiunta di nuovo con lo stesso nome riparte
    con i suoi valori interni (le ultime scelte delle entità comprese)."""
    await archivio(hass, nome).async_remove()
    memoria = _memoria_interna(hass, nome)
    dati = await memoria.async_load()
    if isinstance(dati, dict):
        await memoria.async_save({**dati, "eliminata": dt_util.utcnow().isoformat()})


async def async_memoria_di_una_vmc_eliminata(hass: HomeAssistant, nome: str) -> None:
    """All'avvio della VMC nativa: la memoria interna di una VMC eliminata vale se la VMC
    torna entro ``STATE_EXPIRATION`` (come gli stati delle entità), poi si toglie."""
    memoria = _memoria_interna(hass, nome)
    dati = await memoria.async_load()
    if not isinstance(dati, dict) or "eliminata" not in dati:
        return
    eliminata = dt_util.parse_datetime(str(dati["eliminata"]))
    if eliminata is None or dt_util.utcnow() - eliminata > STATE_EXPIRATION:
        await memoria.async_remove()
        return
    await memoria.async_save({k: v for k, v in dati.items() if k != "eliminata"})


# --- la conferma ----------------------------------------------------------------------------------


@dataclass
class EsitoConferma:
    """Cosa ha fatto la conferma per una VMC."""

    nome: str
    voci_tolte: list[str] = field(default_factory=list)
    cartella_tolta: bool = False
    riavvio: bool = False
    errore: str | None = None
    riferimenti: list[tuple[str, str, str | None]] = field(default_factory=list)
    """Dove l'utente usa ancora i vecchi nomi (``async_riferimenti_personali``)."""


def _togli_cartella(config_dir: str, nome: str) -> bool:
    """Toglie la cartella del package scritta dalla beta (solo con il marcatore); la
    cartella vmc_helty_flow solo se resta vuota."""
    cartella = cartella_package(config_dir, nome)
    if esamina_cartella(config_dir, nome) != "beta":
        return False
    shutil.rmtree(cartella)
    try:
        cartella.parent.rmdir()
    except OSError:
        pass  # ci sono altre VMC (o altri file): resta
    _LOGGER.info("Cartella del package della beta tolta: %s", cartella)
    return True


async def async_conferma(hass: HomeAssistant, nome: str) -> EsitoConferma:
    """Il passaggio confermato dall'utente per la VMC ``nome``: rilegge e salva i valori,
    toglie dal registro gli elementi del package (le entità caricate escono subito) e
    toglie la cartella scritta dalla beta. Se il package era caricato serve un riavvio."""
    esito = EsitoConferma(nome)
    config_dir = hass.config.config_dir
    letti = leggi_valori(hass, nome)
    await async_salva_letti(hass, nome, letti, CONFERMATO)
    id_package = await hass.async_add_executor_job(id_del_package, config_dir, nome)
    # prima di togliere gli elementi del package (servono a riconoscere i suoi)
    esito.riferimenti = await async_riferimenti_personali(hass, nome, id_package)
    registro = er.async_get(hass)
    for entity_id in voci_del_package(hass, id_package):
        registro.async_remove(entity_id)
        esito.voci_tolte.append(entity_id)
    try:
        esito.cartella_tolta = await hass.async_add_executor_job(
            _togli_cartella, config_dir, nome
        )
    except OSError as errore:
        esito.errore = str(errore)
        _LOGGER.warning("Cartella del package della VMC %s non tolta: %s", nome, errore)
    esito.riavvio = letti.caricato or esito.cartella_tolta
    _LOGGER.info(
        "Passaggio della VMC %s confermato: %s valori, %s elementi del registro tolti",
        nome,
        len(letti.impostazioni) + len(letti.interni) + len(letti.memorie),
        len(esito.voci_tolte),
    )
    return esito


# --- le impostazioni che cambiano dominio ------------------------------------------------------------


_RE_ENTITY_ID = re.compile(r"(?<![\w.])([a-z_]+\.vmc_[a-z]+_[a-z0-9_]+)(?![\w])")


def _configurazioni_personali(
    hass: HomeAssistant, del_package: set[str]
) -> Iterator[tuple[str, str]]:
    """(entity_id, testo) di ogni automazione e script caricato che non è del package:
    la configurazione come l'utente l'ha scritta (``raw_config``), gli ingressi dei
    progetti (blueprint) e le entità che Home Assistant vi trova."""
    for dominio in ("automation", "script"):
        componente = hass.data.get(dominio)
        for entita in getattr(componente, "entities", ()):
            if entita.entity_id in del_package:
                continue
            parti = [
                getattr(entita, "raw_config", None),
                getattr(entita, "_raw_blueprint_inputs", None),
                sorted(getattr(entita, "referenced_entities", ())),
            ]
            yield (
                entita.entity_id,
                json.dumps([p for p in parti if p], ensure_ascii=False, default=str),
            )


async def async_riferimenti_personali(
    hass: HomeAssistant, nome: str, id_package: Iterable[tuple[str, str, str]]
) -> list[tuple[str, str, str | None]]:
    """Dove l'utente usa le voci del package che domani cambiano dominio o non ci sono
    più: automazioni e script suoi (non quelli del package) e plance salvate in Home
    Assistant. Restituisce (dove, nome di oggi, entity_id di domani o None).

    Si cerca nel testo della configurazione, quindi ogni uso: entità (anche nei modelli
    e come bersaglio dei servizi ``input_*.*``, ``timer.*``, ``script.turn_on``) e
    servizi del package che non ci sono più (``script.‹id›`` e ``shell_command.‹id›``
    come azione)."""
    vecchi = {entity_id_di_oggi(c, nome): entity_id_di_domani(c, nome) for c in DOMANI}
    del_package = set(voci_del_package(hass, id_package))
    trovati: list[tuple[str, str, str | None]] = []
    for dove, testo in _configurazioni_personali(hass, del_package):
        for vecchio in sorted(set(_RE_ENTITY_ID.findall(testo)) & set(vecchi)):
            trovati.append((dove, vecchio, vecchi[vecchio]))
    dati = hass.data.get(LOVELACE_DATA)
    for chiave, plancia in dati.dashboards.items() if dati is not None else ():
        try:
            config = await plancia.async_load(False)
        except Exception as errore:  # noqa: BLE001 - plancia YAML o vuota: non si legge
            _LOGGER.debug("Plancia %s non letta: %s", chiave, errore)
            continue
        testo = json.dumps(config, ensure_ascii=False)
        for vecchio in sorted(set(_RE_ENTITY_ID.findall(testo)) & set(vecchi)):
            trovati.append(
                (f"lovelace:{chiave or 'lovelace'}", vecchio, vecchi[vecchio])
            )
    return sorted(set(trovati), key=lambda t: (t[0], t[1]))
