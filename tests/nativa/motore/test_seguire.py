"""Il proprio tracciamento del motore (``seguire.py``) come quello di Home Assistant.

Ogni prova fa girare gli stessi passi (cambi di stato, tempo che passa, eventi) due volte,
ognuna con un Home Assistant nuovo e lo stesso orologio fermo: una con le funzioni di Home
Assistant (``async_track_state_change_event``, ``async_track_template_result``,
``async_track_same_state``, ``async_track_template``), una con quelle del motore
(``segui_cambi``, ``traccia_modelli``, ``segui_stesso_stato``, ``segui_modello``). Il
registro (chi è stato chiamato, in che ordine, a che istante, con quali argomenti, e i
messaggi nel registro di Home Assistant) deve essere identico.

Per i valori interni la seconda corsa ha gli stessi entity_id come valori di una sorgente
finta (``SorgenteFinta``: come ``MemoriaInterna``, ogni cambio si annuncia sul bus con un
``state_reported`` marchiato e alla consegna va a ``CambiInterni.consegna``), mentre la
prima corsa li ha come entità vere seguite da Home Assistant: i valori interni devono
arrivare come le entità vere.
"""

from __future__ import annotations

import ast
import asyncio
import inspect
import logging
import re
import time
from collections.abc import Awaitable, Callable, Iterable, Iterator
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from freezegun.api import FrozenDateTimeFactory
from homeassistant.const import EVENT_STATE_CHANGED, EVENT_STATE_REPORTED
from homeassistant.core import (
    Context,
    CoreState,
    Event,
    EventOrigin,
    HomeAssistant,
    State,
    callback,
)
from homeassistant.exceptions import TemplateError
from homeassistant.helpers.event import (
    TrackTemplate,
    TrackTemplateResult,
    async_track_same_state,
    async_track_state_change_event,
    async_track_template,
    async_track_template_result,
)
from homeassistant.helpers.template import Template
from homeassistant.helpers.template.render_info import render_info_cv
from homeassistant.util import dt as dt_util
from homeassistant.util.ulid import ulid_at_time
from pytest_homeassistant_custom_component.common import async_test_home_assistant

from custom_components.vmc_master.nativa.motore import seguire
from custom_components.vmc_master.nativa.motore.seguire import (
    CambiInterni,
    cambi_interni,
    segui_cambi,
    segui_modello,
    segui_stesso_stato,
    stato_di,
    traccia_modelli,
)

from .test_semantica import _gira
from .test_semantica_tempi import (  # noqa: F401
    T0,
    _avanza,
    _fino_alla_fine,
    ordine_dei_timer,
    tempi_casuali,
)

pytestmark = pytest.mark.usefixtures("tempi_casuali", "ordine_dei_timer")

HA = SimpleNamespace(
    nome="ha",
    segui=async_track_state_change_event,
    traccia=async_track_template_result,
    stesso=async_track_same_state,
    modello=async_track_template,
)
MIO = SimpleNamespace(
    nome="mio",
    segui=segui_cambi,
    traccia=traccia_modelli,
    stesso=segui_stesso_stato,
    modello=segui_modello,
)

# I registri dei messaggi confrontati: quelli di Home Assistant e quelli del motore che
# li sostituiscono (stessi messaggi, nome del registro a parte).
REGISTRI = (
    "homeassistant.helpers.event",
    "homeassistant.helpers.trigger",
    "homeassistant.components.template.trigger",
    "homeassistant.components.homeassistant.triggers",
    "custom_components.vmc_master.nativa.motore.seguire",
    "custom_components.vmc_master.nativa.motore.attivazioni",
    "custom_components.vmc_master.nativa.motore.timer",
)


# --- la sorgente finta dei valori interni ---------------------------------------------------

MARCHIO = "prova_valore_interno"


