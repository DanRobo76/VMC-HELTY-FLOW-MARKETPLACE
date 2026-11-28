"""Il runtime del motore riga per riga: ogni ramo raggiunto a confronto con Home Assistant.

Le prove di ``test_semantica.py``, ``test_traduttore_casi.py`` e ``test_avvio_motore.py``
non passano da alcuni rami del runtime (``esecuzione.py``, ``condizioni.py``,
``contesto.py``, ``jinja.py``, ``ha.py``). Qui ogni ramo che rifà un comportamento di Home
Assistant si raggiunge con una prova a confronto: lo stesso YAML gira con Home Assistant e,
tradotto, con il motore (``_corsa`` di ``test_semantica``), oppure lo stesso modello si
rende con Home Assistant e tradotto (il banco di ``test_traduttore_casi``).

Alcuni rami si raggiungono solo con servizi di prova che fanno, dentro un'esecuzione, ciò
che il banco da solo non fa:

- ``prova.salta``: l'orologio va avanti di colpo (un ciclo stretto è in corso quando
  scade il timer di Home Assistant dei 60 secondi dopo la chiusura);
- ``prova.rimuovi``: un'entità esce dal registro delle entità (Home Assistant la toglie
  mentre gira).
"""

from __future__ import annotations

import difflib
import re
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import timedelta
from pathlib import Path
from typing import Any

import pytest
import yaml
from freezegun.api import FrozenDateTimeFactory
from homeassistant.const import EVENT_CALL_SERVICE, EVENT_STATE_CHANGED, MATCH_ALL
from homeassistant.core import Event, HomeAssistant, ServiceCall, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.template import Template
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import async_test_home_assistant

from custom_components.vmc_master.nativa.motore.stati_logiche import stati_logiche
from custom_components.vmc_master.trasforma import rinomina

from . import generato
from . import test_semantica as semantica
from .fase3 import MotoreFase3
from .test_semantica import (
    AIUTANTI,
    T0,
    _avanza,
    _carica,
    _corsa,
    _gira,
    _norma,
    acceso,
    attendi,
    moduli,  # noqa: F401
    numero,
    spento,
)
from .test_traduttore_casi import Banco, _esito, banco  # noqa: F401
from .traduci import traduci_configurazione

SCENARI: dict[str, tuple[str, list[tuple[Any, ...]]]] = {}
# Scenari con la chiusura di Home Assistant: 60 secondi dopo, Home Assistant ferma gli
# script ancora in corso e non ne avvia di nuovi (il plugin dei test lo toglie, qui no).
SCENARI_CHIUSURA: dict[str, tuple[str, list[tuple[Any, ...]]]] = {}


def scenario(
    nome: str, configurazione: str, *passi: Any, dopo_la_chiusura: bool = False
) -> None:
    """Come ``scenario`` di test_semantica; un passo può essere una lista di passi."""
    piatti: list[tuple[Any, ...]] = []
    for passo in passi:
        piatti.extend(passo if isinstance(passo, list) else [passo])
    (SCENARI_CHIUSURA if dopo_la_chiusura else SCENARI)[nome] = (configurazione, piatti)


def tutti_accesi(*entita: str) -> tuple[Any, ...]:
    """Più input_boolean accesi con una sola chiamata: Home Assistant li accende uno
    dopo l'altro in task separati (``asyncio.gather``), prima che riprenda chi aspetta."""
    return ("servizio", "input_boolean.turn_on", {"entity_id": list(entita)})


# --- condizioni.py ----------------------------------------------------------------------

