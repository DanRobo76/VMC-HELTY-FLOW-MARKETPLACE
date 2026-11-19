"""b25: dopo un'installazione o un aggiornamento resta una sola riparazione di riavvio."""

from __future__ import annotations

import dataclasses

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.helpers import issue_registry as ir
from homeassistant.setup import async_setup_component

from custom_components.vmc_master import _segnala_riavvio
from custom_components.vmc_master.const import DOMAIN

from .test_integrazione import _aggiungi

MARKETPLACE = "marketplace"
RIAVVIO_MARKETPLACE = "restart_required_1234567_v9.0.0b25"
RIAVVIO_VMC = "riavvio_necessario"


def _riavvio_del_marketplace(
    hass: HomeAssistant,
    dominio: str = MARKETPLACE,
    issue_id: str = RIAVVIO_MARKETPLACE,
    issue_domain: str = DOMAIN,
) -> None:
    """La riparazione «Restart required» come la crea il Marketplace di Home Assistant."""
    ir.async_create_issue(
        hass,
        dominio,
        issue_id,
        is_fixable=True,
        issue_domain=issue_domain,
        severity=ir.IssueSeverity.WARNING,
        translation_key="restart_required",
        translation_placeholders={"name": "VMC Master"},
    )


def _riparazione_vmc(hass: HomeAssistant) -> ir.IssueEntry | None:
    return ir.async_get(hass).async_get_issue(DOMAIN, RIAVVIO_VMC)


async def test_prima_installazione_con_riavvio_del_marketplace(hass: HomeAssistant) -> None:
    """Il Marketplace chiede gia' il riavvio: aggiungere la VMC non ne aggiunge un'altra."""
    await async_setup_component(hass, "http", {})
    _riavvio_del_marketplace(hass)
    risultato = await _aggiungi(hass, "master", "192.168.1.160")
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    assert _riparazione_vmc(hass) is None
    assert ir.async_get(hass).async_get_issue(MARKETPLACE, RIAVVIO_MARKETPLACE) is not None


async def test_riavvio_del_marketplace_dopo_quello_della_vmc(hass: HomeAssistant) -> None:
    """La VMC chiede il riavvio, poi lo chiede il Marketplace: resta solo il suo."""
    await async_setup_component(hass, "http", {})
    risultato = await _aggiungi(hass, "master", "192.168.1.160")
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    assert _riparazione_vmc(hass) is not None
    _riavvio_del_marketplace(hass)
    await hass.async_block_till_done()
    assert _riparazione_vmc(hass) is None
    assert ir.async_get(hass).async_get_issue(MARKETPLACE, RIAVVIO_MARKETPLACE) is not None
    # quando il Marketplace la toglie, la VMC non la rimette da sola
    ir.async_delete_issue(hass, MARKETPLACE, RIAVVIO_MARKETPLACE)
    await hass.async_block_till_done()
    assert _riparazione_vmc(hass) is None


@pytest.mark.parametrize(
    ("dominio", "issue_id", "issue_domain"),
    [
        (MARKETPLACE, RIAVVIO_MARKETPLACE, "altra_integrazione"),  # riavvio per un'altra integrazione
        (MARKETPLACE, "repository_removed_1234567", DOMAIN),  # altra riparazione del Marketplace
        ("altra_integrazione", RIAVVIO_MARKETPLACE, DOMAIN),  # non e' il Marketplace
    ],
)
async def test_altre_riparazioni_non_contano(
    hass: HomeAssistant, dominio: str, issue_id: str, issue_domain: str
) -> None:
    """Solo il «Restart required» del Marketplace per questa integrazione sostituisce il suo."""
    assert await async_setup_component(hass, DOMAIN, {})
    _riavvio_del_marketplace(hass, dominio, issue_id, issue_domain)
    _segnala_riavvio(hass)
    assert _riparazione_vmc(hass) is not None
    # e arrivando dopo non la tolgono
    ir.async_delete_issue(hass, dominio, issue_id)
    _riavvio_del_marketplace(hass, dominio, issue_id, issue_domain)
    await hass.async_block_till_done()
    assert _riparazione_vmc(hass) is not None


async def test_riavvio_del_marketplace_non_attivo(hass: HomeAssistant) -> None:
    """Una riparazione del Marketplace rimasta in memoria da un avvio precedente (non attiva)
    non conta: la VMC chiede il riavvio."""
    assert await async_setup_component(hass, DOMAIN, {})
    _riavvio_del_marketplace(hass)
    registro = ir.async_get(hass)
    chiave = (MARKETPLACE, RIAVVIO_MARKETPLACE)
    registro.issues[chiave] = dataclasses.replace(registro.issues[chiave], active=False)
    _segnala_riavvio(hass)
    assert _riparazione_vmc(hass) is not None
