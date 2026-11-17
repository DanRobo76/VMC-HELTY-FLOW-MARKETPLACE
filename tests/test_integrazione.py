"""Prova configurazione da interfaccia, installazione del package e scheda."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote
from unittest.mock import patch

import pytest
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.helpers import issue_registry as ir
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.vmc_master.const import DOMAIN

PROVA_VMC = "custom_components.vmc_master.config_flow.async_prova_vmc"
NOME_VMC = "custom_components.vmc_master.config_flow.async_nome_vmc"
HASSIO = "custom_components.vmc_master.config_flow.is_hassio"
PI = "custom_components.vmc_master.prima_installazione"
MANIFEST = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "manifest.json"
RADICE = Path(__file__).parent.parent


@pytest.fixture(autouse=True)
def _nessuna_vmc_in_rete():
    """Nei test non c'e' nessuna VMC vera: all'avvio il nome non si legge e il titolo
    della voce resta quello scritto. I test che leggono il nome lo impostano da se'."""
    with patch(NOME_VMC, return_value=None):
        yield


# Link a immagini e video, contati uno per uno: 77 nella scheda (51 file diversi)
# piu' il link «GitHub» del Pannello Informazioni; 14 nel README
FILE_COLLEGATI_SCHEDA = 77
FILE_COLLEGATI_README = 10
# Link al repository della release manuale (non seguito da «-MARKETPLACE»)
RE_LINK_8 = re.compile(r"DanRobo76/VMC-HELTY-FLOW(?![-\w])")
# File letti dal repository dell'integrazione (immagini, video)
RE_FILE_9 = re.compile(
    r"DanRobo76/VMC-HELTY-FLOW-MARKETPLACE/(?:main|raw/main)/([^\s\"'<>?]+)"
)


def _controlla_link(testo: str) -> int:
    """Nessun link al repository VMC-HELTY-FLOW; ogni file collegato esiste nel
    repository dell'integrazione. Restituisce quanti file collegati ci sono."""
    assert RE_LINK_8.findall(testo) == []
    percorsi = [unquote(p) for p in RE_FILE_9.findall(testo)]
    mancanti = [p for p in percorsi if not (RADICE / p).is_file()]
    assert mancanti == []
    return len(percorsi)


async def _aggiungi(hass: HomeAssistant, nome: str, ip: str, risponde: bool = True):
    """«Aggiungi dispositivo» per una VMC gia' collegata al Wi-Fi: solo l'IP, poi il nome
    letto dalla VMC (per la master nessuna domanda sul nome)."""
    risultato = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert risultato["type"] is FlowResultType.MENU
    risultato = await hass.config_entries.flow.async_configure(
        risultato["flow_id"], {"next_step_id": "in_rete"}
    )
    assert risultato["type"] is FlowResultType.FORM and risultato["step_id"] == "in_rete"
    with (
        patch(PROVA_VMC, return_value=risponde),
        patch(NOME_VMC, return_value=f"VMC {nome}" if risponde else None),
    ):
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"host": ip}
        )
        if risultato["type"] is FlowResultType.FORM and risultato["step_id"] in ("nome", "nome_manuale"):
            risultato = await hass.config_entries.flow.async_configure(
                risultato["flow_id"], {"nome": nome}
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
    automazione = (cartella / "vmc_master_automazione.yaml").read_text(encoding="utf-8")
    # l'avviso di aggiornamento lo da' il Marketplace: nessuna notifica dall'automazione
    assert "VMC: aggiornamento disponibile" not in automazione
    # il confronto delle versioni riconosce le beta (9.0.0b13 -> 9.0.0b14 -> 9.0.0)
    assert "(b[0-9]+)?$" in automazione and "(b[0-9]+)?$" in package
    # tutti i file del package: nessun link al repository VMC-HELTY-FLOW
    for file in sorted(cartella.iterdir()):
        if file.is_file():
            assert _controlla_link(file.read_text(encoding="utf-8")) == 0
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
        # Pannello Informazioni: «GitHub» apre il repository dell'integrazione
        assert testo.count('href="https://github.com/DanRobo76/VMC-HELTY-FLOW-MARKETPLACE">GitHub</a>') == 1
        assert testo.count("VMC-HELTY-FLOW-MARKETPLACE/raw/main/Video/VMC_MASTER_promo_IT.mp4") == 2
        # immagini e video: tutti dal repository dell'integrazione, e ci sono tutti
        assert _controlla_link(testo) == FILE_COLLEGATI_SCHEDA
    risposta = await client.get("/api/vmc_master/scheda/inesistente")
    assert risposta.status == 404
    risposta = await client.get("/vmc_master_frontend/vmc-master-card.js")
    assert risposta.status == 200


async def test_errori_nome_e_ip(hass: HomeAssistant) -> None:
    MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    ).add_to_hass(hass)
    risultato = await _aggiungi(hass, "sala", "999.999.999.999")
    assert risultato["errors"] == {"host": "ip_non_valido"}
    risultato = await _aggiungi(hass, "sala", "192.168.1.160")
    assert risultato["errors"] == {"host": "ip_in_uso"}
    for nome, errore in (("Sala1", "nome_non_valido"), ("master", "nome_in_uso")):
        risultato = await _aggiungi(hass, nome, "192.168.1.161")
        assert risultato["step_id"] == "nome" and risultato["errors"] == {"nome": errore}


