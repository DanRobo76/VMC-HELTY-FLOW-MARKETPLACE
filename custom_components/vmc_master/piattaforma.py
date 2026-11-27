"""Le piattaforme delle entità native: le entità le aggiunge l'assemblaggio.

Ogni piattaforma della voce (switch, sensor...) all'avvio si registra soltanto
(``DatiVoce.piattaforme``): l'assemblaggio (nativa/assemblaggio.py) aggiunge poi le entità
di ogni dominio nel suo ordine, aspettando che ogni gruppo sia aggiunto prima del
successivo (le impostazioni prima delle letture, il motore prima dei sensori template...).
"""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_platform
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Registra la piattaforma della voce per il suo dominio."""
    piattaforma = entity_platform.async_get_current_platform()
    entry.runtime_data.piattaforme[piattaforma.domain] = piattaforma
