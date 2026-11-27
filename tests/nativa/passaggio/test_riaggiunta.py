"""VMC eliminata e aggiunta di nuovo con lo stesso nome (Home Assistant vero).

Home Assistant ricorda le entità tolte con la voce (``deleted_entities``: stessa voce del
registro e stesso stato da ripristinare se tornano), quindi le impostazioni visibili
tornano come erano. Con la beta valeva lo stesso per tutti gli aiutanti del package,
anche quelli che oggi sono valori interni (``input_text.‹nome›_last_humidity_internal_entity``
e gli altri «ultima scelta» con cui il motore, a ogni avvio, rimette l'entità scelta nei
7 elenchi di scelta delle entità): i valori interni non si dimenticano con la voce."""

from __future__ import annotations

from datetime import timedelta
from pathlib import Path

import pytest
from homeassistant.core import Context, HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.restore_state import STATE_EXPIRATION
from homeassistant.util import dt as dt_util

from custom_components.vmc_master import passaggio
from custom_components.vmc_master.const import DOMAIN
from custom_components.vmc_master.nativa.motore.memoria_interna import (
    CHIAVE_ARCHIVIO as CHIAVE_MEMORIA_INTERNA,
)

from .banco import (
    aggiungi_e_avvia,
    carica_package,
    riavvio,
    scrivi_package_beta,
    senza_rete,
    voce,
)

ULTIMA_SCELTA = "input_text.last_humidity_internal_entity"


@pytest.fixture(autouse=True)
def rete_finta():
    with senza_rete():
        yield


@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_valori_interni_dopo_eliminazione_e_nuova_aggiunta(
    hass: HomeAssistant, hass_storage
) -> None:
    sud = voce("sud", 2)
    await aggiungi_e_avvia(hass, [sud])
    memoria = sud.runtime_data.vmc.memoria
    entity_id = memoria.entity_id(ULTIMA_SCELTA)
    await memoria.async_chiama(
        "input_text",
        "set_value",
        {"entity_id": entity_id, "value": "sensor.sonda_umidita_interna"},
        Context(),
    )
    assert memoria.stato(entity_id).state == "sensor.sonda_umidita_interna"

    assert await hass.config_entries.async_remove(sud.entry_id)
    await hass.async_block_till_done()
    di_nuovo = voce("sud", 2, entry_id="voce_sud_di_nuovo")
    di_nuovo.add_to_hass(hass)
    assert await hass.config_entries.async_setup(di_nuovo.entry_id)
    await hass.async_block_till_done()

    assert hass.config_entries.async_get_entry(di_nuovo.entry_id) is not None
    memoria = di_nuovo.runtime_data.vmc.memoria
    assert memoria.stato(entity_id).state == "sensor.sonda_umidita_interna"
    assert len(hass.config_entries.async_entries(DOMAIN)) == 1
    chiave = CHIAVE_MEMORIA_INTERNA.format(nome="sud")
    assert "eliminata" not in hass_storage[chiave]["data"]

    # aggiunta di nuovo dopo più di 7 giorni: come gli stati delle entità, non vale più
    assert await hass.config_entries.async_remove(di_nuovo.entry_id)
    await hass.async_block_till_done()
    hass_storage[chiave]["data"]["eliminata"] = (
        dt_util.utcnow() - STATE_EXPIRATION - timedelta(minutes=1)
    ).isoformat()
    ancora = voce("sud", 2, entry_id="voce_sud_ancora")
    ancora.add_to_hass(hass)
    assert await hass.config_entries.async_setup(ancora.entry_id)
    await hass.async_block_till_done()
    assert ancora.runtime_data.vmc.memoria.stato(entity_id).state == "unknown"


@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_con_la_beta_gli_aiutanti_tornavano(
    hass: HomeAssistant, tmp_path: Path
) -> None:
    """Il confronto con la beta: «Elimina» spostava il package nel backup e toglieva dal
    registro le sue entità (``_togli_entita_della_vmc``); aggiunta di nuovo, la VMC
    aveva lo stesso package e Home Assistant rimetteva gli aiutanti com'erano, anche
    l'ultima scelta della sonda (l'elenco di scelta riparte dalla sua opzione, poi il
    motore lo rimette dall'ultima scelta)."""
    config_dir = str(tmp_path)
    cartella = scrivi_package_beta(config_dir, "sud", "192.168.1.162")
    await carica_package(hass, [cartella])
    ultima = "input_text.vmc_sud_last_humidity_internal_entity"
    scelta = "input_select.vmc_sud_selected_humidity_internal_entity"
    await hass.services.async_call(
        "input_text",
        "set_value",
        {"entity_id": ultima, "value": "sensor.sonda_umidita_interna"},
        blocking=True,
    )
    await hass.services.async_call(
        "input_select",
        "set_options",
        {"entity_id": scelta, "options": ["sensor.sonda_umidita_interna"]},
        blocking=True,
    )
    registro = er.async_get(hass)
    del_package = passaggio.id_del_package(config_dir, "sud")
    for voce_registro in list(registro.entities.values()):
        if (
            voce_registro.config_entry_id is None
            and (voce_registro.domain, voce_registro.platform, voce_registro.unique_id)
            in del_package
        ):
            registro.async_remove(voce_registro.entity_id)
    backup = tmp_path / "vmc_master_backup" / "sud"
    backup.parent.mkdir()
    cartella.rename(backup)

    async with riavvio(hass, [], config_dir) as senza:  # VMC eliminata: niente package
        await senza.async_block_till_done()
        backup.rename(cartella)  # aggiunta di nuovo: lo stesso package
        async with riavvio(senza, [], config_dir) as di_nuovo:
            await carica_package(di_nuovo, [cartella])
            assert di_nuovo.states.get(ultima).state == "sensor.sonda_umidita_interna"
            # l'elenco riparte dalla sua opzione, come a ogni avvio
            assert di_nuovo.states.get(scelta).state == (
                "Aggiorna Elenco Entità Umidità Interna"
            )
