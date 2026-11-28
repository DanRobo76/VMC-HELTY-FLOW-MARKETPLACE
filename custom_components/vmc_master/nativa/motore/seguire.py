"""Chi segue i cambi delle entità e dei valori interni del motore (il proprio tracciamento).

Home Assistant consegna ogni cambio di un'entità a chi la segue
(``async_track_state_change_event``: un elenco per entity_id, nell'ordine delle iscrizioni)
e su questo costruisce trigger ``state`` e ``template``, attese e sensori template. I valori
interni del motore (i valori della memoria interna e i timer del motore) non sono nella
macchina degli stati: i loro cambi li annuncia il motore stesso sul bus, nel punto in cui
Home Assistant consegnerebbe ``state_changed`` (``MemoriaInterna._consegna``,
``AnnunciDeiTimer._consegna``), e da lì vanno a ``CambiInterni.consegna``.

Qui ci sono:

- ``CambiInterni`` (uno per ``hass``): chi segue i valori interni, per entity_id e
  nell'ordine delle iscrizioni, con la consegna di Home Assistant
  (``helpers.event._async_dispatch_entity_id_event``: ``HassJob``, copia dell'elenco,
  errori nel registro);
- ``segui_cambi``: al posto di ``async_track_state_change_event``; un'entità vera la segue
  Home Assistant (la sua funzione pubblica), un valore interno ``CambiInterni``;
- ``stato_di``: lo stato di un valore interno o di un'entità;
- ``segui_stesso_stato``, ``traccia_modelli``, ``segui_modello``: ``async_track_same_state``,
  ``async_track_template_result`` (``TrackTemplateResultInfo``) e ``async_track_template``
  di Home Assistant, riga per riga, con ``segui_cambi`` per le entità lette.

Le parti riportate vengono da ``homeassistant/helpers/event.py`` di Home Assistant
2026.11.2 (Apache-2.0, licenza nel file ``LICENSE-Apache-2.0.txt`` dell'integrazione):
stesse regole, stesso ordine, stessi messaggi nel registro (con il
registro di questo modulo). Cambia solo da dove arrivano i cambi dei valori interni. I
domini e «tutti gli stati» letti da un modello restano quelli delle entità vere (come oggi:
i valori interni arrivano solo a chi segue il loro entity_id).
"""

from __future__ import annotations

import copy
import logging
import time
from collections import defaultdict, deque
from collections.abc import Callable, Coroutine, Iterable, Mapping, Sequence
from datetime import datetime, timedelta
from typing import Any, Protocol

from homeassistant.const import EVENT_STATE_CHANGED, MATCH_ALL
from homeassistant.core import (
    CALLBACK_TYPE,
    Context,
    Event,
    EventOrigin,
    EventStateChangedData,
    HassJob,
    HassJobType,
    HomeAssistant,
    State,
    async_noop,
    callback,
    split_entity_id,
)
from homeassistant.exceptions import TemplateError
from homeassistant.helpers.event import (
    TrackStates,
    TrackTemplate,
    TrackTemplateResult,
    async_call_later,
    async_track_utc_time_change,
)
from homeassistant.helpers.ratelimit import KeyedRateLimit
from homeassistant.helpers.template import Template, result_as_boolean
from homeassistant.helpers.template.render_info import RenderInfo
from homeassistant.helpers.typing import TemplateVarsType
from homeassistant.util.hass_dict import HassKey

_LOGGER = logging.getLogger(__name__)

_ALL_LISTENER = "all"
_DOMAINS_LISTENER = "domains"
_ENTITIES_LISTENER = "entities"

Seguace = Callable[[Event[EventStateChangedData]], Any]


# --- i valori interni -----------------------------------------------------------------------


class Sorgente(Protocol):
    """Chi ha dei valori interni (la memoria interna, i timer del motore)."""

    def contiene(self, entity_id: str) -> bool:
        """Se ``entity_id`` è un suo valore interno."""

    def stato(self, entity_id: str) -> State | None:
        """Lo stato di un suo valore interno (come lo terrebbe la macchina degli stati)."""


