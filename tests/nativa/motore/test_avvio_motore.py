"""Avvio, chiusura, servizi e piattaforme dei trigger: il motore come Home Assistant.

Come ``test_semantica.py`` ogni prova scrive automazioni e script in YAML, li fa girare con
Home Assistant e poi, tradotti, con il motore; qui però Home Assistant parte da fermo
(``CoreState.not_running``): le integrazioni si avviano come nel bootstrap, poi
``hass.async_start()``. Il registro degli eventi si annota dal primo istante (avvio
compreso) e, alla fine, si confrontano anche gli stati, il registro delle entità e le
descrizioni dei servizi degli script; alcune prove chiudono Home Assistant
(``hass.async_stop``) con esecuzioni in corso.
"""

from __future__ import annotations

import asyncio
import difflib
import json
import random
from collections.abc import Awaitable, Callable
from datetime import timedelta
from pathlib import Path
from typing import Any

import pytest
import yaml
from freezegun.api import FrozenDateTimeFactory
from homeassistant.const import (
    EVENT_HOMEASSISTANT_START,
    EVENT_HOMEASSISTANT_STARTED,
    MATCH_ALL,
)
from homeassistant.core import (
    CoreState,
    Event,
    HomeAssistant,
    ServiceCall,
    State,
    callback,
)
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import restore_state
from homeassistant.helpers.json import JSONEncoder
from homeassistant.helpers.script import DATA_NEW_SCRIPT_RUNS_NOT_ALLOWED
from homeassistant.helpers.service import (
    async_get_all_descriptions,
    async_set_service_schema,
)
from homeassistant.setup import async_setup_component
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import async_test_home_assistant

from custom_components.vmc_master.nativa.motore import generato
from custom_components.vmc_master.nativa.motore.ha import Motore

from .test_semantica import (
    AIUTANTI,
    PASSO,
    T0,
    _avanza,
    _carica,
    _gira,
    _norma,
    moduli,  # noqa: F401
)
from .traduci import leggi_package, traduci_configurazione

# Eventi dell'avvio delle integrazioni. Con il YAML le entità nascono dentro il setup di
# automation e script, prima dei loro servizi e di component_loaded; il motore le crea
# dopo aver avviato le due integrazioni (come ogni integrazione che aggiunge entità a un
# dominio): l'ordine di questi eventi rispetto alla nascita delle entità è diverso per
# costruzione, prima dell'avvio di Home Assistant, quando nessun trigger è armato. Si
# confrontano a parte, come insieme.
DI_SETUP = {"component_loaded", "service_registered", "service_removed"}

SCENARI: dict[str, dict[str, Any]] = {}


def scenario(
    nome: str,
    configurazione: str,
    *passi: tuple[Any, ...],
    ripristino: list[State] | None = None,
    cambi_all_avvio: bool = False,
    altre: str | None = None,
) -> None:
    """``ripristino``: gli stati salvati all'ultima chiusura (``_ripristina``);
    ``cambi_all_avvio``: durante l'avvio input_boolean.b si accende all'evento di avvio
    (trigger non ancora armati) e input_boolean.a all'evento di avvio completato
    (trigger appena armati); ``altre``: automazioni e script YAML dell'utente, che
    restano YAML anche con il motore (prima di quelli della prova)."""
    SCENARI[nome] = {
        "configurazione": configurazione,
        "passi": list(passi),
        "ripristino": ripristino or [],
        "cambi_all_avvio": cambi_all_avvio,
        "altre": altre,
    }


def servizio(nome: str, dati: dict[str, Any] | None = None) -> tuple[Any, ...]:
    """Un servizio chiamato e atteso (``blocking``) come in test_semantica."""
    return ("servizio", nome, dati or {})


def chiama(nome: str, dati: dict[str, Any] | None = None) -> tuple[Any, ...]:
    """Un servizio chiamato con ``blocking`` in un task: la fine si annota quando arriva
    (con l'istante), così si vede quanto il servizio aspetta."""
    return ("chiama", nome, dati or {})


def acceso(entita: str) -> tuple[Any, ...]:
    return servizio("input_boolean.turn_on", {"entity_id": entita})


def spento(entita: str) -> tuple[Any, ...]:
    return servizio("input_boolean.turn_off", {"entity_id": entita})


def numero(valore: float) -> tuple[Any, ...]:
    return servizio(
        "input_number.set_value", {"entity_id": "input_number.n", "value": valore}
    )


def attendi(secondi: float) -> tuple[Any, ...]:
    return ("attendi", secondi)


def evento(tipo: str, dati: dict[str, Any] | None = None) -> tuple[Any, ...]:
    return ("evento", tipo, dati or {})


def nuove_altre(testo: str) -> tuple[Any, ...]:
    """Le automazioni e gli script YAML dell'utente cambiano in configuration.yaml."""
    return ("altre", testo)


