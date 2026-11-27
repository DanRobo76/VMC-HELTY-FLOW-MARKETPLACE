"""I sensori calcolati dell'integrazione contro le entità template di Home Assistant.

Le 121 configurazioni vere della VMC «master» (``generato_fase4.sensori``) una volta con le
entità template di Home Assistant (``StateSensorEntity``, ``StateBinarySensorEntity``) e una
volta con quelle dell'integrazione (``SensoreModello``, ``BinarioModello``, da
``sensori_template.in_ordine``), tutte e due con ``async_track_template_result`` di Home
Assistant, ognuna in un Home Assistant suo con l'orologio fermo (anche quello del ciclo
degli eventi: i ritardi scattano solo quando la prova fa passare il tempo). Gli stessi
cambi delle entità lette (letture, impostazioni, valori interni, timer del motore, tempo
che passa, ``homeassistant.update_entity``, entity_id cambiati, entità tolte) devono dare
la stessa sequenza di scritture delle entità (``state_changed`` e ``state_reported``,
nell'ordine, passo per passo), con gli stessi stati, attributi, istanti e contesti, e gli
stessi messaggi nel registro. Con Home Assistant che parte (i modelli si seguono
all'avvio, dopo il ripristino) e già avviato (prima i modelli, poi il ripristino), con
stati da ripristinare.

Il motore qui è senza memoria interna: i valori interni sono stati con l'entity_id di
oggi, le altre entità lette quelle di domani (colonna «Domani» della fase 1).
"""

from __future__ import annotations

import ast
import csv
import logging
import random
from collections.abc import AsyncIterator, Callable, Sequence
from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import pytest
from freezegun.api import FrozenDateTimeFactory
from homeassistant.components.template.binary_sensor import StateBinarySensorEntity
from homeassistant.components.template.sensor import StateSensorEntity
from homeassistant.const import EVENT_STATE_CHANGED, EVENT_STATE_REPORTED
from homeassistant.core import CoreState, Event, HomeAssistant, State, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import restore_state as rs
from homeassistant.helpers.entity import Entity
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import (
    MockEntityPlatform,
    async_fire_time_changed,
    async_test_home_assistant,
)

from custom_components.vmc_master.nativa.assemblaggio import configurazione_timer
from custom_components.vmc_master.nativa.motore.contesto import Contesto
from custom_components.vmc_master.nativa.motore.generato_fase4 import (
    sensori as codice_sensori,
)
from custom_components.vmc_master.nativa.motore.timer import TimerDelMotore
from custom_components.vmc_master.nativa.sensori_modello import (
    BinarioModello,
    SensoreModello,
)
from custom_components.vmc_master.nativa.sensori_template import (
    AnnunciDeiTimer,
    a_gruppi,
    in_ordine,
)

from . import confronto as c
from .motore.traduci import RADICE

T0 = datetime(2026, 11, 27, 9, 0, 0, tzinfo=UTC)
FASE_1 = RADICE / "tests/nativa/motore/aiutanti_fase1.csv"
INTEGRAZIONE = RADICE / "custom_components" / "vmc_master"

Operazione = tuple[Any, ...]
Crea = Callable[[HomeAssistant, Contesto], list[Entity]]
# uno stato da ripristinare: stato, dati in più (o None), unique_id dell'entità
DaRipristinare = tuple[State, dict[str, Any] | None, str]


# --- i due lati ---------------------------------------------------------------------------------


def _entita_di_home_assistant(hass: HomeAssistant, contesto: Contesto) -> list[Entity]:
    """Le entità template di Home Assistant, come le creava sensori_template fino alla b45."""
    uscita: list[Entity] = []
    for dominio, config in codice_sensori.sensori(contesto, c.IP):
        if dominio == "sensor":
            uscita.append(StateSensorEntity(hass, config, config.get("unique_id")))
        else:
            uscita.append(
                StateBinarySensorEntity(hass, config, config.get("unique_id"))
            )
    return uscita


def _entita_dell_integrazione(hass: HomeAssistant, contesto: Contesto) -> list[Entity]:
    entita: list[Entity] = list(in_ordine(hass, contesto, codice_sensori, c.IP))
    assert all(isinstance(e, (SensoreModello, BinarioModello)) for e in entita)
    return entita