class SorgenteFinta:
    """Dei valori interni come quelli di ``MemoriaInterna``: lo ``State`` calcolato come
    ``StateMachine.async_set_internal``, il cambio annunciato sul bus nel punto in cui
    Home Assistant manderebbe ``state_changed`` e consegnato a ``CambiInterni``."""

    def __init__(self, hass: HomeAssistant, entity_ids: Iterable[str]) -> None:
        self.hass = hass
        self._entity_ids = set(entity_ids)
        self._stati: dict[str, State] = {}
        self.annulla = [
            cambi_interni(hass).aggiungi(self),
            hass.bus.async_listen(
                EVENT_STATE_REPORTED,
                self._consegna,
                event_filter=callback(lambda dati: dati.get(MARCHIO, (None,))[0] is self),
            ),
        ]

    def contiene(self, entity_id: str) -> bool:
        return entity_id in self._entity_ids

    def stato(self, entity_id: str) -> State | None:
        return self._stati.get(entity_id)

    @callback
    def imposta(
        self,
        entity_id: str,
        nuovo: str,
        attributi: dict[str, Any] | None = None,
        contesto: Context | None = None,
    ) -> None:
        attributi = attributi or {}
        timestamp = time.time()
        vecchio = self._stati.get(entity_id)
        stesso_stato = vecchio is not None and vecchio.state == nuovo
        stessi_attributi = vecchio is not None and vecchio.attributes == attributi
        if contesto is None:
            contesto = Context(id=ulid_at_time(timestamp))
        if stesso_stato and stessi_attributi:
            return
        if stessi_attributi:
            assert vecchio is not None
            attributi = vecchio.attributes  # type: ignore[assignment]
        adesso = dt_util.utc_from_timestamp(timestamp)
        stato = State(
            entity_id,
            nuovo,
            attributi,
            vecchio.last_changed if stesso_stato and vecchio is not None else None,
            adesso,
            adesso,
            contesto,
            vecchio is None,
            None,
            timestamp,
        )
        self._stati[entity_id] = stato
        self.hass.bus.async_fire_internal(
            EVENT_STATE_REPORTED,
            {"entity_id": "", MARCHIO: (self, entity_id, vecchio, stato)},
            context=contesto,
            time_fired=timestamp,
        )

    @callback
    def _consegna(self, evento: Event[Any]) -> None:
        _, entity_id, vecchio, nuovo = evento.data[MARCHIO]
        cambio: Event[Any] = Event(
            EVENT_STATE_CHANGED,
            {"entity_id": entity_id, "old_state": vecchio, "new_state": nuovo},
            EventOrigin.local,
            evento.time_fired_timestamp,
            evento.context,
        )
        cambi_interni(self.hass).consegna(cambio)


class ModelloProva(Template):
    """Un modello scritto in Python che legge gli stati con ``stato_di`` (entità vere o
    valori interni) e annota le letture nel ``RenderInfo``, come i modelli del motore
    (``ModelloHA`` con la memoria interna)."""

    def __init__(
        self,
        hass: HomeAssistant,
        testo: str,
        funzione: Callable[[Callable[[str], str], dict[str, Any]], str],
    ) -> None:
        super().__init__(testo, hass)
        self.is_static = False
        self.funzione = funzione

    def ensure_valid(self) -> None:
        """Già valido."""

    def async_render(  # type: ignore[override]
        self,
        variables: Any = None,
        parse_result: bool = True,
        limited: bool = False,
        strict: bool = False,
        log_fn: Any = None,
        **kwargs: Any,
    ) -> Any:
        hass = self.hass
        assert hass is not None

        def leggi(entity_id: str) -> str:
            if (info := render_info_cv.get()) is not None and info.collecting:
                info.entities.add(entity_id)  # type: ignore[attr-defined]
            stato = stato_di(hass, entity_id)
            return stato.state if stato is not None else "unknown"

        try:
            return self.funzione(leggi, dict(variables or {}))
        except Exception as err:
            raise TemplateError(err) from err


# --- il banco -------------------------------------------------------------------------------


class _Messaggi(logging.Handler):
    """I messaggi dei registri confrontati, nel registro della corsa."""

    def __init__(self, annota: Callable[..., None]) -> None:
        super().__init__(logging.INFO)
        self.annota = annota

    def emit(self, record: logging.LogRecord) -> None:
        if not record.name.startswith(REGISTRI):
            return
        errore = record.exc_info[1] if record.exc_info else None
        self.annota(
            "messaggio",
            record.levelname,
            # gli indirizzi degli oggetti (funzioni nate in ogni corsa) non contano
            re.sub(r" at 0x[0-9a-f]+", " at 0x", record.getMessage()),
            None if errore is None else (type(errore).__name__, str(errore)),
        )


