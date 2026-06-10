"""Switch platform for Oklyn auxiliaries."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import OklynAuxState
from .const import (
    DEFAULT_AUX1_NAME,
    DEFAULT_AUX2_NAME,
    DEVICE_ID,
    DOMAIN,
    OPT_AUX1_NAME,
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
    entities: list[OklynAuxSwitch] = []

    if entry.options.get(OPT_ENABLE_AUX1, True):
        entities.append(OklynAuxSwitch(coordinator, entry, aux_id=1))

    if entry.options.get(OPT_ENABLE_AUX2, True):
        entities.append(OklynAuxSwitch(coordinator, entry, aux_id=2))

    async_add_entities(entities)


class OklynAuxSwitch(OklynEntity, SwitchEntity):
    """Switch for an Oklyn auxiliary output."""

    def __init__(
        self,
        coordinator: OklynDataUpdateCoordinator,
        entry: ConfigEntry,
        aux_id: int,
    ) -> None:
        super().__init__(coordinator, entry)
        self._aux_id = aux_id
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
            "in_transition": aux.in_transition,
            "changed_at": aux.changed_at_iso,
            "changed_at_raw": aux.changed_at_raw,
        }

    async def async_turn_on(self, **kwargs: Any) -> None:
        _LOGGER.debug("Turning on aux%d", self._aux_id)
        await self.coordinator._client.async_set_aux(self._aux_id, "on")  # type: ignore[attr-defined]
        await self.coordinator.async_refresh_after_command()

    async def async_turn_off(self, **kwargs: Any) -> None:
        _LOGGER.debug("Turning off aux%d", self._aux_id)
        await self.coordinator._client.async_set_aux(self._aux_id, "off")  # type: ignore[attr-defined]
        await self.coordinator.async_refresh_after_command()