async def test_vmc_in_rete_basta_l_ip(hass: HomeAssistant) -> None:
    """VMC gia' collegata al Wi-Fi: si scrive solo l'IP, il nome si legge dalla VMC."""
    MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    ).add_to_hass(hass)
    risultato = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert risultato["menu_options"] == ["in_rete", "da_installare"]
    risultato = await hass.config_entries.flow.async_configure(
        risultato["flow_id"], {"next_step_id": "in_rete"}
    )
    assert [str(k) for k in risultato["data_schema"].schema] == ["host"]
    with patch(NOME_VMC, return_value="VMC Sala Grande"):
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"host": "192.168.1.161"}
        )
    assert risultato["step_id"] == "nome" and risultato["errors"] == {}
    assert risultato["description_placeholders"] == {
        "ip": "192.168.1.161", "nome_vmc": "VMC Sala Grande", "proposta": "salagrande"
    }
    risultato = await hass.config_entries.flow.async_configure(
        risultato["flow_id"], {"nome": "salagrande"}
    )
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    # il titolo della voce e' il nome della VMC; il nome interno resta «salagrande»
    assert risultato["title"] == "VMC Sala Grande"
    assert risultato["data"] == {
        "nome": "salagrande", "host": "192.168.1.161", "titolo": "VMC Sala Grande"
    }

    # VMC che non risponde: il nome si scrive a mano e si conferma l'aggiunta
    risultato = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    risultato = await hass.config_entries.flow.async_configure(
        risultato["flow_id"], {"next_step_id": "in_rete"}
    )
    with patch(NOME_VMC, return_value=None):
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"host": "192.168.1.162"}
        )
    assert risultato["step_id"] == "nome_manuale" and risultato["errors"] == {}
    risultato = await hass.config_entries.flow.async_configure(
        risultato["flow_id"], {"nome": "camera"}
    )
    assert risultato["step_id"] == "non_raggiungibile"
    risultato = await hass.config_entries.flow.async_configure(risultato["flow_id"], {})
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    assert risultato["title"] == "VMC camera"
    assert risultato["data"] == {"nome": "camera", "host": "192.168.1.162", "titolo": "VMC camera"}


def test_nome_da_vmc() -> None:
    from custom_components.vmc_master.config_flow import nome_da_vmc

    assert nome_da_vmc("VMC Sala Grande") == "salagrande"
    assert nome_da_vmc("Cucina_2") == "cucina"
    assert nome_da_vmc("VMC") == "vmc"
    assert nome_da_vmc("Città*") == "citta"
    assert nome_da_vmc("Soggiorno-Grande") == "soggiornog"
    assert nome_da_vmc("1234") == ""


async def test_cambia_ip_da_configura(hass: HomeAssistant) -> None:
    voce = MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    )
    voce.add_to_hass(hass)
    assert await hass.config_entries.async_setup(voce.entry_id)
    await hass.async_block_till_done()
    risultato = await hass.config_entries.options.async_init(voce.entry_id)
    assert risultato["type"] is FlowResultType.MENU
    assert risultato["menu_options"] == ["cambia_ip", "elimina"]
    risultato = await hass.config_entries.options.async_configure(
        risultato["flow_id"], {"next_step_id": "cambia_ip"}
    )
    assert risultato["step_id"] == "cambia_ip"
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
    # come lo script Cambia IP (sed -i): tutti gli IP del file diventano il nuovo, fine riga intatti
    yaml_master.write_bytes(yaml_master.read_bytes().replace(b"192.168.1.160", b"192.168.1.180"))
    assert await hass.config_entries.async_reload(voce.entry_id)
    await hass.async_block_till_done()
    assert voce.data["host"] == "192.168.1.180"
    assert "192.168.1.180" in yaml_master.read_text(encoding="utf-8")
    # l'IP cambiato dalla scheda non e' una modifica a mano: nessuna copia salvata
    assert not Path(hass.config.path("vmc_master_backup")).exists()


def test_file_modificati_a_mano(tmp_path: Path) -> None:
    """Un file del package modificato a mano non si perde: prima di riscriverlo
    l'integrazione ne salva una copia in /config/vmc_master_backup."""
    from custom_components.vmc_master.installatore import cartella_vmc, installa

    config_dir = str(tmp_path)
    esito = installa(config_dir, "master", "192.168.1.160", "9.0.0b13")
    assert esito.file_modificati == [] and esito.backup_modificati is None
    automazione = cartella_vmc(config_dir, "master") / "vmc_master_automazione.yaml"
    originale = automazione.read_bytes()
    modificato = originale + b"# riga aggiunta a mano\r\n"
    automazione.write_bytes(modificato)

    esito = installa(config_dir, "master", "192.168.1.160", "9.0.0b13")
    assert esito.file_modificati == ["vmc_master_automazione.yaml"]
    copia = esito.backup_modificati / "vmc_master_automazione.yaml"
    assert copia.read_bytes() == modificato  # copia identica, fine riga compresi
    assert esito.backup_modificati.parent == tmp_path / "vmc_master_backup"
    assert esito.backup_modificati.name.startswith("master_modificati_")
    assert automazione.read_bytes() == originale  # torna il file dell'integrazione
    assert esito.file_scritti == ["vmc_master_automazione.yaml"]

    # file di nuovo uguale a quello scritto: niente da salvare
    esito = installa(config_dir, "master", "192.168.1.160", "9.0.0b13")
    assert esito.file_modificati == [] and esito.file_scritti == []

    # nuova versione dell'integrazione: un file non toccato si aggiorna senza copie
    esito = installa(config_dir, "master", "192.168.1.160", "9.0.0b14")
    assert esito.file_modificati == [] and esito.file_scritti == ["vmc_master.yaml"]
    assert len(list((tmp_path / "vmc_master_backup").iterdir())) == 1


