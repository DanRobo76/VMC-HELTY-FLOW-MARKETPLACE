"""Integrazione VMC Master per VMC Helty Flow Plus/Elite.

Ogni voce di configurazione e' una VMC (nome + IP). Per ogni VMC l'integrazione
installa e aggiorna il package della release 8.6.0 in packages/vmc_helty_flow/<nome>
e serve la scheda «VMC Master», che si aggiunge dalla plancia senza incollare codice.
"""

from __future__ import annotations

import logging
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
from homeassistant.helpers.typing import ConfigType
from homeassistant.loader import async_get_integration

from .const import (
    CONF_HOST,
    CONF_NOME,
    DOMAIN,
    ENTITA_FINESTRA_CLONA,
    FILE_SCHEDA,
    FILE_SCHEDA_JS,
    NOME_MASTER,
    URL_FRONTEND,
)
from .installatore import installa, ip_nel_package, leggi_marcatore, sposta_in_backup
from .trasforma import per_vmc

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

_CARTELLA = Path(__file__).parent

ISSUE_RIAVVIO = "riavvio_necessario"
ISSUE_PACKAGES = "packages_non_abilitati"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Registra la scheda «VMC Master»: file JavaScript e configurazione per ogni VMC."""
    integrazione = await async_get_integration(hass, DOMAIN)
    await hass.http.async_register_static_paths(
        [StaticPathConfig(URL_FRONTEND, str(_CARTELLA / "frontend"), False)]
    )
    # Il numero di versione nell'indirizzo fa ricaricare la scheda dopo ogni aggiornamento
    add_extra_js_url(hass, f"{URL_FRONTEND}/{FILE_SCHEDA_JS}?v={integrazione.version}")
    hass.http.register_view(VmcSchedaView())
    return True


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
        ip = ip_file
        hass.config_entries.async_update_entry(entry, data={**entry.data, CONF_HOST: ip})

    esito = await hass.async_add_executor_job(
        installa, config_dir, nome, ip, str(integrazione.version)
    )
    if esito.backup is not None:
        # la 8.6.0 chiama «Automazione VMC Master» la principale e «Automazione VMC ‹nome›» le clonate
        nome_automazione = "Master" if nome == NOME_MASTER else nome
        persistent_notification.async_create(
            hass,
            (
                f"La precedente installazione manuale della VMC {nome} e' stata spostata in "
                f"`{esito.backup}` e sostituita dal package dell'integrazione (stessi nomi delle "
                "entita', la cronologia resta).\n\n"
                f"PRIMA di riavviare eliminare l'automazione incollata a mano «Automazione VMC {nome_automazione}» "
                "(Impostazioni → Automazioni e scenari), altrimenti dopo il riavvio girano due "
                "automazioni uguali. Poi riavviare, togliere la vecchia scheda manuale e aggiungere "
                "la scheda «VMC Master» dalla plancia."
            ),
            title=f"VMC Master: VMC {nome} passata all'integrazione",
            notification_id=f"{DOMAIN}_migrazione_{nome}",
        )
    if esito.riavvio_necessario:
        _segnala_riavvio(hass)
    else:
        _controlla_packages_dopo_avvio(hass, entry, nome)

    entry.async_on_unload(entry.add_update_listener(_async_aggiornata))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Niente da scaricare: il package resta caricato fino al prossimo riavvio."""
    return True


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """VMC eliminata: la sua cartella va in /config/vmc_master_backup e serve un riavvio."""
    nome = entry.data[CONF_NOME]
    destinazione = await hass.async_add_executor_job(
        sposta_in_backup, hass.config.config_dir, nome
    )
    if destinazione is not None:
        _segnala_riavvio(hass)


async def _async_aggiornata(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


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
def _controlla_packages_dopo_avvio(hass: HomeAssistant, entry: ConfigEntry, nome: str) -> None:
    """File gia' installati ma entita' assenti: i package non sono abilitati."""

    @callback
    def _controlla(_hass: HomeAssistant) -> None:
        if hass.states.get(f"sensor.vmc_{nome}_status_ip") is None:
            ir.async_create_issue(
                hass,
                DOMAIN,
                ISSUE_PACKAGES,
                is_fixable=False,
                is_persistent=False,
                severity=ir.IssueSeverity.ERROR,
                translation_key=ISSUE_PACKAGES,
                learn_more_url="https://www.home-assistant.io/docs/configuration/packages/",
            )
        else:
            ir.async_delete_issue(hass, DOMAIN, ISSUE_PACKAGES)
            if nome == NOME_MASTER:
                _togli_entita_finestra_clona(hass)

    entry.async_on_unload(async_at_started(hass, _controlla))


@callback
def _togli_entita_finestra_clona(hass: HomeAssistant) -> None:
    """Dopo la migrazione della Master 8.6.0 le entita' della Finestra Clona non sono piu'
    fornite: si tolgono dal registro, solo se nessuno le fornisce."""
    registro = er.async_get(hass)
    for entity_id in ENTITA_FINESTRA_CLONA:
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
    return yaml.safe_load(per_vmc(_leggi_scheda_master(), nome, ip))


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
