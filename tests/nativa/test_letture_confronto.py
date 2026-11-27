"""Le letture native contro i sensori di oggi: stessi istanti, stesse scritture.

Oggi lo stato della VMC è un sensore ``tcp`` (aggiornato dal giro della sua piattaforma,
ogni 5 s) e la raggiungibilità un sensore ``command_line`` (il ping, ogni 10 s con
``async_track_time_interval``). Domani sono i coordinatori di letture.py con i sensori
di entita.py (``SensoreLetturaVMC``). In Home Assistant vero, con la stessa VMC finta e lo
stesso orologio, i due lati devono scrivere negli stessi momenti: un cambio di stato se
la lettura cambia, una scrittura senza cambio (``state_reported``) se è uguale, anche
quando la VMC non risponde (il sensore resta non disponibile e si riscrive a ogni giro); e
``homeassistant.update_entity`` rilegge la VMC prima di scrivere.

Il tempo avanza a passi di 1 s (``freezer.tick`` e ``async_fire_time_changed``, l'orologio
del ciclo compreso): a ogni passo si annota chi ha scritto, come e che cosa.

L'ambiente delle prove non ha ``jsonpath`` (requisito di command_line, usato solo per gli
attributi JSON, che il ping non ha): al suo posto un modulo vuoto con gli stessi nomi.
"""

from __future__ import annotations

import asyncio
import sys
import types
from datetime import timedelta
from typing import Any
from unittest.mock import patch

from freezegun.api import FrozenDateTimeFactory
from homeassistant.const import EVENT_STATE_CHANGED, EVENT_STATE_REPORTED
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import (
    MockEntityPlatform,
    async_fire_time_changed,
)

from custom_components.vmc_master.nativa.client import ErroreVMC
from custom_components.vmc_master.nativa.entita import SensoreLetturaVMC, crea_entita
from custom_components.vmc_master.nativa.vmc import VMCNativa

from .confronto import package

OGGI_STATO = "sensor.vmc_master_status_ventola"
OGGI_PING = "sensor.vmc_master_status_ip"
DOMANI_STATO = "sensor.vmc_nativa_status_ventola"
DOMANI_PING = "sensor.vmc_nativa_status_ip"


class _VMC:
    """La VMC finta dei due lati: la risposta a VMGH? e se risponde al ping."""

    def __init__(self) -> None:
        self.vmgh = "VMGO,00001" + ",00000" * 13
        self.accesa = True


class _Client:
    """Il client TCP finto del lato nativo (stesse risposte del sensore tcp finto)."""

    host = "192.168.1.50"

    def __init__(self, vmc: _VMC) -> None:
        self._vmc = vmc

    async def interroga(self, richiesta: str) -> str:
        if not self._vmc.accesa:
            raise ErroreVMC("VMC finta spenta")
        return self._vmc.vmgh if richiesta.startswith("VMGH") else ""

    async def comanda(self, comando: str) -> str:
        return ""


def _jsonpath() -> types.ModuleType:
    """Un ``jsonpath`` vuoto (command_line lo importa; il ping non lo usa)."""
    modulo = types.ModuleType("jsonpath")
    for nome in ("ExprSyntaxError", "JSONPathTypeError"):
        setattr(modulo, nome, type(nome, (Exception,), {}))
    modulo.search = lambda *argomenti, **kwargs: None  # type: ignore[attr-defined]
    return modulo


def _configurazione_di_oggi() -> list[dict[str, Any]]:
    """Il sensore tcp dello stato e il sensore command_line del ping, dal package."""
    tcp = next(
        dict(s)
        for s in package()["sensor"]
        if s.get("platform") == "tcp" and s["payload"] == "VMGH?"
    )
    ping = next(
        dict(voce["sensor"])
        for voce in package()["command_line"]
        if voce.get("sensor", {}).get("name") == "vmc_master_status_ip"
    )
    return [tcp, ping]


