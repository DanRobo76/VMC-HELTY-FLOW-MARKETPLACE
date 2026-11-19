"""Prove della 9.0.0b22 (audit tecnico del 18-11-2026): M-1, B-1..B-6, B-9 e il messaggio
finale dopo l'aggiunta di una VMC."""

from __future__ import annotations

import errno
import hashlib
import json
import logging
import os
import stat
import time
from pathlib import Path
from unittest.mock import patch

import pytest
from homeassistant.config_entries import ConfigEntryDisabler, ConfigEntryState
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.helpers import issue_registry as ir
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.vmc_master import installatore
from custom_components.vmc_master.config_flow import async_nome_vmc as _NOME_VERO
from custom_components.vmc_master.config_flow import ip_valido
from custom_components.vmc_master.const import DOMAIN
from custom_components.vmc_master.installatore import (
    FILE_MARCATORE,
    _scrivi,
    _solo_esclusioni_cambiate,
    cartella_vmc,
    installa,
    installazione_manuale,
    leggi_marcatore,
)

NOME_VMC = "custom_components.vmc_master.config_flow.async_nome_vmc"
PI = "custom_components.vmc_master.prima_installazione"
CARTELLA = Path(__file__).parent.parent / "custom_components" / "vmc_master"
# Controllo della configurazione fatto dalla riparazione «Riavviare» prima del riavvio
CONTROLLO_CONFIG = "homeassistant.config.async_check_ha_config_file"


@pytest.fixture(autouse=True)
def _nessuna_vmc_in_rete():
    with patch(NOME_VMC, return_value=None):
        yield


def _togli_filtri_tcp() -> None:
    logger = logging.getLogger("homeassistant.components.tcp.entity")
    for filtro in [f for f in logger.filters if type(f).__name__ == "_FiltroTcpVmc"]:
        logger.removeFilter(filtro)


@pytest.fixture(autouse=True)
def _senza_filtri_tcp_rimasti():
    """Il logger e' globale: un filtro di un altro test (hass chiuso senza scaricare le
    voci) non deve contare qui."""
    _togli_filtri_tcp()
    yield
    _togli_filtri_tcp()


def _impronte(cartella: Path) -> dict[str, str]:
    return {
        f.name: hashlib.md5(f.read_bytes()).hexdigest()
        for f in sorted(cartella.iterdir())
        if f.is_file()
    }


def _disco_pieno(*_args, **_kwargs):
    raise OSError(errno.ENOSPC, "No space left on device")


# ---- M-1: scritture atomiche ---------------------------------------------------------


def test_scrivi_mantiene_crlf_e_lf(tmp_path: Path) -> None:
    file = tmp_path / "prova.yaml"
    _scrivi(file, "a\r\nb\nc\r\n")
    assert file.read_bytes() == b"a\r\nb\nc\r\n"
    assert [f.name for f in tmp_path.iterdir()] == ["prova.yaml"]


@pytest.mark.parametrize("dove", ["fsync", "replace"])
def test_scrittura_interrotta_lascia_il_file_di_prima(tmp_path: Path, dove: str) -> None:
    """Disco pieno durante la scrittura: il file di prima resta intero, nessun temporaneo."""
    file = tmp_path / "prova.yaml"
    file.write_bytes(b"vecchio: 1\r\naltro: 2\r\n")
    with patch.object(installatore.os, dove, side_effect=_disco_pieno), pytest.raises(OSError):
        _scrivi(file, "nuovo: 1\r\n" * 1000)
    assert file.read_bytes() == b"vecchio: 1\r\naltro: 2\r\n"
    assert [f.name for f in tmp_path.iterdir()] == ["prova.yaml"]


