"""La memoria interna del motore come gli aiutanti di oggi (fase 4).

Home Assistant è l'oracolo: le stesse operazioni girano una volta con i 68 aiutanti del
package (``input_number``, ``input_text``, ``input_boolean`` con la configurazione del
package) e una volta con ``MemoriaInterna``, con lo stesso orologio fermo. Si
confrontano:

- gli stati all'avvio (con e senza stati salvati, anche fuori dai limiti);
- l'esito di ogni chiamata (riuscita, o errore con la stessa classe e lo stesso
  messaggio), gli avvisi nel registro;
- ogni cambio (``state_changed`` dell'aiutante e cambio della memoria): istante, stato
  vecchio e nuovo con attributi, ``last_changed``, ``last_updated`` e contesto;
- gli stati finali, ``last_reported`` compreso;
- che i valori interni non entrino mai nella macchina degli stati né negli eventi che
  vedono gli ascoltatori di tutti gli eventi (registro di Home Assistant compreso);
- il salvataggio nell'archivio (``Store``): quando si salva e che cosa si ripristina.
"""

from __future__ import annotations

import csv
import logging
from datetime import UTC, datetime, timedelta
from typing import Any

import pytest
from freezegun.api import FrozenDateTimeFactory
from homeassistant.const import (
    EVENT_HOMEASSISTANT_STOP,
    EVENT_STATE_CHANGED,
    MATCH_ALL,
)
from homeassistant.core import Context, Event, HomeAssistant, State, callback
from homeassistant.helpers.storage import Store
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import (
    async_fire_time_changed,
    async_test_home_assistant,
)

from custom_components.vmc_master.nativa.motore.memoria_interna import (
    CHIAVE_ARCHIVIO,
    INTERNI,
    RITARDO_SALVATAGGIO,
    MemoriaInterna,
    da_stato,
)
from custom_components.vmc_master.nativa.stato import StatoVMC
from custom_components.vmc_master.nativa.tabelle import IMPOSTAZIONI

from .rinomina import FASE_1
from .test_avvio_motore import _ripristina

T0 = datetime(2026, 11, 25, 10, 0, 0, tzinfo=UTC)
DOMINI = ("input_boolean", "input_number", "input_text")

ATTESA = "input_number.vmc_master_attesa_avvisi"
DELTA = "input_number.vmc_master_attesa_delta_avvio"
ARIA = "input_number.vmc_master_aria_scambiata_v1"
RICOMINCIO = "input_number.vmc_master_aria_scambiata_ricomincio"
COUNTDOWN = "input_text.vmc_master_countdown_avvisi"
PRECEDENTE = "input_text.vmc_master_velocita_precedente"
ULTIMA = "input_text.vmc_master_last_temp_external_entity"
SPIA = "input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0"
TUTTE_LE_ARIE = [f"input_number.vmc_master_aria_scambiata_{n}" for n in (
    "v1", "v2", "v3", "v4", "iperventilazione", "notte", "freecooling", "ricomincio"
)]  # fmt: skip


def _entity_id(chiave: str) -> str:
    dominio, oggetto = chiave.split(".", 1)
    return f"{dominio}.vmc_master_{oggetto}"


IDS = [_entity_id(c) for c in INTERNI]


def _configurazione() -> dict[str, dict[str, Any]]:
    """Gli aiutanti dei 68 valori come li scrive il package (stesso ordine)."""
    config: dict[str, dict[str, Any]] = {d: {} for d in DOMINI}
    for chiave in INTERNI:
        dominio, oggetto = chiave.split(".", 1)
        config[dominio][f"vmc_master_{oggetto}"] = dict(IMPOSTAZIONI[chiave])
    return config


# --- l'elenco ------------------------------------------------------------------------------


def test_interni_sono_quelli_della_fase_1() -> None:
    """I 68 valori interni sono quelli della colonna «Domani» della fase 1, con lo stesso
    comportamento dopo un riavvio: 63 conservano il valore, 5 ripartono vuoti (sono
    quelli con ``initial`` nel package)."""
    with FASE_1.open(encoding="utf-8-sig", newline="") as flusso:
        righe = [
            r
            for r in csv.DictReader(flusso, delimiter=";")
            if r["Domani"] == "interna (stato del motore)"
            and r["Tipo oggi"].startswith("input_")
        ]
    assert sorted(r["Entità oggi"] for r in righe) == sorted(IDS)
    assert len(IDS) == len(set(IDS)) == 68
    per_dominio = {d: sum(1 for c in INTERNI if c.startswith(d)) for d in DOMINI}
    assert per_dominio == {"input_boolean": 1, "input_number": 32, "input_text": 35}
    vuoti = sorted(_entity_id(c) for c in INTERNI if "initial" in IMPOSTAZIONI[c])
    assert vuoti == sorted(
        r["Entità oggi"] for r in righe if r["Dopo un riavvio"] == "riparte vuoto"
    )
    assert len(vuoti) == 5


