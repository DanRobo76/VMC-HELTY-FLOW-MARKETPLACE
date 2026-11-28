"""Il motore con la memoria interna si comporta come Home Assistant con gli aiutanti.

Prove mirate (fase 4): automazioni e script in YAML che leggono e scrivono valori
interni (con il nome scritto e con nomi composti dai modelli) girano con Home Assistant e
con i 67 aiutanti del package, poi, tradotti con i valori interni
(``traduci_configurazione(..., interni=INTERNI)``), con il motore e la memoria interna.
Si confronta tutto il registro degli eventi (con istanti e contesti) come spiega
``banco_memoria``: gli eventi degli aiutanti interni con gli annunci della memoria.

Coperti: trigger ``template`` che leggono valori interni (anche dentro ``or``), trigger
``state`` su un valore interno (qualsiasi cambio e ``to:``), ``for:`` di un trigger
scritto con un modello che legge un'attesa, ``wait_template``, condizioni ``state`` e
``template``, letture di ``last_changed``, attributi, ``has_value``, ``expand``,
``states.d.o``, scritture con bersaglio scritto, composto o reso da una variabile, più
bersagli, servizi misti (interruttori veri e valore interno insieme), aggiornamento delle
entità, errori di validazione, chiamate di un utente.
"""

from __future__ import annotations

import difflib
from datetime import UTC, datetime
from typing import Any
from unittest.mock import patch

import pytest
import yaml
from freezegun.api import FrozenDateTimeFactory
from homeassistant.components.homeassistant import services as servizi_ha
from homeassistant.const import EVENT_STATE_CHANGED, MATCH_ALL
from homeassistant.core import (
    Context,
    HomeAssistant,
    ServiceCall,
    State,
    callback,
)
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import async_test_home_assistant

from custom_components.vmc_master.nativa.motore.memoria_interna import (
    INTERNI,
    MemoriaInterna,
    da_stato,
)
from custom_components.vmc_master.nativa.motore.stati_logiche import stati_logiche

from . import generato
from .banco_memoria import Smistatore, servizi_misti
from .fase3 import MotoreFase3
from .nel_canale import (
    ordine_esterno,
    osserva_nel_canale,
    rinumera_ovunque,
    voce_interna,
)
from .test_avvio_motore import _ripristina
from .test_memoria_interna import IDS, _configurazione, _entity_id
from .test_pacchetto_casuale import Normalizzatore
from .test_semantica import _avanza, _carica, _gira, moduli  # noqa: F401
from .traduci import traduci_configurazione
from .traduci_jinja import NonTraducibile

T0 = datetime(2026, 11, 25, 10, 0, 0, tzinfo=UTC)
ALTRI = {
    "input_boolean": {"a": {}, "b": {}},
    "input_select": {"s": {"options": ["x", "y"]}},
}
# Senza ``automation_triggered``: le automazioni del motore sono logiche dell'integrazione,
# senza l'evento (l'istante in cui partono è nel loro stato: ``last_triggered``, ``current``)
EVENTI = {
    "state_changed",
    "call_service",
    "script_started",
}
RIPRISTINO = [
    State("input_number.vmc_master_attesa_avvisi", "3"),
    State("input_number.vmc_master_aria_scambiata_v1", "4.5"),
    State("input_text.vmc_master_countdown_avvisi", "3"),
    State("input_text.vmc_master_ultima_scelta_utente", "Velocità 1"),
    State("input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0", "on"),
]

SCENARI: dict[str, tuple[str, list[tuple[Any, ...]]]] = {}


def scenario(nome: str, configurazione: str, *passi: tuple[Any, ...]) -> None:
    SCENARI[nome] = (configurazione, list(passi))


def acceso(entita: str) -> tuple[Any, ...]:
    return ("servizio", "input_boolean.turn_on", {"entity_id": entita})


def spento(entita: str) -> tuple[Any, ...]:
    return ("servizio", "input_boolean.turn_off", {"entity_id": entita})


def script(chiave: str, utente: bool = False, **dati: Any) -> tuple[Any, ...]:
    return ("servizio", f"script.{chiave}", dati, utente)


def attendi(secondi: float) -> tuple[Any, ...]:
    return ("attendi", secondi)


