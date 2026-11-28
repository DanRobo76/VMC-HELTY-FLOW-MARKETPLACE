"""Prova configurazione da interfaccia, VMC nativa e scheda."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote
from unittest.mock import patch

import pytest
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.helpers import issue_registry as ir
from homeassistant.helpers.selector import TextSelector, TextSelectorType
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


# Link a immagini e video, contati uno per uno: 75 nella scheda (50 file diversi),
# 10 in ciascuno dei due README (9 file diversi): README.md nella radice, che il
# Marketplace mostra, e .github/README.md, che GitHub mostra al suo posto
FILE_COLLEGATI_SCHEDA = 75
FILE_COLLEGATI_README = {"README.md": 10, ".github/README.md": 10}
# Link al repository della release manuale (non seguito da «-MARKETPLACE»)
RE_LINK_8 = re.compile(r"DanRobo76/VMC-HELTY-FLOW(?![-\w])")
# File letti dal repository dell'integrazione (immagini, video)
RE_FILE_9 = re.compile(
    r"DanRobo76/VMC-HELTY-FLOW-MARKETPLACE/(?:main|raw/main)/([^\s\"'<>?]+)"
)
# ... e dalla scheda nativa, che usa il repository della versione nativa (const.REPOSITORY)
RE_FILE_NATIVA = re.compile(
    r"DanRobo76/VMC-HELTY-FLOW-MASTER/(?:main|raw/main)/([^\s\"'<>?]+)"
)


def _serve_checkout_completo() -> None:
    """immagini/ e Video/ sono export-ignore: nell'archivio della release non ci sono."""
    mancanti = [c for c in ("immagini", "Video") if not (RADICE / c).is_dir()]
    if mancanti:
        pytest.skip(
            f"Serve un checkout git completo: {', '.join(mancanti)} non c'è "
            "(export-ignore, esclusa dall'archivio della release)"
        )


def _controlla_link(testo: str, re_file: re.Pattern[str] = RE_FILE_9) -> int:
    """Nessun link al repository VMC-HELTY-FLOW; ogni file collegato esiste nel
    repository dell'integrazione. Restituisce quanti file collegati ci sono."""
    assert RE_LINK_8.findall(testo) == []
    percorsi = [unquote(p) for p in re_file.findall(testo)]
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
    _serve_checkout_completo()
    await async_setup_component(hass, "http", {})
    risultato = await _aggiungi(hass, "master", "192.168.1.160")
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    # la VMC nativa parte subito: nessun package scritto, nessun riavvio chiesto
    assert not Path(hass.config.path("packages")).exists()
    assert ir.async_get(hass).async_get_issue(DOMAIN, "riavvio_necessario") is None
    assert hass.config_entries.async_entries(DOMAIN)[0].runtime_data.vmc is not None

    # Seconda VMC, non raggiungibile: avviso subito dopo l'IP, poi «Aggiungi comunque» e il
    # nome scritto a mano
    risultato = await _aggiungi(hass, "sala", "192.168.1.161", risponde=False)
    assert risultato["type"] is FlowResultType.MENU
    assert risultato["step_id"] == "non_raggiungibile"
    assert risultato["menu_options"] == ["in_rete", "aggiungi_comunque"]
    risultato = await hass.config_entries.flow.async_configure(
        risultato["flow_id"], {"next_step_id": "aggiungi_comunque"}
    )
    assert risultato["step_id"] == "nome_manuale" and risultato["errors"] == {}
    risultato = await hass.config_entries.flow.async_configure(
        risultato["flow_id"], {"nome": "sala"}
    )
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    assert not Path(hass.config.path("packages")).exists()

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
        # la scheda nativa: nessuna cartella dei backup (la VMC non ha file da spostare)
        assert testo.count("vmc_master_backup") == 0
        assert testo.count("Controllo aggiornamenti non riuscito (nessuna connessione a GitHub)") == 1
        assert "Strumenti per sviluppatori" not in testo and "Velocita 1" not in testo
        # Pannello Informazioni: «GitHub» apre il repository della versione nativa
        assert testo.count('href="https://github.com/DanRobo76/VMC-HELTY-FLOW-MASTER">GitHub</a>') == 1
        assert "/raw/main/Video/VMC_MASTER_promo_IT.mp4" not in testo
        # l'immagine apre la pagina dell'integrazione nel Marketplace (pulsante «Aggiorna»);
        # il nome del repository in questo link è quello di scheda_nativa.txt
        assert len(re.findall(
            r'<a href="/marketplace/repository\?owner=DanRobo76&repository=VMC-HELTY-FLOW-'
            r'(?:MARKETPLACE|MASTER)&category=integration"><img ',
            testo,
        )) == 1
        # immagini e video: tutti dal repository della versione nativa, e ci sono tutti
        assert RE_FILE_9.findall(testo) == []
        assert _controlla_link(testo, RE_FILE_NATIVA) == FILE_COLLEGATI_SCHEDA
    risposta = await client.get("/api/vmc_master/scheda/inesistente")
    assert risposta.status == 404
    risposta = await client.get("/vmc_master_frontend/vmc-master-card.js")
    assert risposta.status == 200