# --- le entità lette e il copione dei cambi ----------------------------------------------------


def _domani() -> dict[str, str]:
    """Colonna «Domani» della fase 1: aiutante di oggi -> entità di domani (o «interna»)."""
    with FASE_1.open(encoding="utf-8-sig", newline="") as f:
        return {r["Entità oggi"]: r["Domani"] for r in csv.DictReader(f, delimiter=";")}


def _di_domani(entity_id: str, domani: dict[str, str]) -> str:
    """L'entity_id che legge il sensore nativo al posto di quello di oggi (i valori
    interni, senza memoria interna, tengono quello di oggi)."""
    nuovo = domani.get(entity_id, entity_id)
    return entity_id if nuovo.startswith("interna") else nuovo


def _numerico(config: dict[str, Any]) -> bool:
    return any(k in config for k in ("unit_of_measurement", "device_class", "state_class"))


class Copione:
    """Gli stati iniziali delle entità lette e i passi, uguali per i due lati (seme fisso)."""

    def __init__(self, seme: int = 46, passi_a_caso: int = 120) -> None:
        rng = random.Random(seme)
        domani = _domani()
        self.iniziali: dict[str, tuple[str, dict[str, Any]]] = {}
        self.candidati: dict[str, tuple[str, ...]] = {}
        self.timer: list[str] = []
        for oggi, valore in sorted(c.base_iniziale(rng).items()):
            if oggi.startswith("timer."):
                self.timer.append(oggi)
                continue
            eid = _di_domani(oggi, domani)
            attributi = {**c.attributi_fissi(oggi), **c.attributi_esterni(rng, oggi)}
            self.iniziali[eid] = (valore, attributi)
            self.candidati[eid] = c.candidati(oggi)
        ingressi = sorted(self.iniziali)
        self.passi: list[list[Operazione]] = []

        def stato(eid: str, valore: str, attributi: dict[str, Any] | None = None) -> Operazione:
            if attributi is None:
                attributi = self.iniziali.get(eid, ("", {}))[1]
            return ("stato", eid, valore, attributi)

        def lettura(oggetto: str) -> str:
            return f"sensor.vmc_master_{oggetto}"

        ventola = c.GREZZI_VMGH[1]
        sensori = c.GREZZI_VMGI[0]
        # una VMC normale: velocità 1, in linea, tutte le spie spente
        self.passi.append(
            [
                *(stato(e, "off") for e in ingressi if "_spia_" in e),
                stato(lettura("status_ventola"), ventola),
                stato(lettura("status_ventola_memorizzata"), ventola),
                stato(lettura("sensori"), sensori),
                stato(lettura("sensori_memorizzata"), sensori),
                stato(lettura("status_ip"), "ON-Line"),
                stato(lettura("nome"), "VMNM Master"),
                stato(lettura("lan"), "VMSL,192,168,1,160"),
                stato("input_number.vmc_master_attesa_blackout_rilevazione", "32.0"),
            ]
        )
        # velocità 3, poi 0
        for codice in ("00003", "00000"):
            valore = ventola.replace("00001", codice, 1)
            self.passi.append(
                [
                    stato(lettura("status_ventola"), valore),
                    stato(lettura("status_ventola_memorizzata"), valore),
                ]
            )
        # black-out a velocità 0: la VMC non risponde per 10 s (nessun black-out), poi
        # per 35 s (black-out dopo i 32 s di «delay_on»); l'attesa cambia durante il ritardo
        self.passi.append([stato(lettura("status_ip"), "OFF-Line")])
        self.passi.append([("tempo", 10)])
        self.passi.append([stato(lettura("status_ip"), "ON-Line")])
        self.passi.append([stato(lettura("status_ip"), "OFF-Line")])
        self.passi.append([("tempo", 20)])
        self.passi.append(
            [stato("input_number.vmc_master_attesa_blackout_rilevazione", "40.0")]
        )
        self.passi.append([("tempo", 15)])
        self.passi.append([stato(lettura("status_ip"), "ON-Line")])
        # fuori -20 °C, poi 5 °C
        for esterna in ("-0200", "00050"):
            valore = sensori.replace("00100", esterna, 1)
            self.passi.append(
                [stato(lettura("sensori"), valore), stato(lettura("sensori_memorizzata"), valore)]
            )
        # un timer del motore letto da Velocità Registrata
        for servizio, tempo in (("start", 5), ("pause", 1), ("start", 0), ("cancel", 0)):
            for timer in self.timer:
                self.passi.append([("timer", servizio, timer), ("tempo", tempo)])
        # cambi a caso, anche di attributi, con il tempo che passa
        esterni = [e for e in ingressi if e in c.ESTERNI]
        for _ in range(passi_a_caso):
            operazioni: list[Operazione] = [
                stato(eid, rng.choice(self.candidati[eid]))
                for eid in rng.sample(ingressi, rng.randint(1, 6))
            ]
            caso = rng.random()
            if caso < 0.1 and esterni:
                eid = rng.choice(esterni)
                operazioni.append(
                    stato(eid, self.iniziali[eid][0], c.attributi_esterni(rng, eid))
                )
            elif caso < 0.25 and self.timer:
                servizio = rng.choice(("start", "pause", "cancel", "finish"))
                operazioni.append(("timer", servizio, rng.choice(self.timer)))
            if rng.random() < 0.35:
                operazioni.append(("tempo", rng.choice((1, 5, 30, 61, 300))))
            self.passi.append(operazioni)
        # tutte le entità lette non disponibili, sconosciute, illeggibili, poi di nuovo
        # come all'inizio
        for valore in ("unavailable", "unknown", "abc"):
            self.passi.append([stato(e, valore) for e in ingressi])
        self.passi.append([stato(e, v, a) for e, (v, a) in self.iniziali.items()])
        self.passi.append([("tempo", 61)])
        self.passi.append([("aggiorna",)])
        # entity_id cambiati (anche di sensori letti da altri) e poi rimessi
        rinominati = (
            "sensor.vmc_master_temp_esterna_status",
            "sensor.vmc_master_temp_esterna_status_grafico",
            "binary_sensor.vmc_master_black_out_rilevato",
        )
        self.passi.append([("rinomina", e, f"{e}_bis") for e in rinominati])
        self.passi.append(
            [
                stato(lettura("sensori"), c.GREZZI_VMGI[1]),
                stato(lettura("status_ip"), "OFF-Line"),
            ]
        )
        self.passi.append([("tempo", 35)])
        self.passi.append([("rinomina", f"{e}_bis", e) for e in rinominati])
        self.passi.append([stato(lettura("status_ip"), "ON-Line")])
        # un ritardo in corso quando le entità si tolgono
        self.passi.append([stato(lettura("status_ip"), "OFF-Line"), ("tempo", 5)])
        self.passi.append([("rimuovi",)])
        self.passi.append([("tempo", 60)])


