"""Sensor platform for Oklyn."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import OklynData, OklynMeasure
from .const import (
    DEVICE_ID,
    DOMAIN,
    MODEL_ANALYSIS,
    MODEL_ANALYSIS_SALT,
    resolve_model,
)
from .coordinator import OklynDataUpdateCoordinator
from .entity import OklynEntity


@dataclass(frozen=True, kw_only=True)
class OklynSensorEntityDescription(SensorEntityDescription):
    data_key: str = ""


SENSOR_DESCRIPTIONS: tuple[OklynSensorEntityDescription, ...] = (
    OklynSensorEntityDescription(
        key=f"oklyn_{DEVICE_ID}_ph",
        translation_key="ph",
        data_key="ph",
        device_class=SensorDeviceClass.PH,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    OklynSensorEntityDescription(
        key=f"oklyn_{DEVICE_ID}_orp",
        translation_key="orp",
        data_key="orp",
        native_unit_of_measurement="mV",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    OklynSensorEntityDescription(
        key=f"oklyn_{DEVICE_ID}_water_temperature",
        translation_key="water_temperature",
        data_key="water",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    OklynSensorEntityDescription(
        key=f"oklyn_{DEVICE_ID}_air_temperature",
        translation_key="air_temperature",
        data_key="air",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    OklynSensorEntityDescription(
        key=f"oklyn_{DEVICE_ID}_salt",
        translation_key="salt",
        data_key="salt",
        native_unit_of_measurement="g/L",
        state_class=SensorStateClass.MEASUREMENT,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: OklynDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    model = resolve_model(entry.options)
    enabled_keys = {"water", "air"}
    if model in (MODEL_ANALYSIS, MODEL_ANALYSIS_SALT):
        enabled_keys |= {"ph", "orp"}
    if model == MODEL_ANALYSIS_SALT:
        enabled_keys.add("salt")
    async_add_entities(
        OklynSensor(coordinator, entry, description)
        for description in SENSOR_DESCRIPTIONS
        if description.data_key in enabled_keys
    )


class OklynSensor(OklynEntity, SensorEntity):
    """Oklyn measurement sensor."""

    entity_description: OklynSensorEntityDescription

    def __init__(
        self,
        coordinator: OklynDataUpdateCoordinator,
        entry: ConfigEntry,
        description: OklynSensorEntityDescription,
    ) -> None:
        super().__init__(coordinator, entry)
        self.entity_description = description
        self._attr_unique_id = description.key

    def _measure(self) -> OklynMeasure | None:
        data: OklynData | None = self.coordinator.data
        if data is None:
            return None
        return getattr(data, self.entity_description.data_key, None)

    @property
    def native_value(self) -> float | None:
        measure = self._measure()
        return measure.value if measure else None

    @property
    def available(self) -> bool:
        if not super().available:
            return False
        measure = self._measure()
        return measure is not None and measure.value is not None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        measure = self._measure()
        if not measure:
            return {}
        return {
            "measured_at": measure.measured_at_iso,
            "measured_at_raw": measure.measured_at_raw,
        }
