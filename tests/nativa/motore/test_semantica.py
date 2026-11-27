"""Il motore tradotto si comporta come Home Assistant: prove mirate a confronto.

Ogni prova scrive automazioni e script in YAML, li fa girare con Home Assistant e poi,
tradotti dallo stesso traduttore del package, con il motore; con lo stesso orologio e gli
stessi passi, il registro degli eventi (servizi chiamati, stati e attributi delle
entità, automazioni e script avviati, con l'istante) deve essere identico.
"""

from __future__ import annotations

import asyncio
import difflib
import sys
import types
from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from typing import Any

import pytest
import yaml
from freezegun.api import FrozenDateTimeFactory
from homeassistant.const import EVENT_CALL_SERVICE, EVENT_STATE_CHANGED, MATCH_ALL
from homeassistant.core import (
    Context,
    Event,
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
    State,
    SupportsResponse,
    callback,
)
from homeassistant.exceptions import HomeAssistantError
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import async_test_home_assistant

from custom_components.vmc_master.nativa.motore import generato
from custom_components.vmc_master.nativa.motore.ha import Motore

from .traduci import traduci_configurazione

T0 = datetime(2026, 11, 25, 10, 0, 0, tzinfo=UTC)
PASSO = 0.1
AIUTANTI = {
    "input_boolean": {"a": {}, "b": {}, "c": {}},
    "input_number": {"n": {"min": 0, "max": 100, "step": 1}},
}
EVENTI = {
    EVENT_STATE_CHANGED,
    EVENT_CALL_SERVICE,
    "automation_triggered",
    "script_started",
    "prova",
}

SCENARI: dict[str, tuple[str, list[tuple[Any, ...]]]] = {}


def scenario(nome: str, configurazione: str, *passi: tuple[Any, ...]) -> None:
    SCENARI[nome] = (configurazione, list(passi))


def acceso(entita: str) -> tuple[Any, ...]:
    return ("servizio", "input_boolean.turn_on", {"entity_id": entita})


def spento(entita: str) -> tuple[Any, ...]:
    return ("servizio", "input_boolean.turn_off", {"entity_id": entita})


def numero(valore: float) -> tuple[Any, ...]:
    return (
        "servizio",
        "input_number.set_value",
        {"entity_id": "input_number.n", "value": valore},
    )


def attendi(secondi: float) -> tuple[Any, ...]:
    return ("attendi", secondi)


def sonda(entita: str, secondi: float) -> list[tuple[Any, ...]]:
    """Per ``secondi``, a ogni passo l'entità riscrive il suo stato
    (``homeassistant.update_entity``): ogni cambio di un attributo, come
    ``last_action`` di uno script, finisce nel registro all'istante in cui c'è."""
    passi: list[tuple[Any, ...]] = []
    for _ in range(round(secondi / PASSO)):
        passi.append(("servizio", "homeassistant.update_entity", {"entity_id": entita}))
        passi.append(attendi(PASSO))
    return passi


scenario(
    "coda_scelte_condizioni",
    """
automation:
  - alias: Prova Coda
    id: prova_coda
    mode: queued
    max: 5
    triggers:
      - {trigger: state, entity_id: input_boolean.a, id: a}
      - {trigger: state, entity_id: input_boolean.b, id: b}
    conditions:
      - condition: template
        value_template: "{{ trigger.to_state.state in ['on', 'off'] }}"
    actions:
      - choose:
          - conditions:
              - {condition: trigger, id: a}
            sequence:
              - action: prova.registra
                data: {passo: "a {{ trigger.to_state.state }}"}
              - delay: 2
              - alias: Seconda chiamata
                action: prova.registra
                data: {passo: a2}
          - conditions: "{{ trigger.id == 'b' and is_state('input_boolean.a', 'on') }}"
            sequence:
              - action: prova.registra
                data: {passo: b-con-a}
        default:
          - action: prova.registra
            data: {passo: default}
      - alias: C spento
        condition: template
        value_template: "{{ is_state('input_boolean.c', 'off') }}"
      - action: prova.registra
        data: {passo: fine}
""",
    acceso("input_boolean.a"),
    attendi(0.5),
    acceso("input_boolean.b"),
    attendi(0.5),
    acceso("input_boolean.c"),
    attendi(5),
    spento("input_boolean.c"),
    spento("input_boolean.a"),
    attendi(3),
)

scenario(
    "script_restart_queued_single",
    """
script:
  prova_restart:
    alias: Prova Restart
    mode: restart
    fields:
      x: {description: valore}
    sequence:
      - action: prova.registra
        data: {passo: "inizio {{ x | default('nessuno') }}"}
      - delay: {seconds: 3}
      - action: prova.registra
        data: {passo: "fine {{ x | default('nessuno') }}"}
  prova_single:
    alias: Prova Single
    sequence:
      - delay: 1
      - action: prova.registra
        data: {passo: single}
  prova_coda_script:
    mode: queued
    sequence:
      - action: script.prova_single
      - action: prova.registra
        data: {passo: dopo-single}
automation:
  - alias: Prova Chiama Script
    id: prova_chiama
    mode: parallel
    triggers:
      - {trigger: state, entity_id: input_number.n}
    actions:
      - action: script.turn_on
        target: {entity_id: script.prova_restart}
        data:
          variables:
            x: "{{ trigger.to_state.state | int }}"
      - action: script.prova_coda_script
      - action: prova.registra
        data: {passo: "chiamata {{ trigger.to_state.state }}"}
""",
    numero(1),
    attendi(1),
    numero(2),
    attendi(0.5),
    numero(3),
    attendi(6),
)

scenario(
    "attese",
    """
automation:
  - alias: Prova Attese
    id: prova_attese
    mode: single
    max_exceeded: silent
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on"}
    actions:
      - wait_template: "{{ is_state('input_boolean.b', 'on') }}"
        timeout: 3
      - action: prova.registra
        data:
          completata: "{{ wait.completed }}"
          resto: "{{ wait.remaining | round(1) if wait.remaining is not none else 'nessuno' }}"
      - alias: Attesa di C
        wait_template: "{{ is_state('input_boolean.c', 'on') }}"
        timeout: "00:00:02"
        continue_on_timeout: false
      - action: prova.registra
        data: {passo: dopo-c}
""",
    acceso("input_boolean.a"),
    attendi(1.2),
    acceso("input_boolean.b"),
    attendi(4),
    spento("input_boolean.a"),
    spento("input_boolean.b"),
    acceso("input_boolean.a"),
    attendi(4),
    spento("input_boolean.a"),
    acceso("input_boolean.b"),
    acceso("input_boolean.a"),
    attendi(1),
    acceso("input_boolean.c"),
    attendi(2),
)

