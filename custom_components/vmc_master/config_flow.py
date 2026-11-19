"""Configurazione da interfaccia: una voce per ogni VMC (nome + IP).

«Aggiungi dispositivo» chiede per prima cosa se la VMC e' gia' collegata al Wi-Fi di casa:
- si': basta l'IP (la prima VMC si chiama «master», per le altre il nome si legge dalla VMC);
  il titolo della voce e' il nome della VMC (quello dell'App Air Guard);
- no: la VMC si collega al Wi-Fi da qui, con il motore della Finestra Prima Installazione VMC
  della release 8.6.0 (serve Home Assistant OS con una scheda Wi-Fi).
"""

from __future__ import annotations

import asyncio
import ipaddress
import logging
import re
import unicodedata
from typing import Any

import voluptuous as vol

from homeassistant.components import persistent_notification
from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import issue_registry as ir
from homeassistant.helpers.hassio import is_hassio
from homeassistant.helpers.translation import async_get_translations
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
    CONF_TITOLO,
    DOMAIN,
    IP_RE,
    NOME_MASTER,
    NOME_RE,
    PORTA_VMC,
    TIMEOUT_VMC,
)
from .installatore import (
    cartella_vmc,
    installazione_manuale,
    ip_nel_package,
    leggi_marcatore,
    nome_manuale_con_ip,
)

_LOGGER = logging.getLogger(__name__)

# Campi del collegamento al Wi-Fi (stessi dati della Finestra Prima Installazione VMC)
CONF_RETE_VMC = "rete_vmc"
CONF_PASSWORD_VMC = "password_vmc"
CONF_RETE_CASA = "rete_casa"
CONF_PASSWORD_CASA = "password_casa"
# Password della rete Wi-Fi a cui e' collegato ora il server, se diversa da quella di casa
CONF_PASSWORD_SERVER = "password_server"
PASSWORD_VMC_FABBRICA = "12345678"

# Avviso delle Riparazioni «VMC Master: riavviare Home Assistant» (stesso id di __init__.py)
ISSUE_RIAVVIO = "riavvio_necessario"

# Errori del motore che dicono che questo Home Assistant non puo' usare il Wi-Fi
_SENZA_WIFI = {"no_wifi", "supervisor_unavailable"}


def ip_valido(ip: str) -> bool:
    """IPv4 con quattro numeri da 0 a 255 (999.999.999.999 non e' valido), senza zeri
    iniziali: «x.x.x.010» non e' valido (per qualcuno e' x.x.x.8).

    Deve poter essere l'indirizzo di un dispositivo (unicast, privato o pubblico): non
    valgono 0.x.x.x (0.0.0.0 raggiunge il server stesso), 127.x.x.x (il server stesso),
    169.254.x.x (link-local), 224.0.0.0-239.255.255.255 (multicast) e da 240.0.0.0 in su
    (riservati, compreso 255.255.255.255)."""
    if not IP_RE.fullmatch(ip):
        return False
    try:
        indirizzo = ipaddress.IPv4Address(ip)
    except ValueError:
        return False
    if str(indirizzo) != ip:
        return False
    return not (
        ip.startswith("0.")
        or indirizzo.is_loopback
        or indirizzo.is_link_local
        or indirizzo.is_multicast
        or indirizzo.is_reserved
        or indirizzo.is_unspecified
    )


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
        # come il motore: la risposta puo' arrivare in piu' pezzi; dopo un pezzo completo
        # si attende al massimo 0,12 s, altrimenti fino a TIMEOUT_VMC dall'invio
        ciclo = asyncio.get_running_loop()
        scadenza = ciclo.time() + TIMEOUT_VMC
        risposta = b""
        while len(risposta) < 256:
            if risposta and pi.motore.name_answer_complete(risposta):
                attesa = 0.12
            else:
                attesa = scadenza - ciclo.time()
                if attesa <= 0:
                    break
            try:
                pezzo = await asyncio.wait_for(lettore.read(256 - len(risposta)), attesa)
            except TimeoutError:
                if risposta:
                    break
                raise
            if not pezzo:
                break
            risposta += pezzo
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