class CambiInterni:
    """Il canale del motore di ``hass`` (di tutte le VMC): chi segue i valori interni e le
    entità, e la consegna dei loro cambi.

    Home Assistant consegna gli eventi con un solo bus: un evento lanciato mentre il bus ne
    consegna un altro aspetta la fine di quella consegna e passa dopo quelli già in attesa
    (``EventBus.async_fire_internal``). I valori interni del motore non sono entità e i loro
    cambi non passano dal bus: li annuncia il motore su questo canale (``manda``). Perché il
    motore veda tutto nell'ordine di un solo bus, anche gli eventi del bus che il motore
    ascolta (i cambi delle entità che segue, i suoi trigger ``event`` e ``homeassistant``)
    passano da qui: un ascoltatore del bus per tipo di evento li mette nel canale. Il canale
    consegna subito, oppure, se sta già consegnando, dopo la consegna in corso e dopo quelli
    già in attesa, nell'ordine.

    Chi segue: come i cambi delle entità in Home Assistant (``_KEYED_TRACK_STATE_CHANGE``),
    un elenco di ``HassJob`` per entity_id nell'ordine delle iscrizioni, eseguiti come
    ``_async_dispatch_entity_id_event``. Le sorgenti dei valori interni (``aggiungi``) dicono
    quali entity_id sono interni: chi si iscrive a un entity_id interno riceve gli annunci
    della sorgente, gli altri i cambi dell'entità vera. Una sorgente si aggiunge prima che
    qualcuno cominci a seguire i suoi valori."""

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self._sorgenti: list[Sorgente] = []
        # chi segue un valore interno e chi segue un'entità vera, per entity_id
        self._seguaci: defaultdict[str, list[HassJob[[Event[Any]], Any]]] = defaultdict(
            list
        )
        self._seguaci_veri: defaultdict[str, list[HassJob[[Event[Any]], Any]]] = (
            defaultdict(list)
        )
        # chi segue le entità aggiunte a un dominio e chi segue tutti i cambi
        self._domini: defaultdict[str, list[HassJob[[Event[Any]], Any]]] = defaultdict(
            list
        )
        self._tutti: list[HassJob[[Event[Any]], Any]] = []
        # chi ascolta gli altri eventi del bus, per tipo
        self._ascolti: defaultdict[str, list[_Ascolto]] = defaultdict(list)
        # chi guarda gli eventi del bus nel punto del canale (le prove, il simulatore)
        self._osservatori: defaultdict[str, list[Callable[[Event[Any]], None]]] = (
            defaultdict(list)
        )
        # l'ascoltatore del bus di ogni tipo di evento che passa dal canale
        self._dal_bus: dict[str, CALLBACK_TYPE] = {}
        # chi aspetta il suo turno e se il canale sta già consegnando
        self._coda: deque[tuple[Callable[[Event[Any]], None], Event[Any]]] = deque()
        self._consegnando = False

    # --- sorgenti ---------------------------------------------------------------------------

    @callback
    def aggiungi(self, sorgente: Sorgente) -> CALLBACK_TYPE:
        """Una sorgente di valori interni; restituisce come toglierla."""
        self._sorgenti.append(sorgente)

        @callback
        def togli() -> None:
            self._sorgenti.remove(sorgente)

        return togli

    def sorgente_di(self, entity_id: str) -> Sorgente | None:
        """La sorgente che ha ``entity_id`` tra i suoi valori interni, o None."""
        for sorgente in self._sorgenti:
            if sorgente.contiene(entity_id):
                return sorgente
        return None

    def contiene(self, entity_id: str) -> bool:
        """Se ``entity_id`` è un valore interno (di una delle sorgenti)."""
        return self.sorgente_di(entity_id) is not None

    def stato(self, entity_id: str) -> State | None:
        """Lo stato di un valore interno, o None se non è un valore interno."""
        if (sorgente := self.sorgente_di(entity_id)) is None:
            return None
        return sorgente.stato(entity_id)

    # --- chi segue --------------------------------------------------------------------------

    @callback
    def segui(
        self,
        entity_ids: Iterable[str],
        azione: Seguace,
        job_type: HassJobType | None = None,
    ) -> CALLBACK_TYPE:
        """``azione(evento)`` a ogni cambio di questi valori interni ed entità (come
        ``_async_track_event``: gli entity_id come sono, un ``HassJob`` per iscrizione);
        restituisce come smettere."""
        chiavi = list(entity_ids)
        if not chiavi:
            return async_noop
        job = HassJob(
            azione, f"track {EVENT_STATE_CHANGED} event {chiavi}", job_type=job_type
        )
        iscritti: list[tuple[defaultdict[str, list[HassJob[[Event[Any]], Any]]], str]] = []
        for chiave in chiavi:
            elenco = self._seguaci if self.contiene(chiave) else self._seguaci_veri
            elenco[chiave].append(job)
            iscritti.append((elenco, chiave))
        if self._seguaci_veri:
            self._aggancia(EVENT_STATE_CHANGED)

        @callback
        def smetti() -> None:
            for elenco, chiave in iscritti:
                elenco[chiave].remove(job)
                if not elenco[chiave]:
                    del elenco[chiave]
            self._sgancia_se_inutile(EVENT_STATE_CHANGED)

        return smetti

    @callback
    def segui_domini(
        self,
        domini: Iterable[str],
        azione: Seguace,
        job_type: HassJobType | None = None,
    ) -> CALLBACK_TYPE:
        """Come ``async_track_state_added_domain`` (i domini già minuscoli): ``azione``
        quando un'entità vera di questi domini compare."""
        chiavi = list(domini)
        if not chiavi:
            return async_noop
        job = HassJob(
            azione, f"track {EVENT_STATE_CHANGED} event {chiavi}", job_type=job_type
        )
        for chiave in chiavi:
            self._domini[chiave].append(job)
        self._aggancia(EVENT_STATE_CHANGED)

        @callback
        def smetti() -> None:
            for chiave in chiavi:
                self._domini[chiave].remove(job)
                if not self._domini[chiave]:
                    del self._domini[chiave]
            self._sgancia_se_inutile(EVENT_STATE_CHANGED)

        return smetti

    @callback
    def segui_tutti(self, azione: Seguace) -> CALLBACK_TYPE:
        """Come ``hass.bus.async_listen(EVENT_STATE_CHANGED, azione)``: ogni cambio di
        un'entità vera."""
        job = HassJob(azione, f"listen {EVENT_STATE_CHANGED}")
        self._tutti.append(job)
        self._aggancia(EVENT_STATE_CHANGED)

        @callback
        def smetti() -> None:
            self._tutti.remove(job)
            self._sgancia_se_inutile(EVENT_STATE_CHANGED)

        return smetti

    @callback
    def ascolta(
        self,
        tipo: str,
        azione: Callable[[Event[Any]], Any],
        filtro: Callable[[Any], bool] | None = None,
        *,
        una_volta: bool = False,
    ) -> CALLBACK_TYPE:
        """Come ``hass.bus.async_listen(tipo, azione, event_filter=filtro)`` (o
        ``async_listen_once`` con ``una_volta``): ogni evento ``tipo`` del bus, nel punto
        del canale."""
        ascolto = _Ascolto(HassJob(azione, f"listen {tipo}"), filtro, una_volta)
        self._ascolti[tipo].append(ascolto)
        self._aggancia(tipo)

        @callback
        def smetti() -> None:
            if ascolto in self._ascolti[tipo]:
                self._ascolti[tipo].remove(ascolto)
                if not self._ascolti[tipo]:
                    del self._ascolti[tipo]
            self._sgancia_se_inutile(tipo)

        ascolto.smetti = smetti
        return smetti

    @callback
    def osserva(self, tipo: str, funzione: Callable[[Event[Any]], None]) -> CALLBACK_TYPE:
        """``funzione(evento)`` per ogni evento ``tipo`` del bus, nel punto del canale e
        prima di chi lo segue (le prove e il simulatore annotano così l'ordine in cui il
        motore vede gli eventi)."""
        self._osservatori[tipo].append(funzione)
        self._aggancia(tipo)

        @callback
        def smetti() -> None:
            self._osservatori[tipo].remove(funzione)
            if not self._osservatori[tipo]:
                del self._osservatori[tipo]
            self._sgancia_se_inutile(tipo)

        return smetti

    # --- dal bus al canale ------------------------------------------------------------------

    @callback
    def _aggancia(self, tipo: str) -> None:
        """L'ascoltatore del bus che mette nel canale gli eventi ``tipo``."""
        if tipo in self._dal_bus:
            return
        self._dal_bus[tipo] = self.hass.bus.async_listen(
            tipo,
            self._dal_bus_al_canale,
            event_filter=self._cambio_voluto if tipo == EVENT_STATE_CHANGED else None,
        )

    @callback
    def _sgancia_se_inutile(self, tipo: str) -> None:
        """Toglie l'ascoltatore del bus quando nessuno vuole più gli eventi ``tipo`` (come
        Home Assistant toglie il distributore di un tracker senza più iscritti)."""
        if tipo not in self._dal_bus or self._osservatori.get(tipo) or self._ascolti.get(tipo):
            return
        if tipo == EVENT_STATE_CHANGED and (
            self._seguaci_veri or self._domini or self._tutti
        ):
            return
        self._dal_bus.pop(tipo)()

    @callback
    def _cambio_voluto(self, dati: Mapping[str, Any]) -> bool:
        """Se qualcuno vuole questo ``state_changed`` (come i filtri dei tracker)."""
        if (
            self._tutti
            or self._osservatori.get(EVENT_STATE_CHANGED)
            or self._ascolti.get(EVENT_STATE_CHANGED)
            or dati["entity_id"] in self._seguaci_veri
        ):
            return True
        return bool(
            self._domini
            and dati["old_state"] is None
            and (MATCH_ALL in self._domini or dati["new_state"].domain in self._domini)
        )

    @callback
    def _dal_bus_al_canale(self, evento: Event[Any]) -> None:
        self._nel_canale(self._smista, evento)

    @callback
    def _smista(self, evento: Event[Any]) -> None:
        """Un evento del bus a chi lo guarda e a chi lo segue: i cambi di un'entità a chi
        la segue, a chi segue il suo dominio (se compare) e a chi segue tutti i cambi."""
        tipo = evento.event_type
        for funzione in list(self._osservatori.get(tipo, ())):
            try:
                funzione(evento)
            except Exception:
                _LOGGER.exception("Error running job: %s", funzione)
        if tipo == EVENT_STATE_CHANGED:
            dati = evento.data
            if seguaci := self._seguaci_veri.get(dati["entity_id"]):
                self._esegui_tutti(seguaci, evento, dati["entity_id"])
            if self._domini and dati["old_state"] is None:
                dominio = split_entity_id(dati["entity_id"])[0]
                for job in self._domini.get(dominio, []) + self._domini.get(MATCH_ALL, []):
                    try:
                        self.hass.async_run_hass_job(job, evento)
                    except Exception:
                        _LOGGER.exception(
                            "Error while processing event %s for domain %s",
                            evento,
                            dominio,
                        )
            for job in list(self._tutti):
                try:
                    self.hass.async_run_hass_job(job, evento)
                except Exception:
                    _LOGGER.exception("Error running job: %s", job)
        for ascolto in list(self._ascolti.get(tipo, ())):
            if ascolto.filtro is not None:
                try:
                    if not ascolto.filtro(evento.data):
                        continue
                except Exception:
                    _LOGGER.exception("Error in event filter")
                    continue
            if ascolto.una_volta:
                if ascolto.smetti is None:
                    continue
                ascolto.smetti()
                ascolto.smetti = None
            try:
                self.hass.async_run_hass_job(ascolto.job, evento)
            except Exception:
                _LOGGER.exception("Error running job: %s", ascolto.job)

    # --- il canale --------------------------------------------------------------------------

    @callback
    def manda(
        self,
        consegna: Callable[[Event[Any]], None],
        dati: dict[str, Any],
        contesto: Context | None = None,
        istante: float | None = None,
    ) -> None:
        """L'annuncio di una sorgente del motore (un cambio di un valore interno, una
        chiamata ai valori interni, un comando): ``consegna`` riceve un evento con i
        ``dati``, il contesto e l'istante dell'annuncio (adesso se manca), nel canale."""
        self._nel_canale(
            consegna,
            Event(
                _ANNUNCIO,
                dati,
                EventOrigin.local,
                istante if istante is not None else time.time(),
                contesto,
            ),
        )

    @callback
    def _nel_canale(
        self, consegna: Callable[[Event[Any]], None], evento: Event[Any]
    ) -> None:
        """Consegna subito; se il canale sta già consegnando, dopo la consegna in corso e
        dopo chi aspetta già, nell'ordine (come il bus di Home Assistant). Un errore di chi
        riceve finisce nel registro e non ferma gli altri."""
        if self._consegnando:
            self._coda.append((consegna, evento))
            return
        self._consegnando = True
        try:
            self._esegui(consegna, evento)
            while self._coda:
                self._esegui(*self._coda.popleft())
        finally:
            self._consegnando = False

    @staticmethod
    def _esegui(consegna: Callable[[Event[Any]], None], evento: Event[Any]) -> None:
        try:
            consegna(evento)
        except Exception:
            _LOGGER.exception("Error running job: %s", consegna)

    def _esegui_tutti(
        self,
        seguaci: list[HassJob[[Event[Any]], Any]],
        evento: Event[Any],
        entity_id: str,
    ) -> None:
        """Come ``_async_dispatch_entity_id_event``."""
        for job in seguaci.copy():
            try:
                self.hass.async_run_hass_job(job, evento)
            except Exception:
                _LOGGER.exception(
                    "Error while dispatching event for %s to %s", entity_id, job
                )

    @callback
    def consegna(self, evento: Event[EventStateChangedData]) -> None:
        """Il cambio di un valore interno a chi lo segue, nell'ordine delle iscrizioni
        (come ``_async_dispatch_entity_id_event``). Lo chiama la sorgente quando il canale
        consegna il suo annuncio."""
        if seguaci := self._seguaci.get(evento.data["entity_id"]):
            self._esegui_tutti(seguaci, evento, evento.data["entity_id"])