scenario(
    "condizioni_composte_e_di_stato_con_errori",
    """
automation:
  - alias: Prova Condizioni Errate
    id: prova_condizioni_errate
    mode: queued
    triggers:
      - {trigger: state, entity_id: input_number.n}
    actions:
      - variables:
          v: "{{ trigger.to_state.state | int }}"
      # and: un errore e una falsa -> falso; un errore e una vera -> errore
      - if:
          - condition: not
            conditions:
              - condition: and
                conditions:
                  - {condition: state, entity_id: sensor.inesistente, state: "on"}
                  - "{{ v == 1 }}"
        then:
          - action: prova.registra
            data: {passo: "and falso {{ v }}"}
        else:
          - action: prova.registra
            data: {passo: "and in errore {{ v }}"}
      # or: un errore e una vera -> vero; un errore e una falsa -> errore
      - if:
          - condition: or
            conditions:
              - {condition: state, entity_id: sensor.inesistente, state: "on"}
              - "{{ v == 1 }}"
        then:
          - action: prova.registra
            data: {passo: "or vero {{ v }}"}
        else:
          - action: prova.registra
            data: {passo: "or non vero {{ v }}"}
      - if:
          - condition: not
            conditions:
              - condition: or
                conditions:
                  - {condition: state, entity_id: sensor.inesistente, state: "on"}
                  - "{{ v == 1 }}"
        then:
          - action: prova.registra
            data: {passo: "or falso {{ v }}"}
        else:
          - action: prova.registra
            data: {passo: "or vero o in errore {{ v }}"}
      # not: una vera -> falso; un errore e nessuna vera -> errore; tutte false -> vero
      - if:
          - condition: not
            conditions:
              - "{{ v == 1 }}"
              - {condition: state, entity_id: sensor.inesistente, state: "on"}
        then:
          - action: prova.registra
            data: {passo: "not vero {{ v }}"}
        else:
          - action: prova.registra
            data: {passo: "not non vero {{ v }}"}
      - if:
          - condition: not
            conditions:
              - condition: not
                conditions:
                  - "{{ v == 1 }}"
                  - {condition: state, entity_id: sensor.inesistente, state: "on"}
        then:
          - action: prova.registra
            data: {passo: "not falso {{ v }}"}
        else:
          - action: prova.registra
            data: {passo: "not vero o in errore {{ v }}"}
      - if:
          - condition: not
            conditions:
              - "{{ v == 3 }}"
              - "{{ false }}"
        then:
          - action: prova.registra
            data: {passo: "not di tutte false {{ v }}"}
      # state: attributo che non c'è -> falso; stato che è un'entità che non c'è -> errore
      - if:
          - condition: not
            conditions:
              - condition: state
                entity_id: input_boolean.a
                attribute: inesistente
                state: "x"
        then:
          - action: prova.registra
            data: {passo: "attributo mancante {{ v }}"}
      - if:
          - condition: not
            conditions:
              - condition: state
                entity_id: input_boolean.a
                state: input_boolean.inesistente
        then:
          - action: prova.registra
            data: {passo: "stato di un'entità mancante: falso {{ v }}"}
        else:
          - action: prova.registra
            data: {passo: "stato di un'entità mancante: errore {{ v }}"}
      - if:
          - condition: state
            entity_id: input_boolean.a
            state: input_boolean.b
        then:
          - action: prova.registra
            data: {passo: "stato come un'altra entità {{ v }}"}
      # state con for: durata, errore del modello, durata non valida
      - if:
          - {condition: state, entity_id: input_boolean.a, state: "off", for: {seconds: 1}}
        then:
          - action: prova.registra
            data: {passo: "spento da un secondo {{ v }}"}
        else:
          - action: prova.registra
            data: {passo: "spento da meno di un secondo {{ v }}"}
      - if:
          - {condition: state, entity_id: input_boolean.a, state: "off", for: "{{ v * 10 }}"}
        then:
          - action: prova.registra
            data: {passo: "spento da {{ v * 10 }} secondi"}
      - if:
          - condition: not
            conditions:
              - {condition: state, entity_id: input_boolean.a, state: "off", for: "{{ 1 / 0 }}"}
        then:
          - action: prova.registra
            data: {passo: "for con errore: falso {{ v }}"}
        else:
          - action: prova.registra
            data: {passo: "for con errore: errore {{ v }}"}
      - if:
          - condition: not
            conditions:
              - {condition: state, entity_id: input_boolean.a, state: "off", for: "{{ -5 }}"}
        then:
          - action: prova.registra
            data: {passo: "for non valido: falso {{ v }}"}
        else:
          - action: prova.registra
            data: {passo: "for non valido: errore {{ v }}"}
      # azione «condition» in errore: ferma solo la sequenza annidata
      - sequence:
          - action: prova.registra
            data: {passo: "prima della condizione {{ v }}"}
          - condition: state
            entity_id: sensor.inesistente
            state: "on"
          - action: prova.registra
            data: {passo: "dopo la condizione {{ v }}"}
      - action: prova.registra
        data: {passo: "fine {{ v }}"}
""",
    attendi(2),
    numero(1),
    attendi(14),
    numero(2),
    attendi(1),
)


