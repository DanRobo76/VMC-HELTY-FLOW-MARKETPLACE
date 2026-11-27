"""Una VMC nell'integrazione nativa: letture, sensori con memoria e stato.

Collega i coordinatori (letture TCP, ping, versione, medie) a StatoVMC come facevano i
sensori tcp/ping/rest e i sensori a trigger del package:

- ogni lettura scrive il suo sensore (non disponibile se la VMC non risponde), agli
  istanti della piattaforma di oggi (letture.LetturaPeriodica); StatoVMC segue lo stato
  del sensore (``async_track_state_change_event``, come i template di oggi seguono il
  sensore tcp: nello stesso evento, prima delle automazioni che si iscrivono dopo), con il
  contesto del suo cambio;
- quando una lettura cambia verso un valore valido, la sua «ultima lettura valida» si
  aggiorna (trigger di stato); all'avvio di Home Assistant si aggiorna con la regola
  di avvio (trigger homeassistant start), partendo dall'ultimo stato conservato;
- le medie e i giorni di dati arrivano dalle statistiche all'avvio e ogni ora al minuto 5.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import partial
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STARTED
from homeassistant.core import (
    CALLBACK_TYPE,
    Context,
    CoreState,
    Event,
    EventStateChangedData,
    HomeAssistant,
    callback,
)
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.restore_state import async_get as restore_state

from .client import ClientVMC
from .letture import (
    LETTURE_TCP,
    LetturaMedie,
    LetturaPeriodica,
    LetturaPing,
    LetturaTCP,
    LetturaVersione,
)
from .memoria import (
    GIORNI_DATI,
    MEDIE,
    TRIGGER_AVVIO,
    TRIGGER_STATO,
    come_stato,
    lettura_prima_dell_interruzione,
    memorizzata,
)
from .stato import NON_DISPONIBILE, SCONOSCIUTO, StatoVMC

ATTRIBUTO_INTERRUZIONE = "lettura_prima_dell_interruzione"
# lettura -> sua «ultima lettura valida» (solo stato ventola, sensori e nome ne hanno una)
MEMORIZZATE = {
    "sensor.status_ventola": "sensor.status_ventola_memorizzata",
    "sensor.sensori": "sensor.sensori_memorizzata",
    "sensor.nome": "sensor.nome_memorizzata",
}
CHIAVE_PING = "sensor.status_ip"
CHIAVE_VERSIONE = "sensor.versione_repository"


def _testo(valore: Any) -> str:
    """Valore calcolato -> stato (None = unknown)."""
    return SCONOSCIUTO if valore is None else str(valore)


class VMCNativa:
    """Letture e stato di una VMC."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry | None,
        nome: str,
        host: str,
        *,
        client: ClientVMC | None = None,
        prova_ping: Callable[[str], Any] | None = None,
        versione: bool = True,
    ) -> None:
        """Prepara stato e coordinatori della VMC ``nome`` all'indirizzo ``host``.

        Con ``versione`` False non c'è la lettura della versione su GitHub (il simulatore
        non va in rete): la chiave della versione resta senza valore, come un sensore
        che non esiste.
        """
        self.hass = hass
        self.nome = nome
        self.stato = StatoVMC(hass, nome, host)
        self.client = client or ClientVMC(host)
        self.letture = {
            lettura.chiave: LetturaTCP(hass, entry, self.client, lettura)
            for lettura in LETTURE_TCP
        }
        self.ping = (
            LetturaPing(hass, entry, host)
            if prova_ping is None
            else LetturaPing(hass, entry, host, prova_ping)
        )
        self.versione = LetturaVersione(hass, entry) if versione else None
        self.medie = LetturaMedie(hass, entry, nome)
        self._annulla: list[CALLBACK_TYPE] = []
        self._trigger_attivi = False
        self._annulla_via: CALLBACK_TYPE | None = None

    def letture_dei_sensori(self) -> dict[str, LetturaPeriodica[str]]:
        """I sensori delle letture (chiave -> coordinatore): letture TCP, ping, versione."""
        letture: dict[str, LetturaPeriodica[str]] = dict(self.letture)
        letture[CHIAVE_PING] = self.ping
        if self.versione is not None:
            letture[CHIAVE_VERSIONE] = self.versione
        return letture

    async def avvia(self) -> None:
        """Ripristina i sensori con memoria, fa le prime letture e collega tutto allo stato.

        Come i sensori a trigger di oggi, «ultima lettura valida» e medie si attivano
        all'avvio di Home Assistant (evento start: da lì seguono le letture e il minuto 5) e
        la regola di avvio, con il calcolo delle medie, vale quando l'avvio è finito (evento
        started, come il trigger ``homeassistant: start``). A una ricarica (Home Assistant
        già avviato) si attivano subito, senza regola di avvio e senza calcolo delle medie
        fino al minuto 5.
        """
        self._ripristina()
        letture = self.letture_dei_sensori()
        # la versione si segue anche senza la sua lettura (chi la scrive al suo posto)
        chiavi = {
            self.stato.entity_id(chiave): chiave
            for chiave in (*letture, CHIAVE_VERSIONE)
        }
        self._annulla.append(
            async_track_state_change_event(
                self.hass, list(chiavi), callback(partial(self._letta, chiavi))
            )
        )
        for coordinatore in letture.values():
            await coordinatore.async_refresh()
            self._annulla.append(coordinatore.avvia_periodica())
        self._annulla.append(self.medie.async_add_listener(self._medie))
        self.stato.avvia()
        if self.hass.state is CoreState.running:
            self._attiva_trigger()
        else:
            self._annulla_via = self.hass.bus.async_listen_once(
                EVENT_HOMEASSISTANT_START, self._al_via
            )

    @callback
    def _al_via(self, _evento: Event) -> None:
        """Avvio di Home Assistant: come i blocchi a trigger di oggi, che qui agganciano i
        loro trigger (``homeassistant: start`` aspetta la fine dell'avvio)."""
        self._attiva_trigger()
        self._annulla_via = self.hass.bus.async_listen_once(
            EVENT_HOMEASSISTANT_STARTED, self._avviato
        )

    async def _avviato(self, _evento: Event) -> None:
        """Avvio finito: regola di avvio delle letture memorizzate, poi le medie."""
        self._annulla_via = None
        for chiave, memoria in MEMORIZZATE.items():
            self._aggiorna_memorizzata(chiave, memoria, TRIGGER_AVVIO, None, None)
        await self.medie.async_refresh()

    @callback
    def _attiva_trigger(self) -> None:
        """Le letture memorizzate seguono le letture; le medie si ricalcolano al minuto 5."""
        self._trigger_attivi = True
        self._annulla.append(self.medie.avvia_orario())

    @callback
    def ferma(self) -> None:
        """Ferma letture, ricalcoli e ascolti."""
        if self._annulla_via is not None:
            self._annulla_via()
            self._annulla_via = None
        for annulla in self._annulla:
            annulla()
        self._annulla.clear()
        self.stato.ferma()

    def _ripristina(self) -> None:
        """Ultimo stato conservato dei sensori con memoria (come i sensori a trigger di oggi);
        senza, il valore passato dalla beta (``StatoVMC.passati``).

        La memoria del ripristino di Home Assistant 2026.11 è per voce del registro delle
        entità (``async_get_stored_state`` la cerca per entity_id, prima o dopo la
        registrazione dell'entità)."""
        conservati = restore_state(self.hass)
        valori: dict[str, tuple[str, dict[str, Any]]] = {}
        for chiave in (*MEMORIZZATE.values(), *(k for k, _, _ in MEDIE), GIORNI_DATI):
            conservato = conservati.async_get_stored_state(self.stato.entity_id(chiave))
            # prima partenza dopo il passaggio dalla beta: lo stato del sensore della beta
            stato = (
                self.stato.passati.get(chiave)
                if conservato is None
                else conservato.state
            )
            if stato is None:
                continue
            attributi = {}
            if ATTRIBUTO_INTERRUZIONE in stato.attributes:
                attributi[ATTRIBUTO_INTERRUZIONE] = stato.attributes[
                    ATTRIBUTO_INTERRUZIONE
                ]
            valori[chiave] = (stato.state, attributi)
        if valori:
            self.stato.imposta(valori)

    @callback
    def _letta(
        self, chiavi: dict[str, str], evento: Event[EventStateChangedData]
    ) -> None:
        """Il sensore di una lettura ha cambiato stato: la sua chiave e, se serve, la sua
        ultima lettura valida (trigger di stato), con il contesto del cambio."""
        nuovo = evento.data["new_state"]
        if nuovo is None:
            return
        chiave = chiavi[evento.data["entity_id"]]
        nuova = nuovo.state
        precedente = self.stato.stato(chiave)
        if nuova == precedente:
            return
        self.stato.imposta({chiave: nuova}, evento.context)
        memoria = MEMORIZZATE.get(chiave)
        if (
            not self._trigger_attivi
            or memoria is None
            or nuova in (NON_DISPONIBILE, SCONOSCIUTO)
        ):
            return
        self._aggiorna_memorizzata(
            chiave, memoria, TRIGGER_STATO, nuova, precedente, evento.context
        )

    def _aggiorna_memorizzata(
        self,
        chiave: str,
        memoria: str,
        piattaforma: str,
        nuova: str | None,
        precedente: str | None,
        contesto: Context | None = None,
    ) -> None:
        voce = self.stato.voce(memoria)
        ricordata = SCONOSCIUTO if voce is None else voce.stato
        cambiata = None if voce is None else voce.cambiato
        ora = self.stato.stato(chiave) or SCONOSCIUTO
        risultato = come_stato(memorizzata(piattaforma, nuova, ora, ricordata))
        attributi: dict[str, Any] = {}
        if chiave == "sensor.status_ventola":
            attributi[ATTRIBUTO_INTERRUZIONE] = lettura_prima_dell_interruzione(
                piattaforma, precedente, ricordata, cambiata
            )
        # a ogni trigger, anche senza cambio (come il sensore a trigger di oggi)
        self.stato.imposta(
            {memoria: (_testo(risultato), attributi)}, contesto, scrivi_sempre=True
        )

    @callback
    def _medie(self) -> None:
        if not self.medie.last_update_success or self.medie.data is None:
            return
        # a ogni calcolo, anche senza cambio (come i sensori a trigger di oggi)
        self.stato.imposta(
            {chiave: _testo(valore) for chiave, valore in self.medie.data.items()},
            scrivi_sempre=True,
        )