class _Ascolto:
    """Chi ascolta un evento del bus nel canale (``CambiInterni.ascolta``)."""

    __slots__ = ("filtro", "job", "smetti", "una_volta")

    def __init__(
        self,
        job: HassJob[[Event[Any]], Any],
        filtro: Callable[[Any], bool] | None,
        una_volta: bool,
    ) -> None:
        self.job = job
        self.filtro = filtro
        self.una_volta = una_volta
        self.smetti: CALLBACK_TYPE | None = None


_CAMBI_INTERNI: HassKey[CambiInterni] = HassKey("vmc_master_cambi_interni")
# il tipo degli eventi del canale degli annunci (non passano dal bus di Home Assistant)
_ANNUNCIO = "vmc_master_annuncio"


@callback
def cambi_interni(hass: HomeAssistant) -> CambiInterni:
    """I valori interni del motore di ``hass`` (uno per tutte le VMC)."""
    if (interni := hass.data.get(_CAMBI_INTERNI)) is None:
        interni = hass.data[_CAMBI_INTERNI] = CambiInterni(hass)
    return interni


# --- seguire le entità e i valori interni ---------------------------------------------------


@callback
def _in_minuscolo(entity_ids: str | Iterable[str]) -> list[str]:
    """Come ``_async_string_to_lower_list``."""
    if isinstance(entity_ids, str):
        return [entity_ids.lower()]
    return [entity_id.lower() for entity_id in entity_ids]