scenario(
    "ripetizioni_e_variabili",
    """
script:
  prova_ripeti:
    sequence:
      - variables:
          totale: 0
      - repeat:
          count: "{{ 3 }}"
          sequence:
            - variables:
                totale: "{{ totale + repeat.index }}"
            - action: prova.registra
              data:
                passo: "conta {{ repeat.index }} {{ repeat.first }} {{ repeat.last }} {{ totale }}"
      - repeat:
          for_each: ["x", "y"]
          sequence:
            - repeat:
                while: "{{ repeat.index < 3 }}"
                sequence:
                  - action: prova.registra
                    data: {passo: "interno {{ repeat.index }} {{ repeat.item | default('?') }}"}
                  - delay: 0.5
            - action: prova.registra
              data: {passo: "esterno {{ repeat.item }}"}
      - repeat:
          until:
            - condition: template
              value_template: "{{ repeat.index >= 2 }}"
          sequence:
            - action: prova.registra
              data: {passo: "finche {{ repeat.index }} totale {{ totale }}"}
automation:
  - alias: Prova Avvia Ripeti
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on"}
    actions:
      - action: script.prova_ripeti
      - action: prova.registra
        data: {passo: "dopo {{ totale | default('non visibile') }}"}
""",
    acceso("input_boolean.a"),
    attendi(5),
)

scenario(
    "errori_e_stop",
    """
script:
  prova_errori:
    sequence:
      - action: prova.registra
        data: {errore: true}
        continue_on_error: true
      - action: prova.registra
        data: {eccezione: true}
        continue_on_error: true
      - action: prova.registra
        data: {passo: dopo-errori}
      - if: "{{ true }}"
        then:
          - condition: template
            value_template: "{{ false }}"
          - action: prova.registra
            data: {passo: mai}
      - action: prova.registra
        data: {passo: dopo-if}
      - sequence:
          - stop: fine voluta
      - action: prova.registra
        data: {passo: mai2}
  prova_errore_modello:
    sequence:
      - action: prova.registra
        data: {passo: "{{ states('sensor.nessuno') | float + 1 }}"}
      - action: prova.registra
        data: {passo: mai3}
  prova_stop_errore:
    sequence:
      - action: prova.registra
        data: {passo: prima}
      - stop: errore voluto
        error: true
  prova_errore_secco:
    sequence:
      - action: prova.registra
        data: {errore: true}
      - action: prova.registra
        data: {passo: mai4}
automation:
  - alias: Prova Errori
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on"}
    actions:
      - action: script.prova_errori
      - action: script.prova_errore_modello
        continue_on_error: true
      - action: prova.registra
        data: {passo: dopo-modello}
      - action: script.prova_stop_errore
        continue_on_error: true
      - action: prova.registra
        data: {passo: dopo-stop-errore}
      - action: script.prova_errore_secco
      - action: prova.registra
        data: {passo: mai5}
  - alias: Prova Errore Condizione
    triggers:
      - {trigger: state, entity_id: input_boolean.b, to: "on"}
    conditions:
      - condition: state
        entity_id: sensor.nessuno
        state: "on"
    actions:
      - action: prova.registra
        data: {passo: mai6}
""",
    acceso("input_boolean.a"),
    attendi(1),
    acceso("input_boolean.b"),
    attendi(1),
)

scenario(
    "ordine_nello_stesso_istante",
    """
automation:
  - alias: Prova Uno
    mode: parallel
    triggers:
      - {trigger: state, entity_id: input_boolean.b}
    actions:
      - action: prova.registra
        data: {passo: uno-1}
      - choose:
          - conditions: "{{ true }}"
            sequence:
              - action: prova.registra
                data: {passo: uno-2}
              - delay: 0
              - action: prova.registra
                data: {passo: uno-3}
      - action: input_boolean.toggle
        target: {entity_id: input_boolean.c}
      - action: prova.registra
        data: {passo: uno-4}
  - alias: Prova Due
    mode: parallel
    triggers:
      - {trigger: state, entity_id: input_boolean.b}
      - {trigger: state, entity_id: input_boolean.c}
    actions:
      - action: prova.registra
        data: {passo: "due {{ trigger.entity_id }}"}
      - if: "{{ is_state('input_boolean.c', 'on') }}"
        then:
          - action: prova.registra
            data: {passo: due-c-on}
        else:
          - delay: 0.3
          - action: prova.registra
            data: {passo: due-c-off}
""",
    acceso("input_boolean.b"),
    spento("input_boolean.b"),
    attendi(1),
    acceso("input_boolean.b"),
    attendi(1),
)

scenario(
    "variabili_e_trigger",
    """
automation:
  - alias: Prova Variabili
    id: prova_variabili
    variables:
      doppio: "{{ (states('input_number.n') | float(0)) * 2 }}"
      fisso: 7
    triggers:
      - trigger: template
        value_template: "{{ states('input_number.n') | float(0) > 50 }}"
        for: {seconds: 2}
        id: alto
      - trigger: numeric_state
        entity_id: input_number.n
        below: 10
        id: basso
    actions:
      - action: prova.registra
        data: {passo: "{{ trigger.id }} {{ doppio }} {{ fisso }} {{ this.state }}"}
""",
    numero(60),
    attendi(3),
    numero(5),
    attendi(1),
    numero(70),
    attendi(1),
    numero(20),
    attendi(3),
)

scenario(
    "single_e_massimo",
    """
script:
  prova_lenta:
    mode: queued
    max: 2
    sequence:
      - delay: 1
      - action: prova.registra
        data: {passo: "lenta {{ n }}"}
automation:
  - alias: Prova Single
    mode: single
    triggers:
      - {trigger: state, entity_id: input_number.n}
    actions:
      - action: script.turn_on
        target: {entity_id: script.prova_lenta}
        data: {variables: {n: "{{ trigger.to_state.state }}"}}
      - delay: 1.5
""",
    numero(1),
    attendi(0.2),
    numero(2),
    attendi(0.2),
    numero(3),
    attendi(0.2),
    numero(4),
    attendi(2),
    numero(5),
    attendi(6),
)

scenario(
    "stop_annidato_risposta_variabili",
    """
script:
  prova_ferma:
    mode: parallel
    sequence:
      - repeat:
          until: "{{ repeat.index >= 5 }}"
          sequence:
            - choose:
                - conditions: "{{ repeat.index == 3 }}"
                  sequence:
                    - action: prova.registra
                      data: {passo: "ferma al giro {{ repeat.index }}"}
                    - stop: basta
            - action: prova.registra
              data: {passo: "giro {{ repeat.index }}"}
            - delay: 0.2
      - action: prova.registra
        data: {passo: mai}
  prova_risposta:
    sequence:
      - action: prova.risposta
        data: {x: 41}
        response_variable: esito
      - if: "{{ esito.valore == 41 }}"
        then:
          - variables:
              messaggio: "risposta {{ esito.valore + 1 }}"
        else:
          - variables:
              messaggio: diversa
      - action: prova.registra
        data: {passo: "{{ messaggio }} {{ this.state }} {{ context.id is string }}"}
automation:
  - alias: Prova Ferma
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on"}
    actions:
      - action: script.prova_ferma
      - action: prova.registra
        data: {passo: dopo-ferma}
      - action: script.prova_risposta
      - stop: fine automazione
      - action: prova.registra
        data: {passo: mai2}
""",
    acceso("input_boolean.a"),
    attendi(2),
)