def test_ip_della_scheda_non_e_una_modifica(tmp_path: Path) -> None:
    """IP cambiato dal campo «Cambia IP VMC» e poi aggiornamento dell'integrazione:
    i file sono diversi da quelli scritti, ma non sono modificati a mano."""
    from custom_components.vmc_master.installatore import cartella_vmc, installa

    config_dir = str(tmp_path)
    installa(config_dir, "master", "192.168.1.160", "9.0.0b13")
    cartella = cartella_vmc(config_dir, "master")
    # come lo script Cambia IP: package e script del nome con il nuovo IP
    for nome_file in ("vmc_master.yaml", "vmc_master_script_cambio_nome.sh"):
        percorso = cartella / nome_file
        percorso.write_bytes(percorso.read_bytes().replace(b"192.168.1.160", b"192.168.1.180"))
    esito = installa(config_dir, "master", "192.168.1.180", "9.0.0b14")
    assert esito.file_modificati == [] and esito.backup_modificati is None
    assert esito.file_scritti == ["vmc_master.yaml"]
    assert not (tmp_path / "vmc_master_backup").exists()

    # IP cambiato e anche una modifica a mano: questa si vede
    percorso = cartella / "vmc_master.yaml"
    percorso.write_bytes(percorso.read_bytes().replace(b"192.168.1.180", b"192.168.1.190") + b"# a mano\r\n")
    esito = installa(config_dir, "master", "192.168.1.190", "9.0.0b14")
    assert esito.file_modificati == ["vmc_master.yaml"]


def test_marcatore_senza_md5(tmp_path: Path) -> None:
    """Marcatore senza md5: non si puo' sapere se il file e' stato modificato, si
    aggiorna come prima senza copie."""
    from custom_components.vmc_master.installatore import FILE_MARCATORE, cartella_vmc, installa

    config_dir = str(tmp_path)
    installa(config_dir, "master", "192.168.1.160", "9.0.0b13")
    cartella = cartella_vmc(config_dir, "master")
    marcatore = json.loads((cartella / FILE_MARCATORE).read_text(encoding="utf-8"))
    del marcatore["md5"]
    (cartella / FILE_MARCATORE).write_text(json.dumps(marcatore), encoding="utf-8")
    (cartella / "vmc_master.yaml").write_bytes(b"# a mano\r\n")
    esito = installa(config_dir, "master", "192.168.1.160", "9.0.0b13")
    assert esito.file_modificati == [] and esito.file_scritti == ["vmc_master.yaml"]


async def test_notifica_file_modificati(hass: HomeAssistant) -> None:
    """All'avvio, se un file era stato modificato a mano, compare la notifica con
    l'elenco dei file e la cartella della copia."""
    voce = MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    )
    voce.add_to_hass(hass)
    assert await hass.config_entries.async_setup(voce.entry_id)
    await hass.async_block_till_done()
    automazione = Path(
        hass.config.path("packages", "vmc_helty_flow", "master", "vmc_master_automazione.yaml")
    )
    automazione.write_bytes(automazione.read_bytes() + b"# a mano\r\n")
    with patch(
        "custom_components.vmc_master.persistent_notification.async_create"
    ) as notifica:
        assert await hass.config_entries.async_reload(voce.entry_id)
        await hass.async_block_till_done()
    chiamate = [c for c in notifica.call_args_list if "modificati" in c.kwargs["notification_id"]]
    assert len(chiamate) == 1
    testo = chiamate[0].args[1]
    assert "`vmc_master_automazione.yaml`" in testo
    assert "`config/vmc_master_backup/master_modificati_" in testo
    assert chiamate[0].kwargs["title"] == "VMC Master: file della VMC master modificati a mano"


async def test_migrazione_da_installazione_manuale(hass: HomeAssistant) -> None:
    cartella = Path(hass.config.path("packages", "vmc_helty_flow", "master"))
    cartella.mkdir(parents=True)
    (cartella / "vmc_master.yaml").write_text("sensor:\n  - platform: tcp\n    host: 192.168.1.150\n", encoding="utf-8")
    risultato = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    risultato = await hass.config_entries.flow.async_configure(
        risultato["flow_id"], {"next_step_id": "in_rete"}
    )
    # l'IP gia' impostato viene proposto
    campi = {str(k): k for k in risultato["data_schema"].schema}
    assert campi["host"].default() == "192.168.1.150"
    with patch(PROVA_VMC, return_value=True):
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"host": "192.168.1.150"}
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
    """Una VMC clonata a mano non va cancellata prima: la sposta in backup l'integrazione.
    Con il suo IP si propone il nome della sua cartella, non quello letto dalla VMC."""
    MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    ).add_to_hass(hass)
    cartella = Path(hass.config.path("packages", "vmc_helty_flow", "sala"))
    cartella.mkdir(parents=True)
    (cartella / "vmc_sala.yaml").write_text("sensor:\n  - platform: tcp\n    host: 192.168.1.161\n", encoding="utf-8")
    risultato = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    risultato = await hass.config_entries.flow.async_configure(
        risultato["flow_id"], {"next_step_id": "in_rete"}
    )
    with patch(NOME_VMC, return_value="VMC Soggiorno"):
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"host": "192.168.1.161"}
        )
    assert risultato["step_id"] == "nome"
    assert risultato["description_placeholders"]["proposta"] == "sala"
    risultato = await hass.config_entries.flow.async_configure(
        risultato["flow_id"], {"nome": "sala"}
    )
    assert risultato["step_id"] == "migra"
    segnaposto = risultato["description_placeholders"]
    assert segnaposto["ip"] == "192.168.1.161" and segnaposto["ip_trovato"] == "192.168.1.161"
    risultato = await hass.config_entries.flow.async_configure(risultato["flow_id"], {})
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    backup = list(Path(hass.config.path("vmc_master_backup")).iterdir())
    assert len(backup) == 1 and backup[0].name.startswith("sala_")
    assert "192.168.1.161" in (cartella / "vmc_sala.yaml").read_text(encoding="utf-8")


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