async def test_errori_nome_e_ip(hass: HomeAssistant) -> None:
    MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    ).add_to_hass(hass)
    for ip in ("999.999.999.999", "192.168.1.010", "192.168.01.160"):
        risultato = await _aggiungi(hass, "sala", ip)
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
        "nome": "salagrande",
        "host": "192.168.1.161",
        "titolo": "VMC Sala Grande",
        "da_inizializzare": True,
    }

    # VMC che non risponde: avviso prima del nome; «Correggi l'IP» riparte dall'IP scritto
    risultato = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    risultato = await hass.config_entries.flow.async_configure(
        risultato["flow_id"], {"next_step_id": "in_rete"}
    )
    with patch(NOME_VMC, return_value=None):
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"host": "192.168.1.163"}
        )
    assert risultato["type"] is FlowResultType.MENU
    assert risultato["step_id"] == "non_raggiungibile"
    assert risultato["description_placeholders"] == {"ip": "192.168.1.163"}
    risultato = await hass.config_entries.flow.async_configure(
        risultato["flow_id"], {"next_step_id": "in_rete"}
    )
    assert risultato["step_id"] == "in_rete"
    campo = next(iter(risultato["data_schema"].schema))
    assert campo.default() == "192.168.1.163"
    # ancora nessuna risposta: di nuovo l'avviso, poi «Aggiungi comunque» e il nome
    with patch(NOME_VMC, return_value=None):
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"host": "192.168.1.162"}
        )
    assert risultato["step_id"] == "non_raggiungibile"
    risultato = await hass.config_entries.flow.async_configure(
        risultato["flow_id"], {"next_step_id": "aggiungi_comunque"}
    )
    assert risultato["step_id"] == "nome_manuale" and risultato["errors"] == {}
    risultato = await hass.config_entries.flow.async_configure(
        risultato["flow_id"], {"nome": "camera"}
    )
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    assert risultato["title"] == "VMC camera"
    assert risultato["data"] == {
        "nome": "camera", "host": "192.168.1.162", "titolo": "VMC camera", "da_inizializzare": True
    }


def test_nome_da_vmc() -> None:
    from custom_components.vmc_master.config_flow import nome_da_vmc

    assert nome_da_vmc("VMC Sala Grande") == "salagrande"
    assert nome_da_vmc("Cucina_2") == "cucina"
    assert nome_da_vmc("VMC") == "vmc"
    assert nome_da_vmc("Città*") == "citta"
    assert nome_da_vmc("Soggiorno-Grande") == "soggiornog"
    assert nome_da_vmc("1234") == ""
    assert nome_da_vmc("VMC_Cucina") == "cucina"
    assert nome_da_vmc("vmc-Sala_Grande") == "salagrande"


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
    # l'IP nuovo non risponde: avviso; un secondo Invia lo salva lo stesso
    risultato = await hass.config_entries.options.async_configure(
        risultato["flow_id"], {"host": "192.168.1.170"}
    )
    assert risultato["type"] is FlowResultType.FORM
    assert risultato["errors"] == {"host": "ip_non_risponde"}
    with patch(PROVA_VMC, return_value=False) as prova:
        risultato = await hass.config_entries.options.async_configure(
            risultato["flow_id"], {"host": "192.168.1.170"}
        )
    prova.assert_not_called()
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    # la VMC nativa riparte subito con il nuovo IP
    assert voce.data["host"] == "192.168.1.170"
    assert voce.runtime_data.ip == "192.168.1.170"


def test_rinomina_protegge_la_cartella_dei_backup() -> None:
    from custom_components.vmc_master.trasforma import rinomina

    assert rinomina("vmc_master_backup master", "prova") == "vmc_master_backup prova"


def test_titolo_voce() -> None:
    from custom_components.vmc_master.config_flow import titolo_voce

    assert titolo_voce("VMC Soggiorno", "master") == "VMC Soggiorno"
    assert titolo_voce("vmc studio", "studio") == "vmc studio"
    assert titolo_voce("Soggiorno", "master") == "VMC Soggiorno"
    assert titolo_voce("", "master") == "VMC master"
    assert titolo_voce(None, "camera") == "VMC camera"


async def test_titolo_delle_voci_gia_aggiunte(hass: HomeAssistant) -> None:
    """Le VMC aggiunte prima della 9.0.0b13 («VMC master») prendono il nome della VMC
    all'avvio, senza ricaricare la voce; un nome scelto dall'utente resta."""
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
    with patch(NOME_VMC, return_value="VMC Soggiorno"), patch.object(
        hass.config_entries, "async_reload"
    ) as ricarica:
        assert await async_setup_component(hass, DOMAIN, {})
        await hass.async_block_till_done()
    ricarica.assert_not_called()  # nessuna ricarica dopo il cambio del titolo
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
    # niente da spostare: nessun file della VMC fuori da Home Assistant
    assert not Path(hass.config.path("packages")).exists()
    assert not Path(hass.config.path("vmc_master_backup")).exists()


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
    hass.config.language = "it"  # messaggi del motore in italiano, come scritti
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
    cartella.mkdir(parents=True)
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


