"""Le attivazioni (trigger) delle automazioni del motore, con il proprio codice.

``inizializza_attivazioni`` fa quello che fa ``helpers.trigger.async_initialize_triggers``
di Home Assistant con le configurazioni dei trigger come le ha il motore (quelle che Home
Assistant valida dal package, scritte nel codice tradotto: ``entity_id`` in una lista,
``for`` come ``timedelta`` o come dizionario di modelli, ``event_type`` come lista di
``Template``, ``at`` come lista di ``datetime.time``...): salta i trigger spenti
(``enabled``, anche come modello), dà ``id`` (l'indice se manca), ``idx`` e ``alias``,
aggiunge le ``variables`` del trigger, aggancia ogni trigger in un compito che parte subito
e restituisce come staccarli tutti; gli errori vanno a ``log_cb`` come in Home Assistant.

Le piattaforme sono quelle che usa il motore, riportate qui riga per riga da Home
Assistant 2026.11.2 (Apache-2.0, licenza nel file ``LICENSE-Apache-2.0.txt``
dell'integrazione), con ``seguire.py`` al posto del tracciamento di Home Assistant, così i
trigger seguono anche i valori interni del motore:

- ``state``: ``homeassistant/components/homeassistant/triggers/state.py``;
- ``template``: ``homeassistant/components/template/trigger.py``;
- ``event``: ``homeassistant/components/homeassistant/triggers/event.py`` (con il bus da
  ascoltare come argomento, per i trigger dei timer del motore);
- ``homeassistant``: ``homeassistant/components/homeassistant/triggers/homeassistant.py``;
- ``time``: ``homeassistant/components/homeassistant/triggers/time.py`` (anche con le ore
  da un'entità ``input_datetime`` o da un sensore con un istante);
- ``time_pattern``: ``homeassistant/components/homeassistant/triggers/time_pattern.py``;
- ``inizializza_attivazioni`` e ``_avvolgi_azione``: ``homeassistant/helpers/trigger/
  __init__.py`` (``async_initialize_triggers``, ``_trigger_action_wrapper``).

Le variabili ``trigger`` di ogni piattaforma sono quelle di Home Assistant. Le piattaforme
che ha solo il motore (il trigger dei timer del motore) arrivano con ``altri``.
"""

from __future__ import annotations

import asyncio
import functools
import inspect
import logging
from collections.abc import Callable, Coroutine, ItemsView, Mapping
from datetime import datetime, timedelta
from functools import partial
from typing import Any, NamedTuple, Protocol, cast

import probatio
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import (
    CONF_ALIAS,
    CONF_AT,
    CONF_ENABLED,
    CONF_ENTITY_ID,
    CONF_EVENT,
    CONF_FOR,
    CONF_ID,
    CONF_OFFSET,
    CONF_PLATFORM,
    CONF_VALUE_TEMPLATE,
    CONF_VARIABLES,
    CONF_WEEKDAY,
    EVENT_HOMEASSISTANT_STARTED,
    EVENT_STATE_REPORTED,
    MATCH_ALL,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
    WEEKDAYS,
    EntityStateAttribute,
)
from homeassistant.core import (
    CALLBACK_TYPE,
    Context,
    Event,
    EventStateChangedData,
    HassJob,
    HomeAssistant,
    State,
    callback,
    is_callback,
)
from homeassistant.exceptions import HomeAssistantError, TemplateError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import template
from homeassistant.helpers.event import (
    TrackTemplate,
    TrackTemplateResult,
    async_call_later,
    async_track_point_in_time,
    async_track_time_change,
    process_state_match,
)
from homeassistant.helpers.template import Template, result_as_boolean
from homeassistant.helpers.trigger import TriggerActionType, TriggerData, TriggerInfo
from homeassistant.helpers.typing import ConfigType
from homeassistant.util import dt as dt_util
from homeassistant.util.async_ import create_eager_task

from .seguire import segui_cambi, segui_stesso_stato, stato_di, traccia_modelli

_LOGGER = logging.getLogger(__name__)

Aggancio = Callable[
    [HomeAssistant, ConfigType, TriggerActionType, TriggerInfo],
    Coroutine[Any, Any, CALLBACK_TYPE],
]
"""Come si aggancia un trigger di una piattaforma (``async_attach_trigger``)."""


