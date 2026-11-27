"""b45: le prove con il package della beta non dipendono dall'ora (27-11-2026).

Il blocco template delle medie del package gira all'avvio e al minuto 5 di ogni ora
con l'azione ``recorder.get_statistics``. Nelle prove il recorder non c'è: al minuto 5
dell'orologio vero il blocco lasciava un'eccezione e la prova che girava in quel minuto
falliva (CI della PR #46, test_passaggio_di_tre_vmc). ``carica_package`` toglie quel
trigger quando il recorder manca; con il recorder lascia il blocco com'è."""

from __future__ import annotations

from datetime import timedelta
from pathlib import Path

import pytest
from homeassistant.core import HomeAssistant, ServiceResponse, SupportsResponse
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import async_fire_time_changed

from .banco import carica_package, scrivi_package_beta


def _blocco_medie(config: dict) -> dict:
    (blocco,) = [
        b
        for b in config["template"]
        if any(
            a.get("action") == "recorder.get_statistics" for a in b.get("actions") or []
        )
    ]
    return blocco


def _minuto_5() -> object:
    adesso = dt_util.utcnow()
    # il minuto 5 dell'ora dopo, appena passato (l'ascolto ha qualche decimo di ritardo)
    return adesso.replace(minute=5, second=1, microsecond=0) + timedelta(hours=1)


@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_senza_recorder_il_minuto_5_non_lascia_eccezioni(
    hass: HomeAssistant, tmp_path: Path
) -> None:
    """Senza recorder il blocco delle medie resta con il solo trigger di avvio e il
    minuto 5 passa senza eccezioni (le eccezioni lasciate fanno fallire la prova)."""
    cartella = scrivi_package_beta(str(tmp_path), "master", "192.168.1.160")
    config = await carica_package(hass, [cartella])
    trigger = _blocco_medie(config)["triggers"]
    assert [t["trigger"] for t in trigger] == ["homeassistant"]
    async_fire_time_changed(hass, _minuto_5())
    await hass.async_block_till_done()


@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_con_recorder_il_blocco_resta_com_e(
    hass: HomeAssistant, tmp_path: Path
) -> None:
    """Con l'azione del recorder il blocco delle medie resta com'è e al minuto 5 la
    chiama."""
    chiamate: list[dict] = []

    async def statistiche(chiamata) -> ServiceResponse:
        chiamate.append(dict(chiamata.data))
        return {"statistics": {}}

    hass.services.async_register(
        "recorder",
        "get_statistics",
        statistiche,
        supports_response=SupportsResponse.ONLY,
    )
    cartella = scrivi_package_beta(str(tmp_path), "master", "192.168.1.160")
    config = await carica_package(hass, [cartella])
    trigger = _blocco_medie(config)["triggers"]
    assert [t["trigger"] for t in trigger] == ["homeassistant", "time_pattern"]
    async_fire_time_changed(hass, _minuto_5())
    await hass.async_block_till_done()
    assert len(chiamate) == 1
