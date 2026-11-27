"""Sostituti della piattaforma number (vedi __init__.py)."""

from .entita import prepara


async def async_setup_platform(
    hass, config, async_add_entities, discovery_info=None
) -> None:
    """Le entità sostitute number."""
    await prepara(hass, "number", async_add_entities)