scenario(
    "pause_e_attese_con_modelli",
    """
script:
  prova_pause:
    mode: queued
    max: 3
    sequence:
      - delay: "{{ (states('input_number.n') | int(0)) / 10 }}"
      - action: prova.registra
        data: {passo: "pausa {{ states('input_number.n') }}"}
      - delay:
          seconds: "{{ 1 if is_state('input_boolean.b', 'on') else 0 }}"
      - alias: Attesa di A spento
        wait_template: "{{ is_state('input_boolean.a', 'off') }}"
        timeout: "{{ states('input_number.n') | int(0) / 10 }}"
      - action: prova.registra
        data: {passo: "attesa {{ wait.completed }}"}
      - delay: "{{ 'non valido' if is_state('input_boolean.c', 'on') else 0 }}"
      - action: prova.registra
        data: {passo: fine-pause}
automation:
  - alias: Prova Pause
    mode: queued
    triggers:
      - {trigger: state, entity_id: input_number.n}
    actions:
      - action: script.turn_on
        target: {entity_id: script.prova_pause}
""",
    acceso("input_boolean.a"),
    numero(15),
    attendi(0.5),
    acceso("input_boolean.b"),
    attendi(2),
    spento("input_boolean.a"),
    attendi(1),
    acceso("input_boolean.c"),
    numero(5),
    attendi(3),
)

scenario(
    "condizioni_di_stato",
    """
automation:
  - alias: Prova Stato
    mode: queued
    triggers:
      - {trigger: state, entity_id: [input_boolean.a, input_boolean.b, input_number.n]}
    actions:
      - choose:
          - conditions:
              - condition: state
                entity_id: [input_boolean.a, input_boolean.b]
                state: ["on", "unavailable"]
            sequence:
              - action: prova.registra
                data: {passo: entrambi}
          - conditions:
              - condition: state
                entity_id: [input_boolean.a, input_boolean.b]
                match: any
                state: "on"
              - condition: or
                conditions:
                  - condition: state
                    entity_id: input_number.n
                    state: "10.0"
                  - "{{ states('input_number.n') | float(0) > 50 }}"
            sequence:
              - action: prova.registra
                data: {passo: uno-e-numero}
          - conditions:
              - condition: state
                entity_id: input_number.n
                attribute: step
                state: 1
              - condition: and
                conditions:
                  - condition: state
                    entity_id: input_boolean.c
                    state: input_boolean.a
            sequence:
              - action: prova.registra
                data: {passo: attributo}
        default:
          - action: prova.registra
            data: {passo: nessuna}
""",
    acceso("input_boolean.a"),
    numero(10),
    acceso("input_boolean.b"),
    spento("input_boolean.a"),
    numero(60),
    spento("input_boolean.b"),
    numero(20),
    attendi(1),
)

scenario(
    "variabili_liste_e_dizionari",
    """
automation:
  - alias: Prova Liste
    id: prova_liste
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on"}
    variables:
      lista: "{{ [3, 4] }}"
    actions:
      - variables:
          diz: "{{ {'x': 1, 'y': [5, 6]} }}"
          coppia: "{{ (7, 8) }}"
      - action: prova.registra
        data:
          primo: "{{ lista[0] }}"
          quanti: "{{ lista | length }}"
          ultimo: "{{ diz.y[-1] }}"
          chiavi: "{{ diz.keys() | list }}"
          coppia: "{{ coppia[1] }}"
          tipi: "{{ lista is list }} {{ diz is mapping }} {{ coppia is tuple }}"
      - repeat:
          for_each: "{{ lista + [9] }}"
          sequence:
            - action: prova.registra
              data: {passo: "{{ repeat.item }}"}
""",
    acceso("input_boolean.a"),
    attendi(1),
)


scenario(
    "fermata_dentro_sequenze_annidate",
    """
script:
  prova_lungo:
    mode: restart
    sequence:
      - action: prova.registra
        data: {passo: "inizio {{ n | default(0) }}"}
      - choose:
          - conditions: "{{ true }}"
            sequence:
              - alias: Pausa interna
                delay: 2
              - action: prova.registra
                data: {passo: "dentro {{ n | default(0) }}"}
      - if: "{{ true }}"
        then:
          - repeat:
              count: 2
              sequence:
                - delay: 1
                - action: prova.registra
                  data: {passo: "giro {{ repeat.index }} {{ n | default(0) }}"}
      - action: prova.registra
        data: {passo: "fine {{ n | default(0) }}"}
automation:
  - alias: Prova Avvia Lungo
    mode: parallel
    triggers:
      - {trigger: state, entity_id: input_number.n}
    actions:
      - action: script.turn_on
        target: {entity_id: script.prova_lungo}
        data: {variables: {n: "{{ trigger.to_state.state }}"}}
""",
    numero(1),
    attendi(1),
    numero(2),
    attendi(2.5),
    numero(3),
    attendi(3.2),
    ("servizio", "script.turn_off", {"entity_id": "script.prova_lungo"}),
    attendi(1),
    numero(4),
    attendi(6),
)

scenario(
    "chiamante_di_uno_script_fermato",
    """
script:
  prova_chiamato:
    sequence:
      - action: prova.registra
        data: {passo: chiamato-inizio}
      - sequence:
          - delay: 2
          - action: prova.registra
            data: {passo: chiamato-dentro}
      - action: prova.registra
        data: {passo: chiamato-fine}
  prova_chiamato_pausa:
    sequence:
      - delay: 2
      - action: prova.registra
        data: {passo: mai}
automation:
  - alias: Prova Chiama A
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on"}
    actions:
      - action: script.prova_chiamato
      - action: prova.registra
        data: {passo: dopo-chiamato}
  - alias: Prova Chiama B
    triggers:
      - {trigger: state, entity_id: input_boolean.b, to: "on"}
    actions:
      - action: script.prova_chiamato_pausa
      - action: prova.registra
        data: {passo: dopo-chiamato-pausa}
  - alias: Prova Chiama C
    triggers:
      - {trigger: state, entity_id: input_boolean.c, to: "on"}
    actions:
      - sequence:
          - action: script.prova_chiamato
      - action: prova.registra
        data: {passo: dopo-chiamato-c}
""",
    acceso("input_boolean.a"),
    attendi(1),
    ("servizio", "script.turn_off", {"entity_id": "script.prova_chiamato"}),
    attendi(1),
    acceso("input_boolean.b"),
    attendi(1),
    ("servizio", "script.turn_off", {"entity_id": "script.prova_chiamato_pausa"}),
    attendi(1),
    acceso("input_boolean.c"),
    attendi(1),
    ("servizio", "automation.turn_off", {"entity_id": "automation.prova_chiama_c"}),
    attendi(3),
    ("servizio", "automation.turn_on", {"entity_id": "automation.prova_chiama_c"}),
    spento("input_boolean.c"),
    acceso("input_boolean.c"),
    attendi(1),
    (
        "servizio",
        "automation.turn_off",
        {"entity_id": "automation.prova_chiama_c", "stop_actions": False},
    ),
    attendi(3),
)