class TrasportoAlterno(TrasportoFinto):
    """Dopo l'invio risponde secondo la sequenza (True = risponde, False = nessuna
    risposta); finita la sequenza non risponde piu'."""

    def __init__(self, risposte: list[bool]) -> None:
        super().__init__()
        self.risposte = list(risposte)
        self.controlli = 0

    def identify(self, ip, interface=""):
        if not self.inviati:
            return "VMC Sala"
        self.controlli += 1
        if self.risposte and self.risposte.pop(0):
            return "VMC Sala"
        raise OSError("nessuna risposta")


def test_rimanda_in_access_point_dopo_due_assenze(tmp_path: Path) -> None:
    """La voce si elimina solo dopo due controlli di fila senza risposta: una sola
    risposta persa non basta."""
    from custom_components.vmc_master import prima_installazione as pi

    # persa, risponde, persa, persa: finisce al quarto controllo, non al primo
    trasporto = TrasportoAlterno([False, True, False, False])
    with patch.object(pi.motore, "Transport", return_value=trasporto):
        nome = pi.rimanda_in_access_point(str(tmp_path), "192.168.1.161", attesa=5, pausa=0)
    assert nome == "VMC Sala"
    assert trasporto.controlli == 4

    # risposte perse una alla volta, mai due di fila: la VMC e' ancora sul Wi-Fi di casa
    trasporto = TrasportoAlterno([False, True] * 1000)
    with patch.object(pi.motore, "Transport", return_value=trasporto):
        with pytest.raises(pi.Failure) as errore:
            pi.rimanda_in_access_point(str(tmp_path), "192.168.1.161", attesa=0.05, pausa=0.001)
    assert errore.value.code == "ap_not_applied"
    assert trasporto.controlli >= 2


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
        assert testo.count("VMC-HELTY-FLOW/raw/main/Video/VMC_MASTER_promo_IT.mp4") == 0
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
    """Immagini e video dei due README vengono dal repository dell'integrazione nativa
    (VMC-HELTY-FLOW-MASTER, il nome nuovo del repository) e ci sono; nessun link resta al
    nome vecchio VMC-HELTY-FLOW-MARKETPLACE."""
    _serve_checkout_completo()
    for nome, quanti in FILE_COLLEGATI_README.items():
        readme = (RADICE / nome).read_text(encoding="utf-8")
        assert _controlla_link(readme, RE_FILE_NATIVA) == quanti, nome
        assert RE_FILE_9.findall(readme) == [], nome
        assert "VMC-HELTY-FLOW/main/" not in readme and "VMC-HELTY-FLOW/raw/main/" not in readme
        # nessun link relativo: in .github/ porterebbe a un altro percorso
        assert re.findall(r"\]\((?!https?:|#|mailto:)", readme) == [], nome
        assert re.findall(r"(?:src|href|srcset)=\"(?!https?:|#|mailto:)", readme) == [], nome


def test_readme_marketplace_e_github() -> None:
    """Il Marketplace mostra README.md, GitHub .github/README.md: chi è nel Marketplace
    ha già aggiunto il repository e non vede i passi per farlo."""
    marketplace = (RADICE / "README.md").read_text(encoding="utf-8")
    github = (RADICE / ".github" / "README.md").read_text(encoding="utf-8")
    for testo in ("| 📌 **1. Aggiungere il repository** (primo passo) |\n|---|\n",
                  "| 📌 **1. Add the repository** (first step) |\n|---|\n",
                  "2. **Installare**: cercare **VMC Master** nel Marketplace e premere **Installa**.",
                  "2. **Install**: search for **VMC Master** in the Marketplace and press **Install**.",
                  "6. **Una volta per ogni VMC**, nel pannello **Opzioni** della scheda:",
                  "6. **Once per unit**, in the card's **Opzioni** panel:",
                  "**Altre VMC**: ripetere il punto 4.", "**More units**: repeat step 4.",
                  "**VMC nuova** (senza l'App Air Guard", "**New unit** (without the Air Guard app",
                  "Dopo l'installazione tutto si regola", "After installation everything is set"):
        assert testo in github and testo not in marketplace, testo
    # versione nativa: configuration.yaml serve solo per le Notifiche Audio (righe tts); b45:
    # prima Installare, poi le Notifiche Audio, dove si suggerisce di verificare se la
    # stringa tts c'è e di aggiungere le righe solo se mancano (nel Marketplace punto 2, su
    # GitHub punto 3, dopo il riquadro «Aggiungere il repository» e «Installare»)
    for testo in ("**Notifiche Audio**: si suggerisce di verificare che `configuration.yaml` contenga la stringa `tts:` (una volta sola):",
                  "**Audio notifications**: it is recommended to check that `configuration.yaml` contains the `tts:` string (once):"):
        assert f"\n2. {testo}" in marketplace and f"\n3. {testo}" in github, testo
    for testo in ("   - se sono già presenti le righe seguenti, chiudere il file senza modificarlo:",
                  "   - in caso di assenza, per le Notifiche Audio aggiungerle in fondo al file e salvare con l'icona del **dischetto**.",
                  "   - if the following lines are already present, close the file without changing it:",
                  "   - if they are missing, add them at the end of the file for audio notifications and save with the **disk** icon."):
        assert marketplace.count(testo) == 1 and github.count(testo) == 1, testo
    for testo in ("aggiungere in fondo:", "add at the end:", "modificare `configuration.yaml`",
                  "edit `configuration.yaml`", "Solo per le Notifiche Audio",
                  "Only for audio notifications", "verificare se sono già presenti",
                  "check whether these lines"):
        assert testo not in marketplace and testo not in github, testo
    for testo in ("1. **Installare**: cercare il pulsante **Installa** in alto a destra, premerlo e seguire le indicazioni a schermo.",
                  "1. **Install**: look for the **Install** button at the top right, press it and follow the on-screen instructions.",
                  "Per ogni VMC nel pannello **Opzioni** della scheda:",
                  "For each unit in the card's **Opzioni** panel:",
                  "**Altre VMC**: *Impostazioni → Dispositivi e servizi → pulsante «Aggiungi integrazione» in basso a destra → VMC Master*.",
                  "**More units**: *Settings → Devices & services → «Add integration» button at the bottom right → VMC Master*."):
        assert testo in marketplace and testo not in github, testo
    # nel Marketplace l'Installazione finisce con la scheda: niente rimando a Configurazione
    for testo in ("**: vedere **Configurazione**", "**: see **Configuration**", "5. **", "**Aggiungere la VMC**", "**Add the unit**",
                  "Cosa lo rende diverso", "Scenario tipico", "What makes it different",
                  "Typical scenario", "Servono proprio", "These exact lines",
                  "si aggiunge con il suo IP", "add each unit with its IP",
                  "riavviare una volta sola", "restart once", "ASPIRATORE MASTER"):
        assert testo not in marketplace, testo
    for testo in (marketplace, github):
        assert "<audio" not in testo
        assert "Strumenti → Riavvia" not in testo and "Developer tools → Restart" not in testo
        # versione nativa: nessun passo «Riavviare» nella nuova installazione
        # (dopo l'aggiunta la VMC nativa parte subito: nessun riavvio)
        assert "3. **Riavviare**:" not in testo and "3. **Restart**:" not in testo
        assert testo.count("cliccare **«VMC Master: riavviare Home Assistant»**") == 0
        assert testo.count("click **«VMC Master: restart Home Assistant»**") == 0


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
    hass.config.language = "it"  # messaggi del motore in italiano, come scritti
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
    assert risultato["data"] == {
        "nome": "bagno", "host": "192.168.1.60", "titolo": "VMC Bagno", "da_inizializzare": True
    }


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
    assert risultato["data"] == {
        "nome": "master", "host": "192.168.1.50", "titolo": "VMC Bagno", "da_inizializzare": True
    }