scenario(
    "trigger_modello",
    """
automation:
  - alias: soglia
    triggers:
      - trigger: template
        value_template: >
          {{ states('input_number.vmc_master_aria_scambiata_v1') | float(0) > 10
             or is_state('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0',
                         'off') }}
    actions:
      - action: prova.registra
        data:
          v: "{{ states('input_number.vmc_master_aria_scambiata_v1') }}"
          ctx: "{{ trigger.to_state is defined }}"
  - alias: scrive
    triggers:
      - trigger: state
        entity_id: input_boolean.a
        to: "on"
    actions:
      - action: input_number.set_value
        target:
          entity_id: input_number.vmc_master_aria_scambiata_v1
        data:
          value: >
            {{ states('input_number.vmc_master_aria_scambiata_v1') | float(0) + 3 }}
      - action: input_boolean.turn_off
        target:
          entity_id: input_boolean.a
""",
    acceso("input_boolean.a"),
    attendi(1),
    acceso("input_boolean.a"),
    attendi(1),
    acceso("input_boolean.a"),
    attendi(1),
    acceso("input_boolean.a"),
    attendi(1),
)

scenario(
    "trigger_stato",
    """
automation:
  - alias: rimando
    mode: restart
    triggers:
      - trigger: state
        entity_id: input_text.vmc_master_ultima_scelta_utente
    actions:
      - action: prova.registra
        data:
          da: "{{ trigger.from_state.state }}"
          a: "{{ trigger.to_state.state }}"
          cambiato: "{{ trigger.to_state.last_changed }}"
      - delay: 2
      - action: prova.registra
        data:
          dopo: "{{ states('input_text.vmc_master_ultima_scelta_utente') }}"
  - alias: reset
    triggers:
      - trigger: state
        entity_id: input_text.vmc_master_tempo_mancante_reset
        to: reset
    conditions:
      - condition: state
        entity_id: input_text.vmc_master_tempo_mancante_reset
        state: reset
    actions:
      - action: input_text.set_value
        target:
          entity_id: input_text.vmc_master_tempo_mancante_reset
        data:
          value: ""
      - action: prova.registra
        data:
          reset: "{{ states('input_text.vmc_master_tempo_mancante_reset') }}"
script:
  scegli:
    fields:
      nome: {}
      valore: {}
    sequence:
      - action: input_text.set_value
        target:
          entity_id: "input_text.vmc_master_{{ nome }}"
        data:
          value: "{{ valore }}"
""",
    script("scegli", nome="ultima_scelta_utente", valore="Velocità 2"),
    attendi(1),
    script("scegli", nome="ultima_scelta_utente", valore="Velocità 3"),
    attendi(3),
    script("scegli", nome="ultima_scelta_utente", valore="Velocità 3"),
    script("scegli", nome="tempo_mancante_reset", valore="reset"),
    attendi(1),
    script("scegli", nome="tempo_mancante_reset", valore="altro"),
    attendi(3),
)

scenario(
    "attesa_for",
    """
automation:
  - alias: attesa
    triggers:
      - trigger: state
        entity_id: input_boolean.b
        to: "on"
        for: "{{ states('input_number.vmc_master_attesa_avvisi') | int(32) }}"
    actions:
      - action: prova.registra
        data:
          attesa: "{{ states('input_number.vmc_master_attesa_' ~ 'avvisi') }}"
      - action: input_boolean.turn_off
        target:
          entity_id: input_boolean.b
script:
  imposta:
    fields:
      valore: {}
    sequence:
      - action: input_number.set_value
        target:
          entity_id: input_number.vmc_master_attesa_avvisi
        data:
          value: "{{ valore }}"
""",
    acceso("input_boolean.b"),
    attendi(4),
    script("imposta", valore=6),
    acceso("input_boolean.b"),
    attendi(5),
    spento("input_boolean.b"),
    acceso("input_boolean.b"),
    attendi(7),
)

