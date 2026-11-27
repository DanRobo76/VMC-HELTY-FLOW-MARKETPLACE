"""Le 13 automazioni del motore e la voce della VMC (Home Assistant vero).

Dalla 9.0.0b46 le automazioni del motore sono logiche dell'integrazione: nessuna entità
``automation`` e nessuna voce del registro (fino alla 9.0.0b45 erano entità del
componente ``automation``, con la voce del registro legata alla voce della VMC, e si
spegnevano, accendevano e avviavano a mano con i servizi ``automation.*``). Hanno uno
stato interno con l'entity_id della beta, girano con la VMC avviata, ricaricata o
riattivata e si fermano con lei (scaricata, disattivata, eliminata); ``automation.reload``
non le tocca. ``initial_state: false`` della beta non conta più: partono accese.

Con il passaggio dalla beta la voce del registro dell'automazione del package (con area,
etichetta e categoria date dall'utente) si toglie con le altre voci del package, e Home
Assistant la ricorda come ogni voce tolta."""

from __future__ import annotations

from pathlib import Path

import pytest
from homeassistant.config_entries import ConfigEntryDisabler
from homeassistant.core import HomeAssistant
from homeassistant.helpers import area_registry as ar
from homeassistant.helpers import category_registry as cr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import label_registry as lr
from homeassistant.setup import async_setup_component

from custom_components.vmc_master.nativa.motore.stati_logiche import stati_logiche

from .banco import (
    aggiungi_e_avvia,
    automazioni_attese,
    carica_package,
    conferma_dalla_riparazione,
    riavvio,
    scrivi_package_beta,
    senza_rete,
    voce,
)

AUTOMAZIONE = "automation.vmc_master_esclusivita_finestre_opzioni"
# la finestra «Timer Lettura Dati VMC» che si apre chiude la finestra dei sensori Extra
FINESTRA_TIMER = "switch.vmc_master_opzione_finestra_prossime_letture"
FINESTRA_EXTRA = "switch.vmc_master_opzioni_interruttore_monitoraggio_sensori_extra"


@pytest.fixture(autouse=True)
def rete_finta():
    with senza_rete():
        yield


async def _servizio(hass: HomeAssistant, servizio: str, entity_id: str) -> None:
    dominio, azione = servizio.split(".")
    await hass.services.async_call(
        dominio, azione, {"entity_id": entity_id}, blocking=True
    )
    await hass.async_block_till_done()


async def _apri_il_timer_con_extra_aperta(hass: HomeAssistant) -> str:
    """Apre la finestra dei sensori Extra, poi quella del timer: con l'automazione
    accesa la prima si chiude. Restituisce lo stato della finestra Extra."""
    await _servizio(hass, "switch.turn_off", FINESTRA_TIMER)
    await _servizio(hass, "switch.turn_on", FINESTRA_EXTRA)
    await _servizio(hass, "switch.turn_on", FINESTRA_TIMER)
    return hass.states.get(FINESTRA_EXTRA).state


def _logiche(hass: HomeAssistant) -> dict[str, str]:
    """Gli stati interni delle logiche della VMC «master» (nessuna entità ``automation``
    della VMC, nessuna voce del registro)."""
    attese = automazioni_attese("master")
    assert [e for e in attese if hass.states.get(e)] == []
    registro = er.async_get(hass)
    assert [e for e in attese if registro.async_get(e)] == []
    stati = stati_logiche(hass)
    return {e: s.state for e in attese if (s := stati.stato(e)) is not None}