async def async_nome_vmc_due_prove(ip: str) -> str | None:
    """Nome della VMC con una seconda prova se la prima non riceve risposta (la prima
    risposta puo' andare persa): stesse attese di async_nome_vmc, nessuna attesa in piu'.

    Lo usano tutte le finestre che leggono il nome a un IP (in_rete, ip_fisso senza MAC,
    cambia_ip) e il servizio verifica_ip del campo «Cambia IP VMC» della scheda."""
    nome = await async_nome_vmc(ip)
    if nome is None:
        # anche la seconda prova legge il nome, che va confrontato come alla prima
        nome = await async_nome_vmc(ip)
    return nome


async def async_prova_vmc(ip: str) -> bool:
    """True se a quell'IP risponde una VMC sulla porta 5001 (risposta «VMNM <nome>»):
    un altro dispositivo che risponde sulla 5001 senza nome non conta come VMC."""
    return bool(await async_nome_vmc(ip))


def nome_da_vmc(nome_vmc: str) -> str:
    """Nome della VMC (Air Guard, fino a 12 caratteri) -> nome per l'integrazione.

    Solo lettere minuscole a-z, senza accenti, spazi e numeri, senza la parola «VMC»
    davanti e al massimo 10 lettere: «VMC Primo Piano» -> «primopiano».
    """
    parole = [p for p in re.split(r"[\s_-]+", nome_vmc) if p]
    if len(parole) > 1 and parole[0].lower() == "vmc":
        parole = parole[1:]
    senza_accenti = unicodedata.normalize("NFKD", "".join(parole))
    lettere = re.sub(r"[^a-z]", "", senza_accenti.encode("ascii", "ignore").decode().lower())
    return lettere[:10]


def titolo_voce(nome_vmc: str | None, nome: str) -> str:
    """Titolo della voce in Dispositivi e servizi: il nome della VMC (Air Guard).

    «VMC Soggiorno» (o «VMC_Soggiorno», «vmc-soggiorno») resta com'e', «Soggiorno» diventa
    «VMC Soggiorno»; senza nome letto resta «VMC ‹nome›» (il nome interno, che non cambia
    mai). Le parole si dividono come in nome_da_vmc: spazi, «_» e «-».
    """
    nome_vmc = (nome_vmc or "").strip()
    parole = [p for p in re.split(r"[\s_-]+", nome_vmc) if p]
    if not parole:
        return f"VMC {nome}"
    if parole[0].lower() == "vmc":
        return nome_vmc
    return f"VMC {nome_vmc}"


def _confrontabile(testo: str) -> str:
    """Nome senza differenze di maiuscole e separatori («VMC_Zona» = «vmc zona»)."""
    return " ".join(p for p in re.split(r"[\s_-]+", testo.lower()) if p)


def esito_verifica_ip(nome_letto: str | None, nome_atteso: str, nome: str = "") -> str:
    """Esito della lettura del nome a un IP nuovo, con le regole dell'ingranaggio
    «Cambia l'IP della VMC» (le usa anche il servizio verifica_ip della scheda):

    - «non_risponde»: nessuna risposta sulla porta 5001 (VMC spenta o IP sbagliato);
    - «altro_dispositivo»: risponde senza il nome della VMC (non e' una VMC);
    - «nome_diverso»: risponde una VMC con un nome diverso da nome_atteso (un'altra VMC,
      oppure nome cambiato nell'App Air Guard); senza nome_atteso non si confronta;
    - «ok»: risponde la VMC attesa.

    I nomi si confrontano come titoli della voce («Soggiorno» = «VMC_Soggiorno»); nome e'
    il nome interno della VMC, usato da titolo_voce solo per un nome senza parole."""
    if nome_letto is None:
        return "non_risponde"
    if not nome_letto:
        return "altro_dispositivo"
    atteso = nome_atteso.rstrip("* ").strip()
    if atteso and _confrontabile(titolo_voce(nome_letto, nome)) != _confrontabile(
        titolo_voce(atteso, nome)
    ):
        return "nome_diverso"
    return "ok"


def _messaggio(errore: pi.Failure) -> str:
    """Messaggio del motore senza il rimando alla tabella della vecchia finestra:
    la tabella dei lampeggi e' nella finestra dell'errore."""
    return errore.message.replace(pi.LED_HINT, "").strip()


