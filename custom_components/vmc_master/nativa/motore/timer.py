"""I timer del package dentro il motore (fase 4).

Oggi ogni VMC ha 34 timer (``timer.vmc_<nome>_*``): sono entità, scrivono il loro stato
nella macchina degli stati e lanciano i loro eventi (``timer.finished``...) sul bus di
Home Assistant. Nell'integrazione nativa diventano timer interni del motore:

- ``TimerMotore`` è un timer: fa esattamente quello che fa
  ``homeassistant.components.timer.entity.Timer`` (stessi stati ``idle``/``active``/
  ``paused``, stessi attributi, stessi istanti, stessi eventi, stesso contesto della
  scrittura), ma il suo stato non va nella macchina degli stati: resta qui
  (``stato_ha``, uno ``State`` uguale a quello che scriverebbe Home Assistant) e lo
  ricevono gli ascoltatori (i sensori con l'istante di fine, StatoVMC);
- i suoi eventi non vanno sul bus di Home Assistant ma su ``BusDelMotore`` (uno per
  ``hass``, per i timer di tutte le VMC, come il bus per tutti i timer di oggi), che li
  consegna ai trigger evento del motore (``TRIGGER``, ``attacca_trigger_timer``) con le
  regole del bus (stesso evento, stesso contesto, eventi lanciati durante una consegna
  messi in coda);
- i servizi (``timer.start``, ``pause``, ``cancel``, ``finish``, ``change``) li chiama il
  codice tradotto con il dominio ``DOMINIO_SERVIZI`` (``Contesto.chiama_servizio``):
  stesso schema dei dati e stessa esecuzione di Home Assistant
  (``helpers.service.entity_service_call``, con i timer del motore al posto delle entità),
  senza l'evento ``call_service``;
- le letture dei modelli (``states``, ``is_state``, ``state_attr`` di un timer) passano da
  ``TimerDelMotore`` (``c.timer``), che risponde per i timer del motore e lascia a Home
  Assistant tutto il resto;
- chi segue un timer del motore (i sensori template che lo leggono) lo segue con
  ``seguire.CambiInterni``: ``TimerDelMotore`` è una sorgente di valori interni.

Il traduttore scrive queste forme solo se glielo si chiede (``traduci.traduzione(...,
timer_motore=True)``); senza, il codice generato è quello di sempre.

Nessun timer del package ha ``restore: true`` (dopo un riavvio ripartono tutti da
``idle``): il ripristino non c'è.
"""

from __future__ import annotations

import logging
import time
from collections import deque
from collections.abc import Callable, Mapping
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

import probatio
from homeassistant.components.timer import CONFIG_SCHEMA as SCHEMA_TIMER
from homeassistant.components.timer.const import (
    ATTR_FINISHED_AT,
    CONF_DURATION,
    CONF_RESTORE,
    DEFAULT_DURATION,
    EVENT_TIMER_CANCELLED,
    EVENT_TIMER_CHANGED,
    EVENT_TIMER_FINISHED,
    EVENT_TIMER_PAUSED,
    EVENT_TIMER_RESTARTED,
    EVENT_TIMER_STARTED,
    STATUS_ACTIVE,
    STATUS_IDLE,
    STATUS_PAUSED,
    TimerEntityStateAttribute,
    TimerServiceArgument,
)
from homeassistant.components.timer.const import (
    DOMAIN as DOMINIO_TIMER,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    CONF_ICON,
    CONF_ID,
    CONF_NAME,
    CONF_PLATFORM,
    EntityStateAttribute,
)
from homeassistant.core import (
    CALLBACK_TYPE,
    Context,
    Event,
    EventOrigin,
    HassJob,
    HomeAssistant,
    ServiceCall,
    State,
    callback,
    get_hassjob_callable_job_type,
)
from homeassistant.exceptions import (
    HomeAssistantError,
    ServiceNotFound,
    ServiceValidationError,
    TemplateError,
)
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity import CONTEXT_RECENT_TIME_SECONDS
from homeassistant.helpers.event import async_track_point_in_utc_time
from homeassistant.helpers.service import entity_service_call
from homeassistant.helpers.template.render_info import render_info_cv
from homeassistant.helpers.template.states import TemplateState
from homeassistant.helpers.translation import async_get_translations
from homeassistant.helpers.trigger import TriggerInfo
from homeassistant.util import dt as dt_util
from homeassistant.util.hass_dict import HassKey
from homeassistant.util.ulid import ulid_at_time