scenario(
    "coda_fermata",
    """
script:
  prova_coda:
    mode: queued
    max: 4
    sequence:
      - action: prova.registra
        data: {passo: "inizio {{ n }}"}
      - delay: 1
      - action: prova.registra
        data: {passo: "fine {{ n }}"}
automation:
  - alias: Prova Accoda
    mode: parallel
    triggers:
      - {trigger: state, entity_id: input_number.n}
    actions:
      - action: script.turn_on
        target: {entity_id: script.prova_coda}
        data: {variables: {n: "{{ trigger.to_state.state }}"}}
  - alias: Prova Coda Automazione
    mode: queued
    triggers:
      - {trigger: state, entity_id: input_boolean.a}
    actions:
      - action: prova.registra
        data: {passo: "automazione {{ trigger.to_state.state }}"}
      - delay: 1
      - action: prova.registra
        data: {passo: "automazione fine {{ trigger.to_state.state }}"}
""",
    numero(1),
    numero(2),
    numero(3),
    attendi(0.5),
    ("servizio", "script.turn_off", {"entity_id": "script.prova_coda"}),
    attendi(0.5),
    numero(4),
    numero(5),
    attendi(1.5),
    acceso("input_boolean.a"),
    spento("input_boolean.a"),
    acceso("input_boolean.a"),
    attendi(0.3),
    (
        "servizio",
        "automation.turn_off",
        {"entity_id": "automation.prova_coda_automazione"},
    ),
    attendi(0.5),
    (
        "servizio",
        "automation.turn_on",
        {"entity_id": "automation.prova_coda_automazione"},
    ),
    spento("input_boolean.a"),
    attendi(3),
)

scenario(
    "ripetizioni_casi_limite",
    """
script:
  prova_limiti:
    sequence:
      - repeat:
          until: "{{ states('sensor.nessuno') | float > 1 }}"
          sequence:
            - action: prova.registra
              data: {passo: "until con errore {{ repeat.index }}"}
      - repeat:
          while: "{{ states('sensor.nessuno') | float > 1 }}"
          sequence:
            - action: prova.registra
              data: {passo: mai-while}
      - repeat:
          for_each: "{{ ['p', 'q'] + [states('input_number.n')] }}"
          sequence:
            - repeat:
                for_each: [1, null, 3]
                sequence:
                  - action: prova.registra
                    data: {passo: "item {{ repeat.item | default('nessuno') }} {{ repeat.index }} {{ repeat.last }}"}
            - action: prova.registra
              data: {passo: "esterno {{ repeat.item }} {{ repeat.first }}"}
      - repeat:
          count: "{{ 0 }}"
          sequence:
            - action: prova.registra
              data: {passo: mai-count}
      - repeat:
          for_each: []
          sequence:
            - action: prova.registra
              data: {passo: mai-vuoto}
      - variables:
          visto: "{{ repeat is defined }}"
      - action: prova.registra
        data: {passo: "repeat fuori {{ visto }}"}
      - repeat:
          for_each: "{{ 'non lista' }}"
          sequence:
            - action: prova.registra
              data: {passo: mai-non-lista}
      - action: prova.registra
        data: {passo: mai-dopo-non-lista}
  prova_conta_errata:
    sequence:
      - repeat:
          count: "{{ 'tre' }}"
          sequence:
            - action: prova.registra
              data: {passo: mai-conta}
      - action: prova.registra
        data: {passo: mai-dopo-conta}
automation:
  - alias: Prova Limiti
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on"}
    actions:
      - action: script.prova_limiti
      - action: prova.registra
        data: {passo: dopo-limiti}
      - action: script.prova_conta_errata
      - action: prova.registra
        data: {passo: dopo-conta-errata}
""",
    numero(7),
    acceso("input_boolean.a"),
    attendi(1),
)

scenario(
    "attese_casi_limite",
    """
script:
  prova_attese:
    sequence:
      - action: prova.registra
        data: {passo: "prima {{ wait is defined }}"}
      - wait_template: "{{ is_state('input_boolean.a', 'on') }}"
        timeout: 5
      - action: prova.registra
        data: {passo: "gia vera {{ wait.completed }} {{ wait.remaining }}"}
      - wait_template: "{{ is_state('input_boolean.b', 'on') }}"
        timeout: 0
      - action: prova.registra
        data: {passo: "zero {{ wait.completed }} {{ wait.remaining }}"}
      - wait_template: "{{ is_state('input_boolean.a', 'on') }}"
      - action: prova.registra
        data: {passo: "senza timeout {{ wait.completed }} {{ wait.remaining }}"}
      - if: "{{ true }}"
        then:
          - wait_template: "{{ is_state('input_boolean.b', 'on') }}"
            timeout: 1
          - repeat:
              count: 2
              sequence:
                - wait_template: "{{ is_state('input_boolean.c', 'on') }}"
                  timeout: 0.5
                - action: prova.registra
                  data: {passo: "nel ciclo {{ repeat.index }} {{ wait.completed }}"}
      - action: prova.registra
        data: {passo: "dopo if {{ wait.completed }} {{ wait.remaining }}"}
      - sequence:
          - wait_template: "{{ is_state('input_boolean.b', 'on') }}"
            timeout: 0
            continue_on_timeout: false
          - action: prova.registra
            data: {passo: mai-annidata}
      - action: prova.registra
        data: {passo: mai-dopo-annidata}
  prova_attesa_errata:
    sequence:
      - wait_template: "{{ states('sensor.nessuno') | float > 1 }}"
        timeout: 1
      - action: prova.registra
        data: {passo: mai-attesa-errata}
automation:
  - alias: Prova Attese Limite
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on"}
    actions:
      - action: script.prova_attese
      - action: prova.registra
        data: {passo: "dopo attese {{ wait is defined }}"}
      - action: script.prova_attesa_errata
        continue_on_error: true
      - action: prova.registra
        data: {passo: mai-dopo-errata}
""",
    acceso("input_boolean.a"),
    attendi(3),
)

scenario(
    "variabili_annidate",
    """
script:
  prova_variabili:
    variables:
      base: "{{ x * 2 }}"
      fissa: 3
    fields:
      x: {description: valore}
    sequence:
      - if: "{{ true }}"
        then:
          - variables:
              da_if: "{{ base + 1 }}"
          - choose:
              - conditions: "{{ true }}"
                sequence:
                  - variables:
                      da_choose: "{{ da_if + 1 }}"
                  - action: prova.risposta
                    data: {x: "{{ da_choose }}"}
                    response_variable: risposta_annidata
      - repeat:
          count: 2
          sequence:
            - variables:
                da_ciclo: "{{ repeat.index }}"
                somma: "{{ (somma | default(0)) + repeat.index }}"
      - variables:
          repeat: {index: 99}
      - action: prova.registra
        data:
          passo: >-
            {{ base }} {{ fissa }} {{ da_if }} {{ da_choose }} {{ risposta_annidata.valore }}
            {{ da_ciclo }} {{ somma }} {{ repeat.index }}
      - repeat:
          count: 2
          sequence:
            - variables:
                repeat: {index: 50, first: false}
            - action: prova.registra
              data: {passo: "ciclo {{ repeat.index }} {{ repeat.first }}"}
      - action: prova.registra
        data: {passo: "dopo ciclo {{ repeat.index }}"}
automation:
  - alias: Prova Variabili Annidate
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on"}
    actions:
      - action: script.prova_variabili
        data: {x: 5}
      - action: prova.registra
        data: {passo: "{{ da_if | default('non visibile') }}"}
""",
    acceso("input_boolean.a"),
    attendi(1),
)

