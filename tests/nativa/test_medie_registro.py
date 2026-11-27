"""Lettura delle statistiche per le medie, con il registro (recorder) vero di Home Assistant."""

from __future__ import annotations

from datetime import timedelta
from unittest.mock import patch

import pytest
from homeassistant.components.recorder import Recorder
from homeassistant.components.recorder.models import StatisticMeanType
from homeassistant.components.recorder.statistics import async_import_statistics
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import UpdateFailed
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import async_fire_time_changed
from pytest_homeassistant_custom_component.components.recorder.common import (
    async_wait_recording_done,
)

from custom_components.vmc_master.nativa.letture import LetturaMedie, leggi_statistiche
from custom_components.vmc_master.nativa.memoria import GIORNI_DATI, calcola_medie

NOME = "master"


# Il registro va preparato prima di Home Assistant: qui le due impostazioni comuni dei
# test (conftest.py) chiedono prima recorder_mock.
@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(recorder_mock, enable_custom_integrations):
    """Integrazioni personalizzate abilitate, dopo il registro."""
    yield


@pytest.fixture(autouse=True)
def cartella_config_temporanea(recorder_mock, hass, tmp_path):
    """Cartella di configurazione temporanea, dopo il registro."""
    hass.config.config_dir = str(tmp_path)
    yield


async def _importa(hass: HomeAssistant, statistica: str, ore: int, base: float) -> None:
    """Statistiche orarie inventate per un sensore della VMC (una ora su sette senza dati)."""
    adesso = dt_util.utcnow().replace(minute=0, second=0, microsecond=0)
    metadati = {
        "has_sum": False,
        "mean_type": StatisticMeanType.ARITHMETIC,
        "name": None,
        "source": "recorder",
        "statistic_id": f"sensor.vmc_{NOME}_{statistica}",
        "unit_of_measurement": None,
        "unit_class": None,
    }
    righe = [
        {
            "start": adesso - timedelta(hours=i),
            "mean": base + (i % 11) / 3,
            "min": base,
            "max": base + 4,
        }
        for i in range(ore, 0, -1)
        if i % 7
    ]
    async_import_statistics(hass, metadati, righe)


async def test_statistiche_uguali_al_servizio(
    recorder_mock: Recorder, hass: HomeAssistant
) -> None:
    """Stesse righe del servizio recorder.get_statistics usato dal Package, stesse medie."""
    await _importa(hass, "temp_interna_numeric", 24 * 90, 20.0)
    await _importa(hass, "hum_interna_numeric", 24 * 40, 50.0)
    await async_wait_recording_done(hass)

    lette = await leggi_statistiche(hass, NOME)
    servizio = await hass.services.async_call(
        "recorder",
        "get_statistics",
        {
            "statistic_ids": [
                f"sensor.vmc_{NOME}_temp_interna_numeric",
                f"sensor.vmc_{NOME}_hum_interna_numeric",
            ],
            "start_time": (dt_util.now() - timedelta(days=84))
            .replace(microsecond=0)
            .isoformat(),
            "period": "hour",
            "types": ["mean"],
        },
        blocking=True,
        return_response=True,
    )
    assert lette == servizio
    assert len(lette["statistics"][f"sensor.vmc_{NOME}_temp_interna_numeric"]) > 1500

    adesso = dt_util.utcnow()
    medie = calcola_medie(lette, adesso, NOME)
    assert medie == calcola_medie(servizio, adesso, NOME)
    assert all(isinstance(v, float) for k, v in medie.items() if k != GIORNI_DATI)
    assert 39 < medie[GIORNI_DATI] < 41

    coordinatore = LetturaMedie(hass, None, NOME)
    await coordinatore.async_refresh()
    assert coordinatore.data == medie


async def test_senza_statistiche(recorder_mock: Recorder, hass: HomeAssistant) -> None:
    """Nessuna statistica: medie senza dati e 0 giorni."""
    coordinatore = LetturaMedie(hass, None, NOME)
    await coordinatore.async_refresh()
    assert coordinatore.data == {
        "sensor.temp_interna_media_4w": None,
        "sensor.hum_interna_media_4w": None,
        "sensor.temp_interna_media_8w": None,
        "sensor.hum_interna_media_8w": None,
        "sensor.temp_interna_media_12w": None,
        "sensor.hum_interna_media_12w": None,
        "sensor.rischio_muffa_giorni_dati": 0,
    }


async def test_lettura_non_riuscita(
    recorder_mock: Recorder, hass: HomeAssistant
) -> None:
    """Errore del servizio, come l'azione del Package con continue_on_error: un errore di
    Home Assistant si salta (medie senza dati); un altro errore ferma l'azione (le medie
    non si scrivono: lettura non riuscita del coordinatore)."""
    servizio = "homeassistant.components.recorder.services.statistics_during_period"
    with patch(servizio, side_effect=HomeAssistantError("database")):
        assert await leggi_statistiche(hass, NOME) is None
    coordinatore = LetturaMedie(hass, None, NOME)
    with patch(servizio, side_effect=RuntimeError("database")):
        with pytest.raises(UpdateFailed):
            await leggi_statistiche(hass, NOME)
        await coordinatore.async_refresh()
    assert coordinatore.last_update_success is False


async def test_ogni_ora_al_minuto_5(
    recorder_mock: Recorder, hass: HomeAssistant, freezer
) -> None:
    """Il ricalcolo parte al minuto 5 di ogni ora, non agli altri minuti."""
    freezer.move_to("2026-11-25 10:03:00+00:00")
    coordinatore = LetturaMedie(hass, None, NOME)
    chiamate = []

    async def conta(hass_, nome):
        chiamate.append(dt_util.utcnow())

    with patch("custom_components.vmc_master.nativa.letture.leggi_statistiche", conta):
        ferma = coordinatore.avvia_orario()
        for minuti in (1, 1, 1, 58, 1, 1):
            freezer.tick(timedelta(minutes=minuti))
            async_fire_time_changed(hass)
            await hass.async_block_till_done()
        ferma()
    assert [c.strftime("%H:%M") for c in chiamate] == ["10:05", "11:05"]
