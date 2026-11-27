"""Casi rari del passaggio e della VMC nativa (Home Assistant vero): cartella della beta
che non si toglie, VMC in attesa eliminata, avvio del motore che non riesce, aiutante
dell'utente con il prefisso della VMC, cambio d'IP dalla scheda per una voce non
avviata, scheda di una VMC disattivata, dati salvati non validi. (L'automazione del
motore disattivata dall'utente nel registro delle entità non c'è più: dalla 9.0.0b46 le
automazioni del motore sono logiche senza entità, test_b45_pagina_automazione.py.)"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
from homeassistant.config_entries import ConfigEntryDisabler, ConfigEntryState
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import issue_registry as ir

from custom_components.vmc_master import (
    ISSUE_PASSAGGIO,
    ISSUE_RIMASTO,
    _async_cambia_ip_dalla_scheda,
    passaggio,
)
from custom_components.vmc_master.const import DOMAIN
from custom_components.vmc_master.passaggio import DOMANI

from .banco import (
    aggiungi_e_avvia,
    conferma_dalla_riparazione,
    scrivi_package_beta,
    senza_rete,
    voce,
)


@pytest.fixture(autouse=True)
def rete_finta():
    with senza_rete():
        yield


def _problema(hass: HomeAssistant, issue_id: str) -> ir.IssueEntry | None:
    return ir.async_get(hass).async_get_issue(DOMAIN, issue_id)


async def test_cartella_della_beta_che_non_si_toglie(
    hass: HomeAssistant, tmp_path: Path
) -> None:
    """Package non caricato (niente riavvio da chiedere) e cartella che non si toglie:
    la riparazione lo dice, la VMC resta in attesa e non si ricarica."""
    master = voce("master")
    cartella = scrivi_package_beta(str(tmp_path), "master", master.data["host"])
    await aggiungi_e_avvia(hass, [master])
    assert master.runtime_data.situazione == passaggio.IN_ATTESA
    with (
        patch.object(passaggio, "_togli_cartella", side_effect=OSError("occupata")),
        patch.object(hass.config_entries, "async_schedule_reload") as ricarica,
    ):
        passo = await conferma_dalla_riparazione(hass)
    assert (passo["type"], passo["reason"]) == ("abort", "cartella_non_tolta")
    assert passo["description_placeholders"] == {"errore": "master: occupata"}
    ricarica.assert_not_called()
    assert cartella.exists()
    assert _problema(hass, ISSUE_PASSAGGIO) is not None
    assert master.runtime_data.situazione == passaggio.IN_ATTESA


async def test_vmc_in_attesa_eliminata(hass: HomeAssistant, tmp_path: Path) -> None:
    """Una VMC che aspetta il passaggio, eliminata: la riparazione del passaggio si
    toglie e un avviso dice che la cartella della beta è rimasta."""
    master = voce("master")
    scrivi_package_beta(str(tmp_path), "master", master.data["host"])
    await aggiungi_e_avvia(hass, [master])
    await hass.async_block_till_done()
    assert _problema(hass, ISSUE_PASSAGGIO) is not None
    assert await hass.config_entries.async_remove(master.entry_id)
    await hass.async_block_till_done()
    assert _problema(hass, ISSUE_PASSAGGIO) is None
    assert _problema(hass, f"{ISSUE_RIMASTO}_master") is not None


async def test_aiutante_dell_utente_con_il_prefisso_della_vmc(
    hass: HomeAssistant,
) -> None:
    """Un aiutante YAML dell'utente chiamato vmc_master_…, senza cartella della beta:
    non è il package, la VMC parte nativa."""
    er.async_get(hass).async_get_or_create(
        "input_boolean",
        "input_boolean",
        "mio_aiutante",
        suggested_object_id="vmc_master_mio",
    )
    master = voce("master")
    await aggiungi_e_avvia(hass, [master])
    assert master.runtime_data.situazione == passaggio.NATIVA


async def test_avvio_del_motore_che_non_riesce(hass: HomeAssistant) -> None:
    """L'avvio della VMC nativa si interrompe: la VMC si ferma (niente resta avviato) e
    la voce non risulta caricata."""
    master = voce("master")
    with patch(
        "custom_components.vmc_master.nativa.assemblaggio.VMCAssemblata.avvia",
        AsyncMock(side_effect=RuntimeError("guasto")),
    ):
        await aggiungi_e_avvia(hass, [master])
    assert master.state is ConfigEntryState.SETUP_ERROR
    assert master.runtime_data.vmc is None


async def test_cambio_ip_dalla_scheda_casi_rari(hass: HomeAssistant) -> None:
    """Voce che non c'è più, stesso IP, voce non avviata: in quest'ultimo caso l'IP
    cambia solo nella voce."""
    master = voce("master")
    master.add_to_hass(hass)
    await _async_cambia_ip_dalla_scheda(hass, "voce_inesistente", "192.168.1.99")
    await _async_cambia_ip_dalla_scheda(hass, master.entry_id, master.data["host"])
    assert master.data["host"] == voce("master").data["host"]
    await _async_cambia_ip_dalla_scheda(hass, master.entry_id, "192.168.1.99")
    assert master.data["host"] == "192.168.1.99"


async def test_scheda_di_una_vmc_disattivata(hass: HomeAssistant, hass_client) -> None:
    attiva, spenta = voce("master"), voce("nord", 1)
    await aggiungi_e_avvia(hass, [attiva, spenta])
    await hass.config_entries.async_set_disabled_by(
        spenta.entry_id, ConfigEntryDisabler.USER
    )
    client = await hass_client()
    risposta = await client.get(f"/api/vmc_master/scheda/{spenta.entry_id}")
    assert risposta.status == 409


def test_valori_passati_non_validi() -> None:
    """Dati del passaggio salvati non validi (archivio modificato a mano): si ignorano."""
    chiave = next(k for k, d in DOMANI.items() if d == "switch")
    dati = {
        "impostazioni": {"input_boolean.non_esiste": "on", chiave: 1},
        "memorie": {"sensor.uno": "non un dizionario", "sensor.due": {"state": 5}},
    }
    assert passaggio.valori_passati(dati, "master") == {}
