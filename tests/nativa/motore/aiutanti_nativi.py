"""Entità native minime al posto degli aiutanti: SOLO per le prove della fase 4.

Non sono le entità dell'integrazione (che non le usa): servono a confrontare, con
Home Assistant vero, un aiutante di oggi con l'entità del dominio di domani
(``test_aiutanti_confronto.py``) e a far girare il motore tradotto con la mappa dei nomi
contro entità native (``test_aiutanti_prototipo.py``).

Ogni entità fa il minimo che fa l'aiutante: stesso valore iniziale, stesso ripristino
dopo un riavvio, stessa scrittura dello stato. ``ScritturaNativa`` è il servizio con cui
il motore scrive interruttori e spie in una sola chiamata, con il contesto della
chiamata (le spie sono ``binary_sensor``: non hanno servizi propri).
"""

from __future__ import annotations

import asyncio
from collections import defaultdict
from collections.abc import Iterable
from datetime import datetime, time
from typing import Any

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.button import ButtonEntity
from homeassistant.components.number import NumberMode, RestoreNumber
from homeassistant.components.select import SelectEntity
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.components.text import TextEntity
from homeassistant.components.time import TimeEntity
from homeassistant.const import ATTR_ENTITY_ID, STATE_ON
from homeassistant.core import Context, HomeAssistant, ServiceCall, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.setup import async_setup_component
from homeassistant.util import dt as dt_util

DOMINIO_SCRITTURA = "nativa_prova"
"""Il dominio del servizio di prova con cui il motore scrive interruttori e spie."""


class _Base(Entity):
    """Identità di un'entità di prova: entity_id fisso, nome e icona dell'aiutante."""

    _attr_should_poll = False

    def __init__(self, entity_id: str, config: dict[str, Any] | None = None) -> None:
        self.entity_id = entity_id
        self._config = config or {}
        self._attr_unique_id = entity_id.split(".", 1)[1]
        self._attr_name = self._config.get("name")
        self._attr_icon = self._config.get("icon")


class _AccesoSpento(_Base, RestoreEntity):
    """Valore acceso/spento come ``input_boolean``: ``initial``, altrimenti l'ultimo
    stato, altrimenti spento."""

    _attr_is_on: bool | None

    def __init__(self, entity_id: str, config: dict[str, Any] | None = None) -> None:
        super().__init__(entity_id, config)
        self._attr_is_on = self._config.get("initial", False)

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        if self._config.get("initial") is not None:
            return
        stato = await self.async_get_last_state()
        self._attr_is_on = stato is not None and stato.state == STATE_ON

    @callback
    def imposta(self, acceso: bool, contesto: Context | None = None) -> None:
        """Scrive il valore con il contesto di chi lo cambia (come un servizio)."""
        if contesto is not None:
            self.async_set_context(contesto)
        self._attr_is_on = acceso
        self.async_write_ha_state()