async def test_ripristino_wifi_all_avvio(hass: HomeAssistant) -> None:
    """Riavvio durante il collegamento: all'avvio il Wi-Fi del server torna com'era."""
    from custom_components.vmc_master.prima_installazione import CARTELLA_MOTORE, Failure

    cartella = Path(hass.config.path(CARTELLA_MOTORE))
    cartella.mkdir(parents=True)
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


def test_motore_identico_alla_copia_del_package() -> None:
    """motore_installa_vmc.py e' il programma della Finestra Prima Installazione VMC,
    carattere per carattere (comando vmc_master_installa_vmc_esegui del package), tranne
    la cartella interna predefinita (ROOT): nell'area dei dati di Home Assistant
    (/config/.storage/vmc_master_installa_vmc) invece di /config/.vmc_master_installa_vmc,
    che la versione nativa non scrive piu'. Senza la riga di comando e il worker separato
    (da NORMALIZE alla fine, con i loro import, ACTIONS e la prima riga «#!»), che la
    versione nativa non usa: la frase della descrizione che li presentava dice che non
    ci sono."""
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
    root_della_beta = 'ROOT = Path(__file__).resolve().parents[1] / ".vmc_master_installa_vmc"\n'
    root_nativa = (
        'ROOT = Path(__file__).resolve().parents[2] / ".storage" / "vmc_master_installa_vmc"\n'
    )
    copia = comando[inizio:fine].lstrip("\n")
    # la riga di comando e il worker: tutto da NORMALIZE (usato solo da launch) alla fine
    riga_di_comando = copia.index("\n\n\nNORMALIZE = {\n")
    assert copia.rstrip().endswith('if __name__ == "__main__":\n    raise SystemExit(main())')
    copia = copia[: riga_di_comando + 1]
    cambi = [
        (root_della_beta, root_nativa),
        ("#!/usr/bin/env python3\n", ""),
        (
            (
                "La CLI avvia un worker separato, così il limite di 60 s di shell_command non\n"
                "interrompe collegamento, ripristino e verifica.\n"
            ),
            (
                "Nell'integrazione nativa il motore si usa da prima_installazione.py: la riga "
                "di comando e\nil worker separato del package (8.6.0) non ci sono.\n"
            ),
        ),
        ("import argparse\n", ""),
        ("import signal\n", ""),
        ("import subprocess\n", ""),
        ("import sys\n", ""),
        (
            (
                'ACTIONS = ("diagnose", "configure", "verify", "recover", "rename", '
                '"ap_password", "ap_mode", "scan")\n'
            ),
            "",
        ),
    ]
    for vecchio, nuovo in cambi:
        assert copia.count(vecchio) == 1, vecchio
        copia = copia.replace(vecchio, nuovo)
    assert copia == (cartella / "motore_installa_vmc.py").read_text(encoding="utf-8")