scenario(
    "attesa_modello",
    """
automation:
  - alias: conto alla rovescia
    mode: queued
    triggers:
      - trigger: state
        entity_id: input_boolean.a
        to: "on"
    actions:
      - repeat:
          for_each: [avvisi, delta_avvio]
          sequence:
            - variables:
                famiglia: "{{ repeat.item }}"
            - action: input_text.set_value
              target:
                entity_id: "input_text.vmc_master_countdown_{{ famiglia }}"
              data:
                value: >
                  {{ states('input_number.vmc_master_attesa_avvisi') | int(0) }}
      - repeat:
          while:
            - condition: template
              value_template: >
                {{ states('input_text.vmc_master_countdown_avvisi') | int(0) > 0 }}
          sequence:
            - delay: 1
            - action: input_text.set_value
              target:
                entity_id: input_text.vmc_master_countdown_avvisi
              data:
                value: >
                  {{ states('input_text.vmc_master_countdown_avvisi') | int(0) - 1 }}
  - alias: aspetta
    triggers:
      - trigger: state
        entity_id: input_boolean.b
        to: "on"
    actions:
      - wait_template: "{{ is_state('input_text.vmc_master_countdown_avvisi', '0') }}"
        timeout: 10
      - action: prova.registra
        data:
          finito: "{{ wait.completed }}"
          da: >
            {{ (now() - states.input_text.vmc_master_countdown_avvisi.last_changed)
               .total_seconds() }}
""",
    acceso("input_boolean.b"),
    acceso("input_boolean.a"),
    attendi(5),
    spento("input_boolean.a"),
    spento("input_boolean.b"),
    acceso("input_boolean.b"),
    attendi(12),
)

scenario(
    "letture",
    """
script:
  leggi:
    sequence:
      - action: prova.registra
        data:
          stato: "{{ states('input_number.vmc_master_attesa_avvisi') }}"
          intero: "{{ states('input_number.vmc_master_attesa_avvisi') | int }}"
          attributo: "{{ state_attr('input_number.vmc_master_attesa_avvisi', 'max') }}"
          unita: >
            {{ states.input_number.vmc_master_attesa_avvisi.attributes
               .unit_of_measurement }}
          nome: "{{ states.input_text.vmc_master_countdown_avvisi.name }}"
          oggetto: "{{ states.input_text.vmc_master_countdown_avvisi.state }}"
          valore: "{{ 'input_text.vmc_master_tempo_mancante_reset' | has_value }}"
          vuoto: "{{ states('input_text.vmc_master_velocita_precedente') == '' }}"
          espansi: >
            {{ expand('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0',
                      'input_boolean.a') | map(attribute='state') | list }}
          spia: "{{ is_state('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0', 'on') }}"
          cambiato: "{{ states.input_number.vmc_master_aria_scambiata_v1.last_changed }}"
          aggiornato: "{{ states.input_number.vmc_master_aria_scambiata_v1.last_updated }}"
          contesto: "{{ states.input_number.vmc_master_aria_scambiata_v1.context.id is string }}"
          dominio: "{{ states.input_number.vmc_master_aria_scambiata_v1.domain }}"
          composto: >
            {{ states('input_text.vmc_master_countdown_' ~ 'avvisi') | float(-1) }}
          filtro: "{{ 'input_number.vmc_master_attesa_avvisi' | has_value }}"
          prova: "{{ 'input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0' is is_state('on') }}"
      - condition: state
        entity_id: input_number.vmc_master_attesa_avvisi
        state: "3.0"
      - action: prova.registra
        data:
          passato: true
      - action: input_number.set_value
        target:
          entity_id: input_number.vmc_master_aria_scambiata_v1
        data:
          value: 4.5
      - action: input_text.set_value
        target:
          entity_id: input_text.vmc_master_countdown_avvisi
        data:
          value: "{{ states('input_text.vmc_master_countdown_avvisi') | int + 1 }}"
""",
    script("leggi"),
    attendi(1),
    script("leggi"),
    attendi(1),
)

scenario(
    "misti",
    """
automation:
  - alias: spie
    triggers:
      - trigger: template
        value_template: >
          {{ is_state('input_boolean.a', 'off')
             and is_state('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0', 'off') }}
    actions:
      - action: prova.registra
        data:
          spie: >
            {{ states('input_boolean.a') }}
            {{ states('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0') }}
script:
  spegni:
    sequence:
      - action: input_boolean.turn_off
        target:
          entity_id:
            - input_boolean.a
            - input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0
            - input_boolean.b
  accendi:
    sequence:
      - action: input_boolean.turn_on
        target:
          entity_id:
            - input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0
            - input_boolean.a
  aggiorna:
    sequence:
      - action: homeassistant.update_entity
        target:
          entity_id:
            - input_select.s
            - input_text.vmc_master_last_temp_external_entity
      - action: prova.registra
        data:
          aggiornato: true
""",
    acceso("input_boolean.a"),
    acceso("input_boolean.b"),
    script("spegni"),
    attendi(1),
    script("accendi"),
    attendi(1),
    script("spegni"),
    script("aggiorna"),
    attendi(1),
)

