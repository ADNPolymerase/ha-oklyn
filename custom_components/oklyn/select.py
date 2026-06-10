"""Select platform for Oklyn pump mode."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DEVICE_ID, DOMAIN, PUMP_MODES
from .coordinator import OklynDataUpdateCoordinator
from .entity import OklynEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: OklynDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([OklynPumpSelect(coordinator, entry)])


class OklynPumpSelect(OklynEntity, SelectEntity):
    """Select entity for pump mode (auto / on / off)."""

    _attr_unique_id = f"oklyn_{DEVICE_ID}_pump_mode"
    _attr_translation_key = "pump_mode"
    _attr_options = PUMP_MODES

    @property
    def current_option(self) -> str | None:
        if self.coordinator.data is None or self.coordinator.data.pump is None:
            return None
        return self.coordinator.data.pump.command

    @property
    def available(self) -> bool:
        if not super().available:
            return False
        return self.coordinator.data is not None and self.coordinator.data.pump is not None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        if self.coordinator.data is None or self.coordinator.data.pump is None:
            return {}
        pump = self.coordinator.data.pump
        return {
            "command": pump.command,
            "status": pump.status,
            "running": pump.running,
            "in_transition": pump.in_transition,
            "changed_at": pump.changed_at_iso,
            "changed_at_raw": pump.changed_at_raw,
        }

    async def async_select_option(self, option: str) -> None:
        if option not in PUMP_MODES:
            raise ValueError(f"Invalid pump mode: {option!r}. Valid: {PUMP_MODES}")
        _LOGGER.debug("Setting pump mode to %s", option)
        await self.coordinator._client.async_set_pump(option)  # type: ignore[attr-defined]
        await self.coordinator.async_refresh_after_command()
