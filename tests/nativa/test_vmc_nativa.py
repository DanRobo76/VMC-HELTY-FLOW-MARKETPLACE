"""Una VMC nativa completa con una VMC finta: letture, memoria, avvio, entità."""

from __future__ import annotations

from datetime import timedelta

import pytest
from homeassistant.const import EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STARTED
from homeassistant.core import CoreState, HomeAssistant, State
from homeassistant.helpers import restore_state
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import MockEntityPlatform

from custom_components.vmc_master.nativa.entita import crea_entita
from custom_components.vmc_master.nativa.letture import URL_VERSIONE
from custom_components.vmc_master.nativa.vmc import VMCNativa

from .test_client import VMGH, VMGI, VmcFinta

pytestmark = pytest.mark.usefixtures("socket_enabled")


def _vmgh(codice: int) -> bytes:
    return (f"VMGO,{codice:05d}" + ",00000" * 13).encode()


@pytest.fixture
async def vmc_finta():
    finta = VmcFinta(
        {
            "VMGH?": VMGH.encode(),
            "VMGI?": VMGI.encode(),
            "VMNM?": b"VMNM Master",
            "VMSL?": b"Rete",
        }
    )
    finta.porta = await finta.avvia()
    yield finta
    await finta.ferma()


def _ricorda(hass: HomeAssistant, stati: list[State]) -> None:
    """Gli ultimi stati di «prima del riavvio» nella memoria del ripristino di Home Assistant.

    Nel 2026.11 la memoria è per voce del registro delle entità (uno stato salvato per
    entity_id passa alla voce del registro quando l'entità viene registrata) e non ha più
    ``last_states``: ``mock_restore_cache`` del plugin di prova scrive ancora quello, che
    Home Assistant non legge più, quindi qui si riempie la memoria vera.
    """
    memoria = restore_state.async_get(hass)
    for stato in stati:
        memoria.last_states_by_entity_id[stato.entity_id] = restore_state.StoredState(
            stato, None, dt_util.utcnow()
        )


async def _porta_chiusa() -> int:
    """Una porta locale su cui non ascolta nessuno."""
    import asyncio

    server = await asyncio.start_server(lambda r, w: None, "127.0.0.1", 0)
    porta = server.sockets[0].getsockname()[1]
    server.close()
    await server.wait_closed()
    return porta


async def _prepara(
    hass: HomeAssistant, vmc_finta: VmcFinta, aioclient_mock
) -> VMCNativa:
    from custom_components.vmc_master.nativa.client import ClientVMC

    aioclient_mock.get(URL_VERSIONE, json={"tag_name": "v9.0.0b42"})

    async def ping(host: str) -> bool:
        return True

    vmc = VMCNativa(
        hass,
        None,
        "master",
        "127.0.0.1",
        client=ClientVMC("127.0.0.1", vmc_finta.porta, attesa=0.3),
        prova_ping=ping,
    )
    sensori, binari = crea_entita(vmc.stato, vmc.letture_dei_sensori())
    await MockEntityPlatform(
        hass, domain="sensor", platform_name="vmc_master"
    ).async_add_entities(sensori)
    await MockEntityPlatform(
        hass, domain="binary_sensor", platform_name="vmc_master"
    ).async_add_entities(binari)
    return vmc


