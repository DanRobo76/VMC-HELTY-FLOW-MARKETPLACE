"""Prove della 9.0.0b29: la scheda VMC Master compare nelle plance anche se la pagina e'
stata aperta (o ricaricata) mentre Home Assistant si avviava.

La copia in www/vmc_master e' servita da /local appena parte il frontend; la risorsa delle
plance (/local/vmc_master/vmc-master-card.js?v=...) si carica all'apertura della plancia,
anche quando l'integrazione non e' ancora avviata."""

from __future__ import annotations

import logging
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
from homeassistant.components.lovelace import LOVELACE_DATA
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

import custom_components.vmc_master as vmc
from custom_components.vmc_master.const import DOMAIN

JS = vmc.FILE_SCHEDA_JS
LOCALE = vmc.URL_LOCALE_SCHEDA


def _cartella(hass: HomeAssistant) -> Path:
    return Path(hass.config.config_dir) / "www" / vmc.CARTELLA_WWW_SCHEDA


def _nostre(hass: HomeAssistant) -> list[dict]:
    return [
        voce
        for voce in hass.data[LOVELACE_DATA].resources.async_items()
        if voce["url"].split("?", 1)[0] == LOCALE
    ]


async def _lovelace(hass: HomeAssistant, modo: str = "storage") -> None:
    assert await async_setup_component(hass, "http", {})
    assert await async_setup_component(hass, "lovelace", {"lovelace": {"resource_mode": modo}})
    await hass.data[LOVELACE_DATA].resources.async_get_info()


# ------------------------------------------------------------------ copia in www
async def test_copia_in_www_solo_se_cambiata(hass: HomeAssistant) -> None:
    config_dir = hass.config.config_dir
    await hass.async_add_executor_job(vmc._copia_scheda_in_www, config_dir)
    copia = _cartella(hass) / JS
    originale = (Path(vmc.__file__).parent / "frontend" / JS).read_bytes()
    assert copia.read_bytes() == originale
    # uguale: non si riscrive
    with patch.object(Path, "replace") as sostituisci:
        await hass.async_add_executor_job(vmc._copia_scheda_in_www, config_dir)
    sostituisci.assert_not_called()
    # diversa (versione vecchia): si riscrive, senza file temporanei lasciati
    copia.write_bytes(b"vecchia")
    await hass.async_add_executor_job(vmc._copia_scheda_in_www, config_dir)
    assert copia.read_bytes() == originale
    assert sorted(p.name for p in _cartella(hass).iterdir()) == [JS]


async def test_local_servito(hass: HomeAssistant) -> None:
    assert await async_setup_component(hass, "http", {})
    assert not vmc._local_servito(hass)
    await hass.http.async_register_static_paths(
        [vmc.StaticPathConfig("/local", hass.config.config_dir, False)]
    )
    assert vmc._local_servito(hass)


# ----------------------------------------------------------- risorsa delle plance
async def test_risorsa_creata_aggiornata_doppie_tolte(hass: HomeAssistant) -> None:
    await _lovelace(hass)
    risorse = hass.data[LOVELACE_DATA].resources
    altra = await risorse.async_create_item({"res_type": "module", "url": "/local/altra.js"})
    await vmc._registra_risorsa_plancia(hass, f"{LOCALE}?v=9.0.0b29")
    assert [(v["type"], v["url"]) for v in _nostre(hass)] == [("module", f"{LOCALE}?v=9.0.0b29")]
    # stessa versione: niente da cambiare
    with patch.object(risorse, "async_update_item") as aggiorna:
        await vmc._registra_risorsa_plancia(hass, f"{LOCALE}?v=9.0.0b29")
    aggiorna.assert_not_called()
    # tipo sbagliato e una doppia: si corregge la prima, si toglie la seconda
    prima = _nostre(hass)[0]
    await risorse.async_update_item(prima["id"], {"res_type": "js"})
    await risorse.async_create_item({"res_type": "module", "url": f"{LOCALE}?v=vecchia"})
    await vmc._registra_risorsa_plancia(hass, f"{LOCALE}?v=9.0.0b30")
    assert [(v["id"], v["type"], v["url"]) for v in _nostre(hass)] == [
        (prima["id"], "module", f"{LOCALE}?v=9.0.0b30")
    ]
    # le risorse dell'utente restano
    assert any(v["id"] == altra["id"] for v in risorse.async_items())


async def test_risorsa_non_toccata_in_modo_yaml(hass: HomeAssistant) -> None:
    await _lovelace(hass, "yaml")
    risorse = hass.data[LOVELACE_DATA].resources
    await vmc._registra_risorsa_plancia(hass, f"{LOCALE}?v=9.0.0b29")
    assert risorse.async_items() == []


async def test_risorsa_senza_plance(hass: HomeAssistant) -> None:
    hass.data.pop(LOVELACE_DATA, None)
    await vmc._registra_risorsa_plancia(hass, f"{LOCALE}?v=9.0.0b29")  # nessun errore


