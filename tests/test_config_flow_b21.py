"""Prove delle correzioni 9.0.0b21 della configurazione da interfaccia."""

from __future__ import annotations

import json
import threading
from pathlib import Path
from unittest.mock import patch

import pytest
from homeassistant import config_entries
from homeassistant.components import persistent_notification
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.vmc_master.const import DOMAIN

PROVA_VMC = "custom_components.vmc_master.config_flow.async_prova_vmc"
NOME_VMC = "custom_components.vmc_master.config_flow.async_nome_vmc"
PI = "custom_components.vmc_master.prima_installazione"
CARTELLA = Path(__file__).parent.parent / "custom_components" / "vmc_master"


@pytest.fixture(autouse=True)
def _nessuna_vmc_in_rete():
    """Nessuna VMC vera: i test che leggono il nome lo impostano da se'."""
    with patch(NOME_VMC, return_value=None):
        yield


async def _voce(hass: HomeAssistant) -> MockConfigEntry:
    voce = MockConfigEntry(
        domain=DOMAIN, unique_id="zona", title="VMC Zona Giorno",
        data={"nome": "zona", "host": "192.168.1.161", "titolo": "VMC Zona Giorno"},
    )
    voce.add_to_hass(hass)
    assert await hass.config_entries.async_setup(voce.entry_id)
    await hass.async_block_till_done()
    return voce


async def _apri_cambia_ip(hass: HomeAssistant, voce: MockConfigEntry):
    risultato = await hass.config_entries.options.async_init(voce.entry_id)
    risultato = await hass.config_entries.options.async_configure(
        risultato["flow_id"], {"next_step_id": "cambia_ip"}
    )
    assert risultato["step_id"] == "cambia_ip"
    return risultato


async def test_cambia_ip_rifiuta_un_dispositivo_senza_nome(hass: HomeAssistant) -> None:
    """Risponde sulla 5001 ma senza «VMNM»: non e' una VMC, neanche al secondo Invia."""
    voce = await _voce(hass)
    risultato = await _apri_cambia_ip(hass, voce)
    for _volta in range(2):
        with patch(NOME_VMC, return_value=""):
            risultato = await hass.config_entries.options.async_configure(
                risultato["flow_id"], {"host": "192.168.1.170"}
            )
        assert risultato["type"] is FlowResultType.FORM
        assert risultato["errors"] == {"host": "ip_altro_dispositivo"}
    assert voce.data["host"] == "192.168.1.161"


async def test_cambia_ip_con_un_altro_nome(hass: HomeAssistant) -> None:
    """Risponde una VMC con un altro nome: avviso; un secondo Invia salva lo stesso."""
    voce = await _voce(hass)
    risultato = await _apri_cambia_ip(hass, voce)
    with patch(NOME_VMC, return_value="VMC Zona Notte"):
        risultato = await hass.config_entries.options.async_configure(
            risultato["flow_id"], {"host": "192.168.1.170"}
        )
    assert risultato["errors"] == {"host": "ip_nome_diverso"}
    assert risultato["description_placeholders"] == {
        "titolo": "VMC Zona Giorno", "nome_letto": "VMC Zona Notte"
    }
    with patch(NOME_VMC, return_value="VMC Zona Notte") as nome:
        risultato = await hass.config_entries.options.async_configure(
            risultato["flow_id"], {"host": "192.168.1.170"}
        )
    nome.assert_not_called()
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    assert voce.data["host"] == "192.168.1.170"


async def test_cambia_ip_stessa_vmc(hass: HomeAssistant) -> None:
    """Stesso nome (maiuscole e separatori a parte): si salva subito."""
    voce = await _voce(hass)
    risultato = await _apri_cambia_ip(hass, voce)
    with patch(NOME_VMC, return_value="vmc_zona-giorno"):
        risultato = await hass.config_entries.options.async_configure(
            risultato["flow_id"], {"host": "192.168.1.170"}
        )
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    assert voce.data["host"] == "192.168.1.170"


