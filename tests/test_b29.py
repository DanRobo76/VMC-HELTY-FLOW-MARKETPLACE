"""Prove della 9.0.0b29: la riparazione «Riavviare Home Assistant» controlla la
configurazione e avvia il riavvio senza aspettarlo, cosi' la risposta arriva al browser
(la finestra si chiude) prima che Home Assistant si fermi."""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from unittest.mock import patch

from homeassistant.components.repairs import ConfirmRepairFlow
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import issue_registry as ir
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry, async_mock_service

from custom_components.vmc_master import _segnala_riavvio
from custom_components.vmc_master.const import DOMAIN
from custom_components.vmc_master.repairs import RiavvioFlow, async_create_fix_flow

CONTROLLO_CONFIG = "homeassistant.config.async_check_ha_config_file"
ISSUE = "riavvio_necessario"


def _flusso(hass: HomeAssistant) -> RiavvioFlow:
    flusso = RiavvioFlow()
    flusso.hass = hass
    flusso.flow_id = "prova"
    flusso.handler = DOMAIN
    return flusso


async def _gira(hass: HomeAssistant) -> None:
    """Lascia girare i compiti appena creati (senza aspettare quelli in corso)."""
    for _ in range(5):
        await asyncio.sleep(0)


class RiavvioLento:
    """Servizio «homeassistant.restart» finto che resta in corso finche' non si sblocca."""

    def __init__(self, hass: HomeAssistant) -> None:
        self.sblocca = asyncio.Event()
        self.chiamate: list[ServiceCall] = []
        self.finiti = 0
        hass.services.async_register("homeassistant", "restart", self._esegui)

    async def _esegui(self, chiamata: ServiceCall) -> None:
        self.chiamate.append(chiamata)
        await self.sblocca.wait()
        self.finiti += 1


# ------------------------------------------------------------- configurazione valida
async def test_riavvio_avviato_senza_aspettarlo(hass: HomeAssistant) -> None:
    """Configurazione valida: il riavvio parte e la riparazione finisce subito come
    riuscita, mentre il servizio di riavvio e' ancora in corso."""
    riavvio = RiavvioLento(hass)
    flusso = _flusso(hass)
    with patch(CONTROLLO_CONFIG, return_value=None) as controllo:
        # con la chiamata bloccante di prima questo attenderebbe per sempre
        risultato = await asyncio.wait_for(flusso.async_step_confirm({}), timeout=5)
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    controllo.assert_awaited_once_with(hass)
    # il riavvio parte subito dopo, in un compito a parte
    assert riavvio.chiamate == []
    await _gira(hass)
    assert len(riavvio.chiamate) == 1 and riavvio.finiti == 0
    chiamata = riavvio.chiamate[0]
    assert (chiamata.domain, chiamata.service) == ("homeassistant", "restart")
    # sbloccato, il riavvio finisce da solo (nessun compito lasciato in sospeso)
    riavvio.sblocca.set()
    await hass.async_block_till_done()
    assert riavvio.finiti == 1


async def test_riavvio_dalle_riparazioni_risposta_prima_del_riavvio(
    hass: HomeAssistant, hass_client
) -> None:
    """Dalle Riparazioni vere (API usata dal browser): la risposta «create_entry» arriva
    mentre il riavvio e' ancora in corso e l'avviso si chiude."""
    assert await async_setup_component(hass, "http", {})
    assert await async_setup_component(hass, "repairs", {})
    MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    ).add_to_hass(hass)
    assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()
    riavvio = RiavvioLento(hass)
    _segnala_riavvio(hass)
    client = await hass_client()
    risposta = await client.post(
        "/api/repairs/issues/fix", json={"handler": DOMAIN, "issue_id": ISSUE}
    )
    assert risposta.status == 200
    flusso = await risposta.json()
    assert flusso["type"] == "form" and flusso["step_id"] == "confirm"
    with patch(CONTROLLO_CONFIG, return_value=None):
        risposta = await asyncio.wait_for(
            client.post(f"/api/repairs/issues/fix/{flusso['flow_id']}", json={}), timeout=5
        )
    assert risposta.status == 200
    dati = await risposta.json()
    assert dati["type"] == "create_entry"
    await _gira(hass)
    assert len(riavvio.chiamate) == 1 and riavvio.finiti == 0
    assert ir.async_get(hass).async_get_issue(DOMAIN, ISSUE) is None
    riavvio.sblocca.set()
    await hass.async_block_till_done()
    assert riavvio.finiti == 1


async def test_errore_del_riavvio_avviso_torna(hass: HomeAssistant, hass_client, caplog) -> None:
    """Il servizio di riavvio rifiuta dopo la chiusura della riparazione (per esempio la
    configurazione cambiata nel frattempo): l'errore va nel registro e l'avviso «riavviare»
    torna, cosi' il riavvio non si perde."""
    assert await async_setup_component(hass, "http", {})
    assert await async_setup_component(hass, "repairs", {})
    MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    ).add_to_hass(hass)
    assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()

    async def riavvio_rotto(_chiamata: ServiceCall) -> None:
        raise HomeAssistantError("riavvio fallito dopo")

    hass.services.async_register("homeassistant", "restart", riavvio_rotto)
    _segnala_riavvio(hass)
    client = await hass_client()
    risposta = await client.post(
        "/api/repairs/issues/fix", json={"handler": DOMAIN, "issue_id": ISSUE}
    )
    flusso = await risposta.json()
    with patch(CONTROLLO_CONFIG, return_value=None), caplog.at_level(logging.WARNING):
        risposta = await client.post(f"/api/repairs/issues/fix/{flusso['flow_id']}", json={})
        dati = await risposta.json()
        assert dati["type"] == "create_entry"
        await hass.async_block_till_done()
    avviso = "Riavvio di Home Assistant non eseguito: riavvio fallito dopo"
    assert any(r.levelno == logging.WARNING and r.getMessage() == avviso for r in caplog.records)
    voce = ir.async_get(hass).async_get_issue(DOMAIN, ISSUE)
    assert voce is not None and voce.active


