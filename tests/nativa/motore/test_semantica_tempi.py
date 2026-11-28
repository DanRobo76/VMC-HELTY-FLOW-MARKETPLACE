"""I tempi del motore tradotto come Home Assistant: prove mirate a confronto.

Come ``test_semantica.py`` ogni prova scrive automazioni e script in YAML, li fa girare
con Home Assistant e poi, tradotti dallo stesso traduttore del package, con il motore, con
lo stesso orologio fermo e gli stessi passi; il registro degli eventi deve essere
identico. Qui le prove guardano i percorsi in cui conta l'istante: pause, attese, trigger
modello con ``for``, modalità delle esecuzioni (``restart``, ``queued``, ``single``,
``parallel``), script che chiamano script, trigger ``time``, ``time_pattern`` e
``homeassistant``, timer.

L'orologio non avanza a passi fissi: salta da un timer di asyncio al successivo
(``_avanza``), così ogni timer scatta all'istante esatto in cui è dovuto e il registro
annota l'istante al microsecondo. Un timer che scatta un giro del ciclo prima o dopo, o
un'esecuzione che riparte in un altro ordine, cambia il registro: l'ordine degli eventi
nello stesso istante, l'istante stesso o il contesto che li ha causati. Nel registro ci
sono anche i messaggi di ``max_exceeded`` (``Already running``, ``Maximum number of runs
exceeded``) con il loro livello: con ``silent`` non ci sono.
"""

from __future__ import annotations

import asyncio
import difflib
import itertools
import logging
import math
from collections.abc import Callable, Iterator
from datetime import UTC, datetime, timedelta
from typing import Any

import pytest
import yaml
from freezegun.api import FrozenDateTimeFactory
from homeassistant.const import EVENT_CALL_SERVICE, EVENT_STATE_CHANGED, MATCH_ALL
from homeassistant.core import Context, CoreState, Event, HomeAssistant, State, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.setup import async_setup_component
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import async_test_home_assistant

from custom_components.vmc_master.nativa.motore import generato
from custom_components.vmc_master.nativa.motore.stati_logiche import stati_logiche

from .fase3 import MotoreFase3
from .test_semantica import _carica, _gira, della_pulizia, moduli  # noqa: F401
from .traduci import traduci_configurazione

# 02:00:00 a US/Pacific, il fuso delle prove
T0 = datetime(2026, 11, 25, 10, 0, 0, tzinfo=UTC)
# 23:59:50 del 24 novembre a US/Pacific: dieci secondi prima di mezzanotte
PRIMA_DI_MEZZANOTTE = datetime(2026, 11, 25, 7, 59, 50, tzinfo=UTC)

AIUTANTI: dict[str, dict[str, Any]] = {
    "input_boolean": {"a": {}, "b": {}, "c": {}},
    "input_number": {"n": {"min": 0, "max": 100, "step": 1}},
    "timer": {"t1": {"duration": "00:00:05"}, "t2": {"duration": 3}},
}
# Senza ``automation_triggered``: le automazioni del motore sono logiche dell'integrazione,
# senza l'evento (l'istante in cui partono è nel loro stato: ``last_triggered``, ``current``)
EVENTI = {
    EVENT_STATE_CHANGED,
    EVENT_CALL_SERVICE,
    "script_started",
    "timer.started",
    "timer.restarted",
    "timer.paused",
    "timer.cancelled",
    "timer.finished",
    "timer.changed",
    "homeassistant_start",
    "homeassistant_started",
    "homeassistant_stop",
    "homeassistant_final_write",
    "prova",
}
# I messaggi di max_exceeded (stesso testo e livello con il YAML e con il motore)
MESSAGGI_MASSIMO = ("Already running", "Maximum number of runs exceeded")

SCENARI: dict[str, dict[str, Any]] = {}


def scenario(
    nome: str,
    configurazione: str,
    *passi: tuple[Any, ...] | list[tuple[Any, ...]],
    inizio: datetime = T0,
    avvio: bool = False,
    aiutanti: dict[str, dict[str, Any]] | None = None,
) -> None:
    """``inizio``: l'istante dell'orologio all'inizio; ``avvio``: Home Assistant parte
    da fermo (``CoreState.not_running``), con i trigger ``homeassistant``; ``aiutanti``:
    aiutanti al posto di quelli predefiniti, per dominio. Un passo può essere una lista
    di passi."""
    piatti: list[tuple[Any, ...]] = []
    for passo in passi:
        if isinstance(passo, list):
            piatti.extend(passo)
        else:
            piatti.append(passo)
    SCENARI[nome] = {
        "configurazione": configurazione,
        "passi": piatti,
        "inizio": inizio,
        "avvio": avvio,
        "aiutanti": {**AIUTANTI, **(aiutanti or {})},
    }


def servizio(nome: str, dati: dict[str, Any] | None = None) -> tuple[Any, ...]:
    """Un servizio chiamato e atteso (``blocking``)."""
    return ("servizio", nome, dati or {})


def chiama(nome: str, dati: dict[str, Any] | None = None) -> tuple[Any, ...]:
    """Un servizio chiamato con ``blocking`` in un task: la fine (o l'errore) si annota
    nel registro quando arriva, con l'istante."""
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
    """L'orologio avanza di ``secondi``, da un timer all'altro."""
    return ("attendi", secondi)


def sonda(entita: str, secondi: float, ogni: float = 0.1) -> list[tuple[Any, ...]]:
    """Per ``secondi``, ogni ``ogni`` secondi l'entità riscrive il suo stato
    (``homeassistant.update_entity``): ogni cambio di un attributo che non scrive da sé
    (``last_action`` di uno script) finisce nel registro all'istante in cui c'è."""
    passi: list[tuple[Any, ...]] = []
    for _ in range(round(secondi / ogni)):
        passi.append(servizio("homeassistant.update_entity", {"entity_id": entita}))
        passi.append(attendi(ogni))
    return passi


def arresto() -> tuple[Any, ...]:
    """Home Assistant si chiude (``hass.async_stop``), con l'orologio che va avanti."""
    return ("arresto",)


# --- restart, queued e single ------------------------------------------------------------