# --- il banco ------------------------------------------------------------------------------


class Norma:
    """Istanti in secondi da T0, contesti con il loro id (quelli del banco) o «nuovo»."""

    def __init__(self, contesti: set[str]) -> None:
        self.contesti = contesti

    def istante(self, valore: datetime) -> float:
        return round((valore - T0).total_seconds(), 6)

    def contesto(self, contesto: Context | None) -> str | None:
        if contesto is None:
            return None
        return contesto.id if contesto.id in self.contesti else "nuovo"

    def stato(self, stato: State | None) -> Any:
        if stato is None:
            return None
        return (
            stato.entity_id,
            stato.state,
            dict(stato.attributes),
            self.istante(stato.last_changed),
            self.istante(stato.last_updated),
            self.istante(stato.last_reported),
            self.contesto(stato.context),
        )


def _contesto(nome: str | None, utenti: dict[str, str]) -> Context | None:
    if nome is None:
        return None
    contesto, _, utente = nome.partition("@")
    return Context(id=contesto, user_id=utenti.get(utente, utente) if utente else None)


async def _corsa(
    freezer: FrozenDateTimeFactory,
    passi: list[tuple[Any, ...]],
    *,
    memoria: bool,
    ripristino: list[State] | None = None,
    caplog: pytest.LogCaptureFixture,
) -> dict[str, Any]:
    """Una corsa con gli aiutanti (``memoria=False``) o con la memoria interna."""
    freezer.move_to(T0)
    contesti = {p[4].partition("@")[0] for p in passi if p[0] == "chiama" and p[4]}
    norma = Norma(contesti)
    esito: dict[str, Any] = {"esiti": [], "cambi": [], "avvisi": []}
    estranei: list[Any] = []
    async with async_test_home_assistant() as hass:
        utenti = {
            "admin": (
                await hass.auth.async_create_user("Admin", group_ids=["system-admin"])
            ).id,
            "utente": (await hass.auth.async_create_user("Utente")).id,
        }

        @callback
        def tutti(evento: Event) -> None:
            # gli eventi che vedono gli ascoltatori di tutti gli eventi (il registro)
            if evento.data.get("entity_id") in IDS or (
                evento.event_type == EVENT_STATE_CHANGED and memoria
            ):
                estranei.append((evento.event_type, dict(evento.data)))

        @callback
        def cambio(evento: Event) -> None:
            dati = evento.data
            if dati["entity_id"] not in IDS:
                return
            esito["cambi"].append(
                (
                    norma.istante(evento.time_fired),
                    dati["entity_id"],
                    norma.stato(dati["old_state"]),
                    norma.stato(dati["new_state"]),
                    norma.contesto(evento.context),
                )
            )

        m: MemoriaInterna | None = None
        if memoria:
            hass.bus.async_listen(MATCH_ALL, tutti)
            m = MemoriaInterna(hass)
            salvati = {
                chiave: da_stato(chiave, s.state)
                for s in ripristino or []
                for chiave in INTERNI
                if _entity_id(chiave) == s.entity_id
            }
            m.ripristina(salvati)
            m.ascolta_cambi(cambio)
        else:
            _ripristina(hass, ripristino or [])
            for dominio, voci in _configurazione().items():
                assert await async_setup_component(hass, dominio, {dominio: voci})
            hass.bus.async_listen(EVENT_STATE_CHANGED, cambio)
        await hass.async_block_till_done()

        def leggi(entity_id: str) -> State | None:
            return m.stato(entity_id) if m is not None else hass.states.get(entity_id)

        esito["iniziali"] = [norma.stato(leggi(e)) for e in IDS]
        caplog.clear()
        for passo in passi:
            if passo[0] == "attendi":
                freezer.tick(timedelta(seconds=passo[1]))
                async_fire_time_changed(hass)
                await hass.async_block_till_done()
                continue
            _, dominio, servizio, dati, contesto = passo
            ctx = _contesto(contesto, utenti)
            try:
                if m is not None:
                    await m.async_chiama(
                        dominio, servizio, dict(dati), ctx or Context()
                    )
                else:
                    await hass.services.async_call(
                        dominio, servizio, dict(dati), blocking=True, context=ctx
                    )
            except Exception as err:  # noqa: BLE001
                esito["esiti"].append((type(err).__name__, str(err)))
            else:
                esito["esiti"].append("ok")
            await hass.async_block_till_done()
        esito["avvisi"] = [
            (r.levelname, r.getMessage())
            for r in caplog.records
            if r.levelno >= logging.WARNING and r.name != "asyncio"
        ]
        esito["finali"] = [norma.stato(leggi(e)) for e in IDS]
        esito["nella_macchina"] = sorted(
            s.entity_id for s in hass.states.async_all() if s.entity_id in IDS
        )
        esito["estranei"] = estranei
        await hass.async_stop(force=True)
    return esito