scenario(
    "piu_bersagli",
    """
automation:
  - alias: somma
    triggers:
      - trigger: template
        value_template: >
          {{ (states('input_number.vmc_master_aria_scambiata_v1') | float(0)
              + states('input_number.vmc_master_aria_scambiata_v2') | float(0)) == 0 }}
    actions:
      - action: prova.registra
        data:
          azzerate: true
script:
  azzera:
    sequence:
      - action: input_number.set_value
        target:
          entity_id:
            - input_number.vmc_master_aria_scambiata_v1
            - input_number.vmc_master_aria_scambiata_v2
            - input_number.vmc_master_aria_scambiata_v3
            - input_number.vmc_master_aria_scambiata_v4
            - input_number.vmc_master_aria_scambiata_iperventilazione
            - input_number.vmc_master_aria_scambiata_notte
            - input_number.vmc_master_aria_scambiata_freecooling
            - input_number.vmc_master_aria_scambiata_ricomincio
        data:
          value: 0
  aumenta:
    variables:
      totale_entity: input_number.vmc_master_aria_scambiata_v2
    sequence:
      - action: input_number.set_value
        data:
          entity_id: "{{ totale_entity }}"
          value: "{{ states(totale_entity) | float(0) + 0.0001 }}"
""",
    script("aumenta"),
    script("azzera"),
    attendi(1),
    script("aumenta"),
    script("aumenta"),
    script("azzera"),
    attendi(1),
)

scenario(
    "errori_e_utenti",
    """
script:
  troppo:
    sequence:
      - action: input_number.set_value
        continue_on_error: true
        target:
          entity_id: input_number.vmc_master_attesa_avvisi
        data:
          value: 301
      - action: prova.registra
        data:
          dopo: true
  lungo:
    sequence:
      - action: input_text.set_value
        target:
          entity_id: input_text.vmc_master_velocita_precedente
        data:
          value: "{{ 'x' * 21 }}"
      - action: prova.registra
        data:
          lungo: "{{ states('input_text.vmc_master_velocita_precedente') }}"
  utente:
    sequence:
      - action: input_number.set_value
        target:
          entity_id: input_number.vmc_master_attesa_avvisi
        data:
          value: 9
      - action: prova.registra
        data:
          utente: "{{ context.user_id is not none }}"
""",
    script("troppo"),
    script("lungo"),
    script("utente", utente=True),
    attendi(1),
)