def test_scrittura_a_meta_lascia_il_file_di_prima(tmp_path: Path) -> None:
    """Il testo si interrompe a meta' (scrittura parziale e poi errore): il file
    definitivo non viene toccato."""
    file = tmp_path / "prova.yaml"
    file.write_bytes(b"vecchio: 1\n")
    apri = open

    class FileAMeta:
        def __init__(self, *args, **kwargs):
            self._file = apri(*args, **kwargs)

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self._file.close()

        def write(self, testo):
            self._file.write(testo[: len(testo) // 2])
            raise OSError(errno.ENOSPC, "No space left on device")

    with patch("builtins.open", FileAMeta), pytest.raises(OSError):
        _scrivi(file, "nuovo: 1\n" * 1000)
    assert file.read_bytes() == b"vecchio: 1\n"
    assert [f.name for f in tmp_path.iterdir()] == ["prova.yaml"]


def test_permessi_dei_file(tmp_path: Path) -> None:
    """Gli script .sh si scrivono gia' eseguibili; un file riscritto tiene i suoi permessi."""
    installa(str(tmp_path), "master", "192.168.1.160", "9.0.0b22")
    cartella = cartella_vmc(str(tmp_path), "master")
    script = cartella / "vmc_master_script_cambio_nome.sh"
    assert stat.S_IMODE(script.stat().st_mode) == 0o755
    _scrivi(script, script.read_text(encoding="utf-8", newline="") + "\n")
    assert stat.S_IMODE(script.stat().st_mode) == 0o755


def test_aggiornamento_interrotto_non_lascia_file_troncati(tmp_path: Path) -> None:
    """Disco pieno durante un aggiornamento: i file restano quelli di prima e il giro dopo
    li aggiorna senza «modificati a mano» e senza backup."""
    config_dir = str(tmp_path)
    installa(config_dir, "master", "192.168.1.160", "9.0.0b21")
    cartella = cartella_vmc(config_dir, "master")
    prima = _impronte(cartella)
    with patch.object(installatore.os, "replace", side_effect=_disco_pieno), pytest.raises(OSError):
        installa(config_dir, "master", "192.168.1.160", "9.0.0b22")
    assert _impronte(cartella) == prima
    esito = installa(config_dir, "master", "192.168.1.160", "9.0.0b22")
    assert esito.file_modificati == [] and esito.backup is None and esito.backup_modificati is None
    assert "vmc_master.yaml" in esito.file_scritti
    assert leggi_marcatore(config_dir, "master")["versione"] == "9.0.0b22"
    assert not (tmp_path / "vmc_master_backup").exists()


def test_prima_installazione_interrotta_non_e_manuale(tmp_path: Path) -> None:
    """Interruzione dopo il primo file: c'e' il marcatore provvisorio, quindi la cartella
    non sembra un'installazione manuale e il giro dopo non la sposta nel backup."""
    config_dir = str(tmp_path)
    vero_replace = os.replace
    chiamate: list[str] = []

    def replace_poi_disco_pieno(sorgente, destinazione):
        chiamate.append(Path(destinazione).name)
        if len(chiamate) > 2:  # marcatore provvisorio e primo file scritti
            _disco_pieno()
        vero_replace(sorgente, destinazione)

    with (
        patch.object(installatore.os, "replace", side_effect=replace_poi_disco_pieno),
        pytest.raises(OSError),
    ):
        installa(config_dir, "master", "192.168.1.160", "9.0.0b22")
    assert chiamate[0] == FILE_MARCATORE
    cartella = cartella_vmc(config_dir, "master")
    assert leggi_marcatore(config_dir, "master").get("in_corso") is True
    assert not installazione_manuale(config_dir, "master")
    assert not list(cartella.glob(".*.tmp"))
    esito = installa(config_dir, "master", "192.168.1.160", "9.0.0b22")
    assert esito.backup is None and esito.file_modificati == []
    marcatore = leggi_marcatore(config_dir, "master")
    assert "in_corso" not in marcatore and len(marcatore["md5"]) == 4


def test_temporanei_rimasti_tolti(tmp_path: Path) -> None:
    config_dir = str(tmp_path)
    installa(config_dir, "master", "192.168.1.160", "9.0.0b22")
    cartella = cartella_vmc(config_dir, "master")
    rimasto = cartella / ".vmc_master.yaml.0123abcd.tmp"
    rimasto.write_text("mezzo", encoding="utf-8")
    installa(config_dir, "master", "192.168.1.160", "9.0.0b22")
    assert not rimasto.exists()


def test_marcatore_riscritto_solo_se_cambia(tmp_path: Path) -> None:
    config_dir = str(tmp_path)
    installa(config_dir, "master", "192.168.1.160", "9.0.0b22")
    with patch.object(installatore, "_scrivi", wraps=installatore._scrivi) as scrivi:
        esito = installa(config_dir, "master", "192.168.1.160", "9.0.0b22")
    assert esito.file_scritti == [] and scrivi.call_count == 0


async def test_disco_pieno_all_avvio(hass: HomeAssistant) -> None:
    """Avvio con il disco pieno: la voce va in errore con un messaggio, il package resta
    quello di prima (valido) e al giro dopo non compare «modificati a mano»."""
    from homeassistant.components import persistent_notification

    config_dir = hass.config.config_dir
    await hass.async_add_executor_job(installa, config_dir, "master", "192.168.1.160", "9.0.0b20")
    cartella = cartella_vmc(config_dir, "master")
    prima = _impronte(cartella)
    voce = MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    )
    voce.add_to_hass(hass)
    with patch.object(installatore.os, "replace", side_effect=_disco_pieno):
        assert not await hass.config_entries.async_setup(voce.entry_id)
    await hass.async_block_till_done()
    assert voce.state is ConfigEntryState.SETUP_ERROR
    assert "spazio libero sul disco" in voce.reason or "free disk space" in voce.reason
    assert _impronte(cartella) == prima
    assert await hass.config_entries.async_reload(voce.entry_id)
    await hass.async_block_till_done()
    assert voce.state is ConfigEntryState.LOADED
    notifiche = persistent_notification._async_get_or_create_notifications(hass)
    assert f"{DOMAIN}_modificati_master" not in notifiche
    assert not Path(hass.config.path("vmc_master_backup")).exists()


# ---- B-1: IP dalla scheda con le voci avviate in parallelo ---------------------------


async def test_ip_della_scheda_con_avvio_in_parallelo(hass: HomeAssistant) -> None:
    """Due VMC con lo stesso IP scritto dalla scheda, avviate insieme con un I/O lento:
    lo prende una sola, l'altra resta sul suo IP e riceve la notifica."""
    from homeassistant.components import persistent_notification

    config_dir = hass.config.config_dir
    voci = {}
    for nome, ip in (("master", "192.168.1.160"), ("sala", "192.168.1.161")):
        await hass.async_add_executor_job(installa, config_dir, nome, ip, "9.0.0b21")
        file = cartella_vmc(config_dir, nome) / f"vmc_{nome}.yaml"
        file.write_bytes(file.read_bytes().replace(ip.encode(), b"192.168.1.200"))
        voci[nome] = MockConfigEntry(
            domain=DOMAIN, unique_id=nome, data={"nome": nome, "host": ip}
        )
        voci[nome].add_to_hass(hass)

    def aggiorna_lento(*_args) -> None:
        time.sleep(0.3)  # come una scheda SD lenta

    with patch(f"{PI}.aggiorna_ip", new=aggiorna_lento):
        assert await async_setup_component(hass, DOMAIN, {})
        await hass.async_block_till_done()
    ips = sorted(voce.data["host"] for voce in voci.values())
    assert ips in (["192.168.1.160", "192.168.1.200"], ["192.168.1.161", "192.168.1.200"])
    notifiche = persistent_notification._async_get_or_create_notifications(hass)
    rifiutata = next(n for n, v in voci.items() if v.data["host"] != "192.168.1.200")
    assert f"{DOMAIN}_ip_scheda_{rifiutata}" in notifiche


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


async def test_ip_riservato_dalla_scheda_rifiutato(hass: HomeAssistant) -> None:
    voce = MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    )
    voce.add_to_hass(hass)
    assert await hass.config_entries.async_setup(voce.entry_id)
    await hass.async_block_till_done()
    file = cartella_vmc(hass.config.config_dir, "master") / "vmc_master.yaml"
    file.write_bytes(file.read_bytes().replace(b"192.168.1.160", b"0.0.0.0"))
    assert await hass.config_entries.async_reload(voce.entry_id)
    await hass.async_block_till_done()
    assert voce.data["host"] == "192.168.1.160"
    assert b"0.0.0.0" not in file.read_bytes()


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