from .attivazioni import aggancia_evento
from .seguire import cambi_interni

if TYPE_CHECKING:
    from .contesto import Contesto

_LOGGER = logging.getLogger(__name__)

DOMINIO_SERVIZI = "motore_timer"
"""Il dominio dei servizi dei timer nel codice tradotto con ``timer_motore``
(``motore_timer.start`` al posto di ``timer.start``): non è un servizio di Home
Assistant, lo esegue ``Contesto.chiama_servizio``."""

TRIGGER = "motore_timer"
"""Il trigger evento dei timer nel codice tradotto con ``timer_motore``
(``{'trigger': 'motore_timer', 'event_type': [...]}``): un trigger ``event`` che ascolta
anche il bus dei timer del motore (``attacca_trigger_timer``)."""

_NON_DATO = object()
"""``rounded`` non dato a ``states()`` (come il valore predefinito di Home Assistant)."""


def durata_testo(delta: timedelta) -> str:
    """Una durata come la scrive il timer di Home Assistant negli attributi
    (``H:MM:SS``, homeassistant/components/timer/entity.py)."""
    total_seconds = delta.total_seconds()
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours)}:{int(minutes):02}:{int(seconds):02}"

EVENTI_TIMER = frozenset(
    {
        EVENT_TIMER_STARTED,
        EVENT_TIMER_RESTARTED,
        EVENT_TIMER_PAUSED,
        EVENT_TIMER_CANCELLED,
        EVENT_TIMER_FINISHED,
        EVENT_TIMER_CHANGED,
    }
)

# I servizi dei timer: metodo del timer e schema dei dati, come li registra
# homeassistant.components.timer.services (con lo schema dei servizi delle entità
# di EntityComponent).
_DURATA = {
    probatio.Optional(
        TimerServiceArgument.DURATION, default=DEFAULT_DURATION
    ): cv.time_period
}
SERVIZI: dict[str, tuple[str, Any]] = {
    "start": ("async_start", cv.make_entity_service_schema(_DURATA)),
    "pause": ("async_pause", cv.make_entity_service_schema(None)),
    "cancel": ("async_cancel", cv.make_entity_service_schema(None)),
    "finish": ("async_finish", cv.make_entity_service_schema(None)),
    "change": ("async_change", cv.make_entity_service_schema(_DURATA)),
}

# Quanti eventi lanciati durante una consegna si mettono in coda al massimo (come il bus).
_MASSIMO_IN_CODA = 1000