scenario(
    "restart_in_pausa_annidata",
    # uno script restart riavviato mentre è in una pausa dentro choose > if > repeat:
    # da una chiamata bloccante, da script.turn_on, e da un'automazione che lui stesso
    # fa partire con il toggle nel mezzo del ciclo (il riavvio arriva mentre la sua
    # chiamata del servizio è ancora in corso)
    """
script:
  prova_riavvia:
    alias: Prova Riavvia
    mode: restart
    sequence:
      - action: prova.registra
        data: {passo: "inizio {{ chi }}"}
      - choose:
          - conditions: "{{ chi != 'breve' }}"
            sequence:
              - if: "{{ true }}"
                then:
                  - repeat:
                      until: "{{ repeat.index >= 3 }}"
                      sequence:
                        - action: prova.registra
                          data: {passo: "giro {{ repeat.index }} {{ chi }}"}
                        - if: "{{ repeat.index == 2 and chi == '1.0' }}"
                          then:
                            - action: input_boolean.toggle
                              target: {entity_id: input_boolean.c}
                        - alias: Pausa nel ciclo
                          delay: 0.75
        default:
          - delay: 0.4
      - action: prova.registra
        data: {passo: "fine {{ chi }}"}
automation:
  - alias: Prova Riavvio Bloccante
    mode: parallel
    triggers:
      - {trigger: state, entity_id: input_number.n}
    actions:
      - action: script.prova_riavvia
        data: {chi: "{{ trigger.to_state.state }}"}
      - action: prova.registra
        data: {passo: "dopo bloccante {{ trigger.to_state.state }}"}
  - alias: Prova Riavvio Da Se
    mode: queued
    triggers:
      - {trigger: state, entity_id: input_boolean.c, to: "on"}
    actions:
      - action: script.turn_on
        target: {entity_id: script.prova_riavvia}
        data: {variables: {chi: "da c"}}
      - action: prova.registra
        data: {passo: "riavviato da c"}
  - alias: Prova Riavvio Breve
    mode: parallel
    triggers:
      - {trigger: state, entity_id: input_boolean.a}
    actions:
      - action: script.turn_on
        target: {entity_id: script.prova_riavvia}
        data: {variables: {chi: breve}}
      - action: prova.registra
        data: {passo: "breve {{ trigger.to_state.state }}"}
""",
    numero(1),
    sonda("script.prova_riavvia", 1.2),
    numero(2),
    attendi(0.75),
    numero(3),
    attendi(0.3),
    acceso("input_boolean.a"),
    spento("input_boolean.a"),
    attendi(0.2),
    numero(4),
    sonda("script.prova_riavvia", 1.6),
    acceso("input_boolean.a"),
    attendi(3),
)

scenario(
    "code_oltre_il_massimo",
    # esecuzioni in coda oltre il massimo nello stesso istante e mentre la prima è in
    # pausa: automazioni queued e parallel con WARNING e con SILENT, script queued
    # avviati con script.turn_on (che, a coda piena, aspetta il prossimo cambio dello
    # script) e con una chiamata bloccante
    """
script:
  prova_coda_silenziosa:
    alias: Prova Coda Silenziosa
    mode: queued
    max: 2
    max_exceeded: silent
    sequence:
      - action: prova.registra
        data: {passo: "silenziosa {{ chi }}"}
      - delay: 1
  prova_coda_rumorosa:
    alias: Prova Coda Rumorosa
    mode: queued
    max: 2
    sequence:
      - action: prova.registra
        data: {passo: "rumorosa {{ chi }}"}
      - delay: 1.3
automation:
  - alias: Prova Accoda Automazione
    mode: queued
    max: 3
    triggers:
      - {trigger: state, entity_id: input_number.n}
    actions:
      - action: prova.registra
        data: {passo: "automazione {{ trigger.to_state.state }}"}
      - delay: 0.5
      - action: script.turn_on
        target: {entity_id: [script.prova_coda_silenziosa, script.prova_coda_rumorosa]}
        data: {variables: {chi: "{{ trigger.to_state.state }}"}}
      - action: prova.registra
        data: {passo: "automazione dopo turn_on {{ trigger.to_state.state }}"}
  - alias: Prova Accoda Silenziosa
    mode: queued
    max: 2
    max_exceeded: silent
    triggers:
      - {trigger: state, entity_id: input_boolean.a}
    actions:
      - delay: 0.3
      - action: script.prova_coda_rumorosa
        data: {chi: "a {{ trigger.to_state.state }}"}
      - action: prova.registra
        data: {passo: "accoda silenziosa {{ trigger.to_state.state }}"}
  - alias: Prova Parallela Massimo
    mode: parallel
    max: 2
    triggers:
      - {trigger: state, entity_id: input_boolean.b}
    actions:
      - delay: 0.6
      - action: prova.registra
        data: {passo: "parallela {{ trigger.to_state.state }}"}
  - alias: Prova Accoda Informa
    mode: queued
    max: 2
    max_exceeded: info
    triggers:
      - {trigger: state, entity_id: input_boolean.b}
    actions:
      - delay: 0.6
      - action: prova.registra
        data: {passo: "informa {{ trigger.to_state.state }}"}
""",
    numero(1),
    numero(2),
    numero(3),
    numero(4),
    numero(5),
    attendi(0.4),
    numero(6),
    attendi(0.4),
    acceso("input_boolean.a"),
    spento("input_boolean.a"),
    acceso("input_boolean.a"),
    spento("input_boolean.a"),
    acceso("input_boolean.b"),
    spento("input_boolean.b"),
    acceso("input_boolean.b"),
    attendi(0.6),
    spento("input_boolean.b"),
    attendi(8),
    numero(7),
    attendi(0.5),
    chiama("script.prova_coda_rumorosa", {"chi": "diretta 1"}),
    chiama("script.prova_coda_rumorosa", {"chi": "diretta 2"}),
    chiama("script.prova_coda_rumorosa", {"chi": "diretta 3"}),
    attendi(6),
)

scenario(
    "single_gia_in_corso",
    # uno script single chiamato mentre è in corso: la chiamata bloccante torna subito,
    # script.turn_on aspetta il prossimo cambio dello script (la fine della pausa);
    # automazioni single con WARNING e SILENT ritriggerate durante la pausa
    """
script:
  prova_singola:
    alias: Prova Singola
    sequence:
      - action: prova.registra
        data: {passo: "singola {{ chi }}"}
      - delay: 2
      - action: prova.registra
        data: {passo: "singola dopo pausa {{ chi }}"}
      - wait_template: "{{ is_state('input_boolean.c', 'on') }}"
        timeout: 1
      - action: prova.registra
        data: {passo: "singola fine {{ chi }}"}
automation:
  - alias: Prova Chiama Singola
    mode: parallel
    triggers:
      - {trigger: state, entity_id: input_number.n}
    actions:
      - action: script.prova_singola
        data: {chi: "bloccante {{ trigger.to_state.state }}"}
      - action: prova.registra
        data: {passo: "dopo bloccante {{ trigger.to_state.state }}"}
  - alias: Prova Accendi Singola
    mode: parallel
    triggers:
      - {trigger: state, entity_id: input_boolean.a}
    actions:
      - action: script.turn_on
        target: {entity_id: script.prova_singola}
        data: {variables: {chi: "accesa {{ trigger.to_state.state }}"}}
      - action: prova.registra
        data: {passo: "dopo turn_on {{ trigger.to_state.state }}"}
  - alias: Prova Automazione Singola
    mode: single
    triggers:
      - {trigger: state, entity_id: input_boolean.b}
    actions:
      - action: prova.registra
        data: {passo: "automazione singola {{ trigger.to_state.state }}"}
      - delay: 1
      - action: prova.registra
        data: {passo: "automazione singola fine {{ trigger.to_state.state }}"}
  - alias: Prova Automazione Singola Silenziosa
    mode: single
    max_exceeded: silent
    triggers:
      - {trigger: state, entity_id: input_boolean.b}
    actions:
      - delay: 1
      - action: prova.registra
        data: {passo: "silenziosa {{ trigger.to_state.state }}"}
""",
    numero(1),
    attendi(0.5),
    numero(2),
    acceso("input_boolean.a"),
    attendi(1),
    spento("input_boolean.a"),
    chiama("script.prova_singola", {"chi": "diretta"}),
    chiama("script.turn_on", {"entity_id": "script.prova_singola"}),
    attendi(1),
    acceso("input_boolean.b"),
    attendi(0.4),
    spento("input_boolean.b"),
    attendi(0.4),
    acceso("input_boolean.b"),
    attendi(0.5),
    acceso("input_boolean.c"),
    attendi(1),
    acceso("input_boolean.b"),
    attendi(3),
)