def _confronta(atteso: dict[str, Any], ottenuto: dict[str, Any]) -> None:
    for chiave in ("iniziali", "esiti", "avvisi", "cambi", "finali"):
        assert ottenuto[chiave] == atteso[chiave], chiave
    assert atteso["nella_macchina"] == sorted(IDS)
    assert ottenuto["nella_macchina"] == []
    assert ottenuto["estranei"] == []


# --- avvio ---------------------------------------------------------------------------------

RIPRISTINI: dict[str, list[State]] = {
    "nessuno": [],
    "validi": [
        State(ATTESA, "5.0"),
        State(DELTA, "300"),
        State(ARIA, "1234.56"),
        State(RICOMINCIO, "123456789012.3456"),
        State(COUNTDOWN, "17"),
        State(ULTIMA, "sensor.temperatura"),
        State(PRECEDENTE, "3"),
        State(SPIA, "on"),
        State("input_text.vmc_master_ultima_scelta_utente", "Velocità 2"),
        State("input_text.vmc_master_tempo_mancante_reset", "reset"),
    ],
    "fuori_dai_limiti": [
        State(ATTESA, "0"),
        State(DELTA, "301"),
        State(ARIA, "abc"),
        State(RICOMINCIO, "unknown"),
        State("input_number.vmc_master_aria_scambiata_v2", "2e13"),
        State("input_number.vmc_master_aria_scambiata_v3", "1e13"),
        State(COUNTDOWN, "x" * 255),
        State(ULTIMA, "y" * 101),
        State("input_text.vmc_master_last_co2_internal_entity", "unknown"),
        State(PRECEDENTE, "z" * 30),
        State(SPIA, "unknown"),
    ],
    "tutti": [
        *(State(e, "7") for e in IDS if e.startswith("input_number")),
        *(State(e, "testo") for e in IDS if e.startswith("input_text")),
        State(SPIA, "off"),
    ],
}


@pytest.mark.parametrize("nome", sorted(RIPRISTINI))
async def test_avvio_come_gli_aiutanti(
    nome: str, freezer: FrozenDateTimeFactory, caplog: pytest.LogCaptureFixture
) -> None:
    """Stati all'avvio come gli aiutanti, dagli stati salvati (con ``initial`` nessun
    ripristino; un numero fuori dai limiti torna al minimo, un testo troppo lungo resta
    «unknown»)."""
    ripristino = RIPRISTINI[nome]
    atteso = await _corsa(
        freezer, [], memoria=False, ripristino=ripristino, caplog=caplog
    )
    ottenuto = await _corsa(
        freezer, [], memoria=True, ripristino=ripristino, caplog=caplog
    )
    _confronta(atteso, ottenuto)


# --- scritture ------------------------------------------------------------------------------


def numero(entita: Any, valore: Any, contesto: str | None = "c1") -> tuple[Any, ...]:
    return (
        "chiama",
        "input_number",
        "set_value",
        {"entity_id": entita, "value": valore},
        contesto,
    )


def un_testo(entita: Any, valore: Any, contesto: str | None = "c1") -> tuple[Any, ...]:
    return (
        "chiama",
        "input_text",
        "set_value",
        {"entity_id": entita, "value": valore},
        contesto,
    )


def interruttore(servizio: str, contesto: str | None = "c1") -> tuple[Any, ...]:
    return ("chiama", "input_boolean", servizio, {"entity_id": SPIA}, contesto)


def attendi(secondi: float) -> tuple[Any, ...]:
    return ("attendi", secondi)


