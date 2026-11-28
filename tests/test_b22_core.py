"""Prove della 9.0.0b22 (audit tecnico del 18-11-2026): M-1, B-1..B-6 e il messaggio finale
dopo l'aggiunta di una VMC. B-9 (il filtro degli errori dei sensori TCP del package nel log)
non c'è più dalla b48: la VMC nativa non usa i sensori TCP."""

from __future__ import annotations

import errno
import hashlib
import json
import time
from pathlib import Path
from unittest.mock import patch

import pytest
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.helpers import issue_registry as ir
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.vmc_master.config_flow import async_nome_vmc as _NOME_VERO
from custom_components.vmc_master.config_flow import ip_valido
from custom_components.vmc_master.const import DOMAIN

NOME_VMC = "custom_components.vmc_master.config_flow.async_nome_vmc"
PI = "custom_components.vmc_master.prima_installazione"
CARTELLA = Path(__file__).parent.parent / "custom_components" / "vmc_master"
# Controllo della configurazione fatto dalla riparazione «Riavviare» prima del riavvio
CONTROLLO_CONFIG = "homeassistant.config.async_check_ha_config_file"


@pytest.fixture(autouse=True)
def _nessuna_vmc_in_rete():
    with patch(NOME_VMC, return_value=None):
        yield


def _impronte(cartella: Path) -> dict[str, str]:
    return {
        f.name: hashlib.md5(f.read_bytes()).hexdigest()
        for f in sorted(cartella.iterdir())
        if f.is_file()
    }


def _disco_pieno(*_args, **_kwargs):
    raise OSError(errno.ENOSPC, "No space left on device")


# ---- M-1: scritture atomiche ---------------------------------------------------------


# ---- B-1: IP dalla scheda con le voci avviate in parallelo ---------------------------


# ---- B-2: IP che non possono essere di una VMC ----------------------------------------


@pytest.mark.parametrize(
    "ip",
    [
        "0.0.0.0",
        "0.1.2.3",
        "127.0.0.1",
        "127.255.255.254",
        "255.255.255.255",
        "224.0.0.1",
        "239.255.255.250",
        "240.0.0.1",
        "169.254.1.1",
        "192.168.1.010",
        "999.999.999.999",
        "192.168.1",
    ],
)
def test_ip_non_valido(ip: str) -> None:
    assert not ip_valido(ip)


@pytest.mark.parametrize(
    "ip", ["192.168.1.160", "10.0.0.1", "172.16.5.4", "100.64.0.1", "8.8.8.8", "192.168.1.255"]
)
def test_ip_valido_privati_e_pubblici(ip: str) -> None:
    assert ip_valido(ip)


@pytest.mark.parametrize("lingua", ["it", "en"])
def test_testo_ip_non_valido(lingua: str) -> None:
    dati = json.loads((CARTELLA / "translations" / f"{lingua}.json").read_text(encoding="utf-8"))
    for sezione in ("config", "options"):
        testo = dati[sezione]["error"]["ip_non_valido"]
        assert "127.x.x.x" in testo and "224.0.0.0" in testo


async def test_in_rete_rifiuta_l_ip_riservato(hass: HomeAssistant) -> None:
    from homeassistant import config_entries

    risultato = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    risultato = await hass.config_entries.flow.async_configure(
        risultato["flow_id"], {"next_step_id": "in_rete"}
    )
    risultato = await hass.config_entries.flow.async_configure(
        risultato["flow_id"], {"host": "127.0.0.1"}
    )
    assert risultato["type"] is FlowResultType.FORM
    assert risultato["errors"] == {"host": "ip_non_valido"}


# ---- B-3: «Cambia l'IP» con la prima lettura persa ------------------------------------


async def _apri_cambia_ip(hass: HomeAssistant) -> tuple[MockConfigEntry, dict]:
    voce = MockConfigEntry(
        domain=DOMAIN, unique_id="zona", title="VMC Zona Giorno",
        data={"nome": "zona", "host": "192.168.1.161", "titolo": "VMC Zona Giorno"},
    )
    voce.add_to_hass(hass)
    assert await hass.config_entries.async_setup(voce.entry_id)
    await hass.async_block_till_done()
    risultato = await hass.config_entries.options.async_init(voce.entry_id)
    risultato = await hass.config_entries.options.async_configure(
        risultato["flow_id"], {"next_step_id": "cambia_ip"}
    )
    return voce, risultato