def arresto() -> tuple[Any, ...]:
    """Home Assistant si chiude (``hass.async_stop``), con l'orologio che va avanti."""
    return ("arresto",)


# --- avvio ------------------------------------------------------------------------------

scenario(
    "avvio",
    """
script:
  prova_avvio:
    alias: Prova Avvio
    icon: mdi:rocket
    description: Lo script dell'avvio
    mode: queued
    fields:
      quale:
        description: chi lo chiama
        example: inizio
        required: true
        selector: {text: {}}
    sequence:
      - action: prova.registra
        data: {passo: "script {{ quale }} {{ this.state }}"}
      - delay: 2
      - action: prova.registra
        data: {passo: "script fine {{ quale }}"}
automation:
  - alias: Prova Inizio
    id: prova_inizio
    triggers:
      - {trigger: homeassistant, event: start, id: inizio}
    actions:
      - action: prova.registra
        data:
          passo: "{{ trigger.id }} {{ trigger.event }} {{ trigger.description }} {{ this.state }}"
      - action: script.prova_avvio
        data: {quale: inizio}
  - alias: Prova Inizio Senza Id
    triggers:
      - trigger: homeassistant
        event: start
    actions:
      - action: prova.registra
        data: {passo: "inizio senza id {{ trigger.platform }}"}
  - alias: Prova Modello Vero
    id: prova_modello_vero
    mode: parallel
    triggers:
      - trigger: template
        value_template: "{{ states('input_number.n') | float(0) < 50 }}"
        id: basso
      - trigger: template
        value_template: "{{ is_state('input_boolean.c', 'off') }}"
        for: {seconds: "{{ 1 + 1 }}"}
        id: c-spento
    actions:
      - action: prova.registra
        data: {passo: "modello {{ trigger.id }} {{ trigger.for }}"}
  - alias: Prova Stato Subito
    triggers:
      - {trigger: state, entity_id: [input_boolean.a, input_boolean.b], to: "on"}
    actions:
      - action: prova.registra
        data: {passo: "subito {{ trigger.entity_id }} {{ trigger.from_state.state }}"}
  - alias: Prova Spenta
    id: prova_spenta
    initial_state: false
    triggers:
      - {trigger: state, entity_id: input_boolean.a}
    actions:
      - action: prova.registra
        data: {passo: mai}
  - triggers:
      - {trigger: state, entity_id: input_boolean.c}
    actions:
      - action: prova.registra
        data: {passo: "senza nome {{ this.entity_id }}"}
""",
    attendi(3),
    numero(60),
    numero(10),
    attendi(1),
    acceso("input_boolean.c"),
    spento("input_boolean.c"),
    attendi(3),
    cambi_all_avvio=True,
)


# --- stato ripristinato -------------------------------------------------------------------

_PRIMA = (T0 - timedelta(hours=1)).isoformat()

scenario(
    "ripristino",
    """
script:
  prova_ripristino:
    alias: Prova Ripristino
    sequence:
      - action: prova.registra
        data: {passo: "script {{ this.attributes.last_triggered }}"}
automation:
  - alias: Prova Ripristinata
    id: prova_ripristinata
    triggers:
      - {trigger: state, entity_id: input_boolean.c}
    actions:
      - action: prova.registra
        data: {passo: "ripristinata {{ this.attributes.last_triggered }}"}
      - action: script.prova_ripristino
  - alias: Prova Ripristinata Spenta
    id: prova_ripristinata_spenta
    triggers:
      - {trigger: state, entity_id: input_boolean.c}
    actions:
      - action: prova.registra
        data: {passo: "ripristinata spenta {{ this.attributes.last_triggered }}"}
  - alias: Prova Iniziale Accesa
    id: prova_iniziale_accesa
    initial_state: true
    triggers:
      - {trigger: state, entity_id: input_boolean.c}
    actions:
      - action: prova.registra
        data: {passo: iniziale-accesa}
  - alias: Prova Iniziale Spenta
    id: prova_iniziale_spenta
    initial_state: false
    triggers:
      - {trigger: state, entity_id: input_boolean.c}
    actions:
      - action: prova.registra
        data: {passo: mai}
  - alias: Prova Senza Id Spenta
    triggers:
      - {trigger: state, entity_id: input_boolean.c}
    actions:
      - action: prova.registra
        data: {passo: mai}
""",
    spento("input_boolean.c"),
    attendi(1),
    servizio(
        "automation.turn_on", {"entity_id": "automation.prova_ripristinata_spenta"}
    ),
    acceso("input_boolean.c"),
    attendi(1),
    ripristino=[
        State("automation.prova_ripristinata", "on", {"last_triggered": _PRIMA}),
        State(
            "automation.prova_ripristinata_spenta", "off", {"last_triggered": _PRIMA}
        ),
        State("automation.prova_iniziale_accesa", "off", {"last_triggered": None}),
        State("automation.prova_iniziale_spenta", "on", {"last_triggered": _PRIMA}),
        State("automation.prova_senza_id_spenta", "off", {}),
        State("script.prova_ripristino", "off", {"last_triggered": _PRIMA}),
        State("input_boolean.c", "on", {}),
    ],
)