class BusDegliEventi(Protocol):
    """Il bus che ascolta un trigger ``event``: quello di Home Assistant
    (``hass.bus``) o uno con lo stesso ``async_listen`` (``timer.BusDelMotore``)."""

    def async_listen(
        self,
        event_type: str,
        listener: Callable[[Event[Any]], Any],
        event_filter: Callable[[Mapping[str, Any]], bool] | None = None,
    ) -> CALLBACK_TYPE:
        """Ascolta gli eventi ``event_type``; restituisce come smettere."""


# --- async_initialize_triggers --------------------------------------------------------------


def _avvolgi_azione(
    hass: HomeAssistant, action: Callable[..., Any], conf: ConfigType
) -> Callable[..., Any]:
    """Come ``_trigger_action_wrapper``: l'azione con le ``variables`` del trigger, se ci
    sono (una coroutine per una coroutine, un callback per un callback)."""
    if CONF_VARIABLES not in conf:
        return action

    # Check for partials to properly determine if coroutine function
    check_func = action
    while isinstance(check_func, functools.partial):
        check_func = check_func.func

    wrapper_func: Callable[..., Any] | Callable[..., Coroutine[Any, Any, Any]]
    if inspect.iscoroutinefunction(check_func):
        async_action = cast(Callable[..., Coroutine[Any, Any, Any]], action)

        @functools.wraps(async_action)
        async def async_with_vars(
            run_variables: dict[str, Any], context: Context | None = None
        ) -> Any:
            """Wrap action with extra vars."""
            trigger_variables = conf[CONF_VARIABLES]
            run_variables.update(trigger_variables.async_render(hass, run_variables))
            return await action(run_variables, context)

        wrapper_func = async_with_vars

    else:

        @functools.wraps(action)
        def with_vars(
            run_variables: dict[str, Any], context: Context | None = None
        ) -> Any:
            """Wrap action with extra vars."""
            trigger_variables = conf[CONF_VARIABLES]
            run_variables.update(trigger_variables.async_render(hass, run_variables))
            return action(run_variables, context)

        if is_callback(check_func):
            with_vars = callback(with_vars)

        wrapper_func = with_vars

    return wrapper_func


def _piattaforma(trigger_key: str, altri: Mapping[str, Aggancio] | None) -> Aggancio:
    """La funzione che aggancia i trigger ``trigger_key``: una di ``altri``, poi una di
    quelle di qui; per le altre lo stesso errore di Home Assistant per un trigger che non
    conosce."""
    if altri is not None and (aggancio := altri.get(trigger_key)) is not None:
        return aggancio
    if (aggancio := PIATTAFORME.get(trigger_key)) is not None:
        return aggancio
    raise probatio.Invalid(f"Invalid trigger '{trigger_key}' specified")


