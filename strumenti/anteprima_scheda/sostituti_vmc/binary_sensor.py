"""Sostituti della piattaforma binary_sensor (vedi __init__.py)."""

from .entita import prepara


async def async_setup_platform(
    hass, config, async_add_entities, discovery_info=None
) -> None:
    """Le entità sostitute binary_sensor."""
    await prepara(hass, "binary_sensor", async_add_entities)
