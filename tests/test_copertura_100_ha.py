"""Copertura al 100 %: parti dell'integrazione che girano dentro Home Assistant
(__init__.py e config_flow.py) e non ancora provate.

Solo test, nessuna modifica al codice dell'integrazione. VMC, motore Wi-Fi, processi e
traduzioni sono finti: nessun hardware e nessuna rete reale.
"""

from __future__ import annotations

import asyncio
import ipaddress
import itertools
import logging
from pathlib import Path
import threading
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant import config_entries
from homeassistant.components import persistent_notification
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import EVENT_DATA_ENTRY_FLOW_PROGRESS_UPDATE, FlowResultType
from homeassistant.helpers import entity_registry as er, issue_registry as ir
from homeassistant.helpers.storage import Store
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

import custom_components.vmc_master as integrazione
from custom_components.vmc_master import config_flow
from custom_components.vmc_master.const import DOMAIN
from custom_components.vmc_master.installatore import cartella_vmc
from custom_components.vmc_master.prima_installazione import LED_HINT, Failure

from .test_integrazione import COLLEGATA, RETI, MotoreFinto, _apri_elimina, _avanza, _voce_sala

PI = "custom_components.vmc_master.prima_installazione"
HASSIO = "custom_components.vmc_master.config_flow.is_hassio"
PROVA_VMC = "custom_components.vmc_master.config_flow.async_prova_vmc"
NOME_VMC = "custom_components.vmc_master.config_flow.async_nome_vmc"
IP = "192.168.1.160"
# funzione vera: nei test di questo file async_nome_vmc è sostituita (nessuna VMC in rete)
_NOME_VMC_VERO = config_flow.async_nome_vmc


@pytest.fixture(autouse=True)
def _nessuna_vmc_in_rete():
    """Nessuna VMC vera: all'avvio il nome non si legge e il titolo della voce resta."""
    with patch(NOME_VMC, return_value=None):
        yield


def _notifiche(hass: HomeAssistant) -> dict:
    return persistent_notification._async_get_or_create_notifications(hass)


def _record(messaggio: str, argomenti: tuple = ()) -> logging.LogRecord:
    return logging.LogRecord("prova", logging.ERROR, __file__, 1, messaggio, argomenti, None)


# ---------------------------------------------------------------- avvio dell'integrazione
async def test_filtro_ping_gia_presente(hass: HomeAssistant) -> None:
    """Integrazione avviata di nuovo nello stesso Home Assistant: un solo filtro del ping."""
    gia = logging.Filter("gia presente")
    hass.data[integrazione.DATI_FILTRO_PING] = gia
    assert await async_setup_component(hass, DOMAIN, {})
    assert hass.data[integrazione.DATI_FILTRO_PING] is gia
    assert gia not in logging.getLogger(integrazione.LOGGER_COMMAND_LINE).filters


def test_versione_su_disco(tmp_path: Path) -> None:
    """Versione su disco solo se c'è prepara.py e il manifest si legge."""
    with patch.object(integrazione, "_CARTELLA", tmp_path):
        assert integrazione._versione_su_disco() is None  # versione senza prepara.py
        (tmp_path / "prepara.py").write_text("", encoding="utf-8")
        assert integrazione._versione_su_disco() is None  # manifest assente
        (tmp_path / "manifest.json").write_text("{rotto", encoding="utf-8")
        assert integrazione._versione_su_disco() is None
        (tmp_path / "manifest.json").write_text('{"domain": "vmc_master"}', encoding="utf-8")
        assert integrazione._versione_su_disco() is None
        (tmp_path / "manifest.json").write_text('{"version": "9.9.9"}', encoding="utf-8")
        assert integrazione._versione_su_disco() == "9.9.9"


class ProcessoFinto:
    """Processo separato che prepara i package: risponde, sbaglia o non finisce in tempo."""

    def __init__(self, returncode: int = 0, errori: bytes = b"", lento: bool = False) -> None:
        self.returncode, self.errori, self.lento = returncode, errori, lento
        self.kill = MagicMock()
        self.atteso = False

    async def communicate(self):
        if self.lento:
            raise TimeoutError
        return b"[]", self.errori

    async def wait(self):
        self.atteso = True
        return self.returncode