async def test_voce_disabilitata(hass: HomeAssistant, hass_client) -> None:
    """Voce disabilitata: la scheda non si serve piu' (409) e un avviso dice che il package
    resta attivo; riabilitata, la scheda torna e l'avviso sparisce."""
    assert await async_setup_component(hass, "http", {})
    voce = MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    )
    voce.add_to_hass(hass)
    assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()
    client = await hass_client()
    assert (await client.get(f"/api/vmc_master/scheda/{voce.entry_id}")).status == 200
    assert await hass.config_entries.async_set_disabled_by(voce.entry_id, ConfigEntryDisabler.USER)
    await hass.async_block_till_done()
    assert (await client.get(f"/api/vmc_master/scheda/{voce.entry_id}")).status == 409
    avviso = ir.async_get(hass).async_get_issue(DOMAIN, "voce_disabilitata_master")
    assert avviso is not None and avviso.translation_key == "voce_disabilitata"
    assert await hass.config_entries.async_set_disabled_by(voce.entry_id, None)
    await hass.async_block_till_done()
    assert (await client.get(f"/api/vmc_master/scheda/{voce.entry_id}")).status == 200
    assert ir.async_get(hass).async_get_issue(DOMAIN, "voce_disabilitata_master") is None
    for lingua in ("it", "en"):
        dati = json.loads((CARTELLA / "translations" / f"{lingua}.json").read_text(encoding="utf-8"))
        assert set(dati["issues"]["voce_disabilitata"]) == {"title", "description"}


