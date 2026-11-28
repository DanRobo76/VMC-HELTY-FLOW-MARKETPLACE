"""Le sequenze del motore alla chiusura di Home Assistant.

Ogni sequenza di primo livello del motore (le automazioni e gli script del package) si
iscrive qui, nel registro dell'integrazione (uno per ``hass``, per le sequenze di tutte le
VMC), con le regole che Home Assistant 2026.11.2 usa per i propri script
(``helpers/script.py``: ``_async_stop_scripts_at_shutdown``,
``_async_stop_scripts_after_shutdown``, ``_SHUTDOWN_MAX_WAIT``; Apache-2.0, licenza nel
file ``LICENSE-Apache-2.0.txt`` dell'integrazione):

- alla chiusura (``homeassistant_stop``) si fermano le sequenze in corso partite prima della
  chiusura;
- 60 secondi dopo non ne parte più nessuna (``vietate``) e si fermano quelle ancora in
  corso, con un avviso.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import TYPE_CHECKING

from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.core import CALLBACK_TYPE, Event, HassJob, HomeAssistant, callback
from homeassistant.helpers.event import async_call_later
from homeassistant.util.async_ import create_eager_task
from homeassistant.util.hass_dict import HassKey

from .seguire import cambi_interni

if TYPE_CHECKING:
    from .esecuzione import Sequenza

_LOGGER = logging.getLogger(__name__)

ATTESA_MASSIMA = 60
"""I secondi dopo la chiusura oltre i quali nessuna sequenza parte più (come
``_SHUTDOWN_MAX_WAIT`` degli script)."""

_DATI: HassKey[RegistroSequenze] = HassKey("vmc_master_sequenze")


class RegistroSequenze:
    """Le sequenze di primo livello del motore, per fermarle alla chiusura."""

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self.vietate = False
        # sequenza -> partita prima della chiusura
        self._sequenze: dict[int, tuple[Sequenza, bool]] = {}
        cambi_interni(hass).ascolta(
            EVENT_HOMEASSISTANT_STOP, self._alla_chiusura, una_volta=True
        )

    @callback
    def iscrivi(self, sequenza: Sequenza) -> CALLBACK_TYPE:
        """Iscrive ``sequenza`` (come ``Script.__init__``); restituisce come toglierla
        (come ``Script.async_unload``)."""
        chiave = id(sequenza)
        self._sequenze[chiave] = (sequenza, not self.hass.is_stopping)

        @callback
        def togli() -> None:
            self._sequenze.pop(chiave, None)

        return togli

    async def _alla_chiusura(self, _evento: Event) -> None:
        """Come ``_async_stop_scripts_at_shutdown``. L'attesa finisce con Home
        Assistant (``cancel_on_shutdown``): se si ferma prima, non serve più."""
        async_call_later(
            self.hass,
            ATTESA_MASSIMA,
            HassJob(
                self._dopo_la_chiusura,
                "vmc_master: sequenze dopo la chiusura",
                cancel_on_shutdown=True,
            ),
        )
        in_corso = [s for s, prima in self._sequenze.values() if s.in_corso and prima]
        if in_corso:
            _LOGGER.debug(
                "Stopping scripts running at shutdown: %s",
                ", ".join(s.nome for s in in_corso),
            )
            await asyncio.gather(*(create_eager_task(s.ferma()) for s in in_corso))

    async def _dopo_la_chiusura(self, _istante: datetime) -> None:
        """Come ``_async_stop_scripts_after_shutdown``."""
        self.vietate = True
        in_corso = [s for s, _ in self._sequenze.values() if s.in_corso]
        if in_corso:
            _LOGGER.warning(
                "Stopping scripts running too long after shutdown: %s",
                ", ".join(s.nome for s in in_corso),
            )
            await asyncio.gather(
                *(create_eager_task(s.ferma(aggiorna=False)) for s in in_corso)
            )


@callback
def registro_sequenze(hass: HomeAssistant) -> RegistroSequenze:
    """Il registro delle sequenze del motore di ``hass``."""
    if (registro := hass.data.get(_DATI)) is None:
        registro = hass.data[_DATI] = RegistroSequenze(hass)
    return registro
