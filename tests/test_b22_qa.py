"""Test mirati sulle parti che nessun altro test protegge (audit 18-11-2026, M-3):
vista della scheda (autenticazione e dominio), notifica di migrazione, lettura del
nome della VMC sulla rete (async_nome_vmc vera, contro un server TCP finto)."""

from __future__ import annotations

import asyncio
import contextlib
from collections.abc import AsyncIterator, Awaitable, Callable
from unittest.mock import patch

import pytest
from homeassistant.components import persistent_notification
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.vmc_master import config_flow
from custom_components.vmc_master.const import DOMAIN

NOME_VMC = "custom_components.vmc_master.config_flow.async_nome_vmc"
# solo socket verso 127.0.0.1 (il plugin dei test blocca tutti gli altri)
RETE_LOCALE = pytest.mark.usefixtures("socket_enabled")


async def _master(hass: HomeAssistant) -> MockConfigEntry:
    voce = MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    )
    voce.add_to_hass(hass)
    with patch(NOME_VMC, return_value=None):
        assert await hass.config_entries.async_setup(voce.entry_id)
        await hass.async_block_till_done()
    return voce


# --- Vista della scheda --------------------------------------------------------------


async def test_scheda_solo_con_login(hass: HomeAssistant, hass_client_no_auth) -> None:
    """Senza login la configurazione della scheda (IP ed entità della VMC) non si legge."""
    assert await async_setup_component(hass, "http", {})
    voce = await _master(hass)
    client = await hass_client_no_auth()
    risposta = await client.get(f"/api/vmc_master/scheda/{voce.entry_id}")
    assert risposta.status == 401
    assert "192.168.1.160" not in await risposta.text()


async def test_scheda_di_un_altra_integrazione(hass: HomeAssistant, hass_client) -> None:
    """L'id di una voce di un'altra integrazione dà «non trovata», non un errore."""
    await _master(hass)
    altra = MockConfigEntry(domain="altro", data={"host": "192.168.1.50"})
    altra.add_to_hass(hass)
    client = await hass_client()
    risposta = await client.get(f"/api/vmc_master/scheda/{altra.entry_id}")
    assert risposta.status == 404


# --- Notifica di migrazione ----------------------------------------------------------


async def test_nessuna_notifica_senza_migrazione(hass: HomeAssistant) -> None:
    await _master(hass)
    notifiche = persistent_notification._async_get_or_create_notifications(hass)
    assert f"{DOMAIN}_migrazione_master" not in notifiche


# --- async_nome_vmc contro un server TCP finto su 127.0.0.1 ---------------------------


@contextlib.asynccontextmanager
async def _vmc_finta(
    risponde: Callable[[asyncio.StreamReader, asyncio.StreamWriter], Awaitable[None]],
) -> AsyncIterator[list[bytes]]:
    """Server sulla porta della VMC (una porta libera di 127.0.0.1): restituisce i
    comandi ricevuti."""
    ricevuti: list[bytes] = []

    async def gestisci(lettore: asyncio.StreamReader, scrittore: asyncio.StreamWriter) -> None:
        ricevuti.append(await lettore.read(64))
        try:
            await risponde(lettore, scrittore)
        finally:
            scrittore.close()

    server = await asyncio.start_server(gestisci, "127.0.0.1", 0)
    porta = server.sockets[0].getsockname()[1]
    try:
        with patch.object(config_flow, "PORTA_VMC", porta):
            yield ricevuti
    finally:
        server.close()
        await server.wait_closed()


def _risposta(dati: bytes):
    async def risponde(_lettore, scrittore: asyncio.StreamWriter) -> None:
        scrittore.write(dati)
        await scrittore.drain()

    return risponde


@RETE_LOCALE
@pytest.mark.parametrize(
    ("dati", "nome"),
    [
        (b"VMNM Zona Giorno", "Zona Giorno"),
        (b"VMNM Sala*******", "Sala"),
        (b"VMNM Sala\r\n", "Sala"),
        (b"VMNM ", ""),
        (b"OK", ""),
        (b"VMNMSala", ""),
    ],
)
async def test_nome_letto_dalla_vmc(dati: bytes, nome: str) -> None:
    """«VMNM ‹nome›» → nome (senza asterischi e a capo); un'altra risposta → "" (risponde
    ma non è una VMC)."""
    async with _vmc_finta(_risposta(dati)) as ricevuti:
        assert await config_flow.async_nome_vmc("127.0.0.1") == nome
    assert ricevuti == [b"VMNM?"]


@RETE_LOCALE
async def test_nome_vmc_chiusura_senza_risposta() -> None:
    async with _vmc_finta(_risposta(b"")):
        assert await config_flow.async_nome_vmc("127.0.0.1") is None


@RETE_LOCALE
async def test_nome_vmc_senza_risposta_entro_il_timeout() -> None:
    async def muta(lettore: asyncio.StreamReader, _scrittore) -> None:
        await lettore.read(64)  # aspetta che il client chiuda

    async with _vmc_finta(muta):
        with patch.object(config_flow, "TIMEOUT_VMC", 0.2):
            inizio = asyncio.get_running_loop().time()
            assert await config_flow.async_nome_vmc("127.0.0.1") is None
            assert asyncio.get_running_loop().time() - inizio < 2


@RETE_LOCALE
async def test_nome_vmc_porta_chiusa() -> None:
    with patch.object(config_flow, "PORTA_VMC", _porta_libera()):
        assert await config_flow.async_nome_vmc("127.0.0.1") is None


@RETE_LOCALE
async def test_prova_vmc_solo_con_un_nome() -> None:
    async with _vmc_finta(_risposta(b"VMNM Sala")):
        assert await config_flow.async_prova_vmc("127.0.0.1") is True
    async with _vmc_finta(_risposta(b"VMNM ")):
        assert await config_flow.async_prova_vmc("127.0.0.1") is False


def _porta_libera() -> int:
    import socket

    with socket.socket() as prova:
        prova.bind(("127.0.0.1", 0))
        return prova.getsockname()[1]
