"""La riparazione dei nomi cambiati elenca ogni vecchio nome che l'utente usa ancora,
non solo le entità: anche i servizi del package che non ci sono più (i 51 script, come
azione ``script.‹id›`` o come entità di ``script.turn_on``, i 16 ``shell_command``) e
gli aiutanti nei servizi ``input_*.*``, nei modelli e nelle plance (Home Assistant
vero: automazioni e script dell'utente con le integrazioni vere, plancia salvata)."""

from __future__ import annotations

from pathlib import Path

import pytest
from homeassistant.components.lovelace.const import LOVELACE_DATA
from homeassistant.core import HomeAssistant
from homeassistant.helpers import issue_registry as ir
from homeassistant.setup import async_setup_component

from custom_components.vmc_master import ISSUE_RINOMINATE
from custom_components.vmc_master.const import DOMAIN

from .banco import (
    aggiungi_e_avvia,
    carica_package,
    conferma_dalla_riparazione,
    riavvio,
    scrivi_package_beta,
    senza_rete,
    voce,
)


@pytest.fixture(autouse=True)
def rete_finta():
    with senza_rete():
        yield


AUTOMAZIONI = [
    {
        # l'automazione d'esempio del README della beta
        "id": "velocita_di_notte",
        "alias": "Velocità di notte",
        "triggers": [{"trigger": "time", "at": "23:00:00"}],
        "actions": [{"action": "shell_command.vmc_master_velocita_1"}],
    },
    {
        "id": "profilo",
        "alias": "Profilo",
        "triggers": [{"trigger": "time", "at": "07:00:00"}],
        "conditions": [
            {
                "condition": "template",
                "value_template": "{{ is_state('input_select.vmc_master_speed_umidita', 'Velocità 2') }}",
            }
        ],
        "actions": [
            {"action": "script.vmc_master_profilo_umidita"},
            {
                "action": "script.turn_on",
                "target": {"entity_id": "script.vmc_master_notifica_cambio_filtro"},
            },
            {
                "action": "input_number.set_value",
                "target": {"entity_id": "input_number.vmc_master_umidita_avvio"},
                "data": {"value": 60},
            },
        ],
    },
]
SCRIPT = {
    "mio_script": {
        "alias": "Mio script",
        "sequence": [
            {"action": "shell_command.vmc_master_pannello_led_off"},
            {
                "action": "timer.cancel",
                "target": {"entity_id": "timer.vmc_master_lettura_ambientali"},
            },
        ],
    }
}
PLANCIA = {
    "views": [
        {
            "cards": [
                {
                    "type": "entities",
                    "entities": [
                        "input_datetime.vmc_master_accensione_lunedi",
                        "sensor.vmc_master_temp_interna_status_senza_offset",
                    ],
                },
                {
                    "type": "button",
                    "tap_action": {
                        "action": "perform-action",
                        "perform_action": "script.vmc_master_bottone_panico",
                    },
                },
            ]
        }
    ]
}


@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_vecchi_nomi_e_servizi_dell_utente(
    hass: HomeAssistant, hass_storage, tmp_path: Path
) -> None:
    config_dir = str(tmp_path)
    master = voce("master")
    cartella = scrivi_package_beta(config_dir, "master", master.data["host"])
    await carica_package(hass, [cartella])

    async with riavvio(hass, [master], config_dir) as beta:
        await carica_package(beta, [cartella], AUTOMAZIONI, SCRIPT)
        assert await async_setup_component(beta, "lovelace", {})
        await beta.data[LOVELACE_DATA].dashboards[None].async_save(PLANCIA)
        await aggiungi_e_avvia(beta, [])
        await conferma_dalla_riparazione(beta)

        problema = ir.async_get(beta).async_get_issue(DOMAIN, ISSUE_RINOMINATE)
        assert problema is not None
        assert problema.translation_placeholders["elenco"].splitlines() == [
            (
                "- automation.profilo: `input_number.vmc_master_umidita_avvio`"
                " → `number.vmc_master_umidita_avvio`"
            ),
            (
                "- automation.profilo: `input_select.vmc_master_speed_umidita`"
                " → `select.vmc_master_speed_umidita`"
            ),
            "- automation.profilo: `script.vmc_master_notifica_cambio_filtro` → `-`",
            (
                "- automation.profilo: `script.vmc_master_profilo_umidita`"
                " → `button.vmc_master_profilo_umidita`"
            ),
            (
                "- automation.velocita_di_notte: `shell_command.vmc_master_velocita_1`"
                " → `button.vmc_master_velocita_1`"
            ),
            (
                "- lovelace:lovelace: `input_datetime.vmc_master_accensione_lunedi`"
                " → `time.vmc_master_accensione_lunedi`"
            ),
            (
                "- lovelace:lovelace: `script.vmc_master_bottone_panico`"
                " → `button.vmc_master_bottone_panico`"
            ),
            (
                "- script.mio_script: `shell_command.vmc_master_pannello_led_off`"
                " → `button.vmc_master_pannello_led_off`"
            ),
            (
                "- script.mio_script: `timer.vmc_master_lettura_ambientali`"
                " → `sensor.vmc_master_lettura_ambientali`"
            ),
        ]
