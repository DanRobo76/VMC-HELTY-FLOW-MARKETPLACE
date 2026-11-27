"""Integrazione VMC Master per VMC Helty Flow Plus/Elite.

Ogni voce di configurazione e' una VMC (nome + IP). Per ogni VMC l'integrazione crea le
entita' native (impostazioni, sensori, pulsanti) e il motore che fa quello che faceva il
package della beta (nativa/assemblaggio.py), e serve la scheda «VMC Master», che si
aggiunge dalla plancia senza incollare codice. Nessun file in /config/packages.

Chi arriva dalla beta ha ancora il package scritto dalla beta: la VMC nativa parte dopo
che l'utente ha confermato la sua rimozione dalle Riparazioni (passaggio.py).
"""

from __future__ import annotations

import contextlib
import importlib
import logging
import re
import threading
from collections.abc import Mapping
from dataclasses import dataclass, field
from functools import lru_cache
from http import HTTPStatus
from pathlib import Path

# non «import time»: la piattaforma time.py, importata, diventa l'attributo «time» del
# pacchetto, cioè di questo modulo, e prenderebbe il posto del modulo time
from time import monotonic
from typing import Any, Final

import yaml
from aiohttp import web
from homeassistant.components import persistent_notification
from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import HomeAssistantView, StaticPathConfig
from homeassistant.components.lovelace import LOVELACE_DATA
from homeassistant.config_entries import ConfigEntry, ConfigEntryState
from homeassistant.const import Platform
from homeassistant.core import CALLBACK_TYPE, Event, HomeAssistant, callback
from homeassistant.helpers import (
    config_validation as cv,
)
from homeassistant.helpers import (
    entity_registry as er,
)
from homeassistant.helpers import (
    issue_registry as ir,
)
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import EntityPlatform
from homeassistant.helpers.event import async_call_later, async_track_state_change_event
from homeassistant.helpers.http import KEY_HASS
from homeassistant.helpers.start import async_at_started
from homeassistant.helpers.storage import Store
from homeassistant.helpers.typing import ConfigType
from homeassistant.loader import async_get_integration

from . import config_flow, passaggio, prima_installazione
from .const import (
    CONF_DA_INIZIALIZZARE,
    CONF_HOST,
    CONF_NOME,
    CONF_TITOLO,
    DOMAIN,
    FILE_SCHEDA,
    FILE_SCHEDA_JS,
    REPOSITORY,
    URL_FRONTEND,
    URL_REPOSITORY,
)
from .trasforma import adatta_link_repository, per_vmc

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

_CARTELLA = Path(__file__).parent

# Le piattaforme delle entita' native di una VMC (le entita' le aggiunge l'assemblaggio)
PIATTAFORME: Final = (
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.TEXT,
    Platform.TIME,
)
# Scheda della VMC nativa (scheda della beta tradotta con i nomi delle entita' native)
FILE_SCHEDA_NATIVA: Final = "scheda_nativa.txt"

ISSUE_RIAVVIO = "riavvio_necessario"
# Riparazione del Marketplace di Home Assistant che chiede il riavvio dopo un'installazione
# o un aggiornamento: quando c'e' lei, quella della VMC non serve (ne resta una sola)
DOMINIO_MARKETPLACE = "marketplace"
PREFISSO_RIAVVIO_MARKETPLACE = "restart_required_"
# Passaggio dalla beta: una riparazione per tutte le VMC con il package della beta
ISSUE_PASSAGGIO: Final = "passaggio_dalla_beta"
# Dopo il passaggio: dove l'utente usa ancora i vecchi nomi delle impostazioni
ISSUE_RINOMINATE: Final = "impostazioni_rinominate"
URL_NOMI_NATIVI: Final = f"{URL_REPOSITORY}/blob/main/NOMI_NATIVI.md"
# Installazione fatta a mano in /config/packages/vmc_helty_flow/<nome>: non si tocca
ISSUE_MANUALE: Final = "installazione_manuale"
# VMC eliminata con il package della beta ancora in /config/packages
ISSUE_RIMASTO: Final = "package_della_beta_rimasto"
DATI_IN_ATTESA: Final = f"{DOMAIN}_in_attesa"
# Errori dei sensori TCP con la VMC spenta: al massimo uno ogni 30 minuti per ogni VMC
LOGGER_TCP = "homeassistant.components.tcp.entity"
INTERVALLO_LOG_TCP = 30 * 60
DATI_FILTRO_TCP = f"{DOMAIN}_filtro_tcp"
# «Timeout for command» del ping delle VMC: nascosto solo nei primi 2 minuti dopo l'avvio
LOGGER_COMMAND_LINE = "homeassistant.components.command_line"
DURATA_FILTRO_PING = 120
DATI_FILTRO_PING = f"{DOMAIN}_filtro_ping"
_RE_IP_NEL_LOG = re.compile(
    r"(?<![0-9.])([0-9]{1,3}(?:\.[0-9]{1,3}){3})(?![0-9]|\.[0-9])"
)


