"""Riparazioni: riavvio di Home Assistant dopo l'installazione o l'aggiornamento del package."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.repairs import ConfirmRepairFlow, RepairsFlow
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

_LOGGER = logging.getLogger(__name__)


class RiavvioFlow(RepairsFlow):
    """Chiede conferma e riavvia Home Assistant."""

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        return await self.async_step_confirm()

    async def async_step_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if user_input is not None:
            # Chiamata bloccante: il servizio controlla prima la configurazione e, se non
            # e' valida, non riavvia e solleva un errore. La riparazione allora non si
            # chiude come riuscita e l'avviso resta.
            try:
                await self.hass.services.async_call("homeassistant", "restart", blocking=True)
            except HomeAssistantError as errore:
                _LOGGER.warning("Riavvio di Home Assistant non eseguito: %s", errore)
                return self.async_abort(
                    reason="riavvio_non_riuscito", description_placeholders={"errore": str(errore)}
                )
            return self.async_create_entry(data={})
        return self.async_show_form(step_id="confirm")


async def async_create_fix_flow(
    hass: HomeAssistant, issue_id: str, data: dict[str, Any] | None
) -> RepairsFlow:
    if issue_id == "riavvio_necessario":
        return RiavvioFlow()
    return ConfirmRepairFlow()