@callback
def segui_cambi(
    hass: HomeAssistant,
    entity_ids: str | Iterable[str],
    azione: Seguace,
    job_type: HassJobType | None = None,
) -> CALLBACK_TYPE:
    """Al posto di ``async_track_state_change_event`` (stessi argomenti): ``azione(evento)``
    a ogni cambio di queste entità o di questi valori interni, nell'ordine delle iscrizioni
    per ogni entity_id. Gli entity_id diventano minuscoli, come in Home Assistant."""
    if not (entity_ids := _in_minuscolo(entity_ids)):
        return async_noop
    return _segui_cambi(hass, entity_ids, azione, job_type)


@callback
def _segui_cambi(
    hass: HomeAssistant,
    entity_ids: Iterable[str],
    azione: Seguace,
    job_type: HassJobType | None,
) -> CALLBACK_TYPE:
    """Come ``_async_track_state_change_event`` (gli entity_id come sono): gli entity_id
    delle entità a Home Assistant, quelli dei valori interni a ``CambiInterni``.

    Home Assistant iscrive gli entity_id come li riceve, e un cambio ha sempre l'entity_id
    in minuscolo: un entity_id con delle maiuscole non riceve mai nulla. Qui non si iscrive
    (la funzione pubblica di Home Assistant lo renderebbe minuscolo)."""
    if not entity_ids:
        return async_noop
    chiavi = [entity_id for entity_id in entity_ids if entity_id == entity_id.lower()]
    return cambi_interni(hass).segui(chiavi, azione, job_type)