SCRITTURE: dict[str, list[tuple[Any, ...]]] = {
    "numeri": [
        numero(ATTESA, 5),
        attendi(1),
        numero(ATTESA, 5, "c2"),  # stesso valore: solo last_reported
        attendi(1),
        numero(ATTESA, "7", "c3"),
        numero(ATTESA, 0),
        numero(ATTESA, 301),
        numero(ATTESA, "abc"),
        numero(ATTESA, None),
        numero(ATTESA, 2.5, "c4"),
        attendi(0.5),
        numero(ARIA, 1234.5678),
        numero(ARIA, 0.1 + 0.2),
        numero(ARIA, 1e13),
        numero(ARIA, 1e13 + 1),
        numero(RICOMINCIO, 1e22, "c5"),
        numero(RICOMINCIO, 123456789012.3456),
        numero(RICOMINCIO, -0.0),
        numero(ATTESA.upper(), 9, "c6"),
        numero(f"{ATTESA}, {DELTA}", 10, "c7"),
        numero([ATTESA, "input_number.vmc_master_inesistente"], 11, "c8"),
        ("chiama", "input_number", "set_value", {"value": 3}, "c9"),
        ("chiama", "input_number", "set_value", {"entity_id": ATTESA}, "c9"),
        (
            "chiama",
            "input_number",
            "set_value",
            {"entity_id": ATTESA, "value": 4, "altro": 1},
            "c9",
        ),
    ],
    "piu_bersagli": [
        numero(TUTTE_LE_ARIE, 0, "c1"),
        attendi(1),
        numero(TUTTE_LE_ARIE, 12.5, "c2"),
        numero(TUTTE_LE_ARIE, 12.5, "c3"),
        numero(list(reversed(TUTTE_LE_ARIE)), 1, "c4"),
        numero("all", 50, "c5"),
        numero([ATTESA, ARIA], 400, "c6"),
    ],
    "testi": [
        un_testo(COUNTDOWN, "12"),
        attendi(2),
        un_testo(COUNTDOWN, "12", "c2"),
        un_testo(COUNTDOWN, "x" * 256, "c3"),
        un_testo(PRECEDENTE, "x" * 21, "c3"),
        un_testo(PRECEDENTE, "x" * 20, "c4"),
        un_testo(ULTIMA, 5, "c5"),
        un_testo(ULTIMA, None, "c5"),
        un_testo(ULTIMA, "", "c6"),
        un_testo(ULTIMA, ["a"], "c6"),
        un_testo([COUNTDOWN, PRECEDENTE, ULTIMA], "-", "c7"),
        attendi(6),
        un_testo(COUNTDOWN, "", "c8"),
    ],
    "interruttore": [
        interruttore("turn_on"),
        interruttore("turn_on", "c2"),
        attendi(1),
        interruttore("toggle", "c3"),
        interruttore("toggle", "c4"),
        interruttore("turn_off", "c5"),
        attendi(10),
        interruttore("turn_off", "c6"),
        ("chiama", "input_boolean", "turn_on", {"entity_id": SPIA, "x": 1}, "c7"),
    ],
    "utenti": [
        numero(ATTESA, 20, "c1@admin"),
        numero(ATTESA, 21, "c2@utente"),
        numero(ATTESA, 22, "c3@sconosciuto"),
        interruttore("turn_on", "c4@admin"),
        un_testo(COUNTDOWN, "5", "c5@utente"),
    ],
}


@pytest.mark.parametrize("nome", sorted(SCRITTURE))
async def test_scritture_come_gli_aiutanti(
    nome: str, freezer: FrozenDateTimeFactory, caplog: pytest.LogCaptureFixture
) -> None:
    """Stesse chiamate ai servizi degli aiutanti: stessi esiti ed errori, stessi
    avvisi, stessi cambi (con istanti, attributi e contesti), stessi stati finali; e i
    valori interni mai nella macchina degli stati né negli eventi del registro."""
    passi = SCRITTURE[nome]
    atteso = await _corsa(
        freezer, passi, memoria=False, ripristino=RIPRISTINI["validi"], caplog=caplog
    )
    ottenuto = await _corsa(
        freezer, passi, memoria=True, ripristino=RIPRISTINI["validi"], caplog=caplog
    )
    assert atteso["cambi"], "il banco deve cambiare qualcosa"
    _confronta(atteso, ottenuto)


# --- StatoVMC --------------------------------------------------------------------------------


async def test_stato_vmc_riceve_i_valori(hass: HomeAssistant) -> None:
    """La memoria scrive i valori nello StatoVMC (all'avvio e a ogni cambio): i sensori
    nativi che li leggono (aria scambiata, tempo mancante, IP inserito, Black-Out)."""
    stato = StatoVMC(hass, "master")
    m = MemoriaInterna(hass, stato=stato)
    m.ripristina({"input_number.attesa_blackout_rilevazione": 45.0})
    assert stato.stato("input_number.attesa_blackout_rilevazione") == "45.0"
    assert stato.stato("input_text.ip_insert_esito") == ""
    assert stato.stato("input_text.tempo_mancante_reset") == "unknown"
    await m.async_chiama(
        "input_text",
        "set_value",
        {"entity_id": "input_text.vmc_master_tempo_mancante_reset", "value": "reset"},
        Context(),
    )
    assert stato.stato("input_text.tempo_mancante_reset") == "reset"
    voce = stato.voce("input_text.tempo_mancante_reset")
    assert voce is not None
    assert voce.attributi["max"] == 100