scenario(
    "script_che_chiamano_script",
    # uno script restart che chiama uno script queued (bloccante, con la pausa dentro
    # una sequenza) e uno restart con script.turn_on; fermati a metà pausa con
    # script.turn_off (chiamante, chiamato, libero) e riavviati mentre aspettano
    """
script:
  prova_padre:
    alias: Prova Padre
    mode: restart
    sequence:
      - action: prova.registra
        data: {passo: "padre {{ chi }}"}
      - action: script.turn_on
        target: {entity_id: script.prova_libero}
        data: {variables: {chi: "{{ chi }}"}}
      - action: script.prova_figlio
        data: {chi: "{{ chi }}"}
      - action: prova.registra
        data: {passo: "padre dopo figlio {{ chi }}"}
      - delay: 1
      - action: prova.registra
        data: {passo: "padre fine {{ chi }}"}
  prova_figlio:
    alias: Prova Figlio
    mode: queued
    sequence:
      - action: prova.registra
        data: {passo: "figlio {{ chi }}"}
      - sequence:
          - alias: Pausa del figlio
            delay: 2
      - action: prova.registra
        data: {passo: "figlio fine {{ chi }}"}
  prova_libero:
    alias: Prova Libero
    mode: restart
    sequence:
      - action: prova.registra
        data: {passo: "libero {{ chi }}"}
      - delay: 3
      - action: prova.registra
        data: {passo: "libero fine {{ chi }}"}
automation:
  - alias: Prova Chiama Padre
    mode: restart
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on"}
    actions:
      - action: script.prova_padre
        data: {chi: automazione}
      - action: prova.registra
        data: {passo: dopo-padre}
""",
    chiama("script.prova_padre", {"chi": "1"}),
    attendi(1),
    servizio("script.turn_off", {"entity_id": "script.prova_padre"}),
    attendi(1),
    chiama(
        "script.turn_on", {"entity_id": "script.prova_padre", "variables": {"chi": 2}}
    ),
    attendi(0.5),
    chiama("script.prova_padre", {"chi": "3"}),
    attendi(1),
    servizio("script.turn_off", {"entity_id": "script.prova_figlio"}),
    attendi(1.5),
    servizio("script.turn_off", {"entity_id": "script.prova_libero"}),
    attendi(3),
    acceso("input_boolean.a"),
    # (le automazioni del motore non hanno automation.turn_off e turn_on)
    attendi(2.5),
    spento("input_boolean.a"),
    acceso("input_boolean.a"),
    attendi(0.7),
    spento("input_boolean.a"),
    acceso("input_boolean.a"),
    attendi(5),
)

scenario(
    "riavvii_nello_stesso_istante",
    # nello stesso istante: un'automazione restart con due trigger sullo stesso cambio;
    # uno script restart riavviato mentre la sua attesa diventa vera, o mentre scade
    # (il timer che accende B nasce con la stessa durata dell'attesa)
    """
script:
  prova_attende_riavvio:
    alias: Prova Attende Riavvio
    mode: restart
    sequence:
      - action: prova.registra
        data: {passo: "attende {{ chi }}"}
      - if: "{{ true }}"
        then:
          - wait_template: "{{ is_state('input_boolean.b', 'on') }}"
            timeout: 2
      - action: prova.registra
        data: {passo: "atteso {{ chi }} {{ wait.completed }} {{ wait.remaining }}"}
      - delay: 1
      - action: prova.registra
        data: {passo: "atteso fine {{ chi }}"}
automation:
  - alias: Prova Riavvio Doppio
    mode: restart
    triggers:
      - {trigger: state, entity_id: input_boolean.b, to: "on", id: uno}
      - {trigger: state, entity_id: input_boolean.b, id: due}
    actions:
      - action: prova.registra
        data: {passo: "doppio {{ trigger.id }}"}
      - delay: 1
      - action: prova.registra
        data: {passo: "doppio fine {{ trigger.id }}"}
  - alias: Prova Riavvia Attesa
    mode: parallel
    triggers:
      - {trigger: state, entity_id: input_boolean.b}
      - {trigger: state, entity_id: input_number.n}
    actions:
      - action: script.turn_on
        target: {entity_id: script.prova_attende_riavvio}
        data: {variables: {chi: "{{ trigger.entity_id }} {{ trigger.to_state.state }}"}}
      - action: prova.registra
        data: {passo: "riavviata {{ trigger.entity_id }} {{ trigger.to_state.state }}"}
  - alias: Prova Accende B
    mode: queued
    triggers:
      - {trigger: event, event_type: timer.finished, event_data: {entity_id: timer.t2}}
    actions:
      - action: input_boolean.toggle
        target: {entity_id: input_boolean.b}
""",
    numero(1),
    attendi(0.5),
    acceso("input_boolean.b"),
    attendi(2.5),
    spento("input_boolean.b"),
    attendi(1.5),
    numero(2),
    servizio("timer.start", {"entity_id": "timer.t2", "duration": 2}),
    attendi(3.5),
    servizio("timer.start", {"entity_id": "timer.t2", "duration": 2}),
    numero(3),
    attendi(1),
    servizio("script.turn_off", {"entity_id": "script.prova_attende_riavvio"}),
    attendi(1),
    numero(4),
    attendi(4),
)