def stato_di(hass: HomeAssistant, entity_id: str) -> State | None:
    """Lo stato di un valore interno, o di un'entità (``hass.states.get``)."""
    if (interni := hass.data.get(_CAMBI_INTERNI)) is not None:
        for chiave in dict.fromkeys((entity_id, entity_id.lower())):
            if (sorgente := interni.sorgente_di(chiave)) is not None:
                return sorgente.stato(chiave)
    return hass.states.get(entity_id)


# --- async_track_same_state -----------------------------------------------------------------


@callback
def segui_stesso_stato(
    hass: HomeAssistant,
    period: timedelta,
    action: Callable[[], Coroutine[Any, Any, None] | None],
    async_check_same_func: Callable[[str, State | None, State | None], bool],
    entity_ids: str | Iterable[str] = MATCH_ALL,
) -> CALLBACK_TYPE:
    """Come ``async_track_same_state``, con ``segui_cambi`` per le entità. Con
    ``MATCH_ALL`` ascolta tutti i ``state_changed`` del bus (le entità vere, come
    Home Assistant)."""
    async_remove_state_for_cancel: CALLBACK_TYPE | None = None
    async_remove_state_for_listener: CALLBACK_TYPE | None = None

    job = HassJob(action, f"track same state {period} {entity_ids}")

    @callback
    def clear_listener() -> None:
        """Clear all unsub listener."""
        nonlocal async_remove_state_for_cancel, async_remove_state_for_listener

        if async_remove_state_for_listener is not None:
            async_remove_state_for_listener()
            async_remove_state_for_listener = None
        if async_remove_state_for_cancel is not None:
            async_remove_state_for_cancel()
            async_remove_state_for_cancel = None

    @callback
    def state_for_listener(now: Any) -> None:
        """Fire on state changes after a delay and calls action."""
        nonlocal async_remove_state_for_listener
        async_remove_state_for_listener = None
        clear_listener()
        hass.async_run_hass_job(job)

    @callback
    def state_for_cancel_listener(event: Event[EventStateChangedData]) -> None:
        """Fire on changes and cancel for listener if changed."""
        entity = event.data["entity_id"]
        from_state = event.data["old_state"]
        to_state = event.data["new_state"]

        if not async_check_same_func(entity, from_state, to_state):
            clear_listener()

    async_remove_state_for_listener = async_call_later(hass, period, state_for_listener)

    if entity_ids == MATCH_ALL:
        async_remove_state_for_cancel = cambi_interni(hass).segui_tutti(
            state_for_cancel_listener
        )
    else:
        async_remove_state_for_cancel = segui_cambi(
            hass,
            entity_ids,
            state_for_cancel_listener,
        )

    return clear_listener


# --- _TrackStateChangeFiltered --------------------------------------------------------------


