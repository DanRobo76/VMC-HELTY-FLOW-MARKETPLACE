"""Letture periodiche della VMC, del ping e della versione su GitHub.

Ogni lettura del Package diventa un coordinatore di Home Assistant con lo stesso
intervallo e gli stessi istanti (``LetturaPeriodica``):

==========================  =============  ===========================================
Sensore del Package          Intervallo     Lettura
==========================  =============  ===========================================
sensor.status_ventola        5 s            VMGH? (stato di ventilazione)
sensor.sensori               1227 s         VMGI? (sensori della VMC)
sensor.nome                  43227 s        VMNM? (nome della VMC)
sensor.lan                   57641 s        VMSL? (dati di rete, password coperta)
sensor.status_ip             10 s           ping: 3 tentativi a 1 s, al massimo 4 s
sensor.versione_repository   86400 s        ultima release su GitHub
==========================  =============  ===========================================

Come nel Package, una lettura TCP non riuscita rende il sensore «non disponibile»,
il ping dà sempre ON-Line o OFF-Line, e la versione dà «Errore Connessione» quando
GitHub risponde senza tag_name (non disponibile se GitHub non risponde affatto); un
sensore non disponibile si riscrive a ogni lettura, come oggi.

Gli istanti sono quelli delle piattaforme di oggi, non quelli di ``DataUpdateCoordinator``
(che riparte dalla fine di ogni lettura, al secondo intero più uno scarto a caso): il
sensore tcp e il sensore rest si aggiornano col giro della loro piattaforma
(``EntityPlatform._async_handle_interval_callback``), il sensore command_line del ping
con ``async_track_time_interval``; in tutti e due il giro parte dopo la prima lettura
(l'aggiornamento prima dell'aggiunta, o quello in ``async_added_to_hass``), il prossimo
giro si programma all'inizio di quello attuale (``loop.call_at(loop.time() +
intervallo)``) e la lettura va in un compito in background, saltata (con un avviso) se
quella di prima non è finita. Ogni lettura riscrive il sensore (``LetturaPeriodica`` non
filtra i dati uguali), come l'aggiornamento di oggi.
"""

from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import Callable
from dataclasses import dataclass
from datetime import timedelta
from typing import Any

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import CALLBACK_TYPE, HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.debounce import Debouncer
from homeassistant.helpers.event import async_track_time_change
from homeassistant.helpers.script import CONFIGURATION_ERRORS
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .client import ClientVMC, ErroreVMC, maschera_lan
from .memoria import (
    GIORNI_STATISTICHE,
    STATISTICA_TEMPERATURA,
    STATISTICA_UMIDITA,
    calcola_medie,
)

_LOGGER = logging.getLogger(__name__)

ON_LINE = "ON-Line"
OFF_LINE = "OFF-Line"
ERRORE_CONNESSIONE = "Errore Connessione"
URL_VERSIONE = (
    "https://api.github.com/repos/DanRobo76/VMC-HELTY-FLOW-MARKETPLACE/releases/latest"
)
INTESTAZIONI_VERSIONE = {
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json",
    "User-Agent": "Home Assistant REST sensor",
}
ATTESA_VERSIONE = 30  # secondi, come timeout: 30 del sensore rest
PING_TENTATIVI = 3
PING_DURATA = 4  # secondi, come ping -w 4


@dataclass(frozen=True)
class Lettura:
    """Una lettura TCP periodica: chiave del sensore, richiesta, intervallo."""

    chiave: str
    richiesta: str
    intervallo: int
    trasforma: Callable[[str], str] | None = None


LETTURE_TCP: tuple[Lettura, ...] = (
    Lettura("sensor.status_ventola", "VMGH?", 5),
    Lettura("sensor.sensori", "VMGI?", 1227),
    Lettura("sensor.nome", "VMNM?", 43227),
    Lettura("sensor.lan", "VMSL?", 57641, maschera_lan),
)


def _rimbalzo(hass: HomeAssistant) -> Debouncer:
    """Nessuna pausa tra due richieste di lettura: le letture ravvicinate sono a 1 s."""
    return Debouncer(hass, _LOGGER, cooldown=0, immediate=True)