@pytest.mark.parametrize(
    ("seconda", "errore"),
    [("VMC Altra Zona", "ip_nome_diverso"), ("", "ip_altro_dispositivo"), (None, "ip_non_risponde")],
)
async def test_cambia_ip_seconda_prova_confronta_il_nome(
    hass: HomeAssistant, seconda: str | None, errore: str
) -> None:
    voce, risultato = await _apri_cambia_ip(hass)
    with patch(NOME_VMC, side_effect=[None, seconda]):
        risultato = await hass.config_entries.options.async_configure(
            risultato["flow_id"], {"host": "192.168.1.171"}
        )
    assert risultato["type"] is FlowResultType.FORM
    assert risultato["errors"] == {"host": errore}
    assert voce.data["host"] == "192.168.1.161"


async def test_cambia_ip_seconda_prova_stessa_vmc(hass: HomeAssistant) -> None:
    voce, risultato = await _apri_cambia_ip(hass)
    with patch(NOME_VMC, side_effect=[None, "VMC Zona Giorno"]):
        risultato = await hass.config_entries.options.async_configure(
            risultato["flow_id"], {"host": "192.168.1.171"}
        )
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    assert voce.data["host"] == "192.168.1.171"


# ---- B-4: riparazione «Riavviare» con la configurazione non valida --------------------


async def test_riparazione_riavvio_rifiutato(hass: HomeAssistant) -> None:
    """Configurazione non valida (b29: controllata dalla riparazione, come fa il servizio
    di riavvio): niente riavvio, la riparazione non si chiude come riuscita ma con un
    messaggio tradotto, e l'avviso resta."""
    from pytest_homeassistant_custom_component.common import async_mock_service

    from custom_components.vmc_master.repairs import RiavvioFlow

    riavvii = async_mock_service(hass, "homeassistant", "restart")
    flusso = RiavvioFlow()
    flusso.hass = hass
    flusso.flow_id = "prova"
    flusso.handler = DOMAIN
    with patch(CONTROLLO_CONFIG, return_value="Invalid config for 'sensor': configuration is not valid"):
        risultato = await flusso.async_step_confirm({})
    await hass.async_block_till_done()
    assert riavvii == []
    assert risultato["type"] is FlowResultType.ABORT
    assert risultato["reason"] == "riavvio_non_riuscito"
    assert "configuration is not valid" in risultato["description_placeholders"]["errore"]
    for lingua in ("it", "en"):
        dati = json.loads((CARTELLA / "translations" / f"{lingua}.json").read_text(encoding="utf-8"))
        testo = dati["issues"]["riavvio_necessario"]["fix_flow"]["abort"]["riavvio_non_riuscito"]
        assert "{errore}" in testo


async def test_riparazione_riavvio_rifiutato_avviso_resta(hass: HomeAssistant, hass_client) -> None:
    """Dalle Riparazioni vere: riavvio rifiutato, l'avviso «riavviare» resta."""
    from custom_components.vmc_master import _segnala_riavvio

    assert await async_setup_component(hass, "http", {})
    assert await async_setup_component(hass, "repairs", {})
    MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    ).add_to_hass(hass)
    assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()

    riavvii: list[ServiceCall] = []

    async def riavvio(chiamata: ServiceCall) -> None:
        riavvii.append(chiamata)

    hass.services.async_register("homeassistant", "restart", riavvio)
    _segnala_riavvio(hass)
    client = await hass_client()
    risposta = await client.post(
        "/api/repairs/issues/fix", json={"handler": DOMAIN, "issue_id": "riavvio_necessario"}
    )
    assert risposta.status == 200
    flusso = await risposta.json()
    with patch(CONTROLLO_CONFIG, return_value="configuration is not valid"):
        risposta = await client.post(f"/api/repairs/issues/fix/{flusso['flow_id']}", json={})
    assert risposta.status == 200
    dati = await risposta.json()
    assert dati["type"] == "abort" and dati["reason"] == "riavvio_non_riuscito"
    assert dati["description_placeholders"] == {"errore": "configuration is not valid"}
    await hass.async_block_till_done()
    assert riavvii == []
    assert ir.async_get(hass).async_get_issue(DOMAIN, "riavvio_necessario") is not None