async def test_nome_vuoto_chiede_il_nome(hass: HomeAssistant) -> None:
    """VMC che risponde senza nome leggibile: finestra «nome_manuale», mai «Nome letto: -»."""
    MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    ).add_to_hass(hass)
    risultato = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    risultato = await hass.config_entries.flow.async_configure(
        risultato["flow_id"], {"next_step_id": "in_rete"}
    )
    with patch(NOME_VMC, return_value=""):
        risultato = await hass.config_entries.flow.async_configure(
            risultato["flow_id"], {"host": "192.168.1.162"}
        )
    assert risultato["step_id"] == "nome_manuale" and risultato["errors"] == {}
    risultato = await hass.config_entries.flow.async_configure(
        risultato["flow_id"], {"nome": "studio"}
    )
    # senza nome non si sa se e' una VMC: si chiede conferma come per una VMC spenta
    assert risultato["step_id"] == "non_raggiungibile"
    risultato = await hass.config_entries.flow.async_configure(risultato["flow_id"], {})
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    assert risultato["title"] == "VMC studio"


async def test_prova_vmc_senza_nome() -> None:
    from custom_components.vmc_master import config_flow

    with patch(NOME_VMC, return_value=""):
        assert await config_flow.async_prova_vmc("192.168.1.170") is False
    with patch(NOME_VMC, return_value="VMC Zona"):
        assert await config_flow.async_prova_vmc("192.168.1.170") is True


def test_titolo_voce_con_separatori() -> None:
    from custom_components.vmc_master.config_flow import titolo_voce

    assert titolo_voce("VMC_Studio", "studio") == "VMC_Studio"
    assert titolo_voce("vmc-studio", "studio") == "vmc-studio"
    assert titolo_voce("Studio_Nord", "studio") == "VMC Studio_Nord"
    assert titolo_voce("  ", "studio") == "VMC studio"
    assert titolo_voce("_", "studio") == "VMC studio"


async def test_access_point_non_riuscito_con_la_finestra_chiusa(hass: HomeAssistant) -> None:
    """Finestra chiusa e Access Point non riuscito: la voce resta e arriva una notifica."""
    from custom_components.vmc_master.prima_installazione import Failure

    hass.config.language = "it"
    voce = await _voce(hass)
    risultato = await hass.config_entries.options.async_init(voce.entry_id)
    risultato = await hass.config_entries.options.async_configure(
        risultato["flow_id"], {"next_step_id": "elimina"}
    )
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
    notifiche = persistent_notification._async_get_or_create_notifications(hass)
    notifica = notifiche[f"{DOMAIN}_access_point_{voce.entry_id}"]
    assert notifica["title"] == "VMC Master: Access Point non riuscito"
    assert "La VMC non risponde." in notifica["message"]
    assert "VMC Zona Giorno non è stata eliminata" in notifica["message"]


async def test_access_point_non_riuscito_con_la_finestra_aperta(hass: HomeAssistant) -> None:
    """Finestra aperta: l'errore lo mostra la finestra, nessuna notifica."""
    from custom_components.vmc_master.prima_installazione import Failure

    voce = await _voce(hass)
    risultato = await hass.config_entries.options.async_init(voce.entry_id)
    risultato = await hass.config_entries.options.async_configure(
        risultato["flow_id"], {"next_step_id": "elimina"}
    )
    with patch(
        f"{PI}.rimanda_in_access_point", side_effect=Failure("vmc_unreachable", "No.")
    ):
        risultato = await hass.config_entries.options.async_configure(
            risultato["flow_id"], {"next_step_id": "elimina_dalla_rete"}
        )
        while risultato["type"] is FlowResultType.SHOW_PROGRESS:
            await hass.async_block_till_done()
            risultato = await hass.config_entries.options.async_configure(risultato["flow_id"])
    assert risultato["step_id"] == "errore_rete"
    notifiche = persistent_notification._async_get_or_create_notifications(hass)
    assert f"{DOMAIN}_access_point_{voce.entry_id}" not in notifiche


