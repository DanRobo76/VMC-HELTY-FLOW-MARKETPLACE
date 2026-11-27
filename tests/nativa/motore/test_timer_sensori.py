"""I sensori con l'istante di fine dei timer del motore (``nativa/sensori_timer.py``).

- identità: i 34 sensori hanno l'entity_id della colonna «Domani» di
  ``aiutanti_fase1.csv`` (lo stesso oggetto del timer), il nome e l'icona del timer, la
  classe ``timestamp``;
- stato: l'istante di fine (``finishes_at`` del timer) mentre il timer è attivo,
  ``unknown`` quando è fermo, scritto con il contesto della scrittura del timer;
- righe del registro: un timer «lettura» che finisce e riparte nello stesso istante
  cambia il sensore una volta sola (il nuovo istante di fine); un countdown cambia a
  ogni avvio e a ogni fine;
- i 5 timer «lettura» (la finestra «Prossime letture» della scheda): con
  ``solo_con_la_finestra`` (il valore normale, progetto E) il sensore scrive solo
  mentre l'interruttore della finestra è acceso; all'accensione scrive subito l'istante
  di fine di quel momento (o ``unknown``), da spenta tiene l'ultimo stato scritto. Senza
  (progetto A, «Sempre») scrive sempre;
- StatoVMC riceve lo stato dei due timer letti dal modello Velocità Registrata.
"""

from __future__ import annotations

import csv
from datetime import UTC, datetime, timedelta
from typing import Any

from freezegun.api import FrozenDateTimeFactory
from homeassistant.const import EVENT_STATE_CHANGED
from homeassistant.core import Context, Event, HomeAssistant, callback
from homeassistant.helpers import entity_registry as er

from custom_components.vmc_master.nativa.comandi import InterruttoreVMC
from custom_components.vmc_master.nativa.motore.contesto import Contesto
from custom_components.vmc_master.nativa.motore.timer import (
    TimerDelMotore,
    configurazione_del_package,
)
from custom_components.vmc_master.nativa.sensori_timer import (
    ATTESA_LETTURE,
    CHIAVE_FINESTRA,
    LETTI_DAI_MODELLI,
    SOLO_CON_LA_FINESTRA,
    collega_a_stato,
    crea_sensori_timer,
)
from custom_components.vmc_master.nativa.stato import StatoVMC
from custom_components.vmc_master.nativa.tabelle import IMPOSTAZIONI

from .aiutanti_nativi import aggiungi
from .rinomina import FASE_1
from .test_semantica import _gira
from .test_semantica_tempi import _avanza

T0 = datetime(2026, 11, 25, 10, 0, 0, 300_000, tzinfo=UTC)


FINESTRA = "switch.vmc_master_opzione_finestra_prossime_letture"


async def _avvia(
    hass: HomeAssistant,
    nome: str = "master",
    *,
    solo_con_la_finestra: bool = False,
) -> TimerDelMotore:
    """Timer e sensori della VMC ``nome``; con ``solo_con_la_finestra`` anche
    l'interruttore della finestra «Prossime letture» (spento)."""
    stato = StatoVMC(hass, nome)
    timer = TimerDelMotore(Contesto(hass, nome), configurazione_del_package(nome))
    await timer.prepara()
    entita: list[Any] = crea_sensori_timer(
        timer, stato, solo_con_la_finestra=solo_con_la_finestra
    )
    if solo_con_la_finestra:
        entita.append(InterruttoreVMC(stato, CHIAVE_FINESTRA))
    await aggiungi(hass, entita)
    await _gira(hass)
    return timer


async def _finestra(hass: HomeAssistant, servizio: str) -> Context:
    """La scheda accende o spegne la finestra «Prossime letture»."""
    contesto = Context()
    await hass.services.async_call(
        "switch", servizio, {"entity_id": FINESTRA}, blocking=True, context=contesto
    )
    return contesto


def _cambi(hass: HomeAssistant, entity_id: str) -> list[Event]:
    cambi: list[Event] = []

    @callback
    def annota(evento: Event) -> None:
        if evento.data["entity_id"] == entity_id:
            cambi.append(evento)

    hass.bus.async_listen(EVENT_STATE_CHANGED, annota)
    return cambi


