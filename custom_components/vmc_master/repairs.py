"""Riparazioni: riavvio di Home Assistant dopo l'installazione o l'aggiornamento del package."""

from __future__ import annotations

from typing import Any

from homeassistant.components.repairs import ConfirmRepairFlow, RepairsFlow
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult


class RiavvioFlow(RepairsFlow):
    """Chiede conferma e riavvia Home Assistant."""

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        return await self.async_step_confirm()

    async def async_step_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if user_input is not None:
            await self.hass.services.async_call("homeassistant", "restart")
            return self.async_create_entry(data={})
        return self.async_show_form(step_id="confirm")


async def async_create_fix_flow(
    hass: HomeAssistant, issue_id: str, data: dict[str, Any] | None
) -> RepairsFlow:
    if issue_id == "riavvio_necessario":
        return RiavvioFlow()
    return ConfirmRepairFlow()