def _voce_caricata(hass: HomeAssistant, stato=ConfigEntryState.LOADED) -> MockConfigEntry:
    voce = MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": IP}, state=stato
    )
    voce.add_to_hass(hass)
    return voce


async def _prepara(hass: HomeAssistant, **avvio):
    with (
        patch.object(integrazione, "_versione_su_disco", return_value="99.0.0"),
        patch.object(integrazione.asyncio, "create_subprocess_exec", new=AsyncMock(**avvio)) as finto,
    ):
        await integrazione._prepara_aggiornamento(hass, "9.0.0")
    return finto


async def test_prepara_senza_voci_caricate(hass: HomeAssistant) -> None:
    _voce_caricata(hass, ConfigEntryState.SETUP_ERROR)
    avvio = await _prepara(hass)
    avvio.assert_not_called()


async def test_prepara_processo_non_avviato(hass: HomeAssistant, caplog) -> None:
    _voce_caricata(hass)
    await _prepara(hass, side_effect=OSError("memoria esaurita"))
    assert "Package non preparati per la versione 99.0.0: memoria esaurita" in caplog.text


async def test_prepara_processo_troppo_lento(hass: HomeAssistant, caplog) -> None:
    """Oltre il tempo massimo il processo si ferma: ogni file resta vecchio o nuovo."""
    _voce_caricata(hass)
    processo = ProcessoFinto(lento=True)
    avvio = await _prepara(hass, return_value=processo)
    assert avvio.await_args.args[-3:] == (
        str(integrazione._CARTELLA), hass.config.config_dir, '[["master", "192.168.1.160"]]')
    processo.kill.assert_called_once()
    assert processo.atteso and "Package non preparati per la versione 99.0.0" in caplog.text


async def test_prepara_processo_con_errore(hass: HomeAssistant, caplog) -> None:
    _voce_caricata(hass)
    processo = ProcessoFinto(returncode=1, errori=b"Traceback\nKeyError: 'version'\n")
    await _prepara(hass, return_value=processo)
    processo.kill.assert_not_called()
    assert "Package non preparati per la versione 99.0.0: Traceback\nKeyError: 'version'" in caplog.text
    assert "Package preparati" not in caplog.text


async def test_ripristino_wifi_non_riuscito_in_italiano(hass: HomeAssistant) -> None:
    hass.config.language = "it"
    with (
        patch(f"{PI}.ripristino_in_sospeso", return_value=True),
        patch(f"{PI}.esegui", side_effect=Failure("restore_failed", "Ripristino non riuscito.")),
    ):
        await integrazione._ripristina_wifi_server(hass)
    notifica = _notifiche(hass)[f"{DOMAIN}_ripristino_wifi"]
    assert notifica["title"] == "VMC Master: ripristino del Wi-Fi del server non riuscito"
    assert notifica["message"].startswith("Ripristino non riuscito.\n\nIl Wi-Fi del server potrebbe")


async def test_disco_pieno_in_italiano(hass: HomeAssistant) -> None:
    hass.config.language = "it"
    voce = _voce_caricata(hass, ConfigEntryState.NOT_LOADED)
    with patch.object(integrazione, "installa", side_effect=OSError(28, "Spazio esaurito")):
        assert not await hass.config_entries.async_setup(voce.entry_id)
    assert voce.state is ConfigEntryState.SETUP_ERROR
    assert voce.reason.startswith("File del package della VMC master non scritti")
    assert "Controllare lo spazio libero sul disco" in voce.reason