class _SeguiStatiFiltrati:
    """Come ``_TrackStateChangeFiltered``: le entità con ``_segui_cambi``, i domini e tutti
    gli stati con Home Assistant (solo le entità vere)."""

    def __init__(
        self,
        hass: HomeAssistant,
        track_states: TrackStates,
        action: Seguace,
    ) -> None:
        self.hass = hass
        self._action = action
        self._action_as_hassjob = HassJob(
            action, f"track state change filtered {track_states}"
        )
        self._listeners: dict[str, Callable[[], None]] = {}
        self._last_track_states: TrackStates = track_states

    @callback
    def async_setup(self) -> None:
        """Create listeners to track states."""
        track_states = self._last_track_states

        if (
            not track_states.all_states
            and not track_states.domains
            and not track_states.entities
        ):
            return

        if track_states.all_states:
            self._setup_all_listener()
            return

        self._setup_domains_listener(track_states.domains)
        self._setup_entities_listener(track_states.domains, track_states.entities)

    @property
    def listeners(self) -> dict[str, bool | set[str]]:
        """State changes that will cause a re-render."""
        track_states = self._last_track_states
        return {
            _ALL_LISTENER: track_states.all_states,
            _ENTITIES_LISTENER: track_states.entities,
            _DOMAINS_LISTENER: track_states.domains,
        }

    @callback
    def async_update_listeners(self, new_track_states: TrackStates) -> None:
        """Update the listeners based on the new TrackStates."""
        last_track_states = self._last_track_states
        self._last_track_states = new_track_states

        had_all_listener = last_track_states.all_states

        if new_track_states.all_states:
            if had_all_listener:
                return
            self._cancel_listener(_DOMAINS_LISTENER)
            self._cancel_listener(_ENTITIES_LISTENER)
            self._setup_all_listener()
            return

        if had_all_listener:
            self._cancel_listener(_ALL_LISTENER)

        domains_changed = new_track_states.domains != last_track_states.domains

        if had_all_listener or domains_changed:
            domains_changed = True
            self._cancel_listener(_DOMAINS_LISTENER)
            self._setup_domains_listener(new_track_states.domains)

        if (
            had_all_listener
            or domains_changed
            or new_track_states.entities != last_track_states.entities
        ):
            self._cancel_listener(_ENTITIES_LISTENER)
            self._setup_entities_listener(
                new_track_states.domains, new_track_states.entities
            )

    @callback
    def async_remove(self) -> None:
        """Cancel the listeners."""
        for key in list(self._listeners):
            self._listeners.pop(key)()

    @callback
    def _cancel_listener(self, listener_name: str) -> None:
        if listener_name not in self._listeners:
            return

        self._listeners.pop(listener_name)()

    @callback
    def _setup_entities_listener(self, domains: set[str], entities: set[str]) -> None:
        if domains:
            entities = entities.copy()
            entities.update(self.hass.states.async_entity_ids(domains))

        # Entities has changed to none
        if not entities:
            return

        self._listeners[_ENTITIES_LISTENER] = _segui_cambi(
            self.hass, entities, self._action, self._action_as_hassjob.job_type
        )

    @callback
    def _state_added(self, event: Event[EventStateChangedData]) -> None:
        self._cancel_listener(_ENTITIES_LISTENER)
        self._setup_entities_listener(
            self._last_track_states.domains, self._last_track_states.entities
        )
        self.hass.async_run_hass_job(self._action_as_hassjob, event)

    @callback
    def _setup_domains_listener(self, domains: set[str]) -> None:
        if not domains:
            return

        self._listeners[_DOMAINS_LISTENER] = cambi_interni(self.hass).segui_domini(
            [dominio.lower() for dominio in domains],
            self._state_added,
            HassJobType.Callback,
        )

    @callback
    def _setup_all_listener(self) -> None:
        self._listeners[_ALL_LISTENER] = cambi_interni(self.hass).segui_tutti(
            self._action
        )


# --- async_track_template -------------------------------------------------------------------


@callback
def segui_modello(
    hass: HomeAssistant,
    template: Template,
    action: Callable[
        [str, State | None, State | None], Coroutine[Any, Any, None] | None
    ],
    variables: TemplateVarsType | None = None,
) -> CALLBACK_TYPE:
    """Come ``async_track_template``: ``action(entity_id, old_state, new_state)`` quando il
    modello passa a vero (con ``traccia_modelli``)."""
    job = HassJob(action, f"track template {template}")

    @callback
    def _template_changed_listener(
        event: Event[EventStateChangedData] | None,
        updates: list[TrackTemplateResult],
    ) -> None:
        """Check if condition is correct and run action."""
        track_result = updates.pop()

        template = track_result.template
        last_result = track_result.last_result
        result = track_result.result

        if isinstance(result, TemplateError):
            _LOGGER.error(
                "Error while processing template: %s",
                template.template,
                exc_info=result,
            )
            return

        if (
            not isinstance(last_result, TemplateError)
            and result_as_boolean(last_result)
        ) or not result_as_boolean(result):
            return

        hass.async_run_hass_job(
            job,
            event and event.data["entity_id"],
            event and event.data["old_state"],
            event and event.data["new_state"],
        )

    info = traccia_modelli(
        hass, [TrackTemplate(template, variables)], _template_changed_listener
    )

    return info.async_remove


# --- TrackTemplateResultInfo ----------------------------------------------------------------

type TrackTemplateResultListener = Callable[
    [
        Event[EventStateChangedData] | None,
        list[TrackTemplateResult],
    ],
    Coroutine[Any, Any, None] | None,
]