# --- servizi ------------------------------------------------------------------------------

scenario(
    "servizi_automazioni",
    """
automation:
  - alias: Prova Servizi
    id: prova_servizi
    mode: single
    variables:
      doppio: "{{ (n | default(1)) * 2 }}"
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on"}
    conditions:
      - condition: state
        entity_id: input_boolean.b
        state: "on"
    actions:
      - action: prova.registra
        data: {passo: "servizi {{ trigger.platform }} {{ doppio }} {{ n | default('?') }}"}
      - delay: 3
      - action: prova.registra
        data: {passo: servizi-fine}
""",
    chiama(
        "automation.trigger",
        {"entity_id": "automation.prova_servizi", "skip_condition": False},
    ),
    chiama(
        "automation.trigger",
        {"entity_id": "automation.prova_servizi", "variables": {"n": 4}},
    ),
    attendi(1),
    servizio(
        "automation.turn_off",
        {"entity_id": "automation.prova_servizi", "stop_actions": False},
    ),
    attendi(3),
    servizio("automation.turn_on", {"entity_id": "automation.prova_servizi"}),
    chiama("automation.trigger", {"entity_id": "automation.prova_servizi"}),
    attendi(1),
    servizio("automation.turn_off", {"entity_id": "automation.prova_servizi"}),
    attendi(1),
    servizio("automation.toggle", {"entity_id": "automation.prova_servizi"}),
    acceso("input_boolean.b"),
    acceso("input_boolean.a"),
    attendi(1),
    servizio("automation.toggle", {"entity_id": "automation.prova_servizi"}),
    attendi(3),
    servizio("automation.toggle", {"entity_id": "automation.prova_servizi"}),
    spento("input_boolean.a"),
    acceso("input_boolean.a"),
    attendi(4),
)

scenario(
    "servizi_script",
    """
script:
  prova_campi:
    alias: Prova Campi
    description: Uno script con campi
    icon: mdi:numeric
    mode: queued
    max: 3
    fields:
      x:
        name: Valore
        description: il valore
        default: 5
        selector: {number: {min: 0, max: 10}}
      y: {description: altro}
    variables:
      doppio: "{{ (x | default(0)) * 2 }}"
    sequence:
      - action: prova.registra
        data:
          passo: "campi {{ x | default('nessuno') }} {{ y | default('nessuno') }} {{ doppio }}"
      - delay: 2
      - action: prova.registra
        data: {passo: "campi fine {{ x | default('nessuno') }}"}
  prova_lungo:
    sequence:
      - delay: 5
      - action: prova.registra
        data: {passo: lungo-fine}
""",
    servizio(
        "script.turn_on", {"entity_id": "script.prova_campi", "variables": {"x": 1}}
    ),
    servizio(
        "script.turn_on", {"entity_id": "script.prova_campi", "variables": {"x": 2}}
    ),
    chiama("script.prova_campi", {"x": 3, "y": "b"}),
    chiama("script.prova_campi", {"x": 4}),
    attendi(1),
    servizio("script.turn_off", {"entity_id": "script.prova_campi"}),
    attendi(1),
    chiama("script.prova_campi", {"x": 7}),
    attendi(3),
    servizio("script.toggle", {"entity_id": "script.prova_lungo"}),
    attendi(1),
    servizio("script.toggle", {"entity_id": "script.prova_lungo"}),
    servizio("script.turn_on", {"entity_id": "script.prova_lungo"}),
    attendi(1),
    chiama("script.turn_on", {"entity_id": "script.prova_lungo"}),
    attendi(5),
    servizio(
        "script.turn_on", {"entity_id": ["script.prova_lungo", "script.prova_campi"]}
    ),
    attendi(1),
    servizio("script.turn_off", {"entity_id": "all"}),
    attendi(1),
)

# --- piattaforme dei trigger --------------------------------------------------------------