async def test_letture_agli_stessi_istanti_dei_sensori_di_oggi(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory
) -> None:
    """Giro delle letture, scritture uguali e diverse, update_entity: identici."""
    vmc = _VMC()

    def aggiorna_tcp(entita: Any) -> None:
        # come TcpEntity.update (e fakevmc.tcp_update del simulatore): la risposta della
        # VMC finta, o non disponibile se non risponde
        entita._attr_available = vmc.accesa
        if vmc.accesa:
            entita._state = vmc.vmgh

    class _Processo:
        returncode = 0

        async def communicate(self, input: bytes | None = None) -> tuple[bytes, bytes]:
            return (b"ON-Line\n" if vmc.accesa else b"OFF-Line\n"), b""

    async def shell(*argomenti: Any, **kwargs: Any) -> _Processo:
        return _Processo()

    async def ping(host: str) -> bool:
        return vmc.accesa

    visti: list[tuple[int, str, str, str]] = []
    passo = 0
    lati = {OGGI_STATO: "stato", DOMANI_STATO: "stato", OGGI_PING: "ping"}
    lati[DOMANI_PING] = "ping"

    @callback
    def annota(evento: Event) -> None:
        entity_id = evento.data["entity_id"]
        lato = "oggi" if "vmc_master_" in entity_id else "domani"
        if evento.event_type == EVENT_STATE_REPORTED:
            visti.append((passo, lato, lati[entity_id], "senza cambio"))
        else:
            visti.append(
                (passo, lato, lati[entity_id], evento.data["new_state"].state[:10])
            )

    @callback
    def filtro(dati: Any) -> bool:
        return dati["entity_id"] in lati

    hass.bus.async_listen(EVENT_STATE_CHANGED, annota, event_filter=filtro)
    hass.bus.async_listen(EVENT_STATE_REPORTED, annota, event_filter=filtro)
    with (
        patch(
            "homeassistant.components.tcp.entity.TcpEntity.update",
            autospec=True,
            side_effect=aggiorna_tcp,
        ),
        patch("asyncio.create_subprocess_shell", shell),
        patch.dict(
            sys.modules, {"jsonpath": sys.modules.get("jsonpath") or _jsonpath()}
        ),
    ):
        assert await async_setup_component(hass, "homeassistant", {})
        tcp, comando = _configurazione_di_oggi()
        assert await async_setup_component(hass, "sensor", {"sensor": [tcp]})
        assert await async_setup_component(
            hass, "command_line", {"command_line": [{"sensor": comando}]}
        )
        nativa = VMCNativa(
            hass,
            None,
            "nativa",
            "192.168.1.50",
            client=_Client(vmc),
            prova_ping=ping,
            versione=False,
        )
        await nativa.avvia()
        sensori, _ = crea_entita(nativa.stato, nativa.letture_dei_sensori())
        letture = [s for s in sensori if s.entity_id in (DOMANI_PING, DOMANI_STATO)]
        assert all(isinstance(s, SensoreLetturaVMC) for s in letture)
        assert len(letture) == 2
        await MockEntityPlatform(
            hass, domain="sensor", platform_name="vmc_master"
        ).async_add_entities(letture)
        await hass.async_block_till_done()

        async def avanza(fino: int) -> None:
            nonlocal passo
            while passo < fino:
                passo += 1
                freezer.tick(timedelta(seconds=1))
                async_fire_time_changed(hass)
                await hass.async_block_till_done(wait_background_tasks=True)

        await avanza(7)
        vmc.vmgh = "VMGO,00003" + ",00000" * 13  # la VMC cambia velocità
        await avanza(11)
        vmc.vmgh = "VMGO,00002" + ",00000" * 13
        for entity_id in (OGGI_STATO, DOMANI_STATO):
            await hass.services.async_call(
                "homeassistant",
                "update_entity",
                {"entity_id": entity_id},
                blocking=True,
            )
        await hass.async_block_till_done()
        vmc.accesa = False
        await avanza(32)
        nativa.ferma()

    oggi = [(p, tipo, cosa) for p, lato, tipo, cosa in visti if lato == "oggi"]
    domani = [(p, tipo, cosa) for p, lato, tipo, cosa in visti if lato == "domani"]
    # a ogni giro la lettura riscrive il sensore, anche non disponibile; update_entity
    # rilegge subito (passo 11)
    assert [voce for voce in oggi if voce[1] == "stato"][:8] == [
        (0, "stato", "VMGO,00001"),
        (5, "stato", "senza cambio"),
        (10, "stato", "VMGO,00003"),
        (11, "stato", "VMGO,00002"),
        (15, "stato", "unavailable"[:10]),
        (20, "stato", "senza cambio"),
        (25, "stato", "senza cambio"),
        (30, "stato", "senza cambio"),
    ]
    assert [voce for voce in oggi if voce[1] == "ping"] == [
        (0, "ping", "ON-Line"),
        (10, "ping", "senza cambio"),
        (20, "ping", "OFF-Line"),
        (30, "ping", "senza cambio"),
    ]
    # nello stesso passo l'ordine tra lo stato e il ping dipende da quando, in tempo vero,
    # sono partiti i loro timer (qui l'orologio del ciclo è quello vero): si confrontano
    # i passi e, in ogni passo, le scritture di ogni lettura
    assert sorted(oggi) == sorted(domani)


class _VMCLenta(_VMC):
    """La VMC finta con un ping che si può tenere in corso (``attesa``)."""

    def __init__(self) -> None:
        super().__init__()
        self.attesa: asyncio.Event | None = None

    async def risponde(self) -> bool:
        if self.attesa is not None:
            await self.attesa.wait()
        return self.accesa