def _ripristino(contesto: Contesto) -> list[DaRipristinare]:
    """Gli stati da ripristinare (uguali nei due lati): ripristinabili, non disponibili,
    senza dati in più (un sensore non si ripristina), nessuno."""
    uscita: list[DaRipristinare] = []
    for i, (dominio, config) in enumerate(codice_sensori.sensori(contesto, c.IP)):
        eid = config["default_entity_id"]
        attributi = {"icon": "mdi:backup-restore", "friendly_name": f"Ripristinato {i}"}
        if dominio == "sensor":
            valore: Any = 12.5 if _numerico(config) else "ripristinato"
            dati: dict[str, Any] | None = {
                "native_value": valore,
                "native_unit_of_measurement": config.get("unit_of_measurement"),
            }
        else:
            valore, dati = "on", None
        unique_id = config["unique_id"]
        if i % 4 == 0:
            uscita.append((State(eid, str(valore), attributi), dati, unique_id))
        elif i % 4 == 1:
            uscita.append((State(eid, "unavailable", attributi), dati, unique_id))
        elif i % 4 == 2:
            uscita.append((State(eid, str(valore), attributi), None, unique_id))
    return uscita


def _carica_ripristino(hass: HomeAssistant, stati: list[DaRipristinare]) -> None:
    """Gli stati da ripristinare come dopo un riavvio: le voci del registro delle entità ci
    sono già, gli stati salvati si caricano con il caricamento di Home Assistant
    (``mock_restore_cache`` del plugin dei test scrive ancora ``last_states``, che Home
    Assistant 2026.11 non legge più)."""
    registro = er.async_get(hass)
    for stato, _dati, unique_id in stati:
        dominio, _, oggetto = stato.entity_id.partition(".")
        voce = registro.async_get_or_create(
            dominio, "vmc_master", unique_id, suggested_object_id=oggetto
        )
        assert voce.entity_id == stato.entity_id
    rs.async_get(hass)._async_load_stored_states(
        [
            {"state": stato.as_dict(), "extra_data": dati, "last_seen": T0.isoformat()}
            for stato, dati, _unique_id in stati
        ]
    )