# ---- B-5: voce disabilitata -------------------------------------------------------------


# ---- recorder: solo l'elenco delle escluse ---------------------------------------------


# ---- Messaggio finale dopo l'aggiunta: come riavviare --------------------------------


async def _aggiungi_in_rete(hass: HomeAssistant, ip: str, nome_vmc: str):
    from homeassistant import config_entries

    risultato = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    risultato = await hass.config_entries.flow.async_configure(
        risultato["flow_id"], {"next_step_id": "in_rete"}
    )
    with (
        patch("custom_components.vmc_master.config_flow.async_prova_vmc", return_value=True),
        patch(NOME_VMC, return_value=nome_vmc),
    ):
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"host": ip}
        )
    await hass.async_block_till_done()
    return risultato


async def test_senza_riavvio_messaggio_normale(hass: HomeAssistant) -> None:
    """La VMC parte subito, nessun riavvio chiesto: messaggio normale."""
    assert ir.async_get(hass).async_get_issue(DOMAIN, "riavvio_necessario") is None
    risultato = await _aggiungi_in_rete(hass, "192.168.1.160", "VMC Giorno")
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    assert risultato.get("description") is None


# ---- B-6: risposta della VMC a VMNM? in piu' pezzi ----------------------------------


async def _vmc_finta(pezzi: list[bytes], pausa: float = 0.3, chiudi: bool = True):
    """VMC finta su 127.0.0.1: a «VMNM?» risponde con i pezzi indicati, una pausa tra l'uno
    e l'altro."""
    import asyncio

    async def gestisci(lettore, scrittore):
        await lettore.read(5)
        for numero, pezzo in enumerate(pezzi):
            if numero:
                await asyncio.sleep(pausa)
            scrittore.write(pezzo)
            await scrittore.drain()
        if not chiudi:
            # resta aperta finche' non chiude il client (niente compiti pendenti a fine test)
            await lettore.read()
        scrittore.close()

    server = await asyncio.start_server(gestisci, "127.0.0.1", 0)
    return server, server.sockets[0].getsockname()[1]


@pytest.mark.parametrize(
    ("pezzi", "atteso", "massimo"),
    [
        ([b"VMNM Pr", b"imo Piano***"], "Primo Piano", 2.0),  # spezzata: nome intero
        ([b"VMNM ", b"Zona Notte\r\n"], "Zona Notte", 2.0),
        ([b"VMNM Giorno******"], "Giorno", 1.0),  # completa: niente attesa lunga
        ([b"HTTP/1.1 400 Bad Request\r\n"], "", 1.0),  # non e' una VMC
        ([], None, 1.0),  # chiusa senza dati
    ],
)
async def test_nome_vmc_in_piu_pezzi(
    socket_enabled, pezzi: list[bytes], atteso: str | None, massimo: float
) -> None:
    from custom_components.vmc_master import config_flow

    server, porta = await _vmc_finta(pezzi)
    try:
        with patch.object(config_flow, "PORTA_VMC", porta):
            inizio = time.monotonic()
            nome = await _NOME_VERO("127.0.0.1")
            durata = time.monotonic() - inizio
    finally:
        server.close()
        await server.wait_closed()
        await server.wait_closed()
    assert nome == atteso
    assert durata < massimo


async def test_nome_vmc_completo_senza_chiusura_e_veloce(socket_enabled) -> None:
    """Risposta completa e connessione lasciata aperta: si attendono solo 0,12 s."""
    from custom_components.vmc_master import config_flow

    server, porta = await _vmc_finta([b"VMNM Giorno******"], chiudi=False)
    try:
        with patch.object(config_flow, "PORTA_VMC", porta):
            inizio = time.monotonic()
            nome = await _NOME_VERO("127.0.0.1")
            durata = time.monotonic() - inizio
    finally:
        server.close()
        await server.wait_closed()
    assert nome == "Giorno" and durata < 1.0
