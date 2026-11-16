"""Configurazione da interfaccia: una voce per ogni VMC (nome + IP).

«Aggiungi dispositivo» chiede per prima cosa se la VMC e' gia' collegata al Wi-Fi di casa:
- si': basta l'IP (la prima VMC si chiama «master», per le altre il nome si legge dalla VMC);
- no: la VMC si collega al Wi-Fi da qui, con il motore della Finestra Prima Installazione VMC
  della release 8.6.0 (serve Home Assistant OS con una scheda Wi-Fi).
"""

from __future__ import annotations

import asyncio
import logging
import re
import unicodedata
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.core import callback
from homeassistant.helpers.hassio import is_hassio
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)

from . import prima_installazione as pi
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
from .installatore import installazione_manuale, ip_nel_package, nome_manuale_con_ip

_LOGGER = logging.getLogger(__name__)

# Campi del collegamento al Wi-Fi (stessi dati della Finestra Prima Installazione VMC)
CONF_RETE_VMC = "rete_vmc"
CONF_PASSWORD_VMC = "password_vmc"
CONF_RETE_CASA = "rete_casa"
CONF_PASSWORD_CASA = "password_casa"
PASSWORD_VMC_FABBRICA = "12345678"

# Errori del motore che dicono che questo Home Assistant non puo' usare il Wi-Fi
_SENZA_WIFI = {"no_wifi", "supervisor_unavailable"}


def ip_valido(ip: str) -> bool:
    """IPv4 con quattro numeri da 0 a 255 (999.999.999.999 non e' valido)."""
    return bool(IP_RE.fullmatch(ip)) and all(0 <= int(p) <= 255 for p in ip.split("."))


async def async_nome_vmc(ip: str) -> str | None:
    """Chiede il nome alla VMC (comando VMNM?) sulla porta 5001.

    None se la VMC non risponde; "" se risponde senza un nome leggibile.
    """
    try:
        lettore, scrittore = await asyncio.wait_for(
            asyncio.open_connection(ip, PORTA_VMC), TIMEOUT_VMC
        )
    except (OSError, TimeoutError):
        return None
    try:
        scrittore.write(b"VMNM?")
        await scrittore.drain()
        risposta = await asyncio.wait_for(lettore.read(256), TIMEOUT_VMC)
    except (OSError, TimeoutError):
        return None
    finally:
        scrittore.close()
    _LOGGER.debug("Risposta della VMC %s: %s", ip, risposta)
    if not risposta:
        return None
    testo = risposta.decode("utf-8", errors="ignore").strip()
    # come il motore della Prima Installazione: «VMNM <nome>» con eventuali «*» in coda
    return testo[5:].rstrip("* ").strip() if testo.startswith("VMNM ") else ""


async def async_prova_vmc(ip: str) -> bool:
    """True se la VMC risponde sulla porta 5001."""
    return await async_nome_vmc(ip) is not None


def nome_da_vmc(nome_vmc: str) -> str:
    """Nome della VMC (Air Guard, fino a 12 caratteri) -> nome per l'integrazione.

    Solo lettere minuscole a-z, senza accenti, spazi e numeri, senza la parola «VMC»
    davanti e al massimo 10 lettere: «VMC Sala Grande» -> «salagrande».
    """
    parole = nome_vmc.split()
    if len(parole) > 1 and parole[0].lower() == "vmc":
        parole = parole[1:]
    senza_accenti = unicodedata.normalize("NFKD", "".join(parole))
    lettere = re.sub(r"[^a-z]", "", senza_accenti.encode("ascii", "ignore").decode().lower())
    return lettere[:10]


def _messaggio(errore: pi.Failure) -> str:
    """Messaggio del motore senza il rimando alla tabella della vecchia finestra:
    la tabella dei lampeggi e' nella finestra dell'errore."""
    return errore.message.replace(pi.LED_HINT, "").strip()


def _opzioni_reti(reti: list[dict[str, Any]]) -> list[SelectOptionDict]:
    opzioni: list[SelectOptionDict] = []
    for rete in reti:
        dettagli = ", ".join(
            p for p in (rete.get("band", ""), f"{rete.get('signal', 0)} %") if p
        )
        opzioni.append(SelectOptionDict(value=rete["ssid"], label=f"{rete['ssid']} ({dettagli})"))
    return opzioni