async def test_notifica_file_modificati_in_inglese(hass: HomeAssistant) -> None:
    hass.config.language = "en"
    voce = _voce_caricata(hass, ConfigEntryState.NOT_LOADED)
    assert await hass.config_entries.async_setup(voce.entry_id)
    await hass.async_block_till_done()
    automazione = cartella_vmc(hass.config.config_dir, "master") / "vmc_master_automazione.yaml"
    automazione.write_bytes(automazione.read_bytes() + b"# a mano\r\n")
    with patch("custom_components.vmc_master.persistent_notification.async_create") as notifica:
        assert await hass.config_entries.async_reload(voce.entry_id)
        await hass.async_block_till_done()
    chiamate = [c for c in notifica.call_args_list if "modificati" in c.kwargs["notification_id"]]
    assert len(chiamate) == 1
    assert chiamate[0].kwargs["title"] == "VMC Master: files of unit master edited by hand"
    testo = chiamate[0].args[1]
    assert testo.startswith("These package files of unit master had been edited by hand")
    assert "- `vmc_master_automazione.yaml`" in testo
    assert "`/config/vmc_master_backup/master_modificati_" in testo


# ---------------------------------------------------------------- VMC eliminate
def _elenco_eliminate(hass_storage, nomi: list) -> None:
    hass_storage[integrazione.CHIAVE_ELIMINATE] = {
        "version": 1, "minor_version": 1, "key": integrazione.CHIAVE_ELIMINATE, "data": {"nomi": nomi},
    }


async def test_vmc_eliminata_gia_ricordata(hass: HomeAssistant, hass_storage) -> None:
    """Nome già nell'elenco delle VMC eliminate: l'elenco non si riscrive."""
    _elenco_eliminate(hass_storage, ["sala", 5])
    voce = MockConfigEntry(domain=DOMAIN, unique_id="sala", data={"nome": "sala", "host": "192.168.1.161"})
    with patch.object(integrazione, "_id_del_package_generato", return_value=None):
        await integrazione.async_remove_entry(hass, voce)
    assert hass_storage[integrazione.CHIAVE_ELIMINATE]["data"] == {"nomi": ["sala", 5]}


async def test_vmc_eliminate_che_restano(hass: HomeAssistant, hass_storage) -> None:
    """All'avvio restano nell'elenco: cartella di nuovo presente, package non leggibile,
    entità ancora fornite. Se l'elenco non cambia non si riscrive."""
    _elenco_eliminate(hass_storage, ["sala", "bagno", "cucina"])
    cartella_vmc(hass.config.config_dir, "sala").mkdir(parents=True)
    registro = er.async_get(hass)
    registro.async_get_or_create(
        "sensor", "command_line", "vmc_cucina_status_ip", suggested_object_id="vmc_cucina_status_ip"
    )
    hass.states.async_set("sensor.vmc_cucina_status_ip", "ON-Line")
    generato = integrazione._id_del_package_generato
    with (
        patch.object(
            integrazione, "_id_del_package_generato",
            side_effect=lambda nome: None if nome == "bagno" else generato(nome),
        ),
        patch.object(Store, "async_save") as salva,
    ):
        await integrazione._togli_entita_vmc_eliminate(hass)
    salva.assert_not_called()
    assert registro.async_get("sensor.vmc_cucina_status_ip") is not None


def test_id_di_configurazioni_di_forma_inattesa() -> None:
    id_package: set = set()
    integrazione._id_della_configurazione(["non", "un", "dizionario"], id_package)
    assert id_package == set()
    integrazione._id_della_configurazione({
        "automation": [{"alias": "senza id"}, "testo", {"id": 7}],
        "input_boolean": ["non", "un", "dizionario"],
        "template": ["testo", {"unique_id": "blocco", "sensor": [{"unique_id": "uno"}, {"name": "senza"}]}],
        "rest": {"sensor": {"unique_id": "due"}},
        "sensor": [{"platform": "rest", "unique_id": "tre"}, {"unique_id": "senza piattaforma"}],
    }, id_package)
    assert id_package == {
        ("automation", "automation", "7"),
        ("sensor", "template", "blocco-uno"),
        ("sensor", "rest", "due"),
        ("sensor", "rest", "tre"),
    }


def test_package_generato_illeggibile(caplog) -> None:
    file = {"vmc_sala.yaml": "sensor: [\n", "vmc_sala_script_cambio_ip.sh": "#!/bin/sh\n"}
    with patch.object(integrazione, "genera_file", return_value=file):
        assert integrazione._id_del_package_generato("sala") is None
    assert "Package della VMC sala non leggibile" in caplog.text