async def inizializza_attivazioni(
    hass: HomeAssistant,
    trigger_config: list[ConfigType],
    action: Callable[..., Any],
    domain: str,
    name: str,
    log_cb: Callable[..., Any],
    home_assistant_start: bool = False,
    variables: Any = None,
    altri: Mapping[str, Aggancio] | None = None,
) -> CALLBACK_TYPE | None:
    """Come ``async_initialize_triggers`` (le stesse righe), con le piattaforme di qui e
    quelle di ``altri`` (nome del trigger -> funzione che lo aggancia, chiamata come le
    piattaforme di qui: ``(hass, conf, azione avvolta, trigger_info)``).

    ``home_assistant_start`` non ha effetto (in Home Assistant 2026.11 è deprecato e non
    fa più nulla). Restituisce come staccare tutti i trigger, o None se nessuno si è
    agganciato."""
    del home_assistant_start
    triggers: list[asyncio.Task[CALLBACK_TYPE]] = []
    for idx, conf in enumerate(trigger_config):
        # Skip triggers that are not enabled
        if CONF_ENABLED in conf:
            enabled = conf[CONF_ENABLED]
            if isinstance(enabled, Template):
                try:
                    enabled = enabled.async_render(variables, limited=True)
                except TemplateError as err:
                    log_cb(logging.ERROR, f"Error rendering enabled template: {err}")
                    continue
            if not enabled:
                continue

        trigger_key: str = conf[CONF_PLATFORM]
        aggancia = _piattaforma(trigger_key, altri)
        trigger_id = conf.get(CONF_ID, f"{idx}")
        trigger_idx = f"{idx}"
        trigger_alias = conf.get(CONF_ALIAS)
        trigger_data = TriggerData(id=trigger_id, idx=trigger_idx, alias=trigger_alias)
        info = TriggerInfo(
            domain=domain,
            name=name,
            variables=variables,
            trigger_data=trigger_data,
        )

        action_wrapper = _avvolgi_azione(hass, action, conf)
        coro = aggancia(hass, conf, action_wrapper, info)

        triggers.append(create_eager_task(coro))

    attach_results = await asyncio.gather(*triggers, return_exceptions=True)
    removes: list[Callable[[], None]] = []

    for result in attach_results:
        if isinstance(result, HomeAssistantError):
            log_cb(logging.ERROR, f"Got error '{result}' when setting up triggers for")
        elif isinstance(result, Exception):
            log_cb(logging.ERROR, "Error setting up trigger", exc_info=result)
        elif isinstance(result, BaseException):
            raise result from None
        elif result is None:
            log_cb(  # type: ignore[unreachable]
                logging.ERROR, "Unknown error while setting up trigger (empty result)"
            )
        else:
            removes.append(result)

    if not removes:
        return None

    log_cb(logging.INFO, "Initialized trigger")

    @callback
    def remove_triggers() -> None:
        """Remove triggers."""
        for remove in removes:
            remove()

    return remove_triggers


# --- state ----------------------------------------------------------------------------------

CONF_FROM = "from"
CONF_TO = "to"
CONF_NOT_FROM = "not_from"
CONF_NOT_TO = "not_to"
CONF_ATTRIBUTE = "attribute"


async def aggancia_stato(
    hass: HomeAssistant,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
    *,
    platform_type: str = "state",
) -> CALLBACK_TYPE:
    """Il trigger ``state`` (come ``triggers/state.py``), con ``segui_cambi`` e
    ``segui_stesso_stato``."""
    entity_ids = config[CONF_ENTITY_ID]

    if (from_state := config.get(CONF_FROM)) is not None:
        match_from_state = process_state_match(from_state)
    elif (not_from_state := config.get(CONF_NOT_FROM)) is not None:
        match_from_state = process_state_match(not_from_state, invert=True)
    else:
        match_from_state = process_state_match(MATCH_ALL)

    if (to_state := config.get(CONF_TO)) is not None:
        match_to_state = process_state_match(to_state)
    elif (not_to_state := config.get(CONF_NOT_TO)) is not None:
        match_to_state = process_state_match(not_to_state, invert=True)
    else:
        match_to_state = process_state_match(MATCH_ALL)

    time_delta = config.get(CONF_FOR)
    # If neither CONF_FROM or CONF_TO are specified,
    # fire on all changes to the state or an attribute
    match_all = all(
        item not in config for item in (CONF_FROM, CONF_NOT_FROM, CONF_NOT_TO, CONF_TO)
    )
    unsub_track_same: dict[str, Callable[[], None]] = {}
    period: dict[str, timedelta] = {}
    attribute = config.get(CONF_ATTRIBUTE)
    job = HassJob(action, f"state trigger {trigger_info}")

    trigger_data = trigger_info["trigger_data"]
    _variables = trigger_info["variables"] or {}

    @callback
    def state_automation_listener(event: Event[EventStateChangedData]) -> None:
        """Listen for state changes and calls action."""
        entity = event.data["entity_id"]
        from_s = event.data["old_state"]
        to_s = event.data["new_state"]

        if from_s is None:
            old_value = None
        elif attribute is None:
            old_value = from_s.state
        else:
            old_value = from_s.attributes.get(attribute)

        if to_s is None:
            new_value = None
        elif attribute is None:
            new_value = to_s.state
        else:
            new_value = to_s.attributes.get(attribute)

        # When we listen for state changes with `match_all`, we
        # will trigger even if just an attribute changes. When
        # we listen to just an attribute, we should ignore all
        # other attribute changes.
        if attribute is not None and old_value == new_value:
            return

        if (
            not match_from_state(old_value)
            or not match_to_state(new_value)
            or (not match_all and old_value == new_value)
        ):
            return

        @callback
        def call_action() -> None:
            """Call action with right context."""
            hass.async_run_hass_job(
                job,
                {
                    "trigger": {
                        **trigger_data,
                        "platform": platform_type,
                        "entity_id": entity,
                        "from_state": from_s,
                        "to_state": to_s,
                        "for": time_delta if not time_delta else period[entity],
                        "attribute": attribute,
                        "description": f"state of {entity}",
                    }
                },
                event.context,
            )

        if not time_delta:
            call_action()
            return

        data = {
            "trigger": {
                "platform": "state",
                "entity_id": entity,
                "from_state": from_s,
                "to_state": to_s,
            }
        }
        variables = {**_variables, **data}

        try:
            period[entity] = cv.positive_time_period(
                template.render_complex(time_delta, variables)
            )
        except (TemplateError, probatio.Invalid) as ex:
            _LOGGER.error(
                "Error rendering '%s' for template: %s", trigger_info["name"], ex
            )
            return

        def _check_same_state(_: str, _2: State | None, new_st: State | None) -> bool:
            if new_st is None:
                return False

            cur_value: str | None
            if attribute is None:
                cur_value = new_st.state
            else:
                cur_value = new_st.attributes.get(attribute)

            if CONF_FROM in config and CONF_TO not in config:
                return cur_value != old_value

            return cur_value == new_value

        unsub_track_same[entity] = segui_stesso_stato(
            hass,
            period[entity],
            call_action,
            _check_same_state,
            entity_ids=entity,
        )

    unsub = segui_cambi(hass, entity_ids, state_automation_listener)

    @callback
    def async_remove() -> None:
        """Remove state listeners async."""
        unsub()
        for async_remove in unsub_track_same.values():
            async_remove()
        unsub_track_same.clear()

    return async_remove