class VmcMasterConfigFlow(ConfigFlow, domain=DOMAIN):
    """Aggiunge una VMC."""

    VERSION = 1

    def __init__(self) -> None:
        self._dati: dict[str, str] = {}
        self._nome_vmc = ""
        self._risponde = True
        # collegamento al Wi-Fi
        self._reti: dict[str, Any] = {}
        self._richiesta: dict[str, str] = {}
        self._collegata: dict[str, str] = {}
        self._errore = ""
        self._errore_ip = ""
        self._ip_da_verificare = ""
        self._task: asyncio.Task | None = None

    def _nomi_e_ip_in_uso(self, escludi: str | None = None) -> tuple[set[str], set[str]]:
        nomi: set[str] = set()
        ips: set[str] = set()
        for voce in self._async_current_entries(include_ignore=False):
            if voce.entry_id == escludi:
                continue
            nomi.add(voce.data[CONF_NOME])
            ips.add(voce.data[CONF_HOST])
        return nomi, ips

    # ---- Domanda iniziale ---------------------------------------------------------
    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """È gia' collegata al Wi-Fi di casa o va installata da zero?"""
        opzioni = ["in_rete", "da_installare"]
        _nomi, ips = self._nomi_e_ip_in_uso()
        ultima = await self.hass.async_add_executor_job(
            pi.ultima_vmc, self.hass.config.config_dir
        )
        segnaposto = {"rete_vmc": "-", "ip": "-"}
        if ultima.get("ip") and ultima.get("ap_ssid") and ultima["ip"] not in ips:
            # VMC collegata al Wi-Fi ma non ancora aggiunta (es. finestra chiusa durante il collegamento)
            opzioni.append("riprendi")
            segnaposto = {"rete_vmc": ultima["ap_ssid"], "ip": ultima["ip"]}
        return self.async_show_menu(
            step_id="user", menu_options=opzioni, description_placeholders=segnaposto
        )

    # ---- VMC gia' collegata al Wi-Fi di casa: basta l'IP ----------------------------
    async def async_step_in_rete(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        errori: dict[str, str] = {}
        nomi, ips = self._nomi_e_ip_in_uso()
        if user_input is not None:
            ip = user_input[CONF_HOST].strip()
            if not ip_valido(ip):
                errori[CONF_HOST] = "ip_non_valido"
            elif ip in ips:
                errori[CONF_HOST] = "ip_in_uso"
            else:
                if NOME_MASTER not in nomi:
                    # la prima VMC si chiama sempre «master»
                    return await self._async_continua(NOME_MASTER, ip, raggiungibile=None)
                nome_vmc = await async_nome_vmc(ip)
                return await self._async_scegli_nome(ip, nome_vmc or "", nome_vmc is not None)

        ip_predefinito = ""
        if NOME_MASTER not in nomi and await self.hass.async_add_executor_job(
            installazione_manuale, self.hass.config.config_dir, NOME_MASTER
        ):
            # Installazione manuale della release 8.6.0: propone l'IP gia' impostato
            ip_trovato = await self.hass.async_add_executor_job(
                ip_nel_package, self.hass.config.config_dir, NOME_MASTER
            )
            if ip_trovato and ip_valido(ip_trovato):
                ip_predefinito = ip_trovato
        schema = vol.Schema(
            {
                vol.Required(
                    CONF_HOST, default=(user_input or {}).get(CONF_HOST, ip_predefinito)
                ): str
            }
        )
        return self.async_show_form(step_id="in_rete", data_schema=schema, errors=errori)

    async def _async_scegli_nome(
        self, ip: str, nome_vmc: str, risponde: bool
    ) -> ConfigFlowResult:
        """La prima VMC e' «master»; per le altre si propone il nome letto dalla VMC."""
        nomi, _ips = self._nomi_e_ip_in_uso()
        if NOME_MASTER not in nomi:
            return await self._async_continua(NOME_MASTER, ip, raggiungibile=risponde)
        self._dati = {CONF_HOST: ip}
        self._nome_vmc = nome_vmc
        self._risponde = risponde
        return await self.async_step_nome()

    async def async_step_nome(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Nome letto dalla VMC: si mostra convertito e si puo' correggere prima di creare."""
        errori: dict[str, str] = {}
        nomi, _ips = self._nomi_e_ip_in_uso()
        ip = self._dati[CONF_HOST]
        # VMC installata a mano con questo IP (migrazione): stesso nome della sua cartella
        proposta = await self.hass.async_add_executor_job(
            nome_manuale_con_ip, self.hass.config.config_dir, ip
        ) or nome_da_vmc(self._nome_vmc)
        nome = proposta if user_input is None else (user_input.get(CONF_NOME) or "").strip()
        if not NOME_RE.fullmatch(nome):
            errori[CONF_NOME] = "nome_non_valido"
        elif nome in nomi or nome == NOME_MASTER:
            errori[CONF_NOME] = "nome_in_uso"
        if user_input is not None and not errori:
            return await self._async_continua(nome, ip, raggiungibile=self._risponde)
        return self.async_show_form(
            # VMC che non risponde: stesso passo, ma la finestra chiede di scrivere il nome
            step_id="nome" if self._risponde else "nome_manuale",
            data_schema=vol.Schema(
                {vol.Required(CONF_NOME, description={"suggested_value": nome}): str}
            ),
            errors=errori if (user_input is not None or proposta) else {},
            description_placeholders={
                "ip": ip,
                "nome_vmc": self._nome_vmc or "-",
                "proposta": proposta or "-",
            },
        )

    async def async_step_nome_manuale(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        return await self.async_step_nome(user_input)

    async def _async_continua(
        self, nome: str, ip: str, raggiungibile: bool | None
    ) -> ConfigFlowResult:
        await self.async_set_unique_id(nome)
        self._abort_if_unique_id_configured()
        self._dati = {CONF_NOME: nome, CONF_HOST: ip}
        if await self.hass.async_add_executor_job(
            installazione_manuale, self.hass.config.config_dir, nome
        ):
            return await self.async_step_migra()
        if raggiungibile is None:
            raggiungibile = await async_prova_vmc(ip)
        if raggiungibile:
            return self._crea_voce()
        return await self.async_step_non_raggiungibile()

    async def async_step_migra(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Trovata un'installazione manuale: la cartella va in backup e la sostituisce l'integrazione."""
        if user_input is not None:
            return self._crea_voce()
        ip_trovato = await self.hass.async_add_executor_job(
            ip_nel_package, self.hass.config.config_dir, self._dati[CONF_NOME]
        )
        return self.async_show_form(
            step_id="migra",
            description_placeholders={
                "nome": self._dati[CONF_NOME],
                "ip": self._dati[CONF_HOST],
                "ip_trovato": ip_trovato or "-",
            },
        )

    async def async_step_non_raggiungibile(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """La VMC non risponde: si puo' aggiungere comunque (es. VMC spenta)."""
        if user_input is not None:
            return self._crea_voce()
        return self.async_show_form(
            step_id="non_raggiungibile",
            description_placeholders={"ip": self._dati[CONF_HOST]},
        )

    def _crea_voce(self) -> ConfigFlowResult:
        nome = self._dati[CONF_NOME]
        return self.async_create_entry(title=f"VMC {nome}", data=self._dati)

    # ---- VMC da installare: collegamento al Wi-Fi di casa ----------------------------
    async def async_step_da_installare(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if not is_hassio(self.hass):
            # Docker o Core: niente Supervisor, il Wi-Fi del server non si puo' usare
            return self.async_abort(reason="senza_supervisor")
        return await self.async_step_cerca()

    def _avvia(self, azione: str, dati: dict[str, Any] | None = None) -> asyncio.Task:
        """Avvia il motore in un thread; la barra di avanzamento segue i suoi passi."""

        def avanzamento(percento: int) -> None:
            self.hass.loop.call_soon_threadsafe(
                self.async_update_progress, min(max(percento, 0), 100) / 100
            )

        async def _esegui() -> dict[str, Any]:
            return await self.hass.async_add_executor_job(
                pi.esegui, self.hass.config.config_dir, azione, dati, avanzamento
            )

        return self.hass.async_create_task(_esegui(), f"{DOMAIN}_{azione}")

    async def async_step_cerca(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Ricerca delle reti Wi-Fi VMC_xxxxxxxx, come la scansione dello smartphone."""
        # La prima volta si mostra sempre la barra, anche se il motore ha gia' finito:
        # passare subito al passo seguente gli darebbe i dati del passo precedente
        nuovo = self._task is None
        if nuovo:
            self._task = self._avvia("scan")
        if nuovo or not self._task.done():
            return self.async_show_progress(
                step_id="cerca", progress_action="cerca", progress_task=self._task
            )
        task, self._task = self._task, None
        self._errore = ""
        try:
            task.result()
        except pi.Failure as errore:
            if errore.code in _SENZA_WIFI:
                return self.async_show_progress_done(next_step_id="senza_wifi")
            # la rete della VMC si puo' scrivere a mano
            self._errore = _messaggio(errore)
        self._reti = await self.hass.async_add_executor_job(
            pi.stato, self.hass.config.config_dir
        )
        if not self._richiesta.get(CONF_RETE_CASA):
            rete_server = await self.hass.async_add_executor_job(
                pi.rete_del_server, self.hass.config.config_dir
            )
            self._richiesta = {**self._richiesta, CONF_RETE_CASA: rete_server}
        return self.async_show_progress_done(next_step_id="rete_vmc")

    async def async_step_senza_wifi(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        return self.async_abort(reason="senza_wifi")

    async def async_step_rete_vmc(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Rete della VMC (VMC_xxxxxxxx) e rete Wi-Fi di casa."""
        errori: dict[str, str] = {}
        if self._errore:
            errori["base"] = "motore"
        if user_input is not None:
            self._richiesta = {
                CONF_RETE_VMC: str(user_input.get(CONF_RETE_VMC, "")).strip(),
                CONF_PASSWORD_VMC: str(user_input.get(CONF_PASSWORD_VMC, "")),
                CONF_RETE_CASA: str(user_input.get(CONF_RETE_CASA, "")).strip(),
                CONF_PASSWORD_CASA: str(user_input.get(CONF_PASSWORD_CASA, "")),
            }
            try:
                # stessi controlli del motore prima di toccare il Wi-Fi del server
                pi.motore.normalize_request(self._dati_motore())
            except pi.Failure as errore:
                self._errore = _messaggio(errore)
                errori["base"] = "motore"
            else:
                self._errore = ""
                return await self.async_step_collega()

        reti_vmc = list(self._reti.get("vmc_networks") or [])
        altre = list(self._reti.get("wifi_networks") or [])
        rete_vmc = self._richiesta.get(CONF_RETE_VMC) or (reti_vmc[0]["ssid"] if reti_vmc else "")
        rete_casa = self._richiesta.get(CONF_RETE_CASA) or (altre[0]["ssid"] if altre else "")
        schema = vol.Schema(
            {
                vol.Required(CONF_RETE_VMC, default=rete_vmc): SelectSelector(
                    SelectSelectorConfig(
                        options=_opzioni_reti(reti_vmc),
                        custom_value=True,
                        mode=SelectSelectorMode.DROPDOWN,
                    )
                ),
                vol.Required(
                    CONF_PASSWORD_VMC,
                    default=self._richiesta.get(CONF_PASSWORD_VMC, PASSWORD_VMC_FABBRICA),
                ): str,
                vol.Required(CONF_RETE_CASA, default=rete_casa): SelectSelector(
                    SelectSelectorConfig(
                        options=_opzioni_reti(altre),
                        custom_value=True,
                        mode=SelectSelectorMode.DROPDOWN,
                    )
                ),
                vol.Required(CONF_PASSWORD_CASA): TextSelector(
                    TextSelectorConfig(type=TextSelectorType.PASSWORD)
                ),
            }
        )
        return self.async_show_form(
            step_id="rete_vmc",
            data_schema=schema,
            errors=errori,
            description_placeholders={
                "trovate": str(len(reti_vmc)),
                "errore": self._errore or "-",
            },
        )

    def _dati_motore(self) -> dict[str, str]:
        return {
            "ap_ssid": self._richiesta.get(CONF_RETE_VMC, ""),
            "ap_password": self._richiesta.get(CONF_PASSWORD_VMC, ""),
            "home_ssid": self._richiesta.get(CONF_RETE_CASA, ""),
            "home_password": self._richiesta.get(CONF_PASSWORD_CASA, ""),
            "final_ip": "",
        }

    async def async_step_collega(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Il server si collega alla rete della VMC, invia la rete di casa e ritrova la VMC."""
        nuovo = self._task is None
        if nuovo:
            self._task = self._avvia("configure", self._dati_motore())
        if nuovo or not self._task.done():
            return self.async_show_progress(
                step_id="collega",
                progress_action="collega",
                progress_task=self._task,
                description_placeholders={
                    "rete_vmc": self._richiesta[CONF_RETE_VMC],
                    "rete_casa": self._richiesta[CONF_RETE_CASA],
                },
            )
        task, self._task = self._task, None
        # la password di casa non resta nella finestra
        self._richiesta[CONF_PASSWORD_CASA] = ""
        try:
            task.result()
        except pi.Failure as errore:
            self._errore = _messaggio(errore)
            return self.async_show_progress_done(next_step_id="errore")
        self._collegata = await self.hass.async_add_executor_job(
            pi.ultima_vmc, self.hass.config.config_dir
        )
        self._errore_ip = ""
        return self.async_show_progress_done(next_step_id="ip_fisso")

    async def async_step_errore(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Collegamento non riuscito: messaggio del motore e tabella dei lampeggi del LED."""
        messaggio, self._errore = self._errore, ""
        return self.async_show_menu(
            step_id="errore",
            menu_options=["rete_vmc", "cerca"],
            description_placeholders={"errore": messaggio or "-"},
        )

    async def async_step_riprendi(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """VMC gia' collegata al Wi-Fi da una procedura precedente: si riparte dall'IP fisso."""
        self._collegata = await self.hass.async_add_executor_job(
            pi.ultima_vmc, self.hass.config.config_dir
        )
        self._errore_ip = ""
        return await self.async_step_ip_fisso()

    async def async_step_ip_fisso(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """IP e MAC della VMC collegata: si prenota l'IP sul router (o se ne scrive un altro)."""
        errori: dict[str, str] = {}
        if self._errore_ip:
            errori["base"] = "motore"
        ip_collegata = self._collegata.get("ip", "")
        if user_input is not None:
            ip = user_input[CONF_HOST].strip()
            _nomi, ips = self._nomi_e_ip_in_uso()
            self._errore_ip = ""
            errori = {}
            if not ip_valido(ip):
                errori[CONF_HOST] = "ip_non_valido"
            elif ip in ips:
                errori[CONF_HOST] = "ip_in_uso"
            elif ip == ip_collegata:
                return await self._async_scegli_nome(
                    ip, self._collegata.get("name", ""), True
                )
            else:
                # IP prenotato diverso: si controlla che risponda la stessa VMC
                self._ip_da_verificare = ip
                return await self.async_step_verifica()
        return self.async_show_form(
            step_id="ip_fisso",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_HOST,
                        default=(user_input or {}).get(
                            CONF_HOST, self._ip_da_verificare or ip_collegata
                        ),
                    ): str
                }
            ),
            errors=errori,
            description_placeholders={
                "rete_vmc": self._collegata.get("ap_ssid", "") or "-",
                "nome_vmc": self._collegata.get("name", "") or "-",
                "ip": ip_collegata or "-",
                "mac": self._collegata.get("mac", "") or "-",
                "errore": self._errore_ip or "-",
            },
        )

    async def async_step_verifica(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Verifica dell'IP prenotato: deve rispondere la stessa VMC (nome e MAC)."""
        nuovo = self._task is None
        if nuovo:
            self._task = self._avvia(
                "verify",
                {"ip": self._ip_da_verificare, "ap_ssid": self._collegata.get("ap_ssid", "")},
            )
        if nuovo or not self._task.done():
            return self.async_show_progress(
                step_id="verifica",
                progress_action="verifica",
                progress_task=self._task,
                description_placeholders={"ip": self._ip_da_verificare},
            )
        task, self._task = self._task, None
        try:
            task.result()
        except pi.Failure as errore:
            self._errore_ip = _messaggio(errore)
        else:
            self._errore_ip = ""
            self._collegata = await self.hass.async_add_executor_job(
                pi.ultima_vmc, self.hass.config.config_dir
            )
        return self.async_show_progress_done(next_step_id="dopo_verifica")

    async def async_step_dopo_verifica(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if self._errore_ip:
            return await self.async_step_ip_fisso()
        self._ip_da_verificare = ""
        return await self._async_scegli_nome(
            self._collegata.get("ip", ""), self._collegata.get("name", ""), True
        )

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