scenario(
    "piattaforme",
    """
automation:
  - alias: Prova Evento
    id: prova_evento
    mode: queued
    triggers:
      - trigger: event
        event_type: call_service
        event_data: {domain: prova, service: segnale}
        id: segnale
      - trigger: event
        event_type: [prova_evento, altro_evento]
        event_data: {quale: uno}
        id: evento
    actions:
      - action: prova.registra
        data:
          passo: "evento {{ trigger.id }} {{ trigger.event.event_type }} {{ trigger.event.data }}"
  - alias: Prova Ora
    mode: parallel
    triggers:
      - {trigger: time, at: "02:00:05", id: ora}
      - {trigger: time_pattern, seconds: "/20", id: secondi}
      - {trigger: time_pattern, minutes: "/1", id: minuti}
    actions:
      - action: prova.registra
        data: {passo: "ora {{ trigger.id }} {{ trigger.now.isoformat() }}"}
  - alias: Prova Stato Per
    mode: parallel
    triggers:
      - trigger: state
        entity_id: input_boolean.a
        from: "off"
        to: "on"
        for: {seconds: 2}
        id: a-per
      - {trigger: state, entity_id: sensor.prova, attribute: livello, id: attributo}
      - trigger: state
        entity_id: input_boolean.b
        not_from: [unavailable, unknown]
        not_to: [unavailable]
        id: b-not
      - trigger: state
        entity_id: input_boolean.c
        to: "on"
        for: "{{ '00:00:01' }}"
        id: c-per-modello
    actions:
      - action: prova.registra
        data:
          passo: "stato {{ trigger.id }} {{ trigger.from_state.state }} {{ trigger.to_state.state }} {{ trigger.for }}"
  - alias: Prova Numerico
    mode: parallel
    triggers:
      - trigger: numeric_state
        entity_id: input_number.n
        above: 50
        for: {seconds: 1}
        id: sopra
      - trigger: numeric_state
        entity_id: input_number.n
        below: 20
        value_template: "{{ state.state | float * 2 }}"
        id: sotto
      - trigger: numeric_state
        entity_id: sensor.prova
        attribute: livello
        above: 3
        id: livello
    actions:
      - action: prova.registra
        data: {passo: "numerico {{ trigger.id }} {{ trigger.below }} {{ trigger.above }}"}
  - alias: Prova Modello Per
    mode: queued
    triggers:
      - trigger: template
        value_template: >-
          {{ is_state('input_boolean.a', 'on') and states('input_number.n') | float(0) > 30 }}
        for: {seconds: "{{ states('input_number.n') | int(0) // 20 }}"}
    actions:
      - action: prova.registra
        data: {passo: "modello per {{ trigger.for }} {{ states('input_number.n') }}"}
""",
    servizio("prova.segnale", {"quale": "uno"}),
    evento("prova_evento", {"quale": "uno", "altro": 1}),
    evento("prova_evento", {"quale": "due"}),
    evento("altro_evento", {"quale": "uno"}),
    acceso("input_boolean.a"),
    attendi(1),
    spento("input_boolean.a"),
    acceso("input_boolean.a"),
    ("stato", "sensor.prova", "1", {"livello": 1}),
    ("stato", "sensor.prova", "1", {"livello": 4}),
    ("stato", "sensor.prova", "2", {"livello": 4}),
    acceso("input_boolean.b"),
    acceso("input_boolean.c"),
    attendi(0.5),
    spento("input_boolean.c"),
    acceso("input_boolean.c"),
    numero(60),
    attendi(0.5),
    numero(70),
    attendi(1.5),
    numero(40),
    numero(10),
    attendi(1),
    numero(35),
    attendi(2),
    numero(80),
    attendi(5),
    numero(5),
    attendi(60),
)

# --- chiusura di Home Assistant -----------------------------------------------------------

scenario(
    "arresto",
    """
script:
  prova_lento:
    alias: Prova Lento
    mode: parallel
    sequence:
      - action: prova.registra
        data: {passo: "lento {{ quale }}"}
      - delay: 30
      - action: prova.registra
        data: {passo: "lento fine {{ quale }}"}
  prova_coda:
    mode: queued
    sequence:
      - delay: 10
      - action: prova.registra
        data: {passo: coda-fine}
  prova_lunghissimo:
    sequence:
      - delay: 100
      - action: prova.registra
        data: {passo: mai}
automation:
  - alias: Prova In Corso
    id: prova_in_corso
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on"}
    actions:
      - action: script.turn_on
        target: {entity_id: script.prova_lento}
        data: {variables: {quale: automazione}}
      - action: script.prova_coda
      - wait_template: "{{ is_state('input_boolean.b', 'on') }}"
      - action: prova.registra
        data: {passo: mai}
  - alias: Prova Allo Spegnimento
    id: prova_allo_spegnimento
    mode: queued
    triggers:
      - {trigger: state, entity_id: script.prova_lento, to: "off", id: lento-spento}
      - {trigger: state, entity_id: automation.prova_in_corso, attribute: current, id: corrente}
      - {trigger: homeassistant, event: shutdown, id: chiusura}
    actions:
      - action: prova.registra
        data: {passo: "spegnimento {{ trigger.id }} {{ trigger.platform }}"}
      - delay: 1
      - action: prova.registra
        data: {passo: "spegnimento fine {{ trigger.id }}"}
  - alias: Prova Dopo
    triggers:
      - {trigger: state, entity_id: input_boolean.c}
    actions:
      - action: prova.registra
        data: {passo: "dopo {{ trigger.to_state.state }}"}
      - action: script.turn_on
        target: {entity_id: script.prova_lunghissimo}
""",
    acceso("input_boolean.a"),
    chiama("script.prova_lento", {"quale": "diretto"}),
    chiama("script.turn_on", {"entity_id": "script.prova_coda"}),
    attendi(2),
    arresto(),
    acceso("input_boolean.c"),
    attendi(30),
    spento("input_boolean.c"),
    attendi(31),
    acceso("input_boolean.c"),
    attendi(1),
    cambi_all_avvio=True,
)