@dataclass
class Banco:
    """Quello che una prova usa in una corsa."""

    hass: HomeAssistant
    F: SimpleNamespace
    registro: list[Any]
    inizio: datetime
    fonte: SorgenteFinta | None
    oggetti: dict[str, Any] = field(default_factory=dict)
    contesti: dict[str | None, int | None] = field(default_factory=lambda: {None: None})

    @property
    def mio(self) -> bool:
        return self.F.nome == "mio"

    def istante(self) -> float:
        return round((dt_util.utcnow() - self.inizio).total_seconds(), 6)

    def contesto(self, identificativo: str | None) -> int | None:
        return self.contesti.setdefault(identificativo, len(self.contesti) - 1)

    def norma(self, valore: Any) -> Any:
        """Un valore confrontabile tra le due corse (contesti come numeri d'ordine)."""
        if isinstance(valore, State):
            return (
                "State",
                valore.entity_id,
                valore.state,
                self.norma(dict(valore.attributes)),
                self.norma(valore.last_changed),
                self.norma(valore.last_updated),
                self.contesto(valore.context.id),
                self.contesto(valore.context.parent_id),
            )
        if isinstance(valore, Event):
            return (
                "Event",
                valore.event_type,
                self.norma(dict(valore.data)),
                self.norma(valore.time_fired),
                self.contesto(valore.context.id),
            )
        if isinstance(valore, Context):
            return ("Context", self.contesto(valore.id))
        if isinstance(valore, datetime):
            return ("datetime", valore.isoformat())
        if isinstance(valore, timedelta):
            return ("timedelta", valore.total_seconds())
        if isinstance(valore, Template):
            return ("Template", valore.template)
        if isinstance(valore, TemplateError):
            return ("TemplateError", str(valore))
        if isinstance(valore, TrackTemplateResult):
            return (
                "TrackTemplateResult",
                self.norma(valore.template),
                self.norma(valore.last_result),
                self.norma(valore.result),
            )
        if isinstance(valore, dict):
            return {
                str(k): self.norma(v)
                for k, v in sorted(valore.items(), key=lambda kv: str(kv[0]))
            }
        if isinstance(valore, (set, frozenset)):
            return sorted(self.norma(v) for v in valore)
        if isinstance(valore, (list, tuple)):
            return [self.norma(v) for v in valore]
        return valore

    def annota(self, etichetta: str, *dati: Any) -> None:
        self.registro.append((self.istante(), etichetta, self.norma(list(dati))))

    @callback
    def scrivi(
        self,
        entity_id: str,
        stato: str,
        attributi: dict[str, Any] | None = None,
        contesto: Context | None = None,
    ) -> None:
        """Un cambio di stato: di un valore interno se la sorgente finta lo ha, altrimenti
        di un'entità vera."""
        if self.fonte is not None and self.fonte.contiene(entity_id):
            self.fonte.imposta(entity_id, stato, attributi, contesto)
        else:
            self.hass.states.async_set(entity_id, stato, attributi, context=contesto)


Prepara = Callable[[Banco], Awaitable[None]]


async def corsa(
    freezer: FrozenDateTimeFactory,
    F: SimpleNamespace,
    prepara: Prepara,
    passi: list[tuple[Any, ...]],
    *,
    interni: Iterable[str] = (),
    iniziali: Iterable[tuple[Any, ...]] = (),
    inizio: datetime = T0,
    avvio: bool = False,
) -> list[Any]:
    """Una corsa: un Home Assistant nuovo, gli stati ``iniziali``, ``prepara`` (che
    aggancia chi segue), poi i ``passi``. Con ``interni`` (solo nella corsa del motore)
    quegli entity_id sono valori interni della sorgente finta."""
    freezer.move_to(inizio)
    registro: list[Any] = []
    stato_iniziale = CoreState.not_running if avvio else CoreState.running
    radice = logging.getLogger()
    messaggi: _Messaggi | None = None
    try:
        async with async_test_home_assistant(initial_state=stato_iniziale) as hass:
            fonte = SorgenteFinta(hass, interni) if interni else None
            banco = Banco(hass, F, registro, inizio, fonte)
            messaggi = _Messaggi(banco.annota)
            radice.addHandler(messaggi)
            for iniziale in iniziali:
                banco.scrivi(*iniziale)
            await _gira(hass)
            await prepara(banco)
            await _gira(hass)
            fermato = False
            for passo in passi:
                fermato = await _passo(banco, freezer, passo) or fermato
            await _gira(hass)
            registro.append((banco.istante(), "fine"))
            if not fermato:
                await hass.async_stop(force=True)
            for maniglia in hass.loop._scheduled:
                maniglia.cancel()
    finally:
        if messaggi is not None:
            radice.removeHandler(messaggi)
    return registro


async def _passo(
    banco: Banco, freezer: FrozenDateTimeFactory, passo: tuple[Any, ...]
) -> bool:
    """Un passo; vero se ha fermato Home Assistant."""
    hass = banco.hass
    tipo = passo[0]
    fermato = False
    if tipo == "stato":
        banco.scrivi(*passo[1:])
    elif tipo == "togli":
        hass.states.async_remove(passo[1])
    elif tipo == "attendi":
        await _avanza(hass, freezer, passo[1])
    elif tipo == "evento":
        dati = passo[2] if len(passo) > 2 else None
        hass.bus.async_fire(passo[1], dati, context=passo[3] if len(passo) > 3 else None)
    elif tipo == "chiama":
        if inspect.isawaitable(risultato := passo[1](banco)):
            await risultato
    elif tipo == "avvia":
        avvio = asyncio.ensure_future(hass.async_start())
        await _fino_alla_fine(hass, freezer, avvio)
        banco.registro.append((banco.istante(), "avviato"))
    elif tipo == "ferma":
        fermata = asyncio.ensure_future(hass.async_stop())
        await _fino_alla_fine(hass, freezer, fermata)
        banco.registro.append((banco.istante(), "fermato"))
        fermato = True
    else:
        raise ValueError(passo)
    await _gira(hass)
    return fermato


