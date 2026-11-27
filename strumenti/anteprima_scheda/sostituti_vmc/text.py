"""Sostituti della piattaforma text (vedi __init__.py)."""

from .entita import prepara


async def async_setup_platform(
    hass, config, async_add_entities, discovery_info=None
) -> None:
    """Le entità sostitute text."""
    await prepara(hass, "text", async_add_entities)
