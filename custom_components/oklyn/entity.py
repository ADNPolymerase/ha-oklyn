"""Base entity for Oklyn."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONFIGURATION_URL,
    DEVICE_ID,
    DOMAIN,
    MANUFACTURER,
    MODEL,
)
from .coordinator import OklynDataUpdateCoordinator


class OklynEntity(CoordinatorEntity[OklynDataUpdateCoordinator]):
    """Base class for Oklyn entities."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: OklynDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        super().__init__(coordinator)
        self._entry = entry

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, DEVICE_ID)},
            name=self._entry.title,
            manufacturer=MANUFACTURER,
            model=MODEL,
            configuration_url=CONFIGURATION_URL,
        )

    @property
    def available(self) -> bool:
        return super().available and self.coordinator.data is not None
