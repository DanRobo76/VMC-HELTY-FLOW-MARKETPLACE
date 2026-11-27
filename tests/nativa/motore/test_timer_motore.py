"""I timer del motore come i timer di Home Assistant: prove a confronto.

Ogni prova fa la stessa cosa due volte, con lo stesso orologio fermo: con i timer di Home
Assistant (l'integrazione ``timer`` con la configurazione del YAML) e con i timer del
motore (``motore.timer.TimerDelMotore`` con la stessa configurazione). Il registro deve
essere identico:

- ogni scrittura di un timer: stato, attributi, ``last_changed``/``last_updated``/
  ``last_reported`` all'istante e contesto (per Home Assistant lo stato nella macchina
  degli stati, per il motore lo stato che terrebbe lì, dal suo registro);
- ogni evento dei timer (``timer.started``, ``finished``...) con l'istante, i dati e il
  contesto (per Home Assistant sul suo bus, per il motore sul bus del motore);
- la fine di ogni chiamata ai servizi (o l'errore, con tipo, chiave di traduzione e
  testo);
- dopo ogni passo, le letture dei modelli: ``states``, ``is_state``, ``state_attr`` (anche
  come filtro e come test) di ogni timer, con le varianti ``rounded``/``with_unit`` e in
  maiuscolo.

L'orologio salta da un timer di asyncio al successivo (come ``test_semantica_tempi``),
così ogni ``timer.finished`` si annota all'istante esatto; i timer di asyncio dello stesso
istante escono nell'ordine in cui sono nati (``ordine_dei_timer``).
"""

from __future__ import annotations

import difflib
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

import probatio
import pytest
from freezegun.api import FrozenDateTimeFactory
from homeassistant.const import EVENT_STATE_CHANGED
from homeassistant.core import Context, Event, HomeAssistant, State, callback
from homeassistant.exceptions import HomeAssistantError, TemplateError
from homeassistant.setup import async_setup_component
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import async_test_home_assistant

from custom_components.vmc_master.nativa.motore.contesto import Contesto
from custom_components.vmc_master.nativa.motore.timer import (
    EVENTI_TIMER,
    TimerDelMotore,
    bus_del_motore,
)

from .test_semantica import _gira
from .test_semantica_tempi import (  # noqa: F401
    _avanza,
    _pulisci_timer,
    ordine_dei_timer,
    tempi_casuali,
)

T0 = datetime(2026, 11, 25, 10, 0, 0, 250_000, tzinfo=UTC)

CONFIGURAZIONE: dict[str, Any] = {
    "t1": {"duration": "00:00:05", "name": "Primo", "icon": "mdi:timer-sand"},
    "t2": {"duration": 3},
    "t3": None,
    "t4": {"duration": "00:01:10", "restore": False, "name": "Quarto"},
}
# Niente attributi personalizzati («homeassistant: customize:»): i timer del motore non sono
# entità e non li hanno (il package personalizza solo le icone delle automazioni)
TIMER = [f"timer.{oggetto}" for oggetto in CONFIGURAZIONE]
ATTRIBUTI = (
    "duration",
    "remaining",
    "finishes_at",
    "restore",
    "editable",
    "last_transition",
    "friendly_name",
    "icon",
    "finished_at",
)
UTENTE_SCONOSCIUTO = "0123456789abcdef0123456789abcdef"


def servizio(
    nome: str,
    entita: Any,
    dati: dict[str, Any] | None = None,
    *,
    contesto: str | None = None,
) -> tuple[Any, ...]:
    """Una chiamata a un servizio dei timer (``entita``: entity_id, lista, «all» o None
    per nessun bersaglio); ``contesto``: «utente» per un utente che non esiste."""
    return ("servizio", nome, entita, dict(dati or {}), contesto)


def attendi(secondi: float) -> tuple[Any, ...]:
    return ("attendi", secondi)