# --- un lato in un Home Assistant suo ----------------------------------------------------------


class Registro:
    """Le scritture delle entità calcolate, in ordine, con il passo del copione."""

    def __init__(self, hass: HomeAssistant, calcolate: set[str]) -> None:
        self.passo = 0
        self.voci: list[tuple[Any, ...]] = []
        self.calcolate = calcolate
        self._contesti: dict[str, int] = {}
        filtro = callback(lambda dati: dati["entity_id"] in self.calcolate)
        for tipo in (EVENT_STATE_CHANGED, EVENT_STATE_REPORTED):
            hass.bus.async_listen(tipo, self._annota, event_filter=filtro)

    @callback
    def _annota(self, evento: Event[Any]) -> None:
        stato: State | None = evento.data["new_state"]
        voce: tuple[Any, ...] = (self.passo, evento.event_type, evento.data["entity_id"])
        if stato is not None:
            # i contesti in ordine di apparizione: stessi contesti negli stessi punti
            contesto = self._contesti.setdefault(stato.context.id, len(self._contesti))
            voce += (
                stato.state,
                dict(stato.attributes),
                stato.last_changed.isoformat(),
                stato.last_updated.isoformat(),
                stato.last_reported.isoformat(),
                contesto,
            )
        self.voci.append(voce)


@asynccontextmanager
async def _istanza(config_dir: str, avviato: bool) -> AsyncIterator[HomeAssistant]:
    """Un Home Assistant per un lato, già avviato o che deve partire."""
    stato = CoreState.running if avviato else CoreState.not_running
    async with async_test_home_assistant(
        config_dir=config_dir, initial_state=stato
    ) as hass:
        try:
            yield hass
        finally:
            if hass.state is not CoreState.not_running:
                await hass.async_stop(force=True)