# ------------------------------------------------------------------ _registra_scheda
async def test_registra_scheda_con_local_servito(hass: HomeAssistant) -> None:
    await _lovelace(hass)
    with (
        patch.object(vmc, "_local_servito", return_value=True),
        patch.object(vmc, "add_extra_js_url") as extra,
    ):
        await vmc._registra_scheda(hass, "9.0.0b29")
    extra.assert_called_once_with(hass, f"{LOCALE}?v=9.0.0b29")
    assert [v["url"] for v in _nostre(hass)] == [f"{LOCALE}?v=9.0.0b29"]
    assert (_cartella(hass) / JS).is_file()


async def test_registra_scheda_senza_local(hass: HomeAssistant) -> None:
    """www appena creata (al prossimo avvio /local c'e'): indirizzo dell'integrazione."""
    await _lovelace(hass)
    with (
        patch.object(vmc, "_local_servito", return_value=False),
        patch.object(vmc, "add_extra_js_url") as extra,
    ):
        await vmc._registra_scheda(hass, "9.0.0b29")
    extra.assert_called_once_with(hass, f"{vmc.URL_FRONTEND}/{JS}?v=9.0.0b29")
    assert _nostre(hass) == []
    assert (_cartella(hass) / JS).is_file()


async def test_registra_scheda_copia_non_riuscita(hass: HomeAssistant, caplog) -> None:
    with (
        patch.object(vmc, "_copia_scheda_in_www", side_effect=PermissionError("sola lettura")),
        patch.object(vmc, "add_extra_js_url") as extra,
        caplog.at_level(logging.WARNING),
    ):
        await vmc._registra_scheda(hass, "9.0.0b29")
    extra.assert_called_once_with(hass, f"{vmc.URL_FRONTEND}/{JS}?v=9.0.0b29")
    assert "Scheda VMC Master non copiata in www: sola lettura" in caplog.text


async def test_registra_scheda_risorsa_non_riuscita(hass: HomeAssistant, caplog) -> None:
    with (
        patch.object(vmc, "_local_servito", return_value=True),
        patch.object(vmc, "_registra_risorsa_plancia", AsyncMock(side_effect=ValueError("no"))),
        patch.object(vmc, "add_extra_js_url") as extra,
    ):
        await vmc._registra_scheda(hass, "9.0.0b29")
    extra.assert_called_once_with(hass, f"{LOCALE}?v=9.0.0b29")
    assert "Risorsa della plancia per la scheda VMC Master non registrata" in caplog.text


# ----------------------------------------------------------- ultima VMC eliminata
async def test_togli_scheda_da_www_e_plance(hass: HomeAssistant) -> None:
    await _lovelace(hass)
    risorse = hass.data[LOVELACE_DATA].resources
    altra = await risorse.async_create_item({"res_type": "module", "url": "/local/altra.js"})
    await vmc._registra_risorsa_plancia(hass, f"{LOCALE}?v=9.0.0b29")
    await hass.async_add_executor_job(vmc._copia_scheda_in_www, hass.config.config_dir)
    await vmc._togli_scheda_da_www_e_plance(hass)
    assert _nostre(hass) == []
    assert [v["id"] for v in risorse.async_items()] == [altra["id"]]
    assert not _cartella(hass).exists()


async def test_togli_scheda_cartella_con_altri_file_resta(hass: HomeAssistant) -> None:
    await _lovelace(hass, "yaml")
    await hass.async_add_executor_job(vmc._copia_scheda_in_www, hass.config.config_dir)
    (_cartella(hass) / "mio.txt").write_text("dell'utente")
    await vmc._togli_scheda_da_www_e_plance(hass)
    assert sorted(p.name for p in _cartella(hass).iterdir()) == ["mio.txt"]


async def test_togli_scheda_errore_nel_registro(hass: HomeAssistant, caplog) -> None:
    hass.data.pop(LOVELACE_DATA, None)
    with patch.object(vmc, "_togli_scheda_da_www", side_effect=OSError("disco")):
        await vmc._togli_scheda_da_www_e_plance(hass)
    assert "Scheda VMC Master non tolta da www o dalle risorse delle plance" in caplog.text


@pytest.mark.parametrize("altre", [0, 1])
async def test_eliminazione_toglie_la_scheda_solo_con_l_ultima_vmc(
    hass: HomeAssistant, altre: int
) -> None:
    voci = [
        MockConfigEntry(domain=DOMAIN, unique_id=nome, data={"nome": nome, "host": ip})
        for nome, ip in (("master", "192.168.1.160"), ("sala", "192.168.1.161"))[: altre + 1]
    ]
    for voce in voci:
        voce.add_to_hass(hass)
    with (
        patch.object(vmc, "_togli_scheda_da_www_e_plance", AsyncMock()) as togli,
        patch.object(vmc, "sposta_in_backup", return_value=None),
        patch.object(vmc, "_togli_entita_della_vmc", return_value=True),
    ):
        await vmc.async_remove_entry(hass, voci[0])
    assert togli.await_count == (1 if altre == 0 else 0)
