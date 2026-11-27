"""La cartella interna del collegamento di una VMC al Wi-Fi (Home Assistant vero).

La versione nativa tiene i file del motore della Finestra Prima Installazione VMC
(identity.json, restore.json, ...) nell'area dei dati di Home Assistant
(/config/.storage/vmc_master_installa_vmc). La cartella della 8.6.0 e della beta
(/config/.vmc_master_installa_vmc) non si scrive più: si legge una volta sola, per
completare un ripristino del Wi-Fi del server lasciato a metà (Home Assistant riavviato
durante il collegamento di una VMC)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import ClassVar
from unittest.mock import patch

from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component

from custom_components.vmc_master import prima_installazione as pi
from custom_components.vmc_master.const import DOMAIN

from .banco import istanza_nuova

RIPRISTINO = {
    "interface": "wlan0",
    "payload": {"enabled": True, "wifi": {"ssid": "Casa", "auth": "open"}},
    "connected": False,
    "ssid": "Casa",
}


class SupervisorFinto:
    """Il Supervisor di Home Assistant OS: registra le reti impostate."""

    impostate: ClassVar[list[tuple[str, dict]]] = []

    def info(self) -> dict:
        return {"interfaces": []}

    def update(self, interface: str, payload: dict) -> dict:
        self.impostate.append((interface, payload))
        return {}


def _fotografia(cartella: Path) -> dict[str, tuple[bytes, int]]:
    """Nome, contenuto e ora di modifica di ogni file della cartella."""
    return {
        str(f.relative_to(cartella)): (f.read_bytes(), f.stat().st_mtime_ns)
        for f in sorted(cartella.rglob("*"))
        if f.is_file()
    } | {"": (b"", cartella.stat().st_mtime_ns)}


async def test_ripristino_della_beta_preso_una_volta(
    hass: HomeAssistant, tmp_path: Path
) -> None:
    config_dir = str(tmp_path)
    della_beta = tmp_path / ".vmc_master_installa_vmc"
    della_beta.mkdir(mode=0o700)
    (della_beta / "restore.json").write_text(json.dumps(RIPRISTINO))
    (della_beta / "identity.json").write_text(json.dumps({"ip": "192.168.1.50"}))
    (della_beta / "worker.py").write_text("# il programma della 8.6.0\n")
    prima = _fotografia(della_beta)
    cartella = Path(hass.config.path(".storage", "vmc_master_installa_vmc"))
    assert pi.cartella(config_dir) == cartella

    # all'avvio: il ripristino della beta si completa dalla cartella del motore
    SupervisorFinto.impostate = []
    with patch.object(pi.motore, "Supervisor", SupervisorFinto):
        assert await async_setup_component(hass, DOMAIN, {})
        await hass.async_block_till_done()
    assert SupervisorFinto.impostate == [("wlan0", RIPRISTINO["payload"])]
    assert not (cartella / "restore.json").exists()  # completato
    assert (cartella / pi.RIPRISTINO_DELLA_BETA_PRESO).exists()
    assert json.loads((cartella / "status.json").read_text())["success"] is True
    assert _fotografia(della_beta) == prima  # mai scritta

    # al riavvio dopo: il restore.json della beta rimasto non si riprende
    await hass.async_stop()
    async with istanza_nuova(config_dir) as dopo:
        with patch.object(pi.motore, "Supervisor", SupervisorFinto):
            assert await async_setup_component(dopo, DOMAIN, {})
            await dopo.async_block_till_done()
    assert len(SupervisorFinto.impostate) == 1
    assert _fotografia(della_beta) == prima


async def test_ripristino_del_motore_prima_di_quello_della_beta(
    hass: HomeAssistant, tmp_path: Path
) -> None:
    """Un ripristino già nella cartella del motore vale più di quello della beta (che
    è più vecchio): si completa quello."""
    config_dir = str(tmp_path)
    della_beta = tmp_path / ".vmc_master_installa_vmc"
    della_beta.mkdir()
    (della_beta / "restore.json").write_text(json.dumps(RIPRISTINO))
    prima = _fotografia(della_beta)
    cartella = pi.cartella(config_dir)
    cartella.mkdir(parents=True)
    del_motore = {**RIPRISTINO, "interface": "wlan1"}
    (cartella / "restore.json").write_text(json.dumps(del_motore))

    SupervisorFinto.impostate = []
    with patch.object(pi.motore, "Supervisor", SupervisorFinto):
        assert await async_setup_component(hass, DOMAIN, {})
        await hass.async_block_till_done()
    assert SupervisorFinto.impostate == [("wlan1", RIPRISTINO["payload"])]
    assert (cartella / pi.RIPRISTINO_DELLA_BETA_PRESO).exists()
    assert _fotografia(della_beta) == prima


async def test_senza_la_cartella_della_beta(
    hass: HomeAssistant, tmp_path: Path
) -> None:
    """Nessun ripristino in sospeso: all'avvio non si crea nessuna cartella."""
    SupervisorFinto.impostate = []
    with patch.object(pi.motore, "Supervisor", SupervisorFinto):
        assert await async_setup_component(hass, DOMAIN, {})
        await hass.async_block_till_done()
    assert SupervisorFinto.impostate == []
    assert not pi.cartella(str(tmp_path)).exists()
    assert not (tmp_path / ".vmc_master_installa_vmc").exists()


def test_ripristino_della_beta_non_copiato(tmp_path: Path, caplog) -> None:
    """La cartella del motore non si crea (un file al suo posto): il ripristino della
    beta resta da prendere, lo dice il log, e la cartella della beta resta com'è."""
    config_dir = str(tmp_path)
    della_beta = tmp_path / ".vmc_master_installa_vmc"
    della_beta.mkdir()
    (della_beta / "restore.json").write_text(json.dumps(RIPRISTINO))
    prima = _fotografia(della_beta)
    pi.cartella(config_dir).parent.mkdir()
    pi.cartella(config_dir).write_text("")
    assert pi.ripristino_in_sospeso(config_dir) is False
    assert "Ripristino del Wi-Fi del server della beta" in caplog.text
    assert _fotografia(della_beta) == prima
