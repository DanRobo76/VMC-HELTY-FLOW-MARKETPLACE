"""Gli stati interni delle logiche del motore (le automazioni del package).

Fino alla 9.0.0b45 ogni automazione del package era un'entità ``automation`` e scriveva il
proprio stato nella macchina degli stati (``on``, ``id``, ``last_triggered``, ``mode``,
``current``, ``max``, ``friendly_name``). Ora le automazioni sono logiche
dell'integrazione (``logiche.Logica``) e quello stato resta qui: non è nella macchina
degli stati, ma i modelli del motore lo leggono come prima (un modello aspetta che
l'Automazione VMC Master non abbia esecuzioni in corso: ``current``) e chi lo segue riceve
i suoi cambi (``seguire.CambiInterni``), con gli stessi istanti e lo stesso contesto.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from homeassistant.const import EVENT_STATE_CHANGED, EVENT_STATE_REPORTED
from homeassistant.core import (
    CALLBACK_TYPE,
    Context,
    Event,
    EventOrigin,
    HomeAssistant,
    State,
    callback,
)
from homeassistant.util import dt as dt_util
from homeassistant.util.hass_dict import HassKey

from .seguire import cambi_interni

_MARCHIO = "vmc_master_annuncio_logica"

_DATI: HassKey[StatiLogiche] = HassKey("vmc_master_stati_logiche")


class StatiLogiche:
    """Gli stati interni delle logiche di ``hass`` (di tutte le VMC).

    Ogni scrittura è come ``StateMachine.async_set_internal``: stesso stato e stessi
    attributi cambiano solo ``last_reported``; altrimenti uno ``State`` nuovo, annunciato
    sul bus nello stesso punto in cui Home Assistant consegnerebbe ``state_changed`` (un
    ``state_reported`` con un marchio e l'entity_id vuoto, che non arriva agli ascoltatori
    di tutti gli eventi né al registro); alla consegna il cambio va prima agli
    ``osservatori`` e poi a chi segue l'entità (``CambiInterni``). Come la memoria interna
    per i suoi valori."""

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self.stati: dict[str, State] = {}
        # gli entity_id delle logiche: interni da quando la logica c'è, anche prima del suo
        # primo stato (chi li segue va seguito qui, non da Home Assistant)
        self.nomi: set[str] = set()
        self._osservatori: list[Callable[[Event[Any]], None]] = []
        self._annulla: CALLBACK_TYPE | None = None
        cambi_interni(hass).aggiungi(self)

    # --- la sorgente di CambiInterni -----------------------------------------------------

    def contiene(self, entity_id: str) -> bool:
        return entity_id in self.nomi

    def stato(self, entity_id: str) -> State | None:
        return self.stati.get(entity_id)

    # --- nomi ----------------------------------------------------------------------------

    @callback
    def aggiungi(self, entity_id: str) -> None:
        """Una logica nuova: da qui il suo entity_id è un valore interno."""
        self.nomi.add(entity_id)

    @callback
    def togli(self, entity_id: str) -> None:
        """La logica non c'è più: lo stato si toglie (come ``StateMachine.async_remove``),
        annunciato."""
        self.nomi.discard(entity_id)
        if (vecchio := self.stati.pop(entity_id, None)) is None:
            return
        self.hass.bus.async_fire(
            EVENT_STATE_REPORTED,
            {"entity_id": "", _MARCHIO: (entity_id, vecchio, None)},
        )

    # --- scritture -----------------------------------------------------------------------

    @callback
    def osserva(self, funzione: Callable[[Event[Any]], None]) -> CALLBACK_TYPE:
        """``funzione(evento state_changed)`` a ogni cambio, prima di chi segue lo stato;
        restituisce come smettere."""
        self._osservatori.append(funzione)

        @callback
        def smetti() -> None:
            self._osservatori.remove(funzione)

        return smetti

    @callback
    def scrivi(
        self,
        entity_id: str,
        nuovo: str,
        attributi: dict[str, Any],
        contesto: Context | None,
        istante: float,
    ) -> None:
        """Come ``StateMachine.async_set_internal`` (senza ``force_update``)."""
        if self._annulla is None:
            self._annulla = self.hass.bus.async_listen(
                EVENT_STATE_REPORTED, self._consegna, event_filter=_marcato
            )
        vecchio = self.stati.get(entity_id)
        adesso = dt_util.utc_from_timestamp(istante)
        if contesto is None:
            contesto = Context()
        if vecchio is not None:
            if vecchio.state == nuovo and vecchio.attributes == attributi:
                # nessuno segue i «state_reported» delle logiche: basta il nuovo istante
                self.stati[entity_id] = State(
                    entity_id,
                    nuovo,
                    vecchio.attributes,
                    vecchio.last_changed,
                    adesso,
                    vecchio.last_updated,
                    vecchio.context,
                    False,
                    None,
                    vecchio.last_updated_timestamp,
                )
                return
            if vecchio.attributes == attributi:
                attributi = vecchio.attributes  # type: ignore[assignment]
        stato = State(
            entity_id,
            nuovo,
            attributi,
            vecchio.last_changed
            if vecchio is not None and vecchio.state == nuovo
            else None,
            adesso,
            adesso,
            contesto,
            vecchio is None,
            None,
            istante,
        )
        self.stati[entity_id] = stato
        self.hass.bus.async_fire(
            EVENT_STATE_REPORTED,
            {"entity_id": "", _MARCHIO: (entity_id, vecchio, stato)},
            context=contesto,
            time_fired=istante,
        )

    @callback
    def _consegna(self, evento: Event[Any]) -> None:
        entity_id, vecchio, nuovo = evento.data[_MARCHIO]
        cambio: Event[Any] = Event(
            EVENT_STATE_CHANGED,
            {"entity_id": entity_id, "old_state": vecchio, "new_state": nuovo},
            EventOrigin.local,
            evento.time_fired_timestamp,
            evento.context,
        )
        for funzione in list(self._osservatori):
            funzione(cambio)
        cambi_interni(self.hass).consegna(cambio)


@callback
def _marcato(dati: Any) -> bool:
    return _MARCHIO in dati


@callback
def stati_logiche(hass: HomeAssistant) -> StatiLogiche:
    """Gli stati delle logiche di ``hass`` (uno per tutte le VMC)."""
    if (stati := hass.data.get(_DATI)) is None:
        stati = hass.data[_DATI] = StatiLogiche(hass)
    return stati