class InterruttoreNativo(_AccesoSpento, SwitchEntity):
    """Un ``input_boolean`` che l'utente comanda: domani è uno ``switch``."""

    async def async_turn_on(self, **kwargs: Any) -> None:
        self.imposta(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        self.imposta(False)


class SpiaNativa(_AccesoSpento, BinarySensorEntity):
    """Un ``input_boolean`` solo mostrato e scritto dal motore: domani è un
    ``binary_sensor`` (senza servizi: lo scrive il motore con ``imposta``)."""


class NumeroNativo(_Base, RestoreNumber):
    """Un ``input_number``: domani è un ``number``."""

    def __init__(self, entity_id: str, config: dict[str, Any]) -> None:
        super().__init__(entity_id, config)
        # float come fa lo schema di input_number: un massimo intero oltre i 64 bit
        # (nel package c'è 10^22) non si può salvare nel registro delle entità
        self._attr_native_min_value = float(config["min"])
        self._attr_native_max_value = float(config["max"])
        self._attr_native_step = float(config.get("step", 1))
        self._attr_mode = NumberMode(config.get("mode", "slider"))
        self._attr_native_unit_of_measurement = config.get("unit_of_measurement")
        # float anche il valore: con un intero lo stato sarebbe «5», non «5.0»
        iniziale = config.get("initial")
        self._attr_native_value = None if iniziale is None else float(iniziale)

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        if self._attr_native_value is not None:
            return
        valore = None
        if (dati := await self.async_get_last_number_data()) is not None:
            valore = dati.native_value
        if (
            valore is not None
            and self.native_min_value <= valore <= self.native_max_value
        ):
            self._attr_native_value = valore
        else:
            self._attr_native_value = self.native_min_value

    async def async_set_native_value(self, value: float) -> None:
        self._attr_native_value = float(value)
        self.async_write_ha_state()


class SceltaNativa(_Base, SelectEntity, RestoreEntity):
    """Un ``input_select``: domani è un ``select``."""

    def __init__(self, entity_id: str, config: dict[str, Any]) -> None:
        super().__init__(entity_id, config)
        self._attr_options = list(config["options"])
        self._attr_current_option = config.get("initial")

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        if self._attr_current_option is not None:
            return
        stato = await self.async_get_last_state()
        if stato is None or stato.state not in self.options:
            self._attr_current_option = self.options[0]
        else:
            self._attr_current_option = stato.state

    async def async_select_option(self, option: str) -> None:
        self._attr_current_option = option
        self.async_write_ha_state()


class TestoNativo(_Base, TextEntity, RestoreEntity):
    """Un ``input_text``: domani è un ``text``."""

    __test__ = False  # non è una classe di prove di pytest

    def __init__(self, entity_id: str, config: dict[str, Any] | None = None) -> None:
        super().__init__(entity_id, config)
        self._attr_native_min = self._config.get("min", 0)
        self._attr_native_max = self._config.get("max", 100)
        self._attr_pattern = self._config.get("pattern")
        self._attr_native_value = self._config.get("initial")

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        if self._attr_native_value is not None:
            return
        stato = await self.async_get_last_state()
        valore = stato.state if stato else None
        if valore is not None and self.native_min <= len(valore) <= self.native_max:
            self._attr_native_value = valore

    async def async_set_value(self, value: str) -> None:
        self._attr_native_value = value
        self.async_write_ha_state()


class OraNativa(_Base, TimeEntity, RestoreEntity):
    """Un ``input_datetime`` con la sola ora: domani è un ``time``."""

    def __init__(self, entity_id: str, config: dict[str, Any] | None = None) -> None:
        super().__init__(entity_id, config)
        iniziale = self._config.get("initial")
        self._attr_native_value = dt_util.parse_time(iniziale) if iniziale else None

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        if self._attr_native_value is not None:
            return
        stato = await self.async_get_last_state()
        vecchia = dt_util.parse_time(stato.state) if stato else None
        self._attr_native_value = vecchia or time(0, 0, 0)

    async def async_set_value(self, value: time) -> None:
        self._attr_native_value = value
        self.async_write_ha_state()


class ScadenzaNativa(_Base, SensorEntity):
    """Un ``timer``: domani è un sensore con l'istante di fine (o sconosciuto)."""

    _attr_device_class = SensorDeviceClass.TIMESTAMP

    @callback
    def imposta(self, fine: datetime | None, contesto: Context | None = None) -> None:
        if contesto is not None:
            self.async_set_context(contesto)
        self._attr_native_value = fine
        self.async_write_ha_state()


class PulsanteNativo(_Base, ButtonEntity):
    """Uno script o un comando che l'utente lancia: domani è un ``button``."""

    def __init__(self, entity_id: str, config: dict[str, Any] | None = None) -> None:
        super().__init__(entity_id, config)
        self.premute: list[Context | None] = []

    async def async_press(self) -> None:
        self.premute.append(self._context)


async def aggiungi(hass: HomeAssistant, entita: Iterable[Entity]) -> None:
    """Aggiunge le entità di prova ai componenti dei loro domini."""
    per_dominio: dict[str, list[Entity]] = defaultdict(list)
    for voce in entita:
        per_dominio[voce.entity_id.split(".", 1)[0]].append(voce)
    for dominio, voci in per_dominio.items():
        assert await async_setup_component(hass, dominio, {})
        await hass.data[dominio].async_add_entities(voci)


class ScritturaNativa:
    """I servizi ``nativa_prova.turn_on/turn_off/toggle``: il motore scrive interruttori
    e spie in una sola chiamata, con il contesto della chiamata, come
    ``input_boolean.turn_on`` su più aiutanti.

    Stessa forma di Home Assistant (``helpers/service.py``): un'entità sola è scritta
    subito, dentro la chiamata; più entità sono scritte ognuna in un suo compito
    (``asyncio.gather``), cioè al giro dopo del ciclo degli eventi. Così chi parte per
    lo stesso evento che ha fatto partire la chiamata si mette in fila come con gli
    aiutanti. L'ordine fra le entità è quello dell'elenco: Home Assistant le prende da un
    insieme, in un ordine che cambia a ogni avvio.

    Con ``subito=True`` anche più entità sono scritte dentro la chiamata, una dopo
    l'altra: la via più semplice, che però NON è quella di Home Assistant (lo mostra
    ``test_aiutanti_prototipo.py``).
    """

    def __init__(
        self,
        hass: HomeAssistant,
        entita: Iterable[_AccesoSpento],
        *,
        subito: bool = False,
    ) -> None:
        self.hass = hass
        self.subito = subito
        self.entita = {voce.entity_id: voce for voce in entita}
        self.mancanti: list[str] = []
        schema = cv.make_entity_service_schema({})
        for servizio in ("turn_on", "turn_off", "toggle"):
            hass.services.async_register(
                DOMINIO_SCRITTURA, servizio, self._scrivi, schema=schema
            )

    async def _scrivi(self, chiamata: ServiceCall) -> None:
        voci: list[_AccesoSpento] = []
        for entity_id in dict.fromkeys(chiamata.data.get(ATTR_ENTITY_ID, [])):
            if (voce := self.entita.get(entity_id)) is None:
                self.mancanti.append(entity_id)  # Home Assistant avvisa e continua
            else:
                voci.append(voce)

        async def una(voce: _AccesoSpento) -> None:
            if chiamata.service == "toggle":
                acceso = not voce.is_on
            else:
                acceso = chiamata.service == "turn_on"
            voce.imposta(acceso, chiamata.context)

        if len(voci) == 1 or self.subito:
            for voce in voci:
                await una(voce)
        else:
            await asyncio.gather(*(una(voce) for voce in voci))
