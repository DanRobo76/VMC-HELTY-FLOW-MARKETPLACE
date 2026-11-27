"""b44: a un IP che non risponde come una VMC si guarda se c'è comunque un apparecchio
acceso (porta 5001 che si apre o rifiuta il collegamento, poi il ping). Se c'è, non è una
VMC: per esempio il router, scritto al posto dell'IP della VMC nella prova del
proprietario del 27-11-2026, che si poteva aggiungere con «Aggiungi comunque». Se non
risponde niente, la VMC è spenta o l'IP è sbagliato.

Stesso controllo in tutte le finestre che leggono il nome a un IP (in_rete, ip_fisso,
cambia_ip) e nel servizio verifica_ip del campo «Cambia IP VMC» della scheda: lo fa
async_nome_vmc_due_prove."""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.setup import async_setup_component

from custom_components.vmc_master import config_flow
from custom_components.vmc_master.const import DOMAIN

from .test_b22_core import _apri_cambia_ip

NOME_VMC = "custom_components.vmc_master.config_flow.async_nome_vmc"
PRESENTE = "custom_components.vmc_master.config_flow.async_apparecchio_presente"
# funzione vera: tests/conftest.py la sostituisce in tutte le prove (non risponde niente)
PRESENTE_VERO = config_flow.async_apparecchio_presente
IP = "192.168.1.1"


@pytest.fixture(autouse=True)
def _nessuna_vmc_in_rete():
    """All'avvio di una VMC il nome non si legge (nessuna VMC vera)."""
    with patch(NOME_VMC, AsyncMock(return_value=None)):
        yield


class ScrittoreFinto:
    chiuso = False

    def close(self) -> None:
        self.chiuso = True


class ProcessoFinto:
    """Il comando ping: finisce con ``codice`` dopo ``durata`` secondi (subito se ucciso)."""

    def __init__(self, codice: int, durata: float = 0) -> None:
        self.codice, self.durata, self.ucciso = codice, durata, False

    async def wait(self) -> int:
        if self.durata and not self.ucciso:
            await asyncio.sleep(self.durata)
        return -9 if self.ucciso else self.codice

    def kill(self) -> None:
        self.ucciso = True


def _asyncio_finto(apri, avvia) -> SimpleNamespace:
    """asyncio di config_flow con collegamento e comando ping finti (solo lì)."""
    return SimpleNamespace(
        open_connection=apri,
        wait_for=asyncio.wait_for,
        timeout=asyncio.timeout,
        create_subprocess_exec=avvia,
        subprocess=asyncio.subprocess,
    )


def _apri_con(errore: BaseException | None = None, scrittore=None):
    async def apri(ip, porta):
        assert (ip, porta) == (IP, 5001)
        if errore is not None:
            raise errore
        return object(), scrittore

    return apri


async def _presente(apri, avvia) -> bool:
    with patch.object(config_flow, "asyncio", _asyncio_finto(apri, avvia)):
        return await PRESENTE_VERO(IP)


async def test_porta_che_rifiuta_e_un_apparecchio() -> None:
    """La porta 5001 rifiuta il collegamento: c'è un apparecchio, senza ping."""
    avvia = AsyncMock()
    assert await _presente(_apri_con(ConnectionRefusedError()), avvia) is True
    avvia.assert_not_called()


async def test_porta_che_si_apre_e_un_apparecchio() -> None:
    """La porta 5001 si apre (ma il nome della VMC non arriva): c'è un apparecchio."""
    scrittore, avvia = ScrittoreFinto(), AsyncMock()
    assert await _presente(_apri_con(scrittore=scrittore), avvia) is True
    assert scrittore.chiuso
    avvia.assert_not_called()


@pytest.mark.parametrize(
    ("errore_porta", "codice_ping", "atteso"),
    [
        (TimeoutError(), 0, True),  # porta muta, risponde al ping
        (OSError(113, "No route to host"), 0, True),
        (TimeoutError(), 1, False),  # non risponde niente
        (OSError(113, "No route to host"), 1, False),
        (TimeoutError(), 2, False),  # errore del comando ping
    ],
)
async def test_porta_muta_decide_il_ping(
    errore_porta: BaseException, codice_ping: int, atteso: bool
) -> None:
    avvia = AsyncMock(return_value=ProcessoFinto(codice_ping))
    assert await _presente(_apri_con(errore_porta), avvia) is atteso
    avvia.assert_awaited_once_with(
        "ping",
        "-q",
        "-c",
        "2",
        "-W",
        "1",
        IP,
        stdin=asyncio.subprocess.DEVNULL,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL,
    )


async def test_porta_che_non_risponde_in_tempo() -> None:
    """La porta 5001 non risponde entro ATTESA_PORTA: si prova il ping."""

    async def apri_senza_fine(_ip, _porta):
        await asyncio.sleep(10)

    avvia = AsyncMock(return_value=ProcessoFinto(1))
    with patch.object(config_flow, "ATTESA_PORTA", 0.01):
        assert await _presente(apri_senza_fine, avvia) is False
    avvia.assert_awaited_once()


async def test_ping_che_manca() -> None:
    """Senza il comando ping decide solo la porta 5001."""
    avvia = AsyncMock(side_effect=FileNotFoundError("ping"))
    assert await _presente(_apri_con(TimeoutError()), avvia) is False