def test_rimetti_ip_con_un_file_mancante(tmp_path: Path) -> None:
    cartella = cartella_vmc(str(tmp_path), "sala")
    cartella.mkdir(parents=True)
    (cartella / "vmc_sala.yaml").write_text("sensor:\n  - host: 192.168.1.99\n", encoding="utf-8")
    integrazione._rimetti_ip_nel_package(str(tmp_path), "sala", "192.168.1.99", "192.168.1.161")
    assert (cartella / "vmc_sala.yaml").read_text(encoding="utf-8") == "sensor:\n  - host: 192.168.1.161\n"
    assert not (cartella / "vmc_sala_script_cambio_nome.sh").exists()


# ---------------------------------------------------------------- filtri dei log
def test_filtro_tcp_casi_limite() -> None:
    filtro = integrazione._FiltroTcpVmc()
    # nessuna VMC configurata: passa tutto
    assert filtro.filter(_record("Unable to connect to 192.168.1.160 on port 5001"))
    filtro.ips = frozenset({IP})
    # messaggio che non si può formattare: passa com'è
    assert filtro.filter(_record("Valore %d", ("non un numero",)))


async def test_filtro_ping_messaggio_non_formattabile(hass: HomeAssistant) -> None:
    filtro = integrazione._FiltroPingAvvio(hass)
    assert filtro.filter(_record("Timeout for command: %d", ("ping",)))


async def test_filtro_tcp_assente(hass: HomeAssistant) -> None:
    integrazione._aggiorna_ip_filtro_tcp(hass)
    integrazione._togli_filtro_tcp(hass)
    assert integrazione.DATI_FILTRO_TCP not in hass.data


# ---------------------------------------------------------------- voce della VMC
def _voce_sala_non_caricata(hass: HomeAssistant, **altro) -> MockConfigEntry:
    voce = MockConfigEntry(
        domain=DOMAIN, unique_id="sala", data={"nome": "sala", "host": "192.168.1.161"}, **altro
    )
    voce.add_to_hass(hass)
    return voce


async def test_voce_aggiornata_senza_cambio_ip(hass: HomeAssistant) -> None:
    """Cambia solo il titolo della voce: il package non si reinstalla."""
    voce = _voce_sala_non_caricata(hass)
    voce.runtime_data = "192.168.1.161"
    with patch.object(hass.config_entries, "async_reload") as ricarica:
        await integrazione._async_aggiornata(hass, voce)
    ricarica.assert_not_called()


async def test_titolo_con_vmc_che_non_risponde(hass: HomeAssistant) -> None:
    voce = _voce_sala_non_caricata(hass, title="VMC sala")
    with patch(NOME_VMC, side_effect=OSError("rete assente")) as nome:
        integrazione._aggiorna_titolo_dopo_avvio(hass, voce)
        await hass.async_block_till_done(wait_background_tasks=True)
    nome.assert_awaited_once_with("192.168.1.161")
    assert voce.title == "VMC sala" and "titolo" not in voce.data


async def test_ricariche_gia_fatte(hass: HomeAssistant) -> None:
    """Ricariche già fatte insieme a un'altra VMC: nulla da ricaricare."""
    voce = _voce_sala_non_caricata(hass)
    with patch.object(integrazione, "_async_ricarica") as ricarica:
        integrazione._ricarica_dopo_avvio(hass, voce, set())
        await hass.async_block_till_done()
    ricarica.assert_not_called()


async def test_package_caricato_di_un_altra_vmc(hass: HomeAssistant) -> None:
    """Package caricato di una VMC che non è la master: niente pulizia della Finestra Clona."""
    voce = _voce_sala_non_caricata(hass)
    hass.states.async_set("sensor.vmc_sala_status_ip", "ON-Line")
    with patch.object(integrazione, "_togli_entita_non_piu_fornite") as togli:
        integrazione._controlla_packages_dopo_avvio(hass, voce, "sala")
    togli.assert_not_called()
    assert ir.async_get(hass).async_get_issue(DOMAIN, "packages_non_abilitati_sala") is None