def confronta(atteso: list[Any], ottenuto: list[Any]) -> None:
    """I due registri uguali (con le righe diverse in vista se non lo sono)."""
    if atteso != ottenuto:
        import difflib

        righe = difflib.unified_diff(
            [repr(r) for r in atteso],
            [repr(r) for r in ottenuto],
            "home assistant",
            "motore",
            lineterm="",
        )
        pytest.fail("registri diversi:\n" + "\n".join(righe))


async def come_home_assistant(
    freezer: FrozenDateTimeFactory,
    prepara: Prepara,
    passi: list[tuple[Any, ...]],
    *,
    interni: Iterable[str] = (),
    **argomenti: Any,
) -> list[Any]:
    """Le due corse e il confronto; restituisce il registro (per guardarci dentro)."""
    atteso = await corsa(freezer, HA, prepara, passi, **argomenti)
    ottenuto = await corsa(freezer, MIO, prepara, passi, interni=interni, **argomenti)
    confronta(atteso, ottenuto)
    return atteso


def etichette(registro: list[Any], etichetta: str) -> list[Any]:
    return [riga for riga in registro if riga[1] == etichetta]


# --- segui_cambi ----------------------------------------------------------------------------


async def _prepara_seguaci(b: Banco) -> None:
    hass, F = b.hass, b.F

    def seguace(nome: str) -> Callable[[Event[Any]], None]:
        @callback
        def segui(evento: Event[Any]) -> None:
            dati = evento.data
            b.annota(
                nome,
                dati["entity_id"],
                dati["old_state"],
                dati["new_state"],
                evento.context,
                evento.time_fired,
            )

        return segui

    b.oggetti["togli_b"] = F.segui(hass, "sensor.a", seguace("b"))
    F.segui(hass, ["sensor.a", "sensor.b"], seguace("c"))
    F.segui(hass, ["Sensor.A"], seguace("maiuscolo"))

    @callback
    def errore(evento: Event[Any]) -> None:
        raise ValueError("errore voluto")

    F.segui(hass, "sensor.b", errore)
    F.segui(hass, "sensor.b", seguace("dopo_errore"))

    @callback
    def annidato(evento: Event[Any]) -> None:
        nuovo = evento.data["new_state"]
        if nuovo is not None and nuovo.state == "2":
            b.scrivi("sensor.b", "da_a")
        b.annota("annidato", evento.data["entity_id"])

    F.segui(hass, "sensor.a", annidato)
    F.segui(hass, ("sensor.a", "sensor.a"), seguace("due_volte"))

    async def asincrono(evento: Event[Any]) -> None:
        b.annota("asincrono_inizio", evento.data["entity_id"])
        await asyncio.sleep(0)
        b.annota("asincrono_fine", evento.data["entity_id"])

    F.segui(hass, "sensor.a", asincrono)
    F.segui(hass, [], seguace("vuoto"))
    F.segui(hass, ["sensor.c", "sensor.a"], seguace("ultimo"))


PASSI_SEGUACI: list[tuple[Any, ...]] = [
    ("stato", "sensor.a", "1"),
    ("stato", "sensor.b", "1", {"x": 1}),
    ("stato", "sensor.a", "1", {"y": 2}),
    ("stato", "sensor.a", "1", {"y": 2}),
    ("stato", "sensor.a", "2"),
    ("chiama", lambda b: b.oggetti.pop("togli_b")()),
    ("stato", "sensor.c", "1"),
    ("attendi", 1.5),
    ("stato", "sensor.a", "3", None, Context(id="contesto_dato")),
]


async def test_segui_cambi_entita_vere(freezer: FrozenDateTimeFactory) -> None:
    """Stessi seguaci chiamati nello stesso ordine (iscrizioni, entity_id ripetuti, in
    maiuscolo, un seguace che sbaglia, uno che cambia un'altra entità, uno asincrono, uno
    tolto) con gli stessi eventi e gli stessi messaggi nel registro."""
    registro = await come_home_assistant(
        freezer,
        _prepara_seguaci,
        [*PASSI_SEGUACI, ("togli", "sensor.a")],
    )
    nomi = [riga[1] for riga in registro if riga[0] == 0 and riga[2][0] == "sensor.a"]
    assert nomi[:6] == ["b", "c", "maiuscolo", "annidato", "due_volte", "due_volte"]
    assert etichette(registro, "messaggio")


