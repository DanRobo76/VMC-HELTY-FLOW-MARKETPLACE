"""Automazioni e script tradotti con ``timer_motore``: i timer del motore al posto di
quelli di Home Assistant, a confronto.

Come ``test_semantica_tempi.py``: ogni prova scrive automazioni e script in YAML con le
forme che il package usa con i suoi timer (``timer.start`` con e senza durata, con il
bersaglio di un modello, ``timer.cancel`` in un ciclo, il trigger ``timer.finished``
senza filtro della Countdown Letture, le letture ``is_state``/``state_attr``/``states``
di un timer...) e li fa girare due volte con lo stesso orologio fermo:

1. con Home Assistant: le integrazioni ``automation``, ``script`` e ``timer``;
2. tradotti con ``timer_motore=True`` sul motore con i timer del motore (``Motore.avvia(
   ..., timer=...)``); l'integrazione ``timer`` di Home Assistant c'è solo con un timer
   «dell'utente», che non è del package e resta di Home Assistant in entrambe le corse.

Si confrontano:

- il registro degli eventi di Home Assistant senza ciò che dei timer del package non c'è
  più nella seconda corsa: i loro cambi di stato, i loro eventi (``timer.started``...)
  e le chiamate ai loro servizi (``call_service`` con dominio ``timer``); i contesti
  diventano numeri d'ordine dopo aver tolto quegli eventi;
- il registro dei timer del package: ogni scrittura (stato, attributi, istanti,
  contesto) e ogni evento, dalla macchina degli stati e dal bus di Home Assistant nella
  prima corsa, dal registro dei timer del motore e dal suo bus nella seconda.
"""

from __future__ import annotations

import asyncio
import difflib
import logging
from collections.abc import Callable
from datetime import datetime, timedelta
from typing import Any

import pytest
import yaml
from freezegun.api import FrozenDateTimeFactory
from homeassistant.const import EVENT_CALL_SERVICE, EVENT_STATE_CHANGED, MATCH_ALL
from homeassistant.core import Context, CoreState, Event, State, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.setup import async_setup_component
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import async_test_home_assistant

from custom_components.vmc_master.nativa.motore.stati_logiche import stati_logiche
from custom_components.vmc_master.nativa.motore.timer import (
    EVENTI_TIMER,
    bus_del_motore,
)

from . import generato
from .fase3 import MotoreFase3
from .nel_canale import ordine_esterno, stato_di_logica
from .test_semantica import _carica, _gira, della_pulizia, moduli  # noqa: F401
from .test_semantica_tempi import (  # noqa: F401
    EVENTI,
    T0,
    _avanza,
    _fino_alla_fine,
    _Messaggi,
    _pulisci_timer,
    ordine_dei_timer,
    tempi_casuali,
    wait_for_stop_scripts_after_shutdown,
)
from .traduci import traduci_configurazione

AIUTANTI: dict[str, dict[str, Any]] = {
    "input_boolean": {"a": {}, "b": {}, "c": {}},
    "input_number": {"n": {"min": 0, "max": 100, "step": 1}},
    "input_text": {"famiglia": {"initial": "uno"}},
}
# I timer «del package» (del motore nella seconda corsa) e quello «dell'utente»
TIMER_PACKAGE: dict[str, Any] = {
    "countdown_uno": {"name": "Uno", "icon": "mdi:timer-sand"},
    "countdown_due": {"name": "Due", "icon": "mdi:timer-sand"},
    "lettura_ping": {"name": "Ping", "icon": "mdi:timer-sand"},
    "lettura_ventilazione": {"name": "Ventilazione", "icon": "mdi:timer-sand"},
    "script_reset": {"duration": "00:00:05", "name": "Reset"},
    "avvio": {"duration": "00:00:07", "name": "Avvio"},
}
TIMER_UTENTE: dict[str, Any] = {"utente": {"duration": "00:00:03"}}
ID_PACKAGE = {f"timer.{oggetto}" for oggetto in TIMER_PACKAGE}

SCENARI: dict[str, dict[str, Any]] = {}


def scenario(nome: str, configurazione: str, *passi: Any, avvio: bool = False) -> None:
    piatti: list[tuple[Any, ...]] = []
    for passo in passi:
        piatti.extend(passo if isinstance(passo, list) else [passo])
    SCENARI[nome] = {"configurazione": configurazione, "passi": piatti, "avvio": avvio}