PROVE: dict[str, list[tuple[Any, ...]]] = {
    "avvio_pausa_ripresa_fine_naturale": [
        servizio("start", "timer.t1"),
        attendi(2),
        servizio("pause", "timer.t1"),
        attendi(1.3),
        servizio("pause", "timer.t1"),
        servizio("start", "timer.t1"),
        attendi(4),
        # oltre 5 secondi dalla chiamata: la fine scrive con un contesto nuovo
        attendi(3),
        servizio("cancel", "timer.t1"),
        servizio("finish", "timer.t1"),
        servizio("pause", "timer.t1"),
    ],
    "durata_data_e_riavvio": [
        servizio("start", "timer.t2", {"duration": 10.7}),
        attendi(0.4),
        servizio("start", "timer.t2", {"duration": "00:00:04"}),
        attendi(1),
        servizio("start", "timer.t2"),
        attendi(2),
        servizio("finish", "timer.t2"),
        servizio("start", "timer.t2"),
        attendi(1),
        servizio("cancel", "timer.t2"),
        servizio("start", "timer.t2", {"duration": 0}),
        attendi(4),
        servizio("start", "timer.t2", {"duration": {"seconds": 2}}),
        attendi(3),
    ],
    "change": [
        servizio("change", "timer.t1", {"duration": 1}),
        servizio("start", "timer.t1", {"duration": 20}),
        attendi(3),
        servizio("change", "timer.t1", {"duration": 2}),
        servizio("change", "timer.t1", {"duration": 5}),
        servizio("change", "timer.t1", {"duration": -30}),
        servizio("change", "timer.t1", {"duration": "-00:00:04"}),
        attendi(1),
        servizio("pause", "timer.t1"),
        servizio("change", "timer.t1", {"duration": 1}),
        servizio("start", "timer.t1"),
        attendi(30),
        servizio("change", "timer.t1"),
        # di 0 secondi, subito dopo l'avvio: stesso stato e stessi attributi
        servizio("start", "timer.t2", {"duration": 10}),
        servizio("change", "timer.t2", {"duration": 0}),
        # annullato in pausa (nessun timer di asyncio da fermare)
        servizio("pause", "timer.t2"),
        servizio("cancel", "timer.t2"),
    ],
    "durata_zero_e_predefinita": [
        servizio("start", "timer.t3"),
        attendi(1),
        servizio("start", "timer.t3", {"duration": "00:00:00"}),
        attendi(1),
        servizio("start", "timer.t3", {"duration": 2}),
        attendi(1),
        servizio("pause", "timer.t3"),
        servizio("finish", "timer.t3"),
        servizio("start", "timer.t4"),
        attendi(65),
        servizio("cancel", "timer.t4"),
    ],
    "piu_timer_insieme": [
        servizio(
            "start", ["timer.t1", "timer.t2", "timer.t3", "timer.t4"], {"duration": 3}
        ),
        attendi(1),
        servizio("pause", ["timer.t2", "timer.t4"]),
        servizio("start", "all", {"duration": 2}),
        attendi(3),
        servizio("start", ["timer.t1", "timer.t2"]),
        servizio("cancel", "all"),
        servizio("start", "timer.T1"),
        attendi(6),
    ],
    "bersagli_ed_errori": [
        servizio("start", "timer.manca"),
        servizio("start", ["timer.manca", "timer.t2"]),
        servizio("start", None),
        servizio("start", "timer.t1", {"duration": "abc"}),
        servizio("start", "timer.t1", {"durata": 3}),
        servizio("start", "luce.t1"),
        servizio("pause", "timer.t2", {"duration": 3}),
        servizio("cancel", "timer.t2", contesto="utente"),
        servizio("inesistente", "timer.t2"),
        attendi(5),
    ],
    "come_il_package": [
        # Countdown Letture: start con la durata di un modello appena finito il timer;
        # Countdown Attese: start e cancel con il bersaglio di un modello
        servizio("start", "timer.t1", {"duration": "00:00:10"}),
        attendi(10),
        servizio("start", "timer.t1", {"duration": "00:00:10"}),
        attendi(4.5),
        servizio("start", "timer.t1", {"duration": "00:00:05"}),
        attendi(5),
        servizio("start", ["timer.t2"], {"duration": "00:00:40"}),
        attendi(2),
        servizio("cancel", ["timer.t2"]),
        servizio("cancel", ["timer.t2"]),
    ],
}


def _norma(valore: Any, contesti: Callable[[Context], Any]) -> Any:
    """Un valore del registro con gli istanti in secondi da T0 e i contesti come numeri
    d'ordine."""
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
        return {k: _norma(v, contesti) for k, v in sorted(valore.items())}
    if isinstance(valore, (list, tuple)):
        return [_norma(v, contesti) for v in valore]
    return valore


def _errore(err: BaseException) -> tuple[Any, ...]:
    if isinstance(err, HomeAssistantError):
        return (
            type(err).__name__,
            err.translation_key,
            err.translation_placeholders,
            str(err),
        )
    return (type(err).__name__, str(err))