async def async_messaggio_errore(hass: HomeAssistant, errore: pi.Failure) -> str:
    """Messaggio di un errore del motore nella lingua di Home Assistant.

    In italiano resta il messaggio del motore (contiene IP, nomi delle reti...); nelle
    altre lingue si usa il testo inglese della sezione «exceptions» delle traduzioni,
    cercato per codice dell'errore, o il messaggio del motore se il codice non c'e'."""
    lingua = hass.config.language or ""
    if lingua.lower().startswith("it"):
        return _messaggio(errore)
    try:
        testi = await async_get_translations(hass, lingua, "exceptions", {DOMAIN})
    except Exception:  # noqa: BLE001 - un testo mancante non deve fermare la finestra
        _LOGGER.debug("Traduzioni degli errori non disponibili", exc_info=True)
        testi = {}
    return testi.get(f"component.{DOMAIN}.exceptions.{errore.code}.message") or _messaggio(
        errore
    )


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
        # rete Wi-Fi del server da ripristinare con una password ("" se non serve)
        self._rete_server = ""
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
                # il nome letto serve anche alla prima VMC («master») per il titolo della voce
                nome_vmc = await async_nome_vmc_due_prove(ip)
                # risponde senza nome («»): non si sa se e' una VMC, il nome si scrive a mano
                return await self._async_scegli_nome(ip, nome_vmc or "", bool(nome_vmc))

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
        self._nome_vmc = nome_vmc
        if NOME_MASTER not in nomi:
            return await self._async_continua(NOME_MASTER, ip, raggiungibile=risponde)
        self._dati = {CONF_HOST: ip}
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
            # VMC che non risponde o senza nome letto: stesso passo, ma la finestra chiede
            # di scrivere il nome (niente «Nome letto: «-»»)
            step_id="nome" if self._risponde and self._nome_vmc else "nome_manuale",
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
            return await self._async_crea_voce()
        return await self.async_step_non_raggiungibile()

    async def async_step_migra(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Trovata un'installazione manuale: la cartella va in backup e la sostituisce l'integrazione."""
        if user_input is not None:
            return await self._async_crea_voce()
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
            return await self._async_crea_voce()
        return self.async_show_form(
            step_id="non_raggiungibile",
            description_placeholders={"ip": self._dati[CONF_HOST]},
        )

    async def _async_crea_voce(self) -> ConfigFlowResult:
        """Crea la voce. Se dopo l'installazione del package serve un riavvio (avviso
        «VMC Master: riavviare Home Assistant»), il messaggio finale dice come farlo."""
        titolo = titolo_voce(self._nome_vmc, self._dati[CONF_NOME])
        if await self._async_serve_riavvio(self._dati[CONF_NOME]):
            return self.async_create_entry(
                title=titolo,
                data={**self._dati, CONF_TITOLO: titolo},
                description="riavvio",
                description_placeholders={"titolo": titolo},
            )
        return self.async_create_entry(
            title=titolo, data={**self._dati, CONF_TITOLO: titolo}
        )

    async def _async_serve_riavvio(self, nome: str) -> bool:
        """True se il package della VMC verra' scritto da zero (file nuovi: Home Assistant
        li carica solo dopo un riavvio) o se un riavvio e' gia' chiesto.

        Package gia' scritto dall'integrazione (marcatore con md5): al massimo si ricarica."""
        if ir.async_get(self.hass).async_get_issue(DOMAIN, ISSUE_RIAVVIO) is not None:
            return True
        config_dir = self.hass.config.config_dir

        def _package_gia_installato() -> bool:
            return (cartella_vmc(config_dir, nome) / f"vmc_{nome}.yaml").is_file() and isinstance(
                leggi_marcatore(config_dir, nome).get("md5"), dict
            )

        return not await self.hass.async_add_executor_job(_package_gia_installato)

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
            self._errore = await async_messaggio_errore(self.hass, errore)
        self._reti = await self.hass.async_add_executor_job(
            pi.stato, self.hass.config.config_dir
        )
        if not self._richiesta.get(CONF_RETE_CASA):
            rete_server = await self.hass.async_add_executor_job(
                pi.rete_del_server, self.hass.config.config_dir
            )
            self._richiesta = {**self._richiesta, CONF_RETE_CASA: rete_server}
        self._rete_server = await self.hass.async_add_executor_job(
            pi.rete_da_ripristinare, self.hass.config.config_dir
        )
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
                CONF_PASSWORD_SERVER: str(user_input.get(CONF_PASSWORD_SERVER, "")),
            }
            try:
                # stessi controlli del motore prima di toccare il Wi-Fi del server
                pi.motore.normalize_request(self._dati_motore())
            except pi.Failure as errore:
                self._errore = await async_messaggio_errore(self.hass, errore)
                errori["base"] = "motore"
            else:
                self._errore = ""
                if (
                    self._rete_server
                    and self._rete_server != self._richiesta[CONF_RETE_CASA]
                    and not self._richiesta[CONF_PASSWORD_SERVER]
                ):
                    # il server e' su un'altra rete Wi-Fi: serve la sua password per tornarci
                    errori[CONF_PASSWORD_SERVER] = "password_server_mancante"
                else:
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
        if self._rete_server:
            # solo se il server e' collegato via Wi-Fi a una rete protetta
            schema = schema.extend(
                {
                    vol.Optional(CONF_PASSWORD_SERVER): TextSelector(
                        TextSelectorConfig(type=TextSelectorType.PASSWORD)
                    )
                }
            )
        return self.async_show_form(
            step_id="rete_vmc",
            data_schema=schema,
            errors=errori,
            description_placeholders={
                "trovate": str(len(reti_vmc)),
                "errore": self._errore or "-",
                "rete_del_server": self._rete_server or "-",
            },
        )

    def _dati_motore(self) -> dict[str, str]:
        dati = {
            "ap_ssid": self._richiesta.get(CONF_RETE_VMC, ""),
            "ap_password": self._richiesta.get(CONF_PASSWORD_VMC, ""),
            "home_ssid": self._richiesta.get(CONF_RETE_CASA, ""),
            "home_password": self._richiesta.get(CONF_PASSWORD_CASA, ""),
            "final_ip": "",
        }
        if self._richiesta.get(CONF_PASSWORD_SERVER):
            # il motore la usa per riportare il Wi-Fi del server alla sua rete
            dati["restore_password"] = self._richiesta[CONF_PASSWORD_SERVER]
        return dati

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
        # le password non restano nella finestra
        self._richiesta[CONF_PASSWORD_CASA] = ""
        self._richiesta[CONF_PASSWORD_SERVER] = ""
        try:
            task.result()
        except pi.Failure as errore:
            self._errore = await async_messaggio_errore(self.hass, errore)
            if errore.code == "restore_password_required":
                # rete del server cambiata dopo la ricerca: il campo della password compare
                self._rete_server = await self.hass.async_add_executor_job(
                    pi.rete_da_ripristinare, self.hass.config.config_dir
                )
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
            elif self._collegata.get("mac"):
                # IP prenotato diverso: il motore controlla che risponda la stessa VMC (nome e MAC)
                self._ip_da_verificare = ip
                return await self.async_step_verifica()
            else:
                # MAC non rilevato: basta che a quell'IP risponda la VMC con lo stesso nome
                atteso = self._collegata.get("name", "")
                nome_letto = await async_nome_vmc_due_prove(ip)
                if nome_letto is None:
                    errori[CONF_HOST] = "ip_non_risponde_riavvia"
                elif not nome_letto or (atteso and nome_letto != atteso):
                    errori[CONF_HOST] = "ip_altro_dispositivo"
                else:
                    await self.hass.async_add_executor_job(
                        pi.aggiorna_ip, self.hass.config.config_dir, ip_collegata, ip
                    )
                    self._collegata = {**self._collegata, "ip": ip}
                    return await self._async_scegli_nome(ip, atteso or nome_letto, True)
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
            self._errore_ip = await async_messaggio_errore(self.hass, errore)
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
    """Ingranaggio della VMC: cambia l'IP oppure elimina la VMC (solo da Home Assistant o
    anche dalla rete). La finestra «Elimina» del menu ⋮ e' di Home Assistant e non si
    puo' cambiare: elimina solo da Home Assistant."""

    def __init__(self) -> None:
        self._task: asyncio.Task | None = None
        self._errore = ""
        # IP che non risponde o con un altro nome, gia' segnalato: con un secondo Invia
        # si salva lo stesso
        self._ip_avvisato = ""
        # segnaposto salvati prima di eliminare la voce (dopo non c'e' piu')
        self._segnaposto_eliminata: dict[str, str] = {}
        # finestra chiusa: un errore dell'Access Point si segnala con una notifica
        self._finestra_chiusa = False

    @callback
    def async_remove(self) -> None:
        """Finestra chiusa (o flusso finito)."""
        self._finestra_chiusa = True

    def _segnaposto(self) -> dict[str, str]:
        return {"titolo": self.config_entry.title, "ip": self.config_entry.data[CONF_HOST]}

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        return self.async_show_menu(
            step_id="init",
            menu_options=["cambia_ip", "elimina"],
            description_placeholders=self._segnaposto(),
        )

    async def async_step_cambia_ip(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Cambia l'IP della VMC (sostituisce lo script Cambia IP).

        A un IP nuovo deve rispondere una VMC (risposta «VMNM <nome>»): un dispositivo senza
        nome si rifiuta; se la VMC non risponde (es. spenta) o ha un nome diverso da quello
        di questa voce si avvisa, e un secondo Invia salva lo stesso."""
        errori: dict[str, str] = {}
        voce = self.config_entry
        segnaposto = {"titolo": voce.title, "nome_letto": "-"}
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
            elif ip != voce.data[CONF_HOST] and ip != self._ip_avvisato:
                # seconda prova se la prima non riceve risposta (puo' andare persa)
                nome_letto = await async_nome_vmc_due_prove(ip)
                # titolo della voce preso dal nome della VMC (assente, o «VMC ‹nome›», se il
                # nome non si e' mai letto: allora non c'e' nulla con cui confrontare)
                titolo = voce.data.get(CONF_TITOLO) or ""
                if titolo == f"VMC {voce.data[CONF_NOME]}":
                    titolo = ""
                esito = esito_verifica_ip(nome_letto, titolo, voce.data[CONF_NOME])
                if esito == "altro_dispositivo":
                    # risponde sulla porta 5001 ma non come una VMC
                    errori[CONF_HOST] = "ip_altro_dispositivo"
                elif esito == "non_risponde":
                    # VMC spenta o IP sbagliato
                    self._ip_avvisato = ip
                    errori[CONF_HOST] = "ip_non_risponde"
                elif esito == "nome_diverso":
                    # un'altra VMC, oppure nome cambiato nell'App Air Guard
                    self._ip_avvisato = ip
                    segnaposto["nome_letto"] = nome_letto or ""
                    errori[CONF_HOST] = "ip_nome_diverso"
            if not errori:
                await self.hass.async_add_executor_job(
                    pi.aggiorna_ip, self.hass.config.config_dir, voce.data[CONF_HOST], ip
                )
                self.hass.config_entries.async_update_entry(
                    voce, data={**voce.data, CONF_HOST: ip}
                )
                return self.async_create_entry(data={})
        schema = vol.Schema(
            {
                vol.Required(
                    CONF_HOST, default=(user_input or {}).get(CONF_HOST, voce.data[CONF_HOST])
                ): str
            }
        )
        return self.async_show_form(
            step_id="cambia_ip",
            data_schema=schema,
            errors=errori,
            description_placeholders=segnaposto,
        )

    # ---- Elimina la VMC -----------------------------------------------------------
    async def async_step_elimina(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Solo da Home Assistant (resta sul Wi-Fi di casa) o anche dalla rete?"""
        return self.async_show_menu(
            step_id="elimina",
            menu_options=["elimina_solo_ha", "elimina_dalla_rete"],
            description_placeholders=self._segnaposto(),
        )

    def _elimina_voce(self) -> None:
        """La voce si elimina appena la finestra si chiude (come «Elimina» del menu ⋮:
        la cartella della VMC va in /config/vmc_master_backup e Home Assistant chiede il riavvio)."""
        entry_id = self.config_entry.entry_id
        self.hass.async_create_task(
            self.hass.config_entries.async_remove(entry_id), f"{DOMAIN}_elimina_{entry_id}"
        )

    async def async_step_elimina_solo_ha(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        segnaposto = self._segnaposto()
        self._elimina_voce()
        return self.async_abort(reason="eliminata", description_placeholders=segnaposto)

    def _avvia_access_point(self) -> asyncio.Task:
        """Access Point e poi eliminazione della voce nello stesso lavoro: se la finestra si
        chiude mentre il motore lavora, la voce si elimina lo stesso appena la VMC lascia
        il Wi-Fi di casa (chiudendo la finestra Home Assistant annulla solo l'attesa)."""
        ip = self.config_entry.data[CONF_HOST]
        entry_id = self.config_entry.entry_id
        self._segnaposto_eliminata = self._segnaposto()
        # avviso di un tentativo precedente fatto con la finestra chiusa
        persistent_notification.async_dismiss(self.hass, f"{DOMAIN}_access_point_{entry_id}")

        def avanzamento(percento: int) -> None:
            self.hass.loop.call_soon_threadsafe(
                self.async_update_progress, min(max(percento, 0), 100) / 100
            )

        async def _esegui() -> str | None:
            try:
                nome = await self.hass.async_add_executor_job(
                    pi.rimanda_in_access_point, self.hass.config.config_dir, ip, avanzamento
                )
            except pi.Failure as errore:
                if not self._finestra_chiusa:
                    raise  # lo mostra la finestra («Access Point non riuscito»)
                # finestra gia' chiusa: l'errore non si perde
                await self._async_notifica_errore_access_point(errore, entry_id)
                return None
            if self.hass.config_entries.async_get_entry(entry_id) is not None:
                await self.hass.config_entries.async_remove(entry_id)
            return nome

        lavoro = self.hass.async_create_background_task(
            _esegui(), f"{DOMAIN}_access_point_{entry_id}"
        )

        async def _attendi() -> str | None:
            return await asyncio.shield(lavoro)

        return self.hass.async_create_task(_attendi(), f"{DOMAIN}_attesa_access_point")

    async def _async_notifica_errore_access_point(
        self, errore: pi.Failure, entry_id: str
    ) -> None:
        """Access Point non riuscito con la finestra chiusa: notifica (la voce resta)."""
        titolo = self._segnaposto_eliminata.get("titolo", "")
        messaggio = await async_messaggio_errore(self.hass, errore)
        if (self.hass.config.language or "").lower().startswith("it"):
            intestazione = "VMC Master: Access Point non riuscito"
            testo = (
                f"{messaggio}\n\n{titolo} non è stata eliminata.\n\n"
                "Per riprovare: icona ingranaggio sulla riga della VMC → «Elimina la VMC»."
            )
        else:
            intestazione = "VMC Master: Access Point failed"
            testo = (
                f"{messaggio}\n\n{titolo} has not been deleted.\n\n"
                "To try again: gear icon on the unit's row → «Delete the unit»."
            )
        persistent_notification.async_create(
            self.hass,
            testo,
            title=intestazione,
            notification_id=f"{DOMAIN}_access_point_{entry_id}",
        )

    async def async_step_elimina_dalla_rete(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """La VMC lascia il Wi-Fi di casa (Access Point), poi si elimina la voce."""
        nuovo = self._task is None
        if nuovo:
            self._task = self._avvia_access_point()
        if nuovo or not self._task.done():
            return self.async_show_progress(
                step_id="elimina_dalla_rete",
                progress_action="access_point",
                progress_task=self._task,
                # la voce puo' essere gia' stata eliminata dal lavoro
                description_placeholders=self._segnaposto_eliminata,
            )
        task, self._task = self._task, None
        try:
            task.result()
        except pi.Failure as errore:
            self._errore = await async_messaggio_errore(self.hass, errore)
            return self.async_show_progress_done(next_step_id="errore_rete")
        return self.async_show_progress_done(next_step_id="eliminata_dalla_rete")

    async def async_step_eliminata_dalla_rete(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        # la voce e' gia' stata eliminata dal lavoro dell'Access Point
        return self.async_abort(
            reason="eliminata_dalla_rete", description_placeholders=self._segnaposto_eliminata
        )

    async def async_step_errore_rete(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Access Point non riuscito: la voce non e' stata eliminata."""
        return self.async_show_menu(
            step_id="errore_rete",
            menu_options=["elimina_dalla_rete", "elimina_solo_ha"],
            description_placeholders={**self._segnaposto(), "errore": self._errore},
        )