def servizio(nome: str, dati: dict[str, Any] | None = None) -> tuple[Any, ...]:
    return ("servizio", nome, dati or {})


def scheda(nome: str, dati: dict[str, Any]) -> tuple[Any, ...]:
    """Un servizio dei timer dalla scheda (un utente): ai timer di Home Assistant nella
    prima corsa, a quelli del motore nella seconda (se il bersaglio è del package)."""
    return ("scheda", nome, dati)


def attendi(secondi: float) -> tuple[Any, ...]:
    return ("attendi", secondi)


def acceso(entita: str) -> tuple[Any, ...]:
    return servizio("input_boolean.turn_on", {"entity_id": entita})


def spento(entita: str) -> tuple[Any, ...]:
    return servizio("input_boolean.turn_off", {"entity_id": entita})


def numero(valore: float) -> tuple[Any, ...]:
    return servizio(
        "input_number.set_value", {"entity_id": "input_number.n", "value": valore}
    )


def famiglia(valore: str) -> tuple[Any, ...]:
    return servizio(
        "input_text.set_value", {"entity_id": "input_text.famiglia", "value": valore}
    )


# --- scenari --------------------------------------------------------------------------------

scenario(
    "countdown_letture",
    # La Countdown Letture VMC del package: time_pattern, homeassistant start e
    # timer.finished senza filtro (anche del timer dell'utente), letture is_state e
    # state_attr del timer di un modello, timer.start con la durata e il bersaglio di un
    # modello, trigger.event.data.entity_id
    """
automation:
  - alias: Countdown Letture
    mode: queued
    max: 10
    triggers:
      - {trigger: homeassistant, event: start, id: allinea}
      - {trigger: time_pattern, seconds: "/4", id: allinea}
      - {trigger: event, event_type: timer.finished, id: scaduto}
    variables:
      chiavi: >-
        {%- if trigger.id == 'allinea' -%}{{ ['ping', 'ventilazione'] }}
        {%- elif trigger.event.data.entity_id | default('') is match('timer\\.lettura_') -%}{{ [trigger.event.data.entity_id | replace('timer.lettura_', '')] }}
        {%- else -%}{{ [] }}{%- endif -%}
    actions:
      - action: prova.registra
        data:
          passo: "{{ trigger.id }} {{ chiavi }} {{ trigger.event.data if trigger.event is defined else '' }}"
      - repeat:
          for_each: "{{ chiavi }}"
          sequence:
            - variables:
                timer_lettura: "timer.lettura_{{ repeat.item }}"
                mancano: "{{ 3 if repeat.item == 'ping' else 5 }}"
                scarto: >-
                  {{ ((as_timestamp(state_attr(timer_lettura, 'finishes_at'), 0) - (as_timestamp(now()) + mancano | int(0))) | abs) | round(3)
                     if is_state(timer_lettura, 'active') else 9999 }}
            - action: prova.registra
              data:
                passo: "{{ repeat.item }} {{ scarto }} {{ states(timer_lettura) }}"
            - if: "{{ trigger.id == 'scaduto' or scarto | float(0) > 1 }}"
              then:
                - action: timer.start
                  target:
                    entity_id: "{{ timer_lettura }}"
                  data:
                    duration: "{{ '00:00:%02d' % (mancano | int(0)) }}"
""",
    attendi(9),
    scheda("timer.start", {"entity_id": "timer.utente"}),
    attendi(4),
    scheda("timer.finish", {"entity_id": "timer.lettura_ping"}),
    scheda("timer.pause", {"entity_id": "timer.lettura_ventilazione"}),
    attendi(6),
    scheda("timer.start", {"entity_id": "timer.lettura_ventilazione"}),
    attendi(7),
    avvio=True,
)