async def test_ping_che_non_finisce() -> None:
    """Un ping che non finisce entro ATTESA_PING si ferma: non risponde niente."""
    processo = ProcessoFinto(0, durata=10)
    with patch.object(config_flow, "ATTESA_PING", 0.01):
        assert (
            await _presente(_apri_con(TimeoutError()), AsyncMock(return_value=processo))
            is False
        )
    assert processo.ucciso


@pytest.mark.parametrize(
    ("letti", "presente", "atteso", "controlli"),
    [
        ([None, None], True, "", 1),  # un apparecchio che non è una VMC (il router)
        ([None, None], False, None, 1),  # non risponde niente
        ([None, "VMC Sala"], True, "VMC Sala", 0),  # risponde alla seconda prova
        ([""], True, "", 0),  # risponde sulla 5001 senza il nome della VMC
        (["VMC Sala"], True, "VMC Sala", 0),
    ],
)
async def test_nome_due_prove_e_apparecchio(
    letti: list[str | None], presente: bool, atteso: str | None, controlli: int
) -> None:
    controllo = AsyncMock(return_value=presente)
    with patch(NOME_VMC, AsyncMock(side_effect=letti)), patch(PRESENTE, controllo):
        assert await config_flow.async_nome_vmc_due_prove(IP) == atteso
    assert controllo.await_count == controlli
    if controlli:
        controllo.assert_awaited_with(IP)


async def _ip_della_prima_vmc(hass: HomeAssistant, ip: str):
    risultato = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    risultato = await hass.config_entries.flow.async_configure(
        risultato["flow_id"], {"next_step_id": "in_rete"}
    )
    return await hass.config_entries.flow.async_configure(
        risultato["flow_id"], {"host": ip}
    )


@pytest.mark.parametrize(("letto", "presente"), [(None, True), ("", False)])
async def test_aggiungi_un_ip_che_non_e_una_vmc(
    hass: HomeAssistant, letto: str | None, presente: bool
) -> None:
    """L'IP del router (risponde al ping, non sulla 5001) o di un apparecchio che risponde
    sulla 5001 senza il nome della VMC: errore sotto l'IP, nessun «Aggiungi comunque». Lo
    stesso IP si può riscrivere per riprovare; con l'IP della VMC si va avanti."""
    with patch(NOME_VMC, AsyncMock(return_value=letto)), patch(
        PRESENTE, AsyncMock(return_value=presente)
    ):
        risultato = await _ip_della_prima_vmc(hass, IP)
        assert risultato["type"] is FlowResultType.FORM
        assert risultato["step_id"] == "in_rete"
        assert risultato["errors"] == {"host": "non_e_una_vmc"}
        assert risultato["data_schema"]({})["host"] == IP  # l'IP scritto resta
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"host": IP}
        )
        assert risultato["errors"] == {"host": "non_e_una_vmc"}
    with patch(NOME_VMC, AsyncMock(return_value="VMC Soggiorno")):
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"host": "192.168.1.160"}
        )
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    assert risultato["data"] == {
        "nome": "master",
        "host": "192.168.1.160",
        "titolo": "VMC Soggiorno",
        "da_inizializzare": True,
    }


async def test_aggiungi_un_ip_dove_non_risponde_niente(hass: HomeAssistant) -> None:
    """Non risponde niente (VMC spenta o IP sbagliato): «VMC non raggiungibile», con
    «Correggi l'IP» e «Aggiungi comunque»."""
    with patch(NOME_VMC, AsyncMock(return_value=None)):
        risultato = await _ip_della_prima_vmc(hass, "192.168.1.160")
    assert risultato["type"] is FlowResultType.MENU
    assert risultato["step_id"] == "non_raggiungibile"
    assert risultato["menu_options"] == ["in_rete", "aggiungi_comunque"]


async def test_cambia_ip_con_un_apparecchio_che_non_e_una_vmc(hass: HomeAssistant) -> None:
    """Ingranaggio «Cambia l'IP della VMC»: l'IP del router non si salva, neppure premendo
    di nuovo Invia (si salva così solo un IP dove non risponde niente)."""
    voce, risultato = await _apri_cambia_ip(hass)
    with patch(NOME_VMC, AsyncMock(return_value=None)), patch(
        PRESENTE, AsyncMock(return_value=True)
    ):
        for _volta in range(2):
            risultato = await hass.config_entries.options.async_configure(
                risultato["flow_id"], {"host": IP}
            )
            assert risultato["type"] is FlowResultType.FORM
            assert risultato["errors"] == {"host": "ip_altro_dispositivo"}
    assert voce.data["host"] == "192.168.1.161"


@pytest.mark.parametrize(
    ("presente", "risposta"),
    [
        (True, {"risponde": True, "nome": "", "esito": "altro_dispositivo"}),
        (False, {"risponde": False, "nome": "", "esito": "non_risponde"}),
    ],
)
async def test_servizio_verifica_ip(
    hass: HomeAssistant, presente: bool, risposta: dict
) -> None:
    """Campo «Cambia IP VMC» della scheda: sotto il campo «Non è una VMC» per il router,
    «VMC non risponde» se non risponde niente."""
    assert await async_setup_component(hass, DOMAIN, {})
    with patch(NOME_VMC, AsyncMock(return_value=None)), patch(
        PRESENTE, AsyncMock(return_value=presente)
    ):
        assert (
            await hass.services.async_call(
                DOMAIN,
                "verifica_ip",
                {"ip": IP, "nome": ""},
                blocking=True,
                return_response=True,
            )
            == risposta
        )