# ---------------------------------------------------------------- config_flow: IP e nome della VMC
def test_ip_con_zeri_iniziali_su_python_vecchio() -> None:
    """Python fino alla 3.9.4 accettava gli zeri iniziali (192.168.1.010 = 192.168.1.10):
    l'IP resta non valido perché non è scritto come lo intende Python."""

    def tollerante(testo: str) -> ipaddress.IPv4Address:
        return ipaddress.IPv4Address(".".join(str(int(parte)) for parte in testo.split(".")))

    with patch.object(config_flow, "ipaddress", SimpleNamespace(IPv4Address=tollerante)):
        assert not config_flow.ip_valido("192.168.1.010")
        assert config_flow.ip_valido("192.168.1.10")


class LettoreFinto:
    def __init__(self, pezzi: list[bytes]) -> None:
        self.pezzi = list(pezzi)

    async def read(self, quanti: int) -> bytes:
        return self.pezzi.pop(0)[:quanti] if self.pezzi else b""


class ScrittoreFinto:
    def __init__(self) -> None:
        self.scritti: list[bytes] = []
        self.chiuso = False

    def write(self, dati: bytes) -> None:
        self.scritti.append(dati)

    async def drain(self) -> None:
        pass

    def close(self) -> None:
        self.chiuso = True


async def _nome_da_vmc_finta(pezzi: list[bytes], orologio) -> tuple[str | None, ScrittoreFinto]:
    """async_nome_vmc con connessione e orologio del ciclo finti (solo in config_flow)."""
    scrittore = ScrittoreFinto()

    async def apri(_ip, _porta):
        return LettoreFinto(pezzi), scrittore

    ciclo = SimpleNamespace(time=lambda: next(orologio))
    finto = SimpleNamespace(
        open_connection=apri, wait_for=asyncio.wait_for, get_running_loop=lambda: ciclo
    )
    with patch.object(config_flow, "asyncio", finto):
        return await _NOME_VMC_VERO("192.168.1.60"), scrittore


async def test_nome_vmc_risposta_lunga() -> None:
    """Risposta più lunga del massimo: si legge solo fino a 256 byte."""
    nome, scrittore = await _nome_da_vmc_finta([b"VMNM " + b"A" * 300], itertools.count())
    assert nome == "A" * 251
    assert scrittore.scritti == [b"VMNM?"] and scrittore.chiuso


async def test_nome_vmc_tempo_massimo_superato() -> None:
    """Risposta a metà quando il tempo massimo è già passato: vale quello che è arrivato."""
    nome, scrittore = await _nome_da_vmc_finta([b"VMNM Pr", b"ova\r\n"], iter([0.0, 1.0, 10.0]))
    assert nome == "Pr" and scrittore.chiuso


async def test_messaggio_senza_traduzioni(hass: HomeAssistant) -> None:
    """Traduzioni non disponibili: resta il messaggio del motore, senza il rimando ai LED."""
    hass.config.language = "en"
    errore = Failure("vmc_unreachable", "La VMC non risponde." + LED_HINT)
    with patch.object(config_flow, "async_get_translations", side_effect=RuntimeError("rotte")):
        assert await config_flow.async_messaggio_errore(hass, errore) == "La VMC non risponde."


# ---------------------------------------------------------------- config_flow: aggiungi dispositivo
async def _menu(hass: HomeAssistant):
    return await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )


async def test_nomi_e_ip_escludendo_una_voce(hass: HomeAssistant) -> None:
    voce = _voce_caricata(hass, ConfigEntryState.NOT_LOADED)
    flusso = config_flow.VmcMasterConfigFlow()
    flusso.hass, flusso.handler = hass, DOMAIN
    flusso.context = {"source": config_entries.SOURCE_USER}
    assert flusso._nomi_e_ip_in_uso() == ({"master"}, {IP})
    assert flusso._nomi_e_ip_in_uso(escludi=voce.entry_id) == (set(), set())