scenario(
    "countdown_attese",
    # La Countdown Attese Automazione del package: trigger modello, timer.start con il
    # bersaglio e la durata di un modello (mode parallel), timer.cancel in un ciclo con il
    # bersaglio di un modello; letture nelle condizioni e nei testi
    """
automation:
  - alias: Countdown Attese
    mode: parallel
    max: 300
    triggers:
      - {trigger: template, value_template: "{{ is_state('input_boolean.a', 'on') }}", id: "ON|uno|3"}
      - {trigger: template, value_template: "{{ is_state('input_boolean.a', 'off') }}", id: "OFF|uno|3"}
      - {trigger: template, value_template: "{{ is_state('input_boolean.b', 'on') }}", id: "ON|due|2"}
      - {trigger: template, value_template: "{{ is_state('input_boolean.b', 'off') }}", id: "OFF|due|2"}
    variables:
      verso: "{{ trigger.id.split('|')[0] }}"
      famiglia: "{{ trigger.id.split('|')[1] }}"
      durata: "{{ trigger.id.split('|')[2] | int }}"
    actions:
      - if: "{{ verso == 'ON' }}"
        then:
          - action: timer.start
            target:
              entity_id: "timer.countdown_{{ famiglia }}"
            data:
              duration: "{{ durata }}"
        else:
          - repeat:
              for_each: "{{ [famiglia] }}"
              sequence:
                - condition: template
                  value_template: "{{ is_state('timer.countdown_' ~ repeat.item, 'active') }}"
                - action: timer.cancel
                  target:
                    entity_id: "timer.countdown_{{ repeat.item }}"
      - action: prova.registra
        data:
          passo: >-
            {{ verso }} {{ famiglia }} {{ states('timer.countdown_' ~ famiglia) }}
            {{ state_attr('timer.countdown_' ~ famiglia, 'remaining') }}
            {{ 'timer.countdown_uno' | state_attr('finishes_at') }}
            {{ 'timer.countdown_due' is is_state('active') }}
            {{ states['timer.countdown_uno'].state }} {{ states.timer.countdown_due.last_changed }}
            {{ is_state('timer.countdown_uno', ['active', 'paused']) }}
            {{ ['timer.countdown_uno', 'timer.countdown_due', 'timer.utente'] | select('is_state', 'active') | list }}
            {{ states('TIMER.COUNTDOWN_UNO') }} {{ states('timer.utente') }}
            {{ states.timer.utente.state }} {{ states['timer.' ~ famiglia] }}
            {{ states['timer.countdown_' ~ famiglia].state }}
""",
    acceso("input_boolean.a"),
    attendi(1),
    acceso("input_boolean.b"),
    attendi(1.5),
    spento("input_boolean.b"),
    attendi(0.5),
    spento("input_boolean.a"),
    acceso("input_boolean.a"),
    attendi(4),
    acceso("input_boolean.b"),
    scheda("timer.start", {"entity_id": "timer.utente"}),
    attendi(3),
)

scenario(
    "script_e_riallineamento",
    # Gli script del package (reset filtro, panic button...): timer.start senza dati,
    # pausa, timer.cancel; il riallineamento al riavvio (homeassistant start); il timer
    # che finisce mentre uno script lo aspetta; il trigger timer.finished con un filtro
    """
script:
  reset_filtro:
    sequence:
      - action: timer.start
        target: {entity_id: timer.script_reset}
      - delay: 2
      - action: prova.registra
        data: {passo: "reset {{ states('timer.script_reset') }} {{ state_attr('timer.script_reset', 'finishes_at') }}"}
      - action: timer.cancel
        target: {entity_id: timer.script_reset}
automation:
  - alias: Riallineamento
    triggers:
      - {trigger: homeassistant, event: start}
    actions:
      - action: timer.start
        entity_id: timer.avvio
      - action: prova.registra
        data: {passo: "avvio {{ states('timer.avvio') }}"}
  - alias: Fine Avvio
    triggers:
      - trigger: event
        event_type: timer.finished
        event_data: {entity_id: timer.avvio}
      - trigger: event
        event_type: [timer.cancelled, timer.started]
    actions:
      - action: prova.registra
        data: {passo: "{{ trigger.event.event_type }} {{ trigger.event.data.entity_id }} {{ trigger.platform }}"}
      - if: "{{ trigger.event.data.entity_id == 'timer.avvio' and trigger.event.event_type == 'timer.finished' }}"
        then:
          - action: script.reset_filtro
""",
    attendi(10),
    servizio("script.turn_on", {"entity_id": "script.reset_filtro"}),
    attendi(1),
    scheda("timer.start", {"entity_id": "timer.utente"}),
    attendi(5),
    avvio=True,
)


# --- macchina delle prove ---------------------------------------------------------------------