class TracciaModelli:
    """Come ``TrackTemplateResultInfo`` (stessa interfaccia: ``async_setup``,
    ``listeners``, ``async_remove``, ``async_refresh``), con ``_SeguiStatiFiltrati``."""

    def __init__(
        self,
        hass: HomeAssistant,
        track_templates: Sequence[TrackTemplate],
        action: TrackTemplateResultListener,
        has_super_template: bool = False,
    ) -> None:
        """Handle removal / refresh of tracker init."""
        self.hass = hass
        self._job = HassJob(action, f"track template result {track_templates}")

        self._track_templates = track_templates
        self._has_super_template = has_super_template

        self._last_result: dict[Template, bool | str | TemplateError] = {}

        self._rate_limit = KeyedRateLimit(hass)
        self._info: dict[Template, RenderInfo] = {}
        self._track_state_changes: _SeguiStatiFiltrati | None = None
        self._time_listeners: dict[Template, Callable[[], None]] = {}

    def __repr__(self) -> str:
        """Return the representation."""
        return f"<TracciaModelli {self._info}>"

    def async_setup(
        self,
        strict: bool = False,
        log_fn: Callable[[int, str], None] | None = None,
    ) -> None:
        """Activation of template tracking."""
        block_render = False
        super_template = self._track_templates[0] if self._has_super_template else None

        # Render the super template first
        if super_template is not None:
            template = super_template.template
            variables = super_template.variables
            self._info[template] = info = template.async_render_to_info(
                variables, strict=strict, log_fn=log_fn
            )

            # If the super template did not render to True, don't update other templates
            try:
                super_result: str | TemplateError = info.result()
            except TemplateError as ex:
                super_result = ex
            if (
                super_result is not None
                and self._super_template_as_boolean(super_result) is not True
            ):
                block_render = True

        # Then update the remaining templates unless blocked by the super template
        for track_template_ in self._track_templates:
            if block_render or track_template_ == super_template:
                continue
            template = track_template_.template
            variables = track_template_.variables
            self._info[template] = info = template.async_render_to_info(
                variables, strict=strict, log_fn=log_fn
            )

            if info.exception:
                if not log_fn:
                    _LOGGER.error(
                        "Error while processing template: %s",
                        track_template_.template,
                        exc_info=info.exception,
                    )
                else:
                    log_fn(logging.ERROR, str(info.exception))

        self._track_state_changes = _SeguiStatiFiltrati(
            self.hass, _render_infos_to_track_states(self._info.values()), self._refresh
        )
        self._track_state_changes.async_setup()
        self._update_time_listeners()
        _LOGGER.debug(
            (
                "Template group %s listens for %s, first render blocked by super"
                " template: %s"
            ),
            self._track_templates,
            self.listeners,
            block_render,
        )

    @property
    def listeners(self) -> dict[str, bool | set[str]]:
        """State changes that will cause a re-render."""
        assert self._track_state_changes
        return {
            **self._track_state_changes.listeners,
            "time": bool(self._time_listeners),
        }

    @callback
    def _setup_time_listener(self, template: Template, has_time: bool) -> None:
        if not has_time:
            if template in self._time_listeners:
                # now() or utcnow() has left the scope of the template
                self._time_listeners.pop(template)()
            return

        if template in self._time_listeners:
            return

        track_templates = [
            track_template_
            for track_template_ in self._track_templates
            if track_template_.template == template
        ]

        @callback
        def _refresh_from_time(now: datetime) -> None:
            self._refresh(None, track_templates=track_templates)

        self._time_listeners[template] = async_track_utc_time_change(
            self.hass, _refresh_from_time, second=0
        )

    @callback
    def _update_time_listeners(self) -> None:
        for template, info in self._info.items():
            self._setup_time_listener(template, info.has_time)

    @callback
    def async_remove(self) -> None:
        """Cancel the listener."""
        assert self._track_state_changes
        self._track_state_changes.async_remove()
        self._rate_limit.async_remove()
        for template in list(self._time_listeners):
            self._time_listeners.pop(template)()

    @callback
    def async_refresh(self) -> None:
        """Force recalculate the template."""
        self._refresh(None)

    def _render_template_if_ready(
        self,
        track_template_: TrackTemplate,
        now: float,
        event: Event[EventStateChangedData] | None,
    ) -> bool | TrackTemplateResult:
        """Re-render the template if conditions match.

        Returns False if the template was not re-rendered.

        Returns True if the template re-rendered and did not
        change.

        Returns TrackTemplateResult if the template re-render
        generates a new result.
        """
        template = track_template_.template

        if event:
            info = self._info[template]

            if not _event_triggers_rerender(event, info):
                return False

            had_timer = self._rate_limit.async_has_timer(template)

            if self._rate_limit.async_schedule_action(
                template,
                _rate_limit_for_event(event, info, track_template_),
                now,
                self._refresh,
                event,
                (track_template_,),
                True,
            ):
                return not had_timer

            _LOGGER.debug(
                "Template update %s triggered by event: %s",
                template.template,
                event,
            )

        self._rate_limit.async_triggered(template, now)
        self._info[template] = info = template.async_render_to_info(
            track_template_.variables
        )

        try:
            result: str | TemplateError = info.result()
        except TemplateError as ex:
            result = ex

        last_result = self._last_result.get(template)

        # Check to see if the result has changed or is new
        if result == last_result and template in self._last_result:
            return True

        if isinstance(result, TemplateError) and isinstance(last_result, TemplateError):
            return True

        return TrackTemplateResult(template, last_result, result)

    @staticmethod
    def _super_template_as_boolean(result: bool | str | TemplateError) -> bool:
        """Return True if the result is truthy or a TemplateError."""
        if isinstance(result, TemplateError):
            return True

        return result_as_boolean(result)

    @callback
    def _apply_update(
        self,
        updates: list[TrackTemplateResult],
        update: bool | TrackTemplateResult,
        template: Template,
    ) -> bool:
        """Handle updates of a tracked template."""
        if not update:
            return False

        self._setup_time_listener(template, self._info[template].has_time)

        if isinstance(update, TrackTemplateResult):
            updates.append(update)

        return True

    @callback
    def _refresh(
        self,
        event: Event[EventStateChangedData] | None,
        track_templates: Iterable[TrackTemplate] | None = None,
        replayed: bool | None = False,
    ) -> None:
        """Refresh the template.

        The event is the state_changed event that caused the refresh
        to be considered.

        track_templates is an optional list of TrackTemplate objects
        to refresh.  If not provided, all tracked templates will be
        considered.

        replayed is True if the event is being replayed because the
        rate limit was hit.
        """
        updates: list[TrackTemplateResult] = []
        info_changed = False
        now = event.time_fired_timestamp if not replayed and event else time.time()

        block_updates = False
        super_template = self._track_templates[0] if self._has_super_template else None

        track_templates = track_templates or self._track_templates

        # Update the super template first
        if super_template is not None:
            update = self._render_template_if_ready(super_template, now, event)
            info_changed |= self._apply_update(updates, update, super_template.template)

            if isinstance(update, TrackTemplateResult):
                super_result = update.result
            else:
                super_result = self._last_result.get(super_template.template)

            # If the super template did not render to True, don't update other templates
            if (
                super_result is not None
                and self._super_template_as_boolean(super_result) is not True
            ):
                block_updates = True

            if (
                isinstance(update, TrackTemplateResult)
                and self._super_template_as_boolean(update.last_result) is not True
                and self._super_template_as_boolean(update.result) is True
            ):
                # Super template changed from not True to True, force re-render
                # of all templates in the group
                event = None
                track_templates = self._track_templates

        # Then update the remaining templates unless blocked by the super template
        if not block_updates:
            for track_template_ in track_templates:
                if track_template_ == super_template:
                    continue

                update = self._render_template_if_ready(track_template_, now, event)
                info_changed |= self._apply_update(
                    updates, update, track_template_.template
                )

        if info_changed:
            assert self._track_state_changes
            self._track_state_changes.async_update_listeners(
                _render_infos_to_track_states(
                    [
                        _suppress_domain_all_in_render_info(info)
                        if self._rate_limit.async_has_timer(template)
                        else info
                        for template, info in self._info.items()
                    ]
                )
            )
            _LOGGER.debug(
                (
                    "Template group %s listens for %s, re-render blocked by super"
                    " template: %s"
                ),
                self._track_templates,
                self.listeners,
                block_updates,
            )

        if not updates:
            return

        for track_result in updates:
            self._last_result[track_result.template] = track_result.result

        self.hass.async_run_hass_job(self._job, event, updates)