# --- servizi: errori, bersagli, risposte -----------------------------------------------

scenario(
    "chiamate_con_errori_e_bersagli",
    """
automation:
  - alias: Prova Chiamate
    id: prova_chiamate
    mode: parallel
    triggers:
      - {trigger: state, entity_id: input_number.n}
    actions:
      - variables:
          caso: "{{ trigger.to_state.state | int }}"
      - action: prova.registra
        data: {passo: "prima {{ caso }}"}
      - choose:
          - conditions: "{{ caso == 1 }}"
            sequence:
              - action: prova.inesistente
          - conditions: "{{ caso == 2 }}"
            sequence:
              - action: prova.inesistente
                continue_on_error: true
          - conditions: "{{ caso == 3 }}"
            sequence:
              - action: prova.registra
                data: {passo: con-risposta}
                response_variable: risposta
          - conditions: "{{ caso == 4 }}"
            sequence:
              - action: prova.registra
                data: {eccezione: true}
          - conditions: "{{ caso == 5 }}"
            sequence:
              - action: "prova.{{ 1 / 0 }}"
          - conditions: "{{ caso == 6 }}"
            sequence:
              - action: "prova.{{ 1 / 0 }}"
                continue_on_error: true
          - conditions: "{{ caso == 7 }}"
            sequence:
              - action: prova.registra
                target: {entity_id: "{{ 1 / 0 }}"}
                continue_on_error: true
          - conditions: "{{ caso == 8 }}"
            sequence:
              - action: input_boolean.turn_on
                target: {area_id: nessuna}
          - conditions: "{{ caso == 9 }}"
            sequence:
              - action: input_boolean.turn_on
                target:
                  entity_id: [input_boolean.b, input_boolean.c]
                  exclude: {entity_id: input_boolean.c}
          - conditions: "{{ caso == 10 }}"
            sequence:
              - action: input_boolean.turn_on
                target:
                  entity_id: [input_boolean.a, input_boolean.c]
                  exclude: {entity_id: "{{ 'non valido' }}"}
                continue_on_error: true
          - conditions: "{{ caso == 11 }}"
            sequence:
              - action: input_boolean.turn_off
                target: {entity_id: all}
          - conditions: "{{ caso == 12 }}"
            sequence:
              - action: input_boolean.turn_on
                target: {entity_id: none}
          - conditions: "{{ caso == 13 }}"
            sequence:
              - repeat:
                  for_each: "{{ 1 / 0 }}"
                  sequence:
                    - action: prova.registra
                      data: {passo: "mai {{ repeat.item }}"}
          - conditions: "{{ caso == 14 }}"
            sequence:
              - action: input_boolean.turn_on
                target: "{{ {'entity_id': 'input_boolean.a', 'exclude': {'entity_id': ['input_boolean.a']}} }}"
      - action: prova.registra
        data: {passo: "dopo {{ caso }}"}
""",
    [passo for caso in range(1, 15) for passo in (numero(caso), attendi(0.5))],
)


# --- esecuzione.py: ricorsioni, restart, cicli fermati, attese --------------------------