scenario(
    "script_parallelo_ultima_azione",
    """
script:
  prova_parallelo:
    mode: parallel
    sequence:
      - sequence:
          - alias: Primo passo
            delay: "{{ d }}"
          - alias: Secondo passo
            delay: 1
          - action: prova.registra
            data: {passo: "fine {{ d }}"}
      - alias: Ultimo passo
        delay: 0.5
automation:
  - alias: Prova Avvia Parallelo
    mode: parallel
    triggers:
      - {trigger: state, entity_id: input_number.n}
    actions:
      - action: script.turn_on
        target: {entity_id: script.prova_parallelo}
        data: {variables: {d: "{{ trigger.to_state.state | int }}"}}
""",
    numero(2),
    attendi(1),
    numero(1),
    attendi(0.5),
    numero(3),
    attendi(6),
)

scenario(
    "errori_e_continua",
    """
script:
  prova_continua:
    sequence:
      - action: prova.registra
        data: {passo: "{{ states('sensor.nessuno') | float }}"}
        continue_on_error: true
      - action: prova.registra
        data: {passo: dopo-dati-errati}
      - action: prova.registra
        target: {entity_id: "{{ 'non valido' }}"}
        continue_on_error: true
      - action: prova.registra
        data: {passo: dopo-bersaglio-errato}
      - action: prova.risposta
        data: {x: 1}
        continue_on_error: true
      - action: prova.registra
        data: {passo: mai-dopo-risposta}
  prova_non_trovato:
    sequence:
      - action: prova.nessuno
        continue_on_error: true
      - action: prova.registra
        data: {passo: mai-dopo-non-trovato}
  prova_eccezione:
    sequence:
      - if: "{{ true }}"
        then:
          - action: prova.registra
            data: {eccezione: true}
      - action: prova.registra
        data: {passo: mai-dopo-eccezione}
  prova_stop_annidato:
    sequence:
      - choose:
          - conditions: "{{ true }}"
            sequence:
              - repeat:
                  count: 2
                  sequence:
                    - stop: errore annidato
                      error: true
      - action: prova.registra
        data: {passo: mai-dopo-stop-annidato}
automation:
  - alias: Prova Continua
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on"}
    actions:
      - action: script.prova_continua
      - action: prova.registra
        data: {passo: dopo-continua}
      - action: script.prova_stop_annidato
      - action: prova.registra
        data: {passo: dopo-stop-annidato}
      - action: script.prova_non_trovato
        continue_on_error: true
      - action: prova.registra
        data: {passo: dopo-non-trovato}
      - action: script.prova_eccezione
        continue_on_error: true
      - action: prova.registra
        data: {passo: dopo-eccezione}
      - action: script.prova_eccezione
      - action: prova.registra
        data: {passo: mai-dopo-eccezione-2}
""",
    acceso("input_boolean.a"),
    attendi(1),
)


scenario(
    "modelli_che_rendono_liste_e_dizionari",
    """
script:
  prova_liste:
    sequence:
      - variables:
          lista: "{{ ['input_boolean.b', 'input_boolean.c'] }}"
          diz: "{{ {'uno': 1, 'due': [2, 3]} }}"
          tupla: "{{ (4, 5) }}"
      - action: prova.registra
        data:
          passo: "{{ lista[1] }} {{ lista | length }} {{ diz.due[0] }} {{ diz['uno'] }} {{ tupla[1] }} {{ 5 in tupla }}"
          testo: "{{ lista }} {{ diz }} {{ tupla }}"
          lista: "{{ lista }}"
          diz: "{{ diz }}"
      - action: input_boolean.turn_on
        target:
          entity_id: "{{ lista }}"
      - repeat:
          for_each: "{{ lista }}"
          sequence:
            - action: prova.registra
              data: {passo: "elemento {{ repeat.item }} {{ repeat.item is string }}"}
      - repeat:
          for_each: "{{ diz.due }}"
          sequence:
            - action: prova.registra
              data: {passo: "numero {{ repeat.item + 1 }}"}
      - action: prova.registra
        data: "{{ {'passo': 'dati da modello ' ~ (lista | join(','))} }}"
automation:
  - alias: Prova Liste
    variables:
      elenco: "{{ [1, 2, 3] }}"
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on"}
    actions:
      - action: prova.registra
        data: {passo: "{{ elenco | sum }} {{ elenco[0] }}"}
      - action: script.prova_liste
""",
    acceso("input_boolean.a"),
    attendi(1),
)

scenario(
    "arresto_di_home_assistant",
    """
script:
  prova_lunga:
    sequence:
      - action: prova.registra
        data: {passo: "inizio {{ chi }}"}
      - delay: 5
      - action: prova.registra
        data: {passo: "fine {{ chi }}"}
automation:
  - alias: Prova Arresto
    mode: queued
    triggers:
      - {trigger: state, entity_id: input_boolean.a}
    actions:
      - action: prova.registra
        data: {passo: "automazione {{ trigger.to_state.state }}"}
      - choose:
          - conditions: "{{ true }}"
            sequence:
              - delay: 2
              - action: prova.registra
                data: {passo: "dopo pausa {{ trigger.to_state.state }}"}
      - action: script.turn_on
        target: {entity_id: script.prova_lunga}
        data: {variables: {chi: "{{ trigger.to_state.state }}"}}
""",
    acceso("input_boolean.a"),
    attendi(3),
    spento("input_boolean.a"),
    attendi(1),
    ("evento", "homeassistant_stop"),
    attendi(1),
    acceso("input_boolean.a"),
    attendi(8),
)


scenario(
    "automazione_restart_dentro_cicli_e_chiamate",
    """
script:
  prova_bloccante:
    mode: queued
    sequence:
      - action: prova.registra
        data: {passo: "bloccante {{ chi }}"}
      - delay: 1.5
      - action: prova.registra
        data: {passo: "bloccante fine {{ chi }}"}
automation:
  - alias: Prova Restart Cicli
    mode: restart
    triggers:
      - {trigger: state, entity_id: input_number.n}
    actions:
      - repeat:
          until: "{{ repeat.index >= 3 or is_state('input_boolean.b', 'on') }}"
          sequence:
            - action: prova.registra
              data: {passo: "giro {{ repeat.index }} {{ trigger.to_state.state }}"}
            - if: "{{ repeat.index == 2 }}"
              then:
                - action: script.prova_bloccante
                  data: {chi: "{{ trigger.to_state.state }}"}
            - delay: 0.7
      - action: prova.registra
        data: {passo: "fine {{ trigger.to_state.state }}"}
""",
    numero(1),
    attendi(0.3),
    numero(2),
    attendi(1.2),
    numero(3),
    attendi(5),
    acceso("input_boolean.b"),
    numero(4),
    attendi(3),
)