@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_avvio_e_letture(
    hass: HomeAssistant, vmc_finta: VmcFinta, aioclient_mock, freezer
) -> None:
    """Avvio di Home Assistant: memoria ripristinata, regola di avvio, poi letture e interruzioni."""
    freezer.move_to("2026-11-25 10:00:00+00:00")
    _ricorda(
        hass,
        [
            State(
                "sensor.vmc_master_status_ventola_memorizzata",
                _vmgh(3).decode(),
                {"lettura_prima_dell_interruzione": ""},
            ),
            State("sensor.vmc_master_nome_memorizzata", "VMNM Sala"),
            State("sensor.vmc_master_temp_interna_media_4w", "21.35"),
        ],
    )
    hass.set_state(CoreState.not_running)
    vmc = await _prepara(hass, vmc_finta, aioclient_mock)
    await vmc.avvia()
    await hass.async_block_till_done()
    s = hass.states.get
    # prima dell'avvio: letture sì, «ultima lettura valida» ancora quella conservata
    assert s("sensor.vmc_master_status_ventola").state == VMGH
    assert s("sensor.vmc_master_status_ventola_memorizzata").state == _vmgh(3).decode()
    assert s("sensor.vmc_master_nome_memorizzata").state == "VMNM Sala"
    assert s("sensor.vmc_master_sensori_memorizzata").state == "unknown"
    assert s("sensor.vmc_master_temp_interna_media_4w").state == "21.35"
    assert s("sensor.vmc_master_lan").state == "Rete"
    assert s("sensor.vmc_master_status_ip").state == "ON-Line"
    assert s("sensor.vmc_master_versione_repository").state == "v9.0.0b42"
    ripristino = vmc.stato.voce("sensor.status_ventola_memorizzata").cambiato

    # all'avvio le letture memorizzate cominciano a seguire le letture; la regola di avvio
    # vale quando l'avvio è finito (come il trigger «homeassistant: start» di oggi)
    hass.set_state(CoreState.starting)
    hass.bus.async_fire(EVENT_HOMEASSISTANT_START)
    await hass.async_block_till_done()
    assert s("sensor.vmc_master_status_ventola_memorizzata").state == _vmgh(3).decode()
    assert s("sensor.vmc_master_nome_memorizzata").state == "VMNM Sala"
    hass.set_state(CoreState.running)
    hass.bus.async_fire(EVENT_HOMEASSISTANT_STARTED)
    await hass.async_block_till_done()
    memoria = s("sensor.vmc_master_status_ventola_memorizzata")
    assert memoria.state == VMGH
    assert (
        memoria.attributes["lettura_prima_dell_interruzione"]
        == f"00003|{round(ripristino.timestamp(), 1)}"
    )
    assert memoria.attributes["icon"] == "mdi:content-save-outline"
    assert s("sensor.vmc_master_nome_memorizzata").state == "VMNM Master"
    assert s("sensor.vmc_master_sensori_memorizzata").state == VMGI
    # medie: senza registro recorder.get_statistics non c'è e l'azione di oggi si ferma
    # (servizio inesistente: continue_on_error non basta), le medie restano quelle di prima
    assert s("sensor.vmc_master_temp_interna_media_4w").state == "21.35"
    assert s("sensor.vmc_master_rischio_muffa_giorni_dati").state == "unknown"
    assert (
        s("sensor.vmc_master_temp_interna_media_4w").attributes["unit_of_measurement"]
        == "°C"
    )

    # la VMC cambia velocità: nuova lettura valida, nessuna interruzione
    freezer.tick(timedelta(seconds=5))
    vmc_finta.risposte["VMGH?"] = _vmgh(4)
    await vmc.letture["sensor.status_ventola"].async_refresh()
    await hass.async_block_till_done()
    memoria = s("sensor.vmc_master_status_ventola_memorizzata")
    assert memoria.state == _vmgh(4).decode()
    assert memoria.attributes["lettura_prima_dell_interruzione"] == ""
    cambio = memoria.last_changed

    # la VMC non risponde (porta chiusa: con l'ora ferma le attese non scadrebbero mai)
    freezer.tick(timedelta(seconds=5))
    porta = vmc.client.porta
    vmc.client.porta = await _porta_chiusa()
    await vmc.letture["sensor.status_ventola"].async_refresh()
    await hass.async_block_till_done()
    assert s("sensor.vmc_master_status_ventola").state == "unavailable"
    assert s("sensor.vmc_master_status_ventola_memorizzata").state == _vmgh(4).decode()

    # torna con la stessa velocità: interruzione con codice e ora dell'ultima lettura valida
    freezer.tick(timedelta(seconds=5))
    vmc.client.porta = porta
    await vmc.letture["sensor.status_ventola"].async_refresh()
    await hass.async_block_till_done()
    memoria = s("sensor.vmc_master_status_ventola_memorizzata")
    assert memoria.state == _vmgh(4).decode()
    assert (
        memoria.attributes["lettura_prima_dell_interruzione"]
        == f"00004|{round(cambio.timestamp(), 1)}"
    )
    assert memoria.last_changed == cambio
    # i sensori calcolati seguono le letture
    assert (
        s("sensor.vmc_master_status_ventola_lettura_codice_interpretato").state
        == "Velocità 4"
    )
    assert s("sensor.vmc_master_status_ip_interfaccia").state == "ON-Line"
    vmc.ferma()


@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_ricarica_senza_regola_di_avvio(
    hass: HomeAssistant, vmc_finta: VmcFinta, aioclient_mock
) -> None:
    """Home Assistant già avviato (ricarica): nessuna regola di avvio, letture subito attive."""
    _ricorda(
        hass, [State("sensor.vmc_master_status_ventola_memorizzata", _vmgh(3).decode())]
    )
    vmc = await _prepara(hass, vmc_finta, aioclient_mock)
    await vmc.avvia()
    await hass.async_block_till_done()
    assert (
        hass.states.get("sensor.vmc_master_status_ventola_memorizzata").state
        == _vmgh(3).decode()
    )
    vmc_finta.risposte["VMGH?"] = _vmgh(1)
    await vmc.letture["sensor.status_ventola"].async_refresh()
    await hass.async_block_till_done()
    assert (
        hass.states.get("sensor.vmc_master_status_ventola_memorizzata").state
        == _vmgh(1).decode()
    )
    vmc.ferma()
