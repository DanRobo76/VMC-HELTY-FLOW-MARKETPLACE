"""Le entità sostitute (vedi __init__.py)."""

from __future__ import annotations

from datetime import time
from typing import Any

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.button import ButtonEntity
from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.components.select import SelectEntity
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.components.text import TextEntity, TextMode
from homeassistant.components.time import TimeEntity
from homeassistant.core import Event, EventStateChangedData, State, callback
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.util import dt as dt_util

from . import DOMINIO


class Sostituto(Entity):
    """Segue lo stato dell'entità di oggi."""

    _attr_should_poll = False

    def __init__(self, voce: dict[str, Any]) -> None:
        self.entity_id = voce["nuova"]
        self._vecchia = voce["vecchia"]
        self._nome = voce["nome"]
        self._stato: State | None = None

    @property
    def name(self) -> str:
        return self._attributo("friendly_name", self._nome)

    @property
    def icon(self) -> str | None:
        return self._attributo("icon")

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(
            async_track_state_change_event(self.hass, [self._vecchia], self._cambio)
        )
        self._stato = self.hass.states.get(self._vecchia)

    @callback
    def _cambio(self, evento: Event[EventStateChangedData]) -> None:
        self._stato = evento.data["new_state"]
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        return self._stato is not None and self._stato.state != "unavailable"

    def _attributo(self, nome: str, predefinito: Any = None) -> Any:
        return (
            self._stato.attributes.get(nome, predefinito)
            if self._stato
            else predefinito
        )

    async def _chiama(self, dominio: str, servizio: str, **dati: Any) -> None:
        await self.hass.services.async_call(
            dominio,
            servizio,
            {"entity_id": self._vecchia, **dati},
            blocking=True,
            context=self._context,
        )


class InterruttoreSostituto(Sostituto, SwitchEntity):
    @property
    def is_on(self) -> bool | None:
        return None if self._stato is None else self._stato.state == "on"

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self._chiama("input_boolean", "turn_on")

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self._chiama("input_boolean", "turn_off")


class SpiaSostituta(Sostituto, BinarySensorEntity):
    @property
    def is_on(self) -> bool | None:
        return None if self._stato is None else self._stato.state == "on"


class NumeroSostituto(Sostituto, NumberEntity):
    @property
    def native_value(self) -> float | None:
        try:
            return float(self._stato.state) if self._stato else None
        except ValueError:
            return None

    @property
    def native_min_value(self) -> float:
        return float(self._attributo("min", 0))

    @property
    def native_max_value(self) -> float:
        return float(self._attributo("max", 100))

    @property
    def native_step(self) -> float:
        return float(self._attributo("step", 1))

    @property
    def mode(self) -> NumberMode:
        return NumberMode(self._attributo("mode", "auto"))

    @property
    def native_unit_of_measurement(self) -> str | None:
        return self._attributo("unit_of_measurement")

    async def async_set_native_value(self, value: float) -> None:
        await self._chiama("input_number", "set_value", value=value)


class SceltaSostituta(Sostituto, SelectEntity):
    @property
    def options(self) -> list[str]:
        return list(self._attributo("options", []))

    @property
    def current_option(self) -> str | None:
        return self._stato.state if self._stato else None

    async def async_select_option(self, option: str) -> None:
        await self._chiama("input_select", "select_option", option=option)


class TestoSostituto(Sostituto, TextEntity):
    @property
    def native_value(self) -> str | None:
        return self._stato.state if self._stato else None

    @property
    def native_min(self) -> int:
        return int(self._attributo("min", 0))

    @property
    def native_max(self) -> int:
        return int(self._attributo("max", 100))

    @property
    def pattern(self) -> str | None:
        return self._attributo("pattern")

    @property
    def mode(self) -> TextMode:
        return TextMode(self._attributo("mode", "text"))

    async def async_set_value(self, value: str) -> None:
        await self._chiama("input_text", "set_value", value=value)


class OraSostituta(Sostituto, TimeEntity):
    @property
    def native_value(self) -> time | None:
        try:
            return time.fromisoformat(self._stato.state) if self._stato else None
        except ValueError:
            return None

    async def async_set_value(self, value: time) -> None:
        await self._chiama("input_datetime", "set_datetime", time=value.isoformat())


class PulsanteSostituto(Sostituto, ButtonEntity):
    @property
    def available(self) -> bool:
        return True

    async def async_press(self) -> None:
        dominio, oggetto = self._vecchia.split(".", 1)
        if dominio == "script":
            await self._chiama("script", "turn_on")
        else:
            await self.hass.services.async_call(
                dominio, oggetto, {}, blocking=True, context=self._context
            )


class SensoreSostituto(Sostituto, SensorEntity):
    def __init__(self, voce: dict[str, Any]) -> None:
        super().__init__(voce)
        self._timer = self._vecchia.startswith("timer.")
        if self._timer:
            self._attr_device_class = SensorDeviceClass.TIMESTAMP

    @property
    def native_value(self) -> Any:
        if self._stato is None:
            return None
        if self._timer:
            fine = (
                self._attributo("finishes_at")
                if self._stato.state == "active"
                else None
            )
            return dt_util.parse_datetime(fine) if fine else None
        dominio = self._vecchia.split(".", 1)[0]
        if dominio == "input_number":
            try:
                return float(self._stato.state)
            except ValueError:
                return None
        return (
            self.hass.data[DOMINIO]["mappa"].get(self._stato.state) or self._stato.state
        )

    @property
    def native_unit_of_measurement(self) -> str | None:
        return self._attributo("unit_of_measurement")


CLASSI: dict[str, type[Sostituto]] = {
    "binary_sensor": SpiaSostituta,
    "button": PulsanteSostituto,
    "number": NumeroSostituto,
    "select": SceltaSostituta,
    "sensor": SensoreSostituto,
    "switch": InterruttoreSostituto,
    "text": TestoSostituto,
    "time": OraSostituta,
}


async def prepara(hass, piattaforma: str, async_add_entities) -> None:
    """Le entità sostitute di una piattaforma."""
    voci = [
        v
        for v in hass.data[DOMINIO]["voci"]
        if v["nuova"].split(".", 1)[0] == piattaforma
    ]
    async_add_entities([CLASSI[piattaforma](v) for v in voci])