scenario(
    "ricorsioni_vietate",
    """
script:
  prova_ricorsiva:
    mode: queued
    sequence:
      - action: prova.registra
        data: {passo: "ricorsiva {{ giro | default(0) }}"}
      - if: "{{ giro is not defined }}"
        then:
          - action: script.prova_ricorsiva
            data: {giro: 1}
      - action: prova.registra
        data: {passo: "ricorsiva fine {{ giro | default(0) }}"}
  prova_riparte:
    mode: restart
    sequence:
      - action: prova.registra
        data: {passo: "riparte {{ giro | default(0) }}"}
      - repeat:
          count: 1
          sequence:
            - action: script.prova_riparte
              data: {giro: 1}
      - action: prova.registra
        data: {passo: "riparte fine {{ giro | default(0) }}"}
  prova_parallela:
    mode: parallel
    sequence:
      - action: prova.registra
        data: {passo: "parallela {{ giro | default(0) }}"}
      - if: "{{ giro is not defined }}"
        then:
          - action: script.prova_parallela
            data: {giro: 1}
      - action: prova.registra
        data: {passo: "parallela fine {{ giro | default(0) }}"}
""",
    ("servizio", "script.prova_ricorsiva", {}),
    attendi(0.5),
    ("servizio", "script.prova_riparte", {}),
    attendi(0.5),
    ("servizio", "script.prova_parallela", {}),
    attendi(0.5),
)

scenario(
    "restart_accavallati",
    """
script:
  prova_riavvio:
    mode: restart
    sequence:
      - action: prova.registra
        data: {passo: "riavvio {{ chi }}"}
      - delay: 3
      - action: prova.registra
        data: {passo: "riavvio fine {{ chi }}"}
automation:
  - alias: Prova Riavvii
    mode: parallel
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on", id: a}
      - {trigger: state, entity_id: input_boolean.b, to: "on", id: b}
      - {trigger: state, entity_id: input_boolean.c, to: "on", id: c}
    actions:
      - action: script.prova_riavvio
        data: {chi: "{{ trigger.id }}"}
      - action: prova.registra
        data: {passo: "chiamata {{ trigger.id }}"}
""",
    acceso("input_boolean.a"),
    attendi(1),
    tutti_accesi("input_boolean.b", "input_boolean.c"),
    attendi(4),
)

scenario(
    "cicli_fermati_da_uno_script_avviato",
    # i cicli sono in due script (le automazioni del motore non hanno automation.turn_off):
    # lo script avviato da un ciclo lo ferma con script.turn_off
    """
script:
  prova_ferma_cicli:
    mode: parallel
    sequence:
      - action: script.turn_off
        target: {entity_id: "{{ quale }}"}
      - action: prova.registra
        data: {passo: "fermata {{ quale }}"}
  prova_conta_fermata:
    alias: Prova Conta Fermata
    sequence:
      - repeat:
          count: 3
          sequence:
            - action: prova.registra
              data: {passo: "conta {{ repeat.index }}"}
            # lo script avviato ferma il ciclo e aspetta: chi l'ha avviato no
            - if: "{{ repeat.index == 2 }}"
              then:
                - action: script.turn_on
                  target: {entity_id: script.prova_ferma_cicli}
                  data: {variables: {quale: script.prova_conta_fermata}}
      - action: prova.registra
        data: {passo: conta-fine}
  prova_ogni_fermata:
    alias: Prova Ogni Fermata
    sequence:
      - repeat:
          for_each: [x, y, z]
          sequence:
            - action: prova.registra
              data: {passo: "ogni {{ repeat.item }}"}
            - if: "{{ repeat.item == 'y' }}"
              then:
                - action: script.turn_on
                  target: {entity_id: script.prova_ferma_cicli}
                  data: {variables: {quale: script.prova_ogni_fermata}}
      - action: prova.registra
        data: {passo: ogni-fine}
automation:
  - alias: Prova Conta
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on"}
    actions:
      - action: script.turn_on
        target: {entity_id: script.prova_conta_fermata}
  - alias: Prova Ogni
    triggers:
      - {trigger: state, entity_id: input_boolean.b, to: "on"}
    actions:
      - action: script.turn_on
        target: {entity_id: script.prova_ogni_fermata}
""",
    acceso("input_boolean.a"),
    attendi(0.5),
    acceso("input_boolean.b"),
    attendi(0.5),
)

