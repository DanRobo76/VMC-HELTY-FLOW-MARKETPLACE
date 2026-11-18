"""b24: dopo un aggiornamento basta UN riavvio, anche quando la nuova versione cambia parti
del package che non si ricaricano (shell_command, sensori TCP).

Scenario reale (18-11-2026): aggiornamento con shell_command cambiati, riavvio, e Home
Assistant chiede un secondo riavvio perche' legge i package prima che l'integrazione li
aggiorni. Ora, quando Home Assistant si ferma con la versione nuova gia' su disco, i
package si scrivono subito con la versione nuova (processo separato, prepara.py)."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

import custom_components.vmc_master as integrazione
from custom_components.vmc_master import prepara
from custom_components.vmc_master.const import DOMAIN
from custom_components.vmc_master.installatore import (
    FILE_MARCATORE,
    cartella_vmc,
    genera_file,
    installa,
)

IP = "192.168.1.160"
CARTELLA = Path(integrazione.__file__).parent
VERSIONE = json.loads((CARTELLA / "manifest.json").read_text(encoding="utf-8"))["version"]
VECCHIA = "9.0.0b1"


def _md5(testo: str) -> str:
    return hashlib.md5(testo.encode("utf-8")).hexdigest()


def _come_versione_vecchia(config_dir: str, nome: str = "master") -> None:
    """Package come l'avrebbe scritto una versione precedente con uno shell_command diverso
    (marcatore coerente: per l'integrazione i file sono suoi, non modificati a mano)."""
    cartella = cartella_vmc(config_dir, nome)
    file_yaml = cartella / f"vmc_{nome}.yaml"
    testo = file_yaml.read_bytes().decode("utf-8")
    vecchio = testo.replace("nc -w 3 ", "nc -w 5 ")
    assert vecchio != testo
    file_yaml.write_bytes(vecchio.encode("utf-8"))
    marcatore = json.loads((cartella / FILE_MARCATORE).read_text(encoding="utf-8"))
    marcatore["versione"] = VECCHIA
    marcatore["md5"][file_yaml.name] = _md5(vecchio)
    (cartella / FILE_MARCATORE).write_text(json.dumps(marcatore), encoding="utf-8")


def test_senza_preparazione_l_aggiornamento_chiede_un_secondo_riavvio(tmp_path):
    installa(str(tmp_path), "master", IP, VERSIONE)
    _come_versione_vecchia(str(tmp_path))
    assert installa(str(tmp_path), "master", IP, VERSIONE).riavvio_necessario


def test_preparati_alla_fermata_all_avvio_niente_secondo_riavvio(tmp_path):
    installa(str(tmp_path), "master", IP, VERSIONE)
    _come_versione_vecchia(str(tmp_path))
    assert prepara.prepara(str(tmp_path), [["master", IP]], VERSIONE) == ["master"]
    esito = installa(str(tmp_path), "master", IP, VERSIONE)
    assert not esito.riavvio_necessario
    assert esito.file_scritti == []


def test_non_si_prepara_se_c_e_qualcosa_da_segnalare(tmp_path):
    config = str(tmp_path)
    # nessuna installazione dell'integrazione
    assert prepara.prepara(config, [["master", IP]], VERSIONE) == []
    installa(config, "master", IP, VERSIONE)
    # stessa versione
    assert prepara.prepara(config, [["master", IP]], VERSIONE) == []
    _come_versione_vecchia(config)
    # IP diverso (cambiato dalla scheda, va gestito all'avvio)
    assert prepara.prepara(config, [["master", "192.168.1.161"]], VERSIONE) == []
    # file modificato a mano: va segnalato all'avvio
    file_yaml = cartella_vmc(config, "master") / "vmc_master.yaml"
    file_yaml.write_bytes(file_yaml.read_bytes() + b"# a mano\r\n")
    assert prepara.prepara(config, [["master", IP]], VERSIONE) == []


def test_programma_del_processo_separato_usa_la_versione_su_disco(tmp_path):
    installa(str(tmp_path), "master", IP, VERSIONE)
    _come_versione_vecchia(str(tmp_path))
    uscita = subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            integrazione._PROGRAMMA_PREPARA,
            str(CARTELLA),
            str(tmp_path),
            json.dumps([["master", IP]]),
        ],
        capture_output=True,
        text=True,
        timeout=60,
        check=True,
    )
    assert json.loads(uscita.stdout) == ["master"]
    assert (cartella_vmc(str(tmp_path), "master") / "vmc_master.yaml").read_bytes().decode(
        "utf-8"
    ) == genera_file("master", IP, VERSIONE)["vmc_master.yaml"]


async def test_fermata_con_versione_nuova_su_disco(hass: HomeAssistant):
    voce = MockConfigEntry(domain=DOMAIN, unique_id="master", data={"nome": "master", "host": IP})
    voce.add_to_hass(hass)
    assert await hass.config_entries.async_setup(voce.entry_id)
    await hass.async_block_till_done()
    await hass.async_add_executor_job(_come_versione_vecchia, hass.config.config_dir)
    # la versione in esecuzione e' la vecchia, su disco c'e' quella del manifest
    await integrazione._prepara_aggiornamento(hass, VECCHIA)
    esito = await hass.async_add_executor_job(
        installa, hass.config.config_dir, "master", IP, VERSIONE
    )
    assert not esito.riavvio_necessario
    assert esito.file_scritti == []


async def test_fermata_senza_aggiornamento_non_avvia_nulla(hass: HomeAssistant):
    with patch.object(integrazione.asyncio, "create_subprocess_exec") as avvio:
        await integrazione._prepara_aggiornamento(hass, VERSIONE)
    avvio.assert_not_called()