@pytest.mark.parametrize("riga", ["", "  host: 999.999.999.999\n"])
async def test_installazione_manuale_senza_ip_valido(hass: HomeAssistant, riga: str) -> None:
    """Installazione manuale della master senza un IP valido nel package: nessun IP proposto."""
    cartella = cartella_vmc(hass.config.config_dir, "master")
    cartella.mkdir(parents=True)
    (cartella / "vmc_master.yaml").write_text("sensor:\n" + riga, encoding="utf-8")
    risultato = await _menu(hass)
    risultato = await hass.config_entries.flow.async_configure(
        risultato["flow_id"], {"next_step_id": "in_rete"}
    )
    assert risultato["step_id"] == "in_rete"
    campi = {str(k): k for k in risultato["data_schema"].schema}
    assert campi["host"].default() == ""


async def test_continua_senza_sapere_se_risponde(hass: HomeAssistant) -> None:
    """Se non si sa ancora se la VMC risponde, la si prova prima di creare la voce."""
    _voce_caricata(hass, ConfigEntryState.NOT_LOADED)
    risultato = await _menu(hass)
    flusso = hass.config_entries.flow._progress[risultato["flow_id"]]
    with patch(PROVA_VMC, return_value=False) as prova:
        passo = await flusso._async_continua("sala", "192.168.1.161", None)
    prova.assert_awaited_once_with("192.168.1.161")
    assert passo["type"] is FlowResultType.FORM and passo["step_id"] == "non_raggiungibile"
    with patch(PROVA_VMC, return_value=True):
        passo = await flusso._async_continua("sala", "192.168.1.161", None)
    assert passo["type"] is FlowResultType.CREATE_ENTRY
    assert passo["data"] == {"nome": "sala", "host": "192.168.1.161", "titolo": "VMC sala"}


async def test_ricerca_non_riuscita_e_password_del_server(hass: HomeAssistant) -> None:
    """Ricerca delle reti non riuscita: la rete VMC si scrive a mano. Collegamento rifiutato
    perché il server è passato a un'altra rete: si ripete la ricerca, la rete di casa
    scritta resta e compare il campo della password del server."""
    hass.config.language = "it"
    motore = MotoreFinto({
        "scan": Failure("scan_failed", "La scheda Wi-Fi del server non ha restituito l'elenco delle reti."),
        "configure": Failure("restore_password_required", "Serve la password della rete Ufficio."),
    })
    with (
        patch(HASSIO, return_value=True),
        patch(f"{PI}.esegui", motore),
        patch(f"{PI}.stato", return_value=RETI),
        patch(f"{PI}.rete_del_server", return_value="CasaMia") as rete_del_server,
        patch(f"{PI}.rete_da_ripristinare", side_effect=["", "Ufficio", "Ufficio"]),
    ):
        risultato = await _menu(hass)
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"next_step_id": "da_installare"}
        )
        risultato = await _avanza(hass, risultato)
        assert risultato["step_id"] == "rete_vmc" and risultato["errors"] == {"base": "motore"}
        assert risultato["description_placeholders"]["errore"] == (
            "La scheda Wi-Fi del server non ha restituito l'elenco delle reti.")
        risultato = await hass.config_entries.flow.async_configure(risultato["flow_id"], {
            "rete_vmc": "VMC_12345678", "password_vmc": "12345678",
            "rete_casa": "CasaMia", "password_casa": "password-di-casa",
        })
        risultato = await _avanza(hass, risultato)
        assert risultato["type"] is FlowResultType.MENU and risultato["step_id"] == "errore"
        assert risultato["description_placeholders"]["errore"] == "Serve la password della rete Ufficio."
        motore.errori.clear()
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"next_step_id": "cerca"}
        )
        risultato = await _avanza(hass, risultato)
    assert risultato["step_id"] == "rete_vmc" and risultato["errors"] == {}
    campi = {str(k): k for k in risultato["data_schema"].schema}
    assert campi["rete_casa"].default() == "CasaMia" and "password_server" in campi
    assert risultato["description_placeholders"]["rete_del_server"] == "Ufficio"
    rete_del_server.assert_called_once()
    assert [azione for azione, _dati in motore.azioni] == ["scan", "configure", "scan"]