async def _gira(
    freezer: FrozenDateTimeFactory,
    config_dir: str,
    caplog: pytest.LogCaptureFixture,
    crea: Crea,
    passi: Sequence[Sequence[Operazione]],
    iniziali: dict[str, tuple[str, dict[str, Any]]],
    *,
    avviato: bool,
    ripristino: Callable[[Contesto], list[DaRipristinare]],
    timer: dict[str, dict[str, Any]] | None = None,
) -> tuple[list[tuple[Any, ...]], list[tuple[int, str]], dict[str, Any]]:
    """Un lato: le scritture delle entità, i messaggi del registro e gli stati finali."""
    freezer.move_to(T0)
    inizio_registro = len(caplog.records)
    async with _istanza(config_dir, avviato) as hass:
        # con le integrazioni dei domini le entità sono nei loro componenti (per
        # homeassistant.update_entity), come quelle della voce di configurazione
        for dominio in ("homeassistant", "sensor", "binary_sensor"):
            assert await async_setup_component(hass, dominio, {})
        contesto = Contesto(hass, "master")
        motore = contesto.timer = TimerDelMotore(contesto, timer or {})
        await motore.prepara()
        annunci = AnnunciDeiTimer(hass, motore)
        for eid, (valore, attributi) in iniziali.items():
            hass.states.async_set(eid, valore, attributi)
        await hass.async_block_till_done()
        _carica_ripristino(hass, ripristino(contesto))

        entita = crea(hass, contesto)
        calcolate = {e.entity_id for e in entita}
        assert len(calcolate) == len(entita)
        registro = Registro(hass, calcolate)
        piattaforme: dict[str, MockEntityPlatform] = {}
        for dominio, gruppo in a_gruppi(entita):
            if (piattaforma := piattaforme.get(dominio)) is None:
                piattaforma = piattaforme[dominio] = MockEntityPlatform(
                    hass, domain=dominio, platform_name="vmc_master"
                )
            await piattaforma.async_add_entities(gruppo)
        await hass.async_block_till_done()
        registro.passo += 1
        if not avviato:
            await hass.async_start()
            await hass.async_block_till_done()
            registro.passo += 1

        for operazioni in passi:
            for operazione in operazioni:
                await _esegui(hass, freezer, motore, entita, calcolate, operazione)
            await hass.async_block_till_done()
            registro.passo += 1
        finali = {
            eid: (s.state, dict(s.attributes)) if (s := hass.states.get(eid)) else None
            for eid in sorted(calcolate)
        }
        annunci.ferma()
        motore.ferma()
    # i messaggi del registro (non quelli di asyncio: compiti e callback lenti, che con
    # l'orologio fermo misurano i salti dell'orologio fatti dalla prova)
    messaggi = [
        (r.levelno, r.getMessage())
        for r in caplog.records[inizio_registro:]
        if r.levelno >= logging.WARNING and r.name != "asyncio"
    ]
    return registro.voci, messaggi, finali


async def _esegui(
    hass: HomeAssistant,
    freezer: FrozenDateTimeFactory,
    motore: TimerDelMotore,
    entita: list[Entity],
    calcolate: set[str],
    operazione: Operazione,
) -> None:
    tipo = operazione[0]
    if tipo == "stato":
        _, eid, valore, attributi = operazione
        hass.states.async_set(eid, valore, attributi)
    elif tipo == "timer":
        _, servizio, eid = operazione
        try:
            await motore.servizio(servizio, {}, {"entity_id": eid}, None)
        except HomeAssistantError:
            pass  # per esempio «pause» di un timer fermo: uguale nei due lati
    elif tipo == "tempo":
        freezer.tick(timedelta(seconds=operazione[1]))
        async_fire_time_changed(hass)
        await hass.async_block_till_done()
    elif tipo == "aggiorna":
        await hass.services.async_call(
            "homeassistant",
            "update_entity",
            {"entity_id": [e.entity_id for e in entita]},
            blocking=True,
        )
    elif tipo == "rinomina":
        _, vecchio, nuovo = operazione
        calcolate.add(nuovo)
        er.async_get(hass).async_update_entity(vecchio, new_entity_id=nuovo)
        await hass.async_block_till_done()
    elif tipo == "rimuovi":
        for una in entita:
            await una.async_remove(force_remove=True)
    else:
        raise AssertionError(tipo)


def _primo_diverso(a: Sequence[Any], b: Sequence[Any]) -> str:
    """Dove due sequenze si separano, con le voci vicine (per il messaggio d'errore)."""
    for i, (x, y) in enumerate(zip(a, b, strict=False)):
        if x != y:
            return f"voce {i}:\n  Home Assistant: {x}\n  integrazione:   {y}"
    return f"lunghezze diverse: {len(a)} contro {len(b)}"


def _confronta(ha: tuple[Any, ...], nostro: tuple[Any, ...]) -> None:
    voci_ha, messaggi_ha, finali_ha = ha
    voci, messaggi, finali = nostro
    assert voci == voci_ha, _primo_diverso(voci_ha, voci)
    assert messaggi == messaggi_ha, _primo_diverso(messaggi_ha, messaggi)
    assert finali == finali_ha


# --- le prove ------------------------------------------------------------------------------------


@pytest.fixture(scope="module")
def copione() -> Copione:
    return Copione()