def test_master_senza_prima_installazione() -> None:
    """Package, automazione e scheda della master (come li scriveva la beta) non
    contengono piu' la Finestra Prima Installazione VMC."""
    from custom_components.vmc_master.installatore import genera_file
    from custom_components.vmc_master.trasforma import per_vmc

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


async def test_cambia_ip_aggiorna_la_vmc_appena_collegata(hass: HomeAssistant) -> None:
    """Dopo «Cambia l'IP della VMC» la VMC non viene riproposta da «Continua con la VMC
    appena collegata» (identity.json prende il nuovo IP)."""
    from custom_components.vmc_master import prima_installazione as pi

    cartella = pi.cartella(hass.config.config_dir)
    cartella.mkdir(parents=True)
    (cartella / "identity.json").write_text(
        json.dumps({**COLLEGATA, "ip": "192.168.1.160"}), encoding="utf-8"
    )
    MockConfigEntry(
        domain=DOMAIN, unique_id="sala", data={"nome": "sala", "host": "192.168.1.161"}
    ).add_to_hass(hass)
    voce = MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    )
    voce.add_to_hass(hass)
    assert await hass.config_entries.async_setup(voce.entry_id)
    await hass.async_block_till_done()
    risultato = await hass.config_entries.options.async_init(voce.entry_id)
    risultato = await hass.config_entries.options.async_configure(
        risultato["flow_id"], {"next_step_id": "cambia_ip"}
    )
    # IP gia' usato da un'altra VMC: errore; IP che risponde: salvato subito
    risultato = await hass.config_entries.options.async_configure(
        risultato["flow_id"], {"host": "192.168.1.161"}
    )
    assert risultato["type"] is FlowResultType.FORM
    assert risultato["errors"] == {"host": "ip_in_uso"}
    with patch(NOME_VMC, return_value="VMC Master"):
        risultato = await hass.config_entries.options.async_configure(
            risultato["flow_id"], {"host": "192.168.1.170"}
        )
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    assert pi.ultima_vmc(hass.config.config_dir)["ip"] == "192.168.1.170"
    risultato = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert risultato["menu_options"] == ["in_rete", "da_installare"]


async def test_elimina_dalla_rete_con_la_finestra_chiusa(hass: HomeAssistant) -> None:
    """Finestra chiusa mentre la VMC passa in Access Point: la voce si elimina lo stesso."""
    import threading

    voce = await _voce_sala(hass)
    risultato = await _apri_elimina(hass, voce)
    via = threading.Event()

    def access_point(*_args, **_kwargs):
        via.wait(5)
        return "VMC Sala"

    # funzione vera, non un Mock: nei test un Mock gira subito, non in un thread
    with patch(f"{PI}.rimanda_in_access_point", new=access_point):
        risultato = await hass.config_entries.options.async_configure(
            risultato["flow_id"], {"next_step_id": "elimina_dalla_rete"}
        )
        assert risultato["type"] is FlowResultType.SHOW_PROGRESS
        hass.config_entries.options.async_abort(risultato["flow_id"])  # finestra chiusa
        assert hass.config_entries.async_get_entry(voce.entry_id) is not None
        assert hass.config_entries.options.async_progress() == []
        via.set()
        await hass.async_block_till_done(wait_background_tasks=True)
    assert hass.config_entries.async_get_entry(voce.entry_id) is None
    assert not Path(hass.config.path("packages", "vmc_helty_flow", "sala")).exists()


# Entita' del package della VMC «sala» come le salva il registro:
# (entity_id, dominio, piattaforma, unique_id)
ENTITA_PACKAGE_SALA = (
    ("sensor.vmc_sala_status_ventola_memorizzata", "sensor", "template", "vmc_sala_status_ventola_memorizzata"),
    ("sensor.vmc_sala_status_ip", "sensor", "command_line", "vmc_sala_status_ip"),
    ("sensor.vmc_sala_versione_repository", "sensor", "rest", "vmc_sala_versione_repository"),
    ("script.vmc_sala_aggiorna_elenco_entita_co2_interna", "script", "script", "vmc_sala_aggiorna_elenco_entita_co2_interna"),
    ("input_boolean.vmc_sala_attese_inizializzate", "input_boolean", "input_boolean", "vmc_sala_attese_inizializzate"),
    ("timer.vmc_sala_countdown_avvisi", "timer", "timer", "vmc_sala_countdown_avvisi"),
    ("automation.vmc_sala_cambio_ip_vmc", "automation", "automation", "vmc_sala_cambio_ip_vmc"),
    ("automation.automazione_vmc_sala", "automation", "automation", "automazione_vmc_sala"),
)


def _registra(registro, entity_id: str, dominio: str, piattaforma: str, unique_id: str, **altro):
    oggetto = entity_id.split(".")[1]
    creata = registro.async_get_or_create(
        dominio, piattaforma, unique_id, suggested_object_id=oggetto, **altro
    )
    assert creata.entity_id == entity_id
    return creata