async def test_update_entity_del_ping_come_il_sensore_di_oggi(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory
) -> None:
    """update_entity sul ping: due scritture (quella della lettura e quella di Home
    Assistant); con un ping del giro in corso nessuna lettura (una scrittura); il giro
    saltato se c'è un update_entity in corso."""
    vmc = _VMCLenta()

    class _Processo:
        returncode = 0

        async def communicate(self, input: bytes | None = None) -> tuple[bytes, bytes]:
            return (b"ON-Line\n" if await vmc.risponde() else b"OFF-Line\n"), b""

    async def shell(*argomenti: Any, **kwargs: Any) -> _Processo:
        return _Processo()

    async def ping(host: str) -> bool:
        return await vmc.risponde()

    visti: list[tuple[int, str, str]] = []
    passo = 0

    @callback
    def annota(evento: Event) -> None:
        lato = "oggi" if evento.data["entity_id"] == OGGI_PING else "domani"
        if evento.event_type == EVENT_STATE_REPORTED:
            visti.append((passo, lato, "senza cambio"))
        else:
            visti.append((passo, lato, evento.data["new_state"].state))

    @callback
    def filtro(dati: Any) -> bool:
        return dati["entity_id"] in (OGGI_PING, DOMANI_PING)

    hass.bus.async_listen(EVENT_STATE_CHANGED, annota, event_filter=filtro)
    hass.bus.async_listen(EVENT_STATE_REPORTED, annota, event_filter=filtro)

    async def aggiorna() -> None:
        # i due sensori insieme, senza aspettare la fine (un ping può essere in corso)
        for entity_id in (OGGI_PING, DOMANI_PING):
            hass.async_create_task(
                hass.services.async_call(
                    "homeassistant",
                    "update_entity",
                    {"entity_id": entity_id},
                    blocking=True,
                )
            )
        await _giri_del_ciclo()

    async def avanza(fino: int, *, aspetta: bool = True) -> None:
        nonlocal passo
        while passo < fino:
            passo += 1
            freezer.tick(timedelta(seconds=1))
            async_fire_time_changed(hass)
            if aspetta:
                await hass.async_block_till_done(wait_background_tasks=True)
            else:
                await _giri_del_ciclo()

    with (
        patch("asyncio.create_subprocess_shell", shell),
        patch.dict(
            sys.modules, {"jsonpath": sys.modules.get("jsonpath") or _jsonpath()}
        ),
    ):
        assert await async_setup_component(hass, "homeassistant", {})
        _, comando = _configurazione_di_oggi()
        assert await async_setup_component(
            hass, "command_line", {"command_line": [{"sensor": comando}]}
        )
        nativa = VMCNativa(
            hass,
            None,
            "nativa",
            "192.168.1.50",
            client=_Client(vmc),
            prova_ping=ping,
            versione=False,
        )
        await nativa.avvia()
        sensori, _ = crea_entita(nativa.stato, nativa.letture_dei_sensori())
        await MockEntityPlatform(
            hass, domain="sensor", platform_name="vmc_master"
        ).async_add_entities([s for s in sensori if s.entity_id == DOMANI_PING])
        await hass.async_block_till_done()

        # passo 3: update_entity con nessun ping in corso
        await avanza(3)
        await aggiorna()
        await hass.async_block_till_done()
        # passo 11: update_entity mentre il ping del giro (passo 10) è in corso
        vmc.accesa = False
        vmc.attesa = asyncio.Event()
        await avanza(11, aspetta=False)
        await aggiorna()
        vmc.attesa.set()
        await hass.async_block_till_done()
        # passo 18: update_entity in corso quando scatta il giro del passo 20
        vmc.attesa = None
        await avanza(18)
        vmc.attesa = asyncio.Event()
        await aggiorna()
        await avanza(20, aspetta=False)
        vmc.attesa.set()
        await hass.async_block_till_done()
        await avanza(22)
        nativa.ferma()

    oggi = [(p, cosa) for p, lato, cosa in visti if lato == "oggi"]
    domani = [(p, cosa) for p, lato, cosa in visti if lato == "domani"]
    assert oggi == [
        (0, "ON-Line"),
        (3, "senza cambio"),
        (3, "senza cambio"),
        (11, "senza cambio"),
        (11, "OFF-Line"),
        (20, "senza cambio"),
        (20, "senza cambio"),
    ]
    assert domani == oggi


async def _giri_del_ciclo() -> None:
    """Qualche giro del ciclo degli eventi, senza aspettare i compiti in corso."""
    for _ in range(20):
        await asyncio.sleep(0)
