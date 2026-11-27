"""b44: il Profilo Inizializzazione parte da solo, una sola volta, per una VMC aggiunta
per la prima volta (scelta del proprietario del 27-11-2026, «Sì, in automatico una
volta»): 140 s dopo l'avvio, appena la VMC è ON-Line (se è spenta aspetta che si accenda).
Mai per una VMC riaggiunta con la sua memoria o passata dalla beta, mai una seconda volta,
anche dopo un riavvio di Home Assistant.

VMC nativa vera (motore tradotto: il pulsante avvia lo script interno), VMC finta che non
risponde alle letture, ping finto."""

from __future__ import annotations

import asyncio
from datetime import timedelta
from unittest.mock import patch

import pytest
from freezegun.api import FrozenDateTimeFactory
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    async_fire_time_changed,
)

from custom_components.vmc_master.const import CONF_DA_INIZIALIZZARE
from custom_components.vmc_master.nativa.letture import LetturaPing
from custom_components.vmc_master.nativa.motore.memoria_interna import (
    CHIAVE_ARCHIVIO as CHIAVE_MEMORIA_INTERNA,
)
from custom_components.vmc_master.nativa.pulsanti import PulsanteVMC

from .banco import ClientFinto, aggiungi_e_avvia, senza_rete, voce

PROFILO = "vmc_master_profilo_inizializzazione"
PING = {"risposta": "ON-Line"}


async def _ping_finto(_self) -> str:
    return PING["risposta"]


@pytest.fixture(autouse=True)
def rete_finta():
    ClientFinto.istanze.clear()
    PING["risposta"] = "ON-Line"
    with senza_rete(), patch.object(LetturaPing, "_async_update_data", _ping_finto):
        yield


@pytest.fixture
def premuti():
    """I pulsanti premuti (unique_id), con la pressione vera."""
    vero = PulsanteVMC.async_press
    elenco: list[str] = []

    async def premi(self: PulsanteVMC) -> None:
        elenco.append(self.unique_id)
        await vero(self)

    with patch.object(PulsanteVMC, "async_press", premi):
        yield elenco


def _nuova() -> MockConfigEntry:
    """La voce di una VMC appena aggiunta dalla finestra «Aggiungi integrazione»."""
    return voce("master", **{CONF_DA_INIZIALIZZARE: True})


async def _lascia_girare() -> None:
    """Il ciclo degli eventi gira senza aspettare gli script fermi nelle loro pause
    (con l'orologio fermo async_block_till_done non finirebbe)."""
    for _ in range(200):
        await asyncio.sleep(0)


async def _avanza(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory, secondi: int, passo: int = 5
) -> None:
    for _ in range(0, secondi, passo):
        freezer.tick(timedelta(seconds=passo))
        async_fire_time_changed(hass)
        await _lascia_girare()


async def _avvia(hass: HomeAssistant, voci: list) -> None:
    for componente in ("homeassistant", "persistent_notification"):
        assert await async_setup_component(hass, componente, {})
    await aggiungi_e_avvia(hass, voci)


async def test_vmc_nuova_una_volta_dopo_140_s(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory, premuti: list[str]
) -> None:
    nuova = _nuova()
    await _avvia(hass, [nuova])
    await _avanza(hass, freezer, 135)
    assert premuti == []
    assert nuova.data[CONF_DA_INIZIALIZZARE] is True
    assert hass.states.get("switch.vmc_master_notifica_status_vmc").state == "off"
    await _avanza(hass, freezer, 10)
    assert premuti == [PROFILO]
    assert CONF_DA_INIZIALIZZARE not in nuova.data
    # il profilo è partito davvero: alla fine accende Invio Notifica (Notifica Status VMC)
    await _avanza(hass, freezer, 30)
    assert hass.states.get("switch.vmc_master_notifica_status_vmc").state == "on"
    # mai una seconda volta, anche dopo una ricarica (come un riavvio)
    assert await hass.config_entries.async_reload(nuova.entry_id)
    await _lascia_girare()
    await _avanza(hass, freezer, 300, 20)
    assert premuti == [PROFILO]


async def test_vmc_spenta_aspetta_che_si_accenda(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory, premuti: list[str]
) -> None:
    PING["risposta"] = "OFF-Line"
    nuova = _nuova()
    await _avvia(hass, [nuova])
    await _avanza(hass, freezer, 600, 20)
    assert premuti == []
    assert nuova.data[CONF_DA_INIZIALIZZARE] is True
    PING["risposta"] = "ON-Line"  # la VMC si accende: il ping la vede entro 10 s
    await _avanza(hass, freezer, 20)
    assert premuti == [PROFILO]
    assert CONF_DA_INIZIALIZZARE not in nuova.data


async def test_ferma_prima_dei_140_s(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory, premuti: list[str]
) -> None:
    """VMC scaricata (o Home Assistant fermo) prima dei 140 s: non parte; la voce lo
    chiede ancora e parte al prossimo avvio."""
    nuova = _nuova()
    await _avvia(hass, [nuova])
    await _avanza(hass, freezer, 60, 20)
    assert await hass.config_entries.async_unload(nuova.entry_id)
    await _lascia_girare()
    await _avanza(hass, freezer, 300, 20)
    assert premuti == []
    assert nuova.state is ConfigEntryState.NOT_LOADED
    assert nuova.data[CONF_DA_INIZIALIZZARE] is True
    assert await hass.config_entries.async_setup(nuova.entry_id)
    await _lascia_girare()
    await _avanza(hass, freezer, 160, 20)
    assert premuti == [PROFILO]


async def test_vmc_riaggiunta_con_la_sua_memoria(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory, premuti: list[str], hass_storage
) -> None:
    """VMC eliminata e aggiunta di nuovo entro 7 giorni: tiene i suoi valori, niente
    Profilo Inizializzazione."""
    chiave = CHIAVE_MEMORIA_INTERNA.format(nome="master")
    hass_storage[chiave] = {
        "version": 1,
        "minor_version": 1,
        "key": chiave,
        "data": {"eliminata": dt_util.utcnow().isoformat()},
    }
    nuova = _nuova()
    await _avvia(hass, [nuova])
    assert CONF_DA_INIZIALIZZARE not in nuova.data
    await _avanza(hass, freezer, 300, 20)
    assert premuti == []


async def test_vmc_gia_presente_senza_richiesta(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory, premuti: list[str]
) -> None:
    """Una voce senza la richiesta (VMC aggiunta prima della b44, o passata dalla
    beta): niente Profilo Inizializzazione."""
    await _avvia(hass, [voce("master")])
    await _avanza(hass, freezer, 300, 20)
    assert premuti == []