scenario(
    "fermata_durante_un_ciclo_stretto",
    """
script:
  prova_stretto:
    mode: restart
    sequence:
      - repeat:
          until: "{{ repeat.index >= 6 }}"
          sequence:
            - action: input_number.increment
              target: {entity_id: input_number.n}
            - action: prova.registra
              data: {passo: "stretto {{ repeat.index }} {{ states('input_number.n') }}"}
      - action: prova.registra
        data: {passo: fine-stretto}
  prova_mentre:
    sequence:
      - repeat:
          while: "{{ repeat.index < 6 }}"
          sequence:
            - action: input_boolean.toggle
              target: {entity_id: input_boolean.c}
            - action: prova.registra
              data: {passo: "mentre {{ repeat.index }}"}
      - action: prova.registra
        data: {passo: fine-mentre}
automation:
  - alias: Prova Avvia Stretto
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on"}
    actions:
      - action: script.turn_on
        target: {entity_id: script.prova_stretto}
  - alias: Prova Ferma Stretto
    mode: parallel
    triggers:
      - {trigger: numeric_state, entity_id: input_number.n, above: 2}
    actions:
      - action: script.turn_off
        target: {entity_id: script.prova_stretto}
  - alias: Prova Riavvia Stretto
    mode: parallel
    triggers:
      - {trigger: numeric_state, entity_id: input_number.n, above: 4}
    actions:
      - action: script.turn_on
        target: {entity_id: script.prova_stretto}
  - alias: Prova Avvia Mentre
    triggers:
      - {trigger: state, entity_id: input_boolean.b, to: "on"}
    actions:
      - action: script.turn_on
        target: {entity_id: script.prova_mentre}
  - alias: Prova Ferma Mentre
    mode: parallel
    triggers:
      - {trigger: state, entity_id: input_boolean.c, to: "on"}
    conditions: "{{ states('input_number.n') | int(0) > 4 }}"
    actions:
      - action: script.turn_off
        target: {entity_id: script.prova_mentre}
""",
    acceso("input_boolean.a"),
    attendi(0.5),
    spento("input_boolean.a"),
    acceso("input_boolean.a"),
    attendi(0.5),
    acceso("input_boolean.b"),
    attendi(1),
)

scenario(
    "attese_fermate",
    """
script:
  prova_attende:
    mode: restart
    sequence:
      - action: prova.registra
        data: {passo: "attende {{ chi }}"}
      - choose:
          - conditions: "{{ true }}"
            sequence:
              - wait_template: "{{ is_state('input_boolean.b', 'on') }}"
                timeout: 3
              - action: prova.registra
                data: {passo: "attesa finita {{ chi }} {{ wait.completed }}"}
      - wait_template: "{{ is_state('input_boolean.c', 'on') }}"
      - action: prova.registra
        data: {passo: "fine {{ chi }}"}
automation:
  - alias: Prova Avvia Attende
    mode: parallel
    triggers:
      - {trigger: state, entity_id: input_number.n}
    actions:
      - action: script.turn_on
        target: {entity_id: script.prova_attende}
        data: {variables: {chi: "{{ trigger.to_state.state }}"}}
""",
    numero(1),
    attendi(1),
    numero(2),
    attendi(1),
    acceso("input_boolean.b"),
    attendi(1),
    ("servizio", "script.turn_off", {"entity_id": "script.prova_attende"}),
    acceso("input_boolean.c"),
    attendi(1),
    spento("input_boolean.c"),
    numero(3),
    attendi(0.5),
    acceso("input_boolean.c"),
    attendi(1),
)

scenario(
    "variabili_di_script_con_errore",
    """
script:
  prova_variabili_errate:
    variables:
      doppio: "{{ x | float * 2 }}"
    fields:
      x: {description: valore}
    sequence:
      - action: prova.registra
        data: {passo: "doppio {{ doppio }}"}
automation:
  - alias: Prova Variabili Errate
    mode: queued
    triggers:
      - {trigger: state, entity_id: input_number.n}
    actions:
      - action: script.prova_variabili_errate
        data: {x: "{{ 'non numero' if trigger.to_state.state == '2.0' else trigger.to_state.state }}"}
        continue_on_error: true
      - action: prova.registra
        data: {passo: "dopo {{ trigger.to_state.state }}"}
      - action: script.prova_variabili_errate
        data: {x: "{{ 'non numero' if trigger.to_state.state == '3.0' else 1 }}"}
      - action: prova.registra
        data: {passo: "dopo senza continua {{ trigger.to_state.state }}"}
""",
    numero(1),
    numero(2),
    numero(3),
    attendi(1),
)


scenario(
    "cicli_oltre_il_massimo_di_giri",
    """
script:
  prova_finche_infinito:
    sequence:
      - repeat:
          until: "{{ false }}"
          sequence:
            - condition: template
              value_template: "{{ repeat.index in [1, 5000, 9999, 10000, 10001] }}"
            - action: prova.registra
              data: {passo: "finche {{ repeat.index }}"}
      - action: prova.registra
        data: {passo: mai-finche}
  prova_mentre_infinito:
    sequence:
      - repeat:
          while: "{{ true }}"
          sequence:
            - condition: template
              value_template: "{{ repeat.index in [1, 5000, 9999, 10000, 10001] }}"
            - action: prova.registra
              data: {passo: "mentre {{ repeat.index }}"}
      - action: prova.registra
        data: {passo: mai-mentre}
automation:
  - alias: Prova Cicli Infiniti
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on"}
    actions:
      - action: script.prova_finche_infinito
      - action: prova.registra
        data: {passo: dopo-finche}
      - action: script.prova_mentre_infinito
      - action: prova.registra
        data: {passo: dopo-mentre}
""",
    acceso("input_boolean.a"),
    attendi(1),
)


scenario(
    "errori_nella_preparazione_della_chiamata",
    """
script:
  prova_bersaglio_errato:
    sequence:
      - action: prova.registra
        target: "{{ 'non un dizionario' }}"
        continue_on_error: true
      - action: prova.registra
        data: {passo: mai-dopo-bersaglio}
  prova_dati_non_dizionario:
    sequence:
      - action: prova.registra
        data: "{{ [1, 2] }}"
        continue_on_error: true
      - action: prova.registra
        data: {passo: dopo-dati-non-dizionario}
      - action: "{{ 'prova.non valido' }}"
        continue_on_error: true
      - action: prova.registra
        data: {passo: dopo-servizio-non-valido}
      - action: prova.registra
        target: {entity_id: "{{ 'input_boolean.a' if true else '' }}"}
        data: {passo: bersaglio-valido}
      - action: prova.registra
        target: {entity_id: "{{ 'non valido' }}"}
        continue_on_error: true
      - action: prova.registra
        data: {passo: dopo-entita-non-valide}
automation:
  - alias: Prova Preparazione
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on"}
    actions:
      - action: script.prova_bersaglio_errato
        continue_on_error: true
      - action: prova.registra
        data: {passo: dopo-bersaglio-errato}
      - action: script.prova_dati_non_dizionario
      - action: prova.registra
        data: {passo: dopo-dati}
""",
    acceso("input_boolean.a"),
    attendi(1),
)


scenario(
    "restart_e_coda_di_script_chiamati",
    """
script:
  prova_riavviabile:
    mode: restart
    sequence:
      - action: prova.registra
        data: {passo: "riavviabile {{ chi }}"}
      - if: "{{ annidata }}"
        then:
          - delay: 2
        else:
          - delay: 2
      - delay: 1
      - action: prova.registra
        data: {passo: "riavviabile fine {{ chi }}"}
  prova_in_coda:
    mode: queued
    sequence:
      - action: prova.registra
        data: {passo: "in coda {{ chi }}"}
      - sequence:
          - delay: 1
      - action: prova.registra
        data: {passo: "in coda fine {{ chi }}"}
automation:
  - alias: Prova Chiama Riavviabile
    mode: parallel
    triggers:
      - {trigger: state, entity_id: input_number.n}
    actions:
      - action: script.prova_riavviabile
        data:
          chi: "{{ trigger.to_state.state }}"
          annidata: "{{ trigger.to_state.state | int < 3 }}"
      - action: prova.registra
        data: {passo: "dopo riavviabile {{ trigger.to_state.state }}"}
  - alias: Prova Chiama In Coda
    mode: parallel
    triggers:
      - {trigger: state, entity_id: input_boolean.a}
    actions:
      - action: script.prova_in_coda
        data: {chi: "{{ trigger.to_state.state }}"}
      - action: prova.registra
        data: {passo: "dopo in coda {{ trigger.to_state.state }}"}
""",
    numero(1),
    attendi(0.5),
    numero(2),
    attendi(2.5),
    numero(3),
    attendi(0.5),
    numero(4),
    attendi(4),
    acceso("input_boolean.a"),
    spento("input_boolean.a"),
    acceso("input_boolean.a"),
    attendi(0.5),
    ("servizio", "script.turn_off", {"entity_id": "script.prova_in_coda"}),
    attendi(2),
)