# ---- recorder: solo l'elenco delle escluse ---------------------------------------------


def test_solo_esclusioni_cambiate() -> None:
    base = {"purge_keep_days": 5, "exclude": {"domains": ["x"], "entities": ["a.b"]}}
    assert _solo_esclusioni_cambiate(base, {**base, "exclude": {"domains": ["x"], "entities": ["a.b", "c.d"]}})
    assert _solo_esclusioni_cambiate(base, {**base, "exclude": {"domains": ["x"]}})
    assert not _solo_esclusioni_cambiate(base, {**base, "exclude": {"domains": ["y"], "entities": ["a.b"]}})
    assert not _solo_esclusioni_cambiate(base, {**base, "purge_keep_days": 3})
    assert not _solo_esclusioni_cambiate(base, {**base, "exclude": {"entities": "a.b"}})
    assert not _solo_esclusioni_cambiate(base, {"purge_keep_days": 5})
    assert not _solo_esclusioni_cambiate(None, base)


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


async def test_prima_vmc_dice_come_riavviare(hass: HomeAssistant) -> None:
    """Prima VMC (package nuovo): il messaggio finale dice i tre passi del riavvio."""
    risultato = await _aggiungi_in_rete(hass, "192.168.1.160", "VMC Giorno")
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    assert risultato["description"] == "riavvio"
    assert risultato["description_placeholders"] == {"titolo": risultato["title"]}
    assert ir.async_get(hass).async_get_issue(DOMAIN, "riavvio_necessario") is not None
    for lingua, passi in (
        ("it", ["1. aprire Impostazioni;", "2. premere «VMC Master: riavviare Home Assistant»;", "3. premere Invia."]),
        ("en", ["1. open Settings;", "2. press «VMC Master: restart Home Assistant»;", "3. press Submit."]),
    ):
        dati = json.loads((CARTELLA / "translations" / f"{lingua}.json").read_text(encoding="utf-8"))
        testo = dati["config"]["create_entry"]["riavvio"]
        assert testo.splitlines()[-3:] == passi
        # il titolo dell'avviso citato e' quello vero
        assert dati["issues"]["riavvio_necessario"]["title"] in testo


async def test_senza_riavvio_messaggio_normale(hass: HomeAssistant) -> None:
    """Package gia' scritto dall'integrazione e nessun riavvio chiesto: messaggio normale."""
    await hass.async_add_executor_job(
        installa, hass.config.config_dir, "master", "192.168.1.160", "9.0.0b22"
    )
    assert ir.async_get(hass).async_get_issue(DOMAIN, "riavvio_necessario") is None
    risultato = await _aggiungi_in_rete(hass, "192.168.1.160", "VMC Giorno")
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    assert risultato.get("description") is None