@pytest.mark.parametrize("avviato", [False, True], ids=["avvio", "avviato"])
async def test_le_121_configurazioni_come_le_entita_template(
    freezer: FrozenDateTimeFactory,
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
    copione: Copione,
    avviato: bool,
) -> None:
    """Stessi stati scritti, nello stesso ordine e negli stessi istanti, con gli stessi
    attributi, contesti e messaggi d'errore."""
    timer = configurazione_timer("master")
    lati = []
    for crea in (_entita_di_home_assistant, _entita_dell_integrazione):
        lati.append(
            await _gira(
                freezer,
                str(tmp_path),
                caplog,
                crea,
                copione.passi,
                copione.iniziali,
                avviato=avviato,
                ripristino=_ripristino,
                timer=timer,
            )
        )
    ha, nostro = lati
    voci = ha[0]
    # la prova vede davvero i casi: tutte le 121 entità scritte, molte con più stati,
    # il black-out dopo il ritardo, errori dei modelli
    scritte: dict[str, set[str]] = {}
    for voce in voci:
        if len(voce) > 3:
            scritte.setdefault(voce[2], set()).add(voce[3])
    assert len(scritte) >= 121
    assert sum(len(s) > 1 for s in scritte.values()) > 80
    assert "on" in scritte["binary_sensor.vmc_master_black_out_rilevato"]
    assert sum("unavailable" in s for s in scritte.values()) > 10
    assert any("TemplateError" in m for _, m in ha[1])
    # stati ripristinati quando le entità si aggiungono (con Home Assistant già avviato
    # solo dove i modelli non danno un valore)
    ripristinati = [
        v
        for v in voci
        if len(v) > 3 and v[0] == 0 and v[4].get("friendly_name", "").startswith("Ripristinato")
    ]
    assert len(ripristinati) > (20 if not avviato else 0)
    _confronta(ha, nostro)


# --- casi che le 121 configurazioni non provocano ----------------------------------------------


def _modello(testo: Callable[[Contesto, Any], str], nome: str) -> Callable[..., str]:
    testo.__name__ = nome
    testo.sorgente = f"{{{{ {nome} }}}}"  # type: ignore[attr-defined]
    return testo


def _leggi(c_: Contesto, eid: str) -> str:
    return c_.states(eid)


def _rari(hass: HomeAssistant, contesto: Contesto) -> list[tuple[str, dict[str, Any]]]:
    """Configurazioni con le stesse chiavi dei 121 sensori per i casi rari: icona non
    valida, nome con un modello, errori dei modelli di disponibilità, stato e ritardo,
    ritardo che non è una durata, stato numerico non valido."""
    m = contesto.modello
    s = contesto.statico

    def errore(nome: str) -> Callable[..., str]:
        def modello(c_: Contesto, _v: Any) -> str:
            valore = c_.states("sensor.prova_a")
            if valore == "errore":
                raise ValueError("modello in errore")
            return valore

        return _modello(modello, nome)

    def anello(c_: Contesto, _v: Any) -> str:
        """Legge la sua entità e cambia a ogni resa (finché sensor.prova_a è «on»)."""
        if c_.states("sensor.prova_a") != "on":
            return "fermo"
        proprio = c_.states("sensor.prova_anello")
        return str(int(proprio) + 1) if proprio.isdigit() else "0"

    return [
        (
            "sensor",
            {
                "default_entity_id": "sensor.prova_icona",
                "name": m(_modello(lambda c_, v: f"Nome {_leggi(c_, 'sensor.prova_a')}", "nome")),
                "unique_id": "prova_icona",
                "state": m(errore("stato_errore")),
                "icon": m(_modello(lambda c_, v: _leggi(c_, "sensor.prova_b"), "icona")),
            },
        ),
        (
            "sensor",
            {
                "default_entity_id": "sensor.prova_numero",
                "name": s("Prova numero"),
                "unique_id": "prova_numero",
                "state": m(_modello(lambda c_, v: _leggi(c_, "sensor.prova_a"), "numero")),
                "availability": m(errore("disponibile_errore")),
                "unit_of_measurement": "°C",
                "icon": s("mdi:thermometer"),
            },
        ),
        (
            "binary_sensor",
            {
                "default_entity_id": "binary_sensor.prova_ritardo",
                "name": s("Prova ritardo"),
                "unique_id": "prova_ritardo",
                "state": m(errore("binario_errore")),
                "delay_on": m(_modello(lambda c_, v: _leggi(c_, "sensor.prova_b"), "ritardo")),
                "icon": s("mdi:flash"),
            },
        ),
        (
            "binary_sensor",
            {
                "default_entity_id": "binary_sensor.prova_disponibile",
                "name": s("Prova disponibile"),
                "unique_id": "prova_disponibile",
                "state": m(_modello(lambda c_, v: _leggi(c_, "sensor.prova_a"), "binario")),
                "availability": m(
                    _modello(lambda c_, v: _leggi(c_, "sensor.prova_b"), "disponibile")
                ),
                "delay_on": s("00:00:07"),
            },
        ),
        (
            "sensor",
            {
                "default_entity_id": "sensor.prova_anello",
                "name": s("Prova anello"),
                "unique_id": "prova_anello",
                "state": m(_modello(anello, "anello")),
                "icon": m(_modello(lambda c_, v: _leggi(c_, "sensor.prova_b"), "icona_anello")),
            },
        ),
    ]