async def test_segui_cambi_valori_interni(freezer: FrozenDateTimeFactory) -> None:
    """Gli stessi seguaci su valori interni (``sensor.a`` e ``sensor.b`` della sorgente
    finta, ``sensor.c`` entità vera) ricevono i cambi come da entità vere seguite da Home
    Assistant: stesso ordine, stessi istanti, stessi eventi, stessi messaggi."""
    await come_home_assistant(
        freezer,
        _prepara_seguaci,
        PASSI_SEGUACI,
        interni=("sensor.a", "sensor.b"),
    )


async def test_cambi_interni_regole(hass: HomeAssistant) -> None:
    """``CambiInterni``: uno per ``hass``; un entity_id è interno solo se una sorgente lo
    ha; chi segue un valore interno non passa da Home Assistant; ``stato_di``."""
    interni = cambi_interni(hass)
    assert cambi_interni(hass) is interni
    assert isinstance(interni, CambiInterni)
    fonte = SorgenteFinta(hass, ["input_number.x"])
    assert interni.contiene("input_number.x")
    assert not interni.contiene("input_number.y")
    assert interni.stato("input_number.x") is None
    fonte.imposta("input_number.x", "5.0")
    hass.states.async_set("input_number.y", "1")
    assert stato_di(hass, "input_number.x").state == "5.0"  # type: ignore[union-attr]
    assert stato_di(hass, "INPUT_NUMBER.X").state == "5.0"  # type: ignore[union-attr]
    assert stato_di(hass, "input_number.y").state == "1"  # type: ignore[union-attr]
    assert stato_di(hass, "input_number.z") is None
    visti: list[str] = []
    togli = segui_cambi(
        hass, ["input_number.x", "input_number.y"], lambda e: visti.append(e.data["entity_id"])
    )
    hass.states.async_set("input_number.x", "9")  # un'entità vera con lo stesso nome
    fonte.imposta("input_number.x", "6.0")
    hass.states.async_set("input_number.y", "2")
    await hass.async_block_till_done()
    assert visti == ["input_number.x", "input_number.y"]
    togli()
    fonte.imposta("input_number.x", "7.0")
    await hass.async_block_till_done()
    assert visti == ["input_number.x", "input_number.y"]
    for annulla in fonte.annulla:
        annulla()
    assert not interni.contiene("input_number.x")


# --- traccia_modelli ------------------------------------------------------------------------


def _azione_modelli(b: Banco, nome: str) -> Callable[..., None]:
    @callback
    def azione(evento: Event[Any] | None, risultati: list[TrackTemplateResult]) -> None:
        b.annota(nome, evento, risultati)

    return azione


def _ascolta(b: Banco, nome: str) -> None:
    b.annota(f"ascolta {nome}", b.oggetti[nome].listeners)


async def _prepara_modelli(b: Banco) -> None:
    hass, F = b.hass, b.F

    def T(testo: str) -> Template:
        return Template(testo, hass)

    b.oggetti["semplici"] = F.traccia(
        hass,
        [
            TrackTemplate(T("{{ states('sensor.a') }}"), None),
            TrackTemplate(
                T("{{ is_state('sensor.b', 'on') and states('sensor.a') | int(0) > 1 }}"),
                None,
            ),
            TrackTemplate(T("{{ x }} {{ states('sensor.c') }}"), {"x": "variabile"}),
        ],
        _azione_modelli(b, "semplici"),
    )
    b.oggetti["dominio"] = F.traccia(
        hass,
        [TrackTemplate(T("{{ states.sensor | count }}"), None)],
        _azione_modelli(b, "dominio"),
    )
    b.oggetti["tutti"] = F.traccia(
        hass,
        [TrackTemplate(T("{{ states | count }}"), None)],
        _azione_modelli(b, "tutti"),
    )
    b.oggetti["limite"] = F.traccia(
        hass,
        [TrackTemplate(T("{{ states.binary_sensor | count }}"), None, rate_limit=5)],
        _azione_modelli(b, "limite"),
    )
    b.oggetti["ora"] = F.traccia(
        hass,
        [TrackTemplate(T("{{ now().minute }} {{ states('sensor.a') }}"), None)],
        _azione_modelli(b, "ora"),
    )
    b.oggetti["errore"] = F.traccia(
        hass,
        [TrackTemplate(T("{{ states('sensor.a') | int }}"), None)],
        _azione_modelli(b, "errore"),
    )

    def registro(livello: int, messaggio: str) -> None:
        b.annota("log_fn", livello, messaggio)

    b.oggetti["severo"] = F.traccia(
        hass,
        [TrackTemplate(T("{{ non_definita }} {{ states('sensor.a') }}"), None)],
        _azione_modelli(b, "severo"),
        strict=True,
        log_fn=registro,
    )
    b.oggetti["super"] = F.traccia(
        hass,
        [
            TrackTemplate(T("{{ is_state('switch.s', 'on') }}"), None),
            TrackTemplate(T("{{ states('sensor.b') }}"), None),
            TrackTemplate(T("{{ states('sensor.c') }}-super"), None),
        ],
        _azione_modelli(b, "super"),
        has_super_template=True,
    )
    _ascolta_tutti(b)


