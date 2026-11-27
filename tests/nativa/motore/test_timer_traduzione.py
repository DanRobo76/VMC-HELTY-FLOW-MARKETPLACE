"""Il traduttore con ``timer_motore`` (fase 4): cosa cambia nel package, e cosa ferma la
traduzione.

- Spento (il valore normale) il codice è quello di sempre (``generato/`` non cambia: lo
  controlla ``test_traduzione.py``).
- Acceso, nel package cambiano esattamente: i 16 servizi dei timer (10 ``start``, 6
  ``cancel``) che vanno a ``motore_timer.*``, il trigger ``timer.finished`` della
  Countdown Letture VMC che diventa ``motore_timer``, e le letture di 7 modelli che
  possono riguardare un timer, che passano da ``c.timer``. Nient'altro.
- Quello che i timer del motore non sanno fare (un trigger o una condizione sullo stato
  di un timer, un modello seguito da Home Assistant che legge un timer, l'attesa della
  chiamata di un servizio dei timer, letture di tutti gli stati...) ferma la traduzione
  invece di tradursi in qualcosa d'altro.
"""

from __future__ import annotations

import re
from collections import Counter
from typing import Any

import pytest
from homeassistant.core import HomeAssistant

from .rinomina import Rinomina
from .traduci import leggi_comandi, leggi_package, traduzione
from .traduci_jinja import NonTraducibile

# I modelli del package che leggono un timer (o qualcosa che può esserlo). Dalla b42 anche
# m0396, la guardia delle 4 opzioni dell'Esclusività Finestre Opzioni
# («is_state(trigger.entity_id, trigger.to_state.state)»: l'entità del trigger non è nota
# prima); i 22 modelli nuovi della b42 spostano di 22 i numeri dopo di lei (m0775 e m0942
# della b41). Il modello nuovo della b44 (nessun avviso dei cellulari aprendo la finestra
# Opzioni) sposta di 1 l'ultimo (m0964 della b43).
INSTRADATI = ["m0011", "m0015", "m0347", "m0350", "m0396", "m0797", "m0965"]


async def test_il_package_con_i_timer_del_motore(hass: HomeAssistant) -> None:
    """Le sole differenze del package tradotto con ``timer_motore``, contate."""
    automazioni, script = leggi_package()
    jinja, _, modelli, motore = await traduzione(hass, automazioni, script)
    spento = await traduzione(hass, automazioni, script, timer_motore=False)
    assert spento[2:] == (modelli, motore)
    assert not jinja.instradati
    jinja_t, _, modelli_t, motore_t = await traduzione(
        hass, automazioni, script, timer_motore=True
    )
    assert sorted(jinja_t.instradati) == INSTRADATI

    # servizi
    assert Counter(re.findall(r"r\.servizio\('timer\.(\w+)'", motore)) == {
        "start": 10,
        "cancel": 6,
    }
    assert Counter(re.findall(r"r\.servizio\('motore_timer\.(\w+)'", motore_t)) == {
        "start": 10,
        "cancel": 6,
    }
    assert not re.findall(r"r\.servizio\('timer\.", motore_t)
    # trigger
    trigger = (
        "{'event_type': [c.statico('timer.finished')], 'id': 'scaduto', 'platform': "
    )
    assert motore.count(trigger + "'event'}") == 1
    assert motore_t.count(trigger + "'motore_timer'}") == 1
    assert motore_t.count("'platform': 'motore_timer'") == 1
    # letture
    letture = Counter(re.findall(r"c\.timer\.(\w+)", modelli_t))
    assert letture == {"states": 2, "stati": 2, "state_attr": 2, "is_state": 3}
    assert "c.timer." not in modelli

    # nient'altro: tolte le differenze contate, il testo è lo stesso
    assert (
        motore_t.replace("r.servizio('motore_timer.", "r.servizio('timer.").replace(
            trigger + "'motore_timer'}", trigger + "'event'}"
        )
        == motore
    )
    indietro = modelli_t
    for nome in ("states(", "state_attr(", "is_state("):
        indietro = indietro.replace(f"c.timer.{nome}", f"c.{nome}")
    assert indietro.replace("c.timer.stati", "c.states") == modelli


async def test_con_gli_script_interni_le_stesse_differenze(hass: HomeAssistant) -> None:
    """Con gli script e i comandi dentro il motore (``comandi=``) ``timer_motore`` cambia
    le stesse cose e nient'altro: i due parametri sono indipendenti."""
    automazioni, script = leggi_package()
    comandi = leggi_comandi()
    _, _, modelli, motore = await traduzione(hass, automazioni, script, comandi=comandi)
    jinja_t, _, modelli_t, motore_t = await traduzione(
        hass, automazioni, script, comandi=comandi, timer_motore=True
    )
    assert sorted(jinja_t.instradati) == INSTRADATI
    assert Counter(re.findall(r"r\.servizio\('motore_timer\.(\w+)'", motore_t)) == {
        "start": 10,
        "cancel": 6,
    }
    assert motore_t.count("'platform': 'motore_timer'") == 1
    assert "def comandi(c):" in motore_t
    trigger = (
        "{'event_type': [c.statico('timer.finished')], 'id': 'scaduto', 'platform': "
    )
    assert (
        motore_t.replace("r.servizio('motore_timer.", "r.servizio('timer.").replace(
            trigger + "'motore_timer'}", trigger + "'event'}"
        )
        == motore
    )
    indietro = modelli_t
    for nome in ("states(", "state_attr(", "is_state("):
        indietro = indietro.replace(f"c.timer.{nome}", f"c.{nome}")
    assert indietro.replace("c.timer.stati", "c.states") == modelli