scenario(
    "script_che_si_richiamano",
    # script che chiamano sé stessi con script.turn_on: restart (il nuovo avvio ferma
    # quello che lo ha chiesto, a metà della chiamata), queued (il nuovo avvio aspetta in
    # coda) e single (script.turn_on aspetta un cambio dello script, che non arriva finché
    # lo script non si ferma)
    """
script:
  prova_si_riavvia:
    alias: Prova Si Riavvia
    mode: restart
    sequence:
      - action: prova.registra
        data: {passo: "si riavvia {{ giro | default(0) }}"}
      - delay: 0.5
      - if: "{{ giro | default(0) < 3 }}"
        then:
          - action: script.turn_on
            target: {entity_id: script.prova_si_riavvia}
            data: {variables: {giro: "{{ giro | default(0) + 1 }}"}}
      - action: prova.registra
        data: {passo: "si riavvia fine {{ giro | default(0) }}"}
  prova_si_accoda:
    alias: Prova Si Accoda
    mode: queued
    sequence:
      - action: prova.registra
        data: {passo: "si accoda {{ giro | default(0) }}"}
      - if: "{{ giro | default(0) < 2 }}"
        then:
          - action: script.turn_on
            target: {entity_id: script.prova_si_accoda}
            data: {variables: {giro: "{{ giro | default(0) + 1 }}"}}
      - delay: 0.7
      - action: prova.registra
        data: {passo: "si accoda fine {{ giro | default(0) }}"}
  prova_si_blocca:
    alias: Prova Si Blocca
    sequence:
      - action: prova.registra
        data: {passo: si-blocca}
      - action: script.turn_on
        target: {entity_id: script.prova_si_blocca}
      - action: prova.registra
        data: {passo: mai-si-blocca}
""",
    servizio("script.turn_on", {"entity_id": "script.prova_si_riavvia"}),
    attendi(3),
    servizio("script.turn_on", {"entity_id": "script.prova_si_accoda"}),
    attendi(3),
    chiama("script.prova_si_blocca"),
    attendi(2),
    servizio("script.turn_off", {"entity_id": "script.prova_si_blocca"}),
    attendi(1),
)

# --- trigger modello con «for» -----------------------------------------------------------

scenario(
    "modello_con_for",
    # «for» con un modello (come i 132 trigger del package): il modello torna falso e
    # poi vero durante l'attesa, il valore di «for» cambia mentre il timer è in corso,
    # «for» non valido o negativo, «for» zero, un risultato vero che cambia valore
    """
automation:
  - alias: Prova Modello Per
    mode: queued
    triggers:
      - trigger: template
        value_template: "{{ is_state('input_boolean.a', 'on') }}"
        for: {seconds: "{{ states('input_number.n') | int(0) }}"}
        id: a-per
      - trigger: template
        value_template: "{{ states('input_number.n') | int(0) > 50 and states('input_number.n') }}"
        for: {seconds: 2}
        id: numero-vero
      - trigger: template
        value_template: "{{ is_state('input_boolean.b', 'on') }}"
        for: {seconds: "{{ 'non valido' if is_state('input_boolean.c', 'on') else -1 }}"}
        id: b-errato
      - trigger: template
        value_template: "{{ is_state('input_boolean.c', 'on') }}"
        for: {seconds: "{{ 0 }}"}
        id: c-zero
      - trigger: template
        value_template: "{{ is_state('input_boolean.b', 'on') and is_state('input_boolean.c', 'off') }}"
        for: {seconds: "{{ states('input_number.n') | float(0) / 10 }}"}
        id: b-decimi
      - trigger: template
        value_template: "{{ is_state('input_boolean.a', 'on') and is_state('input_boolean.b', 'on') }}"
        for: "{{ '00:00:0' ~ (states('input_number.n') | int(0) % 10) }}"
        id: a-e-b
    actions:
      - action: prova.registra
        data:
          passo: >-
            {{ trigger.id }} {{ trigger.for }} {{ trigger.entity_id }}
            {{ trigger.to_state.state if trigger.to_state else '' }} {{ trigger.description }}
""",
    numero(3),
    acceso("input_boolean.a"),
    attendi(1),
    spento("input_boolean.a"),
    attendi(0.5),
    acceso("input_boolean.a"),
    attendi(1),
    numero(1),
    attendi(2.5),
    spento("input_boolean.a"),
    numero(60),
    attendi(1),
    numero(70),
    attendi(3),
    numero(40),
    numero(80),
    attendi(2.5),
    acceso("input_boolean.b"),
    attendi(1),
    spento("input_boolean.b"),
    acceso("input_boolean.c"),
    acceso("input_boolean.b"),
    attendi(1),
    spento("input_boolean.c"),
    attendi(1),
    spento("input_boolean.b"),
    numero(15),
    acceso("input_boolean.b"),
    attendi(0.7),
    acceso("input_boolean.a"),
    attendi(1),
    numero(12),
    attendi(6),
)

scenario(
    "modello_vero_all_avvio",
    # trigger modello (con e senza «for») già veri quando si armano all'avvio: non
    # scattano finché non tornano falsi; uno falso all'avvio scatta dopo «for»
    """
automation:
  - alias: Prova Vero All Avvio
    id: prova_vero_all_avvio
    mode: parallel
    triggers:
      - trigger: template
        value_template: "{{ is_state('input_boolean.c', 'on') }}"
        for: {seconds: "{{ states('input_number.n') | int(0) }}"}
        id: c-per
      - trigger: template
        value_template: "{{ states('input_number.n') | int(0) > 2 }}"
        id: numero
      - trigger: template
        value_template: "{{ is_state('input_boolean.a', 'on') }}"
        for: {seconds: 1}
        id: a-per
    actions:
      - action: prova.registra
        data: {passo: "{{ trigger.id }} {{ trigger.for }} {{ trigger.description }}"}
      - delay: 1
      - action: prova.registra
        data: {passo: "{{ trigger.id }} fine"}
""",
    attendi(3),
    spento("input_boolean.c"),
    attendi(0.5),
    acceso("input_boolean.c"),
    attendi(1),
    numero(1),
    numero(4),
    attendi(5),
    avvio=True,
    aiutanti={
        "input_boolean": {"a": {}, "b": {}, "c": {"initial": True}},
        "input_number": {"n": {"min": 0, "max": 100, "step": 1, "initial": 3}},
    },
)

# --- attese -------------------------------------------------------------------------------

scenario(
    "attese_e_variabile_wait",
    # wait_template vero subito, vero prima del timeout, timeout con
    # continue_on_timeout vero e falso (come le 6 attese del package); wait.completed e
    # wait.remaining scritti per intero (la differenza tra due istanti dei timer)
    """
script:
  prova_attese:
    alias: Prova Attese
    mode: queued
    sequence:
      - wait_template: "{{ is_state('input_boolean.a', 'on') }}"
        timeout: 2
        continue_on_timeout: true
      - action: prova.registra
        data: {passo: "a {{ chi }} {{ wait.completed }} {{ wait.remaining }}"}
      - choose:
          - conditions: "{{ true }}"
            sequence:
              - alias: Attesa di B
                wait_template: "{{ is_state('input_boolean.b', 'on') }}"
                timeout: "00:00:01.5"
                continue_on_timeout: false
              - action: prova.registra
                data: {passo: "b {{ chi }} {{ wait.completed }} {{ wait.remaining }}"}
      - action: prova.registra
        data: {passo: "dopo b {{ chi }} {{ wait.completed }} {{ wait.remaining }}"}
      - wait_template: "{{ is_state('input_boolean.c', 'on') }}"
        timeout: {seconds: 1, milliseconds: 250}
        continue_on_timeout: true
      - action: prova.registra
        data: {passo: "c {{ chi }} {{ wait.completed }} {{ wait.remaining }}"}
automation:
  - alias: Prova Avvia Attese
    mode: queued
    triggers:
      - {trigger: state, entity_id: input_number.n}
    actions:
      - action: script.prova_attese
        data: {chi: "{{ trigger.to_state.state }}"}
      - action: prova.registra
        data: {passo: "dopo attese {{ trigger.to_state.state }} {{ wait is defined }}"}
  - alias: Prova Accende Dopo Timer
    mode: parallel
    triggers:
      - {trigger: event, event_type: timer.finished, event_data: {entity_id: timer.t2}}
    actions:
      - action: input_boolean.turn_on
        target: {entity_id: input_boolean.a}
""",
    acceso("input_boolean.a"),
    numero(1),
    attendi(0.7),
    acceso("input_boolean.b"),
    attendi(0.3),
    acceso("input_boolean.c"),
    attendi(1),
    spento("input_boolean.a"),
    spento("input_boolean.b"),
    spento("input_boolean.c"),
    numero(2),
    attendi(2),
    attendi(2),
    numero(3),
    servizio("timer.start", {"entity_id": "timer.t2", "duration": 2}),
    attendi(1.6),
    acceso("input_boolean.b"),
    attendi(1.3),
    spento("input_boolean.a"),
    spento("input_boolean.b"),
    servizio("timer.start", {"entity_id": "timer.t2", "duration": 1.5}),
    numero(4),
    attendi(1.5),
    attendi(1.5),
    spento("input_boolean.a"),
    numero(5),
    servizio("timer.start", {"entity_id": "timer.t2", "duration": 2}),
    attendi(5),
)

