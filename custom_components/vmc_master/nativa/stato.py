"""Stato di una VMC nell'integrazione nativa.

Oggi i valori della VMC stanno nella macchina degli stati di Home Assistant (helper,
timer, sensori tcp e template). Nell'integrazione nativa stanno qui, per chiave (entity_id
di oggi senza «vmc_<nome>_»):

- ingressi: letture della VMC, sensori con memoria, impostazioni (gli helper di oggi),
  timer; li scrivono i coordinatori, il motore e le entità native;
- calcolati: i 120 modelli (template di oggi), ricalcolati a ogni cambio di un ingresso,
  di un'entità esterna letta (sensori scelti dall'utente) e a ogni minuto (now()).

Chi ascolta (entità native, motore) riceve le chiavi cambiate con valore vecchio e nuovo;
durante l'avviso ``contesto_cambi`` è il contesto della scrittura che ha causato i cambi (il
template di oggi prende quello dell'evento che lo fa ricalcolare), None per un ricalcolo a
tempo (ogni minuto, «delay_on»), che non ne ha.
I sensori binari con «delay_on» (Black-Out rilevato) tengono qui il loro ritardo.
"""

from __future__ import annotations

import logging
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from homeassistant.core import (
    CALLBACK_TYPE,
    Context,
    Event,
    EventStateChangedData,
    HomeAssistant,
    State,
    callback,
)
from homeassistant.helpers.event import async_call_later, async_track_time_change
from homeassistant.util import dt as dt_util

from .lettore import Lettore
from .modelli import MODELLI, Calcolo
from .motore.seguire import segui_cambi

_LOGGER = logging.getLogger(__name__)

SCONOSCIUTO = "unknown"
NON_DISPONIBILE = "unavailable"

Cambi = dict[str, tuple[str | None, str | None]]


@dataclass
class Voce:
    """Valore di una chiave: stato (testo), attributi e istanti di cambio."""

    stato: str
    attributi: dict[str, Any] = field(default_factory=dict)
    cambiato: datetime = field(default_factory=dt_util.utcnow)
    aggiornato: datetime = field(default_factory=dt_util.utcnow)


