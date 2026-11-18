"""Integrazione VMC Master per VMC Helty Flow Plus/Elite.

Ogni voce di configurazione e' una VMC (nome + IP). Per ogni VMC l'integrazione
installa e aggiorna il package della release 8.6.0 in packages/vmc_helty_flow/<nome>
e serve la scheda «VMC Master», che si aggiunge dalla plancia senza incollare codice.
"""

from __future__ import annotations

import asyncio
import json
import logging
import sys
import re
import threading
import time
from functools import lru_cache
from http import HTTPStatus
from pathlib import Path
from typing import Any

import yaml
from aiohttp import web

from homeassistant.components import persistent_notification
from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import HomeAssistantView, StaticPathConfig
from homeassistant.config_entries import ConfigEntry, ConfigEntryState
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.exceptions import ConfigEntryError
from homeassistant.helpers import (
    config_validation as cv,
    entity_registry as er,
    issue_registry as ir,
)
from homeassistant.helpers.http import KEY_HASS
from homeassistant.helpers.start import async_at_started
from homeassistant.helpers.storage import Store
from homeassistant.helpers.typing import ConfigType
from homeassistant.loader import async_get_integration

from .const import (
    CONF_HOST,
    CONF_NOME,
    CONF_TITOLO,
    DOMAIN,
    ENTITA_FINESTRA_CLONA,
    ENTITA_PRIMA_INSTALLAZIONE,
    FILE_SCHEDA,
    FILE_SCHEDA_JS,
    NOME_MASTER,
    NOME_RE,
    URL_FRONTEND,
)
from . import config_flow, prima_installazione
from .installatore import (
    _leggi,
    _rimetti_ip,
    _scrivi,
    cartella_vmc,
    genera_file,
    installa,
    ip_nel_package,
    leggi_marcatore,
    sposta_in_backup,
)
from .trasforma import adatta_link_repository, per_vmc

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

_CARTELLA = Path(__file__).parent

ISSUE_RIAVVIO = "riavvio_necessario"
ISSUE_PACKAGES = "packages_non_abilitati"
ISSUE_DISABILITATA = "voce_disabilitata"
DATI_RICARICHE = f"{DOMAIN}_ricariche"
# Nomi delle VMC eliminate: al prossimo avvio si tolgono dal registro le loro entita'
CHIAVE_ELIMINATE = f"{DOMAIN}.vmc_eliminate"
DATI_ELIMINATE = f"{DOMAIN}_eliminate"
DATI_BLOCCO_ELIMINATE = f"{DOMAIN}_eliminate_blocco"
# Errori dei sensori TCP con la VMC spenta: al massimo uno ogni 30 minuti per ogni VMC
LOGGER_TCP = "homeassistant.components.tcp.entity"
INTERVALLO_LOG_TCP = 30 * 60
DATI_FILTRO_TCP = f"{DOMAIN}_filtro_tcp"
_RE_IP_NEL_LOG = re.compile(r"(?<![0-9.])([0-9]{1,3}(?:\.[0-9]{1,3}){3})(?![0-9]|\.[0-9])")
# Un solo controllo alla volta dell'IP scritto dalla scheda (voci avviate in parallelo)
DATI_BLOCCO_IP = f"{DOMAIN}_ip_scheda_blocco"

