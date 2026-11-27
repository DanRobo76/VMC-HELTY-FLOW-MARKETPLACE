"""b45: la pagina di un'automazione della VMC si apre (27-11-2026).

Impostazioni → Automazioni e scenari → clic su un'automazione della VMC: la pagina chiede
a Home Assistant la configurazione (``automation/config``) e con ``None`` girava
all'infinito. Ora riceve il nome e la descrizione (con la nota che attivazioni,
condizioni e azioni sono nel codice dell'integrazione), senza attivazioni, condizioni e
azioni: la pagina si apre in sola lettura, come ogni automazione fuori da automations.yaml;
con l'``id`` dell'automazione il pulsante «Tracce» della pagina apre le esecuzioni.
``automation.reload`` lascia le 13 automazioni come sono (stesse entità, accese), anche
con la configurazione mostrata.

Home Assistant vero, VMC finta (nessuna rete)."""

from __future__ import annotations

from pathlib import Path

from homeassistant.components.automation import DATA_COMPONENT
from homeassistant.core import HomeAssistant

from custom_components.vmc_master.nativa.motore.ha import NOTA_CONFIGURAZIONE

from .banco import aggiungi_e_avvia, automazioni_attese, senza_rete, voce


async def test_pagina_e_ricarica(hass: HomeAssistant, hass_ws_client) -> None:
    """Le 13 automazioni della VMC danno alla pagina una configurazione che si apre;
    automation.reload le lascia come sono."""
    with senza_rete():
        una = voce("master")
        await aggiungi_e_avvia(hass, [una])
        client = await hass_ws_client(hass)
        attese = automazioni_attese("master")
        assert len(attese) == 13
        for numero, entity_id in enumerate(sorted(attese), start=1):
            await client.send_json(
                {"id": numero, "type": "automation/config", "entity_id": entity_id}
            )
            risposta = await client.receive_json()
            assert risposta["success"], (entity_id, risposta)
            config = risposta["result"]["config"]
            assert isinstance(config, dict), entity_id
            assert list(config) == [
                "id",
                "alias",
                "description",
                "triggers",
                "conditions",
                "actions",
            ]
            assert config["id"] == hass.states.get(entity_id).attributes["id"]
            assert config["alias"] == hass.states.get(entity_id).name
            assert config["description"].startswith(NOTA_CONFIGURAZIONE + "\n\n"), (
                entity_id
            )
            assert len(config["description"]) > len(NOTA_CONFIGURAZIONE) + 2, entity_id
            assert config["triggers"] == config["conditions"] == config["actions"] == []

        componente = hass.data[DATA_COMPONENT]
        prima = {e: componente.get_entity(e) for e in attese}
        accese = {e for e in attese if hass.states.get(e).state == "on"}
        # automation.reload rilegge configuration.yaml, senza automazioni della VMC
        Path(hass.config.path("configuration.yaml")).write_text(
            "automation: []\n", encoding="utf-8"
        )
        await hass.services.async_call("automation", "reload", blocking=True)
        await hass.async_block_till_done()
        assert {e: componente.get_entity(e) for e in attese} == prima
        assert all(componente.get_entity(e) is prima[e] for e in attese)
        assert {e for e in attese if hass.states.get(e).state == "on"} == accese

        assert await hass.config_entries.async_unload(una.entry_id)
        await hass.async_block_till_done()