def _ascolta_tutti(b: Banco) -> None:
    for nome in ("semplici", "dominio", "tutti", "limite", "ora", "errore", "super"):
        if nome in b.oggetti:
            _ascolta(b, nome)


PASSI_MODELLI: list[tuple[Any, ...]] = [
    ("stato", "sensor.a", "1"),
    ("stato", "sensor.b", "on"),
    ("stato", "sensor.a", "2"),
    ("chiama", _ascolta_tutti),
    ("stato", "sensor.c", "nuovo"),
    ("stato", "binary_sensor.uno", "on"),
    ("attendi", 0.4),
    ("stato", "sensor.d", "altro"),
    ("stato", "binary_sensor.due", "off"),
    ("chiama", _ascolta_tutti),
    ("attendi", 1.0),
    ("togli", "sensor.d"),
    ("stato", "sensor.a", "testo"),
    ("stato", "switch.s", "on"),
    ("stato", "sensor.b", "off"),
    ("stato", "switch.s", "off"),
    ("stato", "sensor.c", "ignorato"),
    ("chiama", _ascolta_tutti),
    ("attendi", 6),
    ("chiama", lambda b: b.oggetti["semplici"].async_refresh()),
    ("chiama", lambda b: b.oggetti["super"].async_refresh()),
    ("attendi", 60),
    ("chiama", lambda b: b.oggetti.pop("dominio").async_remove()),
    ("stato", "sensor.e", "1"),
    ("stato", "sensor.a", "3"),
    ("chiama", _ascolta_tutti),
    ("attendi", 61),
]


async def test_traccia_modelli_entita_vere(freezer: FrozenDateTimeFactory) -> None:
    """``traccia_modelli`` come ``async_track_template_result``: primi risultati, cambi,
    domini e tutti gli stati con i loro limiti (1 s, 60 s, ``rate_limit``), ``now()``
    ogni minuto, errori (anche con ``strict`` e ``log_fn``), il modello «super», il
    ricalcolo a mano, la rimozione, e gli ascoltatori (``listeners``) a ogni passo."""
    registro = await come_home_assistant(
        freezer,
        _prepara_modelli,
        PASSI_MODELLI,
        iniziali=[("sensor.x", "0"), ("binary_sensor.zero", "off")],
    )
    assert etichette(registro, "limite")
    assert etichette(registro, "ora")


def _modelli_interni(b: Banco) -> None:
    hass, F = b.hass, b.F

    def somma(leggi: Callable[[str], str], V: dict[str, Any]) -> str:
        try:
            return str(int(leggi("input_number.a")) + int(leggi("input_number.b")))
        except ValueError:
            return "nessuna"

    def acceso(leggi: Callable[[str], str], V: dict[str, Any]) -> str:
        return str(leggi("input_boolean.c") == "on")

    def scelta(leggi: Callable[[str], str], V: dict[str, Any]) -> str:
        if leggi("input_boolean.c") == "on":
            return leggi("input_number.a")
        return leggi("sensor.vero")

    b.oggetti["interni"] = F.traccia(
        hass,
        [
            TrackTemplate(ModelloProva(hass, "somma", somma), None),
            TrackTemplate(ModelloProva(hass, "scelta", scelta), None),
        ],
        _azione_modelli(b, "interni"),
    )
    b.oggetti["super_interni"] = F.traccia(
        hass,
        [
            TrackTemplate(ModelloProva(hass, "acceso", acceso), None),
            TrackTemplate(ModelloProva(hass, "somma2", somma), None),
        ],
        _azione_modelli(b, "super_interni"),
        has_super_template=True,
    )


async def _prepara_modelli_interni(b: Banco) -> None:
    _modelli_interni(b)
    _ascolta(b, "interni")