# ---- B-9: errori dei sensori TCP con la VMC spenta ----------------------------------


def _record(ip: str, porta: int = 5001) -> logging.LogRecord:
    return logging.LogRecord(
        "homeassistant.components.tcp.entity", logging.ERROR, __file__, 1,
        "Unable to connect to %s on port %s: %s", (ip, porta, "[Errno 113] No route to host"), None,
    )


def test_filtro_tcp_un_messaggio_ogni_30_minuti() -> None:
    from custom_components.vmc_master import _FiltroTcpVmc

    filtro = _FiltroTcpVmc()
    filtro.ips = frozenset({"192.168.1.160", "192.168.1.161"})
    ora = [1000.0]
    filtro._ora = lambda: ora[0]
    assert filtro.filter(_record("192.168.1.160"))
    assert not filtro.filter(_record("192.168.1.160"))
    assert filtro.filter(_record("192.168.1.161"))  # un'altra VMC: conto suo
    # altri dispositivi (anche con un IP che contiene quello della VMC): passano sempre
    for _volta in range(3):
        assert filtro.filter(_record("192.168.1.16"))
        assert filtro.filter(_record("192.168.1.1600"))
        assert filtro.filter(_record("10.0.0.5"))
    ora[0] += 30 * 60 - 1
    assert not filtro.filter(_record("192.168.1.160"))
    ora[0] += 1
    assert filtro.filter(_record("192.168.1.160"))
    assert not filtro.filter(_record("192.168.1.160"))


async def test_filtro_tcp_installato_e_tolto(hass: HomeAssistant, caplog) -> None:
    """Installato con la prima VMC, IP aggiornati quando cambiano, tolto con l'ultima."""
    logger = logging.getLogger("homeassistant.components.tcp.entity")
    voce = MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    )
    voce.add_to_hass(hass)
    assert await hass.config_entries.async_setup(voce.entry_id)
    await hass.async_block_till_done()
    filtri = [f for f in logger.filters if type(f).__name__ == "_FiltroTcpVmc"]
    assert filtri == [hass.data["vmc_master_filtro_tcp"]]
    assert len(filtri) == 1 and filtri[0].ips == {"192.168.1.160"}
    with caplog.at_level(logging.ERROR, logger="homeassistant.components.tcp.entity"):
        for _volta in range(5):
            logger.error("Unable to connect to %s on port %s: %s", "192.168.1.160", 5001, "timeout")
            logger.error("Unable to connect to %s on port %s: %s", "192.168.1.50", 8080, "timeout")
    messaggi = [r.getMessage() for r in caplog.records if r.name == logger.name]
    assert sum("192.168.1.160" in m for m in messaggi) == 1
    assert sum("192.168.1.50" in m for m in messaggi) == 5
    # IP cambiato (la voce si ricarica): il filtro conosce il nuovo
    hass.config_entries.async_update_entry(voce, data={**voce.data, "host": "192.168.1.170"})
    await hass.async_block_till_done()

    def _filtri() -> list:
        return [f for f in logger.filters if type(f).__name__ == "_FiltroTcpVmc"]

    assert _filtri() == [hass.data["vmc_master_filtro_tcp"]]
    assert _filtri()[0].ips == {"192.168.1.170"}
    # una seconda voce non installa un secondo filtro
    sala = MockConfigEntry(
        domain=DOMAIN, unique_id="sala", data={"nome": "sala", "host": "192.168.1.161"}
    )
    sala.add_to_hass(hass)
    assert await hass.config_entries.async_setup(sala.entry_id)
    await hass.async_block_till_done()
    assert len(_filtri()) == 1
    assert _filtri()[0].ips == {"192.168.1.170", "192.168.1.161"}
    assert await hass.config_entries.async_unload(sala.entry_id)
    assert len(_filtri()) == 1
    assert await hass.config_entries.async_unload(voce.entry_id)
    assert _filtri() == []
    assert "vmc_master_filtro_tcp" not in hass.data


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
