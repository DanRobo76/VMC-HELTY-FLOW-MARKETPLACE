"""Prova configurazione da interfaccia, installazione del package e scheda."""

from __future__ import annotations

import json
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
MANIFEST = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "manifest.json"


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
    # versione dell'integrazione e release del repository dell'integrazione
    versione = json.loads(MANIFEST.read_text(encoding="utf-8"))["version"]
    package = (cartella / "vmc_master.yaml").read_text(encoding="utf-8")
    assert f'state: "v.{versione}"' in package and '"v.8.6.0"' not in package
    assert "repos/DanRobo76/VMC-HELTY-FLOW-MARKETPLACE/releases/latest" in package
    assert "repos/DanRobo76/VMC-HELTY-FLOW/releases" not in package
    automazione = (cartella / "vmc_master_automazione.yaml").read_text(encoding="utf-8")
    assert "[Link](https://github.com/DanRobo76/VMC-HELTY-FLOW-MARKETPLACE)" in automazione
    assert "[Link](https://github.com/DanRobo76/VMC-HELTY-FLOW)" not in automazione
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
    assert risultato["description_placeholders"]["ip_trovato"] == "192.168.1.150"
    risultato = await hass.config_entries.flow.async_configure(risultato["flow_id"], {})
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    backup = list(Path(hass.config.path("vmc_master_backup")).iterdir())
    assert len(backup) == 1 and (backup[0] / "vmc_master.yaml").is_file()
    assert (cartella / ".vmc_master_integrazione.json").is_file()


async def test_migrazione_vmc_clonata(hass: HomeAssistant) -> None:
    """Una VMC clonata a mano non va cancellata prima: la sposta in backup l'integrazione."""
    cartella = Path(hass.config.path("packages", "vmc_helty_flow", "sala"))
    cartella.mkdir(parents=True)
    (cartella / "vmc_sala.yaml").write_text("sensor:\n  - platform: tcp\n    host: 192.168.1.161\n", encoding="utf-8")
    risultato = await _aggiungi(hass, "sala", "192.168.1.171")
    assert risultato["step_id"] == "migra"
    segnaposto = risultato["description_placeholders"]
    assert segnaposto["ip"] == "192.168.1.171" and segnaposto["ip_trovato"] == "192.168.1.161"
    risultato = await hass.config_entries.flow.async_configure(risultato["flow_id"], {})
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    backup = list(Path(hass.config.path("vmc_master_backup")).iterdir())
    assert len(backup) == 1 and backup[0].name.startswith("sala_")
    assert "192.168.1.171" in (cartella / "vmc_sala.yaml").read_text(encoding="utf-8")


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


async def test_toglie_entita_finestra_clona(hass: HomeAssistant) -> None:
    """Dopo la migrazione della Master le 18 entita' della Finestra Clona non piu' fornite
    vengono tolte dal registro; quelle ancora fornite restano."""
    from homeassistant.helpers import entity_registry as er

    from custom_components.vmc_master.const import ENTITA_FINESTRA_CLONA

    assert len(ENTITA_FINESTRA_CLONA) == 18
    voce = MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    )
    voce.add_to_hass(hass)
    assert await hass.config_entries.async_setup(voce.entry_id)
    await hass.async_block_till_done()

    registro = er.async_get(hass)
    for entity_id in ENTITA_FINESTRA_CLONA:
        dominio, oggetto = entity_id.split(".")
        creata = registro.async_get_or_create(dominio, dominio, oggetto, suggested_object_id=oggetto)
        assert creata.entity_id == entity_id
    fornita = "input_boolean.vmc_master_clona_eseguita"
    hass.states.async_set(fornita, "off")
    hass.states.async_set("input_text.vmc_master_clona_ip", "unavailable", {"restored": True})
    # package caricato dopo il riavvio
    hass.states.async_set("sensor.vmc_master_status_ip", "ON-Line")

    assert await hass.config_entries.async_reload(voce.entry_id)
    await hass.async_block_till_done()
    rimaste = [e for e in ENTITA_FINESTRA_CLONA if registro.async_get(e) is not None]
    assert rimaste == [fornita]


async def test_modelli_della_scheda_senza_errori(hass: HomeAssistant) -> None:
    """Ogni modello della scheda (master e VMC clonata) si calcola senza errori e il link
    del video resta quello del repository."""
    import yaml

    from homeassistant.exceptions import TemplateError
    from homeassistant.helpers.template import Template

    from custom_components.vmc_master.trasforma import per_vmc

    sorgente = (
        Path(__file__).parent.parent
        / "custom_components" / "vmc_master" / "package"
        / "vmc_master_scheda_manuale_interfaccia.txt"
    )
    scheda = sorgente.read_text(encoding="utf-8")

    def modelli(nodo, uscita):
        if isinstance(nodo, dict):
            for valore in nodo.values():
                modelli(valore, uscita)
        elif isinstance(nodo, list):
            for valore in nodo:
                modelli(valore, uscita)
        elif isinstance(nodo, str) and ("{{" in nodo or "{%" in nodo):
            uscita.append(nodo)
        return uscita

    for nome, ip in (("master", "192.168.1.160"), ("sala", "192.168.1.161")):
        testo = per_vmc(scheda, nome, ip)
        assert "is_state('on')" not in testo
        assert testo.count("VMC-HELTY-FLOW/raw/main/Video/VMC_MASTER_promo_IT.mp4") == 2
        elenco = modelli(yaml.safe_load(testo), [])
        assert elenco
        errori = []
        for modello in elenco:
            try:
                Template(modello, hass).async_render(parse_result=False)
            except TemplateError as errore:
                errori.append(str(errore)[:120])
        assert errori == [], (nome, errori)