async def test_traccia_modelli_valori_interni(freezer: FrozenDateTimeFactory) -> None:
    """Modelli che leggono valori interni (annotati nel ``RenderInfo`` come fanno i modelli
    del motore) si ricalcolano ai loro cambi come con entità vere, anche quando le letture
    cambiano (entità vera al posto di un valore interno e viceversa)."""
    await come_home_assistant(
        freezer,
        _prepara_modelli_interni,
        [
            ("stato", "input_number.a", "1"),
            ("stato", "input_number.b", "2"),
            ("stato", "sensor.vero", "v1"),
            ("stato", "input_boolean.c", "on"),
            ("chiama", lambda b: _ascolta(b, "interni")),
            ("stato", "sensor.vero", "v2"),
            ("stato", "input_number.a", "5"),
            ("stato", "input_boolean.c", "off"),
            ("chiama", lambda b: _ascolta(b, "interni")),
            ("stato", "input_number.a", "6"),
            ("stato", "input_number.b", "x"),
            ("attendi", 2),
            ("stato", "input_boolean.c", "on"),
            ("stato", "input_number.b", "3"),
        ],
        interni=("input_number.a", "input_number.b", "input_boolean.c"),
        iniziali=[
            ("input_number.a", "0"),
            ("input_number.b", "0"),
            ("input_boolean.c", "off"),
        ],
    )


# --- segui_stesso_stato ---------------------------------------------------------------------


async def _prepara_stesso_stato(b: Banco) -> None:
    hass, F = b.hass, b.F

    @callback
    def acceso(entity_id: str, vecchio: State | None, nuovo: State | None) -> bool:
        b.annota("controllo", entity_id, vecchio, nuovo)
        return nuovo is not None and nuovo.state == "on"

    def azione(nome: str) -> Callable[[], None]:
        @callback
        def fai() -> None:
            b.annota(nome)

        return fai

    F.stesso(hass, timedelta(seconds=5), azione("cinque"), acceso, entity_ids="sensor.a")
    F.stesso(
        hass,
        timedelta(seconds=3),
        azione("tre"),
        acceso,
        entity_ids=["sensor.a", "sensor.b"],
    )

    def dopo(b: Banco) -> None:
        b.oggetti["togli"] = F.stesso(
            hass, timedelta(seconds=4), azione("quattro"), acceso, entity_ids="sensor.b"
        )
        F.stesso(
            hass,
            timedelta(seconds=2.5),
            azione("annullato"),
            acceso,
            entity_ids=["sensor.b"],
        )

    b.oggetti["dopo"] = dopo


PASSI_STESSO_STATO: list[tuple[Any, ...]] = [
    ("attendi", 1),
    ("stato", "sensor.b", "on", {"x": 1}),
    ("attendi", 1),
    ("stato", "sensor.a", "on", {"y": 2}),
    ("attendi", 2.5),
    ("chiama", lambda b: b.oggetti["dopo"](b)),
    ("attendi", 1),
    ("stato", "sensor.b", "off"),
    ("attendi", 6),
]


async def test_stesso_stato_entita_vere(freezer: FrozenDateTimeFactory) -> None:
    """``segui_stesso_stato`` come ``async_track_same_state``: scatta dopo il periodo se
    il controllo regge, un cambio che non regge lo annulla."""
    registro = await come_home_assistant(
        freezer,
        _prepara_stesso_stato,
        PASSI_STESSO_STATO,
        iniziali=[("sensor.a", "on"), ("sensor.b", "on")],
    )
    assert [r[1] for r in registro if r[1] in ("cinque", "tre", "quattro")] == [
        "tre",
        "cinque",
    ]


async def test_stesso_stato_valori_interni(freezer: FrozenDateTimeFactory) -> None:
    """Lo stesso con ``sensor.a`` valore interno."""
    await come_home_assistant(
        freezer,
        _prepara_stesso_stato,
        PASSI_STESSO_STATO,
        interni=("sensor.a",),
        iniziali=[("sensor.a", "on"), ("sensor.b", "on")],
    )


# --- segui_modello (le attese) --------------------------------------------------------------


def _attese(b: Banco, crea: Callable[[str], Template]) -> None:
    hass, F = b.hass, b.F

    def azione(nome: str) -> Callable[..., None]:
        @callback
        def fai(entity_id: Any, vecchio: Any, nuovo: Any) -> None:
            b.annota(nome, entity_id, vecchio, nuovo)

        return fai

    b.oggetti["acceso"] = F.modello(hass, crea("acceso"), azione("acceso"))
    F.modello(hass, crea("acceso"), azione("acceso_bis"))
    F.modello(hass, crea("numero"), azione("numero"), {"soglia": 3})


async def _prepara_attese_vere(b: Banco) -> None:
    testi = {
        "acceso": "{{ is_state('sensor.a', 'on') }}",
        "numero": "{{ states('sensor.n') | int > soglia }}",
    }
    _attese(b, lambda nome: Template(testi[nome], b.hass))