class LetturaPeriodica[T](DataUpdateCoordinator[T]):
    """Un coordinatore che si aggiorna agli istanti della piattaforma di oggi.

    Nessun ``update_interval`` di ``DataUpdateCoordinator``: il giro lo fa
    ``avvia_periodica``, da chiamare dopo la prima lettura.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry | None,
        nome: str,
        intervallo: float,
    ) -> None:
        """Prepara la lettura ``nome`` ogni ``intervallo`` secondi."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=nome,
            update_interval=None,
            request_refresh_debouncer=_rimbalzo(hass),
        )
        self.intervallo = intervallo
        self._prossimo: asyncio.TimerHandle | None = None
        self._in_corso: asyncio.Lock | None = None

    @callback
    def avvia_periodica(self) -> CALLBACK_TYPE:
        """Il giro delle letture da adesso (prima lettura già fatta); restituisce come
        fermarlo."""
        self._programma()
        return self.ferma_periodica

    @callback
    def ferma_periodica(self) -> None:
        """Ferma il giro delle letture."""
        if self._prossimo is not None:
            self._prossimo.cancel()
            self._prossimo = None

    def _programma(self) -> None:
        loop = self.hass.loop
        self._prossimo = loop.call_at(loop.time() + self.intervallo, self._scatta)

    @callback
    def _scatta(self) -> None:
        """Come ``_async_handle_interval_callback``: prima il prossimo giro, poi la lettura
        in un compito in background che parte subito."""
        self._programma()
        nome = f"{self.name} lettura periodica"
        if self.config_entry is not None:
            self.config_entry.async_create_background_task(
                self.hass, self._periodica(), name=nome, eager_start=True
            )
        else:
            self.hass.async_create_background_task(
                self._periodica(), name=nome, eager_start=True
            )

    async def async_refresh(self) -> None:
        """Una lettura, come ``DataUpdateCoordinator.async_refresh``; in più una lettura
        non riuscita dopo un'altra non riuscita avvisa comunque le entità, che
        ``DataUpdateCoordinator`` non avvisa: il sensore di oggi si riscrive a ogni
        lettura anche quando resta non disponibile (``state_reported``)."""
        riuscita_prima = self.last_update_success
        await super().async_refresh()
        if not riuscita_prima and not self.last_update_success:
            self.async_update_listeners()

    async def _periodica(self) -> None:
        """Una lettura del giro; saltata se quella di prima non è ancora finita."""
        await self.lettura_con_blocco()

    async def lettura_con_blocco(self) -> None:
        """Una lettura con il blocco del giro: saltata (con un avviso) se un'altra lettura
        con il blocco non è ancora finita (``_update_entity_state`` del sensore
        command_line di oggi, che fa così anche per ``update_entity``)."""
        if self._in_corso is None:
            self._in_corso = asyncio.Lock()
        if self._in_corso.locked():
            _LOGGER.warning(
                "Lettura %s più lunga dell'intervallo di %s s",
                self.name,
                self.intervallo,
            )
            return
        async with self._in_corso:
            await self.async_refresh()


class LetturaTCP(LetturaPeriodica[str]):
    """Legge periodicamente una risposta della VMC (stato, sensori, nome o rete)."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry | None,
        client: ClientVMC,
        lettura: Lettura,
    ) -> None:
        """Prepara la lettura con il suo intervallo."""
        super().__init__(
            hass,
            entry,
            f"VMC {lettura.richiesta} {client.host}",
            lettura.intervallo,
        )
        self.client = client
        self.lettura = lettura

    async def _async_update_data(self) -> str:
        """Una lettura: la risposta della VMC, o non disponibile se non risponde."""
        try:
            valore = await self.client.interroga(self.lettura.richiesta)
        except ErroreVMC as err:
            raise UpdateFailed(str(err)) from err
        if self.lettura.trasforma is not None:
            return self.lettura.trasforma(valore)
        return valore


async def _ping_icmp(host: str) -> bool:
    """Ping con icmplib senza privilegi: True se arriva almeno una risposta."""
    from icmplib import async_ping

    risultato = await async_ping(
        host, count=PING_TENTATIVI, interval=1, timeout=1, privileged=False
    )
    return risultato.packets_received > 0


async def _ping_comando(host: str) -> bool:
    """Ping con il comando di sistema (come il Package), se icmplib non ha i permessi."""
    processo = await asyncio.create_subprocess_exec(
        "ping",
        "-c",
        str(PING_TENTATIVI),
        "-W",
        "1",
        "-w",
        str(PING_DURATA),
        host,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL,
    )
    try:
        uscita, _ = await asyncio.wait_for(processo.communicate(), PING_DURATA + 6)
    except TimeoutError:
        processo.kill()
        await processo.wait()
        return False
    return b"bytes from" in uscita


async def raggiungibile(host: str) -> bool:
    """True se la VMC risponde al ping (protocollo ICMP, non la porta 5001)."""
    from icmplib.exceptions import ICMPLibError, SocketPermissionError

    try:
        async with asyncio.timeout(PING_DURATA + 1):
            return await _ping_icmp(host)
    except SocketPermissionError:
        pass
    except (ICMPLibError, OSError, TimeoutError, ValueError):
        return False
    try:
        return await _ping_comando(host)
    except OSError:
        return False


class LetturaPing(LetturaPeriodica[str]):
    """Raggiungibilità della VMC ogni 10 s: ON-Line o OFF-Line, mai non disponibile."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry | None,
        host: str,
        prova: Callable[[str], Any] = raggiungibile,
    ) -> None:
        """Prepara il ping verso ``host``."""
        super().__init__(hass, entry, f"VMC ping {host}", 10)
        self.host = host
        self._prova = prova

    async def aggiorna_per_entita(self) -> None:
        """``homeassistant.update_entity`` sul sensore: come il sensore command_line di
        oggi, una lettura con il blocco del giro (saltata se un'altra è in corso, e il giro
        saltato finché questa non finisce) che scrive il sensore; poi Home Assistant lo
        riscrive (due scritture, la seconda senza cambio)."""
        await self.lettura_con_blocco()

    async def _async_update_data(self) -> str:
        """Un ping: ON-Line se arriva almeno una risposta, altrimenti OFF-Line."""
        return ON_LINE if await self._prova(self.host) else OFF_LINE