def test_traduzioni() -> None:
    """strings.json uguale a en.json; stesse chiavi in italiano; abort tradotti."""
    strings = (CARTELLA / "strings.json").read_text(encoding="utf-8")
    assert strings == (CARTELLA / "translations" / "en.json").read_text(encoding="utf-8")

    def chiavi(dati: dict, prefisso: str = "") -> set[str]:
        risultato: set[str] = set()
        for chiave, valore in dati.items():
            if isinstance(valore, dict):
                risultato |= chiavi(valore, f"{prefisso}{chiave}.")
            else:
                risultato.add(f"{prefisso}{chiave}")
        return risultato

    lingue = {
        lingua: json.loads((CARTELLA / "translations" / f"{lingua}.json").read_text(encoding="utf-8"))
        for lingua in ("it", "en")
    }
    assert chiavi(lingue["it"]) == chiavi(lingue["en"])
    for dati in lingue.values():
        assert dati["config"]["abort"]["already_in_progress"]
        assert "ip_altro_dispositivo" in dati["options"]["error"]
        assert "ip_nome_diverso" in dati["options"]["error"]
    it = lingue["it"]
    assert "zeri iniziali" in it["config"]["error"]["ip_non_valido"]
    assert "zeri iniziali" in it["options"]["error"]["ip_non_valido"]
    assert "VMC_…." not in json.dumps(it, ensure_ascii=False)
    assert it["options"]["step"]["elimina"]["description"].count("Aggiungi dispositivo") == 1
    assert "vuoi" not in json.dumps(it["options"], ensure_ascii=False).lower()
    assert "riavvia Home" not in json.dumps(it["options"], ensure_ascii=False)


async def test_errori_del_motore_in_inglese(hass: HomeAssistant) -> None:
    """Fuori dall'italiano il messaggio del motore si sostituisce col testo per codice."""
    from custom_components.vmc_master.config_flow import async_messaggio_errore
    from custom_components.vmc_master.prima_installazione import LED_HINT, Failure

    errore = Failure("vmc_unreachable", "La VMC non risponde all'indirizzo 192.168.1.161.")
    hass.config.language = "en"
    assert await async_messaggio_errore(hass, errore) == (
        "The unit does not answer. Check that it is on, the IP and the reservation on the router."
    )
    # codice sconosciuto: resta il messaggio del motore, senza il rimando alla tabella
    sconosciuto = Failure("codice_nuovo", "Messaggio del motore." + LED_HINT)
    assert await async_messaggio_errore(hass, sconosciuto) == "Messaggio del motore."
    hass.config.language = "it"
    assert await async_messaggio_errore(hass, errore) == errore.message
    tornata = Failure("back_to_access_point", "Tornata in Access Point." + LED_HINT)
    assert await async_messaggio_errore(hass, tornata) == "Tornata in Access Point."


def test_ogni_codice_del_motore_ha_un_testo() -> None:
    """Ogni codice di errore del motore (anche quelli dei campi da 32 caratteri e
    communication_error) ha un testo in «exceptions», in italiano e in inglese."""
    import re

    codici: set[str] = set()
    for nome in ("motore_installa_vmc.py", "prima_installazione.py"):
        testo = (CARTELLA / nome).read_text(encoding="utf-8")
        codici |= set(re.findall(r'Failure\(\s*"([a-z_]+)"', testo))
        codici |= set(re.findall(r'field32\([^)]*?,\s*"([a-z_]+)"', testo))
    assert "communication_error" in codici and "invalid_ssid" in codici
    for lingua in ("it", "en"):
        dati = json.loads((CARTELLA / "translations" / f"{lingua}.json").read_text(encoding="utf-8"))
        assert set(dati["exceptions"]) == codici, codici ^ set(dati["exceptions"])
        assert all(v["message"] for v in dati["exceptions"].values())
        # una azione per riga anche nel Ripristino Wi-Fi
        for passo in ("rete_vmc", "errore"):
            descrizione = dati["config"]["step"][passo]["description"]
            assert "\n4. " in descrizione
            assert ("Notturna**;" in descrizione) or ("button**;" in descrizione)