def _crea_rari(nostre: bool) -> Crea:
    def crea(hass: HomeAssistant, contesto: Contesto) -> list[Entity]:
        uscita: list[Entity] = []
        for dominio, config in _rari(hass, contesto):
            if nostre:
                classe: Any = SensoreModello if dominio == "sensor" else BinarioModello
            else:
                classe = StateSensorEntity if dominio == "sensor" else StateBinarySensorEntity
            uscita.append(classe(hass, config, config["unique_id"]))
        return uscita

    return crea


def _ripristino_rari(contesto: Contesto) -> list[DaRipristinare]:
    return [
        (
            State("sensor.prova_numero", "3.5", {"friendly_name": "Vecchio"}),
            {"native_value": 3.5, "native_unit_of_measurement": "°C"},
            "prova_numero",
        ),
        (
            State("binary_sensor.prova_ritardo", "on", {"icon": "mdi:alert"}),
            None,
            "prova_ritardo",
        ),
        (
            State("sensor.prova_icona", "vecchio", {"icon": "mdi:alert"}),
            {"native_value": "vecchio", "native_unit_of_measurement": None},
            "prova_icona",
        ),
    ]


@pytest.mark.parametrize("avviato", [False, True], ids=["avvio", "avviato"])
async def test_casi_rari_come_le_entita_template(
    freezer: FrozenDateTimeFactory,
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
    avviato: bool,
) -> None:
    """Icona non valida, nome con un modello, errori, ritardi che non sono durate,
    ritardi annullati e ripresi: come le entità template."""
    # all'inizio i modelli sono in errore: anche con Home Assistant già avviato gli stati
    # restano senza valore e si ripristinano
    iniziali = {"sensor.prova_a": ("errore", {}), "sensor.prova_b": ("mdi:fan", {})}
    valori_a = ("on", "errore", "off", "21.5", "abc", "on", "true", "errore", "1")
    valori_b = ("non un'icona", "5", "on", "00:00:03", "errore", "mdi:fan", "-4", "off")
    passi: list[list[Operazione]] = []
    for a in valori_a:
        for b in valori_b:
            passi.append([("stato", "sensor.prova_a", a, {})])
            passi.append([("stato", "sensor.prova_b", b, {}), ("tempo", 2)])
    passi.append([("aggiorna",)])
    passi.append([("rinomina", "binary_sensor.prova_ritardo", "binary_sensor.prova_r2")])
    passi.append([("stato", "sensor.prova_a", "off", {}), ("stato", "sensor.prova_b", "4", {})])
    passi.append([("stato", "sensor.prova_a", "on", {}), ("tempo", 1)])
    passi.append([("rimuovi",)])
    passi.append([("tempo", 10)])
    lati = [
        await _gira(
            freezer,
            str(tmp_path),
            caplog,
            _crea_rari(nostre),
            passi,
            iniziali,
            avviato=avviato,
            ripristino=_ripristino_rari,
        )
        for nostre in (False, True)
    ]
    ha, nostro = lati
    messaggi = " ".join(m for _, m in ha[1])
    for atteso in (
        "TemplateError",
        "Error validating template result",
        "expected a number",
        "Template loop detected",
    ):
        assert atteso in messaggi
    # gli stati ripristinati, scritti quando le entità si aggiungono (con Home Assistant
    # già avviato un modello dello stato in errore rende l'entità non disponibile)
    ripristinati = {(v[2], v[3]) for v in ha[0] if len(v) > 3 and v[0] == 0}
    attesi = {("sensor.prova_numero", "3.5")}
    if not avviato:
        attesi |= {("sensor.prova_icona", "vecchio"), ("binary_sensor.prova_ritardo", "on")}
    assert attesi <= ripristinati
    _confronta(ha, nostro)


