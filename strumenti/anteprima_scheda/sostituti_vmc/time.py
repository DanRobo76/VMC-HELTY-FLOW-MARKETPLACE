"""Sostituti della piattaforma time (vedi __init__.py)."""

from .entita import prepara


async def async_setup_platform(
    hass, config, async_add_entities, discovery_info=None
) -> None:
    """Le entità sostitute time."""
    await prepara(hass, "time", async_add_entities)
