"""Il motore tradotto si avvia su Home Assistant con le logiche e gli script del package."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component

from custom_components.vmc_master.nativa.motore.ha import Motore
from custom_components.vmc_master.nativa.motore.stati_logiche import stati_logiche


async def test_avvio_logiche_e_script(hass: HomeAssistant) -> None:
    """14 automazioni come logiche (stati interni con gli entity_id e gli attributi che
    avrebbero le entità di Home Assistant) e 51 script interni: nessuna entità
    ``automation`` o ``script``, nessun servizio ``script.*``. Fermato, il motore toglie
    gli stati delle logiche."""
    assert await async_setup_component(hass, "homeassistant", {})
    motore = Motore(hass)
    await motore.avvia()
    await hass.async_block_till_done()
    assert hass.states.async_entity_ids(("automation", "script")) == []
    assert len(motore.automazioni) == 14
    stati = stati_logiche(hass)
    assert sorted(stati.stati) == sorted(a.entity_id for a in motore.automazioni)
    stato = stati.stato("automation.automazione_vmc_master")
    assert stato is not None
    assert stato.state == "on"
    assert stato.attributes["mode"] == "queued"
    assert motore.c.interni is not None
    assert len(motore.c.interni.script) == 51
    assert not hass.services.async_services_for_domain("script")
    await motore.ferma()
    assert stati.stati == {}
