"""b44: gli avvisi «Aggiornare Manualmente l'Entità…» e «Nessun cellulare…» compaiono
all'avvio di Home Assistant, con la VMC di nuovo ON-Line, accendendo Invio Notifica e con
Agg. Sensori; aprendo la finestra Opzioni gli elenchi si aggiornano senza avvisi (prova
del proprietario del 27-11-2026: l'avviso tornava a ogni apertura della finestra).

VMC nativa vera (motore tradotto, script interni con le variabili di script.turn_on), VMC
finta che non risponde alle letture, ping ON-Line."""

from __future__ import annotations

import asyncio
from datetime import timedelta
from unittest.mock import AsyncMock, patch

import pytest
from freezegun.api import FrozenDateTimeFactory
from homeassistant.components import persistent_notification as pn
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import async_fire_time_changed

from custom_components.vmc_master.nativa.letture import LetturaPing

from .banco import ClientFinto, aggiungi_e_avvia, senza_rete, voce

# Gli avvisi degli elenchi senza una scelta: 4 sensori (Temperatura Esterna e Interna,
# Umidità Interna, CO₂ Interna: nell'elenco c'è sempre la sonda della VMC) e il cellulare;
# l'Umidità Esterna non ha una sonda nella VMC, senza sensori l'elenco è vuoto e non avvisa
AVVISI = {
    "vmc_master_aggiorna_entita_temperatura_esterna",
    "vmc_master_aggiorna_entita_temperatura_interna",
    "vmc_master_aggiorna_entita_umidita_interna",
    "vmc_master_aggiorna_entita_co2_interna",
    "vmc_master_aggiorna_entita_dispositivo_notifica",
}


@pytest.fixture(autouse=True)
def rete_finta():
    ClientFinto.istanze.clear()
    with (
        senza_rete(),
        patch.object(
            LetturaPing, "_async_update_data", AsyncMock(return_value="ON-Line")
        ),
    ):
        yield


def _avvisi(hass: HomeAssistant) -> set[str]:
    """Le notifiche persistenti di adesso (notification_id)."""
    return set(pn._async_get_or_create_notifications(hass))


def _togli_avvisi(hass: HomeAssistant) -> None:
    for avviso in _avvisi(hass):
        pn.async_dismiss(hass, avviso)


async def _avanza(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory, secondi: int, passo: int = 2
) -> None:
    """Avanza di ``secondi`` a passi di ``passo`` secondi (le pause degli script, 2 s e
    3 s, partono una dopo l'altra)."""
    for _ in range(0, secondi, passo):
        freezer.tick(timedelta(seconds=passo))
        async_fire_time_changed(hass)
        await _lascia_girare()


async def _lascia_girare() -> None:
    """Lascia girare il ciclo degli eventi senza aspettare la fine di tutto
    (async_block_till_done aspetterebbe anche gli script fermi nelle loro pause, che con
    l'orologio fermo non finiscono)."""
    for _ in range(200):
        await asyncio.sleep(0)


async def _cambia(hass: HomeAssistant, entity_id: str, servizio: str) -> None:
    await hass.services.async_call("switch", servizio, {"entity_id": entity_id})
    await _lascia_girare()


async def test_avvisi_non_a_ogni_apertura_della_finestra_opzioni(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory
) -> None:
    for componente in ("homeassistant", "persistent_notification"):
        assert await async_setup_component(hass, componente, {})
    master = voce("master")
    await aggiungi_e_avvia(hass, [master])
    await _avanza(hass, freezer, 200, 20)  # avvio della VMC (140 s) e prime letture
    _togli_avvisi(hass)
    invio = "switch.vmc_master_notifica_status_vmc"
    opzioni = "switch.vmc_master_opzioni_offset_sensori"

    # Invio Notifica acceso: gli avvisi compaiono
    await _cambia(hass, invio, "turn_off")
    await _cambia(hass, invio, "turn_on")
    await _avanza(hass, freezer, 10)
    assert _avvisi(hass) >= AVVISI
    _togli_avvisi(hass)

    # finestra Opzioni aperta (due volte): gli elenchi si aggiornano, nessun avviso
    for _volta in range(2):
        await _cambia(hass, opzioni, "turn_on")
        await _avanza(hass, freezer, 10)
        assert not _avvisi(hass) & AVVISI
        await _cambia(hass, opzioni, "turn_off")
        await _avanza(hass, freezer, 2)

    # un avviso già comparso resta, aprendo la finestra non si toglie
    await _cambia(hass, invio, "turn_off")
    await _cambia(hass, invio, "turn_on")
    await _avanza(hass, freezer, 10)
    await _cambia(hass, opzioni, "turn_on")
    await _avanza(hass, freezer, 10)
    assert _avvisi(hass) >= AVVISI