def test_titolo_voce() -> None:
    from custom_components.vmc_master.config_flow import titolo_voce

    assert titolo_voce("VMC Soggiorno", "master") == "VMC Soggiorno"
    assert titolo_voce("vmc studio", "studio") == "vmc studio"
    assert titolo_voce("Soggiorno", "master") == "VMC Soggiorno"
    assert titolo_voce("", "master") == "VMC master"
    assert titolo_voce(None, "camera") == "VMC camera"


async def test_titolo_delle_voci_gia_aggiunte(hass: HomeAssistant) -> None:
    """Le VMC aggiunte prima della 9.0.0b13 («VMC master») prendono il nome della VMC
    all'avvio, senza ricaricare il package; un nome scelto dall'utente resta."""
    voce = MockConfigEntry(
        domain=DOMAIN, unique_id="master", title="VMC master",
        data={"nome": "master", "host": "192.168.1.160"},
    )
    rinominata = MockConfigEntry(
        domain=DOMAIN, unique_id="sala", title="Il mio salotto",
        data={"nome": "sala", "host": "192.168.1.161"},
    )
    voce.add_to_hass(hass)
    rinominata.add_to_hass(hass)
    with patch(NOME_VMC, return_value="VMC Soggiorno"), patch(
        "custom_components.vmc_master.installa", wraps=__import__(
            "custom_components.vmc_master.installatore", fromlist=["installa"]
        ).installa,
    ) as installa:
        assert await async_setup_component(hass, DOMAIN, {})
        await hass.async_block_till_done()
        assert installa.call_count == 2  # nessuna ricarica dopo il cambio del titolo
    assert voce.title == "VMC Soggiorno"
    assert voce.data == {"nome": "master", "host": "192.168.1.160", "titolo": "VMC Soggiorno"}
    assert rinominata.title == "Il mio salotto" and "titolo" not in rinominata.data
    # nome cambiato nell'App Air Guard: al prossimo avvio cambia anche il titolo
    assert await hass.config_entries.async_unload(voce.entry_id)
    with patch(NOME_VMC, return_value="VMC Studio"):
        assert await hass.config_entries.async_setup(voce.entry_id)
        await hass.async_block_till_done()
    assert voce.title == "VMC Studio" and voce.data["nome"] == "master"


async def _apri_elimina(hass: HomeAssistant, voce: MockConfigEntry):
    risultato = await hass.config_entries.options.async_init(voce.entry_id)
    risultato = await hass.config_entries.options.async_configure(
        risultato["flow_id"], {"next_step_id": "elimina"}
    )
    assert risultato["type"] is FlowResultType.MENU and risultato["step_id"] == "elimina"
    assert risultato["menu_options"] == ["elimina_solo_ha", "elimina_dalla_rete"]
    return risultato


async def _voce_sala(hass: HomeAssistant) -> MockConfigEntry:
    voce = MockConfigEntry(
        domain=DOMAIN, unique_id="sala", title="VMC Sala",
        data={"nome": "sala", "host": "192.168.1.161", "titolo": "VMC Sala"},
    )
    voce.add_to_hass(hass)
    assert await hass.config_entries.async_setup(voce.entry_id)
    await hass.async_block_till_done()
    return voce


async def test_elimina_solo_da_home_assistant(hass: HomeAssistant) -> None:
    voce = await _voce_sala(hass)
    risultato = await _apri_elimina(hass, voce)
    with patch(f"{PI}.rimanda_in_access_point") as access_point:
        risultato = await hass.config_entries.options.async_configure(
            risultato["flow_id"], {"next_step_id": "elimina_solo_ha"}
        )
        await hass.async_block_till_done()
    assert risultato["type"] is FlowResultType.ABORT and risultato["reason"] == "eliminata"
    assert risultato["description_placeholders"]["titolo"] == "VMC Sala"
    access_point.assert_not_called()
    assert hass.config_entries.async_get_entry(voce.entry_id) is None
    assert not Path(hass.config.path("packages", "vmc_helty_flow", "sala")).exists()
    assert len(list(Path(hass.config.path("vmc_master_backup")).iterdir())) == 1


async def _avanza_opzioni(hass: HomeAssistant, risultato):
    if risultato["type"] is not FlowResultType.SHOW_PROGRESS:
        return risultato
    await hass.async_block_till_done()
    return await hass.config_entries.options.async_configure(risultato["flow_id"])