# --- template -------------------------------------------------------------------------------


async def aggancia_modello(
    hass: HomeAssistant,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
    *,
    platform_type: str = "template",
) -> CALLBACK_TYPE:
    """Il trigger ``template`` (come ``template/trigger.py``), con ``traccia_modelli``."""
    trigger_data = trigger_info["trigger_data"]
    variables = trigger_info["variables"] or {}
    value_template: Template = config[CONF_VALUE_TEMPLATE]
    time_delta = config.get(CONF_FOR)
    delay_cancel = None
    job = HassJob(action)
    armed = False

    # Arm at setup if the template is already false.
    try:
        if not result_as_boolean(value_template.async_render(variables)):
            armed = True
    except TemplateError as ex:
        _LOGGER.warning(
            "Error initializing 'template' trigger for '%s': %s",
            trigger_info["name"],
            ex,
        )

    @callback
    def template_listener(
        event: Event[EventStateChangedData] | None,
        updates: list[TrackTemplateResult],
    ) -> None:
        """Listen for state changes and calls action."""
        nonlocal delay_cancel, armed
        result = updates.pop().result

        if isinstance(result, TemplateError):
            _LOGGER.warning(
                "Error evaluating 'template' trigger for '%s': %s",
                trigger_info["name"],
                result,
            )
            return

        if delay_cancel:
            delay_cancel()
            delay_cancel = None

        if not result_as_boolean(result):
            armed = True
            return

        # Only fire when previously armed.
        if not armed:
            return

        # Fire!
        armed = False

        entity_id = event and event.data["entity_id"]
        from_s = event and event.data["old_state"]
        to_s = event and event.data["new_state"]

        if entity_id is not None:
            description = f"{entity_id} via template"
        else:
            description = "time change or manual update via template"

        template_variables = {
            "platform": platform_type,
            "entity_id": entity_id,
            "from_state": from_s,
            "to_state": to_s,
        }
        trigger_variables = {
            **trigger_data,
            "for": time_delta,
            "description": description,
        }

        @callback
        def call_action(*_: Any) -> None:
            """Call action with right context."""
            nonlocal trigger_variables
            hass.async_run_hass_job(
                job,
                {"trigger": {**template_variables, **trigger_variables}},
                (to_s.context if to_s else None),
            )

        if not time_delta:
            call_action()
            return

        data = {"trigger": template_variables}
        period_variables = {**variables, **data}

        try:
            period: timedelta = cv.positive_time_period(
                template.render_complex(time_delta, period_variables)
            )
        except (TemplateError, probatio.Invalid) as ex:
            _LOGGER.error(
                "Error rendering '%s' for template: %s", trigger_info["name"], ex
            )
            return

        trigger_variables["for"] = period

        delay_cancel = async_call_later(hass, period.total_seconds(), call_action)

    info = traccia_modelli(
        hass,
        [TrackTemplate(value_template, variables)],
        template_listener,
    )
    unsub = info.async_remove

    @callback
    def async_remove() -> None:
        """Remove state listeners async."""
        unsub()
        if delay_cancel:
            delay_cancel()

    return async_remove


