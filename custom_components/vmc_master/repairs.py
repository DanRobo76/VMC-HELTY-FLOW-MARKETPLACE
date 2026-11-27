"""Riparazioni: passaggio dalla beta con la conferma dell'utente e riavvio di Home Assistant."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant import config as conf_util
from homeassistant.components.repairs import ConfirmRepairFlow, RepairsFlow
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import recorder

from . import (
    ISSUE_PASSAGGIO,
    ISSUE_RIAVVIO,
    _italiano,
    _segnala_riavvio,
    async_conferma_passaggio,
)

_LOGGER = logging.getLogger(__name__)


class RiavvioFlow(RepairsFlow):
    """Chiede conferma e riavvia Home Assistant."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        return await self.async_step_confirm()

    async def async_step_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if user_input is not None:
            # Prima gli stessi controlli che fa il servizio di riavvio: se il riavvio non
            # puo' partire, la riparazione non si chiude come riuscita e l'avviso resta.
            if errori := await conf_util.async_check_ha_config_file(self.hass):
                return self._non_riavviato(errori)
            if recorder.async_migration_in_progress(self.hass):
                return self._non_riavviato(
                    "aggiornamento del database della cronologia in corso: riprovare tra "
                    "qualche minuto"
                    if _italiano(self.hass)
                    else "history database upgrade in progress: try again in a few minutes"
                )
            if not self.hass.services.has_service("homeassistant", "restart"):
                return self._non_riavviato("homeassistant.restart")
            # Riavvio senza aspettarlo, come il Marketplace di HA: con la chiamata bloccante
            # HA si fermava prima che la risposta arrivasse al browser (con il Supervisor la
            # chiamata non torna mai), la finestra restava aperta e dopo il riavvio ogni
            # Invia dava «Invalid flow specified». Il compito parte dopo la chiusura della
            # riparazione: se il riavvio poi non parte, l'avviso torna.
            self.hass.async_create_background_task(
                _async_riavvia(self.hass), "vmc_master_riavvio", eager_start=False
            )
            return self.async_create_entry(data={})
        return self.async_show_form(step_id="confirm")

    def _non_riavviato(self, errore: str) -> FlowResult:
        _LOGGER.warning("Riavvio di Home Assistant non eseguito: %s", errore)
        return self.async_abort(
            reason="riavvio_non_riuscito", description_placeholders={"errore": errore}
        )


class PassaggioFlow(RiavvioFlow):
    """Passaggio dalla beta: con Invia si tolgono le cartelle del package della beta e i
    loro elementi del registro (i valori sono gia' salvati), poi si riavvia (secondo passo,
    quello del riavvio). Se nessun package era caricato le VMC ripartono subito, native."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        return await self.async_step_conferma()

    async def async_step_conferma(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if user_input is None:
            return self.async_show_form(step_id="conferma")
        esiti = await async_conferma_passaggio(self.hass)
        errori = [f"{esito.nome}: {esito.errore}" for esito in esiti if esito.errore]
        if errori:
            return self.async_abort(
                reason="cartella_non_tolta",
                description_placeholders={"errore": "\n".join(errori)},
            )
        if any(esito.riavvio for esito in esiti):
            return await self.async_step_confirm()
        return self.async_create_entry(data={})


async def _async_riavvia(hass: HomeAssistant) -> None:
    """Riavvia Home Assistant; se il servizio rifiuta (per esempio la configurazione
    cambiata nel frattempo), lo scrive nel registro e rimette l'avviso di riavvio."""
    try:
        await hass.services.async_call("homeassistant", "restart", blocking=True)
    except Exception as errore:  # noqa: BLE001 - qualunque errore: l'avviso deve tornare
        _LOGGER.warning("Riavvio di Home Assistant non eseguito: %s", errore)
        _segnala_riavvio(hass)


async def async_create_fix_flow(
    hass: HomeAssistant, issue_id: str, data: dict[str, Any] | None
) -> RepairsFlow:
    if issue_id == ISSUE_RIAVVIO:
        return RiavvioFlow()
    if issue_id == ISSUE_PASSAGGIO:
        return PassaggioFlow()
    return ConfirmRepairFlow()