async def test_elimina_anche_dalla_rete(hass: HomeAssistant) -> None:
    """La VMC torna in Access Point (lascia il Wi-Fi di casa), poi si elimina la voce."""
    voce = await _voce_sala(hass)
    risultato = await _apri_elimina(hass, voce)
    with patch(f"{PI}.rimanda_in_access_point", return_value="VMC Sala") as access_point:
        risultato = await hass.config_entries.options.async_configure(
            risultato["flow_id"], {"next_step_id": "elimina_dalla_rete"}
        )
        assert risultato["type"] is FlowResultType.SHOW_PROGRESS
        assert risultato["progress_action"] == "access_point"
        risultato = await _avanza_opzioni(hass, risultato)
        await hass.async_block_till_done()
    assert access_point.call_args.args[:2] == (hass.config.config_dir, "192.168.1.161")
    assert risultato["type"] is FlowResultType.ABORT
    assert risultato["reason"] == "eliminata_dalla_rete"
    assert hass.config_entries.async_get_entry(voce.entry_id) is None
    assert not Path(hass.config.path("packages", "vmc_helty_flow", "sala")).exists()


async def test_elimina_dalla_rete_non_riuscita(hass: HomeAssistant) -> None:
    """VMC che non risponde: la voce resta; si puo' riprovare o eliminarla solo da HA."""
    from custom_components.vmc_master.prima_installazione import Failure

    voce = await _voce_sala(hass)
    risultato = await _apri_elimina(hass, voce)
    errore = Failure("vmc_unreachable", "La VMC non risponde all'indirizzo 192.168.1.161.")
    with patch(f"{PI}.rimanda_in_access_point", side_effect=errore):
        risultato = await hass.config_entries.options.async_configure(
            risultato["flow_id"], {"next_step_id": "elimina_dalla_rete"}
        )
        risultato = await _avanza_opzioni(hass, risultato)
    assert risultato["type"] is FlowResultType.MENU and risultato["step_id"] == "errore_rete"
    assert risultato["menu_options"] == ["elimina_dalla_rete", "elimina_solo_ha"]
    assert risultato["description_placeholders"]["errore"] == errore.message
    assert hass.config_entries.async_get_entry(voce.entry_id) is not None
    # riprova: la seconda volta riesce
    with patch(f"{PI}.rimanda_in_access_point", return_value="VMC Sala"):
        risultato = await hass.config_entries.options.async_configure(
            risultato["flow_id"], {"next_step_id": "elimina_dalla_rete"}
        )
        risultato = await _avanza_opzioni(hass, risultato)
        await hass.async_block_till_done()
    assert risultato["reason"] == "eliminata_dalla_rete"
    assert hass.config_entries.async_get_entry(voce.entry_id) is None


class TrasportoFinto:
    """Al posto di motore.Transport: la VMC risponde finche' non riceve l'Access Point."""

    def __init__(self, applica: bool = True) -> None:
        self.inviati: list[tuple[str, bytes]] = []
        self.applica = applica

    def identify(self, ip, interface=""):
        if self.inviati and self.applica:
            raise OSError("la VMC non e' piu' sulla rete di casa")
        return "VMC Sala"

    def send(self, ip, packet, interface=""):
        self.inviati.append((ip, packet))


def test_rimanda_in_access_point(tmp_path: Path) -> None:
    from custom_components.vmc_master import prima_installazione as pi

    cartella = pi.cartella(str(tmp_path))
    cartella.mkdir()
    (cartella / "identity.json").write_text(json.dumps({"ip": "192.168.1.161"}), encoding="utf-8")
    trasporto = TrasportoFinto()
    passi: list[int] = []
    with patch.object(pi.motore, "Transport", return_value=trasporto):
        nome = pi.rimanda_in_access_point(
            str(tmp_path), "192.168.1.161", passi.append, attesa=5, pausa=0
        )
    assert nome == "VMC Sala"
    # stesso pacchetto della funzione «Access Point» della Finestra Prima Installazione VMC
    assert trasporto.inviati == [("192.168.1.161", pi.motore.access_point_packet())]
    assert passi[0] == 10 and passi[-1] == 100
    assert not (cartella / "identity.json").exists()

    # la VMC risponde ancora: errore e nessuna eliminazione
    with patch.object(pi.motore, "Transport", return_value=TrasportoFinto(applica=False)):
        with pytest.raises(pi.Failure) as errore:
            pi.rimanda_in_access_point(str(tmp_path), "192.168.1.161", attesa=0.05, pausa=0.01)
    assert errore.value.code == "ap_not_applied"


async def test_toglie_entita_finestra_clona(hass: HomeAssistant) -> None:
    """Dopo la migrazione della Master le 18 entita' della Finestra Clona e le 27 della
    Finestra Prima Installazione VMC non piu' fornite vengono tolte dal registro;
    quelle ancora fornite restano."""
    from homeassistant.helpers import entity_registry as er

    from custom_components.vmc_master.const import (
        ENTITA_FINESTRA_CLONA,
        ENTITA_PRIMA_INSTALLAZIONE,
    )

    assert len(ENTITA_FINESTRA_CLONA) == 18
    tutte = (*ENTITA_FINESTRA_CLONA, *ENTITA_PRIMA_INSTALLAZIONE)
    voce = MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    )
    voce.add_to_hass(hass)
    assert await hass.config_entries.async_setup(voce.entry_id)
    await hass.async_block_till_done()

    registro = er.async_get(hass)
    for entity_id in tutte:
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
    rimaste = [e for e in tutte if registro.async_get(e) is not None]
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