def test_id_del_package(tmp_path: Path) -> None:
    """Gli id del package della beta si leggono come li salva il registro: dominio,
    piattaforma e unique_id (sono quelli che la conferma del passaggio toglie)."""
    from custom_components.vmc_master.installatore import genera_file
    from custom_components.vmc_master.passaggio import (
        _id_del_package_della_beta,
        cartella_package,
        id_del_package,
    )

    config_dir = str(tmp_path)
    cartella = cartella_package(config_dir, "sala")
    cartella.mkdir(parents=True)
    for nome_file, testo in genera_file("sala", "192.168.1.161", "9.0.0").items():
        (cartella / nome_file).write_text(testo, encoding="utf-8")
    id_package = id_del_package(config_dir, "sala")
    assert id_package == _id_del_package_della_beta("sala")
    for _entity_id, *chiave in ENTITA_PACKAGE_SALA:
        assert tuple(chiave) in id_package
    assert all("vmc_sala_" in unique_id or unique_id == "automazione_vmc_sala" for *_d, unique_id in id_package)
    # 133 unique_id e 14 automazioni, piu' le chiavi di aiutanti, timer e script
    assert sum(1 for d, p, _u in id_package if p in ("template", "command_line", "rest")) == 133
    assert sum(1 for d, _p, _u in id_package if d == "automation") == 14
    # b28: timer del countdown di riattivazione; b30: timer del countdown di gruppo;
    # b31: campo di esito della verifica dell'IP (input_text ..._ip_insert_esito);
    # b34: Spia Comando non eseguito del Calendario (input_boolean);
    # b38: automazioni Registro Comandi e Scelte, Rimando della Scelta e Letture Ravvicinate, 3 input_text del registro;
    # b39: Comando non Eseguito durante una Fascia (input_text);
    # b40: automazione Ripartenza della VMC
    assert len(id_package) == 473
    # nessun id in comune con un'altra VMC
    assert id_package.isdisjoint(_id_del_package_della_beta("salab"))
    # tag di Home Assistant e unique_id di blocco dei template (file aggiunti a mano)
    (cartella / "altro.yaml").write_text(
        "template:\n  - unique_id: blocco\n    sensor:\n      - unique_id: uno\n        state: !secret x\n",
        encoding="utf-8",
    )
    assert ("sensor", "template", "blocco-uno") in id_del_package(config_dir, "sala")
    # cartella gia' tolta: gli id del package che la beta scriveva
    assert id_del_package(config_dir, "inesistente") == _id_del_package_della_beta("inesistente")


async def test_notifiche_in_inglese(hass: HomeAssistant) -> None:
    """Notifiche in italiano solo se Home Assistant e' in italiano."""
    from homeassistant.components import persistent_notification

    from custom_components.vmc_master.prima_installazione import CARTELLA_MOTORE, Failure

    hass.config.language = "en"
    cartella = Path(hass.config.path(CARTELLA_MOTORE))
    cartella.mkdir(parents=True)
    (cartella / "restore.json").write_text("{}", encoding="utf-8")
    motore = MotoreFinto({"recover": Failure("restore_failed", "Ripristino non riuscito.")})
    with patch(f"{PI}.esegui", motore):
        assert await async_setup_component(hass, DOMAIN, {})
        await hass.async_block_till_done()
    notifica = persistent_notification._async_get_or_create_notifications(hass)[
        f"{DOMAIN}_ripristino_wifi"
    ]
    assert notifica["title"] == "VMC Master: server Wi-Fi restore failed"


async def test_ip_prenotato_senza_mac(hass: HomeAssistant) -> None:
    """MAC non rilevato e IP prenotato diverso: basta che a quell'IP risponda la VMC con
    lo stesso nome; se non risponde o risponde un altro dispositivo, lo dice la finestra."""
    MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    ).add_to_hass(hass)
    senza_mac = {**COLLEGATA, "mac": ""}
    motore = MotoreFinto()
    with (
        patch(HASSIO, return_value=True),
        patch(f"{PI}.esegui", motore),
        patch(f"{PI}.ultima_vmc", return_value=dict(senza_mac)),
    ):
        risultato = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"next_step_id": "riprendi"}
        )
        assert risultato["step_id"] == "ip_fisso"
        assert risultato["description_placeholders"]["mac"] == "-"
        # IP gia' usato da un'altra VMC
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"host": "192.168.1.160"}
        )
        assert risultato["errors"] == {"host": "ip_in_uso"}
        for letto, errore in ((None, "ip_non_risponde_riavvia"), ("VMC Altra", "ip_altro_dispositivo")):
            with patch(NOME_VMC, return_value=letto):
                risultato = await hass.config_entries.flow.async_configure(
                    risultato["flow_id"], {"host": "192.168.1.60"}
                )
            assert risultato["step_id"] == "ip_fisso" and risultato["errors"] == {"host": errore}
        with patch(NOME_VMC, return_value="VMC Bagno"):
            risultato = await hass.config_entries.flow.async_configure(
                risultato["flow_id"], {"host": "192.168.1.60"}
            )
        assert risultato["step_id"] == "nome"
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"nome": "bagno"}
        )
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    assert risultato["data"]["host"] == "192.168.1.60"
    # nessuna verifica del motore (che senza MAC non si puo' fare)
    assert [azione for azione, _dati in motore.azioni] == []