async def _corsa(
    freezer: FrozenDateTimeFactory,
    nome: str,
    configurazione: dict[str, Any],
    passi: list[tuple[Any, ...]],
    *,
    motore: bool,
    caricati: list[str],
) -> dict[str, Any]:
    freezer.move_to(T0)
    norma = Normalizzatore(T0)
    smistatore = Smistatore(IDS, norma)
    async with async_test_home_assistant() as hass:
        utente = await hass.auth.async_create_user(
            "Utente scheda", group_ids=["system-admin"]
        )
        assert await async_setup_component(hass, "homeassistant", {})
        configurazioni = {d: dict(v) for d, v in ALTRI.items()}
        memoria: MemoriaInterna | None = None
        if motore:
            memoria = MemoriaInterna(hass)
            memoria.ripristina(
                {
                    c: da_stato(c, s.state)
                    for s in RIPRISTINO
                    for c in INTERNI
                    if _entity_id(c) == s.entity_id
                }
            )
        else:
            _ripristina(hass, RIPRISTINO)
            for dominio, voci in _configurazione().items():
                configurazioni.setdefault(dominio, {}).update(voci)
        for dominio, voci in configurazioni.items():
            assert await async_setup_component(hass, dominio, {dominio: voci})

        async def registra(chiamata: ServiceCall) -> None:
            pass

        hass.services.async_register("prova", "registra", registra)
        automazioni = configurazione.get("automation", [])
        script = configurazione.get("script", {})
        if memoria is not None:
            servizi_misti(
                hass,
                memoria,
                [
                    f"input_boolean.{o}"
                    for o in [
                        *ALTRI["input_boolean"],
                        *_configurazione()["input_boolean"],
                    ]
                ],
            )
            testo_modelli, testo_motore = await traduci_configurazione(
                hass,
                automazioni,
                script,
                nome_modelli=f"memoria_{nome}_modelli",
                interni=INTERNI,
            )
            assert "c.memoria_interna(INTERNI)" in testo_motore
            caricati.append(f"{generato.__name__}.memoria_{nome}_modelli")
            caricati.append(f"{generato.__name__}.memoria_{nome}_motore")
            _carica(f"memoria_{nome}_modelli", testo_modelli)
            codice = _carica(f"memoria_{nome}_motore", testo_motore)
            m = MotoreFase3(hass, memoria=memoria)
            await m.avvia(crea=codice.crea)
            memoria.ascolta_cambi(smistatore.cambio)
            memoria.ascolta_chiamate(smistatore.chiamata)
        else:
            assert await async_setup_component(hass, "script", {"script": script})
            assert await async_setup_component(
                hass, "automation", {"automation": automazioni}
            )
        await _gira(hass)

        @callback
        def annota(evento: Any) -> None:
            if evento.event_type in EVENTI:
                smistatore.evento(evento)

        if memoria is None:
            togli = hass.bus.async_listen(MATCH_ALL, annota)
            togli_rapporti = smistatore.ascolta_rapporti(hass)
        else:
            # il motore vede gli eventi del bus nel suo canale (seguire.CambiInterni):
            # il registro li annota lì, nell'ordine in cui il motore li vede
            togli = osserva_nel_canale(hass, EVENTI, annota)
            togli_rapporti = memoria.ascolta_rapporti(smistatore.rapporto)
            # gli stati delle logiche (le automazioni del motore) non sono nella macchina
            # degli stati: entrano nel registro nel punto del canale di state_changed
            smetti = stati_logiche(hass).osserva(
                callback(lambda e: annota(e) if e.event_type == EVENT_STATE_CHANGED else None)
            )
        segnato = smistatore.segna_aggiornamenti(servizi_ha.async_update_entity)
        segna = patch.object(servizi_ha, "async_update_entity", segnato)
        segna.start()
        for passo in passi:
            if passo[0] == "servizio":
                dominio, servizio = passo[1].split(".")
                contesto = Context(
                    user_id=utente.id if len(passo) > 3 and passo[3] else None
                )
                try:
                    await hass.services.async_call(
                        dominio, servizio, passo[2], blocking=True, context=contesto
                    )
                except Exception as err:  # noqa: BLE001
                    smistatore.nota(("errore", type(err).__name__, str(err)))
                await _gira(hass)
            else:
                await _avanza(hass, freezer, passo[1])
        togli()
        togli_rapporti()
        segna.stop()
        if memoria is not None:
            finali = [memoria.stato(e) for e in IDS]
            assert not any(hass.states.get(e) for e in IDS)
        else:
            finali = [hass.states.get(e) for e in IDS]
        esito = {
            "registro": smistatore.registro,
            "interni": smistatore.interni_cambi,
            "chiamate_interne": smistatore.chiamate_interne,
            "rapporti": smistatore.interni_rapporti,
            "sequenza": smistatore.sequenza,
            "finali": [(*norma(s), norma(s.last_updated)) for s in finali],
            "riportati": {s.entity_id: norma(s.last_reported) for s in finali},
            "da_aggiornamento": smistatore.rapporti_da_aggiornamento,
        }
        if memoria is not None:
            smetti()
            # le logiche si fermano (non hanno automation.turn_off)
            await m.ferma()
        else:
            await hass.services.async_call(
                "automation", "turn_off", {"entity_id": "all"}, blocking=True
            )
        await hass.services.async_call(
            "script", "turn_off", {"entity_id": "all"}, blocking=True
        )
        await _gira(hass)
        await hass.async_stop(force=True)
    return esito


def _confrontabile(esito: dict[str, Any]) -> dict[str, Any]:
    """Le voci di una corsa come si confrontano (``nel_canale``): le voci esterne nello
    stesso ordine, quelle interne nel loro ordine (tutte insieme), i contesti rinumerati
    in quell'ordine."""
    sequenza, registro, interni, chiamate, rapporti = rinumera_ovunque(
        ordine_esterno(esito["sequenza"], voce_interna),
        ordine_esterno(esito["registro"], voce_interna),
        esito["interni"],
        esito["chiamate_interne"],
        esito["rapporti"],
    )
    return {
        **esito,
        "sequenza": sequenza,
        "registro": registro,
        "interni": interni,
        "chiamate_interne": chiamate,
        "rapporti": rapporti,
    }