async def test_identita_dei_34_sensori(hass: HomeAssistant) -> None:
    """Entity_id della colonna «Domani», unique_id, nome, icona e classe."""
    with FASE_1.open(encoding="utf-8-sig", newline="") as flusso:
        domani = {
            riga["Entità oggi"]: riga["Domani"]
            for riga in csv.DictReader(flusso, delimiter=";")
            if riga["Tipo oggi"] == "timer"
        }
    assert len(domani) == 34
    timer = await _avvia(hass)
    assert sorted(timer.timer) == sorted(domani)
    registro = er.async_get(hass)
    for vecchio, nuovo in domani.items():
        stato = hass.states.get(nuovo)
        assert stato is not None, nuovo
        assert stato.state == "unknown"
        chiave = "timer." + vecchio.removeprefix("timer.vmc_master_")
        voce = IMPOSTAZIONI[chiave]
        assert stato.attributes == {
            "device_class": "timestamp",
            "friendly_name": voce["name"],
            "icon": voce["icon"],
        }
        entrata = registro.async_get(nuovo)
        assert entrata is not None
        assert entrata.unique_id == nuovo.removeprefix("sensor.")


async def test_altra_vmc(hass: HomeAssistant) -> None:
    """Per un'altra VMC timer e sensori hanno il suo nome."""
    timer = await _avvia(hass, "cucina")
    assert "timer.vmc_cucina_lettura_ping" in timer.timer
    assert hass.states.get("sensor.vmc_cucina_lettura_ping") is not None


async def test_countdown_avvio_fine_annullamento(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory
) -> None:
    """Un countdown: l'istante di fine a ogni avvio, ``unknown`` subito alla fine o
    all'annullamento, con il contesto della chiamata."""
    freezer.move_to(T0)
    timer = await _avvia(hass)
    sensore = "sensor.vmc_master_countdown_avvisi"
    cambi = _cambi(hass, sensore)
    contesto = Context()
    await timer.servizio(
        "start",
        {"duration": 30},
        {"entity_id": "timer.vmc_master_countdown_avvisi"},
        contesto,
    )
    assert hass.states.get(sensore).state == "2026-11-25T10:00:30+00:00"
    assert hass.states.get(sensore).context is contesto
    freezer.tick(timedelta(seconds=10))
    await timer.servizio(
        "start",
        {"duration": 30},
        {"entity_id": "timer.vmc_master_countdown_avvisi"},
        Context(),
    )
    assert hass.states.get(sensore).state == "2026-11-25T10:00:40+00:00"
    annulla = Context()
    await timer.servizio(
        "cancel", {}, {"entity_id": "timer.vmc_master_countdown_avvisi"}, annulla
    )
    assert hass.states.get(sensore).state == "unknown"
    assert hass.states.get(sensore).context is annulla
    await timer.servizio(
        "start",
        {"duration": 2},
        {"entity_id": "timer.vmc_master_countdown_avvisi"},
        Context(),
    )
    await _avanza(hass, freezer, 3)
    assert timer.timer["timer.vmc_master_countdown_avvisi"].state == "idle"
    assert hass.states.get(sensore).state == "unknown"
    assert [e.data["new_state"].state for e in cambi] == [
        "2026-11-25T10:00:30+00:00",
        "2026-11-25T10:00:40+00:00",
        "unknown",
        "2026-11-25T10:00:12+00:00",
        "unknown",
    ]


async def _giri_di_lettura(
    hass: HomeAssistant,
    freezer: FrozenDateTimeFactory,
    timer: TimerDelMotore,
    giri: int,
) -> list[Event]:
    """La Countdown Letture VMC per la ventilazione: alla fine il timer riparte subito
    (5 secondi)."""
    cambi = _cambi(hass, "sensor.vmc_master_lettura_ventilazione")
    finiti = await _lettura_continua(hass, timer)
    await _avanza(hass, freezer, giri * 5, 1)
    assert len(finiti) == giri
    return cambi


async def _lettura_continua(
    hass: HomeAssistant,
    timer: TimerDelMotore,
    entity_id: str = "timer.vmc_master_lettura_ventilazione",
) -> list[Event]:
    """Come la Countdown Letture VMC: avvia il timer (5 secondi) e lo riavvia appena
    finisce. Restituisce gli eventi ``timer.finished``."""
    finiti: list[Event] = []

    @callback
    def finito(evento: Event) -> None:
        if evento.data["entity_id"] == entity_id:
            finiti.append(evento)
            hass.async_create_task(
                timer.servizio(
                    "start",
                    {"duration": "00:00:05"},
                    {"entity_id": entity_id},
                    Context(parent_id=evento.context.id),
                )
            )

    timer.bus.async_listen("timer.finished", finito)
    await timer.servizio(
        "start", {"duration": "00:00:05"}, {"entity_id": entity_id}, Context()
    )
    return finiti


