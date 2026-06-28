"""Binary sensor platform for Oklyn: pump running state + auxiliaries in regulator mode."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import OklynAuxState
from .const import (
    AUX_MODE_REGULATOR,
    DEFAULT_AUX1_NAME,
    DEFAULT_AUX2_NAME,
    DEFAULT_AUX_MODE,
    DEVICE_ID,
    DOMAIN,
    OPT_AUX1_MODE,
    OPT_AUX1_NAME,
    OPT_AUX2_MODE,
    OPT_AUX2_NAME,
    OPT_ENABLE_AUX1,
    OPT_ENABLE_AUX2,
)
from .coordinator import OklynDataUpdateCoordinator
from .entity import OklynEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: OklynDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[BinarySensorEntity] = [OklynPumpRunningSensor(coordinator, entry)]

    if (
        entry.options.get(OPT_ENABLE_AUX1, True)
        and entry.options.get(OPT_AUX1_MODE, DEFAULT_AUX_MODE) == AUX_MODE_REGULATOR
    ):
        entities.append(OklynAuxBinarySensor(coordinator, entry, aux_id=1))

    if (
        entry.options.get(OPT_ENABLE_AUX2, True)
        and entry.options.get(OPT_AUX2_MODE, DEFAULT_AUX_MODE) == AUX_MODE_REGULATOR
    ):
        entities.append(OklynAuxBinarySensor(coordinator, entry, aux_id=2))

    async_add_entities(entities)


class OklynPumpRunningSensor(OklynEntity, BinarySensorEntity):
    """Binary sensor: is the pump actually running (real status, not commanded mode)."""

    _attr_translation_key = "pump_running"
    _attr_device_class = BinarySensorDeviceClass.RUNNING
    _attr_icon = "mdi:pump"
    _attr_unique_id = f"oklyn_{DEVICE_ID}_pump_running"

    @property
    def is_on(self) -> bool | None:
        if self.coordinator.data is None or self.coordinator.data.pump is None:
            return None
        return self.coordinator.data.pump.running

    @property
    def available(self) -> bool:
        return super().available and self.coordinator.data is not None and self.coordinator.data.pump is not None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        if self.coordinator.data is None or self.coordinator.data.pump is None:
            return {}
        pump = self.coordinator.data.pump
        return {
            "command": pump.command,
            "changed_at": pump.changed_at_iso,
        }


class OklynAuxBinarySensor(OklynEntity, BinarySensorEntity):
    """Read-only on/off state of an Oklyn auxiliary configured as a regulator."""

    _attr_device_class = BinarySensorDeviceClass.RUNNING

    def __init__(
        self,
        coordinator: OklynDataUpdateCoordinator,
        entry: ConfigEntry,
        aux_id: int,
    ) -> None:
        super().__init__(coordinator, entry)
        self._aux_id = aux_id
        # Same unique_id as the switch variant: switching the mode in the
        # options migrates the entity instead of creating a duplicate.
        self._attr_unique_id = f"oklyn_{DEVICE_ID}_aux{aux_id}"

    @property
    def name(self) -> str:
        if self._aux_id == 1:
            return self._entry.options.get(OPT_AUX1_NAME, DEFAULT_AUX1_NAME)
        return self._entry.options.get(OPT_AUX2_NAME, DEFAULT_AUX2_NAME)

    def _aux_state(self) -> OklynAuxState | None:
        data = self.coordinator.data
        if data is None:
            return None
        return data.aux1 if self._aux_id == 1 else data.aux2

    @property
    def is_on(self) -> bool:
        aux = self._aux_state()
        if aux is None or not aux.available:
            return False
        return aux.status == "on"

    @property
    def available(self) -> bool:
        if not super().available:
            return False
        aux = self._aux_state()
        return aux is not None and aux.available

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        aux = self._aux_state()
        if aux is None or not aux.available:
            return {}
        return {
            "command": aux.command,
            "status": aux.status,
            "changed_at": aux.changed_at_iso,
            "changed_at_raw": aux.changed_at_raw,
        }