def tag_versione(dati: Any) -> str:
    """Il tag dell'ultima release, o «Errore Connessione», come il value_template del Package."""
    if isinstance(dati, dict) and dati.get("tag_name"):
        return str(dati["tag_name"]).strip()
    return ERRORE_CONNESSIONE


class LetturaVersione(LetturaPeriodica[str]):
    """Versione dell'ultima release pubblicata, una volta al giorno."""

    def __init__(
        self, hass: HomeAssistant, entry: ConfigEntry | None, url: str = URL_VERSIONE
    ) -> None:
        """Prepara la lettura giornaliera della versione."""
        super().__init__(hass, entry, "VMC versione repository", 86400)
        self.url = url

    async def _async_update_data(self) -> str:
        """Il tag dell'ultima release; non disponibile se GitHub non risponde."""
        sessione = async_get_clientsession(self.hass)
        try:
            async with sessione.get(
                self.url,
                headers=INTESTAZIONI_VERSIONE,
                timeout=aiohttp.ClientTimeout(total=ATTESA_VERSIONE),
            ) as risposta:
                testo = await risposta.text()
        except (aiohttp.ClientError, TimeoutError) as err:
            raise UpdateFailed(f"GitHub non risponde: {err}") from err
        try:
            dati = json.loads(testo)
        except ValueError:
            dati = None
        return tag_versione(dati)


async def leggi_statistiche(hass: HomeAssistant, nome: str) -> dict[str, Any] | None:
    """Statistiche orarie (media) degli ultimi 84 giorni: la risposta di
    ``recorder.get_statistics``, chiamato come l'azione del Package (stessi dati, stesso
    evento ``call_service``).

    Come ``continue_on_error`` dell'azione: None se il servizio dà un errore di Home
    Assistant che l'azione salterebbe; con un errore che fermerebbe l'azione (registro
    assente, cioè servizio che non c'è, o un errore che non è di Home Assistant)
    ``UpdateFailed``: le medie non si scrivono, come oggi.
    """
    inizio = (dt_util.now() - timedelta(days=GIORNI_STATISTICHE)).replace(microsecond=0)
    dati = {
        "statistic_ids": [
            f"sensor.vmc_{nome}_{statistica}"
            for statistica in (STATISTICA_TEMPERATURA, STATISTICA_UMIDITA)
        ],
        "start_time": inizio.isoformat(),
        "period": "hour",
        "types": ["mean"],
    }
    try:
        return await hass.services.async_call(
            "recorder", "get_statistics", dati, blocking=True, return_response=True
        )
    except HomeAssistantError as err:
        if isinstance(err, CONFIGURATION_ERRORS):
            raise UpdateFailed(f"Statistiche per le medie non lette: {err}") from err
        _LOGGER.debug("Statistiche per le medie non lette", exc_info=True)
        return None
    except Exception as err:
        raise UpdateFailed(f"Statistiche per le medie non lette: {err}") from err


class LetturaMedie(DataUpdateCoordinator[dict[str, float | int | None]]):
    """Medie interne di 4, 8 e 12 settimane e giorni di dati: all'avvio e ogni ora al minuto 5."""

    def __init__(
        self, hass: HomeAssistant, entry: ConfigEntry | None, nome: str
    ) -> None:
        """Prepara il calcolo delle medie per la VMC ``nome``."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=f"VMC medie {nome}",
            update_interval=None,
            request_refresh_debouncer=_rimbalzo(hass),
        )
        self.nome = nome
        self._annulla: Callable[[], None] | None = None

    def avvia_orario(self) -> Callable[[], None]:
        """Ricalcola ogni ora al minuto 5 (time_pattern minutes: 5); restituisce come fermarlo."""

        async def al_minuto_5(_istante: Any) -> None:
            await self.async_refresh()

        self._annulla = async_track_time_change(
            self.hass, al_minuto_5, minute=5, second=0
        )
        return self._annulla

    async def _async_update_data(self) -> dict[str, float | int | None]:
        """Le 7 grandezze calcolate dalle statistiche (senza dati se non si leggono)."""
        risultato = await leggi_statistiche(self.hass, self.nome)
        return calcola_medie(risultato, dt_util.utcnow(), self.nome)