class TimerMotore:
    """Un timer del motore: ``homeassistant.components.timer.entity.Timer`` senza entità.

    I metodi ``async_*`` sono quelli del timer di Home Assistant, riga per riga; al posto
    di ``async_write_ha_state`` e di ``hass.bus.async_fire`` c'è ``_scrivi`` (lo stato
    come lo calcolerebbe Home Assistant, agli ascoltatori) e ``BusDelMotore.lancia``.
    Gli attributi di classe e ``async_set_context``, ``async_request_call``,
    ``get_hassjob_type`` sono quello che ``entity_service_call`` legge di un'entità.
    """

    available = True
    should_poll = False
    supported_features = None
    device_class = None
    editable = False  # come un timer del YAML

    def __init__(
        self,
        hass: HomeAssistant,
        registro: TimerDelMotore,
        entity_id: str,
        config: Mapping[str, Any],
    ) -> None:
        self.hass = hass
        self.entity_id = entity_id
        self._registro = registro
        self._config = dict(config)
        if self._config.get(CONF_RESTORE):
            raise ValueError(f"{entity_id}: restore non serve al package")
        self._last_transition: str | None = None
        self._state: str = STATUS_IDLE
        self._configured_duration = cv.time_period_str(self._config[CONF_DURATION])
        self._running_duration: timedelta = self._configured_duration
        self._remaining: timedelta | None = None
        self._end: datetime | None = None
        self._listener: Callable[[], None] | None = None
        self._context: Context | None = None
        self._context_set: float | None = None
        self._job_types: dict[str, Any] = {}
        # l'ultimo stato «scritto» (quello che Home Assistant terrebbe nella macchina degli
        # stati): None prima della prima scrittura
        self.stato_ha: State | None = None

    # --- come Entity ------------------------------------------------------------------------

    @property
    def name(self) -> str | None:
        return self._config.get(CONF_NAME)

    @property
    def icon(self) -> str | None:
        return self._config.get(CONF_ICON)

    @property
    def state(self) -> str:
        return self._state

    @property
    def fine(self) -> datetime | None:
        """L'istante di fine se il timer è attivo (``finishes_at``), altrimenti None."""
        return self._end

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Come ``Timer.extra_state_attributes``."""
        attrs: dict[str, Any] = {
            TimerEntityStateAttribute.DURATION: durata_testo(self._running_duration),
            TimerEntityStateAttribute.EDITABLE: self.editable,
            TimerEntityStateAttribute.LAST_TRANSITION: self._last_transition,
        }
        if self._end is not None:
            attrs[TimerEntityStateAttribute.FINISHES_AT] = self._end.isoformat()
        if self._remaining is not None:
            attrs[TimerEntityStateAttribute.REMAINING] = durata_testo(self._remaining)
        # niente «restore»: Home Assistant lo aggiunge solo se vero, e nessun timer del
        # package lo chiede (rifiutato nel costruttore)
        return attrs

    @callback
    def async_set_context(self, context: Context) -> None:
        """Il contesto della chiamata che comanda il timer (come Entity)."""
        self._context = context
        self._context_set = time.time()

    async def async_request_call[T](self, coro: Any) -> T:
        """Come Entity senza ``parallel_updates``."""
        return await coro  # type: ignore[no-any-return]

    def get_hassjob_type(self, function_name: str) -> Any:
        if function_name not in self._job_types:
            self._job_types[function_name] = get_hassjob_callable_job_type(
                getattr(self, function_name)
            )
        return self._job_types[function_name]

    @callback
    def async_write_ha_state(self) -> None:
        """Lo stato come lo scriverebbe Home Assistant (``Entity._async_write_ha_state``
        e ``StateMachine.async_set_internal`` con ``force_update``: ogni scrittura è un
        cambio, ``last_changed`` compreso), dato agli ascoltatori invece che alla macchina
        degli stati."""
        time_now = time.time()
        attributi = dict(self.extra_state_attributes)
        if (icona := self.icon) is not None:
            attributi[EntityStateAttribute.ICON] = icona
        if nome := self.name:
            attributi[EntityStateAttribute.FRIENDLY_NAME] = nome
        if (
            self._context_set is not None
            and time_now - self._context_set > CONTEXT_RECENT_TIME_SECONDS
        ):
            self._context = None
            self._context_set = None
        contesto = self._context or Context(id=ulid_at_time(time_now))
        adesso = dt_util.utc_from_timestamp(time_now)
        vecchio = self.stato_ha
        if vecchio is not None and vecchio.attributes == attributi:
            attributi = vecchio.attributes  # type: ignore[assignment]
        self.stato_ha = State(
            self.entity_id,
            self._state,
            attributi,
            None,
            adesso,
            adesso,
            contesto,
            vecchio is None,
            None,
            time_now,
        )
        self._registro._scritto(self)

    # --- come Timer -------------------------------------------------------------------------

    @callback
    def async_start(self, duration: timedelta | None = None) -> None:
        """Start a timer."""
        if self._listener:
            self._listener()
            self._listener = None

        event = EVENT_TIMER_STARTED
        if self._state in (STATUS_ACTIVE, STATUS_PAUSED):
            event = EVENT_TIMER_RESTARTED

        self._state = STATUS_ACTIVE
        start = dt_util.utcnow().replace(microsecond=0)

        # Set remaining and running duration unless resuming or restarting
        if duration:
            self._remaining = self._running_duration = duration
        elif not self._remaining:
            self._remaining = self._running_duration

        self._end = start + self._remaining

        self._listener = async_track_point_in_utc_time(
            self.hass, self._async_finished, self._end
        )

        self._fire_event_and_write_state(event)

    @callback
    def async_change(self, duration: timedelta) -> None:
        """Change duration of a running timer."""
        if self._listener is None or self._end is None:
            raise self._registro.errore("timer_not_running", self.entity_id)
        # Check against new remaining time before checking boundaries
        new_remaining = (self._end + duration) - dt_util.utcnow().replace(microsecond=0)
        if self._remaining and new_remaining > self._running_duration:
            raise self._registro.errore("change_beyond_duration", self.entity_id)
        if self._remaining and (self._remaining + duration) < timedelta():
            raise self._registro.errore("change_negative_remaining", self.entity_id)

        self._listener()
        self._end += duration
        self._remaining = new_remaining
        self._listener = async_track_point_in_utc_time(
            self.hass, self._async_finished, self._end
        )
        # come Timer: senza toccare last_transition
        self.async_write_ha_state()
        self._registro.lancia(EVENT_TIMER_CHANGED, {ATTR_ENTITY_ID: self.entity_id})

    @callback
    def async_pause(self) -> None:
        """Pause a timer."""
        if self._listener is None or self._end is None:
            return

        self._listener()
        self._listener = None
        self._remaining = self._end - dt_util.utcnow().replace(microsecond=0)
        self._state = STATUS_PAUSED
        self._end = None
        self._fire_event_and_write_state(EVENT_TIMER_PAUSED)

    @callback
    def async_cancel(self) -> None:
        """Cancel a timer."""
        if self._state == STATUS_IDLE:
            return

        if self._listener:
            self._listener()
            self._listener = None
        self._state = STATUS_IDLE
        self._end = None
        self._remaining = None
        self._running_duration = self._configured_duration
        self._fire_event_and_write_state(EVENT_TIMER_CANCELLED)

    @callback
    def async_finish(self) -> None:
        """Reset and updates the states, fire finished event."""
        if self._state == STATUS_IDLE:
            return

        if self._listener:
            self._listener()
            self._listener = None
        end = self._end
        if end is None:
            end = dt_util.utcnow().replace(microsecond=0)
        self._state = STATUS_IDLE
        self._end = None
        self._remaining = None
        self._running_duration = self._configured_duration
        self._fire_event_and_write_state(
            EVENT_TIMER_FINISHED, extra_attrs={ATTR_FINISHED_AT: end.isoformat()}
        )

    @callback
    def _async_finished(self, time: datetime) -> None:
        """Reset and updates the states, fire finished event."""
        if self._state != STATUS_ACTIVE or self._end is None:
            return

        self._listener = None
        self._state = STATUS_IDLE
        end = self._end
        self._end = None
        self._remaining = None
        self._running_duration = self._configured_duration
        self._fire_event_and_write_state(
            EVENT_TIMER_FINISHED, extra_attrs={ATTR_FINISHED_AT: end.isoformat()}
        )

    def _fire_event_and_write_state(
        self, event: str, *, extra_attrs: dict[str, Any] | None = None
    ) -> None:
        """Fire the event and write state."""
        self._last_transition = event.partition(".")[2]
        self.async_write_ha_state()
        event_data = {ATTR_ENTITY_ID: self.entity_id}
        if extra_attrs:
            event_data.update(extra_attrs)
        self._registro.lancia(event, event_data)

    @callback
    def ferma(self) -> None:
        """Come ``async_will_remove_from_hass``: il timer non scatta più."""
        if self._listener:
            self._listener()
            self._listener = None


Ascoltatore = Callable[[TimerMotore], None]


def _annota(entity_id: str) -> None:
    """La lettura di un'entità nel ``RenderInfo`` del modello che si sta rendendo, come
    ``_collect_state`` di Home Assistant (``is_state``, ``state_attr``)."""
    if (info := render_info_cv.get()) is not None and info.collecting:
        info.entities.add(entity_id)  # type: ignore[attr-defined]


class TimerDelMotore:
    """I timer del motore di una VMC (``c.timer``): servizi, letture dei modelli,
    eventi e ascoltatori.

    ``configurazione`` è quella della chiave ``timer:`` del package (oggetto -> nome,
    icona, durata), validata con lo schema di Home Assistant.
    """

    def __init__(
        self,
        c: Contesto,
        configurazione: Mapping[str, Mapping[str, Any] | None],
    ) -> None:
        self.c = c
        self.hass = hass = c.hass
        voci = SCHEMA_TIMER({DOMINIO_TIMER: dict(configurazione)})[DOMINIO_TIMER]
        self.timer: dict[str, TimerMotore] = {
            f"{DOMINIO_TIMER}.{oggetto}": TimerMotore(
                hass, self, f"{DOMINIO_TIMER}.{oggetto}", {CONF_ID: oggetto, **voce}
            )
            for oggetto, voce in voci.items()
        }
        self.bus = bus_del_motore(hass)
        self._ascoltatori_timer: dict[str | None, list[Ascoltatore]] = {}
        self._testi_errori: dict[str, str] = {}
        # chi segue un timer del motore lo segue da qui (prima di ogni iscrizione)
        self._togli_sorgente: CALLBACK_TYPE | None = cambi_interni(hass).aggiungi(self)
        # come l'aggiunta delle entità: la prima scrittura, idle, senza eventi
        for timer in self.timer.values():
            timer.async_write_ha_state()

    async def prepara(self) -> None:
        """I testi degli errori dei servizi dei timer (``timer_not_running``...), in
        inglese come li scrive Home Assistant (``async_get_exception_message``): Home
        Assistant li ha perché l'integrazione ``timer`` è avviata; il motore li legge
        dalle traduzioni dell'integrazione."""
        self._testi_errori = await async_get_translations(
            self.hass, "en", "exceptions", [DOMINIO_TIMER]
        )

    def errore(self, chiave: str, entity_id: str) -> ServiceValidationError:
        """L'errore di un servizio dei timer, uguale a quello di Home Assistant: stessa
        traduzione e lo stesso testo (quello che ``async_get_exception_message`` calcola
        dalle traduzioni dell'integrazione ``timer``)."""
        segnaposto = {"entity_id": entity_id}
        testo = self._testi_errori.get(
            f"component.{DOMINIO_TIMER}.exceptions.{chiave}.message"
        )
        argomenti = (testo.rstrip(".").format(**segnaposto),) if testo else ()
        return ServiceValidationError(
            *argomenti,
            translation_domain=DOMINIO_TIMER,
            translation_key=chiave,
            translation_placeholders=segnaposto,
        )

    # --- la sorgente di CambiInterni ----------------------------------------------------------

    def contiene(self, entity_id: str) -> bool:
        """Se ``entity_id`` è un timer del motore."""
        return entity_id in self.timer

    def stato(self, entity_id: str) -> State | None:
        """Lo stato di un timer del motore (quello che Home Assistant terrebbe)."""
        timer = self.timer.get(entity_id)
        return None if timer is None else timer.stato_ha

    # --- ascolto ----------------------------------------------------------------------------

    @callback
    def ascolta(
        self, funzione: Ascoltatore, entity_id: str | None = None
    ) -> CALLBACK_TYPE:
        """``funzione(timer)`` a ogni scrittura di un timer (di ``entity_id``, o di tutti),
        nel punto in cui Home Assistant scrive lo stato, prima dell'evento; restituisce
        come smettere."""
        elenco = self._ascoltatori_timer.setdefault(entity_id, [])
        elenco.append(funzione)

        @callback
        def smetti() -> None:
            elenco.remove(funzione)

        return smetti

    @callback
    def _scritto(self, timer: TimerMotore) -> None:
        for chiave in (timer.entity_id, None):
            if elenco := self._ascoltatori_timer.get(chiave):
                for funzione in list(elenco):
                    funzione(timer)

    @callback
    def lancia(self, tipo: str, dati: dict[str, Any]) -> None:
        """Un evento di un timer sul bus del motore."""
        self.bus.lancia(tipo, dati)

    @callback
    def ferma(self) -> None:
        for timer in self.timer.values():
            timer.ferma()
        if self._togli_sorgente is not None:
            self._togli_sorgente()
            self._togli_sorgente = None

    # --- servizi ----------------------------------------------------------------------------

    async def servizio(
        self,
        servizio: str,
        dati: dict[str, Any],
        bersaglio: dict[str, Any] | None,
        contesto: Context | None,
    ) -> None:
        """Un servizio dei timer come ``ServiceRegistry.async_call(blocking=True)`` del
        servizio di Home Assistant: i dati con il bersaglio, lo schema del servizio, poi
        ``entity_service_call`` sui timer del motore (lo stesso codice di Home Assistant:
        utente, entità mancanti, una chiamata o un compito per timer). Niente evento
        ``call_service``: non è più un servizio di Home Assistant."""
        if servizio not in SERVIZI:
            raise ServiceNotFound(DOMINIO_TIMER, servizio)
        metodo, schema = SERVIZI[servizio]
        contesto = contesto or Context()
        dati = dati or {}
        if bersaglio:
            dati.update(bersaglio)
        elaborati = schema(dati)
        chiamata = ServiceCall(
            self.hass, DOMINIO_TIMER, servizio, elaborati, contesto, False
        )
        await entity_service_call(self.hass, self.timer, metodo, chiamata)

    # --- letture dei modelli ----------------------------------------------------------------

    def _letto(self, entity_id: Any) -> TimerMotore | None:
        """Il timer del motore di un entity_id letto da un modello (come
        ``StateMachine.get``: anche in maiuscolo), o None."""
        if not isinstance(entity_id, str):
            return None
        return self.timer.get(entity_id) or self.timer.get(entity_id.lower())

    def states(
        self,
        entity_id: Any,
        rounded: bool | object = _NON_DATO,
        with_unit: bool = False,
    ) -> str:
        """``states(entity_id)`` (come ``AllStates.__call__``).

        Come in Home Assistant la lettura si annota nel ``RenderInfo`` del modello (se
        c'è): un sensore template che legge un timer lo segue, e i cambi dei timer del
        motore gli arrivano con ``sensori_template.AnnunciDeiTimer``. I trigger e le
        attese non leggono mai i timer del motore (lo controlla il traduttore)."""
        if rounded is _NON_DATO:
            # come Home Assistant: senza ``rounded`` vale ``with_unit``
            rounded = with_unit
        if (timer := self._letto(entity_id)) is None:
            return self.c.states(entity_id, rounded, with_unit)  # type: ignore[no-any-return]
        stato = TemplateState(self.hass, timer.stato_ha, collect=True)  # type: ignore[arg-type]
        if rounded or with_unit:
            return stato.format_state(rounded, with_unit)  # type: ignore[arg-type]
        return stato.state

    def is_state(self, entity_id: Any, state: Any) -> bool:
        """``is_state(entity_id, state)`` (come in Home Assistant)."""
        if (timer := self._letto(entity_id)) is None:
            return self.c.is_state(entity_id, state)  # type: ignore[no-any-return]
        _annota(timer.entity_id)
        valore = timer.state
        return valore == state or (isinstance(state, list) and valore in state)

    def state_attr(self, entity_id: Any, name: Any) -> Any:
        """``state_attr(entity_id, name)`` (come in Home Assistant)."""
        if (timer := self._letto(entity_id)) is None:
            return self.c.state_attr(entity_id, name)
        _annota(timer.entity_id)
        return timer.stato_ha.attributes.get(name)  # type: ignore[union-attr]

    def filtro(self, nome: str) -> Callable[..., Any]:
        """Il filtro ``states`` o ``state_attr`` (come la funzione)."""
        return {"states": self.states, "state_attr": self.state_attr}[nome]

    def test(self, nome: str) -> Callable[..., Any]:
        """Il test ``is_state`` (come la funzione)."""
        return {"is_state": self.is_state}[nome]

    def oggetto(self, entity_id: str) -> Any:
        """``states.<dominio>.<oggetto>`` di un modello (come ``Contesto.oggetto``)."""
        if (timer := self._letto(entity_id)) is None:
            return self.c.oggetto(entity_id)
        return TemplateState(self.hass, timer.stato_ha, collect=True)  # type: ignore[arg-type]

    @property
    def stati(self) -> _StatiConTimer:
        """``states`` di un modello per ``states[entity_id]``."""
        return _StatiConTimer(self)


