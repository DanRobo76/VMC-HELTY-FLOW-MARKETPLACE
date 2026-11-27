"""Prove della 9.0.0b29, nella versione nativa: la scheda VMC Master compare nelle plance
anche se la pagina e' stata aperta (o ricaricata) mentre Home Assistant si avviava.

Il file JavaScript si serve dalla cartella dell'integrazione (percorso statico registrato
prima che il server http accetti richieste); la risorsa delle plance
(/vmc_master_frontend/vmc-master-card.js?v=...) si carica all'apertura della plancia.
Nessuna copia in /config/www: quella che scriveva la beta si toglie solo con il passaggio
confermato (tests/nativa/passaggio/test_scheda_js.py)."""

from __future__ import annotations

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
NATIVA = vmc.URL_SCHEDA
BETA = vmc.URL_LOCALE_DELLA_BETA


def _cartella_della_beta(hass: HomeAssistant) -> Path:
    return Path(hass.config.config_dir) / "www" / vmc.CARTELLA_WWW_DELLA_BETA


def _nostre(hass: HomeAssistant) -> list[dict]:
    return [
        voce
        for voce in hass.data[LOVELACE_DATA].resources.async_items()
        if voce["url"].split("?", 1)[0] in (NATIVA, BETA)
    ]


async def _lovelace(hass: HomeAssistant, modo: str = "storage") -> None:
    assert await async_setup_component(hass, "http", {})
    assert await async_setup_component(hass, "lovelace", {"lovelace": {"resource_mode": modo}})
    await hass.data[LOVELACE_DATA].resources.async_get_info()


# ----------------------------------------------------------- risorsa delle plance
async def test_risorsa_creata_aggiornata_doppie_tolte(hass: HomeAssistant) -> None:
    await _lovelace(hass)
    risorse = hass.data[LOVELACE_DATA].resources
    altra = await risorse.async_create_item({"res_type": "module", "url": "/local/altra.js"})
    await vmc._registra_risorsa_plancia(hass, f"{NATIVA}?v=9.0.0b29")
    assert [(v["type"], v["url"]) for v in _nostre(hass)] == [("module", f"{NATIVA}?v=9.0.0b29")]
    # stessa versione: niente da cambiare
    with patch.object(risorse, "async_update_item") as aggiorna:
        await vmc._registra_risorsa_plancia(hass, f"{NATIVA}?v=9.0.0b29")
    aggiorna.assert_not_called()
    # tipo sbagliato e una doppia: si corregge la prima, si toglie la seconda
    prima = _nostre(hass)[0]
    await risorse.async_update_item(prima["id"], {"res_type": "js"})
    await risorse.async_create_item({"res_type": "module", "url": f"{NATIVA}?v=vecchia"})
    await vmc._registra_risorsa_plancia(hass, f"{NATIVA}?v=9.0.0b30")
    assert [(v["id"], v["type"], v["url"]) for v in _nostre(hass)] == [
        (prima["id"], "module", f"{NATIVA}?v=9.0.0b30")
    ]
    # le risorse dell'utente restano
    assert any(v["id"] == altra["id"] for v in risorse.async_items())


async def test_risorsa_della_beta_fino_al_passaggio(hass: HomeAssistant) -> None:
    """La risorsa della beta resta com'e' finche' il passaggio non e' confermato; poi la
    stessa voce prende l'indirizzo dell'integrazione."""
    await _lovelace(hass)
    risorse = hass.data[LOVELACE_DATA].resources
    beta = await risorse.async_create_item({"res_type": "module", "url": f"{BETA}?v=9.0.0b41"})
    await vmc._registra_risorsa_plancia(hass, f"{NATIVA}?v=9.0.0")
    assert [(v["id"], v["url"]) for v in _nostre(hass)] == [(beta["id"], f"{BETA}?v=9.0.0b41")]
    await vmc._registra_risorsa_plancia(hass, f"{NATIVA}?v=9.0.0", anche_della_beta=True)
    assert [(v["id"], v["url"]) for v in _nostre(hass)] == [(beta["id"], f"{NATIVA}?v=9.0.0")]


async def test_risorsa_non_toccata_in_modo_yaml(hass: HomeAssistant) -> None:
    await _lovelace(hass, "yaml")
    risorse = hass.data[LOVELACE_DATA].resources
    await vmc._registra_risorsa_plancia(hass, f"{NATIVA}?v=9.0.0b29")
    assert risorse.async_items() == []