async def test_lettura_una_riga_per_giro(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory
) -> None:
    """Un timer «lettura» che finisce e riparte nello stesso istante: il timer scrive
    due volte per giro, il sensore una sola (il nuovo istante di fine). Progetto A: senza finestra."""
    freezer.move_to(T0)
    timer = await _avvia(hass, solo_con_la_finestra=False)
    scritture: list[Any] = []
    timer.ascolta(
        callback(lambda t: scritture.append(t.state)),
        "timer.vmc_master_lettura_ventilazione",
    )
    cambi = await _giri_di_lettura(hass, freezer, timer, 12)
    assert len(scritture) == 1 + 2 * 12
    assert len(cambi) == 1 + 12
    assert [e.data["new_state"].state for e in cambi][:3] == [
        "2026-11-25T10:00:05+00:00",
        "2026-11-25T10:00:10+00:00",
        "2026-11-25T10:00:15+00:00",
    ]
    timer.ferma()


async def test_lettura_che_non_riparte(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory
) -> None:
    """Un timer «lettura» che finisce e non riparte: ``unknown`` dopo
    ``ATTESA_LETTURE`` secondi, con il contesto della fine; annullato: subito."""
    freezer.move_to(T0)
    timer = await _avvia(hass, solo_con_la_finestra=False)
    entity_id = "timer.vmc_master_lettura_ping"
    sensore = "sensor.vmc_master_lettura_ping"
    await timer.servizio("start", {"duration": 3}, {"entity_id": entity_id}, Context())
    await _avanza(hass, freezer, 3)
    assert timer.timer[entity_id].state == "idle"
    fine = timer.timer[entity_id].stato_ha
    assert hass.states.get(sensore).state == "2026-11-25T10:00:03+00:00"
    # finito alle 10:00:03 (adesso 10:00:03.3): la fine si scrive alle 10:00:04
    await _avanza(hass, freezer, ATTESA_LETTURE / 2)
    assert hass.states.get(sensore).state == "2026-11-25T10:00:03+00:00"
    await _avanza(hass, freezer, ATTESA_LETTURE / 2)
    assert hass.states.get(sensore).state == "unknown"
    assert hass.states.get(sensore).context is fine.context
    await timer.servizio("start", {"duration": 3}, {"entity_id": entity_id}, Context())
    await timer.servizio("cancel", {}, {"entity_id": entity_id}, Context())
    assert hass.states.get(sensore).state == "unknown"


async def test_stato_vmc_riceve_i_timer_letti_dai_modelli(hass: HomeAssistant) -> None:
    """I due timer di annullamento della memoria Free Heating/Cooling arrivano a
    StatoVMC (lo stato), che ricalcola i modelli."""
    timer = TimerDelMotore(Contesto(hass), configurazione_del_package("master"))
    stato = StatoVMC(hass, "master")
    cambi: list[Any] = []
    stato.ascolta(cambi.append)
    smetti = collega_a_stato(timer, stato)
    for chiave in LETTI_DAI_MODELLI:
        assert stato.stato(chiave) == "idle"
    entity_id = "timer.vmc_master_countdown_free_heating_annullamento"
    await timer.servizio("start", {"duration": 60}, {"entity_id": entity_id}, Context())
    assert stato.stato("timer.countdown_free_heating_annullamento") == "active"
    assert cambi[-1]["timer.countdown_free_heating_annullamento"] == ("idle", "active")
    smetti()
    await timer.servizio("cancel", {}, {"entity_id": entity_id}, Context())
    assert stato.stato("timer.countdown_free_heating_annullamento") == "active"


async def test_lettura_solo_con_la_finestra_aperta(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory
) -> None:
    """Progetto E (il valore normale): finestra spenta, nessuna scrittura; accesa,
    subito l'istante di fine di quel momento con il contesto dell'accensione, poi una
    riga per giro; spenta di nuovo, resta l'ultimo stato scritto (non ``unknown``)."""
    freezer.move_to(T0)
    timer = await _avvia(hass, solo_con_la_finestra=True)
    sensore = "sensor.vmc_master_lettura_ventilazione"
    cambi = _cambi(hass, sensore)
    scritture: list[Any] = []
    timer.ascolta(
        callback(lambda t: scritture.append(t.state)),
        "timer.vmc_master_lettura_ventilazione",
    )
    finiti = await _lettura_continua(hass, timer)
    await _avanza(hass, freezer, 12, 1)  # 10:00:12.3, giri alle :05 e :10
    assert len(finiti) == 2
    assert not cambi
    assert hass.states.get(sensore).state == "unknown"
    accesa = await _finestra(hass, "turn_on")
    assert hass.states.get(sensore).state == "2026-11-25T10:00:15+00:00"
    assert hass.states.get(sensore).context is accesa
    await _avanza(hass, freezer, 10, 1)  # giri alle :15 e :20
    assert hass.states.get(sensore).state == "2026-11-25T10:00:25+00:00"
    await _finestra(hass, "turn_off")
    await _avanza(hass, freezer, 10, 1)  # giri alle :25 e :30
    assert hass.states.get(sensore).state == "2026-11-25T10:00:25+00:00"
    accesa = await _finestra(hass, "turn_on")
    assert hass.states.get(sensore).state == "2026-11-25T10:00:35+00:00"
    assert hass.states.get(sensore).context is accesa
    assert len(finiti) == 6
    assert len(scritture) == 1 + 2 * 6
    assert [e.data["new_state"].state for e in cambi] == [
        "2026-11-25T10:00:15+00:00",
        "2026-11-25T10:00:20+00:00",
        "2026-11-25T10:00:25+00:00",
        "2026-11-25T10:00:35+00:00",
    ]
    timer.ferma()