async def test_la_mappa_dei_nomi_non_rinomina_i_timer(hass: HomeAssistant) -> None:
    """Con ``timer_motore`` i timer tengono il loro entity_id: la mappa dei nomi non può
    cambiarli."""
    rinomina = Rinomina(
        {"timer.vmc_master_lettura_ping": "sensor.vmc_master_lettura_ping"}
    )
    with pytest.raises(ValueError, match="timer_motore"):
        await traduzione(hass, [], {}, rinomina=rinomina, timer_motore=True)


def _automazione(**parti: Any) -> dict[str, Any]:
    return {
        "id": "prova",
        "alias": "Prova",
        "triggers": [{"trigger": "event", "event_type": "prova"}],
        "actions": [{"delay": 1}],
        **parti,
    }


def _variabile(modello: str) -> dict[str, Any]:
    return _automazione(actions=[{"variables": {"x": modello}}])


TIMER = "timer.vmc_master_lettura_ping"

NON_TRADUCIBILI: dict[str, dict[str, Any]] = {
    "trigger_state": _automazione(
        triggers=[{"trigger": "state", "entity_id": TIMER, "to": "active"}]
    ),
    "trigger_numeric_state": _automazione(
        triggers=[{"trigger": "numeric_state", "entity_id": TIMER, "above": 1}]
    ),
    "trigger_template": _automazione(
        triggers=[
            {
                "trigger": "template",
                "value_template": f"{{{{ is_state('{TIMER}', 'idle') }}}}",
            }
        ]
    ),
    "condizione_state": _automazione(
        conditions=[{"condition": "state", "entity_id": TIMER, "state": "idle"}]
    ),
    "wait_template": _automazione(
        actions=[{"wait_template": f"{{{{ states('{TIMER}') == 'idle' }}}}"}]
    ),
    "trigger_call_service_senza_dominio": _automazione(
        triggers=[{"trigger": "event", "event_type": "call_service"}]
    ),
    "trigger_call_service_dei_timer": _automazione(
        triggers=[
            {
                "trigger": "event",
                "event_type": "call_service",
                "event_data": {"domain": "timer"},
            }
        ]
    ),
    "trigger_evento_dinamico_senza_dominio": _automazione(
        triggers=[{"trigger": "event", "event_type": "{{ 'call_' ~ 'service' }}"}]
    ),
    "servizio_sconosciuto": _automazione(
        actions=[{"action": "timer.reload", "data": {}}]
    ),
    "states_timer": _variabile("{{ states.timer | count }}"),
    "tutti_gli_stati": _variabile("{{ states | count }}"),
    "expand": _variabile(f"{{{{ expand('{TIMER}') | count }}}}"),
    "integration_entities": _variabile("{{ integration_entities('timer') }}"),
}


@pytest.mark.parametrize("nome", sorted(NON_TRADUCIBILI))
async def test_quello_che_i_timer_del_motore_non_sanno_fare(
    hass: HomeAssistant, nome: str
) -> None:
    """Si traduce senza ``timer_motore``, ferma la traduzione con ``timer_motore``."""
    automazione = NON_TRADUCIBILI[nome]
    await traduzione(hass, [automazione], {})
    with pytest.raises(NonTraducibile):
        await traduzione(hass, [automazione], {}, timer_motore=True)


# modello -> instradato (passa da ``c.timer``)
LETTURE: dict[str, bool] = {
    f"{{{{ states('{TIMER}') }}}}": True,
    f"{{{{ is_state('{TIMER}', 'active') }}}}": True,
    f"{{{{ state_attr('{TIMER}', 'finishes_at') }}}}": True,
    f"{{{{ '{TIMER}' | states }}}}": True,
    f"{{{{ '{TIMER}' is is_state('idle') }}}}": True,
    f"{{{{ states['{TIMER}'].state }}}}": True,
    f"{{{{ states.{TIMER}.last_changed }}}}": True,
    "{{ states(x) }}": True,
    "{{ states('timer.vmc_master_' ~ x) }}": True,
    "{{ states('sensor.vmc_master_t') }}": False,
    "{{ states('sensor.' ~ x) }}": False,
    "{{ is_state('input_boolean.vmc_master_a', 'on') }}": False,
    "{{ states.sensor.vmc_master_t.state }}": False,
    "{{ states['sensor.vmc_master_t'].state }}": False,
    "{{ integration_entities('mobile_app') | select('is_state', 'on') | list }}": False,
    "{{ now() }}": False,
}


@pytest.mark.parametrize("modello", list(LETTURE), ids=range(len(LETTURE)))
async def test_letture_che_passano_dai_timer_del_motore(
    hass: HomeAssistant, modello: str
) -> None:
    """Passano da ``c.timer`` solo le letture che possono riguardare un timer
    (``c.timer`` manda a Home Assistant quelle che non lo riguardano)."""
    jinja, _, modelli, _ = await traduzione(
        hass, [_variabile(modello)], {}, timer_motore=True
    )
    assert bool(jinja.instradati) is LETTURE[modello]
    assert ("c.timer." in modelli) is LETTURE[modello]