# --- event ----------------------------------------------------------------------------------

CONF_EVENT_TYPE = "event_type"
CONF_EVENT_DATA = "event_data"
CONF_EVENT_CONTEXT = "context"


def _schema_value(value: Any) -> Any:
    if isinstance(value, list):
        return probatio.In(value)

    return value


async def aggancia_evento(
    hass: HomeAssistant,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
    *,
    platform_type: str = "event",
    bus: BusDegliEventi | None = None,
) -> CALLBACK_TYPE:
    """Il trigger ``event`` (come ``triggers/event.py``) sul bus di Home Assistant, o su
    ``bus`` (per esempio il bus dei timer del motore). Il contesto dell'evento si legge con
    ``Context.as_dict()``."""
    trigger_data = trigger_info["trigger_data"]
    variables = trigger_info["variables"]
    if bus is None:
        bus = hass.bus

    event_types = template.render_complex(
        config[CONF_EVENT_TYPE], variables, limited=True
    )
    if EVENT_STATE_REPORTED in event_types:
        raise HomeAssistantError(
            f"Can't listen to {EVENT_STATE_REPORTED} in event trigger"
        )
    event_data_schema: probatio.Schema | None = None
    event_data_items: ItemsView[Any, Any] | None = None
    if CONF_EVENT_DATA in config:
        # Render the schema input
        event_data = {}
        event_data.update(
            template.render_complex(config[CONF_EVENT_DATA], variables, limited=True)
        )

        # For performance reasons, we want to avoid using a probatio schema here
        # unless required. Thus, if possible, we try to use a simple items comparison
        # For that, we explicitly do not check for list like the context data below
        # since lists are a special case only used for context data, see test
        # test_event_data_with_list. Otherwise, we build a volutupus schema, see test
        # test_event_data_with_list_nested
        if any(isinstance(value, dict) for value in event_data.values()):
            event_data_schema = probatio.Schema(
                event_data,
                extra=probatio.ALLOW_EXTRA,
                required=True,
            )
        else:
            # Use a simple items comparison if possible
            event_data_items = event_data.items()

    event_context_schema: probatio.Schema | None = None
    event_context_items: ItemsView[Any, Any] | None = None
    if CONF_EVENT_CONTEXT in config:
        # Render the schema input
        event_context = {}
        event_context.update(
            template.render_complex(config[CONF_EVENT_CONTEXT], variables, limited=True)
        )
        # Build the schema or a an items view if the schema is simple
        # and does not contain lists. Lists are a special case to support
        # matching events by user_id. (see test test_if_fires_on_multiple_user_ids)
        # This can likely be optimized further in the future to handle the
        # multiple user_id case without requiring expensive schema
        # validation.
        if any(isinstance(value, list) for value in event_context.values()):
            event_context_schema = probatio.Schema(
                {
                    probatio.Required(key): _schema_value(value)
                    for key, value in event_context.items()
                },
                extra=probatio.ALLOW_EXTRA,
            )
        else:
            # Use a simple items comparison if possible
            event_context_items = event_context.items()

    job = HassJob(action, f"event trigger {trigger_info}")

    @callback
    def filter_event(event_data: Mapping[str, Any]) -> bool:
        """Filter events."""
        try:
            # Check that the event data and context match the configured
            # schema if one was provided
            if event_data_items:
                # Fast path for simple items comparison
                if not (event_data.items() >= event_data_items):
                    return False
            elif event_data_schema:
                # Slow path for schema validation
                event_data_schema(event_data)
        except probatio.Invalid:
            # If event doesn't match, skip event
            return False
        return True

    @callback
    def handle_event(event: Event) -> None:
        """Listen for events and calls the action when data matches."""
        if event_context_items:
            # Fast path for simple items comparison
            if not (event.context.as_dict().items() >= event_context_items):
                return
        elif event_context_schema:
            try:
                # Slow path for schema validation
                event_context_schema(dict(event.context.as_dict()))
            except probatio.Invalid:
                # If event doesn't match, skip event
                return

        hass.loop.call_soon(
            hass.async_run_hass_job,
            job,
            {
                "trigger": {
                    **trigger_data,
                    "platform": platform_type,
                    "event": event,
                    "description": f"event '{event.event_type}'",
                }
            },
            event.context,
        )

    event_filter = filter_event if event_data_items or event_data_schema else None
    removes = [
        bus.async_listen(event_type, handle_event, event_filter=event_filter)
        for event_type in event_types
    ]

    @callback
    def remove_listen_events() -> None:
        """Remove event listeners."""
        for remove in removes:
            remove()

    return remove_listen_events