scenario(
    "liste_e_dizionari_resi",
    # come l'automazione Countdown Attese del package: variabili, dati, bersagli e
    # for_each resi come liste, dizionari, tuple e insiemi (ResultWrapper di Home Assistant)
    """
automation:
  - alias: Prova Liste
    id: prova_liste
    mode: queued
    variables:
      letture: "{{ {'a': ['input_boolean.a', 10], 'b': ['input_boolean.b', 5]} }}"
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on", id: "ON|a|10|testo lungo"}
      - {trigger: state, entity_id: input_boolean.b, to: "on", id: "OFF|b|5|altro"}
    actions:
      - variables:
          parti: "{{ trigger.id.split('|') }}"
          chiavi: "{{ letture.keys() | list }}"
          coppia: "{{ (1, 'x') }}"
          insieme: "{{ '{1, 2}' }}"
      - action: prova.registra
        data:
          passo: >-
            {{ parti[1] }} {{ parti | length }} {{ letture.a[1] }} {{ chiavi }}
            {{ coppia[1] }} {{ insieme | list }} {{ parti[3][:5] }}
          lista: "{{ parti }}"
          diz: "{{ letture }}"
      - repeat:
          for_each: "{{ chiavi }}"
          sequence:
            - action: prova.registra
              data: {passo: "giro {{ repeat.item }} {{ letture[repeat.item][0] }}"}
      - action: input_boolean.turn_on
        target:
          entity_id: "{{ ['input_boolean.c'] }}"
      - action: prova.registra
        data: "{{ {'passo': 'dati ' ~ parti[0]} }}"
""",
    acceso("input_boolean.a"),
    attendi(0.5),
    acceso("input_boolean.b"),
    attendi(0.5),
)


scenario(
    "nomi_dei_passi",
    # last_action dopo ogni tipo di passo (alias o descrizione di Home Assistant), anche
    # dentro choose, if, repeat e sequence; variables e fields dello script, metadata,
    # enabled, condizioni abbreviate, azione con modello, entity_id dell'azione
    """
script:
  prova_lenta:
    mode: parallel
    sequence:
      - delay: 0.3
  prova_passi:
    alias: Prova Passi
    mode: queued
    variables:
      base: "{{ 10 }}"
      doppio: "{{ base * 2 }}"
      x: "{{ 'dalle variabili' }}"
    fields:
      x:
        description: valore
        default: 5
        required: false
        selector: {number: {min: 0, max: 10}}
    sequence:
      - alias: Variabili con nome
        variables: {a: "{{ base + 1 }}"}
      - alias: Chiamata lenta
        action: script.prova_lenta
      - variables: {b: 2}
      - action: script.prova_lenta
        metadata: {}
        enabled: true
      - alias: Pausa con nome
        delay: 0.3
      - delay: {seconds: "{{ 0.3 }}"}
      - alias: Attesa con nome
        wait_template: "{{ is_state('input_boolean.c', 'on') }}"
        timeout: "{{ 0.3 }}"
      - wait_template: "{{ is_state('input_boolean.c', 'on') }}"
        timeout: 0.3
      - alias: Condizione con nome
        condition: template
        value_template: "{{ true }}"
      - action: script.prova_lenta
      - condition: template
        value_template: "{{ true }}"
        enabled: true
      - action: script.prova_lenta
      - condition: state
        entity_id: input_boolean.a
        state: "off"
      - action: script.prova_lenta
      - alias: Scelta
        choose:
          - alias: Opzione
            conditions: "{{ false }}"
            sequence:
              - action: prova.registra
                data: {passo: mai}
          - conditions:
              - "{{ true }}"
              - condition: trigger
                id: nessuno
            sequence:
              - action: prova.registra
                data: {passo: mai2}
        default:
          - alias: Pausa annidata
            delay: 0.3
          - alias: Chiamata annidata
            action: script.prova_lenta
      - action: script.prova_lenta
      - alias: Se
        if: "{{ x is defined }}"
        then:
          - delay: 0.2
          - alias: Condizione annidata
            condition: template
            value_template: "{{ false }}"
          - action: prova.registra
            data: {passo: mai3}
        else:
          - alias: Pausa altrimenti
            delay: 0.2
      - action: script.prova_lenta
      - alias: Ripeti
        repeat:
          while: "{{ repeat.index <= 2 }}"
          sequence:
            - alias: Pausa nel ciclo
              delay: 0.2
      - alias: Sequenza
        sequence:
          - variables: {c: 3}
          - alias: Chiamata in sequenza
            action: script.prova_lenta
      - action: script.prova_lenta
      - action: "{{ 'prova.' ~ 'registra' }}"
        data:
          passo: "{{ a }} {{ b }} {{ c }} {{ base }} {{ doppio }} {{ x }}"
      - action: input_boolean.turn_on
        entity_id: input_boolean.c
      - alias: Errore ignorato
        action: prova.registra
        data: {errore: true}
        continue_on_error: true
      - action: script.prova_lenta
      - alias: Stop con nome
        stop: fine
      - action: prova.registra
        data: {passo: mai4}
""",
    ("servizio", "script.turn_on", {"entity_id": "script.prova_passi"}),
    *sonda("script.prova_passi", 7),
    spento("input_boolean.c"),
    (
        "servizio",
        "script.turn_on",
        {"entity_id": "script.prova_passi", "variables": {"x": 1}},
    ),
    *sonda("script.prova_passi", 8),
)


scenario(
    "configurazioni_dei_trigger",
    # i trigger come nel package: «for» con modelli (template e state), from/not_from/
    # not_to in lista, event su call_service con event_data, time e time_pattern, alias,
    # id ed enabled; l'orologio di prova è alle 02:00 di US/Pacific
    """
automation:
  - alias: Prova Trigger
    id: prova_trigger
    mode: queued
    max: 10
    triggers:
      - trigger: template
        alias: Numero alto
        value_template: "{{ states('input_number.n') | int(0) > 20 }}"
        for: {seconds: "{{ states('input_number.n') | int(0) // 10 }}"}
        id: alto
        enabled: true
      - trigger: state
        alias: A acceso a lungo
        entity_id: [input_boolean.a]
        from: ["off"]
        not_to: [unavailable, unknown]
        for: {seconds: "{{ 1 + 1 }}"}
        id: a
      - trigger: state
        entity_id: [input_boolean.b]
        not_from: [unavailable, unknown]
        to: "on"
        for: "00:00:01"
        id: b
      - trigger: event
        alias: Spegnimento chiesto
        event_type: [call_service]
        event_data: {domain: input_boolean, service: turn_off}
        id: evento
      - trigger: time_pattern
        seconds: "/7"
        id: ritmo
      - trigger: time
        at: ["02:00:12"]
        id: ora
      - trigger: homeassistant
        event: start
        id: avvio
      - trigger: state
        entity_id: [input_boolean.c]
        enabled: false
        id: spento
    actions:
      - action: prova.registra
        data:
          passo: >-
            {{ trigger.id }}|{{ trigger.idx }}|{{ trigger.alias }}|{{ trigger.platform }}|
            {{ trigger.for }}|{{ trigger.event.data.service if trigger.event is defined }}
""",
    numero(30),
    attendi(4),
    acceso("input_boolean.a"),
    attendi(3),
    spento("input_boolean.a"),
    acceso("input_boolean.b"),
    acceso("input_boolean.c"),
    attendi(2),
    numero(10),
    attendi(6),
)