# --- pause --------------------------------------------------------------------------------

scenario(
    "pause_casi_limite",
    # pause zero (non cedono il ciclo), pause che finiscono nello stesso istante di un
    # trigger time_pattern, un ciclo «until» con molti giri e una pausa a ogni giro
    """
script:
  prova_zero:
    alias: Prova Zero
    mode: parallel
    sequence:
      - action: prova.registra
        data: {passo: "zero 1 {{ chi }}"}
      - delay: 0
      - action: prova.registra
        data: {passo: "zero 2 {{ chi }}"}
      - delay: "00:00:00"
      - action: prova.registra
        data: {passo: "zero 3 {{ chi }}"}
      - delay: {milliseconds: 0}
      - action: prova.registra
        data: {passo: "zero 4 {{ chi }}"}
  prova_giri:
    alias: Prova Giri
    mode: restart
    sequence:
      - repeat:
          until: "{{ states('input_number.n') | int(0) >= 40 }}"
          sequence:
            - action: input_number.increment
              target: {entity_id: input_number.n}
            - delay: {milliseconds: 50}
      - action: prova.registra
        data: {passo: "giri fine {{ states('input_number.n') }}"}
automation:
  - alias: Prova Zero Uno
    mode: parallel
    triggers:
      - {trigger: state, entity_id: input_boolean.a}
    actions:
      - action: script.turn_on
        target: {entity_id: script.prova_zero}
        data: {variables: {chi: "uno {{ trigger.to_state.state }}"}}
      - action: prova.registra
        data: {passo: "uno {{ trigger.to_state.state }}"}
      - delay: 0
      - action: prova.registra
        data: {passo: "uno dopo zero {{ trigger.to_state.state }}"}
  - alias: Prova Zero Due
    mode: parallel
    triggers:
      - {trigger: state, entity_id: input_boolean.a}
    actions:
      - action: script.prova_zero
        data: {chi: "due {{ trigger.to_state.state }}"}
      - action: prova.registra
        data: {passo: "due {{ trigger.to_state.state }}"}
  - alias: Prova Ritmo
    mode: queued
    triggers:
      - {trigger: time_pattern, seconds: "/2", id: ritmo}
      - {trigger: state, entity_id: input_boolean.b, to: "on", id: b}
    conditions: "{{ is_state('input_boolean.c', 'on') or trigger.id == 'b' }}"
    actions:
      - action: prova.registra
        data: {passo: "ritmo {{ trigger.id }} {{ now().strftime('%S.%f') }}"}
      - delay: 2
      - action: input_boolean.toggle
        target: {entity_id: input_boolean.b}
      - action: prova.registra
        data: {passo: "ritmo dopo pausa {{ trigger.id }} {{ now().strftime('%S.%f') }}"}
  - alias: Prova Conta Giri
    mode: parallel
    max: 100
    triggers:
      # numeric_state come modello (le attivazioni del motore non lo hanno)
      - {trigger: template, value_template: "{{ states('input_number.n') | float(0) > 9 }}"}
      - {trigger: template, value_template: "{{ states('input_number.n') | float(0) > 29 }}"}
    actions:
      - action: script.turn_on
        target: {entity_id: script.prova_giri}
      - action: prova.registra
        data: {passo: "riavvia giri {{ trigger.to_state.state }}"}
""",
    acceso("input_boolean.a"),
    spento("input_boolean.a"),
    attendi(0.5),
    acceso("input_boolean.c"),
    attendi(4.5),
    spento("input_boolean.c"),
    attendi(3),
    servizio("script.turn_on", {"entity_id": "script.prova_giri"}),
    attendi(1),
    servizio("script.turn_on", {"entity_id": "script.prova_giri"}),
    attendi(3),
)

# --- trigger di tempo -----------------------------------------------------------------------

scenario(
    "ore_a_mezzanotte",
    # trigger time con «at» in lista (anche mezzanotte) e time_pattern a cavallo della
    # mezzanotte; la pausa di 4 secondi finisce nello stesso istante del prossimo
    # time_pattern «/4» (coda: il nuovo avvio aspetta la fine del precedente)
    """
automation:
  - alias: Prova Mezzanotte
    mode: queued
    triggers:
      - {trigger: time, at: ["00:00:00", "23:59:55", "00:00:03"], id: ora}
      - {trigger: time_pattern, seconds: "/4", id: ritmo}
      - {trigger: time_pattern, minutes: "/1", id: minuto}
    actions:
      - action: prova.registra
        data:
          passo: "{{ trigger.id }} {{ trigger.now.isoformat() }} {{ now().day }}"
      - delay: 4
      - action: prova.registra
        data: {passo: "dopo pausa {{ trigger.id }} {{ now().strftime('%H:%M:%S.%f') }}"}
  - alias: Prova Ora Singola
    mode: single
    triggers:
      - {trigger: time, at: "00:00:00"}
      - {trigger: time_pattern, hours: 0, minutes: 0, seconds: 1}
    actions:
      - action: prova.registra
        data: {passo: "singola {{ trigger.platform }} {{ trigger.now.isoformat() }}"}
      - delay: 1.5
""",
    attendi(20),
    inizio=PRIMA_DI_MEZZANOTTE,
)