def test_link_del_readme() -> None:
    """Immagini e video del README vengono dal repository dell'integrazione e ci sono."""
    readme = (RADICE / "README.md").read_text(encoding="utf-8")
    percorsi = [unquote(p) for p in RE_FILE_9.findall(readme)]
    assert len(percorsi) == FILE_COLLEGATI_README
    assert [p for p in percorsi if not (RADICE / p).is_file()] == []
    assert "VMC-HELTY-FLOW/main/" not in readme and "VMC-HELTY-FLOW/raw/main/" not in readme


def test_ricariche_dopo_aggiornamento() -> None:
    """Quali modifiche del package si applicano ricaricando e quali vogliono il riavvio."""
    from custom_components.vmc_master import ORDINE_RICARICHE
    from custom_components.vmc_master.installatore import (
        SERVIZI_RICARICA,
        SERVIZI_RICARICA_SENSORI,
        genera_file,
        ricariche_necessarie,
    )

    # ogni servizio di ricarica ha il suo posto nell'ordine
    servizi = set(SERVIZI_RICARICA.values()) | set(SERVIZI_RICARICA_SENSORI.values())
    assert servizi == set(ORDINE_RICARICHE)

    vecchi = genera_file("master", "192.168.1.160", "9.0.0b1")
    nuovi = genera_file("master", "192.168.1.160", "9.0.0b2")
    # nuova versione dell'integrazione: cambia solo il sensore template della versione
    assert ricariche_necessarie(vecchi["vmc_master.yaml"], nuovi["vmc_master.yaml"]) == {
        "template.reload"
    }
    assert vecchi["vmc_master_automazione.yaml"] == nuovi["vmc_master_automazione.yaml"]
    # solo commenti: niente da fare
    assert ricariche_necessarie(
        vecchi["vmc_master.yaml"], "# commento\r\n" + vecchi["vmc_master.yaml"]
    ) == set()
    # automazione cambiata: si ricaricano le automazioni
    automazione = vecchi["vmc_master_automazione.yaml"]
    assert ricariche_necessarie(
        automazione, automazione.replace("automazione_vmc_master", "automazione_vmc_master_2", 1)
    ) == {"automation.reload"}
    # sensore REST (versione nel repository) cambiato: si ricarica
    package = vecchi["vmc_master.yaml"]
    assert "VMC-HELTY-FLOW-MARKETPLACE/releases/latest" in package
    assert ricariche_necessarie(
        package, package.replace("VMC-HELTY-FLOW-MARKETPLACE/releases/latest", "ALTRO/releases/latest")
    ) == {"rest.reload"}
    # IP cambiato: i sensori TCP vogliono il riavvio
    altro_ip = genera_file("master", "192.168.1.170", "9.0.0b1")
    assert ricariche_necessarie(package, altro_ip["vmc_master.yaml"]) is None
    # file non leggibile: riavvio
    assert ricariche_necessarie(package, "sensor: [") is None


async def test_aggiornamento_senza_secondo_riavvio(hass: HomeAssistant) -> None:
    """Dopo l'aggiornamento dell'integrazione basta il riavvio dell'aggiornamento: il
    package riscritto si ricarica e la riparazione «riavviare» non compare."""
    from pytest_homeassistant_custom_component.common import async_mock_service

    from custom_components.vmc_master.installatore import installa

    # package scritto da una versione precedente dell'integrazione
    esito = await hass.async_add_executor_job(
        installa, hass.config.config_dir, "master", "192.168.1.160", "9.0.0b1"
    )
    assert esito.riavvio_necessario
    chiamate = async_mock_service(hass, "template", "reload")
    voce = MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    )
    voce.add_to_hass(hass)
    assert await hass.config_entries.async_setup(voce.entry_id)
    await hass.async_block_till_done()
    assert len(chiamate) == 1
    assert ir.async_get(hass).async_get_issue(DOMAIN, "riavvio_necessario") is None
    versione = json.loads(MANIFEST.read_text(encoding="utf-8"))["version"]
    package = Path(hass.config.path("packages", "vmc_helty_flow", "master", "vmc_master.yaml"))
    assert f'state: "v.{versione}"' in package.read_text(encoding="utf-8")

    # stessa versione: niente da ricaricare
    assert await hass.config_entries.async_reload(voce.entry_id)
    await hass.async_block_till_done()
    assert len(chiamate) == 1


async def test_ricarica_non_riuscita_chiede_il_riavvio(hass: HomeAssistant) -> None:
    from custom_components.vmc_master.installatore import installa

    await hass.async_add_executor_job(
        installa, hass.config.config_dir, "master", "192.168.1.160", "9.0.0b1"
    )
    # nessun servizio template.reload: la ricarica fallisce e si torna al riavvio
    voce = MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    )
    voce.add_to_hass(hass)
    assert await hass.config_entries.async_setup(voce.entry_id)
    await hass.async_block_till_done()
    assert ir.async_get(hass).async_get_issue(DOMAIN, "riavvio_necessario") is not None


# ---- VMC da installare: collegamento al Wi-Fi da «Aggiungi dispositivo» -------------------