# --- ricarica di automation e script -------------------------------------------------------

# In queste prove la pausa dello script (4 s) e quella dell'automazione (5 s) non
# scadono nello stesso istante: con l'orologio fermo due timer con lo stesso istante
# escono dal heap di asyncio in un ordine che dipende dai timer cancellati che vi restano
# (per esempio i salvataggi rimandati del registro delle entità, diversi con il motore
# perché le sue entità nascono dopo l'avvio delle integrazioni), non dalle automazioni;
# con l'orologio vero i due istanti differiscono (con 5 e 5 s ricarica_con_altre dava
# l'ordine opposto nello stesso istante).

scenario(
    "ricarica",
    """
script:
  prova_ricarica:
    alias: Prova Ricarica
    sequence:
      - action: prova.registra
        data: {passo: script-inizio}
      - delay: 4
      - action: prova.registra
        data: {passo: script-fine}
automation:
  - alias: Prova Ricarica Con Id
    id: prova_ricarica_con_id
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on"}
    actions:
      - action: script.turn_on
        target: {entity_id: script.prova_ricarica}
      - delay: 5
      - action: prova.registra
        data: {passo: automazione-fine}
  - alias: Prova Ricarica Senza Id
    triggers:
      - {trigger: state, entity_id: input_boolean.b}
    actions:
      - action: prova.registra
        data: {passo: "senza id {{ trigger.to_state.state }}"}
""",
    acceso("input_boolean.a"),
    attendi(1),
    servizio("automation.reload"),
    servizio("script.reload"),
    acceso("input_boolean.b"),
    attendi(5),
    spento("input_boolean.a"),
    acceso("input_boolean.a"),
    attendi(1),
)


_ALTRE = """
automation:
  - alias: Altra Automazione
    id: altra
    mode: parallel
    triggers:
      - {trigger: state, entity_id: input_boolean.c}
    actions:
      - action: script.altro_script
      - action: prova.registra
        data: {passo: "altra {{ trigger.to_state.state }}"}
  - triggers:
      - {trigger: state, entity_id: input_boolean.b}
    actions:
      - action: prova.registra
        data: {passo: "altra senza nome {{ this.entity_id }}"}
script:
  altro_script:
    sequence:
      - delay: 3
      - action: prova.registra
        data: {passo: altro-fine}
"""

scenario(
    "ricarica_con_altre",
    """
script:
  prova_ricarica:
    alias: Prova Ricarica
    sequence:
      - action: prova.registra
        data: {passo: script-inizio}
      - delay: 4
      - action: prova.registra
        data: {passo: script-fine}
automation:
  - alias: Prova Ricarica Con Id
    id: prova_ricarica_con_id
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on"}
    actions:
      - action: script.turn_on
        target: {entity_id: script.prova_ricarica}
      - delay: 5
      - action: prova.registra
        data: {passo: automazione-fine}
  - alias: Prova Ricarica Senza Id
    triggers:
      - {trigger: state, entity_id: input_boolean.b}
    actions:
      - action: prova.registra
        data: {passo: "senza id {{ trigger.to_state.state }}"}
""",
    acceso("input_boolean.c"),
    acceso("input_boolean.a"),
    attendi(1),
    nuove_altre(_ALTRE.replace("altra {{", "altra cambiata {{")),
    servizio("automation.reload"),
    servizio("script.reload"),
    servizio("automation.reload", {"id": "prova_ricarica_con_id"}),
    servizio("automation.reload", {"id": "altra"}),
    acceso("input_boolean.b"),
    spento("input_boolean.c"),
    attendi(5),
    nuove_altre(_ALTRE.replace("delay: 3", "delay: 1")),
    servizio("script.reload"),
    acceso("input_boolean.c"),
    spento("input_boolean.a"),
    acceso("input_boolean.a"),
    attendi(6),
    altre=_ALTRE,
)