class _StatiConTimer:
    """``states[chiave]`` di un modello con i timer del motore: lo stato di un timer del
    motore come lo darebbe Home Assistant, ``states[chiave]`` di Home Assistant per il
    resto. ``states['timer']`` (gli stati di tutti i timer) non c'è: i timer del motore
    non sono nella macchina degli stati."""

    __slots__ = ("_registro",)

    def __init__(self, registro: TimerDelMotore) -> None:
        self._registro = registro

    def __getitem__(self, chiave: Any) -> Any:
        registro = self._registro
        if (timer := registro._letto(chiave)) is not None:
            return TemplateState(registro.hass, timer.stato_ha, collect=False)  # type: ignore[arg-type]
        if isinstance(chiave, str) and chiave == DOMINIO_TIMER:
            raise TemplateError(
                "states['timer']: i timer del motore non sono nella macchina degli stati"
            )
        return registro.c.states[chiave]


def configurazione_del_package(nome: str) -> dict[str, dict[str, Any]]:
    """I timer del package per la VMC ``nome`` (come la chiave ``timer:`` del package:
    ``vmc_<nome>_<oggetto>`` -> nome, icona, durata), dalle impostazioni di
    ``tabelle.py``. Nessun timer ha ``restore``."""
    from ..tabelle import IMPOSTAZIONI

    return {
        f"vmc_{nome}_{chiave.split('.', 1)[1]}": dict(voce)
        for chiave, voce in IMPOSTAZIONI.items()
        if chiave.startswith(f"{DOMINIO_TIMER}.")
    }