RETI = {
    "vmc_networks": [{"ssid": "VMC_12345678", "signal": 70, "band": "2,4 GHz"}],
    "wifi_networks": [{"ssid": "CasaMia", "signal": 80, "band": "2,4 GHz"}],
}
COLLEGATA = {"ap_ssid": "VMC_12345678", "ip": "192.168.1.50", "name": "VMC Bagno", "mac": "AA:BB:CC:DD:EE:FF"}


class MotoreFinto:
    """Al posto di prima_installazione.esegui: registra le azioni, puo' fallire."""

    def __init__(self, errori: dict[str, Exception] | None = None) -> None:
        self.azioni: list[tuple[str, dict | None]] = []
        self.errori = errori or {}

    def __call__(self, config_dir, azione, dati=None, avanzamento=None):
        self.azioni.append((azione, dati))
        if avanzamento is not None:
            avanzamento(50)
        if azione in self.errori:
            raise self.errori[azione]
        return {}


async def _avanza(hass: HomeAssistant, risultato):
    """Attende la fine della barra di avanzamento e passa al passo seguente (se il motore
    finisce subito, Home Assistant e' gia' passato da solo al passo seguente)."""
    if risultato["type"] is not FlowResultType.SHOW_PROGRESS:
        return risultato
    await hass.async_block_till_done()
    return await hass.config_entries.flow.async_configure(risultato["flow_id"])


async def test_da_installare_senza_supervisor(hass: HomeAssistant) -> None:
    risultato = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    risultato = await hass.config_entries.flow.async_configure(
        risultato["flow_id"], {"next_step_id": "da_installare"}
    )
    assert risultato["type"] is FlowResultType.ABORT
    assert risultato["reason"] == "senza_supervisor"


async def test_da_installare_senza_wifi(hass: HomeAssistant) -> None:
    from custom_components.vmc_master.prima_installazione import Failure

    motore = MotoreFinto({"scan": Failure("no_wifi", "nessuna scheda")})
    with patch(HASSIO, return_value=True), patch(f"{PI}.esegui", motore):
        risultato = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"next_step_id": "da_installare"}
        )
        risultato = await _avanza(hass, risultato)
    assert risultato["type"] is FlowResultType.ABORT and risultato["reason"] == "senza_wifi"


async def test_da_installare_completo(hass: HomeAssistant) -> None:
    """Ricerca, collegamento, IP prenotato diverso e verificato, nome dalla VMC."""
    from custom_components.vmc_master.prima_installazione import LED_HINT, Failure

    MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    ).add_to_hass(hass)
    motore = MotoreFinto({
        "configure": Failure("back_to_access_point", "La VMC è tornata in Access Point." + LED_HINT),
    })
    collegata = dict(COLLEGATA)
    with (
        patch(HASSIO, return_value=True),
        patch(f"{PI}.esegui", motore),
        patch(f"{PI}.stato", return_value=RETI),
        patch(f"{PI}.rete_del_server", return_value="CasaMia"),
        patch(f"{PI}.ultima_vmc", side_effect=lambda _c: dict(collegata)),
        patch(PROVA_VMC, return_value=True),
    ):
        risultato = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        # ultima VMC collegata non ancora aggiunta: si puo' riprendere
        assert risultato["menu_options"] == ["in_rete", "da_installare", "riprendi"]
        assert risultato["description_placeholders"] == {"rete_vmc": "VMC_12345678", "ip": "192.168.1.50"}
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"next_step_id": "da_installare"}
        )
        risultato = await _avanza(hass, risultato)
        assert risultato["step_id"] == "rete_vmc" and risultato["errors"] == {}
        campi = {str(k): k for k in risultato["data_schema"].schema}
        assert campi["rete_vmc"].default() == "VMC_12345678"
        assert campi["password_vmc"].default() == "12345678"
        assert campi["rete_casa"].default() == "CasaMia"
        dati = {"rete_vmc": "VMC_12345678", "password_vmc": "12345678", "rete_casa": "CasaMia"}

        # password di casa troppo corta: lo dice il motore, il Wi-Fi non viene toccato
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {**dati, "password_casa": "corta"}
        )
        assert risultato["errors"] == {"base": "motore"}
        assert "8" in risultato["description_placeholders"]["errore"]
        assert motore.azioni == [("scan", None)]

        # la VMC non si collega: messaggio del motore senza il rimando alla vecchia tabella
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {**dati, "password_casa": "password-di-casa"}
        )
        risultato = await _avanza(hass, risultato)
        assert risultato["type"] is FlowResultType.MENU and risultato["step_id"] == "errore"
        assert risultato["description_placeholders"]["errore"] == "La VMC è tornata in Access Point."
        assert motore.azioni[-1] == ("configure", {
            "ap_ssid": "VMC_12345678", "ap_password": "12345678", "home_ssid": "CasaMia",
            "home_password": "password-di-casa", "final_ip": "",
        })
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"next_step_id": "rete_vmc"}
        )
        assert risultato["step_id"] == "rete_vmc" and risultato["errors"] == {}

        # riprova: collegata
        motore.errori.clear()
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {**dati, "password_casa": "password-di-casa"}
        )
        risultato = await _avanza(hass, risultato)
        assert risultato["step_id"] == "ip_fisso"
        assert risultato["description_placeholders"]["mac"] == "AA:BB:CC:DD:EE:FF"
        campi = {str(k): k for k in risultato["data_schema"].schema}
        assert campi["host"].default() == "192.168.1.50"

        # IP prenotato diverso: la verifica fallisce, poi riesce
        motore.errori["verify"] = Failure("vmc_unreachable", "La VMC non risponde all'IP inserito.")
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"host": "192.168.1.60"}
        )
        risultato = await _avanza(hass, risultato)
        assert risultato["step_id"] == "ip_fisso" and risultato["errors"] == {"base": "motore"}
        assert motore.azioni[-1] == ("verify", {"ip": "192.168.1.60", "ap_ssid": "VMC_12345678"})
        motore.errori.clear()
        collegata["ip"] = "192.168.1.60"
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"host": "192.168.1.60"}
        )
        risultato = await _avanza(hass, risultato)
        assert risultato["step_id"] == "nome"
        assert risultato["description_placeholders"]["proposta"] == "bagno"
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"nome": "bagno"}
        )
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    assert risultato["data"] == {"nome": "bagno", "host": "192.168.1.60", "titolo": "VMC Bagno"}