scenario(
    "avvio_e_chiusura",
    # trigger homeassistant start e shutdown; chiusura con pause in corso (le automazioni
    # del motore non hanno initial_state, automation.turn_off e turn_on: niente
    # automazioni spente e riaccese)
    """
script:
  prova_lungo:
    alias: Prova Lungo
    sequence:
      - action: prova.registra
        data: {passo: lungo}
      - delay: 10
      - action: prova.registra
        data: {passo: mai-lungo}
automation:
  - alias: Prova All Avvio
    id: prova_all_avvio
    mode: restart
    triggers:
      - {trigger: homeassistant, event: start, id: avvio}
      - {trigger: state, entity_id: input_boolean.a, to: "on", id: a}
    actions:
      - action: prova.registra
        data: {passo: "avvio {{ trigger.id }} {{ trigger.description | default('') }}"}
      - delay: 3
      - action: prova.registra
        data: {passo: "avvio fine {{ trigger.id }}"}
  - alias: Prova Riaccesa
    id: prova_riaccesa
    triggers:
      - {trigger: homeassistant, event: start}
    actions:
      - action: script.turn_on
        target: {entity_id: script.prova_lungo}
      - delay: 2
      - action: prova.registra
        data: {passo: riaccesa-fine}
  - alias: Prova Alla Chiusura
    id: prova_alla_chiusura
    mode: queued
    triggers:
      - {trigger: homeassistant, event: shutdown}
      - {trigger: state, entity_id: input_boolean.b}
    actions:
      - action: prova.registra
        data: {passo: "chiusura {{ trigger.platform }} {{ trigger.event | default('') }}"}
      - delay: 1
      - action: prova.registra
        data: {passo: "chiusura fine {{ trigger.platform }}"}
""",
    attendi(2.5),
    acceso("input_boolean.a"),
    attendi(4),
    acceso("input_boolean.b"),
    attendi(0.5),
    spento("input_boolean.a"),
    acceso("input_boolean.a"),
    attendi(0.5),
    arresto(),
    attendi(3),
    avvio=True,
)

scenario(
    "trigger_come_nel_package",
    # le forme dei trigger di tempo del package: due trigger time alla stessa ora nella
    # stessa automazione queued, state con «for» dizionario zero, con modello e
    # timedelta, template con «for» e enabled; come Aggiorna Aria Scambiata (single,
    # time_pattern «/1» e time alla stessa ora: il secondo trova la prima in corso)
    """
automation:
  - alias: Prova Filtro
    mode: queued
    max: 10
    triggers:
      - {trigger: time, at: "02:00:03", id: interfaccia, alias: Filtro Interfaccia}
      - {trigger: time, at: "02:00:03", id: mobile, alias: Filtro Mobile}
      - trigger: state
        entity_id: [input_boolean.a]
        from: "on"
        to: "off"
        for: {hours: 0, minutes: 0, seconds: 0}
        id: a-spento
      - trigger: state
        entity_id: input_boolean.b
        to: "on"
        for: {seconds: "{{ states('input_number.n') | int(0) }}"}
        id: b-per
      - trigger: state
        entity_id: input_boolean.c
        to: "on"
        for: "00:00:02"
        id: c-per
      - trigger: template
        value_template: "{{ is_state('input_boolean.a', 'on') and is_state('input_boolean.b', 'on') }}"
        for: {seconds: "{{ states('input_number.n') | int(16) }}"}
        id: modello
        enabled: true
    actions:
      - action: prova.registra
        data: {passo: "{{ trigger.id }} {{ trigger.for }} {{ now().strftime('%S.%f') }}"}
      - delay: 1
      - action: prova.registra
        data: {passo: "{{ trigger.id }} fine"}
  - alias: Prova Aria Scambiata
    triggers:
      - {trigger: time_pattern, seconds: /1}
      - {trigger: time, at: "02:00:05"}
    actions:
      - variables:
          quale: "{{ trigger.platform }}"
      - action: input_number.increment
        target: {entity_id: input_number.n}
      - action: prova.registra
        data: {passo: "aria {{ quale }} {{ trigger.now.strftime('%S.%f') }}"}
""",
    attendi(2),
    acceso("input_boolean.a"),
    spento("input_boolean.a"),
    attendi(1.5),
    acceso("input_boolean.c"),
    spento("input_boolean.c"),
    acceso("input_boolean.c"),
    numero(0),
    acceso("input_boolean.b"),
    attendi(2.5),
    # (le automazioni del motore non hanno automation.turn_off: Prova Aria Scambiata
    # continua)
    spento("input_boolean.b"),
    numero(2),
    acceso("input_boolean.a"),
    acceso("input_boolean.b"),
    attendi(1),
    spento("input_boolean.b"),
    acceso("input_boolean.b"),
    attendi(5),
)

# --- timer --------------------------------------------------------------------------------

scenario(
    "timer_e_loro_eventi",
    # timer.start, pause, cancel e finish da un'automazione restart; timer.finished e
    # timer.cancelled che fanno partire un'automazione; un timer che finisce nello stesso
    # istante di una pausa partita con lui; come l'automazione Countdown delle Letture del
    # package (time_pattern, homeassistant start e timer.finished con timer.start)
    """
automation:
  - alias: Prova Timer Eventi
    mode: queued
    max: 10
    triggers:
      - {trigger: event, event_type: timer.finished, id: finito}
      - {trigger: event, event_type: timer.cancelled, id: annullato}
      - {trigger: state, entity_id: timer.t1, id: stato}
    actions:
      - action: prova.registra
        data:
          passo: >-
            {{ trigger.id }}
            {{ trigger.event.data.entity_id if trigger.event is defined else trigger.to_state.state }}
            {{ state_attr('timer.t1', 'remaining') }}
  - alias: Prova Timer Comandi
    mode: restart
    triggers:
      - {trigger: state, entity_id: input_number.n}
    actions:
      - action: timer.start
        target: {entity_id: timer.t1}
        data: {duration: "00:00:0{{ trigger.to_state.state | int }}"}
      - delay: 1
      - choose:
          - conditions: "{{ trigger.to_state.state | int == 2 }}"
            sequence:
              - action: timer.pause
                target: {entity_id: timer.t1}
              - delay: 1.5
              - action: timer.start
                target: {entity_id: timer.t1}
          - conditions: "{{ trigger.to_state.state | int == 3 }}"
            sequence:
              - action: timer.cancel
                target: {entity_id: timer.t1}
          - conditions: "{{ trigger.to_state.state | int == 4 }}"
            sequence:
              - action: timer.finish
                target: {entity_id: timer.t1}
      - action: prova.registra
        data: {passo: "comandi fine {{ trigger.to_state.state }} {{ states('timer.t1') }}"}
  - alias: Prova Timer Coincide
    mode: restart
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on"}
    actions:
      - action: timer.start
        target: {entity_id: timer.t2}
        data: {duration: 2}
      - delay: 2
      - action: prova.registra
        data: {passo: "pausa finita {{ states('timer.t2') }}"}
  - alias: Prova Conto Alla Rovescia
    mode: queued
    max: 10
    triggers:
      - {trigger: time_pattern, seconds: "/3", id: allinea}
      - {trigger: event, event_type: timer.finished, id: scaduto}
    conditions: "{{ is_state('input_boolean.c', 'on') }}"
    actions:
      - if:
          - condition: template
            value_template: "{{ trigger.id == 'scaduto' or not is_state('timer.t2', 'active') }}"
        then:
          - action: timer.start
            target: {entity_id: timer.t2}
            data:
              duration: "{{ '00:00:%02d' % (2 if trigger.id == 'scaduto' else 1) }}"
""",
    numero(3),
    attendi(1.5),
    numero(2),
    attendi(0.5),
    numero(4),
    attendi(2),
    numero(2),
    attendi(5),
    numero(6),
    attendi(7),
    acceso("input_boolean.a"),
    attendi(3),
    acceso("input_boolean.c"),
    attendi(9),
    spento("input_boolean.c"),
    attendi(3),
)