def _norma(valore: Any, contesti: Callable[[Context], Any]) -> Any:
    if isinstance(valore, datetime):
        return round((valore - T0).total_seconds(), 6)
    if isinstance(valore, Context):
        return contesti(valore)
    if isinstance(valore, State):
        return (
            valore.entity_id,
            valore.state,
            _norma(dict(valore.attributes), contesti),
            _norma(valore.last_changed, contesti),
            _norma(valore.last_updated, contesti),
            _norma(valore.last_reported, contesti),
            contesti(valore.context),
        )
    if isinstance(valore, dict):
        return {
            str(k): _norma(v, contesti)
            for k, v in sorted(valore.items(), key=lambda kv: str(kv[0]))
            if k != "run_id"
        }
    if isinstance(valore, (list, tuple)):
        return [_norma(v, contesti) for v in valore]
    return valore


def _del_package(evento: Event) -> bool:
    """Un evento che nella seconda corsa non c'è più: dei timer del package."""
    dati = evento.data
    if evento.event_type == EVENT_STATE_CHANGED:
        return dati["entity_id"] in ID_PACKAGE
    if evento.event_type in EVENTI_TIMER:
        return dati.get("entity_id") in ID_PACKAGE
    if evento.event_type == EVENT_CALL_SERVICE:
        return dati["domain"] == "timer"
    return False