async def _corsa(
    freezer: FrozenDateTimeFactory,
    passi: list[tuple[Any, ...]],
    *,
    motore: bool,
    chiave: Callable[[Any], Any],
) -> list[Any]:
    freezer.move_to(T0)
    registro: list[Any] = []
    async with async_test_home_assistant() as hass:
        numeri: dict[str | None, int] = {}

        def contesti(contesto: Context) -> tuple[int, int | None, str | None]:
            numero = numeri.setdefault(contesto.id, len(numeri))
            genitore = (
                None
                if contesto.parent_id is None
                else numeri.setdefault(contesto.parent_id, len(numeri))
            )
            return (numero, genitore, contesto.user_id)

        def annota(*voce: Any) -> None:
            registro.append(_norma(voce, contesti))

        assert await async_setup_component(hass, "homeassistant", {})
        c = Contesto(hass)
        if motore:
            timer = TimerDelMotore(c, CONFIGURAZIONE)
            await timer.prepara()
            letture = timer
            for tipo in sorted(EVENTI_TIMER):
                bus_del_motore(hass).async_listen(
                    tipo,
                    callback(
                        lambda e: annota(
                            "evento", e.time_fired, e.event_type, e.data, e.context
                        )
                    ),
                )

            def stato(entity_id: str) -> State | None:
                voce = timer._letto(entity_id)
                return None if voce is None else voce.stato_ha

            @callback
            def scritto(t: Any) -> None:
                annota("stato", t.stato_ha)

            timer.ascolta(scritto)

            async def chiama(
                nome: str, dati: dict[str, Any], contesto: Context
            ) -> None:
                await timer.servizio(nome, dati, None, contesto)

        else:
            assert await async_setup_component(hass, "timer", {"timer": CONFIGURAZIONE})
            letture = c  # type: ignore[assignment]

            @callback
            def evento(e: Event) -> None:
                if e.event_type == EVENT_STATE_CHANGED:
                    if e.data["entity_id"].startswith("timer."):
                        annota("stato", e.data["new_state"])
                elif e.event_type in EVENTI_TIMER:
                    annota("evento", e.time_fired, e.event_type, e.data, e.context)

            hass.bus.async_listen("*", evento)

            def stato(entity_id: str) -> State | None:
                return hass.states.get(entity_id)

            async def chiama(
                nome: str, dati: dict[str, Any], contesto: Context
            ) -> None:
                await hass.services.async_call(
                    "timer", nome, dati, blocking=True, context=contesto
                )

        await _gira(hass)
        _pulisci_timer(hass, chiave)
        # lo stato di partenza (la prima scrittura, all'aggiunta)
        for entity_id in TIMER:
            annota("iniziale", stato(entity_id))

        for indice, passo in enumerate(passi):
            if passo[0] == "servizio":
                _, nome, entita, dati, utente = passo
                dati = dict(dati)
                if entita is not None:
                    dati["entity_id"] = entita
                contesto = Context(
                    user_id=UTENTE_SCONOSCIUTO if utente == "utente" else None
                )
                try:
                    await chiama(nome, dati, contesto)
                except (HomeAssistantError, probatio.Invalid) as err:
                    annota("errore", indice, _errore(err))
                else:
                    annota("fine", indice, dt_util.utcnow())
                await _gira(hass)
            else:
                await _avanza(hass, freezer, passo[1])
            # le letture dei modelli dopo ogni passo
            for entity_id in [*TIMER, "timer.T1", "timer.manca"]:
                annota(
                    "letture",
                    entity_id,
                    letture.states(entity_id),
                    letture.states(entity_id, rounded=True),
                    letture.states(entity_id, with_unit=True),
                    letture.is_state(entity_id, "active"),
                    letture.is_state(entity_id, ["paused", "idle"]),
                    letture.test("is_state")(entity_id, "paused"),
                    [letture.state_attr(entity_id, a) for a in ATTRIBUTI],
                    [letture.filtro("state_attr")(entity_id, a) for a in ATTRIBUTI],
                )
        for entity_id in TIMER:
            annota("finale", stato(entity_id))
        await hass.async_stop(force=True)
    return registro


@pytest.mark.usefixtures("tempi_casuali")
@pytest.mark.parametrize("nome", sorted(PROVE))
async def test_timer_del_motore_come_home_assistant(
    nome: str,
    freezer: FrozenDateTimeFactory,
    ordine_dei_timer: Callable[[Any], Any],  # noqa: F811
) -> None:
    """Stesse scritture, stessi eventi, stessi istanti e contesti, stessi errori e stesse
    letture dei modelli con i timer di Home Assistant e con quelli del motore."""
    passi = PROVE[nome]
    atteso = await _corsa(freezer, passi, motore=False, chiave=ordine_dei_timer)
    ottenuto = await _corsa(freezer, passi, motore=True, chiave=ordine_dei_timer)
    tipi = {v[2] for v in atteso if v[0] == "evento"}
    assert tipi, "nessun evento dei timer"
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


async def test_restore_non_previsto(hass: HomeAssistant) -> None:
    """Nessun timer del package chiede ``restore``: i timer del motore lo rifiutano invece
    di ignorarlo."""
    with pytest.raises(ValueError, match="restore"):
        TimerDelMotore(Contesto(hass), {"t": {"duration": 5, "restore": True}})


async def test_states_timer_non_e_un_dominio(hass: HomeAssistant) -> None:
    """``states['timer']`` (il dominio, con una chiave calcolata) non elenca i timer del
    motore: errore, invece dei soli timer rimasti a Home Assistant. Le altre chiavi vanno
    a Home Assistant."""
    c = Contesto(hass)
    timer = TimerDelMotore(c, CONFIGURAZIONE)
    hass.states.async_set("sensor.s", "7")
    with pytest.raises(TemplateError):
        timer.stati["timer"]
    assert timer.stati["sensor.s"].state == "7"
    assert timer.stati["timer.t1"].state == "idle"
    for chiave in (None, 3, ["timer.t1"]):
        assert _esito(lambda: timer.states(chiave)) == _esito(lambda: c.states(chiave))  # noqa: B023
        assert _esito(lambda: timer.stati[chiave]) == _esito(lambda: c.states[chiave])  # noqa: B023
    timer.ferma()


def _esito(funzione: Callable[[], Any]) -> tuple[Any, ...]:
    try:
        return ("valore", funzione())
    except Exception as err:  # noqa: BLE001
        return ("errore", type(err), str(err))