def _norma(valore: Any) -> Any:
    """Un valore del registro senza ciò che cambia da una corsa all'altra."""
    if isinstance(valore, datetime):
        return round((valore - T0).total_seconds(), 3)
    if isinstance(valore, Context):
        return None
    if isinstance(valore, State):
        return (valore.entity_id, valore.state, _norma(dict(valore.attributes)))
    if isinstance(valore, dict):
        return {k: _norma(v) for k, v in sorted(valore.items()) if k != "run_id"}
    if isinstance(valore, (list, tuple)):
        return [_norma(v) for v in valore]
    return valore


async def _gira(hass: HomeAssistant) -> None:
    """Il ciclo degli eventi lavora finché ha qualcosa di pronto (senza aspettare): come
    asyncio, un timer è dovuto se scade prima di ``time() + clock_resolution``."""
    loop = hass.loop
    for _ in range(100_000):
        await asyncio.sleep(0)
        fine = loop.time() + loop._clock_resolution
        if not loop._ready and not any(
            not h.cancelled() and h.when() < fine for h in loop._scheduled
        ):
            return
    raise AssertionError(f"il ciclo degli eventi non si ferma: {list(loop._ready)[:5]}")


async def _avanza(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory, secondi: float
) -> None:
    for _ in range(round(secondi / PASSO)):
        freezer.tick(timedelta(seconds=PASSO))
        await _gira(hass)


def _carica(nome: str, testo: str) -> types.ModuleType:
    """Un modulo generato per la prova, dentro il pacchetto ``generato``."""
    pieno = f"{generato.__name__}.{nome}"
    modulo = types.ModuleType(pieno)
    modulo.__package__ = generato.__name__
    sys.modules[pieno] = modulo
    exec(compile(testo, pieno, "exec"), modulo.__dict__)  # noqa: S102
    return modulo


@pytest.fixture
def moduli() -> Iterator[list[str]]:
    nomi: list[str] = []
    yield nomi
    for nome in nomi:
        sys.modules.pop(nome, None)


async def _corsa(
    freezer: FrozenDateTimeFactory,
    nome: str,
    configurazione: dict[str, Any],
    passi: list[tuple[Any, ...]],
    *,
    motore: bool,
    moduli: list[str],
) -> list[Any]:
    freezer.move_to(T0)
    registro: list[Any] = []
    async with async_test_home_assistant() as hass:
        assert await async_setup_component(hass, "homeassistant", {})
        for dominio, voci in AIUTANTI.items():
            assert await async_setup_component(hass, dominio, {dominio: voci})

        async def registra(chiamata: ServiceCall) -> None:
            if chiamata.data.get("errore"):
                raise HomeAssistantError("errore voluto")
            if chiamata.data.get("eccezione"):
                raise ValueError("eccezione voluta")

        async def risposta(chiamata: ServiceCall) -> ServiceResponse:
            return {"valore": chiamata.data.get("x")}

        hass.services.async_register("prova", "registra", registra)
        hass.services.async_register(
            "prova", "risposta", risposta, supports_response=SupportsResponse.ONLY
        )
        automazioni = configurazione.get("automation", [])
        script = configurazione.get("script", {})
        if motore:
            testo_modelli, testo_motore = await traduci_configurazione(
                hass, automazioni, script, nome_modelli=f"prova_{nome}_modelli"
            )
            moduli.append(f"{generato.__name__}.prova_{nome}_modelli")
            moduli.append(f"{generato.__name__}.prova_{nome}_motore")
            _carica(f"prova_{nome}_modelli", testo_modelli)
            codice = _carica(f"prova_{nome}_motore", testo_motore)
            m = Motore(hass)
            await m.avvia(crea=codice.crea)
        else:
            assert await async_setup_component(hass, "script", {"script": script})
            assert await async_setup_component(
                hass, "automation", {"automation": automazioni}
            )
        await _gira(hass)

        @callback
        def annota(evento: Event) -> None:
            if evento.event_type not in EVENTI:
                return
            dati = evento.data
            if evento.event_type == EVENT_STATE_CHANGED:
                dati = {"entity_id": dati["entity_id"], "new_state": dati["new_state"]}
            registro.append(
                (_norma(evento.time_fired), evento.event_type, _norma(dict(dati)))
            )

        togli = hass.bus.async_listen(MATCH_ALL, annota)
        for passo in passi:
            if passo[0] == "servizio":
                dominio, servizio = passo[1].split(".")
                await hass.services.async_call(
                    dominio, servizio, passo[2], blocking=True
                )
                await _gira(hass)
            elif passo[0] == "evento":
                hass.bus.async_fire(passo[1])
                await _gira(hass)
            else:
                await _avanza(hass, freezer, passo[1])
        togli()
        await hass.services.async_call(
            "automation", "turn_off", {"entity_id": "all"}, blocking=True
        )
        await hass.services.async_call(
            "script", "turn_off", {"entity_id": "all"}, blocking=True
        )
        await _gira(hass)
        await hass.async_stop(force=True)
    return registro


@pytest.mark.parametrize("nome", sorted(SCENARI))
async def test_come_home_assistant(
    nome: str,
    freezer: FrozenDateTimeFactory,
    moduli: list[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Stesso registro degli eventi con Home Assistant e con il motore tradotto."""
    # Home Assistant sposta i trigger time_pattern di una frazione di secondo a caso: in
    # entrambe le corse la stessa
    monkeypatch.setattr(
        "homeassistant.helpers.event.randint", lambda minimo, massimo: minimo
    )
    testo, passi = SCENARI[nome]
    configurazione = yaml.safe_load(testo)
    atteso = await _corsa(
        freezer, nome, configurazione, passi, motore=False, moduli=moduli
    )
    ottenuto = await _corsa(
        freezer, nome, configurazione, passi, motore=True, moduli=moduli
    )
    assert any(
        voce[1] == EVENT_CALL_SERVICE and voce[2]["domain"] == "prova"
        for voce in atteso
    )
    if ottenuto != atteso:
        righe_attese = [repr(v) for v in atteso]
        righe_ottenute = [repr(v) for v in ottenuto]
        diff = "\n".join(
            difflib.unified_diff(
                righe_attese,
                righe_ottenute,
                "home_assistant",
                "motore",
                lineterm="",
                n=2,
            )
        )
        pytest.fail(f"registri diversi:\n{diff}")