async def _corsa(
    freezer: FrozenDateTimeFactory,
    nome: str,
    prova: dict[str, Any],
    *,
    motore: bool,
    moduli: list[str],  # noqa: F811
    chiave: Callable[[Any], Any],
    a_passi: float | None,
) -> tuple[list[Any], list[Any]]:
    """Una corsa: il registro degli eventi (senza quelli dei timer del package) e il
    registro dei timer del package, normalizzati con la stessa numerazione dei
    contesti."""
    freezer.move_to(T0)
    registro: list[Any] = []
    dei_timer: list[Any] = []
    configurazione = yaml.safe_load(prova["configurazione"])

    def istante() -> datetime:
        return dt_util.utcnow()

    messaggi = _Messaggi(registro, istante)
    radice = logging.getLogger()
    radice.addHandler(messaggi)
    stato_iniziale = CoreState.not_running if prova["avvio"] else CoreState.running
    try:
        async with async_test_home_assistant(initial_state=stato_iniziale) as hass:
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
                if _del_package(evento):
                    if evento.event_type == EVENT_STATE_CHANGED:
                        dei_timer.append(("stato", dati["new_state"]))
                    elif evento.event_type != EVENT_CALL_SERVICE:
                        dei_timer.append(
                            (
                                "evento",
                                evento.time_fired,
                                evento.event_type,
                                dict(dati),
                                evento.context,
                            )
                        )
                    return
                registro.append(
                    (evento.time_fired, evento.event_type, dict(dati), evento.context)
                )

            assert await async_setup_component(hass, "homeassistant", {})
            for dominio, voci in AIUTANTI.items():
                assert await async_setup_component(hass, dominio, {dominio: voci})
            timer_ha = (
                dict(TIMER_UTENTE) if motore else {**TIMER_PACKAGE, **TIMER_UTENTE}
            )
            assert await async_setup_component(hass, "timer", {"timer": timer_ha})

            async def registra(chiamata: Any) -> None:
                if chiamata.data.get("errore"):
                    raise HomeAssistantError("errore voluto")

            hass.services.async_register("prova", "registra", registra)
            automazioni = configurazione.get("automation", [])
            script = configurazione.get("script", {})
            if motore:
                testo_modelli, testo_motore = await traduci_configurazione(
                    hass,
                    automazioni,
                    script,
                    nome_modelli=f"timer_{nome}_modelli",
                    timer_motore=True,
                )
                moduli.append(f"{generato.__name__}.timer_{nome}_modelli")
                moduli.append(f"{generato.__name__}.timer_{nome}_motore")
                _carica(f"timer_{nome}_modelli", testo_modelli)
                codice = _carica(f"timer_{nome}_motore", testo_motore)
                m = MotoreFase3(hass)
                await m.avvia(crea=codice.crea, timer=TIMER_PACKAGE)
                assert m.c.timer is not None
                m.c.timer.ascolta(
                    callback(lambda t: dei_timer.append(("stato", t.stato_ha)))
                )
                for tipo in sorted(EVENTI_TIMER):
                    bus_del_motore(hass).async_listen(
                        tipo,
                        callback(
                            lambda e: dei_timer.append(
                                (
                                    "evento",
                                    e.time_fired,
                                    e.event_type,
                                    dict(e.data),
                                    e.context,
                                )
                            )
                        ),
                    )

                async def scheda(
                    nome_servizio: str, dati: dict[str, Any], contesto: Context
                ) -> None:
                    dominio, servizio_timer = nome_servizio.split(".")
                    if dati["entity_id"] in ID_PACKAGE:
                        await m.c.timer.servizio(
                            servizio_timer, dict(dati), None, contesto
                        )
                    else:
                        await hass.services.async_call(
                            dominio,
                            servizio_timer,
                            dati,
                            blocking=True,
                            context=contesto,
                        )
            else:
                assert await async_setup_component(hass, "script", {"script": script})
                assert await async_setup_component(
                    hass, "automation", {"automation": automazioni}
                )

                async def scheda(
                    nome_servizio: str, dati: dict[str, Any], contesto: Context
                ) -> None:
                    dominio, servizio_timer = nome_servizio.split(".")
                    await hass.services.async_call(
                        dominio, servizio_timer, dati, blocking=True, context=contesto
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

            for passo in prova["passi"]:
                if passo[0] == "servizio":
                    dominio, nome_servizio = passo[1].split(".")
                    await hass.services.async_call(
                        dominio, nome_servizio, passo[2], blocking=True
                    )
                    await _gira(hass)
                elif passo[0] == "scheda":
                    await scheda(passo[1], passo[2], Context())
                    await _gira(hass)
                else:
                    await _avanza(hass, freezer, passo[1], a_passi)
            # con Home Assistant spegne le automazioni (automation.turn_off), con il motore
            # ferma le logiche: i loro stati non si confrontano
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
            freezer.tick(timedelta(seconds=61))
            await _gira(hass)
            for maniglia in hass.loop._scheduled:
                maniglia.cancel()
    finally:
        radice.removeHandler(messaggi)
    numeri: dict[str | None, int] = {}

    def contesti(contesto: Context) -> tuple[int, int | None]:
        numero = numeri.setdefault(contesto.id, len(numeri))
        genitore = (
            None
            if contesto.parent_id is None
            else numeri.setdefault(contesto.parent_id, len(numeri))
        )
        return (numero, genitore)

    # gli stati delle logiche (le automazioni del motore) non passano dal bus: possono
    # passare prima degli eventi che Home Assistant tiene in coda (nel_canale); i contesti
    # diventano numeri in quest'ordine
    return (
        [_norma(v, contesti) for v in ordine_esterno(registro, stato_di_logica)],
        [_norma(v, contesti) for v in dei_timer],
    )


def _diff(atteso: list[Any], ottenuto: list[Any]) -> str:
    return "\n".join(
        difflib.unified_diff(
            [repr(v) for v in atteso],
            [repr(v) for v in ottenuto],
            "home_assistant",
            "motore",
            lineterm="",
            n=3,
        )
    )


@pytest.mark.usefixtures("tempi_casuali")
@pytest.mark.parametrize("passo", [None, 0.1], ids=["timer_per_timer", "a_passi"])
@pytest.mark.parametrize("nome", sorted(SCENARI))
async def test_timer_del_motore_nel_codice_tradotto(
    nome: str,
    passo: float | None,
    freezer: FrozenDateTimeFactory,
    moduli: list[str],  # noqa: F811
    ordine_dei_timer: Callable[[Any], Any],  # noqa: F811
) -> None:
    """Stesso registro degli eventi (senza quelli dei timer del package) e stesse
    scritture ed eventi dei timer del package, istante per istante, con i timer di Home
    Assistant e con quelli del motore nel codice tradotto con ``timer_motore``."""
    prova = SCENARI[nome]
    argomenti = {"moduli": moduli, "chiave": ordine_dei_timer, "a_passi": passo}
    atteso, timer_atteso = await _corsa(freezer, nome, prova, motore=False, **argomenti)
    ottenuto, timer_ottenuto = await _corsa(
        freezer, nome, prova, motore=True, **argomenti
    )
    assert any(v[2] == "timer.finished" for v in timer_atteso if v[0] == "evento")
    assert any(v[1] == EVENT_CALL_SERVICE and v[2]["domain"] == "prova" for v in atteso)
    if ottenuto != atteso:
        pytest.fail(f"registri diversi:\n{_diff(atteso, ottenuto)}")
    if timer_ottenuto != timer_atteso:
        pytest.fail(
            f"registri dei timer diversi:\n{_diff(timer_atteso, timer_ottenuto)}"
        )