scenario(
    "attesa_vera_due_volte_prima_di_riprendere",
    """
automation:
  - alias: Prova Attesa Doppia
    triggers:
      - {trigger: state, entity_id: input_number.n}
    actions:
      - wait_template: >-
          {{ [is_state('input_boolean.a', 'on'), is_state('input_boolean.b', 'on'),
          is_state('input_boolean.c', 'on')] | select | list | count in [1, 3] }}
        timeout: 10
      - action: prova.registra
        data: {passo: "attesa {{ wait.completed }} {{ wait.remaining }}"}
""",
    numero(1),
    attendi(1),
    tutti_accesi("input_boolean.a", "input_boolean.b", "input_boolean.c"),
    attendi(1),
)

scenario(
    "ciclo_stretto_dopo_la_chiusura",
    """
automation:
  - alias: Prova Ciclo Dopo Chiusura
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on"}
    actions:
      - repeat:
          until: "{{ repeat.index >= 5 }}"
          sequence:
            - action: prova.registra
              data: {passo: "giro {{ repeat.index }}"}
            - if: "{{ repeat.index == 1 }}"
              then:
                - action: prova.salta
                  data: {secondi: 61}
      - action: prova.registra
        data: {passo: fine-ciclo}
""",
    ("evento", "homeassistant_stop"),
    acceso("input_boolean.a"),
    attendi(1),
    dopo_la_chiusura=True,
)


# --- ha.py: variabili, rimozione delle entità -------------------------------------------

scenario(
    "variabili_di_automazione_con_liste",
    """
automation:
  - alias: Prova Variabili Liste
    variables:
      lista: ["{{ 1 + 1 }}", testo, ["{{ 'annidata' }}", 3]]
    triggers:
      - {trigger: state, entity_id: input_boolean.a}
    actions:
      - action: prova.registra
        data: {passo: "{{ lista }} {{ lista[2][0] }} {{ lista[0] + 1 }}"}
""",
    acceso("input_boolean.a"),
)

scenario(
    "entita_rimosse_mentre_girano",
    """
script:
  prova_rimossa:
    sequence:
      - action: prova.registra
        data: {passo: script-inizio}
      - delay: 5
      - action: prova.registra
        data: {passo: script-fine}
automation:
  - alias: Prova Rimossa
    id: prova_rimossa
    mode: parallel
    triggers:
      - {trigger: state, entity_id: input_boolean.a}
    actions:
      - action: prova.registra
        data: {passo: "rimossa {{ trigger.platform }}"}
      - delay: 5
      - action: prova.registra
        data: {passo: rimossa-fine}
  - alias: Prova Restante
    id: prova_restante
    triggers:
      - {trigger: state, entity_id: input_boolean.b}
    actions:
      - action: prova.registra
        data: {passo: "restante {{ trigger.platform }}"}
""",
    acceso("input_boolean.a"),
    ("servizio", "script.turn_on", {"entity_id": "script.prova_rimossa"}),
    attendi(1),
    ("servizio", "prova.rimuovi", {"entity_id": "script.prova_rimossa"}),
    # (le automazioni del motore sono logiche: niente voce del registro da togliere,
    # niente automation.trigger)
    attendi(2),
    spento("input_boolean.a"),
    acceso("input_boolean.b"),
    attendi(6),
)


# --- il banco -------------------------------------------------------------------------


def _servizi_di_prova(hass: HomeAssistant, freezer: FrozenDateTimeFactory) -> None:
    """``prova.salta`` e ``prova.rimuovi`` (vedi la descrizione del modulo)."""

    async def salta(chiamata: ServiceCall) -> None:
        freezer.tick(timedelta(seconds=chiamata.data["secondi"]))

    async def rimuovi(chiamata: ServiceCall) -> None:
        er.async_get(hass).async_remove(chiamata.data["entity_id"])

    hass.services.async_register("prova", "salta", salta)
    hass.services.async_register("prova", "rimuovi", rimuovi)