def _differenza(atteso: list[Any], ottenuto: list[Any], cosa: str) -> str | None:
    if atteso == ottenuto:
        return None
    diff = difflib.unified_diff(
        [repr(v) for v in atteso],
        [repr(v) for v in ottenuto],
        "home_assistant",
        "motore",
        lineterm="",
        n=2,
    )
    return f"{cosa} diversi:\n" + "\n".join(list(diff)[:60])


@pytest.mark.parametrize("nome", sorted(SCENARI))
async def test_come_gli_aiutanti(
    nome: str,
    freezer: FrozenDateTimeFactory,
    moduli: list[str],  # noqa: F811
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Stesso registro con Home Assistant e gli aiutanti e con il motore e la memoria
    interna; gli eventi degli aiutanti interni uguali agli annunci della memoria."""
    monkeypatch.setattr(
        "homeassistant.helpers.event.randint", lambda minimo, massimo: minimo
    )
    testo, passi = SCENARI[nome]
    configurazione = yaml.safe_load(testo)
    atteso = await _corsa(
        freezer, nome, configurazione, passi, motore=False, caricati=moduli
    )
    ottenuto = await _corsa(
        freezer, nome, configurazione, passi, motore=True, caricati=moduli
    )
    assert atteso["interni"], "lo scenario deve cambiare valori interni"
    assert any(
        v[1] == "call_service" and v[2]["domain"] == "prova" for v in atteso["registro"]
    )
    # gli eventi che il motore non lancia sul bus (gli stati delle logiche e gli annunci
    # della memoria) possono passare prima di quelli che Home Assistant tiene in coda
    # (nel_canale): stesso ordine per tutto il resto e, tra loro, la stessa sequenza
    atteso, ottenuto = _confrontabile(atteso), _confrontabile(ottenuto)
    for chiave in (
        "registro",
        "interni",
        "chiamate_interne",
        "rapporti",
        "sequenza",
        "finali",
    ):
        if differenza := _differenza(atteso[chiave], ottenuto[chiave], chiave):
            pytest.fail(differenza)
    # homeassistant.update_entity: con gli aiutanti rinnova last_reported dei valori
    # interni (state_reported, nei «rapporti» e nella sequenza), con la memoria lo
    # rinnova il motore (che toglie i valori interni dalla chiamata): stessi rapporti
    assert atteso["riportati"] == ottenuto["riportati"]
    assert not ottenuto["da_aggiornamento"]
    assert len(atteso["da_aggiornamento"]) == (1 if nome == "misti" else 0)


def test_traduzione_senza_interni_invariata() -> None:
    """Senza ``interni`` il codice generato non dichiara la memoria interna (il codice
    di ``generato/`` resta quello di sempre: lo prova test_traduzione.py)."""
    testo = generato.__path__[0] + "/motore.py"  # type: ignore[attr-defined]
    with open(testo, encoding="utf-8") as flusso:
        assert "memoria_interna" not in flusso.read()


async def test_traduzione_rifiuta_servizi_sconosciuti(hass: HomeAssistant) -> None:
    """Con la memoria interna un servizio che il motore non sa fare su un valore
    interno scritto nel bersaglio non si traduce."""
    for azione in (
        {"action": "input_number.increment", "target": {"entity_id": IDS[1]}},
        {
            "action": "input_text.set_value",
            "target": {"entity_id": [IDS[40], "input_text.altro"]},
            "data": {"value": "x"},
        },
        {"action": "homeassistant.update_entity", "target": {"entity_id": IDS[40]}},
        {"action": "homeassistant.turn_off", "target": {"entity_id": IDS[0]}},
    ):
        with pytest.raises(NonTraducibile):
            await traduci_configurazione(
                hass,
                [],
                {"s": {"sequence": [azione]}},
                nome_modelli="rifiuto_modelli",
                interni=INTERNI,
            )
    # senza memoria interna si traducono come sempre
    await traduci_configurazione(
        hass,
        [],
        {
            "s": {
                "sequence": [
                    {
                        "action": "input_number.increment",
                        "target": {"entity_id": IDS[1]},
                    }
                ]
            }
        },
        nome_modelli="rifiuto_modelli",
    )