class StatoVMC:
    """Ingressi e sensori calcolati di una VMC, con chi li ascolta."""

    def __init__(self, hass: HomeAssistant, nome: str, ip: str = "") -> None:
        """Stato vuoto della VMC ``nome`` (indirizzo ``ip``): tutto «unknown» finché non arriva un valore."""
        self.hass = hass
        self.nome = nome
        self.ip = ip
        self._ingressi: dict[str, Voce] = {}
        self._calcolati: dict[str, Voce] = {}
        self._icone: dict[str, str | None] = {}
        self._memoria: dict[str, Any] = {}
        self._condizioni: dict[str, str] = {}
        self._ritardi: dict[str, CALLBACK_TYPE] = {}
        self._ascoltatori: list[Callable[[Cambi], None]] = []
        self.contesto_cambi: Context | None = None
        self._esterni: frozenset[str] = frozenset()
        self._letti: set[str] = set()
        self._annulla_esterni: CALLBACK_TYPE | None = None
        self._annulla_minuto: CALLBACK_TYPE | None = None
        # fase 5: i valori passati dalla beta (chiave -> State con l'entity_id nativo), da
        # usare all'avvio solo se Home Assistant non ha conservato uno stato dell'entità
        self.passati: dict[str, State] = {}

    # --- lettura -------------------------------------------------------------------------

    def stato(self, chiave: str) -> str | None:
        """Stato di una chiave (ingresso o calcolato); None se non esiste."""
        voce = self._calcolati.get(chiave) or self._ingressi.get(chiave)
        return None if voce is None else voce.stato

    def voce(self, chiave: str) -> Voce | None:
        """Valore completo di una chiave (stato, attributi, istanti)."""
        return self._calcolati.get(chiave) or self._ingressi.get(chiave)

    def icona(self, chiave: str) -> str | None:
        """Icona calcolata di un modello (None se il modello non ha icona calcolata)."""
        return self._icone.get(chiave)

    def entity_id(self, chiave: str) -> str:
        """entity_id di oggi per una chiave («sensor.x» -> «sensor.vmc_<nome>_x»)."""
        dominio, oggetto = chiave.split(".", 1)
        return f"{dominio}.vmc_{self.nome}_{oggetto}"

    # --- scrittura -----------------------------------------------------------------------

    @callback
    def imposta(
        self,
        valori: Mapping[str, str | tuple[str, Mapping[str, Any]]],
        contesto: Context | None = None,
        *,
        scrivi_sempre: bool = False,
    ) -> Cambi:
        """Scrive uno o più ingressi (stato, oppure (stato, attributi)) e ricalcola.

        Come nella macchina degli stati: last_changed cambia solo se cambia lo stato.
        Restituisce (e manda a chi ascolta) le chiavi cambiate; ``contesto`` è quello della
        scrittura (None: nessuno). Con ``scrivi_sempre`` anche gli ingressi rimasti uguali
        vanno a chi ascolta (come (stato, stato)): la loro entità li riscrive, e Home
        Assistant ne fa una scrittura senza cambio (``state_reported``), come i sensori a
        trigger di oggi, che scrivono a ogni trigger.
        """
        adesso = dt_util.utcnow()
        cambi: Cambi = {}
        for chiave, valore in valori.items():
            stato, attributi = (valore, None) if isinstance(valore, str) else valore
            vecchia = self._ingressi.get(chiave)
            if vecchia is None:
                self._ingressi[chiave] = Voce(
                    stato, dict(attributi or {}), adesso, adesso
                )
                cambi[chiave] = (None, stato)
                continue
            nuovi = vecchia.attributi if attributi is None else dict(attributi)
            if vecchia.stato == stato and nuovi == vecchia.attributi:
                if scrivi_sempre:
                    cambi[chiave] = (stato, stato)
                continue
            if vecchia.stato != stato:
                cambi[chiave] = (vecchia.stato, stato)
                vecchia.cambiato = adesso
            vecchia.stato = stato
            vecchia.attributi = nuovi
            vecchia.aggiornato = adesso
            cambi.setdefault(chiave, (stato, stato))
        cambi.update(self._ricalcola(adesso))
        self._avvisa(cambi, contesto)
        return cambi

    @callback
    def ricalcola(self, contesto: Context | None = None) -> Cambi:
        """Ricalcola i modelli (es. a ogni minuto, o per un'entità esterna cambiata, con
        il contesto del suo cambio)."""
        cambi = self._ricalcola(dt_util.utcnow())
        self._avvisa(cambi, contesto)
        return cambi

    # --- ascolto -------------------------------------------------------------------------

    @callback
    def ascolta(
        self, funzione: Callable[[Cambi], None], *, prima: bool = False
    ) -> CALLBACK_TYPE:
        """Chiama ``funzione`` con le chiavi cambiate; restituisce come smettere.

        Con ``prima`` la funzione passa davanti agli altri ascoltatori: le impostazioni
        (comandi.py) scrivono il loro stato prima dei sensori che lo leggono, come un
        aiutante di oggi cambia prima dei template che dipendono da lui.
        """
        if prima:
            self._ascoltatori.insert(0, funzione)
        else:
            self._ascoltatori.append(funzione)

        @callback
        def smetti() -> None:
            self._ascoltatori.remove(funzione)

        return smetti

    @callback
    def avvia(self) -> None:
        """Ricalcolo a ogni minuto (i modelli che usano l'ora) e primo calcolo."""

        @callback
        def ogni_minuto(_istante: datetime) -> None:
            self.ricalcola()

        self._annulla_minuto = async_track_time_change(self.hass, ogni_minuto, second=0)
        self.ricalcola()

    @callback
    def ferma(self) -> None:
        """Ferma ricalcoli, ritardi e ascolto delle entità esterne."""
        for annulla in (
            self._annulla_minuto,
            self._annulla_esterni,
            *self._ritardi.values(),
        ):
            if annulla is not None:
                annulla()
        self._annulla_minuto = self._annulla_esterni = None
        self._ritardi.clear()

    # --- interno -------------------------------------------------------------------------

    def _avvisa(self, cambi: Cambi, contesto: Context | None = None) -> None:
        if not cambi:
            return
        precedente = self.contesto_cambi
        self.contesto_cambi = contesto
        try:
            for funzione in list(self._ascoltatori):
                funzione(cambi)
        finally:
            self.contesto_cambi = precedente

    def _ingresso(self, chiave: str) -> str | None:
        voce = self._ingressi.get(chiave)
        return None if voce is None else voce.stato

    def _attributo(self, chiave: str, nome: str) -> Any:
        voce = self.voce(chiave)
        return None if voce is None else voce.attributi.get(nome)

    def _esterno(self, entity_id: str) -> str | None:
        self._letti.add(entity_id)
        stato = self.hass.states.get(entity_id)
        return None if stato is None else stato.state

    def _attributo_esterno(self, entity_id: str, nome: str) -> Any:
        self._letti.add(entity_id)
        stato = self.hass.states.get(entity_id)
        return None if stato is None else stato.attributes.get(nome)

    def _elenca(self, dominio: str) -> list[Any]:
        """Stati di un dominio (es. i sensori IP delle altre VMC): si seguono quelli trovati."""
        stati = self.hass.states.async_all(dominio)
        self._letti.update(
            s.entity_id for s in stati if s.entity_id.startswith(f"{dominio}.vmc_")
        )
        return stati

    def _ricalcola(self, adesso: datetime) -> Cambi:
        """Ricalcola tutti i modelli; se un sensore con ritardo si spegne subito, di nuovo."""
        cambi: Cambi = {}
        for _giro in range(5):
            subito = self._un_calcolo(adesso, cambi)
            if not subito:
                break
            for chiave, valore in subito.items():
                vecchia = self._ingressi.get(chiave)
                prima = None if vecchia is None else vecchia.stato
                if vecchia is None:
                    self._ingressi[chiave] = Voce(valore, {}, adesso, adesso)
                else:
                    vecchia.stato = valore
                    vecchia.cambiato = vecchia.aggiornato = adesso
                cambi[chiave] = (cambi.get(chiave, (prima, None))[0], valore)
        self._segui_esterni()
        return cambi

    def _un_calcolo(self, adesso: datetime, cambi: Cambi) -> dict[str, str]:
        """Un giro di calcolo; restituisce i sensori con ritardo da cambiare subito."""
        calcolo = Calcolo(self._ingresso)
        self._letti = set()
        lettore = Lettore(
            self.nome,
            calcolo.valore,
            self._esterno,
            dt_util.now,
            self._attributo,
            self._attributo_esterno,
            ip=self.ip,
            elenca=self._elenca,
            memoria=self._memoria,
        )
        calcolo.lettore = lettore
        subito: dict[str, str] = {}
        for chiave, modello in MODELLI.items():
            if modello.ritardo_on is not None:
                valore = self._aggiorna_ritardo(
                    chiave, calcolo.condizione(chiave), lettore
                )
                if valore is not None:
                    subito[chiave] = valore
                continue
            nuovo = calcolo.valore(chiave)
            assert nuovo is not None
            vecchia = self._calcolati.get(chiave)
            if vecchia is None:
                self._calcolati[chiave] = Voce(nuovo, {}, adesso, adesso)
                cambi[chiave] = (None, nuovo)
            elif vecchia.stato != nuovo:
                cambi[chiave] = (cambi.get(chiave, (vecchia.stato, None))[0], nuovo)
                vecchia.stato = nuovo
                vecchia.cambiato = vecchia.aggiornato = adesso
            if modello.icona is not None:
                icona = calcolo.icona(chiave)
                if self._icone.get(chiave) != icona:
                    self._icone[chiave] = icona
                    cambi.setdefault(chiave, (nuovo, nuovo))
        if subito:
            return subito
        # le icone dei sensori con ritardo dipendono dal loro stato: si calcolano per ultime
        for chiave, modello in MODELLI.items():
            if modello.ritardo_on is not None and modello.icona is not None:
                icona = calcolo.icona(chiave)
                if self._icone.get(chiave) != icona:
                    self._icone[chiave] = icona
                    stato = self._ingresso(chiave)
                    cambi.setdefault(chiave, (stato, stato))
        return subito

    def _aggiorna_ritardo(
        self, chiave: str, condizione: str, lettore: Lettore
    ) -> str | None:
        """«delay_on»: la condizione vera accende il sensore solo dopo il ritardo; falsa
        (o non disponibile) lo cambia subito: in quel caso restituisce il nuovo stato."""
        precedente = self._condizioni.get(chiave)
        self._condizioni[chiave] = condizione
        attuale = self._ingresso(chiave)
        if condizione != "on":
            if (annulla := self._ritardi.pop(chiave, None)) is not None:
                annulla()
            return condizione if attuale != condizione else None
        if condizione == precedente or attuale == "on" or chiave in self._ritardi:
            return None
        modello = MODELLI[chiave]
        assert modello.ritardo_on is not None
        secondi = modello.ritardo_on(lettore)

        @callback
        def accendi(_istante: Any) -> None:
            self._ritardi.pop(chiave, None)
            if self._condizioni.get(chiave) == "on":
                self.imposta({chiave: "on"})

        self._ritardi[chiave] = async_call_later(self.hass, secondi, accendi)
        return None

    def _segui_esterni(self) -> None:
        """Ricalcola quando cambia un'entità esterna letta dai modelli (es. sensori scelti)."""
        letti = frozenset(self._letti)
        if letti == self._esterni:
            return
        self._esterni = letti
        if self._annulla_esterni is not None:
            self._annulla_esterni()
            self._annulla_esterni = None
        if not letti:
            return

        @callback
        def cambiato(evento: Event[EventStateChangedData]) -> None:
            self.ricalcola(evento.context)

        # come async_track_state_change_event, nel canale del motore
        self._annulla_esterni = segui_cambi(self.hass, letti, cambiato)
