"""Le 14 automazioni del motore e la voce della VMC (Home Assistant vero).

Le automazioni del motore sono entità del componente ``automation``, con gli entity_id
e gli unique_id della beta: la loro voce del registro è legata alla voce della VMC
(``config_entry_id``), così Home Assistant le toglie con la voce quando la VMC si
elimina, come le altre sue entità, senza pulizie dell'integrazione. Restano automazioni
come le altre: girano, si spengono, si accendono e si avviano a mano; area, etichette e
categoria date dall'utente con la beta restano dopo il passaggio.

Il componente ``automation`` stacca il legame a ogni aggiunta delle entità (le sue
entità non hanno una voce: ``config_entry=None``), quindi l'integrazione lo rimette a
ogni avvio del motore; ``automation.reload`` lascia le entità del motore come sono."""

from __future__ import annotations

from pathlib import Path

import pytest
from homeassistant.config_entries import ConfigEntryDisabler
from homeassistant.core import HomeAssistant
from homeassistant.helpers import area_registry as ar
from homeassistant.helpers import category_registry as cr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import label_registry as lr
from pytest_homeassistant_custom_component.common import async_capture_events

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


def _legate(hass: HomeAssistant) -> dict[str, str | None]:
    registro = er.async_get(hass)
    return {
        e: (v.config_entry_id if (v := registro.async_get(e)) else None)
        for e in automazioni_attese("master")
    }


@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_automazioni_legate_alla_voce(
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

            # stessa voce del registro, con area, etichetta e categoria; legata alla VMC
            dopo = registro.async_get(AUTOMAZIONE)
            assert (dopo.id, dopo.area_id, dopo.labels, dopo.categories) == (
                della_beta.id,
                area.id,
                {etichetta.label_id},
                {"automation": categoria.category_id},
            )
            assert _legate(nativa) == dict.fromkeys(
                automazioni_attese("master"), master.entry_id
            )

            # spenta come nella beta della prova (initial_state: false): si accende e
            # gira con i suoi trigger
            assert nativa.states.get(AUTOMAZIONE).state == "off"
            await _servizio(nativa, "automation.turn_on", AUTOMAZIONE)
            assert nativa.states.get(AUTOMAZIONE).state == "on"
            assert await _apri_il_timer_con_extra_aperta(nativa) == "off"
            assert nativa.states.get(AUTOMAZIONE).attributes["last_triggered"]

            # spenta non gira
            await _servizio(nativa, "automation.turn_off", AUTOMAZIONE)
            assert nativa.states.get(AUTOMAZIONE).state == "off"
            assert await _apri_il_timer_con_extra_aperta(nativa) == "on"

            # avviata a mano
            await _servizio(nativa, "automation.turn_on", AUTOMAZIONE)
            avviate = async_capture_events(nativa, "automation_triggered")
            await _servizio(nativa, "automation.trigger", AUTOMAZIONE)
            assert [e.data["entity_id"] for e in avviate] == [AUTOMAZIONE]

            # automation.reload (rilegge configuration.yaml, senza automazioni della
            # VMC) le lascia come sono, legate
            (tmp_path / "configuration.yaml").write_text("automation: []\n")
            await nativa.services.async_call("automation", "reload", blocking=True)
            await nativa.async_block_till_done()
            assert nativa.states.get(AUTOMAZIONE).state == "on"
            assert set(_legate(nativa).values()) == {master.entry_id}

            # la VMC ricaricata: il motore ripartito le lega di nuovo
            assert await nativa.config_entries.async_reload(master.entry_id)
            await nativa.async_block_till_done()
            assert set(_legate(nativa).values()) == {master.entry_id}
            assert await _apri_il_timer_con_extra_aperta(nativa) == "off"

            # la VMC disattivata: Home Assistant disattiva anche le sue automazioni (il
            # motore è fermo); riattivata, tornano attive e girano
            await nativa.config_entries.async_set_disabled_by(
                master.entry_id, ConfigEntryDisabler.USER
            )
            await nativa.async_block_till_done()
            assert {
                registro.async_get(e).disabled_by for e in automazioni_attese("master")
            } == {er.RegistryEntryDisabler.CONFIG_ENTRY}
            await nativa.config_entries.async_set_disabled_by(master.entry_id, None)
            await nativa.async_block_till_done()
            assert {
                registro.async_get(e).disabled_by for e in automazioni_attese("master")
            } == {None}
            assert set(_legate(nativa).values()) == {master.entry_id}
            assert nativa.states.get(AUTOMAZIONE).state == "on"
            assert await _apri_il_timer_con_extra_aperta(nativa) == "off"

            # la VMC eliminata: Home Assistant toglie le automazioni con la voce
            assert await nativa.config_entries.async_remove(master.entry_id)
            await nativa.async_block_till_done()
            assert _legate(nativa) == dict.fromkeys(automazioni_attese("master"))
            assert [
                e for e in automazioni_attese("master") if nativa.states.get(e)
            ] == []
            # ricordate come le altre entità tolte (area ed etichetta comprese)
            ricordata = registro.deleted_entities[
                ("automation", "automation", "vmc_master_esclusivita_finestre_opzioni")
            ]
            assert (ricordata.id, ricordata.area_id, ricordata.config_entry_id) == (
                della_beta.id,
                area.id,
                None,
            )