@pytest.fixture
def servizi_di_prova(
    monkeypatch: pytest.MonkeyPatch, freezer: FrozenDateTimeFactory
) -> None:
    """Ogni Home Assistant di ``_corsa`` (test_semantica) ha anche i servizi di prova."""
    originale = semantica.async_test_home_assistant

    @asynccontextmanager
    async def con_servizi(*args: Any, **kwargs: Any) -> AsyncIterator[HomeAssistant]:
        async with originale(*args, **kwargs) as hass:
            _servizi_di_prova(hass, freezer)
            yield hass

    monkeypatch.setattr(semantica, "async_test_home_assistant", con_servizi)


def _confronta(atteso: list[Any], ottenuto: list[Any], cosa: str) -> None:
    if ottenuto == atteso:
        return
    diff = "\n".join(
        difflib.unified_diff(
            [repr(v) for v in atteso],
            [repr(v) for v in ottenuto],
            "home_assistant",
            "motore",
            lineterm="",
            n=2,
        )
    )
    pytest.fail(f"{cosa} diversi:\n{diff}")


async def _confronta_scenario(
    nome: str,
    testo: str,
    passi: list[tuple[Any, ...]],
    freezer: FrozenDateTimeFactory,
    moduli: list[str],  # noqa: F811
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Stesso registro degli eventi con Home Assistant e con il motore tradotto."""
    monkeypatch.setattr(
        "homeassistant.helpers.event.randint", lambda minimo, massimo: minimo
    )
    configurazione = yaml.safe_load(testo)
    atteso = await _corsa(
        freezer, f"c_{nome}", configurazione, passi, motore=False, moduli=moduli
    )
    ottenuto = await _corsa(
        freezer, f"c_{nome}", configurazione, passi, motore=True, moduli=moduli
    )
    assert any(
        voce[1] == EVENT_CALL_SERVICE and voce[2]["domain"] == "prova"
        for voce in atteso
    )
    _confronta(atteso, ottenuto, "registri")


@pytest.mark.parametrize("nome", sorted(SCENARI))
async def test_come_home_assistant(
    nome: str,
    freezer: FrozenDateTimeFactory,
    moduli: list[str],  # noqa: F811
    monkeypatch: pytest.MonkeyPatch,
    servizi_di_prova: None,
) -> None:
    """Stesso registro degli eventi con Home Assistant e con il motore tradotto."""
    await _confronta_scenario(nome, *SCENARI[nome], freezer, moduli, monkeypatch)


@pytest.mark.parametrize("wait_for_stop_scripts_after_shutdown", [True])
@pytest.mark.parametrize("nome", sorted(SCENARI_CHIUSURA))
async def test_dopo_la_chiusura_come_home_assistant(
    nome: str,
    freezer: FrozenDateTimeFactory,
    moduli: list[str],  # noqa: F811
    monkeypatch: pytest.MonkeyPatch,
    servizi_di_prova: None,
) -> None:
    """Come ``test_come_home_assistant``, con il timer di Home Assistant che 60 secondi
    dopo la chiusura ferma gli script in corso e vieta di avviarne di nuovi."""
    await _confronta_scenario(
        nome, *SCENARI_CHIUSURA[nome], freezer, moduli, monkeypatch
    )


# --- modelli: contesto.py e jinja.py ----------------------------------------------------

MODELLI = [
    # un filtro scelto per nome da una variabile: lo cerca l'ambiente di jinja.py
    "{% set f = 'regex_findall' %}{{ ['a1b22c', 12, none] | map(f, '\\\\d') | list }}",
    "{% set f = 'regex_findall' %}{{ ['A1a'] | map(f, 'a', true) | list }}",
    "{% set f = 'regex_findall_index' %}{{ ['a1b22', 345] | map(f, '\\\\d+', 1) | list }}",
    "{% set f = 'regex_findall_index' %}{{ ['a1'] | map(f, '\\\\d', 3) | list }}",
    "{% set f = 'regex_findall_index' %}{{ ['xAx', 'a'] | map(f, 'a', 0, true) | list }}",
    # una resa oltre il massimo di Home Assistant (256 KiB)
    "{{ 'x' * 262144 }}",
    "{{ 'x' * 262145 }}",
    "{% for i in [1, 2, 3] %}{{ 'y' * 100000 }}{% endfor %}",
]


async def test_modelli_come_home_assistant(banco: Banco) -> None:  # noqa: F811
    """Stesso testo, stesso valore interpretato, o errore in tutte e due."""
    for sorgente in MODELLI:
        banco.confronta(sorgente)
    assert banco.confronti == len(MODELLI) * 5 * 2
    assert not banco.differenze, "\n".join(banco.differenze)


async def test_modello_reso_senza_variabili(banco: Banco) -> None:  # noqa: F811
    """``ModelloHA`` è un ``Template``: reso senza variabili, come Home Assistant."""
    for sorgente in (
        "{{ 1 + 1 }}",
        "{{ x | default('nessuna') }}",
        "{{ states('sensor.t1') }} {{ is_state('input_boolean.a', 'on') }}",
        "{{ [1, 2] }}",
    ):
        funzione = banco.funzione(sorgente)
        modello_ha = Template(sorgente, banco.hass)
        modello_motore = banco.c.modello(funzione, sorgente)
        for interpreta in (False, True):
            assert _esito(
                lambda: modello_motore.async_render(parse_result=interpreta)  # noqa: B023
            ) == _esito(lambda: modello_ha.async_render(parse_result=interpreta))  # noqa: B023
        info_ha = modello_ha.async_render_to_info()
        info_motore = modello_motore.async_render_to_info()
        assert _esito(info_motore.result) == _esito(info_ha.result)
        assert info_motore.entities == info_ha.entities


# --- ha.py: più motori (una VMC ciascuno) e ricarica ------------------------------------

DUE_VMC = """
script:
  prova_master:
    alias: Prova Script Master
    mode: queued
    sequence:
      - action: prova.registra
        data: {passo: "script master {{ chi }}"}
      - delay: 3
      - action: prova.registra
        data: {passo: "script master fine {{ chi }}"}
automation:
  - alias: Prova Master
    id: prova_master
    mode: queued
    triggers:
      - {trigger: state, entity_id: input_boolean.a}
    actions:
      - action: prova.registra
        data: {passo: "automazione master {{ trigger.to_state.state }}"}
      - action: script.prova_master
        data: {chi: "{{ trigger.to_state.state }}"}
      - action: prova.registra
        data: {passo: "automazione master fine {{ trigger.to_state.state }}"}
"""

# senza automation_triggered: le logiche del motore non hanno l'evento
EVENTI_DUE_VMC = {EVENT_STATE_CHANGED, EVENT_CALL_SERVICE}


async def _due_vmc(
    freezer: FrozenDateTimeFactory,
    cartella: Path,
    *,
    motore: bool,
    moduli: list[str],  # noqa: F811
) -> list[Any]:
    """Le automazioni e gli script di due VMC (master e cucina): YAML in Home Assistant,
    o due motori (uno per VMC) con lo stesso codice tradotto; a metà, automation.reload
    e script.reload rileggono configuration.yaml."""
    freezer.move_to(T0)
    master = yaml.safe_load(DUE_VMC)
    cucina = yaml.safe_load(rinomina(DUE_VMC, "cucina"))
    yaml_utente: dict[str, Any] = {"automation": [], "script": {}}
    if not motore:
        yaml_utente = {
            "automation": [*master["automation"], *cucina["automation"]],
            "script": {**master["script"], **cucina["script"]},
        }
    cartella.mkdir()
    (cartella / "configuration.yaml").write_text(
        yaml.safe_dump(yaml_utente, allow_unicode=True), encoding="utf-8"
    )
    registro: list[Any] = []
    async with async_test_home_assistant(config_dir=str(cartella)) as hass:
        assert await async_setup_component(hass, "homeassistant", {})
        for dominio, voci in AIUTANTI.items():
            assert await async_setup_component(hass, dominio, {dominio: voci})

        async def registra(_chiamata: ServiceCall) -> None:
            return None

        hass.services.async_register("prova", "registra", registra)
        if motore:
            testo_modelli, testo_motore = await traduci_configurazione(
                hass,
                master["automation"],
                master["script"],
                nome_modelli="due_vmc_modelli",
            )
            moduli.append(f"{generato.__name__}.due_vmc_modelli")
            moduli.append(f"{generato.__name__}.due_vmc_motore")
            _carica("due_vmc_modelli", testo_modelli)
            codice = _carica("due_vmc_motore", testo_motore)
            for nome in ("master", "cucina"):
                await MotoreFase3(hass, nome).avvia(
                    crea=codice.crea, configurazione={"automation": [], "script": {}}
                )
        else:
            assert await async_setup_component(
                hass, "script", {"script": yaml_utente["script"]}
            )
            assert await async_setup_component(
                hass, "automation", {"automation": yaml_utente["automation"]}
            )
        await _gira(hass)

        @callback
        def annota(evento: Event) -> None:
            if evento.event_type not in EVENTI_DUE_VMC:
                return
            dati = evento.data
            if evento.event_type == EVENT_STATE_CHANGED:
                dati = {"entity_id": dati["entity_id"], "new_state": dati["new_state"]}
            registro.append(
                (_norma(evento.time_fired), evento.event_type, _norma(dict(dati)))
            )

        togli = hass.bus.async_listen(MATCH_ALL, annota)
        # gli stati delle logiche (le automazioni dei motori) entrano nel registro nel
        # punto del bus di state_changed (con Home Assistant non ce ne sono)
        smetti = stati_logiche(hass).osserva(
            callback(lambda e: annota(e) if e.event_type == EVENT_STATE_CHANGED else None)
        )
        for passo in (
            ("input_boolean", "turn_on", {"entity_id": "input_boolean.a"}),
            1,
            ("automation", "reload", {}),
            ("script", "reload", {}),
            1,
            ("input_boolean", "turn_off", {"entity_id": "input_boolean.a"}),
            8,
        ):
            if isinstance(passo, tuple):
                await hass.services.async_call(*passo, blocking=True)
                await _gira(hass)
            else:
                await _avanza(hass, freezer, passo)
        togli()
        smetti()
        stati = [
            *hass.states.async_all(("automation", "script")),
            *stati_logiche(hass).stati.values(),
        ]
        registro.append(
            sorted((s.entity_id, s.state, _norma(dict(s.attributes))) for s in stati)
        )
        await hass.async_stop(force=True)
    return registro


async def test_due_motori_e_ricarica_come_home_assistant(
    freezer: FrozenDateTimeFactory,
    moduli: list[str],  # noqa: F811
    tmp_path: Path,
) -> None:
    """Due VMC sullo stesso Home Assistant: le automazioni (logiche) e gli script di
    entrambi i motori restano (con le esecuzioni in corso) quando automation.reload e
    script.reload rileggono la configurazione, come il YAML invariato."""
    atteso = await _due_vmc(freezer, tmp_path / "ha", motore=False, moduli=moduli)
    ottenuto = await _due_vmc(freezer, tmp_path / "m", motore=True, moduli=moduli)
    avvii = [
        voce
        for voce in atteso[:-1]
        if voce[1] == EVENT_CALL_SERVICE
        and re.fullmatch(
            r"automazione \w+ (on|off)", str(voce[2]["service_data"].get("passo"))
        )
    ]
    assert len(avvii) == 4
    assert len(atteso[-1]) == 4
    _confronta(atteso, ottenuto, "registri")
