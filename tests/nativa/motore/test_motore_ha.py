"""Il motore tradotto si avvia su Home Assistant con le entità del package."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component

from custom_components.vmc_master.nativa.motore.ha import Motore


async def test_avvio_entita(hass: HomeAssistant) -> None:
    """14 automazioni e 51 script, con gli entity_id e gli attributi di Home Assistant."""
    assert await async_setup_component(hass, "homeassistant", {})
    motore = Motore(hass)
    await motore.avvia()
    await hass.async_block_till_done()
    automazioni = hass.states.async_entity_ids("automation")
    script = hass.states.async_entity_ids("script")
    assert len(automazioni) == 14
    assert len(script) == 51
    assert "automation.automazione_vmc_master" in automazioni
    stato = hass.states.get("automation.automazione_vmc_master")
    assert stato.state == "on"
    assert stato.attributes["mode"] == "queued"
    assert hass.services.has_service("script", script[0].split(".", 1)[1])
    await hass.services.async_call(
        "automation", "turn_off", {"entity_id": "all"}, blocking=True
    )
    assert hass.states.get("automation.automazione_vmc_master").state == "off"