@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_automazioni_della_vmc_senza_voce(
    hass: HomeAssistant, tmp_path: Path
) -> None:
    config_dir = str(tmp_path)
    master = voce("master")
    cartella = scrivi_package_beta(config_dir, "master", master.data["host"])

    # la beta: l'utente dà area, etichetta e categoria a un'automazione del package
    await carica_package(hass, [cartella])
    area = ar.async_get(hass).async_create("Cantina")
    etichetta = lr.async_get(hass).async_create("Aria")
    categoria = cr.async_get(hass).async_create(scope="automation", name="VMC")
    registro = er.async_get(hass)
    registro.async_update_entity(
        AUTOMAZIONE,
        area_id=area.id,
        labels={etichetta.label_id},
        categories={"automation": categoria.category_id},
    )
    della_beta = registro.async_get(AUTOMAZIONE)
    assert della_beta.config_entry_id is None

    async with riavvio(hass, [master], config_dir) as beta:
        await carica_package(beta, [cartella])
        await aggiungi_e_avvia(beta, [])
        await conferma_dalla_riparazione(beta)

        async with riavvio(beta, [master], config_dir) as nativa:
            await aggiungi_e_avvia(nativa, [])
            registro = er.async_get(nativa)

            # la voce della beta tolta con le altre del package e ricordata da Home
            # Assistant come ogni voce tolta (area compresa); nessuna voce nuova
            ricordata = registro.deleted_entities[
                ("automation", "automation", "vmc_master_esclusivita_finestre_opzioni")
            ]
            assert (ricordata.id, ricordata.area_id, ricordata.config_entry_id) == (
                della_beta.id,
                area.id,
                None,
            )
            assert registro.async_get(AUTOMAZIONE) is None

            # le 13 logiche accese (anche quella spenta nella beta della prova con
            # initial_state: false), girano con i loro trigger
            assert _logiche(nativa) == dict.fromkeys(automazioni_attese("master"), "on")
            voce_nativa = nativa.config_entries.async_get_entry(master.entry_id)
            assert voce_nativa is not None
            motore = voce_nativa.runtime_data.vmc.motore
            assert not nativa.services.has_service("automation", "turn_off")
            assert await _apri_il_timer_con_extra_aperta(nativa) == "off"
            stato = stati_logiche(nativa).stato(AUTOMAZIONE)
            assert stato is not None
            assert stato.attributes["last_triggered"]

            # automation.reload (rilegge configuration.yaml, senza automazioni) non le
            # tocca
            assert await async_setup_component(nativa, "automation", {})
            (tmp_path / "configuration.yaml").write_text("automation: []\n")
            await nativa.services.async_call("automation", "reload", blocking=True)
            await nativa.async_block_till_done()
            assert voce_nativa.runtime_data.vmc.motore is motore
            assert _logiche(nativa) == dict.fromkeys(automazioni_attese("master"), "on")
            assert await _apri_il_timer_con_extra_aperta(nativa) == "off"

            # la VMC ricaricata: un motore nuovo, logiche di nuovo avviate
            assert await nativa.config_entries.async_reload(master.entry_id)
            await nativa.async_block_till_done()
            assert voce_nativa.runtime_data.vmc.motore is not motore
            assert _logiche(nativa) == dict.fromkeys(automazioni_attese("master"), "on")
            assert await _apri_il_timer_con_extra_aperta(nativa) == "off"

            # la VMC disattivata: logiche fermate; riattivata, tornano e girano
            await nativa.config_entries.async_set_disabled_by(
                master.entry_id, ConfigEntryDisabler.USER
            )
            await nativa.async_block_till_done()
            assert _logiche(nativa) == {}
            await nativa.config_entries.async_set_disabled_by(master.entry_id, None)
            await nativa.async_block_till_done()
            assert _logiche(nativa) == dict.fromkeys(automazioni_attese("master"), "on")
            assert await _apri_il_timer_con_extra_aperta(nativa) == "off"

            # la VMC eliminata: logiche fermate, nulla nel registro; la voce della beta
            # resta ricordata com'era
            assert await nativa.config_entries.async_remove(master.entry_id)
            await nativa.async_block_till_done()
            assert _logiche(nativa) == {}
            assert registro.deleted_entities[
                ("automation", "automation", "vmc_master_esclusivita_finestre_opzioni")
            ] == ricordata