async def test_risorsa_senza_plance(hass: HomeAssistant) -> None:
    hass.data.pop(LOVELACE_DATA, None)
    await vmc._registra_risorsa_plancia(hass, f"{NATIVA}?v=9.0.0b29")  # nessun errore


# ------------------------------------------------------------------ _registra_scheda
async def test_registra_scheda(hass: HomeAssistant) -> None:
    await _lovelace(hass)
    with patch.object(vmc, "add_extra_js_url") as extra:
        await vmc._registra_scheda(hass, "9.0.0b29")
    extra.assert_called_once_with(hass, f"{NATIVA}?v=9.0.0b29")
    assert [v["url"] for v in _nostre(hass)] == [f"{NATIVA}?v=9.0.0b29"]
    assert not (Path(hass.config.config_dir) / "www").exists()


async def test_registra_scheda_risorsa_non_riuscita(hass: HomeAssistant, caplog) -> None:
    with (
        patch.object(vmc, "_registra_risorsa_plancia", AsyncMock(side_effect=ValueError("no"))),
        patch.object(vmc, "add_extra_js_url") as extra,
    ):
        await vmc._registra_scheda(hass, "9.0.0b29")
    extra.assert_called_once_with(hass, f"{NATIVA}?v=9.0.0b29")
    assert "Risorsa della plancia per la scheda VMC Master non registrata" in caplog.text


# ----------------------------------------------------------- ultima VMC eliminata
async def test_togli_risorse_plancia(hass: HomeAssistant) -> None:
    await _lovelace(hass)
    risorse = hass.data[LOVELACE_DATA].resources
    altra = await risorse.async_create_item({"res_type": "module", "url": "/local/altra.js"})
    await risorse.async_create_item({"res_type": "module", "url": f"{BETA}?v=9.0.0b41"})
    await vmc._registra_risorsa_plancia(hass, f"{NATIVA}?v=9.0.0b29", anche_della_beta=True)
    await risorse.async_create_item({"res_type": "module", "url": f"{BETA}?v=9.0.0b41"})
    _cartella_della_beta(hass).mkdir(parents=True)
    (_cartella_della_beta(hass) / JS).write_text("// beta")
    await vmc._togli_risorse_plancia(hass)
    assert _nostre(hass) == []
    assert [v["id"] for v in risorse.async_items()] == [altra["id"]]
    # in /config non si tocca nulla
    assert (_cartella_della_beta(hass) / JS).read_text() == "// beta"


async def test_togli_risorse_errore_nel_registro(hass: HomeAssistant, caplog) -> None:
    with patch.object(vmc, "_risorse_plance", AsyncMock(side_effect=OSError("disco"))):
        await vmc._togli_risorse_plancia(hass)
    assert "Scheda VMC Master non tolta dalle risorse delle plance" in caplog.text


# ------------------------------------------------------- copia della beta in www
async def test_copia_della_beta_tolta_cartella_con_altri_file_resta(hass: HomeAssistant) -> None:
    _cartella_della_beta(hass).mkdir(parents=True)
    (_cartella_della_beta(hass) / JS).write_text("// beta")
    (_cartella_della_beta(hass) / "mio.txt").write_text("dell'utente")
    hass.data[vmc.DATI_URL_SCHEDA] = f"{NATIVA}?v=9.0.0"
    await vmc._scheda_dopo_il_passaggio(hass)
    assert sorted(p.name for p in _cartella_della_beta(hass).iterdir()) == ["mio.txt"]


async def test_copia_della_beta_non_tolta(hass: HomeAssistant, caplog) -> None:
    hass.data[vmc.DATI_URL_SCHEDA] = f"{NATIVA}?v=9.0.0"
    with patch.object(vmc, "_togli_copia_della_beta", side_effect=OSError("disco")):
        await vmc._scheda_dopo_il_passaggio(hass)
    assert "Scheda della beta non tolta da www o dalle risorse" in caplog.text


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
        patch.object(vmc, "_togli_risorse_plancia", AsyncMock()) as togli,
    ):
        await vmc.async_remove_entry(hass, voci[0])
    assert togli.await_count == (1 if altre == 0 else 0)