@pytest.fixture
def wait_for_stop_scripts_after_shutdown() -> bool:
    """Alla chiusura Home Assistant ferma dopo 60 secondi gli script ancora in corso
    (il plugin dei test lo toglie: qui serve vero)."""
    return True


def _ripristina(hass: HomeAssistant, stati: list[State]) -> None:
    """Gli stati salvati all'ultima chiusura, come li legge Home Assistant dal proprio
    archivio all'avvio (mock_restore_cache del plugin scrive ``last_states``, che
    Home Assistant 2026.11 non legge più)."""
    adesso = dt_util.utcnow().isoformat()
    restore_state.async_get(hass)._async_load_stored_states(
        [
            {
                "state": json.loads(json.dumps(stato.as_dict(), cls=JSONEncoder)),
                "last_seen": adesso,
            }
            for stato in stati
        ]
    )


def _registro_entita(hass: HomeAssistant) -> list[Any]:
    """Le voci del registro delle entità di automazioni e script (senza gli id interni
    e gli istanti di creazione)."""
    voci = []
    for voce in er.async_get(hass).entities.values():
        if voce.domain not in ("automation", "script"):
            continue
        voci.append(
            (
                voce.entity_id,
                voce.unique_id,
                voce.platform,
                voce.original_name,
                voce.original_icon,
                voce.name,
                voce.icon,
                _norma(dict(voce.capabilities or {})),
                voce.supported_features,
                voce.has_entity_name,
                voce.disabled_by,
                voce.hidden_by,
                voce.entity_category,
                voce.config_entry_id,
            )
        )
    return sorted(voci)


async def _fino_alla_fine(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory, compito: asyncio.Future[Any]
) -> None:
    """Il ciclo lavora (e l'orologio va avanti di un passo quando è fermo) finché il
    compito non finisce."""
    for _ in range(100_000):
        await _gira(hass)
        if compito.done():
            return
        freezer.tick(timedelta(seconds=PASSO))
    raise AssertionError("il compito non finisce")