async def test_server_su_un_altro_wifi(hass: HomeAssistant) -> None:
    """Server su un Wi-Fi diverso dalla rete di casa scelta: la password della sua rete,
    che il motore usa per riportarlo li' (restore_password), si chiede in un passo a parte,
    solo in questo caso. La maschera delle reti ha solo campi obbligatori."""
    hass.config.language = "it"  # messaggi del motore in italiano, come scritti
    motore = MotoreFinto()
    with (
        patch(HASSIO, return_value=True),
        patch(f"{PI}.esegui", motore),
        patch(f"{PI}.stato", return_value=RETI),
        patch(f"{PI}.rete_del_server", return_value="Casa_5G"),
        patch(f"{PI}.rete_da_ripristinare", return_value="Casa_5G"),
        patch(f"{PI}.ultima_vmc", return_value={}),
    ):
        risultato = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"next_step_id": "da_installare"}
        )
        risultato = await _avanza(hass, risultato)
        assert risultato["step_id"] == "rete_vmc"
        campi = {str(k): k for k in risultato["data_schema"].schema}
        assert list(campi) == ["rete_vmc", "password_vmc", "rete_casa", "password_casa"]
        assert all(isinstance(k, vol.Required) for k in campi.values())
        # le due password si scrivono nascoste, anche quella dell'access point della VMC
        for nome in ("password_vmc", "password_casa"):
            selettore = risultato["data_schema"].schema[campi[nome]]
            assert isinstance(selettore, TextSelector)
            assert selettore.config["type"] == TextSelectorType.PASSWORD
        dati = {
            "rete_vmc": "VMC_12345678", "password_vmc": "12345678",
            "rete_casa": "CasaMia", "password_casa": "password-di-casa",
        }
        risultato = await hass.config_entries.flow.async_configure(risultato["flow_id"], dati)
        assert risultato["step_id"] == "password_server" and risultato["errors"] == {}
        assert [str(k) for k in risultato["data_schema"].schema] == ["password_server"]
        assert risultato["description_placeholders"]["rete_del_server"] == "Casa_5G"
        assert risultato["description_placeholders"]["rete_casa"] == "CasaMia"
        assert motore.azioni == [("scan", None)]
        # vuota (l'interfaccia non la manda, ma si controlla lo stesso)
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"password_server": ""}
        )
        assert risultato["errors"] == {"password_server": "password_server_mancante"}
        # password troppo corta: lo dice il motore prima di toccare il Wi-Fi
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"password_server": "corta"}
        )
        assert risultato["step_id"] == "password_server"
        assert risultato["errors"] == {"base": "motore"}
        assert "Password del Wi-Fi attuale del server" in risultato["description_placeholders"]["errore"]
        assert motore.azioni == [("scan", None)]
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"password_server": "password-5g"}
        )
        risultato = await _avanza(hass, risultato)
    assert motore.azioni[-1] == ("configure", {
        "ap_ssid": "VMC_12345678", "ap_password": "12345678", "home_ssid": "CasaMia",
        "home_password": "password-di-casa", "final_ip": "", "restore_password": "password-5g",
    })


async def test_server_sulla_rete_di_casa_scelta(hass: HomeAssistant) -> None:
    """Server gia' sulla rete di casa scelta: torna con la password di casa, il passo della
    password del server non compare."""
    motore = MotoreFinto()
    with (
        patch(HASSIO, return_value=True),
        patch(f"{PI}.esegui", motore),
        patch(f"{PI}.stato", return_value=RETI),
        patch(f"{PI}.rete_del_server", return_value="CasaMia"),
        patch(f"{PI}.rete_da_ripristinare", return_value="CasaMia"),
        patch(f"{PI}.ultima_vmc", return_value={}),
    ):
        risultato = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"next_step_id": "da_installare"}
        )
        risultato = await _avanza(hass, risultato)
        assert "password_server" not in [str(k) for k in risultato["data_schema"].schema]
        risultato = await hass.config_entries.flow.async_configure(risultato["flow_id"], {
            "rete_vmc": "VMC_12345678", "password_vmc": "12345678",
            "rete_casa": "CasaMia", "password_casa": "password-di-casa",
        })
        assert risultato.get("step_id") != "password_server"
        risultato = await _avanza(hass, risultato)
    azione, dati = motore.azioni[-1]
    assert azione == "configure" and "restore_password" not in dati


def test_motore_password_del_server_e_reti_grandi() -> None:
    """Il motore riceve la password del Wi-Fi del server; con una rete di casa piu' ampia
    di /24 cerca la VMC nei 256 indirizzi intorno al server."""
    from custom_components.vmc_master import prima_installazione as pi

    base = {"ap_ssid": "VMC_1", "ap_password": "12345678", "home_ssid": "Casa", "home_password": "password1"}
    richiesta = pi.motore.normalize_request({**base, "restore_password": "password-5g"})
    assert richiesta["restore_password"] == "password-5g" and richiesta["lan_cidr"] == ""
    assert pi.motore.normalize_request(base)["restore_password"] == ""
    with pytest.raises(pi.Failure) as errore:
        pi.motore.normalize_request({**base, "home_ssid": "x" * 33})
    assert errore.value.message == "«Rete Wi-Fi di casa» deve avere da 1 a 32 caratteri."

    def info(*indirizzi):
        return {"interfaces": [
            {"interface": "end0", "type": "ethernet", "connected": True, "ipv4": {"address": list(indirizzi)}},
        ]}

    assert pi.rete_di_ricerca(info("192.168.2.10/22")) == "192.168.2.0/24"
    assert pi.rete_di_ricerca(info("192.168.1.10/24")) == ""
    obiettivi = pi.motore.lan_targets(info("192.168.2.10/22"), pi.rete_di_ricerca(info("192.168.2.10/22")))
    assert len(obiettivi) == 253 and "192.168.2.10" not in obiettivi

    class SupervisorFinto:
        def __init__(self, auth):
            self.auth = auth

        def info(self):
            return {"interfaces": [{
                "interface": "wlan0", "type": "wireless", "enabled": True, "connected": True,
                "wifi": {"ssid": "Casa_5G", "mode": "infrastructure", "auth": self.auth},
            }]}

    with patch.object(pi.motore, "Supervisor", return_value=SupervisorFinto("wpa-psk")):
        assert pi.rete_da_ripristinare("/config") == "Casa_5G"
    with patch.object(pi.motore, "Supervisor", return_value=SupervisorFinto("open")):
        assert pi.rete_da_ripristinare("/config") == ""
    # senza Supervisor
    assert pi.rete_da_ripristinare("/config") == ""