@dataclass
class DatiVoce:
    """Cosa tiene una voce caricata (entry.runtime_data)."""

    situazione: str
    """passaggio.NATIVA, IN_ATTESA o MANUALE."""
    ip: str
    """L'IP con cui e' partita la VMC (la voce si ricarica se cambia)."""
    vmc: Any = None
    """La VMC nativa (VMCAssemblata), se e' partita."""
    piattaforme: dict[str, EntityPlatform] = field(default_factory=dict)
    """Le piattaforme della voce per dominio (le registra platform.py)."""


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Registra la scheda «VMC Master»: file JavaScript e configurazione per ogni VMC."""
    integrazione = await async_get_integration(hass, DOMAIN)
    await hass.http.async_register_static_paths(
        [StaticPathConfig(URL_FRONTEND, str(_CARTELLA / "frontend"), False)]
    )
    # Il numero di versione nell'indirizzo fa ricaricare la scheda dopo ogni aggiornamento
    await _registra_scheda(hass, str(integrazione.version))
    hass.http.register_view(VmcSchedaView())
    async_at_started(hass, _ripristina_wifi_server)
    await _async_togli_resti_della_beta(hass)
    if DATI_FILTRO_PING not in hass.data:
        filtro_ping = hass.data[DATI_FILTRO_PING] = _FiltroPingAvvio(hass)
        logging.getLogger(LOGGER_COMMAND_LINE).addFilter(filtro_ping)

    @callback
    def _riparazione_cambiata(evento: Event) -> None:
        # Il Marketplace chiede il riavvio dopo la VMC: si toglie quella della VMC
        if evento.data[
            "domain"
        ] == DOMINIO_MARKETPLACE and _riavvio_chiesto_dal_marketplace(hass):
            ir.async_delete_issue(hass, DOMAIN, ISSUE_RIAVVIO)

    hass.bus.async_listen(
        ir.EVENT_REPAIRS_ISSUE_REGISTRY_UPDATED, _riparazione_cambiata
    )
    return True


# Avvisi della beta che la versione nativa non crea più («voce_disabilitata_‹nome›» la
# beta lo salvava: resterebbe nelle Riparazioni senza testo) e l'elenco delle VMC
# eliminate della sua pulizia automatica del registro
_AVVISI_DELLA_BETA: Final = ("packages_non_abilitati", "voce_disabilitata_")
_ARCHIVIO_VMC_ELIMINATE_DELLA_BETA: Final = "vmc_master.vmc_eliminate"


async def _async_togli_resti_della_beta(hass: HomeAssistant) -> None:
    for dominio, issue_id in list(ir.async_get(hass).issues):
        if dominio == DOMAIN and issue_id.startswith(_AVVISI_DELLA_BETA):
            ir.async_delete_issue(hass, DOMAIN, issue_id)
    await Store(hass, 1, _ARCHIVIO_VMC_ELIMINATE_DELLA_BETA).async_remove()


# Il file JavaScript della scheda si serve dalla cartella dell'integrazione (URL_FRONTEND,
# percorso statico registrato in async_setup, prima che il server http accetti richieste):
# nessuna copia in /config. Lo caricano «extra_module_url» e la risorsa delle plance.
URL_SCHEDA: Final = f"{URL_FRONTEND}/{FILE_SCHEDA_JS}"
DATI_URL_SCHEDA: Final = f"{DOMAIN}_url_scheda"
# La beta copiava il file in <config>/www/vmc_master e la risorsa delle plance puntava a
# /local/vmc_master/...: finche' una VMC aspetta il passaggio copia e risorsa restano come
# le ha lasciate la beta; con il passaggio confermato la risorsa passa all'indirizzo
# dell'integrazione e la copia si toglie, come la cartella del package.
CARTELLA_WWW_DELLA_BETA: Final = "vmc_master"
URL_LOCALE_DELLA_BETA: Final = f"/local/{CARTELLA_WWW_DELLA_BETA}/{FILE_SCHEDA_JS}"


async def _risorse_plance(hass: HomeAssistant) -> Any | None:
    """Le risorse delle plance, se sono in modalita' storage (caricate); altrimenti None
    (in modalita' YAML le risorse le scrive l'utente)."""
    dati = hass.data.get(LOVELACE_DATA)
    if dati is None or getattr(dati, "resource_mode", None) != "storage":
        return None
    await dati.resources.async_get_info()  # carica le risorse salvate
    return dati.resources


def _indirizzo(voce: Mapping[str, Any]) -> str:
    return str(voce.get("url", "")).split("?", 1)[0]


async def _registra_risorsa_plancia(
    hass: HomeAssistant, url: str, *, anche_della_beta: bool = False
) -> None:
    """Una sola risorsa «module» della scheda con l'indirizzo ``url`` (versione
    installata). Una risorsa della beta (/local/vmc_master/...) resta com'e', se non con
    ``anche_della_beta`` (passaggio confermato): allora diventa questa, stessa voce."""
    risorse = await _risorse_plance(hass)
    if risorse is None:
        return
    della_beta = [
        voce
        for voce in risorse.async_items()
        if _indirizzo(voce) == URL_LOCALE_DELLA_BETA
    ]
    if della_beta and not anche_della_beta:
        return
    nostre = della_beta + [
        voce for voce in risorse.async_items() if _indirizzo(voce) == URL_SCHEDA
    ]
    if not nostre:
        await risorse.async_create_item({"res_type": "module", "url": url})
        return
    if nostre[0].get("url") != url or nostre[0].get("type") != "module":
        await risorse.async_update_item(
            nostre[0]["id"], {"res_type": "module", "url": url}
        )
    for doppia in nostre[1:]:
        await risorse.async_delete_item(doppia["id"])


def _togli_copia_della_beta(config_dir: str) -> None:
    """Toglie la copia della scheda che la beta scriveva in www/vmc_master; la cartella
    solo se resta vuota (altri file dell'utente restano)."""
    cartella = Path(config_dir) / "www" / CARTELLA_WWW_DELLA_BETA
    for nome_file in (FILE_SCHEDA_JS, f"{Path(FILE_SCHEDA_JS).stem}.tmp"):
        (cartella / nome_file).unlink(missing_ok=True)
    with contextlib.suppress(OSError):
        cartella.rmdir()


async def _scheda_dopo_il_passaggio(hass: HomeAssistant) -> None:
    """Passaggio confermato: la risorsa della beta passa all'indirizzo dell'integrazione e
    la copia della beta in www si toglie."""
    try:
        await _registra_risorsa_plancia(
            hass, hass.data[DATI_URL_SCHEDA], anche_della_beta=True
        )
        await hass.async_add_executor_job(
            _togli_copia_della_beta, hass.config.config_dir
        )
    except Exception:
        _LOGGER.exception("Scheda della beta non tolta da www o dalle risorse")


async def _togli_risorse_plancia(hass: HomeAssistant) -> None:
    """Ultima VMC eliminata: via le risorse della scheda (della beta e nativa). In /config
    non si tocca nulla."""
    try:
        risorse = await _risorse_plance(hass)
        for voce in list(risorse.async_items()) if risorse is not None else ():
            if _indirizzo(voce) in (URL_SCHEDA, URL_LOCALE_DELLA_BETA):
                await risorse.async_delete_item(voce["id"])
    except Exception:
        _LOGGER.exception("Scheda VMC Master non tolta dalle risorse delle plance")


async def _registra_scheda(hass: HomeAssistant, versione: str) -> None:
    """File JavaScript della scheda per il frontend: «extra_module_url» e risorsa delle
    plance con l'indirizzo dell'integrazione (la risorsa della beta resta fino al
    passaggio confermato)."""
    url = hass.data[DATI_URL_SCHEDA] = f"{URL_SCHEDA}?v={versione}"
    add_extra_js_url(hass, url)
    try:
        await _registra_risorsa_plancia(hass, url)
    except Exception:
        _LOGGER.exception(
            "Risorsa della plancia per la scheda VMC Master non registrata"
        )


def _italiano(hass: HomeAssistant) -> bool:
    """Notifiche in italiano se Home Assistant e' in italiano, altrimenti in inglese."""
    return (hass.config.language or "").lower().startswith("it")


async def _ripristina_wifi_server(hass: HomeAssistant) -> None:
    """Home Assistant riavviato durante il collegamento di una VMC al Wi-Fi: il Wi-Fi
    del server si riporta alla rete di prima (come faceva l'avvio della Finestra
    Prima Installazione VMC della release 8.6.0)."""
    config_dir = hass.config.config_dir
    if not await hass.async_add_executor_job(
        prima_installazione.ripristino_in_sospeso, config_dir
    ):
        return
    try:
        await hass.async_add_executor_job(
            prima_installazione.esegui, config_dir, "recover"
        )
    except prima_installazione.Failure as errore:
        _LOGGER.warning(
            "Ripristino del Wi-Fi del server non riuscito: %s", errore.message
        )
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
    """Avvia la VMC nativa; con il package della beta ancora presente aspetta la conferma
    del passaggio (la VMC continua con il package)."""
    nome: str = entry.data[CONF_NOME]
    dati = entry.runtime_data = DatiVoce(passaggio.NATIVA, entry.data[CONF_HOST])
    _installa_filtro_tcp(hass)
    _aggiorna_titolo_dopo_avvio(hass, entry)
    entry.async_on_unload(entry.add_update_listener(_async_aggiornata))
    ir.async_delete_issue(hass, DOMAIN, f"{ISSUE_RIMASTO}_{nome}")
    dati.situazione = await _async_situazione(hass, nome)
    if dati.situazione == passaggio.MANUALE:
        ir.async_create_issue(
            hass,
            DOMAIN,
            f"{ISSUE_MANUALE}_{nome}",
            is_fixable=False,
            is_persistent=False,
            severity=ir.IssueSeverity.ERROR,
            translation_key=ISSUE_MANUALE,
            translation_placeholders={"nome": nome},
        )
        return True
    ir.async_delete_issue(hass, DOMAIN, f"{ISSUE_MANUALE}_{nome}")
    if dati.situazione == passaggio.IN_ATTESA:
        _aspetta_il_passaggio(hass, entry)
        return True
    await _async_avvia_nativa(hass, entry)
    return True


async def _async_situazione(hass: HomeAssistant, nome: str) -> str:
    """NATIVA, IN_ATTESA (cartella della beta, o suoi elementi ancora nel registro) o
    MANUALE (cartella senza il marcatore della beta)."""
    config_dir = hass.config.config_dir
    cartella = await hass.async_add_executor_job(
        passaggio.esamina_cartella, config_dir, nome
    )
    if cartella == "manuale":
        return passaggio.MANUALE
    if cartella == "beta":
        return passaggio.IN_ATTESA
    if passaggio.possibili_voci_della_beta(hass, nome):
        id_package = await hass.async_add_executor_job(
            passaggio.id_del_package, config_dir, nome
        )
        if passaggio.voci_del_package(hass, id_package, anche_automazioni=False):
            return passaggio.IN_ATTESA
    return passaggio.NATIVA


@callback
def _aspetta_il_passaggio(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Package della beta ancora presente: ad avvio finito (aiutanti del package tutti
    caricati) si leggono e si salvano i suoi valori, poi la riparazione chiede la conferma."""
    nome: str = entry.data[CONF_NOME]
    in_attesa: dict[str, str] = hass.data.setdefault(DATI_IN_ATTESA, {})
    in_attesa[nome] = entry.entry_id

    @callback
    def _non_piu_in_attesa() -> None:
        if in_attesa.get(nome) == entry.entry_id:
            del in_attesa[nome]
            segnala_passaggio(hass)

    entry.async_on_unload(_non_piu_in_attesa)

    async def _leggi() -> None:
        letti = passaggio.leggi_valori(hass, nome)
        await passaggio.async_salva_letti(hass, nome, letti)
        segnala_passaggio(hass)

    @callback
    def _avviato(_hass: HomeAssistant) -> None:
        entry.async_create_background_task(hass, _leggi(), f"{DOMAIN}_passaggio_{nome}")

    entry.async_on_unload(async_at_started(hass, _avviato))


@callback
def segnala_passaggio(hass: HomeAssistant) -> None:
    """Una riparazione per tutte le VMC in attesa del passaggio (nessuna: la si toglie)."""
    in_attesa: dict[str, str] = hass.data.get(DATI_IN_ATTESA, {})
    if not in_attesa:
        ir.async_delete_issue(hass, DOMAIN, ISSUE_PASSAGGIO)
        return
    elenco = "\n".join(
        f"- `/config/packages/vmc_helty_flow/{nome}`" for nome in sorted(in_attesa)
    )
    ir.async_create_issue(
        hass,
        DOMAIN,
        ISSUE_PASSAGGIO,
        is_fixable=True,
        is_persistent=False,
        severity=ir.IssueSeverity.WARNING,
        translation_key=ISSUE_PASSAGGIO,
        translation_placeholders={"elenco": elenco},
    )


async def async_conferma_passaggio(
    hass: HomeAssistant,
) -> list[passaggio.EsitoConferma]:
    """Il passaggio confermato dall'utente per tutte le VMC in attesa (la riparazione, o le
    prove, chiamano questo). Se un package era caricato chiede il riavvio; altrimenti le
    VMC ripartono subito, native."""
    tutte: dict[str, str] = hass.data.get(DATI_IN_ATTESA, {})
    in_attesa = dict(tutte)
    esiti = [await passaggio.async_conferma(hass, nome) for nome in sorted(in_attesa)]
    for esito in esiti:
        if esito.errore is None:
            tutte.pop(esito.nome, None)
    segnala_passaggio(hass)
    if any(esito.errore is None for esito in esiti):
        await _scheda_dopo_il_passaggio(hass)
    riferimenti = [r for esito in esiti for r in esito.riferimenti]
    if riferimenti:
        ir.async_create_issue(
            hass,
            DOMAIN,
            ISSUE_RINOMINATE,
            is_fixable=True,
            is_persistent=True,
            # l'elenco completo dei nomi vecchi e nuovi (NOMI_NATIVI.md, guida)
            learn_more_url=URL_NOMI_NATIVI,
            severity=ir.IssueSeverity.WARNING,
            translation_key=ISSUE_RINOMINATE,
            translation_placeholders={
                "elenco": "\n".join(
                    f"- {dove}: `{vecchio}` → `{nuovo or '-'}`"
                    for dove, vecchio, nuovo in riferimenti
                )
            },
        )
    if any(esito.riavvio for esito in esiti):
        _segnala_riavvio(hass)
    else:
        for nome, entry_id in in_attesa.items():
            if not any(e.nome == nome and e.errore for e in esiti):
                hass.config_entries.async_schedule_reload(entry_id)
    return esiti


def _importa_motore() -> None:
    """Il motore e il codice tradotto (moduli grandi: secondi di importazione)."""
    from .nativa import assemblaggio  # nell'esecutore delle importazioni

    importlib.import_module(assemblaggio.CODICE_FASE4)
    importlib.import_module(assemblaggio.CODICE_SENSORI)


async def _async_avvia_nativa(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """La VMC nativa della voce: piattaforme, poi tutte le parti nell'ordine
    dell'assemblaggio. Dopo il passaggio dalla beta parte con i valori della beta."""
    # il motore si carica solo qui, nell'esecutore delle importazioni di Home Assistant:
    # nel ciclo degli eventi lo bloccherebbe (Home Assistant lo segnala nel registro)
    await hass.async_add_import_executor_job(_importa_motore)
    from .nativa.assemblaggio import VMCAssemblata  # già importato: nessuna attesa

    dati: DatiVoce = entry.runtime_data
    nome: str = entry.data[CONF_NOME]
    riaggiunta = await passaggio.async_memoria_di_una_vmc_eliminata(hass, nome)
    archivio = await passaggio.archivio(hass, nome).async_load() or {}
    vmc = VMCAssemblata(hass, nome, dati.ip)
    confermato = archivio.get("stato") == passaggio.CONFERMATO
    if confermato:
        vmc.stato.passati = passaggio.valori_passati(archivio, nome)
    dati.vmc = vmc
    _togli_entita_tolte(hass, entry)
    await hass.config_entries.async_forward_entry_setups(entry, PIATTAFORME)

    async def aggiungi(dominio: str, entita: list[Entity]) -> None:
        await dati.piattaforme[dominio].async_add_entities(entita)

    try:
        await vmc.avvia(aggiungi)
    except BaseException:
        await _async_ferma_nativa(hass, entry)
        raise
    _lega_automazioni_alla_voce(hass, entry, vmc)
    if entry.data.get(CONF_DA_INIZIALIZZARE):
        if riaggiunta or confermato:
            # VMC riaggiunta con la sua memoria, o passata dalla beta: tiene i suoi valori
            _inizializzata(hass, entry)
        else:
            entry.async_on_unload(_inizializza_una_volta(hass, entry, vmc))
    if confermato:

        @callback
        def _avviato(_hass: HomeAssistant) -> None:
            # Home Assistant conserva gli stati delle entita' native appena avviato
            entry.async_create_background_task(
                hass,
                passaggio.async_applicato(hass, nome, archivio),
                f"{DOMAIN}_applicato_{nome}",
            )

        entry.async_on_unload(async_at_started(hass, _avviato))


# Le entità della b44 e della b45 che la VMC non ha più dalla b46 (il campo «Cambia IP
# VMC» della scheda, il sensore che lo controllava e l'automazione che cambiava l'IP e
# riavviava Home Assistant: l'IP si cambia dall'ingranaggio della VMC). Dominio,
# piattaforma e unique_id senza «vmc_‹nome›_».
ENTITA_TOLTE: Final = (
    ("text", DOMAIN, "ip_insert"),
    ("sensor", DOMAIN, "verifica_ip_inserito"),
    ("automation", "automation", "cambio_ip_vmc"),
)


@callback
def _togli_entita_tolte(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Toglie dal registro le entità tolte (``ENTITA_TOLTE``) rimaste legate alla voce:
    nessuno le aggiunge più, resterebbero «non disponibili». Quelle non legate alla voce
    non sono della VMC: restano."""
    registro = er.async_get(hass)
    nome = entry.data[CONF_NOME]
    for dominio, piattaforma, oggetto in ENTITA_TOLTE:
        entity_id = registro.async_get_entity_id(
            dominio, piattaforma, f"vmc_{nome}_{oggetto}"
        )
        if (
            entity_id is not None
            and registro.entities[entity_id].config_entry_id == entry.entry_id
        ):
            registro.async_remove(entity_id)


# Il Profilo Inizializzazione automatico di una VMC nuova parte dopo i 140 s dell'avvio
# (come la riattivazione di tutte le allerte dopo un riavvio di Home Assistant)
ATTESA_INIZIALIZZAZIONE: Final = 140


@callback
def _inizializzata(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """La voce non chiede piu' il Profilo Inizializzazione automatico."""
    hass.config_entries.async_update_entry(
        entry,
        data={k: v for k, v in entry.data.items() if k != CONF_DA_INIZIALIZZARE},
    )


@callback
def _inizializza_una_volta(
    hass: HomeAssistant, entry: ConfigEntry, vmc: Any
) -> CALLBACK_TYPE:
    """Profilo Inizializzazione automatico, una sola volta per una VMC aggiunta per la
    prima volta: dopo i 140 s dell'avvio, appena la VMC e' ON-Line (se e' spenta aspetta
    che si accenda). Come il pulsante della scheda; poi la voce non lo chiede piu', anche
    dopo un riavvio di Home Assistant. Se Home Assistant si ferma prima, riparte al
    prossimo avvio."""
    nome = entry.data[CONF_NOME]
    registro = er.async_get(hass)
    stato_vmc = registro.async_get_entity_id(
        "sensor", DOMAIN, f"vmc_{nome}_status_ip_interfaccia"
    ) or f"sensor.vmc_{nome}_status_ip_interfaccia"
    pulsante = next(
        p for p in vmc.pulsanti if p.unique_id == f"vmc_{nome}_profilo_inizializzazione"
    )
    annulla: list[CALLBACK_TYPE] = []

    @callback
    def _ferma() -> None:
        while annulla:
            annulla.pop()()

    @callback
    def _prova(_evento: Event | None = None) -> None:
        if not hass.states.is_state(stato_vmc, "ON-Line"):
            return
        _ferma()
        _inizializzata(hass, entry)
        _LOGGER.info("VMC %s: Profilo Inizializzazione automatico (VMC nuova)", nome)
        entry.async_create_background_task(
            hass, pulsante.async_press(), f"{DOMAIN}_inizializzazione_{nome}"
        )

    @callback
    def _dopo_l_avvio(_ora: Any) -> None:
        annulla.clear()  # l'attesa e' finita
        annulla.append(async_track_state_change_event(hass, [stato_vmc], _prova))
        _prova()

    annulla.append(async_call_later(hass, ATTESA_INIZIALIZZAZIONE, _dopo_l_avvio))
    return _ferma


@callback
def _lega_automazioni_alla_voce(
    hass: HomeAssistant, entry: ConfigEntry, vmc: Any
) -> None:
    """Le automazioni del motore sono entita' del componente automation (stesso
    unique_id, quindi stessa voce del registro, delle automazioni della beta: area,
    etichette e categoria dell'utente restano). La loro voce del registro si lega alla
    voce della VMC, cosi' Home Assistant le toglie quando la VMC si elimina (e le
    disabilita con lei). Il componente automation, quando la aggiunge, toglie il legame
    (piattaforma senza voce): si rimette dopo ogni avvio."""
    registro = er.async_get(hass)
    # anche quelle disattivate dall'utente (voce del registro senza entita')
    registrate = [
        a.entity_id for a in vmc.motore.automazioni if a.entity_id in registro.entities
    ]
    for entity_id in registrate:  # gia' legata: nessun cambio (async_update_entity)
        registro.async_update_entity(entity_id, config_entry_id=entry.entry_id)


async def _async_ferma_nativa(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Ferma la VMC nativa e toglie le sue entita' (le automazioni del motore sono nel
    componente automation: si tolgono da li', la voce del registro resta)."""
    dati: DatiVoce = entry.runtime_data
    vmc, dati.vmc = dati.vmc, None
    if vmc is None:
        return True
    # i valori interni di adesso (una ricarica non perde gli ultimi cambi)
    await vmc.memoria.async_salva()
    await vmc.ferma()
    for automazione in list(vmc.motore.automazioni):
        if automazione.hass is not None:
            await automazione.async_remove()
    caricate = [p for p in PIATTAFORME if p in dati.piattaforme]
    return await hass.config_entries.async_unload_platforms(entry, caricate)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Ferma la VMC nativa (niente da fermare se aspetta il passaggio: il package della
    beta resta caricato fino al riavvio)."""
    if not any(
        voce.state is ConfigEntryState.LOADED
        for voce in hass.config_entries.async_entries(DOMAIN)
        if voce.entry_id != entry.entry_id
    ):
        _togli_filtro_tcp(hass)  # ultima VMC scaricata
    else:
        _aggiorna_ip_filtro_tcp(hass)
    return await _async_ferma_nativa(hass, entry)


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """VMC eliminata: le sue entita' native le toglie Home Assistant con la voce; qui si
    tolgono i suoi archivi e i suoi avvisi. Il registro delle entita' e /config non si
    toccano: se c'e' ancora il package della beta lo dice un avviso."""
    nome = entry.data[CONF_NOME]
    if not any(
        voce.entry_id != entry.entry_id
        for voce in hass.config_entries.async_entries(DOMAIN)
    ):
        await _togli_risorse_plancia(hass)  # ultima VMC: la scheda non serve piu'
    ir.async_delete_issue(hass, DOMAIN, f"{ISSUE_MANUALE}_{nome}")
    await passaggio.async_togli_archivi(hass, nome)
    if (
        await hass.async_add_executor_job(
            passaggio.esamina_cartella, hass.config.config_dir, nome
        )
        == "beta"
    ):
        ir.async_create_issue(
            hass,
            DOMAIN,
            f"{ISSUE_RIMASTO}_{nome}",
            is_fixable=False,
            is_persistent=True,
            severity=ir.IssueSeverity.WARNING,
            translation_key=ISSUE_RIMASTO,
            translation_placeholders={"nome": nome},
        )


async def _async_aggiornata(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """IP cambiato dall'ingranaggio: la VMC riparte con il nuovo IP. Il solo titolo non
    serve."""
    _aggiorna_ip_filtro_tcp(hass)
    dati: DatiVoce = entry.runtime_data
    if entry.data[CONF_HOST] == dati.ip:
        return
    await hass.config_entries.async_reload(entry.entry_id)


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
        self._ora = monotonic

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


class _FiltroPingAvvio(logging.Filter):
    """All'avvio Home Assistant e' carico e il ping delle VMC puo' superare il suo tempo
    massimo: «Timeout for command: ping … ‹IP›» compare una volta per VMC. Per gli IP delle
    VMC il messaggio si nasconde solo nei primi 2 minuti dall'avvio; dopo, e per tutti gli
    altri comandi, passa sempre. Ping, tempi e intervalli dei sensori non cambiano."""

    def __init__(self, hass: HomeAssistant) -> None:
        super().__init__()
        self._hass = hass
        self._ora = monotonic
        self._fine = self._ora() + DURATA_FILTRO_PING

    def filter(self, record: logging.LogRecord) -> bool:
        if self._ora() >= self._fine:
            return True
        try:
            messaggio = record.getMessage()
        except Exception:  # noqa: BLE001 - messaggio non formattabile: passa com'e'
            return True
        if not messaggio.startswith("Timeout for command: ping "):
            return True
        ips = {
            voce.data.get(CONF_HOST)
            for voce in self._hass.config_entries.async_entries(DOMAIN)
        }
        return not any(t in ips for t in _RE_IP_NEL_LOG.findall(messaggio))


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
        entry.async_create_background_task(
            hass, _aggiorna(), f"{DOMAIN}_titolo_{entry.entry_id}"
        )

    entry.async_on_unload(async_at_started(hass, _avvia))


@callback
def _riavvio_chiesto_dal_marketplace(hass: HomeAssistant) -> bool:
    """Il Marketplace ha gia' la sua riparazione «Restart required» per questa integrazione."""
    return any(
        dominio == DOMINIO_MARKETPLACE
        and issue_id.startswith(PREFISSO_RIAVVIO_MARKETPLACE)
        and issue.issue_domain == DOMAIN
        and issue.active
        for (dominio, issue_id), issue in ir.async_get(hass).issues.items()
    )


@callback
def _segnala_riavvio(hass: HomeAssistant) -> None:
    """Chiede il riavvio con una riparazione, se non lo chiede gia' il Marketplace."""
    if _riavvio_chiesto_dal_marketplace(hass):
        return
    ir.async_create_issue(
        hass,
        DOMAIN,
        ISSUE_RIAVVIO,
        is_fixable=True,
        is_persistent=False,
        severity=ir.IssueSeverity.WARNING,
        translation_key=ISSUE_RIAVVIO,
    )
    # Un «Ignora» di una volta resterebbe valido anche per i riavvii chiesti dopo (HA
    # ricorda la scelta fino al suo prossimo aggiornamento): ogni nuova richiesta si vede
    ir.async_ignore_issue(hass, DOMAIN, ISSUE_RIAVVIO, False)


@lru_cache(maxsize=2)
def _leggi_scheda(file: str) -> str:
    # newline="" mantiene i CRLF del file
    with open(_CARTELLA / file, encoding="utf-8", newline="") as testo:
        return testo.read()


@lru_cache(maxsize=32)
def _configurazione_scheda(nome: str, ip: str, nativa: bool = True) -> dict[str, Any]:
    """La scheda della VMC: quella nativa, oppure quella della beta finche' la VMC aspetta
    il passaggio (le entita' sono ancora quelle del package)."""
    file = f"nativa/{FILE_SCHEDA_NATIVA}" if nativa else f"package/{FILE_SCHEDA}"
    return yaml.safe_load(
        adatta_link_repository(per_vmc(_leggi_scheda(file), nome, ip), REPOSITORY)
    )


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
            return self.json_message("VMC disabilitata", HTTPStatus.CONFLICT)
        dati = getattr(voce, "runtime_data", None)
        nativa = not (
            isinstance(dati, DatiVoce) and dati.situazione != passaggio.NATIVA
        )
        configurazione = await hass.async_add_executor_job(
            _configurazione_scheda, voce.data[CONF_NOME], voce.data[CONF_HOST], nativa
        )
        return self.json(configurazione)
