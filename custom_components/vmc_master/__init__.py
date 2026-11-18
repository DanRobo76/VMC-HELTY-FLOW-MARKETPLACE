"""Integrazione VMC Master per VMC Helty Flow Plus/Elite.

Ogni voce di configurazione e' una VMC (nome + IP). Per ogni VMC l'integrazione
installa e aggiorna il package della release 8.6.0 in packages/vmc_helty_flow/<nome>
e serve la scheda «VMC Master», che si aggiunge dalla plancia senza incollare codice.
"""

from __future__ import annotations

import logging
import re
from functools import lru_cache
from http import HTTPStatus
from pathlib import Path
from typing import Any

import yaml
from aiohttp import web

from homeassistant.components import persistent_notification
from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import HomeAssistantView, StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
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
    cartella_vmc,
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
DATI_RICARICHE = f"{DOMAIN}_ricariche"
# Nomi delle VMC eliminate: al prossimo avvio si tolgono dal registro le loro entita'
CHIAVE_ELIMINATE = f"{DOMAIN}.vmc_eliminate"
DATI_ELIMINATE = f"{DOMAIN}_eliminate"

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
    return True


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
        if _italiano(hass):
            testo = (
                f"{errore.message}\n\nIl Wi-Fi del server potrebbe essere ancora sulla rete della VMC: "
                "controllarlo in Impostazioni → Sistema → Rete, oppure riavviare Home Assistant per "
                "riprovare il ripristino."
            )
            titolo = "VMC Master: ripristino del Wi-Fi del server non riuscito"
        else:
            testo = (
                f"{errore.message}\n\nThe server Wi-Fi may still be on the unit's network: "
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

    marcatore = await hass.async_add_executor_job(leggi_marcatore, config_dir, nome)
    ip_file = await hass.async_add_executor_job(ip_nel_package, config_dir, nome)
    if marcatore and ip == marcatore.get("ip") and ip_file and ip_file != ip:
        # IP cambiato dal campo «Cambia IP VMC» della scheda: vale quello del package
        await hass.async_add_executor_job(
            prima_installazione.aggiorna_ip, config_dir, ip, ip_file
        )
        ip = ip_file
        hass.config_entries.async_update_entry(entry, data={**entry.data, CONF_HOST: ip})

    esito = await hass.async_add_executor_job(
        installa, config_dir, nome, ip, str(integrazione.version)
    )
    if esito.backup is not None:
        # la 8.6.0 chiama «Automazione VMC Master» la principale e «Automazione VMC ‹nome›» le clonate
        nome_automazione = "Master" if nome == NOME_MASTER else nome
        if _italiano(hass):
            testo = (
                f"La precedente installazione manuale della VMC {nome} è stata spostata in "
                f"`{esito.backup}` e sostituita dal package dell'integrazione (stessi nomi delle "
                "entità, la cronologia resta).\n\n"
                f"PRIMA di riavviare eliminare l'automazione incollata a mano «Automazione VMC {nome_automazione}» "
                "(Impostazioni → Automazioni e scenari), altrimenti dopo il riavvio girano due "
                "automazioni uguali. Poi riavviare, togliere la vecchia scheda manuale e aggiungere "
                "la scheda «VMC Master» dalla plancia."
            )
            titolo = f"VMC Master: VMC {nome} passata all'integrazione"
        else:
            testo = (
                f"The previous manual installation of unit {nome} has been moved to "
                f"`{esito.backup}` and replaced by the integration package (same entity "
                "names, the history is kept).\n\n"
                f"BEFORE restarting, delete the automation pasted by hand «Automazione VMC {nome_automazione}» "
                "(Settings → Automations & scenes), otherwise two identical automations run "
                "after the restart. Then restart, remove the old manual card and add the "
                "«VMC Master» card from the dashboard."
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
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Niente da scaricare: il package resta caricato fino al prossimo riavvio."""
    return True


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """VMC eliminata: la sua cartella va in /config/vmc_master_backup e serve un riavvio.

    Le entita' della VMC escono subito dal registro (la cartella e' gia' nel backup,
    quindi al riavvio non tornano), anche quando e' l'ultima VMC e l'integrazione non
    si avviera' piu'. Se qualcuna resta, il nome si ricorda e si toglie al riavvio."""
    nome = entry.data[CONF_NOME]
    destinazione = await hass.async_add_executor_job(
        sposta_in_backup, hass.config.config_dir, nome
    )
    ir.async_delete_issue(hass, DOMAIN, f"{ISSUE_PACKAGES}_{nome}")
    if destinazione is not None:
        _segnala_riavvio(hass)
    if _togli_entita_della_vmc(hass, nome, anche_fornite=destinazione is not None):
        return
    store = _store_eliminate(hass)
    dati = await store.async_load() or {}
    nomi = [n for n in dati.get("nomi", []) if isinstance(n, str)]
    if nome not in nomi:
        await store.async_save({"nomi": [*nomi, nome]})


def _store_eliminate(hass: HomeAssistant) -> Store[dict[str, Any]]:
    if DATI_ELIMINATE not in hass.data:
        hass.data[DATI_ELIMINATE] = Store(hass, 1, CHIAVE_ELIMINATE)
    return hass.data[DATI_ELIMINATE]


async def _togli_entita_vmc_eliminate(hass: HomeAssistant) -> None:
    """Dopo il riavvio che segue «Elimina la VMC» si tolgono dal registro le entita'
    della VMC eliminata non piu' fornite, solo se nessuna VMC con quel nome e' stata
    aggiunta di nuovo. Il nome si dimentica quando non resta piu' niente da togliere."""
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
        if not _togli_entita_della_vmc(hass, nome):
            rimasti.append(nome)  # entita' ancora fornite (nessun riavvio dopo l'eliminazione)
    if rimasti != dati.get("nomi"):
        await store.async_save({"nomi": rimasti})


@callback
def _togli_entita_della_vmc(
    hass: HomeAssistant, nome: str, anche_fornite: bool = False
) -> bool:
    """Toglie dal registro le entita' del package della VMC (‹dominio›.vmc_‹nome›_… e
    l'automazione principale) non piu' fornite, o tutte con anche_fornite (VMC appena
    eliminata, cartella gia' nel backup). False se qualcuna resta.
    Il nome ha solo lettere, quindi «vmc_‹nome›_» non comprende altre VMC."""
    registro = er.async_get(hass)
    modello = re.compile(rf"^[a-z_]+\.vmc_{nome}_")
    automazione = f"automazione_vmc_{nome}"
    da_togliere = [
        voce.entity_id
        for voce in registro.entities.values()
        if voce.config_entry_id is None  # entita' dei package YAML
        and (
            modello.match(voce.entity_id)
            or voce.entity_id == f"automation.{automazione}"
            or (voce.domain == "automation" and voce.unique_id == automazione)
        )
    ]
    tutte = True
    for entity_id in da_togliere:
        stato = hass.states.get(entity_id)
        if anche_fornite or stato is None or stato.attributes.get("restored"):
            registro.async_remove(entity_id)
        else:
            tutte = False
    if da_togliere:
        _LOGGER.info("VMC %s eliminata: entita' tolte dal registro se non piu' fornite", nome)
    return tutte


async def _async_aggiornata(hass: HomeAssistant, entry: ConfigEntry) -> None:
    # IP cambiato dall'ingranaggio: si aggiorna il package. Il solo titolo non serve.
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
        configurazione = await hass.async_add_executor_job(
            _configurazione_scheda, voce.data[CONF_NOME], voce.data[CONF_HOST]
        )
        return self.json(configurazione)
