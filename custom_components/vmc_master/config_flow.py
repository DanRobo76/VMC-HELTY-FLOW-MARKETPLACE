"""Configurazione da interfaccia: una voce per ogni VMC (nome + IP)."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.core import callback

from .const import (
    CONF_HOST,
    CONF_NOME,
    DOMAIN,
    IP_RE,
    NOME_MASTER,
    NOME_RE,
    PORTA_VMC,
    TIMEOUT_VMC,
)
from .installatore import installazione_manuale, ip_nel_package

_LOGGER = logging.getLogger(__name__)


def ip_valido(ip: str) -> bool:
    """IPv4 con quattro numeri da 0 a 255 (999.999.999.999 non e' valido)."""
    return bool(IP_RE.fullmatch(ip)) and all(0 <= int(p) <= 255 for p in ip.split("."))


async def async_prova_vmc(ip: str) -> bool:
    """Chiede il nome alla VMC (comando VMNM?) sulla porta 5001: True se risponde."""
    try:
        lettore, scrittore = await asyncio.wait_for(
            asyncio.open_connection(ip, PORTA_VMC), TIMEOUT_VMC
        )
    except (OSError, TimeoutError):
        return False
    try:
        scrittore.write(b"VMNM?")
        await scrittore.drain()
        risposta = await asyncio.wait_for(lettore.read(256), TIMEOUT_VMC)
    except (OSError, TimeoutError):
        return False
    finally:
        scrittore.close()
    _LOGGER.debug("Risposta della VMC %s: %s", ip, risposta)
    return bool(risposta)


class VmcMasterConfigFlow(ConfigFlow, domain=DOMAIN):
    """Aggiunge una VMC."""

    VERSION = 1

    def __init__(self) -> None:
        self._dati: dict[str, str] = {}

    def _nomi_e_ip_in_uso(self, escludi: str | None = None) -> tuple[set[str], set[str]]:
        nomi: set[str] = set()
        ips: set[str] = set()
        for voce in self._async_current_entries(include_ignore=False):
            if voce.entry_id == escludi:
                continue
            nomi.add(voce.data[CONF_NOME])
            ips.add(voce.data[CONF_HOST])
        return nomi, ips

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        errori: dict[str, str] = {}
        nomi, ips = self._nomi_e_ip_in_uso()
        if user_input is not None:
            nome = user_input[CONF_NOME].strip()
            ip = user_input[CONF_HOST].strip()
            if not NOME_RE.fullmatch(nome):
                errori[CONF_NOME] = "nome_non_valido"
            elif nome in nomi:
                errori[CONF_NOME] = "nome_in_uso"
            if not ip_valido(ip):
                errori[CONF_HOST] = "ip_non_valido"
            elif ip in ips:
                errori[CONF_HOST] = "ip_in_uso"
            if not errori:
                await self.async_set_unique_id(nome)
                self._abort_if_unique_id_configured()
                self._dati = {CONF_NOME: nome, CONF_HOST: ip}
                if await self.hass.async_add_executor_job(
                    installazione_manuale, self.hass.config.config_dir, nome
                ):
                    return await self.async_step_migra()
                if await async_prova_vmc(ip):
                    return self._crea_voce()
                return await self.async_step_non_raggiungibile()

        predefinito = NOME_MASTER if NOME_MASTER not in nomi else ""
        ip_predefinito = ""
        if predefinito and await self.hass.async_add_executor_job(
            installazione_manuale, self.hass.config.config_dir, predefinito
        ):
            # Installazione manuale della release 8.6.0: propone l'IP gia' impostato
            ip_trovato = await self.hass.async_add_executor_job(
                ip_nel_package, self.hass.config.config_dir, predefinito
            )
            if ip_trovato and ip_valido(ip_trovato):
                ip_predefinito = ip_trovato
        schema = vol.Schema(
            {
                vol.Required(
                    CONF_NOME, default=(user_input or {}).get(CONF_NOME, predefinito)
                ): str,
                vol.Required(
                    CONF_HOST, default=(user_input or {}).get(CONF_HOST, ip_predefinito)
                ): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errori)

    async def async_step_migra(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Trovata un'installazione manuale: la cartella va in backup e la sostituisce l'integrazione."""
        if user_input is not None:
            return self._crea_voce()
        return self.async_show_form(
            step_id="migra",
            description_placeholders={"nome": self._dati[CONF_NOME]},
        )

    async def async_step_non_raggiungibile(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """La VMC non risponde: si puo' aggiungere comunque (es. Prima Installazione VMC)."""
        if user_input is not None:
            return self._crea_voce()
        return self.async_show_form(
            step_id="non_raggiungibile",
            description_placeholders={"ip": self._dati[CONF_HOST]},
        )

    def _crea_voce(self) -> ConfigFlowResult:
        nome = self._dati[CONF_NOME]
        return self.async_create_entry(title=f"VMC {nome}", data=self._dati)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        return VmcMasterOptionsFlow()


class VmcMasterOptionsFlow(OptionsFlow):
    """Cambia l'IP della VMC (sostituisce lo script Cambia IP)."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        errori: dict[str, str] = {}
        voce = self.config_entry
        if user_input is not None:
            ip = user_input[CONF_HOST].strip()
            ips = {
                v.data[CONF_HOST]
                for v in self.hass.config_entries.async_entries(DOMAIN)
                if v.entry_id != voce.entry_id
            }
            if not ip_valido(ip):
                errori[CONF_HOST] = "ip_non_valido"
            elif ip in ips:
                errori[CONF_HOST] = "ip_in_uso"
            else:
                self.hass.config_entries.async_update_entry(
                    voce, data={**voce.data, CONF_HOST: ip}
                )
                return self.async_create_entry(data={})
        schema = vol.Schema(
            {vol.Required(CONF_HOST, default=voce.data[CONF_HOST]): str}
        )
        return self.async_show_form(step_id="init", data_schema=schema, errors=errori)