@callback
def traccia_modelli(
    hass: HomeAssistant,
    track_templates: Sequence[TrackTemplate],
    action: TrackTemplateResultListener,
    strict: bool = False,
    log_fn: Callable[[int, str], None] | None = None,
    has_super_template: bool = False,
) -> TracciaModelli:
    """Come ``async_track_template_result`` (stessi argomenti, stesso oggetto restituito):
    ``action(evento, risultati)`` con il primo risultato e poi a ogni cambio del risultato
    dei modelli; le entità lette (anche i valori interni annotati nel ``RenderInfo``) le
    segue ``segui_cambi``."""
    tracker = TracciaModelli(hass, track_templates, action, has_super_template)
    tracker.async_setup(strict=strict, log_fn=log_fn)
    return tracker


# --- le funzioni sul RenderInfo di helpers/event.py ------------------------------------------


@callback
def _entities_domains_from_render_infos(
    render_infos: Iterable[RenderInfo],
) -> tuple[set[str], set[str]]:
    """Combine from multiple RenderInfo."""
    entities: set[str] = set()
    domains: set[str] = set()

    for render_info in render_infos:
        if render_info.entities:
            entities.update(render_info.entities)
        if render_info.domains:
            domains.update(render_info.domains)
        if render_info.domains_lifecycle:
            domains.update(render_info.domains_lifecycle)
    return entities, domains


@callback
def _render_infos_needs_all_listener(render_infos: Iterable[RenderInfo]) -> bool:
    """Determine if an all listener is needed from RenderInfo."""
    for render_info in render_infos:
        # Tracking all states
        if render_info.all_states or render_info.all_states_lifecycle:
            return True

    return False


@callback
def _render_infos_to_track_states(render_infos: Iterable[RenderInfo]) -> TrackStates:
    """Create a TrackStates dataclass from the latest RenderInfo."""
    if _render_infos_needs_all_listener(render_infos):
        return TrackStates(True, set(), set())

    return TrackStates(False, *_entities_domains_from_render_infos(render_infos))


@callback
def _event_triggers_rerender(
    event: Event[EventStateChangedData], info: RenderInfo
) -> bool:
    """Determine if a template should be re-rendered from an event."""
    entity_id = event.data["entity_id"]

    if info.filter(entity_id):
        return True

    if event.data["new_state"] is not None and event.data["old_state"] is not None:
        return False

    return bool(info.filter_lifecycle(entity_id))


@callback
def _rate_limit_for_event(
    event: Event[EventStateChangedData],
    info: RenderInfo,
    track_template_: TrackTemplate,
) -> float | None:
    """Determine the rate limit for an event."""
    # Specifically referenced entities are excluded
    # from the rate limit
    if event.data["entity_id"] in info.entities:
        return None

    if track_template_.rate_limit is not None:
        return track_template_.rate_limit

    rate_limit: float | None = info.rate_limit
    return rate_limit


def _suppress_domain_all_in_render_info(render_info: RenderInfo) -> RenderInfo:
    """Remove the domains and all_states from render info during a ratelimit."""
    rate_limited_render_info = copy.copy(render_info)
    rate_limited_render_info.all_states = False
    rate_limited_render_info.all_states_lifecycle = False
    rate_limited_render_info.domains = set()
    rate_limited_render_info.domains_lifecycle = set()
    return rate_limited_render_info