# --- macchina delle prove -------------------------------------------------------------------


class _Messaggi(logging.Handler):
    """Annota nel registro i messaggi di max_exceeded (livello e testo)."""

    def __init__(self, registro: list[Any], istante: Any) -> None:
        super().__init__(logging.DEBUG)
        self.registro = registro
        self.istante = istante

    def emit(self, record: logging.LogRecord) -> None:
        messaggio = record.getMessage()
        if messaggio.endswith(MESSAGGI_MASSIMO):
            self.registro.append((self.istante(), "log", record.levelname, messaggio))


def _norma(valore: Any, inizio: datetime) -> Any:
    """Un valore del registro senza ciò che cambia da una corsa all'altra; gli istanti
    in secondi dall'inizio, al microsecondo."""
    if isinstance(valore, datetime):
        return round((valore - inizio).total_seconds(), 6)
    if isinstance(valore, Context):
        return None
    if isinstance(valore, State):
        return (valore.entity_id, valore.state, _norma(dict(valore.attributes), inizio))
    if isinstance(valore, dict):
        # le chiavi come testo (gli attributi delle entità di Home Assistant sono StrEnum,
        # uguali al loro testo ma con un'altra repr)
        return {
            str(k) if isinstance(k, str) else k: _norma(v, inizio)
            for k, v in sorted(valore.items())
            if k != "run_id"
        }
    if isinstance(valore, (list, tuple)):
        return [_norma(v, inizio) for v in valore]
    return valore


def _pulisci_timer(hass: HomeAssistant, chiave: Callable[[Any], Any]) -> None:
    """Toglie dalla coda dei timer di asyncio quelli cancellati (durante l'avvio, diversi
    con il YAML e con il motore) e la riordina con ``chiave``."""
    loop = hass.loop
    vivi = []
    for maniglia in loop._scheduled:
        if maniglia.cancelled():
            maniglia._scheduled = False
        else:
            vivi.append(maniglia)
    vivi.sort(key=chiave)
    loop._scheduled[:] = vivi
    loop._timer_cancelled_count = 0


async def _avanza(
    hass: HomeAssistant,
    freezer: FrozenDateTimeFactory,
    secondi: float,
    passo: float | None = None,
) -> None:
    """L'orologio avanza di ``secondi``.

    Senza ``passo`` salta da un timer al successivo: ogni timer scatta al primo
    microsecondo in cui è dovuto (asyncio lo esegue solo quando l'orologio ha superato il
    suo istante) e il ciclo lavora fino a fermarsi. Con ``passo`` avanza a passi fissi,
    come il simulatore: i timer di un passo scattano insieme, nell'ordine dei loro istanti.
    """
    loop = hass.loop
    mancano = round(secondi * 1_000_000)
    fisso = None if passo is None else round(passo * 1_000_000)
    await _gira(hass)
    while mancano > 0:
        salto = mancano
        if fisso is not None:
            salto = min(salto, fisso)
        elif (
            prossimo := min(
                (m.when() for m in loop._scheduled if not m.cancelled()), default=None
            )
        ) is not None:
            salto = min(salto, max(1, math.ceil((prossimo - loop.time()) * 1_000_000)))
        freezer.tick(timedelta(microseconds=salto))
        mancano -= salto
        await _gira(hass)


async def _fino_alla_fine(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory, compito: asyncio.Future[Any]
) -> None:
    """Il ciclo lavora (e l'orologio salta al timer successivo quando è fermo) finché il
    compito non finisce."""
    for _ in range(10_000):
        await _gira(hass)
        if compito.done():
            return
        await _avanza(hass, freezer, 0.1)
    raise AssertionError("il compito non finisce")


async def _corsa(
    freezer: FrozenDateTimeFactory,
    nome: str,
    prova: dict[str, Any],
    *,
    motore: bool,
    moduli: list[str],  # noqa: F811
    chiave: Callable[[Any], Any],
    a_passi: float | None,
) -> list[Any]:
    inizio: datetime = prova["inizio"]
    freezer.move_to(inizio)
    registro: list[Any] = []
    configurazione = yaml.safe_load(prova["configurazione"])
    stato_iniziale = CoreState.not_running if prova["avvio"] else CoreState.running

    def istante() -> float:
        return _norma(dt_util.utcnow(), inizio)

    messaggi = _Messaggi(registro, istante)
    radice = logging.getLogger()
    radice.addHandler(messaggi)
    try:
        async with async_test_home_assistant(initial_state=stato_iniziale) as hass:
            # i contesti (id casuali) come numeri d'ordine: si confronta chi ha causato
            # cosa
            contesti: dict[str | None, int | None] = {None: None}

            def contesto(identificativo: str | None) -> int | None:
                return contesti.setdefault(identificativo, len(contesti) - 1)

            pulizia = False

            @callback
            def annota(evento: Event) -> None:
                if evento.event_type not in EVENTI:
                    return
                if pulizia and della_pulizia(evento):
                    return
                dati = evento.data
                if evento.event_type == EVENT_STATE_CHANGED:
                    dati = {
                        "entity_id": dati["entity_id"],
                        "new_state": dati["new_state"],
                    }
                registro.append(
                    (
                        _norma(evento.time_fired, inizio),
                        evento.event_type,
                        _norma(dict(dati), inizio),
                        contesto(evento.context.id),
                        contesto(evento.context.parent_id),
                    )
                )

            assert await async_setup_component(hass, "homeassistant", {})
            for dominio, voci in prova["aiutanti"].items():
                assert await async_setup_component(hass, dominio, {dominio: voci})

            async def registra(chiamata: Any) -> None:
                if chiamata.data.get("errore"):
                    raise HomeAssistantError("errore voluto")

            hass.services.async_register("prova", "registra", registra)
            automazioni = configurazione.get("automation", [])
            script = configurazione.get("script", {})
            if motore:
                testo_modelli, testo_motore = await traduci_configurazione(
                    hass, automazioni, script, nome_modelli=f"tempi_{nome}_modelli"
                )
                moduli.append(f"{generato.__name__}.tempi_{nome}_modelli")
                moduli.append(f"{generato.__name__}.tempi_{nome}_motore")
                _carica(f"tempi_{nome}_modelli", testo_modelli)
                codice = _carica(f"tempi_{nome}_motore", testo_motore)
                m = MotoreFase3(hass)
                await m.avvia(crea=codice.crea)
            else:
                assert await async_setup_component(hass, "script", {"script": script})
                assert await async_setup_component(
                    hass, "automation", {"automation": automazioni}
                )
            if prova["avvio"]:
                await hass.async_block_till_done()
            await _gira(hass)
            _pulisci_timer(hass, chiave)
            hass.bus.async_listen(MATCH_ALL, annota)
            if motore:
                # gli stati delle logiche (le automazioni del motore) non sono nella
                # macchina degli stati: entrano nel registro nel punto del bus di
                # state_changed
                stati_logiche(hass).osserva(
                    callback(
                        lambda e: annota(e) if e.event_type == EVENT_STATE_CHANGED else None
                    )
                )
            if prova["avvio"]:
                avvio = asyncio.ensure_future(hass.async_start())
                await _fino_alla_fine(hass, freezer, avvio)
                registro.append((istante(), "avviato"))

            chiamate: list[asyncio.Future[Any]] = []
            for passo in prova["passi"]:
                if passo[0] == "servizio":
                    dominio, nome_servizio = passo[1].split(".")
                    await hass.services.async_call(
                        dominio, nome_servizio, passo[2], blocking=True
                    )
                    await _gira(hass)
                elif passo[0] == "chiama":
                    chiamate.append(
                        asyncio.ensure_future(
                            _chiama(hass, registro, istante, passo[1], passo[2])
                        )
                    )
                    await _gira(hass)
                elif passo[0] == "attendi":
                    await _avanza(hass, freezer, passo[1], a_passi)
                else:
                    fermata = asyncio.ensure_future(hass.async_stop())
                    await _fino_alla_fine(hass, freezer, fermata)
                    registro.append((istante(), "fermato"))
            if hass.state is CoreState.running:
                # con Home Assistant spegne le automazioni (automation.turn_off), con il
                # motore ferma le logiche: i loro stati non si confrontano
                pulizia = True
                if motore:
                    await m.ferma()
                else:
                    await hass.services.async_call(
                        "automation", "turn_off", {"entity_id": "all"}, blocking=True
                    )
                await hass.services.async_call(
                    "script", "turn_off", {"entity_id": "all"}, blocking=True
                )
                await _gira(hass)
                registro.append((istante(), "fine"))
                await hass.async_stop(force=True)
            # i 60 secondi dopo la chiusura (_schedule_stop_scripts_after_shutdown)
            freezer.tick(timedelta(seconds=61))
            await _gira(hass)
            # i trigger time_pattern restano armati dopo la chiusura (come con il YAML)
            for maniglia in hass.loop._scheduled:
                maniglia.cancel()
            for chiamata in chiamate:
                if not chiamata.done():
                    chiamata.cancel()
            await asyncio.gather(*chiamate, return_exceptions=True)
    finally:
        radice.removeHandler(messaggi)
    return registro