async def test_prima_vmc_da_installare_diventa_master(hass: HomeAssistant) -> None:
    """La prima VMC in assoluto: dopo il collegamento si chiama «master», senza domande."""
    with (
        patch(HASSIO, return_value=True),
        patch(f"{PI}.ultima_vmc", return_value=dict(COLLEGATA)),
        patch(PROVA_VMC, return_value=True),
    ):
        risultato = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"next_step_id": "riprendi"}
        )
        assert risultato["step_id"] == "ip_fisso"
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"host": "192.168.1.50"}
        )
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    # la prima VMC si chiama «master», ma la voce mostra il nome della VMC
    assert risultato["title"] == "VMC Bagno"
    assert risultato["data"] == {"nome": "master", "host": "192.168.1.50", "titolo": "VMC Bagno"}


async def test_ripristino_wifi_all_avvio(hass: HomeAssistant) -> None:
    """Riavvio durante il collegamento: all'avvio il Wi-Fi del server torna com'era."""
    from custom_components.vmc_master.prima_installazione import CARTELLA_MOTORE, Failure

    cartella = Path(hass.config.path(CARTELLA_MOTORE))
    cartella.mkdir()
    (cartella / "restore.json").write_text("{}", encoding="utf-8")
    motore = MotoreFinto({"recover": Failure("restore_failed", "Ripristino non riuscito.")})
    with patch(f"{PI}.esegui", motore):
        assert await async_setup_component(hass, DOMAIN, {})
        await hass.async_block_till_done()
    assert motore.azioni == [("recover", None)]
    # ripristino non riuscito: lo dice una notifica
    from homeassistant.components import persistent_notification

    assert any(
        n["notification_id"] == f"{DOMAIN}_ripristino_wifi"
        for n in persistent_notification._async_get_or_create_notifications(hass).values()
    )


def test_motore_identico_alla_release_8_6_0() -> None:
    """motore_installa_vmc.py e' il programma della Finestra Prima Installazione VMC,
    carattere per carattere (comando vmc_master_installa_vmc_esegui del package)."""
    import yaml

    class Caricatore(yaml.SafeLoader):
        pass

    Caricatore.add_multi_constructor("!", lambda loader, suffix, node: None)
    cartella = RADICE / "custom_components" / "vmc_master"
    with open(cartella / "package" / "vmc_master.yaml", encoding="utf-8") as file:
        package = yaml.load(file, Loader=Caricatore)
    comando = package["shell_command"]["vmc_master_installa_vmc_esegui"]
    inizio = comando.index("SOURCE = r'''") + len("SOURCE = r'''")
    fine = comando.index("'''.lstrip(")
    assert comando[inizio:fine].lstrip("\n") == (cartella / "motore_installa_vmc.py").read_text(
        encoding="utf-8"
    )


def test_master_senza_prima_installazione() -> None:
    """Package, automazione e scheda della master non contengono piu' la Finestra Prima
    Installazione VMC; l'aggiornamento dalla versione con la finestra non chiede il riavvio."""
    from custom_components.vmc_master.const import ENTITA_PRIMA_INSTALLAZIONE
    from custom_components.vmc_master.installatore import genera_file, ricariche_necessarie
    from custom_components.vmc_master.trasforma import (
        adatta_link_repository,
        adatta_versione,
        per_vmc,
        rimuovi_clona,
        sostituisci_ip,
    )

    assert len(ENTITA_PRIMA_INSTALLAZIONE) == 27
    sorgenti = RADICE / "custom_components" / "vmc_master" / "package"
    file = genera_file("master", "192.168.1.160", "9.0.0b12")
    for testo in file.values():
        assert "installa_vmc" not in testo and "INSTALLA VMC" not in testo
    scheda = per_vmc(
        (sorgenti / "vmc_master_scheda_manuale_interfaccia.txt").read_text(encoding="utf-8"),
        "master",
        "192.168.1.160",
    )
    assert "installa_vmc" not in scheda and "Prima Installazione VMC" not in scheda
    # package della master come lo scriveva la 9.0.0b11 (con la finestra)
    yaml_master = (sorgenti / "vmc_master.yaml").read_text(encoding="utf-8")
    vecchio = adatta_link_repository(
        adatta_versione(sostituisci_ip(rimuovi_clona(yaml_master), "192.168.1.160"), "9.0.0b12")
    )
    assert "vmc_master_installa_vmc_stato" in vecchio
    servizi = ricariche_necessarie(vecchio, file["vmc_master.yaml"])
    assert servizi is not None
    assert {"command_line.reload", "template.reload", "script.reload", "automation.reload"} <= servizi