async def test_finestra_accesa_con_il_timer_fermo(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory
) -> None:
    """Il timer si ferma a finestra spenta: il sensore tiene l'istante vecchio; alla
    riaccensione scrive subito ``unknown`` (senza l'attesa di ``ATTESA_LETTURE``)."""
    freezer.move_to(T0)
    timer = await _avvia(hass, solo_con_la_finestra=True)
    entity_id = "timer.vmc_master_lettura_ping"
    sensore = "sensor.vmc_master_lettura_ping"
    await _finestra(hass, "turn_on")
    await timer.servizio("start", {"duration": 3}, {"entity_id": entity_id}, Context())
    assert hass.states.get(sensore).state == "2026-11-25T10:00:03+00:00"
    await _finestra(hass, "turn_off")
    await timer.servizio("cancel", {}, {"entity_id": entity_id}, Context())
    assert hass.states.get(sensore).state == "2026-11-25T10:00:03+00:00"
    accesa = await _finestra(hass, "turn_on")
    assert hass.states.get(sensore).state == "unknown"
    assert hass.states.get(sensore).context is accesa


async def test_finestra_spenta_durante_l_attesa(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory
) -> None:
    """Il timer finisce senza ripartire e la finestra si spegne durante l'attesa: la
    fine non si scrive più."""
    freezer.move_to(T0)
    timer = await _avvia(hass, solo_con_la_finestra=True)
    entity_id = "timer.vmc_master_lettura_ping"
    sensore = "sensor.vmc_master_lettura_ping"
    await _finestra(hass, "turn_on")
    await timer.servizio("start", {"duration": 3}, {"entity_id": entity_id}, Context())
    await _avanza(hass, freezer, 3)
    assert timer.timer[entity_id].state == "idle"
    await _finestra(hass, "turn_off")
    await _avanza(hass, freezer, 2 * ATTESA_LETTURE)
    assert hass.states.get(sensore).state == "2026-11-25T10:00:03+00:00"


async def test_i_countdown_non_guardano_la_finestra(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory
) -> None:
    """La finestra riguarda solo i 5 timer «lettura»: un countdown scrive anche a
    finestra spenta."""
    freezer.move_to(T0)
    timer = await _avvia(hass, solo_con_la_finestra=True)
    assert hass.states.get(FINESTRA).state == "off"
    await timer.servizio(
        "start",
        {"duration": 30},
        {"entity_id": "timer.vmc_master_countdown_avvisi"},
        Context(),
    )
    stato = hass.states.get("sensor.vmc_master_countdown_avvisi")
    assert stato.state == "2026-11-25T10:00:30+00:00"
    timer.ferma()


async def test_progetto_e_e_il_valore_normale(hass: HomeAssistant) -> None:
    """Senza dire nulla i sensori «lettura» seguono la finestra (progetto E); i
    countdown no."""
    stato = StatoVMC(hass, "master")
    timer = TimerDelMotore(Contesto(hass), configurazione_del_package("master"))
    sensori = {s.entity_id: s for s in crea_sensori_timer(timer, stato)}
    assert SOLO_CON_LA_FINESTRA is True
    seguono = sorted(e for e, s in sensori.items() if s.segue_la_finestra)
    assert seguono == [
        "sensor.vmc_master_lettura_ambientali",
        "sensor.vmc_master_lettura_lan",
        "sensor.vmc_master_lettura_nome",
        "sensor.vmc_master_lettura_ping",
        "sensor.vmc_master_lettura_ventilazione",
    ]
    sempre = crea_sensori_timer(timer, stato, solo_con_la_finestra=False)
    assert not any(s.segue_la_finestra for s in sempre)