async def _corsa(
    freezer: FrozenDateTimeFactory,
    nome: str,
    prova: dict[str, Any],
    *,
    motore: bool,
    caricati: list[str],
    cartella: Path,
) -> dict[str, Any]:
    freezer.move_to(T0)
    # i trigger time e time_pattern scattano a un microsecondo a caso (randint di
    # async_track_utc_time_change): stessa sequenza casuale per Home Assistant e motore
    random.seed(0)
    registro: list[Any] = []
    configurazione = yaml.safe_load(prova["configurazione"])
    di_setup: list[Any] = []
    esito: dict[str, Any] = {"registro": registro, "di_setup": di_setup}

    def scrivi_configurazione(testo_altre: str | None) -> dict[str, Any]:
        """configuration.yaml (lo rileggono automation.reload e script.reload): le
        altre automazioni e gli altri script e, solo senza il motore, quelli della prova
        (come il package nella variante nativa). Restituisce le altre."""
        altre = yaml.safe_load(testo_altre or "") or {}
        altre = {
            "automation": altre.get("automation", []),
            "script": altre.get("script", {}),
        }
        tutte = altre
        if not motore:
            tutte = {
                "automation": [
                    *altre["automation"],
                    *configurazione.get("automation", []),
                ],
                "script": {**altre["script"], **configurazione.get("script", {})},
            }
        (cartella / "configuration.yaml").write_text(
            yaml.safe_dump(tutte, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        return altre

    cartella.mkdir()
    altre = scrivi_configurazione(prova["altre"])
    async with async_test_home_assistant(
        config_dir=str(cartella), initial_state=CoreState.not_running
    ) as hass:
        if prova["ripristino"]:
            _ripristina(hass, prova["ripristino"])

        # i contesti (id casuali) come numeri d'ordine: si confronta chi ha causato cosa
        contesti: dict[str | None, int | None] = {None: None}

        def contesto(identificativo: str | None) -> int | None:
            return contesti.setdefault(identificativo, len(contesti) - 1)

        @callback
        def annota(evento: Event) -> None:
            if evento.event_type in DI_SETUP:
                di_setup.append((evento.event_type, _norma(dict(evento.data))))
                return
            dati = evento.data
            if "new_state" in dati:
                dati = {"entity_id": dati["entity_id"], "new_state": dati["new_state"]}
            registro.append(
                (
                    _norma(evento.time_fired),
                    evento.event_type,
                    _norma(dict(dati)),
                    contesto(evento.context.id),
                    contesto(evento.context.parent_id),
                )
            )

        hass.bus.async_listen(MATCH_ALL, annota)
        assert await async_setup_component(hass, "homeassistant", {})
        for dominio, voci in AIUTANTI.items():
            assert await async_setup_component(hass, dominio, {dominio: voci})

        async def registra(chiamata: ServiceCall) -> None:
            if chiamata.data.get("errore"):
                raise HomeAssistantError("errore voluto")

        for nome_servizio in ("registra", "segnale"):
            hass.services.async_register("prova", nome_servizio, registra)
            # la descrizione c'è già: async_get_all_descriptions non cerca services.yaml
            async_set_service_schema(hass, "prova", nome_servizio, {"fields": {}})

        def cambia(entita: str) -> Callable[[Event], Awaitable[None]]:
            async def _cambia(_evento: Event) -> None:
                await hass.services.async_call(
                    "input_boolean", "turn_on", {"entity_id": entita}, blocking=True
                )

            return _cambia

        if prova["cambi_all_avvio"]:
            hass.bus.async_listen_once(
                EVENT_HOMEASSISTANT_START, cambia("input_boolean.b")
            )
            hass.bus.async_listen_once(
                EVENT_HOMEASSISTANT_STARTED, cambia("input_boolean.a")
            )

        automazioni = configurazione.get("automation", [])
        script = configurazione.get("script", {})
        m: Motore | None = None
        if motore:
            testo_modelli, testo_motore = await traduci_configurazione(
                hass, automazioni, script, nome_modelli=f"avvio_{nome}_modelli"
            )
            caricati.append(f"{generato.__name__}.avvio_{nome}_modelli")
            caricati.append(f"{generato.__name__}.avvio_{nome}_motore")
            _carica(f"avvio_{nome}_modelli", testo_modelli)
            codice = _carica(f"avvio_{nome}_motore", testo_motore)
            m = Motore(hass)
            await m.avvia(crea=codice.crea, configurazione=altre)
        else:
            assert await async_setup_component(
                hass, "script", {"script": {**altre["script"], **script}}
            )
            assert await async_setup_component(
                hass,
                "automation",
                {"automation": [*altre["automation"], *automazioni]},
            )
        # come il bootstrap: l'avvio aspetta i lavori delle integrazioni (anche quelli
        # nei thread, che non devono far avanzare l'orologio fermo)
        await hass.async_block_till_done()
        registro.append(("bootstrap finito",))
        avvio = asyncio.ensure_future(hass.async_start())
        await _fino_alla_fine(hass, freezer, avvio)
        registro.append(("avviato",))

        chiamate: list[asyncio.Future[Any]] = []
        for passo in prova["passi"]:
            if passo[0] == "servizio":
                dominio, nome_servizio = passo[1].split(".")
                await hass.services.async_call(
                    dominio, nome_servizio, passo[2], blocking=True
                )
                await _gira(hass)
            elif passo[0] == "chiama":
                dominio, nome_servizio = passo[1].split(".")
                etichetta = f"{passo[1]} {passo[2]}"

                async def _chiama(
                    dominio: str, nome_servizio: str, dati: Any, etichetta: str
                ) -> None:
                    try:
                        await hass.services.async_call(
                            dominio, nome_servizio, dati, blocking=True
                        )
                    except BaseException as err:
                        registro.append(
                            (
                                _norma(dt_util.utcnow()),
                                "fine",
                                etichetta,
                                type(err).__name__,
                            )
                        )
                        raise
                    registro.append((_norma(dt_util.utcnow()), "fine", etichetta))

                chiamate.append(
                    asyncio.ensure_future(
                        _chiama(dominio, nome_servizio, passo[2], etichetta)
                    )
                )
                await _gira(hass)
            elif passo[0] == "altre":
                scrivi_configurazione(passo[1])
            elif passo[0] == "stato":
                hass.states.async_set(passo[1], passo[2], passo[3])
                await _gira(hass)
            elif passo[0] == "evento":
                hass.bus.async_fire(passo[1], passo[2])
                await _gira(hass)
            elif passo[0] == "attendi":
                await _avanza(hass, freezer, passo[1])
            else:
                fermata = asyncio.ensure_future(hass.async_stop())
                await _fino_alla_fine(hass, freezer, fermata)
                registro.append(("fermato",))

        esito["stati"] = sorted(
            (s.entity_id, s.state, _norma(dict(s.attributes)))
            for s in hass.states.async_all(("automation", "script"))
        )
        esito["entita"] = _registro_entita(hass)
        esito["nuove_vietate"] = DATA_NEW_SCRIPT_RUNS_NOT_ALLOWED in hass.data
        descrizioni = await async_get_all_descriptions(hass)
        esito["descrizioni"] = _norma(descrizioni.get("script", {}))
        if hass.state is CoreState.running:
            await hass.services.async_call(
                "automation", "turn_off", {"entity_id": "all"}, blocking=True
            )
            await hass.services.async_call(
                "script", "turn_off", {"entity_id": "all"}, blocking=True
            )
            await _gira(hass)
            await hass.async_stop(force=True)
        # i 60 secondi dopo la chiusura (_schedule_stop_scripts_after_shutdown)
        freezer.tick(timedelta(seconds=61))
        await _gira(hass)
        for chiamata in chiamate:
            if not chiamata.done():
                chiamata.cancel()
        await asyncio.gather(*chiamate, return_exceptions=True)
    return esito


def _confronta(atteso: Any, ottenuto: Any, cosa: str) -> None:
    if ottenuto == atteso:
        return
    righe_attese = [repr(v) for v in atteso]
    righe_ottenute = [repr(v) for v in ottenuto]
    diff = "\n".join(
        difflib.unified_diff(
            righe_attese, righe_ottenute, "home_assistant", "motore", lineterm="", n=2
        )
    )
    pytest.fail(f"{cosa} diversi:\n{diff}")


@pytest.mark.parametrize("nome", sorted(SCENARI))
async def test_avvio_come_home_assistant(
    nome: str,
    freezer: FrozenDateTimeFactory,
    moduli: list[str],  # noqa: F811
    tmp_path: Path,
) -> None:
    """Stessi eventi (dall'avvio), stati, entità e descrizioni dei servizi."""
    prova = SCENARI[nome]
    atteso = await _corsa(
        freezer, nome, prova, motore=False, caricati=moduli, cartella=tmp_path / "ha"
    )
    ottenuto = await _corsa(
        freezer, nome, prova, motore=True, caricati=moduli, cartella=tmp_path / "m"
    )
    if prova["altre"]:
        # con altre automazioni e altri script YAML le entità del motore nascono dopo
        # tutte quelle YAML (le integrazioni automation e script si avviano prima):
        # nel bootstrap, a trigger non armati, si confronta l'insieme degli eventi
        fine = atteso["registro"].index(("bootstrap finito",))
        assert ottenuto["registro"].index(("bootstrap finito",)) == fine
        _confronta(
            sorted(repr(v[:3]) for v in atteso["registro"][:fine]),
            sorted(repr(v[:3]) for v in ottenuto["registro"][:fine]),
            "eventi del bootstrap",
        )
        del atteso["registro"][:fine], ottenuto["registro"][:fine]
    _confronta(atteso["registro"], ottenuto["registro"], "registri")
    _confronta(atteso["stati"], ottenuto["stati"], "stati")
    _confronta(atteso["entita"], ottenuto["entita"], "registri delle entità")
    assert ottenuto["nuove_vietate"] == atteso["nuove_vietate"]
    _confronta(
        sorted(map(repr, atteso["di_setup"])),
        sorted(map(repr, ottenuto["di_setup"])),
        "eventi del setup",
    )
    _confronta(
        sorted(atteso["descrizioni"].items()),
        sorted(ottenuto["descrizioni"].items()),
        "descrizioni dei servizi",
    )


async def _entita_del_package(
    freezer: FrozenDateTimeFactory, *, motore: bool
) -> dict[str, Any]:
    freezer.move_to(T0)
    automazioni, script = leggi_package()
    async with async_test_home_assistant(initial_state=CoreState.not_running) as hass:
        assert await async_setup_component(hass, "homeassistant", {})
        if motore:
            await Motore(hass).avvia()
        else:
            assert await async_setup_component(hass, "script", {"script": script})
            assert await async_setup_component(
                hass, "automation", {"automation": automazioni}
            )
        await hass.async_block_till_done()
        descrizioni = await async_get_all_descriptions(hass)
        esito = {
            "entita": _registro_entita(hass),
            "stati": sorted(
                (s.entity_id, s.state, _norma(dict(s.attributes)))
                for s in hass.states.async_all(("automation", "script"))
            ),
            "descrizioni": sorted(_norma(descrizioni["script"]).items()),
        }
        await hass.async_stop(force=True)
        freezer.tick(timedelta(seconds=61))
        await _gira(hass)
    return esito


async def test_entita_del_package_come_home_assistant(
    freezer: FrozenDateTimeFactory,
) -> None:
    """Le automazioni (tutte con id: l'Automazione VMC Master ha quello che le dà
    l'integrazione) e gli script del package: stessi entity_id, unique_id, nomi, icone,
    stati e descrizioni dei servizi con il YAML e con il motore."""
    atteso = await _entita_del_package(freezer, motore=False)
    ottenuto = await _entita_del_package(freezer, motore=True)
    assert len(atteso["stati"]) == 14 + 51
    assert (
        sum(1 for voce in atteso["entita"] if voce[0].startswith("automation.")) == 14
    )
    _confronta(atteso["entita"], ottenuto["entita"], "registri delle entità")
    _confronta(atteso["stati"], ottenuto["stati"], "stati")
    _confronta(
        atteso["descrizioni"], ottenuto["descrizioni"], "descrizioni dei servizi"
    )