async def test_riparazione_riavvio(hass: HomeAssistant) -> None:
    """«Riavviare Home Assistant» nelle Riparazioni: chiede conferma, controlla la
    configurazione, poi riavvia. Gli altri avvisi si chiudono con una semplice conferma."""
    from homeassistant.components.repairs import ConfirmRepairFlow
    from pytest_homeassistant_custom_component.common import async_mock_service

    from custom_components.vmc_master.repairs import RiavvioFlow, async_create_fix_flow

    riavvii = async_mock_service(hass, "homeassistant", "restart")
    flusso = await async_create_fix_flow(hass, "riavvio_necessario", None)
    assert isinstance(flusso, RiavvioFlow)
    flusso.hass = hass
    flusso.flow_id = "prova"
    flusso.handler = DOMAIN
    risultato = await flusso.async_step_init()
    assert risultato["type"] is FlowResultType.FORM and risultato["step_id"] == "confirm"
    assert riavvii == []
    with patch("homeassistant.config.async_check_ha_config_file", return_value=None):
        risultato = await flusso.async_step_confirm({})
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    assert len(riavvii) == 1
    altro = await async_create_fix_flow(hass, "packages_non_abilitati_sala", None)
    assert type(altro) is ConfirmRepairFlow


def test_rete_di_ricerca_passata_al_motore(tmp_path: Path) -> None:
    """«configure»: con una rete di casa piu' ampia di /24 il motore riceve lan_cidr con i
    256 indirizzi intorno al server; con una /24 lan_cidr resta vuoto; un lan_cidr gia'
    scritto non si cambia."""
    from custom_components.vmc_master import prima_installazione as pi

    richieste: list[dict] = []
    indirizzo = ["192.168.2.10/22"]

    class SupervisorFinto:
        def info(self):
            return {"interfaces": [{
                "interface": "end0", "type": "ethernet", "connected": True,
                "ipv4": {"address": list(indirizzo)},
            }]}

    class EngineFinto:
        def __init__(self, root):
            self.root = Path(root)
            self.supervisor = SupervisorFinto()

        def run(self, dati):
            richieste.append(dati)

    with patch.object(pi.motore, "Engine", EngineFinto):
        pi.esegui(str(tmp_path), "configure", {"ap_ssid": "VMC_1"})
        indirizzo[:] = ["192.168.1.10/24"]
        pi.esegui(str(tmp_path), "configure", {"ap_ssid": "VMC_1"})
        pi.esegui(str(tmp_path), "configure", {"ap_ssid": "VMC_1", "lan_cidr": "10.0.0.0/24"})
    assert [r["lan_cidr"] for r in richieste] == ["192.168.2.0/24", "", "10.0.0.0/24"]


async def test_toglie_gli_avvisi_della_beta(hass: HomeAssistant, hass_storage) -> None:
    """Gli avvisi della beta che la versione nativa non ha più (package non caricati, anche
    quello unico delle versioni fino alla 9.0.0b18, e voce disabilitata, che la beta
    salvava) e l'elenco delle VMC eliminate della pulizia del registro si tolgono
    all'avvio dell'integrazione."""
    for issue_id, persistente in (
        ("packages_non_abilitati", False),
        ("packages_non_abilitati_master", False),
        ("voce_disabilitata_sala", True),
    ):
        ir.async_create_issue(
            hass, DOMAIN, issue_id, is_fixable=False, is_persistent=persistente,
            severity=ir.IssueSeverity.ERROR, translation_key=issue_id.rsplit("_", 1)[0],
            translation_placeholders={"nome": "master", "titolo": "VMC sala"},
        )
    hass_storage["vmc_master.vmc_eliminate"] = {
        "version": 1, "minor_version": 1, "key": "vmc_master.vmc_eliminate",
        "data": {"nomi": ["cucina"]},
    }
    voce = MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    )
    voce.add_to_hass(hass)
    assert await hass.config_entries.async_setup(voce.entry_id)
    await hass.async_block_till_done()
    registro = ir.async_get(hass)
    assert [i for d, i in registro.issues if d == DOMAIN] == []
    assert "vmc_master.vmc_eliminate" not in hass_storage