def _crea_attese_interne(b: Banco) -> Callable[[str], Template]:
    def acceso(leggi: Callable[[str], str], V: dict[str, Any]) -> str:
        return str(leggi("sensor.a") == "on")

    def numero(leggi: Callable[[str], str], V: dict[str, Any]) -> str:
        return str(int(leggi("sensor.n")) > V["soglia"])

    funzioni = {"acceso": acceso, "numero": numero}
    return lambda nome: ModelloProva(b.hass, nome, funzioni[nome])


async def _prepara_attese_interne(b: Banco) -> None:
    _attese(b, _crea_attese_interne(b))


PASSI_ATTESE: list[tuple[Any, ...]] = [
    ("stato", "sensor.a", "on"),
    ("stato", "sensor.a", "on", {"x": 1}),
    ("stato", "sensor.n", "2"),
    ("stato", "sensor.n", "testo"),
    ("stato", "sensor.n", "5"),
    ("stato", "sensor.a", "off"),
    ("attendi", 1),
    ("chiama", lambda b: b.oggetti.pop("acceso")()),
    ("stato", "sensor.a", "on"),
    ("stato", "sensor.n", "1"),
    ("stato", "sensor.n", "9"),
]


async def test_attese_entita_vere(freezer: FrozenDateTimeFactory) -> None:
    """``segui_modello`` come ``async_track_template`` (le attese ``wait_template``)."""
    await come_home_assistant(
        freezer,
        _prepara_attese_vere,
        PASSI_ATTESE,
        iniziali=[("sensor.a", "off"), ("sensor.n", "0")],
    )


async def test_attese_valori_interni(freezer: FrozenDateTimeFactory) -> None:
    """Le stesse attese con modelli che leggono valori interni: con il motore sono valori
    della sorgente finta, con Home Assistant entità vere."""
    atteso = await corsa(
        freezer,
        HA,
        _prepara_attese_interne,
        PASSI_ATTESE,
        iniziali=[("sensor.a", "off"), ("sensor.n", "0")],
    )
    ottenuto = await corsa(
        freezer,
        MIO,
        _prepara_attese_interne,
        PASSI_ATTESE,
        interni=("sensor.a", "sensor.n"),
        iniziali=[("sensor.a", "off"), ("sensor.n", "0")],
    )
    confronta(atteso, ottenuto)
    assert [r[1] for r in atteso if r[1].startswith("acceso")] == [
        "acceso",
        "acceso_bis",
        "acceso_bis",
    ]


# --- niente nomi privati di Home Assistant --------------------------------------------------

MODULI_PROPRI = (
    Path(seguire.__file__),
    Path(seguire.__file__).with_name("attivazioni.py"),
)


def _nomi_privati(percorso: Path) -> Iterator[str]:
    """I nomi privati di Home Assistant che un modulo usa: nomi con il trattino basso
    importati da ``homeassistant.*``, moduli privati, attributi privati letti da oggetti
    che non sono ``self``, ``_TRACK_STATE_CHANGE_DATA`` scritto da qualche parte."""
    testo = percorso.read_text(encoding="utf-8")
    if "_TRACK_STATE_CHANGE_DATA" in testo:
        yield "_TRACK_STATE_CHANGE_DATA"
    for nodo in ast.walk(ast.parse(testo)):
        if isinstance(nodo, ast.ImportFrom) and (modulo := nodo.module or "").startswith(
            "homeassistant"
        ):
            if any(parte.startswith("_") for parte in modulo.split(".")):
                yield modulo
            for nome in nodo.names:
                if nome.name.startswith("_"):
                    yield f"{modulo}.{nome.name}"
        elif isinstance(nodo, ast.Import):
            for nome in nodo.names:
                if nome.name.startswith("homeassistant") and any(
                    parte.startswith("_") for parte in nome.name.split(".")
                ):
                    yield nome.name
        elif (
            isinstance(nodo, ast.Attribute)
            and nodo.attr.startswith("_")
            and not (nodo.attr.startswith("__") and nodo.attr.endswith("__"))
            and not (isinstance(nodo.value, ast.Name) and nodo.value.id == "self")
        ):
            yield f"{ast.unparse(nodo.value)}.{nodo.attr}"


@pytest.mark.parametrize("percorso", MODULI_PROPRI, ids=lambda p: p.name)
def test_niente_nomi_privati_di_home_assistant(percorso: Path) -> None:
    """``seguire.py`` e ``attivazioni.py`` usano solo nomi pubblici di Home Assistant e
    non importano un'altra integrazione (trigger di ``homeassistant`` o di ``template``)."""
    assert list(_nomi_privati(percorso)) == []
    testo = percorso.read_text(encoding="utf-8")
    for vietato in (
        "homeassistant.components.homeassistant",
        "homeassistant.components.template",
        "homeassistant.components.automation",
        "homeassistant.components.script",
    ):
        assert f"from {vietato}" not in testo
        assert f"import {vietato}" not in testo