# --- stessi entity_id, unique_id e nomi --------------------------------------------------------


async def test_stessi_entity_id_unique_id_e_nomi(hass: HomeAssistant) -> None:
    """Le entità dell'integrazione hanno gli entity_id, gli unique_id, i nomi, le icone
    e le classi delle entità template di prima (la cronologia resta)."""
    for nome in ("master", "sala"):
        contesto = Contesto(hass, nome)
        contesto.timer = TimerDelMotore(contesto, {})
        prima = _entita_di_home_assistant(hass, contesto)
        dopo = _entita_dell_integrazione(hass, contesto)
        assert len(dopo) == 121
        for vecchia, nuova in zip(prima, dopo, strict=True):
            for proprieta in (
                "entity_id",
                "unique_id",
                "name",
                "icon",
                "device_class",
                "should_poll",
                "has_entity_name",
                "translation_key",
            ):
                assert getattr(nuova, proprieta) == getattr(vecchia, proprieta), (
                    vecchia.entity_id,
                    proprieta,
                )
            if isinstance(nuova, SensoreModello):
                for proprieta in ("native_unit_of_measurement", "state_class"):
                    assert getattr(nuova, proprieta) == getattr(vecchia, proprieta)
        assert [d for d, _ in a_gruppi(dopo)] == [d for d, _ in a_gruppi(prima)]


def test_chiavi_non_gestite(hass: HomeAssistant) -> None:
    """Una configurazione con chiavi che le classi non hanno portato non si accetta."""
    contesto = Contesto(hass, "master")
    stato = contesto.statico("1")
    with pytest.raises(ValueError, match="attributes"):
        SensoreModello(hass, {"state": stato, "attributes": {}}, None)
    with pytest.raises(ValueError, match="delay_off"):
        BinarioModello(hass, {"state": stato, "delay_off": stato}, None)
    with pytest.raises(ValueError, match="delay_on"):
        SensoreModello(hass, {"state": stato, "delay_on": stato}, None)
    with pytest.raises(ValueError, match="timestamp"):
        SensoreModello(hass, {"state": stato, "device_class": "timestamp"}, None)


# --- nessuna dipendenza dall'integrazione template ---------------------------------------------


def test_l_integrazione_non_importa_l_integrazione_template() -> None:
    """Nessun modulo dell'integrazione importa ``homeassistant.components.template`` (né
    altri moduli interni delle integrazioni di Home Assistant tramite ``template``)."""
    trovati: list[str] = []
    for percorso in sorted(INTEGRAZIONE.rglob("*.py")):
        albero = ast.parse(percorso.read_text(encoding="utf-8"))
        for nodo in ast.walk(albero):
            moduli: list[str] = []
            if isinstance(nodo, ast.Import):
                moduli = [a.name for a in nodo.names]
            elif isinstance(nodo, ast.ImportFrom) and nodo.module:
                moduli = [nodo.module]
                if nodo.module == "homeassistant.components":
                    moduli += [f"homeassistant.components.{a.name}" for a in nodo.names]
            for modulo in moduli:
                if modulo == "homeassistant.components.template" or modulo.startswith(
                    "homeassistant.components.template."
                ):
                    trovati.append(f"{percorso.relative_to(INTEGRAZIONE)}: {modulo}")
    assert not trovati