async def test_altra_vmc(hass: HomeAssistant) -> None:
    """Per un'altra VMC gli entity_id e i nomi sono quelli del suo package."""
    m = MemoriaInterna(hass, "sala")
    m.ripristina()
    stato = m.stato("input_number.vmc_sala_aria_scambiata_v4")
    assert stato is not None
    assert stato.attributes["friendly_name"] == "Aria Scambiata a Velocità 4"
    assert "input_number.vmc_master_aria_scambiata_v4" not in m
    assert len(m.entity_ids) == 68


# --- archivio ---------------------------------------------------------------------------------


async def test_archivio(
    hass: HomeAssistant,
    hass_storage: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Con l'archivio: si ripristina da lì; dopo un cambio si chiede un salvataggio
    entro ``RITARDO_SALVATAGGIO`` (uno solo, anche con tanti cambi, finché non si
    scrive); alla chiusura si salvano i valori di quel momento, poi più nulla."""
    chiave = CHIAVE_ARCHIVIO.format(nome="master")
    hass_storage[chiave] = {
        "version": 1,
        "minor_version": 1,
        "key": chiave,
        "data": {
            "valori": {
                "input_number.attesa_avvisi": 12.0,
                "input_number.aria_scambiata_ricomincio": 123456789012.3456,
                "input_text.countdown_avvisi": "33",
                "input_text.velocita_precedente": "3",
                "input_boolean.spia_umidita_mantenuta_velocita_0": True,
            }
        },
    }
    richieste: list[tuple[Any, float]] = []
    originale = Store.async_delay_save

    def ritardato(self: Store, data_func: Any, delay: float = 0) -> None:
        richieste.append((data_func, delay))
        originale(self, data_func, delay)

    monkeypatch.setattr(Store, "async_delay_save", ritardato)
    m = MemoriaInterna(hass)
    await m.async_carica()
    assert m.stato(ATTESA).state == "12.0"  # type: ignore[union-attr]
    assert m.salvati()["input_number.aria_scambiata_ricomincio"] == 123456789012.3456
    assert m.stato(COUNTDOWN).state == "33"  # type: ignore[union-attr]
    assert m.stato(PRECEDENTE).state == ""  # type: ignore[union-attr]
    assert m.stato(SPIA).state == "on"  # type: ignore[union-attr]
    assert richieste == []

    async def aria(valore: float) -> None:
        await m.async_chiama(
            "input_number", "set_value", {"entity_id": ARIA, "value": valore}, Context()
        )

    for secondi in range(30):
        await aria(float(secondi))
    # stesso valore: nessun cambio, nessuna richiesta
    await aria(29.0)
    assert [r[1] for r in richieste] == [RITARDO_SALVATAGGIO]
    # quando l'archivio scrive, legge i valori di quel momento; il cambio dopo chiede
    # un altro salvataggio
    dati = richieste[0][0]()
    assert dati["valori"]["input_number.aria_scambiata_v1"] == 29.0
    assert dati == {"valori": m.salvati()}
    await aria(30.0)
    assert [r[1] for r in richieste] == [RITARDO_SALVATAGGIO] * 2
    # alla chiusura: i valori di quel momento, poi più nulla
    await m.async_chiama(
        "input_text", "set_value", {"entity_id": COUNTDOWN, "value": "1"}, Context()
    )
    hass.bus.async_fire(EVENT_HOMEASSISTANT_STOP)
    await hass.async_block_till_done()
    valori = hass_storage[chiave]["data"]["valori"]
    assert valori["input_text.countdown_avvisi"] == "1"
    assert valori["input_number.aria_scambiata_v1"] == 30.0
    await m.async_chiama(
        "input_text", "set_value", {"entity_id": COUNTDOWN, "value": "2"}, Context()
    )
    assert len(richieste) == 2
    assert hass_storage[chiave]["data"]["valori"]["input_text.countdown_avvisi"] == "1"
    # un'altra memoria (dopo il riavvio) riparte dai valori salvati (i testi con
    # ``initial`` ripartono vuoti)
    altra = MemoriaInterna(hass)
    await altra.async_carica()
    assert altra.salvati() == {**valori, "input_text.velocita_precedente": ""}
    m.ferma()
    altra.ferma()