# Domini YAML in cui l'unique_id di un'entita' e' la sua chiave (piattaforma = dominio)
DOMINI_CON_CHIAVE = (
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
# Integrazioni con un elenco di blocchi {dominio: entita'} (piattaforma = integrazione)
INTEGRAZIONI_A_BLOCCHI = ("command_line", "rest", "template")


class _CaricatoreYaml(getattr(yaml, "CSafeLoader", yaml.SafeLoader)):  # type: ignore[misc]
    """Legge i file del package; i tag di Home Assistant (!secret, !include...) valgono None."""


_CaricatoreYaml.add_multi_constructor("!", lambda _loader, _suffisso, _nodo: None)

# Ordine delle ricariche: prima aiutanti e sensori, per ultime script e automazioni che li usano
ORDINE_RICARICHE = (
    "homeassistant.reload_core_config",
    "input_boolean.reload",
    "input_datetime.reload",
    "input_number.reload",
    "input_select.reload",
    "input_text.reload",
    "timer.reload",
    "command_line.reload",
    "rest.reload",
    "template.reload",
    "script.reload",
    "automation.reload",
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Registra la scheda «VMC Master»: file JavaScript e configurazione per ogni VMC."""
    integrazione = await async_get_integration(hass, DOMAIN)
    await hass.http.async_register_static_paths(
        [StaticPathConfig(URL_FRONTEND, str(_CARTELLA / "frontend"), False)]
    )
    # Il numero di versione nell'indirizzo fa ricaricare la scheda dopo ogni aggiornamento
    add_extra_js_url(hass, f"{URL_FRONTEND}/{FILE_SCHEDA_JS}?v={integrazione.version}")
    hass.http.register_view(VmcSchedaView())
    async_at_started(hass, _ripristina_wifi_server)
    async_at_started(hass, _togli_entita_vmc_eliminate)

    async def _alla_fermata(_evento: Event) -> None:
        await _prepara_aggiornamento(hass, str(integrazione.version))

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, _alla_fermata)
    return True


# Programma del processo separato: carica i moduli della versione su disco senza il loro
# __init__.py (che importa Home Assistant) e avvia prepara.main
_PROGRAMMA_PREPARA = (
    "import importlib, sys, types\n"
    "p = types.ModuleType('vmc_master_aggiornata'); p.__path__ = [sys.argv[1]]\n"
    "sys.modules['vmc_master_aggiornata'] = p\n"
    "sys.exit(importlib.import_module('vmc_master_aggiornata.prepara').main(sys.argv[2:]))\n"
)
TIMEOUT_PREPARA = 60


def _versione_su_disco() -> str | None:
    """Versione dell'integrazione su disco, se ha il modulo che prepara i package."""
    if not (_CARTELLA / "prepara.py").is_file():
        return None
    try:
        return str(json.loads((_CARTELLA / "manifest.json").read_text(encoding="utf-8"))["version"])
    except (OSError, ValueError, KeyError):
        return None


async def _prepara_aggiornamento(hass: HomeAssistant, versione: str) -> None:
    """Home Assistant si ferma con una versione nuova gia' su disco (aggiornamento
    scaricato): i package si scrivono adesso con la versione nuova, cosi' al riavvio
    Home Assistant li legge gia' aggiornati e non chiede un secondo riavvio."""
    su_disco = await hass.async_add_executor_job(_versione_su_disco)
    if su_disco is None or su_disco == versione:
        return
    voci = [
        [voce.data[CONF_NOME], voce.data[CONF_HOST]]
        for voce in hass.config_entries.async_entries(DOMAIN)
        if voce.state is ConfigEntryState.LOADED
    ]
    if not voci:
        return
    try:
        processo = await asyncio.create_subprocess_exec(
            sys.executable,
            "-I",
            "-c",
            _PROGRAMMA_PREPARA,
            str(_CARTELLA),
            hass.config.config_dir,
            json.dumps(voci),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    except OSError as errore:
        _LOGGER.warning("Package non preparati per la versione %s: %s", su_disco, errore)
        return
    try:
        uscita, errori = await asyncio.wait_for(processo.communicate(), TIMEOUT_PREPARA)
    except TimeoutError as errore:
        processo.kill()  # le scritture sono atomiche: ogni file resta vecchio o nuovo
        await processo.wait()
        _LOGGER.warning("Package non preparati per la versione %s: %s", su_disco, errore)
        return
    if processo.returncode:
        _LOGGER.warning(
            "Package non preparati per la versione %s: %s",
            su_disco,
            errori.decode(errors="replace").strip()[-500:],
        )
        return
    _LOGGER.info(
        "Package preparati per la versione %s: %s", su_disco, uscita.decode(errors="replace").strip()
    )


def _italiano(hass: HomeAssistant) -> bool:
    """Notifiche in italiano se Home Assistant e' in italiano, altrimenti in inglese."""
    return (hass.config.language or "").lower().startswith("it")


async def _ripristina_wifi_server(hass: HomeAssistant) -> None:
    """Home Assistant riavviato durante il collegamento di una VMC al Wi-Fi: il Wi-Fi
    del server si riporta alla rete di prima (come faceva l'avvio della Finestra
    Prima Installazione VMC della release 8.6.0)."""
    config_dir = hass.config.config_dir
    if not await hass.async_add_executor_job(prima_installazione.ripristino_in_sospeso, config_dir):
        return
    try:
        await hass.async_add_executor_job(prima_installazione.esegui, config_dir, "recover")
    except prima_installazione.Failure as errore:
        _LOGGER.warning("Ripristino del Wi-Fi del server non riuscito: %s", errore.message)
        messaggio = await config_flow.async_messaggio_errore(hass, errore)
        if _italiano(hass):
            testo = (
                f"{messaggio}\n\nIl Wi-Fi del server potrebbe essere ancora sulla rete della VMC: "
                "controllarlo in Impostazioni → Sistema → Rete, oppure riavviare Home Assistant per "
                "riprovare il ripristino."
            )
            titolo = "VMC Master: ripristino del Wi-Fi del server non riuscito"
        else:
            testo = (
                f"{messaggio}\n\nThe server Wi-Fi may still be on the unit's network: "
                "check it in Settings → System → Network, or restart Home Assistant to "
                "retry the restore."
            )
            titolo = "VMC Master: server Wi-Fi restore failed"
        persistent_notification.async_create(
            hass, testo, title=titolo, notification_id=f"{DOMAIN}_ripristino_wifi"
        )


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Installa o aggiorna il package della VMC."""
    integrazione = await async_get_integration(hass, DOMAIN)
    config_dir = hass.config.config_dir
    nome: str = entry.data[CONF_NOME]
    ip: str = entry.data[CONF_HOST]

    # voce di nuovo abilitata: l'avviso «voce disabilitata» non serve piu'
    ir.async_delete_issue(hass, DOMAIN, f"{ISSUE_DISABILITATA}_{nome}")

    try:
        ip = await _adotta_ip_della_scheda(hass, entry, config_dir, nome, ip)
        esito = await hass.async_add_executor_job(
            installa, config_dir, nome, ip, str(integrazione.version)
        )
    except OSError as errore:
        # disco pieno o file non scrivibili: i file scritti restano quelli di prima
        if _italiano(hass):
            messaggio = (
                f"File del package della VMC {nome} non scritti ({errore}): i file di prima "
                "sono intatti. Controllare lo spazio libero sul disco, poi riavviare Home Assistant."
            )
        else:
            messaggio = (
                f"Package files of unit {nome} not written ({errore}): the previous files are "
                "intact. Check the free disk space, then restart Home Assistant."
            )
        raise ConfigEntryError(messaggio) from errore
    if esito.backup is not None:
        # la 8.6.0 chiama «Automazione VMC Master» la principale e «Automazione VMC ‹nome›» le clonate
        nome_automazione = "Master" if nome == NOME_MASTER else nome
        if _italiano(hass):
            testo = (
                f"La precedente installazione manuale della VMC {nome} è stata spostata in "
                f"`{esito.backup}`.\n\n"
                "Al suo posto c'è il package dell'integrazione: stessi nomi delle entità, "
                "la cronologia resta.\n\n"
                "Cosa fare:\n"
                "1. Aprire Impostazioni → Automazioni e scenari.\n"
                f"2. Eliminare l'automazione incollata a mano «Automazione VMC {nome_automazione}». "
                "Va fatto PRIMA di riavviare, altrimenti dopo il riavvio girano due automazioni uguali.\n"
                "3. Riavviare Home Assistant.\n"
                "4. Togliere dalla plancia la vecchia scheda manuale.\n"
                "5. Aggiungere dalla plancia la scheda «VMC Master»."
            )
            titolo = f"VMC Master: VMC {nome} passata all'integrazione"
        else:
            testo = (
                f"The previous manual installation of unit {nome} has been moved to "
                f"`{esito.backup}`.\n\n"
                "It has been replaced by the integration package: same entity names, "
                "the history is kept.\n\n"
                "What to do:\n"
                "1. Open Settings → Automations & scenes.\n"
                f"2. Delete the automation pasted by hand «Automazione VMC {nome_automazione}». "
                "Do it BEFORE restarting, otherwise two identical automations run after the restart.\n"
                "3. Restart Home Assistant.\n"
                "4. Remove the old manual card from the dashboard.\n"
                "5. Add the «VMC Master» card from the dashboard."
            )
            titolo = f"VMC Master: unit {nome} moved to the integration"
        persistent_notification.async_create(
            hass, testo, title=titolo, notification_id=f"{DOMAIN}_migrazione_{nome}"
        )
    if esito.backup_modificati is not None:
        elenco = "\n".join(f"- `{nome_file}`" for nome_file in esito.file_modificati)
        copia = f"/config/{esito.backup_modificati.relative_to(config_dir).as_posix()}"
        if _italiano(hass):
            testo = (
                f"Questi file del package della VMC {nome} erano stati modificati a mano:\n\n"
                f"{elenco}\n\n"
                "I file del package sono scritti dall'integrazione e non vanno modificati: "
                f"la versione modificata è stata salvata in `{copia}` e al suo "
                "posto è stata rimessa quella dell'integrazione. Le impostazioni si cambiano "
                "dalla scheda «VMC Master»."
            )
            titolo = f"VMC Master: file della VMC {nome} modificati a mano"
        else:
            testo = (
                f"These package files of unit {nome} had been edited by hand:\n\n"
                f"{elenco}\n\n"
                "The package files are written by the integration and must not be edited: "
                f"the edited version has been saved in `{copia}` and replaced by the "
                "integration's one. Settings are changed from the «VMC Master» card."
            )
            titolo = f"VMC Master: files of unit {nome} edited by hand"
        persistent_notification.async_create(
            hass, testo, title=titolo, notification_id=f"{DOMAIN}_modificati_{nome}"
        )
    if esito.riavvio_necessario:
        _segnala_riavvio(hass)
    else:
        if esito.ricariche:
            # Aggiornamento dell'integrazione: Home Assistant ha gia' letto i package
            # all'avvio, le parti cambiate si ricaricano senza chiedere un altro riavvio
            _ricarica_dopo_avvio(hass, entry, esito.ricariche)
        _controlla_packages_dopo_avvio(hass, entry, nome)

    _aggiorna_titolo_dopo_avvio(hass, entry)
    # IP con cui e' stato installato il package: la voce si ricarica solo se cambia
    entry.runtime_data = ip
    entry.async_on_unload(entry.add_update_listener(_async_aggiornata))
    _installa_filtro_tcp(hass)
    return True


async def _adotta_ip_della_scheda(
    hass: HomeAssistant, entry: ConfigEntry, config_dir: str, nome: str, ip: str
) -> str:
    """IP cambiato dal campo «Cambia IP VMC» della scheda: vale quello del package, solo se
    e' valido e non e' gia' di un'altra VMC. Restituisce l'IP con cui installare.

    Home Assistant avvia insieme le voci dello stesso dominio: controllo e aggiornamento
    della voce stanno in un'unica sezione protetta, cosi' due VMC non prendono lo stesso IP."""
    async with hass.data.setdefault(DATI_BLOCCO_IP, asyncio.Lock()):
        marcatore = await hass.async_add_executor_job(leggi_marcatore, config_dir, nome)
        ip_file = await hass.async_add_executor_job(ip_nel_package, config_dir, nome)
        if not (marcatore and ip == marcatore.get("ip") and ip_file and ip_file != ip):
            return ip
        altra = next(
            (
                voce.data.get(CONF_NOME)
                for voce in hass.config_entries.async_entries(DOMAIN)
                if voce.entry_id != entry.entry_id and voce.data.get(CONF_HOST) == ip_file
            ),
            None,
        )
        if config_flow.ip_valido(ip_file) and altra is None:
            await hass.async_add_executor_job(
                prima_installazione.aggiorna_ip, config_dir, ip, ip_file
            )
            hass.config_entries.async_update_entry(entry, data={**entry.data, CONF_HOST: ip_file})
            return ip_file
        # si rimette l'IP di prima: i file tornano quelli scritti dall'integrazione
        await hass.async_add_executor_job(_rimetti_ip_nel_package, config_dir, nome, ip_file, ip)
        _segnala_ip_scheda_rifiutato(hass, nome, ip, ip_file, altra)
        _segnala_riavvio(hass)  # Home Assistant ha gia' caricato il package con l'IP rifiutato
        return ip


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Niente da scaricare: il package resta caricato fino al prossimo riavvio.

    Una voce disabilitata non ferma il package (resta in /config/packages e si carica a ogni
    avvio) e non lo aggiorna piu': lo dice un avviso, la scheda non viene piu' servita."""
    if not any(
        voce.state is ConfigEntryState.LOADED
        for voce in hass.config_entries.async_entries(DOMAIN)
        if voce.entry_id != entry.entry_id
    ):
        _togli_filtro_tcp(hass)  # ultima VMC scaricata
    else:
        _aggiorna_ip_filtro_tcp(hass)
    if entry.disabled_by is not None:
        nome = entry.data[CONF_NOME]
        ir.async_create_issue(
            hass,
            DOMAIN,
            f"{ISSUE_DISABILITATA}_{nome}",
            is_fixable=False,
            is_persistent=True,
            severity=ir.IssueSeverity.WARNING,
            translation_key=ISSUE_DISABILITATA,
            translation_placeholders={"nome": nome, "titolo": entry.title},
        )
    return True


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """VMC eliminata: la sua cartella va in /config/vmc_master_backup e serve un riavvio.

    Le entita' del package della VMC escono subito dal registro (la cartella e' gia' nel
    backup, quindi al riavvio non tornano), anche quando e' l'ultima VMC e l'integrazione
    non si avviera' piu'. Si tolgono solo quelle del package (unique_id letti dai file
    spostati nel backup): le entita' create dall'utente restano, anche se si chiamano
    «vmc_‹nome›_…». Se qualcuna resta, il nome si ricorda e si toglie al riavvio."""
    nome = entry.data[CONF_NOME]
    destinazione = await hass.async_add_executor_job(
        sposta_in_backup, hass.config.config_dir, nome
    )
    ir.async_delete_issue(hass, DOMAIN, f"{ISSUE_PACKAGES}_{nome}")
    ir.async_delete_issue(hass, DOMAIN, f"{ISSUE_DISABILITATA}_{nome}")
    id_package = None
    if destinazione is not None:
        _segnala_riavvio(hass)
        id_package = await hass.async_add_executor_job(_id_del_package, destinazione)
    if id_package is None:
        # cartella assente o file non leggibili: gli id del package scritto dall'integrazione
        id_package = await hass.async_add_executor_job(_id_del_package_generato, nome)
    if id_package is not None and _togli_entita_della_vmc(
        hass, nome, id_package, anche_fornite=destinazione is not None
    ):
        return
    async with _blocco_eliminate(hass):
        store = _store_eliminate(hass)
        dati = await store.async_load() or {}
        nomi = [n for n in dati.get("nomi", []) if isinstance(n, str)]
        if nome not in nomi:
            await store.async_save({"nomi": [*nomi, nome]})


def _store_eliminate(hass: HomeAssistant) -> Store[dict[str, Any]]:
    if DATI_ELIMINATE not in hass.data:
        hass.data[DATI_ELIMINATE] = Store(hass, 1, CHIAVE_ELIMINATE)
    return hass.data[DATI_ELIMINATE]


def _blocco_eliminate(hass: HomeAssistant) -> asyncio.Lock:
    """Un solo accesso alla volta all'elenco delle VMC eliminate (due VMC eliminate insieme)."""
    return hass.data.setdefault(DATI_BLOCCO_ELIMINATE, asyncio.Lock())


async def _togli_entita_vmc_eliminate(hass: HomeAssistant) -> None:
    """Dopo il riavvio che segue «Elimina la VMC» si tolgono dal registro le entita'
    del package della VMC eliminata non piu' fornite, solo se nessuna VMC con quel nome
    e' stata aggiunta di nuovo. Il nome si dimentica quando non resta piu' niente da togliere."""
    async with _blocco_eliminate(hass):
        store = _store_eliminate(hass)
        dati = await store.async_load() or {}
        nomi = [n for n in dati.get("nomi", []) if isinstance(n, str) and NOME_RE.fullmatch(n)]
        if not nomi:
            return
        presenti = {voce.data.get(CONF_NOME) for voce in hass.config_entries.async_entries(DOMAIN)}
        rimasti: list[str] = []
        for nome in nomi:
            if nome in presenti:
                continue  # aggiunta di nuovo: le entita' sono di nuovo sue
            if await hass.async_add_executor_job(cartella_vmc(hass.config.config_dir, nome).is_dir):
                rimasti.append(nome)  # cartella del package di nuovo presente: non si tocca niente
                continue
            id_package = await hass.async_add_executor_job(_id_del_package_generato, nome)
            if id_package is None or not _togli_entita_della_vmc(hass, nome, id_package):
                rimasti.append(nome)  # entita' ancora fornite (nessun riavvio dopo l'eliminazione)
        if rimasti != dati.get("nomi"):
            await store.async_save({"nomi": rimasti})


def _come_lista(valore: object) -> list:
    return valore if isinstance(valore, list) else [valore]


def _id_della_configurazione(configurazione: object, id_package: set[tuple[str, str, str]]) -> None:
    """Aggiunge gli id delle entita' di un file YAML come (dominio, piattaforma, unique_id),
    come li salva il registro delle entita' (anche per le entita' rinominate dall'utente)."""
    if not isinstance(configurazione, dict):
        return
    for dominio, valore in configurazione.items():
        if dominio == "automation":
            for automazione in _come_lista(valore):
                if isinstance(automazione, dict) and automazione.get("id") is not None:
                    id_package.add(("automation", "automation", str(automazione["id"])))
        elif dominio in DOMINI_CON_CHIAVE:
            if isinstance(valore, dict):
                id_package.update((dominio, dominio, str(chiave)) for chiave in valore)
        elif dominio in INTEGRAZIONI_A_BLOCCHI:
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
                if isinstance(voce, dict) and voce.get("platform") and voce.get("unique_id") is not None:
                    id_package.add((dominio, str(voce["platform"]), str(voce["unique_id"])))


def _id_del_package(cartella: Path) -> set[tuple[str, str, str]] | None:
    """Id delle entita' dei file YAML di un package (cartella appena spostata nel backup).
    None se non ci sono file YAML o non si possono leggere."""
    id_package: set[tuple[str, str, str]] = set()
    try:
        file_yaml = sorted(percorso for percorso in cartella.glob("*.yaml") if percorso.is_file())
        if not file_yaml:
            return None
        for percorso in file_yaml:
            with open(percorso, encoding="utf-8") as file:
                _id_della_configurazione(yaml.load(file, Loader=_CaricatoreYaml), id_package)
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as errore:
        _LOGGER.warning("File del package in %s non leggibili: %s", cartella, errore)
        return None
    return id_package


def _id_del_package_generato(nome: str) -> set[tuple[str, str, str]] | None:
    """Id delle entita' del package che l'integrazione scrive per la VMC (gli unique_id
    non dipendono dall'IP). None se i file dell'integrazione non si possono leggere."""
    id_package: set[tuple[str, str, str]] = set()
    try:
        for nome_file, testo in genera_file(nome, "0.0.0.0", "0").items():
            if nome_file.endswith(".yaml"):
                _id_della_configurazione(yaml.load(testo, Loader=_CaricatoreYaml), id_package)
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as errore:
        _LOGGER.warning("Package della VMC %s non leggibile: %s", nome, errore)
        return None
    return id_package


@callback
def _togli_entita_della_vmc(
    hass: HomeAssistant,
    nome: str,
    id_package: set[tuple[str, str, str]],
    anche_fornite: bool = False,
) -> bool:
    """Toglie dal registro le entita' del package della VMC non piu' fornite, o tutte con
    anche_fornite (VMC appena eliminata, cartella gia' nel backup). False se qualcuna resta.

    Si confrontano dominio, piattaforma e unique_id con gli id del package: non si tocca
    niente creato dall'utente (automazioni, aiutanti, sensori YAML), anche se il suo
    entity_id comincia con «vmc_‹nome›_», e si trovano anche le entita' rinominate."""
    registro = er.async_get(hass)
    da_togliere = [
        voce.entity_id
        for voce in list(registro.entities.values())
        if voce.config_entry_id is None  # entita' dei package YAML
        and (voce.domain, voce.platform, voce.unique_id) in id_package
    ]
    tutte = True
    for entity_id in da_togliere:
        stato = hass.states.get(entity_id)
        if anche_fornite or stato is None or stato.attributes.get("restored"):
            registro.async_remove(entity_id)
        else:
            tutte = False
    if da_togliere:
        _LOGGER.info("VMC %s eliminata: entita' del package tolte dal registro se non piu' fornite", nome)
    return tutte


def _rimetti_ip_nel_package(config_dir: str, nome: str, ip_scheda: str, ip: str) -> None:
    """IP della scheda rifiutato: nei file cambiati dallo script «Cambia IP VMC» torna l'IP
    di prima, cosi' i file sono di nuovo quelli scritti dall'integrazione."""
    cartella = cartella_vmc(config_dir, nome)
    for nome_file in (f"vmc_{nome}.yaml", f"vmc_{nome}_script_cambio_nome.sh"):
        percorso = cartella / nome_file
        if not percorso.is_file():
            continue
        testo = _leggi(percorso)
        nuovo = _rimetti_ip(testo, ip_scheda, ip)
        if nuovo != testo:
            _scrivi(percorso, nuovo)  # scrittura atomica, stessi fine riga e permessi


@callback
def _segnala_ip_scheda_rifiutato(
    hass: HomeAssistant, nome: str, ip: str, ip_scheda: str, altra: str | None
) -> None:
    """Notifica: l'IP scritto nel campo «Cambia IP VMC» della scheda non si usa."""
    if _italiano(hass):
        motivo = (
            f"è già usato dalla VMC {altra}"
            if altra is not None
            else (
                "non è valido: servono quattro numeri da 0 a 255, senza zeri iniziali. "
                "Non sono ammessi 0.x.x.x, 127.x.x.x, 169.254.x.x e gli indirizzi da 224.0.0.0 in su"
            )
        )
        testo = (
            f"L'IP {ip_scheda} scritto dalla scheda {motivo}.\n\n"
            f"La VMC {nome} resta sull'IP {ip}.\n\n"
            "Per cambiarlo:\n"
            "1. Aprire Impostazioni → Dispositivi e servizi → VMC Master.\n"
            f"2. Premere l'icona ingranaggio sulla riga della VMC {nome}.\n"
            "3. Scegliere «Cambia l'IP della VMC»."
        )
        titolo = f"VMC Master: IP della VMC {nome} non cambiato"
    else:
        motivo = (
            f"is already used by unit {altra}"
            if altra is not None
            else (
                "is not valid: four numbers from 0 to 255 are needed, without leading zeros. "
                "0.x.x.x, 127.x.x.x, 169.254.x.x and the addresses from 224.0.0.0 up are not allowed"
            )
        )
        testo = (
            f"The IP {ip_scheda} written from the card {motivo}.\n\n"
            f"Unit {nome} keeps the IP {ip}.\n\n"
            "To change it:\n"
            "1. Open Settings → Devices & services → VMC Master.\n"
            f"2. Press the gear icon on the row of unit {nome}.\n"
            "3. Choose «Change the unit's IP»."
        )
        titolo = f"VMC Master: IP of unit {nome} not changed"
    persistent_notification.async_create(
        hass, testo, title=titolo, notification_id=f"{DOMAIN}_ip_scheda_{nome}"
    )


class _FiltroTcpVmc(logging.Filter):
    """Con una VMC spenta i suoi sensori TCP scrivono un errore «Unable to connect to ‹IP›
    on port 5001» a ogni lettura (migliaia al giorno). Per gli IP delle VMC passa al massimo
    un messaggio ogni 30 minuti per IP; i messaggi degli altri dispositivi passano tutti.
    Gli intervalli di lettura dei sensori non cambiano."""

    def __init__(self) -> None:
        super().__init__()
        self.ips: frozenset[str] = frozenset()
        self._ultimo: dict[str, float] = {}
        self._blocco = threading.Lock()
        self._ora = time.monotonic

    def filter(self, record: logging.LogRecord) -> bool:
        ips = self.ips
        if not ips:
            return True
        try:
            messaggio = record.getMessage()
        except Exception:  # noqa: BLE001 - messaggio non formattabile: passa com'e'
            return True
        ip = next((t for t in _RE_IP_NEL_LOG.findall(messaggio) if t in ips), None)
        if ip is None:
            return True
        ora = self._ora()
        with self._blocco:
            ultimo = self._ultimo.get(ip)
            if ultimo is not None and ora - ultimo < INTERVALLO_LOG_TCP:
                return False
            self._ultimo[ip] = ora
        return True


@callback
def _installa_filtro_tcp(hass: HomeAssistant) -> None:
    filtro = hass.data.get(DATI_FILTRO_TCP)
    if filtro is None:
        filtro = hass.data[DATI_FILTRO_TCP] = _FiltroTcpVmc()
        logging.getLogger(LOGGER_TCP).addFilter(filtro)
    _aggiorna_ip_filtro_tcp(hass)


@callback
def _aggiorna_ip_filtro_tcp(hass: HomeAssistant) -> None:
    """IP di tutte le VMC configurate (anche disabilitate: il loro package resta attivo)."""
    filtro: _FiltroTcpVmc | None = hass.data.get(DATI_FILTRO_TCP)
    if filtro is not None:
        filtro.ips = frozenset(
            voce.data[CONF_HOST]
            for voce in hass.config_entries.async_entries(DOMAIN)
            if voce.data.get(CONF_HOST)
        )


@callback
def _togli_filtro_tcp(hass: HomeAssistant) -> None:
    filtro = hass.data.pop(DATI_FILTRO_TCP, None)
    if filtro is not None:
        logging.getLogger(LOGGER_TCP).removeFilter(filtro)


async def _async_aggiornata(hass: HomeAssistant, entry: ConfigEntry) -> None:
    # IP cambiato dall'ingranaggio: si aggiorna il package. Il solo titolo non serve.
    _aggiorna_ip_filtro_tcp(hass)
    if entry.data[CONF_HOST] != entry.runtime_data:
        await hass.config_entries.async_reload(entry.entry_id)


@callback
def _aggiorna_titolo_dopo_avvio(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Titolo della voce = nome della VMC (quello dell'App Air Guard), anche per le VMC
    aggiunte prima della 9.0.0b13 («VMC ‹nome›»). Se l'utente ha rinominato la voce,
    il suo nome resta. Il nome interno (cartella, entita', scheda) non cambia."""

    async def _aggiorna() -> None:
        nome = entry.data[CONF_NOME]
        if entry.title not in {f"VMC {nome}", entry.data.get(CONF_TITOLO)}:
            return
        try:
            nome_vmc = await config_flow.async_nome_vmc(entry.data[CONF_HOST])
        except Exception:  # noqa: BLE001 - VMC spenta o rete assente: resta il titolo
            return
        if not nome_vmc:
            return
        titolo = config_flow.titolo_voce(nome_vmc, nome)
        if titolo != entry.title or entry.data.get(CONF_TITOLO) != titolo:
            hass.config_entries.async_update_entry(
                entry, title=titolo, data={**entry.data, CONF_TITOLO: titolo}
            )

    @callback
    def _avvia(_hass: HomeAssistant) -> None:
        entry.async_create_background_task(hass, _aggiorna(), f"{DOMAIN}_titolo_{entry.entry_id}")

    entry.async_on_unload(async_at_started(hass, _avvia))


@callback
def _segnala_riavvio(hass: HomeAssistant) -> None:
    ir.async_create_issue(
        hass,
        DOMAIN,
        ISSUE_RIAVVIO,
        is_fixable=True,
        is_persistent=False,
        severity=ir.IssueSeverity.WARNING,
        translation_key=ISSUE_RIAVVIO,
    )


@callback
def _ricarica_dopo_avvio(hass: HomeAssistant, entry: ConfigEntry, servizi: set[str]) -> None:
    """Ricarica le parti cambiate del package appena Home Assistant e' avviato.

    Con piu' VMC le ricariche si fanno una volta sola per tutte."""
    in_attesa: set[str] = hass.data.setdefault(DATI_RICARICHE, set())
    in_attesa.update(servizi)

    @callback
    def _avviato(_hass: HomeAssistant) -> None:
        if not in_attesa:
            return  # gia' fatte insieme a un'altra VMC
        da_fare = sorted(in_attesa, key=ORDINE_RICARICHE.index)
        in_attesa.clear()
        hass.async_create_task(_async_ricarica(hass, da_fare))

    entry.async_on_unload(async_at_started(hass, _avviato))


async def _async_ricarica(hass: HomeAssistant, servizi: list[str]) -> None:
    for servizio in servizi:
        dominio, nome_servizio = servizio.split(".")
        try:
            await hass.services.async_call(dominio, nome_servizio, blocking=True)
        except Exception:  # noqa: BLE001 - qualunque errore: si torna al riavvio
            _LOGGER.exception("Ricarica %s non riuscita: serve un riavvio", servizio)
            _segnala_riavvio(hass)
            return
    _LOGGER.info("Package delle VMC aggiornato senza riavvio: %s", ", ".join(servizi))


@callback
def _controlla_packages_dopo_avvio(hass: HomeAssistant, entry: ConfigEntry, nome: str) -> None:
    """File gia' installati ma entita' assenti: i package non sono abilitati."""

    @callback
    def _controlla(_hass: HomeAssistant) -> None:
        # un avviso per ogni VMC: una VMC caricata non cancella l'avviso di un'altra
        ir.async_delete_issue(hass, DOMAIN, ISSUE_PACKAGES)  # avviso unico fino alla 9.0.0b18
        if hass.states.get(f"sensor.vmc_{nome}_status_ip") is None:
            ir.async_create_issue(
                hass,
                DOMAIN,
                f"{ISSUE_PACKAGES}_{nome}",
                is_fixable=False,
                is_persistent=False,
                severity=ir.IssueSeverity.ERROR,
                translation_key=ISSUE_PACKAGES,
                translation_placeholders={"nome": nome},
                learn_more_url="https://www.home-assistant.io/docs/configuration/packages/",
            )
        else:
            ir.async_delete_issue(hass, DOMAIN, f"{ISSUE_PACKAGES}_{nome}")
            if nome == NOME_MASTER:
                _togli_entita_non_piu_fornite(hass)

    entry.async_on_unload(async_at_started(hass, _controlla))


@callback
def _togli_entita_non_piu_fornite(hass: HomeAssistant) -> None:
    """Dopo la migrazione della Master 8.6.0 (o l'aggiornamento dell'integrazione) le
    entita' della Finestra Clona e della Finestra Prima Installazione VMC non sono piu'
    fornite: si tolgono dal registro, solo se nessuno le fornisce."""
    registro = er.async_get(hass)
    for entity_id in (*ENTITA_FINESTRA_CLONA, *ENTITA_PRIMA_INSTALLAZIONE):
        if registro.async_get(entity_id) is None:
            continue
        stato = hass.states.get(entity_id)
        if stato is None or stato.attributes.get("restored"):
            registro.async_remove(entity_id)


@lru_cache(maxsize=1)
def _leggi_scheda_master() -> str:
    # newline="" mantiene i CRLF del file, come gli script della release 8.6.0
    with open(_CARTELLA / "package" / FILE_SCHEDA, encoding="utf-8", newline="") as file:
        return file.read()


@lru_cache(maxsize=16)
def _configurazione_scheda(nome: str, ip: str) -> dict[str, Any]:
    return yaml.safe_load(adatta_link_repository(per_vmc(_leggi_scheda_master(), nome, ip)))


class VmcSchedaView(HomeAssistantView):
    """Restituisce la configurazione della scheda per una VMC (solo utenti autenticati)."""

    url = "/api/vmc_master/scheda/{entry_id}"
    name = "api:vmc_master:scheda"
    requires_auth = True

    async def get(self, request: web.Request, entry_id: str) -> web.Response:
        hass = request.app[KEY_HASS]
        voce = hass.config_entries.async_get_entry(entry_id)
        if voce is None or voce.domain != DOMAIN:
            return self.json_message("VMC non trovata", HTTPStatus.NOT_FOUND)
        if voce.disabled_by is not None:
            # il package della voce disabilitata non si aggiorna piu': la scheda della
            # versione installata potrebbe non corrispondere
            return self.json_message("VMC disabilitata", HTTPStatus.CONFLICT)
        configurazione = await hass.async_add_executor_job(
            _configurazione_scheda, voce.data[CONF_NOME], voce.data[CONF_HOST]
        )
        return self.json(configurazione)