# --- il bus degli eventi dei timer del motore --------------------------------------------------


class BusDelMotore:
    """Gli eventi dei timer del motore (di tutte le VMC), come ``EventBus`` per gli eventi
    dei timer di Home Assistant: stessi ascoltatori (un ``HassJob`` e un filtro dei dati),
    nello stesso ordine; un evento lanciato mentre se ne consegna un altro si mette in coda
    e si consegna dopo (come ``async_fire_internal``)."""

    def __init__(self, hass: HomeAssistant) -> None:
        self._hass = hass
        self._ascoltatori: dict[str, list[tuple[HassJob[..., Any], Any]]] = {}
        self._in_consegna = False
        self._coda: deque[tuple[str, dict[str, Any], float]] = deque()
        self._in_coda = 0

    @callback
    def async_listen(
        self,
        event_type: str,
        listener: Callable[[Event[Any]], Any],
        event_filter: Callable[[Mapping[str, Any]], bool] | None = None,
    ) -> CALLBACK_TYPE:
        voce = (HassJob(listener, f"listen {event_type}"), event_filter)
        self._ascoltatori.setdefault(event_type, []).append(voce)

        @callback
        def togli() -> None:
            self._ascoltatori[event_type].remove(voce)

        return togli

    @callback
    def lancia(self, tipo: str, dati: dict[str, Any]) -> None:
        if self._in_consegna:
            if self._in_coda >= _MASSIMO_IN_CODA:
                raise HomeAssistantError(
                    f"Event {tipo} not fired: more than {_MASSIMO_IN_CODA} events were"
                    " queued by event listeners while dispatching a single event"
                )
            self._in_coda += 1
            self._coda.append((tipo, dati, time.time()))
            return
        self._in_consegna = True
        self._in_coda = 0
        try:
            self._consegna(tipo, dati, None)
            while self._coda:
                self._consegna(*self._coda.popleft())
        finally:
            self._in_consegna = False

    def _consegna(self, tipo: str, dati: dict[str, Any], istante: float | None) -> None:
        evento: Event[Any] | None = None
        for job, filtro in list(self._ascoltatori.get(tipo, ())):
            if filtro is not None:
                try:
                    if not filtro(dati):
                        continue
                except Exception:
                    _LOGGER.exception("Error in event filter")
                    continue
            if evento is None:
                evento = Event(tipo, dati, EventOrigin.local, istante, None)
            try:
                self._hass.async_run_hass_job(job, evento)
            except Exception:
                _LOGGER.exception("Error running job: %s", job)


_BUS: HassKey[BusDelMotore] = HassKey("vmc_master_bus_dei_timer")


def bus_del_motore(hass: HomeAssistant) -> BusDelMotore:
    """Il bus dei timer del motore di ``hass`` (uno per tutte le VMC)."""
    if (bus := hass.data.get(_BUS)) is None:
        bus = hass.data[_BUS] = BusDelMotore(hass)
    return bus


# --- il trigger evento dei timer -------------------------------------------------------------


async def attacca_trigger_timer(
    hass: HomeAssistant,
    conf: Mapping[str, Any],
    action: Callable[..., Any],
    info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Il trigger ``TRIGGER`` (``motore_timer``): un trigger ``event`` (lo stesso codice,
    ``attivazioni.aggancia_evento``) due volte: sul bus di Home Assistant, per gli eventi
    dei timer che restano entità; poi sul bus dei timer del motore."""
    conf_evento = {**conf, CONF_PLATFORM: "event"}
    togli = [
        await aggancia_evento(hass, conf_evento, action, info),
        await aggancia_evento(hass, conf_evento, action, info, bus=bus_del_motore(hass)),
    ]

    @callback
    def togli_tutto() -> None:
        for una in togli:
            una()

    return togli_tutto