async def test_ip_fisso_non_valido(hass: HomeAssistant) -> None:
    with patch(f"{PI}.ultima_vmc", return_value=dict(COLLEGATA)):
        risultato = await _menu(hass)
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"next_step_id": "riprendi"}
        )
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"host": "192.168.1.256"}
        )
    assert risultato["step_id"] == "ip_fisso" and risultato["errors"] == {"host": "ip_non_valido"}


# ---------------------------------------------------------------- config_flow: ingranaggio
async def test_cambia_ip_non_valido(hass: HomeAssistant) -> None:
    voce = _voce_sala_non_caricata(hass, title="VMC Sala")
    risultato = await hass.config_entries.options.async_init(voce.entry_id)
    risultato = await hass.config_entries.options.async_configure(
        risultato["flow_id"], {"next_step_id": "cambia_ip"}
    )
    risultato = await hass.config_entries.options.async_configure(
        risultato["flow_id"], {"host": "127.0.0.1"}
    )
    assert risultato["step_id"] == "cambia_ip" and risultato["errors"] == {"host": "ip_non_valido"}
    assert voce.data["host"] == "192.168.1.161"


async def test_elimina_dalla_rete_con_la_voce_gia_eliminata(hass: HomeAssistant) -> None:
    """La barra segue il motore (sempre tra 0 e 100 %). Voce eliminata dal menu ⋮ mentre la
    VMC passa in Access Point: alla fine non c'è più niente da eliminare."""
    voce = await _voce_sala(hass)
    risultato = await _apri_elimina(hass, voce)
    avanzamenti: list[float] = []
    hass.bus.async_listen(
        EVENT_DATA_ENTRY_FLOW_PROGRESS_UPDATE, lambda evento: avanzamenti.append(evento.data["progress"])
    )
    via = threading.Event()

    def access_point(_config_dir, _ip, avanzamento):
        avanzamento(150)
        via.wait(5)
        return "VMC Sala"

    # funzione vera, non un Mock: gira in un thread come il motore
    with (
        patch(f"{PI}.rimanda_in_access_point", new=access_point),
        patch.object(hass.config_entries, "async_remove", wraps=hass.config_entries.async_remove) as rimuovi,
    ):
        risultato = await hass.config_entries.options.async_configure(
            risultato["flow_id"], {"next_step_id": "elimina_dalla_rete"}
        )
        assert risultato["type"] is FlowResultType.SHOW_PROGRESS
        assert await hass.config_entries.async_remove(voce.entry_id)
        via.set()
        await hass.async_block_till_done(wait_background_tasks=True)
    assert avanzamenti == [1.0]
    assert hass.config_entries.async_get_entry(voce.entry_id) is None
    assert rimuovi.call_count == 1  # solo quella del menu ⋮


async def test_access_point_non_riuscito_con_la_finestra_chiusa_in_inglese(hass: HomeAssistant) -> None:
    hass.config.language = "en"
    voce = await _voce_sala(hass)
    risultato = await _apri_elimina(hass, voce)
    via = threading.Event()

    def access_point(*_args, **_kwargs):
        via.wait(5)
        raise Failure("vmc_unreachable", "La VMC non risponde.")

    with patch(f"{PI}.rimanda_in_access_point", new=access_point):
        risultato = await hass.config_entries.options.async_configure(
            risultato["flow_id"], {"next_step_id": "elimina_dalla_rete"}
        )
        assert risultato["type"] is FlowResultType.SHOW_PROGRESS
        hass.config_entries.options.async_abort(risultato["flow_id"])  # finestra chiusa
        via.set()
        await hass.async_block_till_done(wait_background_tasks=True)
    assert hass.config_entries.async_get_entry(voce.entry_id) is not None
    notifica = _notifiche(hass)[f"{DOMAIN}_access_point_{voce.entry_id}"]
    assert notifica["title"] == "VMC Master: Access Point failed"
    assert "VMC Sala has not been deleted" in notifica["message"]
    assert "La VMC non risponde." not in notifica["message"]  # testo inglese delle traduzioni