# --- homeassistant --------------------------------------------------------------------------

DOMINIO_HOME_ASSISTANT = "homeassistant"
EVENT_START = "start"
EVENT_SHUTDOWN = "shutdown"


async def aggancia_home_assistant(
    hass: HomeAssistant,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Il trigger ``homeassistant`` (come ``triggers/homeassistant.py``): ``start`` scatta
    solo se agganciato prima di ``homeassistant_started``, ``shutdown`` alla chiusura."""
    trigger_data = trigger_info["trigger_data"]
    event = config.get(CONF_EVENT)
    job = HassJob(action, f"homeassistant trigger {trigger_info}")

    if event == EVENT_SHUTDOWN:
        return hass.async_add_shutdown_job(
            job,
            {
                "trigger": {
                    **trigger_data,
                    "platform": DOMINIO_HOME_ASSISTANT,
                    "event": event,
                    "description": "Home Assistant stopping",
                }
            },
        )

    unsub: CALLBACK_TYPE | None = None

    @callback
    def hass_started(_: Event) -> None:
        nonlocal unsub
        unsub = None
        hass.async_run_hass_job(
            job,
            {
                "trigger": {
                    **trigger_data,
                    "platform": DOMINIO_HOME_ASSISTANT,
                    "event": event,
                    "description": "Home Assistant starting",
                }
            },
        )

    # Only fires if armed before EVENT_HOMEASSISTANT_STARTED; if hass is already
    # started, the trigger doesn't fire.
    unsub = hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, hass_started)

    @callback
    def remove() -> None:
        if unsub is not None:
            unsub()

    return remove


# --- time -----------------------------------------------------------------------------------

_DOMINIO_INPUT_DATETIME = "input_datetime"
_DOMINIO_SENSORE = "sensor"
_TIME_TRIGGER_ENTITY = probatio.All(
    str, cv.entity_domain([_DOMINIO_INPUT_DATETIME, _DOMINIO_SENSORE])
)
_TIME_AT_SCHEMA = probatio.Any(cv.time, _TIME_TRIGGER_ENTITY)


class TrackEntity(NamedTuple):
    """Represents a tracking entity for a time trigger."""

    entity_id: str
    callback: Callable[..., Any]


async def aggancia_ora(
    hass: HomeAssistant,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Il trigger ``time`` (come ``triggers/time.py``): un'ora, o l'ora di un'entità
    ``input_datetime`` o di un sensore con un istante (letta con ``stato_di`` e seguita
    con ``segui_cambi``), anche da un modello limitato, con ``weekday``."""
    trigger_data = trigger_info["trigger_data"]
    variables = trigger_info["variables"] or {}
    entities: dict[tuple[str, timedelta], CALLBACK_TYPE] = {}
    removes: list[CALLBACK_TYPE] = []
    job = HassJob(action, f"time trigger {trigger_info}")

    @callback
    def time_automation_listener(
        description: str, now: datetime, *, entity_id: str | None = None
    ) -> None:
        """Listen for time changes and calls action."""
        # Check weekday filter if configured
        if CONF_WEEKDAY in config:
            weekday_config = config[CONF_WEEKDAY]
            current_weekday = WEEKDAYS[now.weekday()]

            # Check if current weekday matches the configuration
            if isinstance(weekday_config, str):
                if current_weekday != weekday_config:
                    return
            elif current_weekday not in weekday_config:
                return

        hass.async_run_hass_job(
            job,
            {
                "trigger": {
                    **trigger_data,
                    "platform": "time",
                    "now": now,
                    "description": description,
                    "entity_id": entity_id,
                }
            },
        )

    @callback
    def update_entity_trigger_event(
        event: Event[EventStateChangedData], offset: timedelta = timedelta(0)
    ) -> None:
        """update_entity_trigger from the event."""
        return update_entity_trigger(
            event.data["entity_id"], event.data["new_state"], offset
        )

    @callback
    def update_entity_trigger(
        entity_id: str, new_state: State | None = None, offset: timedelta = timedelta(0)
    ) -> None:
        """Update the entity trigger for the entity_id."""
        # If a listener was already set up for entity, remove it.
        if remove := entities.pop((entity_id, offset), None):
            remove()
            remove = None

        if not new_state:
            return

        trigger_dt: datetime | None

        # Check state of entity. If valid, set up a listener.
        if new_state.domain == _DOMINIO_INPUT_DATETIME:
            if has_date := new_state.attributes["has_date"]:
                year = new_state.attributes["year"]
                month = new_state.attributes["month"]
                day = new_state.attributes["day"]
            if has_time := new_state.attributes["has_time"]:
                hour = new_state.attributes["hour"]
                minute = new_state.attributes["minute"]
                second = new_state.attributes["second"]
            else:
                # If no time then use midnight.
                hour = minute = second = 0

            if has_date:
                # If input_datetime has date, then track point in time.
                trigger_dt = (
                    datetime(
                        year,
                        month,
                        day,
                        hour,
                        minute,
                        second,
                        tzinfo=dt_util.get_default_time_zone(),
                    )
                    + offset
                )
                # Only set up listener if time is now or in the future.
                if trigger_dt >= dt_util.now():
                    remove = async_track_point_in_time(
                        hass,
                        partial(
                            time_automation_listener,
                            f"time set in {entity_id}",
                            entity_id=entity_id,
                        ),
                        trigger_dt,
                    )
            elif has_time:
                # Else if it has time, then track time change.
                if offset != timedelta(0):
                    # Create a temporary datetime object to get an offset.
                    temp_dt = dt_util.now().replace(
                        hour=hour, minute=minute, second=second, microsecond=0
                    )
                    temp_dt += offset
                    # Ignore the date and apply the offset even if it wraps
                    # around to the next day.
                    hour = temp_dt.hour
                    minute = temp_dt.minute
                    second = temp_dt.second
                remove = async_track_time_change(
                    hass,
                    partial(
                        time_automation_listener,
                        f"time set in {entity_id}",
                        entity_id=entity_id,
                    ),
                    hour=hour,
                    minute=minute,
                    second=second,
                )
        elif (
            new_state.domain == _DOMINIO_SENSORE
            and new_state.attributes.get(EntityStateAttribute.DEVICE_CLASS)
            in (SensorDeviceClass.TIMESTAMP, SensorDeviceClass.UPTIME)
            and new_state.state not in (STATE_UNAVAILABLE, STATE_UNKNOWN)
        ):
            trigger_dt = dt_util.parse_datetime(new_state.state)

            if trigger_dt is not None:
                trigger_dt += offset

            if trigger_dt is not None and trigger_dt > dt_util.utcnow():
                remove = async_track_point_in_time(
                    hass,
                    partial(
                        time_automation_listener,
                        f"time set in {entity_id}",
                        entity_id=entity_id,
                    ),
                    trigger_dt,
                )

        # Was a listener set up?
        if remove:
            entities[(entity_id, offset)] = remove

    to_track: list[TrackEntity] = []

    for at_time in config[CONF_AT]:
        if isinstance(at_time, Template):
            render = template.render_complex(at_time, variables, limited=True)
            try:
                at_time = _TIME_AT_SCHEMA(render)
            except probatio.Invalid as exc:
                raise HomeAssistantError(
                    f"Limited Template for 'at' rendered a"
                    f" unexpected value '{render}', expected"
                    " HH:MM, HH:MM:SS or Entity ID with domain"
                    " 'input_datetime' or 'sensor'"
                ) from exc

        if isinstance(at_time, str):
            # entity
            update_entity_trigger(at_time, new_state=stato_di(hass, at_time))
            to_track.append(TrackEntity(at_time, update_entity_trigger_event))
        elif isinstance(at_time, dict):
            # entity with optional offset
            entity_id: str = at_time[CONF_ENTITY_ID]
            offset: timedelta = at_time.get(CONF_OFFSET, timedelta(0))
            update_entity_trigger(
                entity_id, new_state=stato_di(hass, entity_id), offset=offset
            )
            to_track.append(
                TrackEntity(
                    entity_id, partial(update_entity_trigger_event, offset=offset)
                )
            )
        else:
            # datetime.time
            removes.append(
                async_track_time_change(
                    hass,
                    partial(time_automation_listener, "time"),
                    hour=at_time.hour,
                    minute=at_time.minute,
                    second=at_time.second,
                )
            )

    # Besides time, we also track state changes of requested entities.
    removes.extend(
        (segui_cambi(hass, entry.entity_id, entry.callback)) for entry in to_track
    )

    @callback
    def remove_track_time_changes() -> None:
        """Remove tracked time changes."""
        for remove in entities.values():
            remove()
        for remove in removes:
            remove()

    return remove_track_time_changes


# --- time_pattern ---------------------------------------------------------------------------

CONF_HOURS = "hours"
CONF_MINUTES = "minutes"
CONF_SECONDS = "seconds"


async def aggancia_orario(
    hass: HomeAssistant,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Il trigger ``time_pattern`` (come ``triggers/time_pattern.py``)."""
    trigger_data = trigger_info["trigger_data"]
    hours = config.get(CONF_HOURS)
    minutes = config.get(CONF_MINUTES)
    seconds = config.get(CONF_SECONDS)
    job = HassJob(action, f"time pattern trigger {trigger_info}")

    # If larger units are specified, default the smaller units to zero
    if minutes is None and hours is not None:
        minutes = 0
    if seconds is None and minutes is not None:
        seconds = 0

    @callback
    def time_automation_listener(now: datetime) -> None:
        """Listen for time changes and calls action."""
        hass.async_run_hass_job(
            job,
            {
                "trigger": {
                    **trigger_data,
                    "platform": "time_pattern",
                    "now": now,
                    "description": "time pattern",
                }
            },
        )

    return async_track_time_change(
        hass, time_automation_listener, hour=hours, minute=minutes, second=seconds
    )


# --- le piattaforme -------------------------------------------------------------------------

PIATTAFORME: dict[str, Aggancio] = {
    "state": aggancia_stato,
    "template": aggancia_modello,
    "event": aggancia_evento,
    DOMINIO_HOME_ASSISTANT: aggancia_home_assistant,
    "time": aggancia_ora,
    "time_pattern": aggancia_orario,
}
"""Le piattaforme dei trigger che usa il motore, per nome del trigger."""


def evento_anche_su(bus: BusDegliEventi) -> Aggancio:
    """Una piattaforma per ``altri``: il trigger ``event`` sul bus di Home Assistant e
    poi, con la stessa configurazione, la stessa azione e le stesse variabili, su ``bus``
    (come oggi il trigger dei timer del motore, ``timer.TRIGGER``, che sente gli eventi dei
    timer sia sul bus di Home Assistant sia su quello del motore). Le variabili ``trigger``
    hanno ``platform: event``."""

    async def aggancia(
        hass: HomeAssistant,
        config: ConfigType,
        action: TriggerActionType,
        trigger_info: TriggerInfo,
    ) -> CALLBACK_TYPE:
        togli = [
            await aggancia_evento(hass, config, action, trigger_info),
            await aggancia_evento(hass, config, action, trigger_info, bus=bus),
        ]

        @callback
        def togli_tutto() -> None:
            for una in togli:
                una()

        return togli_tutto

    return aggancia