async def _chiama(
    hass: HomeAssistant,
    registro: list[Any],
    istante: Any,
    nome: str,
    dati: dict[str, Any],
) -> None:
    """Un servizio atteso in un task: la fine si annota con l'istante."""
    dominio, nome_servizio = nome.split(".")
    etichetta = f"{nome} {dati}"
    try:
        await hass.services.async_call(dominio, nome_servizio, dati, blocking=True)
    except BaseException as err:
        registro.append((istante(), "fine chiamata", etichetta, type(err).__name__))
        raise
    registro.append((istante(), "fine chiamata", etichetta))


@pytest.fixture
def wait_for_stop_scripts_after_shutdown() -> bool:
    """Alla chiusura Home Assistant ferma dopo 60 secondi gli script ancora in corso
    (il plugin dei test lo toglie: qui serve vero)."""
    return True


@pytest.fixture
def ordine_dei_timer(monkeypatch: pytest.MonkeyPatch) -> Callable[[Any], Any]:
    """Due timer di asyncio con lo stesso istante escono dalla coda nell'ordine in cui
    sono nati.

    Con l'orologio fermo due timer per lo stesso istante (due pause partite insieme, due
    trigger time alla stessa ora...) hanno lo stesso ``when``; asyncio non li ordina e
    l'ordine con cui escono dalla coda (un heap) dipende dalla sua forma, cioè da tutti
    i timer, anche cancellati, passati di lì dall'avvio. Con l'orologio vero i due
    istanti differiscono di poco, nell'ordine in cui i timer sono nati: qui lo stesso
    ordine, uguale per Home Assistant e per il motore se nascono nello stesso ordine.
    Restituisce la chiave di ordinamento (istante, numero di nascita)."""
    nati: dict[int, tuple[int, asyncio.TimerHandle]] = {}
    contatore = itertools.count()
    originale = asyncio.TimerHandle.__init__

    def __init__(self: asyncio.TimerHandle, *args: Any, **kwargs: Any) -> None:
        originale(self, *args, **kwargs)
        nati[id(self)] = (next(contatore), self)

    def chiave(maniglia: asyncio.TimerHandle) -> tuple[float, int]:
        voce = nati.get(id(maniglia))
        return (
            maniglia._when,
            voce[0] if voce is not None and voce[1] is maniglia else -1,
        )

    def __lt__(self: asyncio.TimerHandle, altro: Any) -> bool:
        if isinstance(altro, asyncio.TimerHandle):
            return chiave(self) < chiave(altro)
        return NotImplemented

    monkeypatch.setattr(asyncio.TimerHandle, "__init__", __init__)
    monkeypatch.setattr(asyncio.TimerHandle, "__lt__", __lt__)
    return chiave


@pytest.fixture
def tempi_casuali(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Home Assistant sposta i trigger time e time_pattern di una frazione di secondo a
    caso: in entrambe le corse la stessa (la minima)."""
    monkeypatch.setattr(
        "homeassistant.helpers.event.randint", lambda minimo, massimo: minimo
    )
    yield


@pytest.mark.usefixtures("tempi_casuali")
@pytest.mark.parametrize("passo", [None, 0.1], ids=["timer_per_timer", "a_passi"])
@pytest.mark.parametrize("nome", sorted(SCENARI))
async def test_tempi_come_home_assistant(
    nome: str,
    passo: float | None,
    freezer: FrozenDateTimeFactory,
    moduli: list[str],  # noqa: F811
    ordine_dei_timer: Callable[[Any], Any],
) -> None:
    """Stesso registro degli eventi, istante per istante, con Home Assistant e con il
    motore tradotto; l'orologio salta da un timer all'altro, o avanza a passi di 0,1 s
    come nel simulatore."""
    prova = SCENARI[nome]
    atteso = await _corsa(
        freezer,
        nome,
        prova,
        motore=False,
        moduli=moduli,
        chiave=ordine_dei_timer,
        a_passi=passo,
    )
    ottenuto = await _corsa(
        freezer,
        nome,
        prova,
        motore=True,
        moduli=moduli,
        chiave=ordine_dei_timer,
        a_passi=passo,
    )
    assert any(
        voce[1] == EVENT_CALL_SERVICE and voce[2]["domain"] == "prova"
        for voce in atteso
    )
    if ottenuto != atteso:
        diff = "\n".join(
            difflib.unified_diff(
                [repr(v) for v in atteso],
                [repr(v) for v in ottenuto],
                "home_assistant",
                "motore",
                lineterm="",
                n=3,
            )
        )
        pytest.fail(f"registri diversi:\n{diff}")