async def test_database_in_aggiornamento_niente_riavvio(hass: HomeAssistant) -> None:
    """Aggiornamento del database della cronologia in corso (il servizio di riavvio lo
    rifiuterebbe): la riparazione non si chiude come riuscita, testo nella lingua di HA."""
    riavvii = async_mock_service(hass, "homeassistant", "restart")
    for lingua, testo in (("it", "aggiornamento del database"), ("en", "database upgrade")):
        hass.config.language = lingua
        with (
            patch(CONTROLLO_CONFIG, return_value=None),
            patch(
                "custom_components.vmc_master.repairs.recorder.async_migration_in_progress",
                return_value=True,
            ),
        ):
            risultato = await _flusso(hass).async_step_confirm({})
        assert risultato["type"] is FlowResultType.ABORT
        assert risultato["reason"] == "riavvio_non_riuscito"
        assert testo in risultato["description_placeholders"]["errore"]
    await hass.async_block_till_done()
    assert riavvii == []


async def test_avviso_ignorato_torna_visibile(hass: HomeAssistant) -> None:
    """Un «Ignora» dato a una richiesta di riavvio non nasconde quelle successive."""
    _segnala_riavvio(hass)
    ir.async_ignore_issue(hass, DOMAIN, ISSUE, True)
    assert ir.async_get(hass).async_get_issue(DOMAIN, ISSUE).dismissed_version is not None
    _segnala_riavvio(hass)
    voce = ir.async_get(hass).async_get_issue(DOMAIN, ISSUE)
    assert voce.dismissed_version is None and voce.active


async def test_servizio_di_riavvio_assente(hass: HomeAssistant) -> None:
    """Servizio «homeassistant.restart» non trovato (errore immediato): la riparazione
    non si chiude come riuscita."""
    if hass.services.has_service("homeassistant", "restart"):
        hass.services.async_remove("homeassistant", "restart")
    with patch(CONTROLLO_CONFIG, return_value=None):
        risultato = await _flusso(hass).async_step_confirm({})
    assert risultato["type"] is FlowResultType.ABORT
    assert risultato["reason"] == "riavvio_non_riuscito"
    assert "homeassistant.restart" in risultato["description_placeholders"]["errore"]


# --------------------------------------------------------- configurazione non valida
async def test_configurazione_non_valida_niente_riavvio(hass: HomeAssistant, caplog) -> None:
    """Configurazione non valida: niente riavvio, la riparazione finisce con
    «riavvio_non_riuscito» e l'errore del controllo, scritto anche nel registro."""
    riavvii = async_mock_service(hass, "homeassistant", "restart")
    errore = "Invalid config for 'sensor' at configuration.yaml, line 3"
    with patch(CONTROLLO_CONFIG, return_value=errore), caplog.at_level(logging.WARNING):
        risultato = await _flusso(hass).async_step_confirm({})
    await hass.async_block_till_done()
    assert risultato["type"] is FlowResultType.ABORT
    assert risultato["reason"] == "riavvio_non_riuscito"
    assert risultato["description_placeholders"] == {"errore": errore}
    assert riavvii == []
    avviso = f"Riavvio di Home Assistant non eseguito: {errore}"
    assert any(r.levelno == logging.WARNING and r.getMessage() == avviso for r in caplog.records)


async def test_controllo_vero_della_configurazione(hass: HomeAssistant) -> None:
    """Con il controllo vero di Home Assistant: configuration.yaml rotto non riavvia,
    configuration.yaml valido riavvia."""
    riavvii = async_mock_service(hass, "homeassistant", "restart")
    configurazione = Path(hass.config.config_dir) / "configuration.yaml"
    configurazione.write_text("homeassistant:\n  name: [rotto\n", encoding="utf-8")
    risultato = await _flusso(hass).async_step_confirm({})
    assert risultato["type"] is FlowResultType.ABORT
    assert risultato["reason"] == "riavvio_non_riuscito"
    assert risultato["description_placeholders"]["errore"]
    await hass.async_block_till_done()
    assert riavvii == []
    configurazione.write_text("homeassistant:\n  name: Casa\n", encoding="utf-8")
    risultato = await _flusso(hass).async_step_confirm({})
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    assert len(riavvii) == 1


# ------------------------------------------------------------------------ fix flow
async def test_fix_flow_della_riparazione_riavvio(hass: HomeAssistant) -> None:
    """«riavvio_necessario» apre ancora RiavvioFlow, che chiede conferma senza riavviare;
    gli altri avvisi si chiudono con una semplice conferma."""
    riavvii = async_mock_service(hass, "homeassistant", "restart")
    flusso = await async_create_fix_flow(hass, ISSUE, None)
    assert isinstance(flusso, RiavvioFlow)
    flusso.hass = hass
    flusso.flow_id = "prova"
    flusso.handler = DOMAIN
    with patch(CONTROLLO_CONFIG) as controllo:
        risultato = await flusso.async_step_init()
    assert risultato["type"] is FlowResultType.FORM and risultato["step_id"] == "confirm"
    controllo.assert_not_called()
    assert riavvii == []
    altro = await async_create_fix_flow(hass, "packages_non_abilitati_master", None)
    assert type(altro) is ConfirmRepairFlow
