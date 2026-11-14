"""Prova configurazione da interfaccia, installazione del package e scheda."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.helpers import issue_registry as ir
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.vmc_master.const import DOMAIN

PROVA_VMC = "custom_components.vmc_master.config_flow.async_prova_vmc"


async def _aggiungi(hass: HomeAssistant, nome: str, ip: str, risponde: bool = True):
    risultato = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert risultato["type"] is FlowResultType.FORM
    with patch(PROVA_VMC, return_value=risponde):
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"nome": nome, "host": ip}
        )
    return risultato


async def test_aggiungi_master_e_sala(hass: HomeAssistant, hass_client) -> None:
    await async_setup_component(hass, "http", {})
    risultato = await _aggiungi(hass, "master", "192.168.1.160")
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    cartella = Path(hass.config.path("packages", "vmc_helty_flow", "master"))
    assert (cartella / "vmc_master.yaml").is_file()
    assert (cartella / "vmc_master_automazione.yaml").is_file()
    assert "192.168.1.160" in (cartella / "vmc_master.yaml").read_text(encoding="utf-8")
    assert ir.async_get(hass).async_get_issue(DOMAIN, "riavvio_necessario") is not None

    # Seconda VMC, non raggiungibile: si aggiunge dopo la conferma
    risultato = await _aggiungi(hass, "sala", "192.168.1.161", risponde=False)
    assert risultato["type"] is FlowResultType.FORM
    assert risultato["step_id"] == "non_raggiungibile"
    risultato = await hass.config_entries.flow.async_configure(risultato["flow_id"], {})
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    assert Path(hass.config.path("packages", "vmc_helty_flow", "sala", "vmc_sala.yaml")).is_file()

    # Scheda: configurazione per ogni VMC
    client = await hass_client()
    for voce in hass.config_entries.async_entries(DOMAIN):
        risposta = await client.get(f"/api/vmc_master/scheda/{voce.entry_id}")
        assert risposta.status == 200
        scheda = await risposta.json()
        assert scheda["type"] == "vertical-stack"
        testo = str(scheda)
        assert "vmc_master_clona_" not in testo
        assert "opzione_finestra_clona" not in testo
        if voce.data["nome"] == "sala":
            assert "vmc_master" not in testo and "vmc_sala_" in testo
    risposta = await client.get("/api/vmc_master/scheda/inesistente")
    assert risposta.status == 404
    risposta = await client.get("/vmc_master_frontend/vmc-master-card.js")
    assert risposta.status == 200


async def test_errori_nome_e_ip(hass: HomeAssistant) -> None:
    MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    ).add_to_hass(hass)
    risultato = await _aggiungi(hass, "Sala1", "999.999.999.999")
    assert risultato["errors"] == {"nome": "nome_non_valido", "host": "ip_non_valido"}
    risultato = await _aggiungi(hass, "master", "192.168.1.160")
    assert risultato["errors"] == {"nome": "nome_in_uso", "host": "ip_in_uso"}


async def test_cambia_ip_da_configura(hass: HomeAssistant) -> None:
    voce = MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    )
    voce.add_to_hass(hass)
    assert await hass.config_entries.async_setup(voce.entry_id)
    await hass.async_block_till_done()
    risultato = await hass.config_entries.options.async_init(voce.entry_id)
    risultato = await hass.config_entries.options.async_configure(
        risultato["flow_id"], {"host": "192.168.1.170"}
    )
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    yaml_master = Path(hass.config.path("packages", "vmc_helty_flow", "master", "vmc_master.yaml"))
    testo = yaml_master.read_text(encoding="utf-8")
    assert "192.168.1.170" in testo and "192.168.1.160" not in testo


async def test_cambia_ip_dalla_scheda(hass: HomeAssistant) -> None:
    """L'IP scritto dal campo «Cambia IP VMC» (script) vale anche per l'integrazione."""
    voce = MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    )
    voce.add_to_hass(hass)
    assert await hass.config_entries.async_setup(voce.entry_id)
    await hass.async_block_till_done()
    yaml_master = Path(hass.config.path("packages", "vmc_helty_flow", "master", "vmc_master.yaml"))
    # come lo script Cambia IP: tutti gli IP del file diventano il nuovo
    yaml_master.write_text(
        yaml_master.read_text(encoding="utf-8").replace("192.168.1.160", "192.168.1.180"),
        encoding="utf-8",
    )
    assert await hass.config_entries.async_reload(voce.entry_id)
    await hass.async_block_till_done()
    assert voce.data["host"] == "192.168.1.180"
    assert "192.168.1.180" in yaml_master.read_text(encoding="utf-8")


async def test_migrazione_da_installazione_manuale(hass: HomeAssistant) -> None:
    cartella = Path(hass.config.path("packages", "vmc_helty_flow", "master"))
    cartella.mkdir(parents=True)
    (cartella / "vmc_master.yaml").write_text("sensor:\n  - platform: tcp\n    host: 192.168.1.150\n", encoding="utf-8")
    risultato = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    # l'IP gia' impostato viene proposto
    campi = {str(k): k for k in risultato["data_schema"].schema}
    assert campi["host"].default() == "192.168.1.150"
    with patch(PROVA_VMC, return_value=True):
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"nome": "master", "host": "192.168.1.150"}
        )
    assert risultato["step_id"] == "migra"
    risultato = await hass.config_entries.flow.async_configure(risultato["flow_id"], {})
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    backup = list(Path(hass.config.path("vmc_master_backup")).iterdir())
    assert len(backup) == 1 and (backup[0] / "vmc_master.yaml").is_file()
    assert (cartella / ".vmc_master_integrazione.json").is_file()


async def test_rimozione_sposta_in_backup(hass: HomeAssistant) -> None:
    voce = MockConfigEntry(
        domain=DOMAIN, unique_id="sala", data={"nome": "sala", "host": "192.168.1.161"}
    )
    voce.add_to_hass(hass)
    assert await hass.config_entries.async_setup(voce.entry_id)
    await hass.async_block_till_done()
    assert await hass.config_entries.async_remove(voce.entry_id)
    await hass.async_block_till_done()
    assert not Path(hass.config.path("packages", "vmc_helty_flow", "sala")).exists()
    assert len(list(Path(hass.config.path("vmc_master_backup")).iterdir())) == 1
