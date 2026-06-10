"""DataUpdateCoordinator for Oklyn."""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    OklynApiClient,
    OklynAuthError,
    OklynAuxState,
    OklynConnectionError,
    OklynData,
    OklynEndpointUnavailable,
    OklynError,
    OklynMeasure,
    OklynPumpState,
)
from .const import (
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    OPT_ENABLE_AUX1,
    OPT_ENABLE_AUX2,
    OPT_SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


class OklynDataUpdateCoordinator(DataUpdateCoordinator[OklynData]):
    """Coordinate polling of all Oklyn endpoints."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        client: OklynApiClient,
        entry: ConfigEntry,
    ) -> None:
        self._client = client
        self._entry = entry
        scan_interval = entry.options.get(OPT_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )

    def update_scan_interval(self, seconds: int) -> None:
        self.update_interval = timedelta(seconds=seconds)

    async def _async_update_data(self) -> OklynData:
        enable_aux1 = self._entry.options.get(OPT_ENABLE_AUX1, True)
        enable_aux2 = self._entry.options.get(OPT_ENABLE_AUX2, True)
        endpoint_errors: dict[str, str] = {}

        async def safe_fetch(coro, key: str):
            try:
                return await coro
            except OklynAuthError as exc:
                raise ConfigEntryAuthFailed(str(exc)) from exc
            except OklynEndpointUnavailable as exc:
                _LOGGER.debug("Endpoint %s unavailable: %s", key, exc)
                endpoint_errors[key] = str(exc)
                return None
            except OklynError as exc:
                _LOGGER.warning("Error fetching %s: %s", key, exc)
                endpoint_errors[key] = str(exc)
                return None

        # Run all fetches in parallel; auth errors propagate immediately
        results = await asyncio.gather(
            safe_fetch(self._client.async_get_measure("ph"), "ph"),
            safe_fetch(self._client.async_get_measure("orp"), "orp"),
            safe_fetch(self._client.async_get_measure("water"), "water"),
            safe_fetch(self._client.async_get_measure("air"), "air"),
            safe_fetch(self._client.async_get_pump(), "pump"),
            safe_fetch(self._client.async_get_aux(1), "aux1") if enable_aux1 else _noop(),
            safe_fetch(self._client.async_get_aux(2), "aux2") if enable_aux2 else _noop(),
            return_exceptions=False,
        )

        ph, orp, water, air, pump, aux1, aux2 = results

        # If ALL primary endpoints failed, raise UpdateFailed
        if pump is None and ph is None and orp is None and water is None and air is None:
            raise UpdateFailed(
                f"All Oklyn endpoints failed: {endpoint_errors}"
            )

        # Mark unavailable aux
        if aux1 is None and enable_aux1:
            aux1 = _unavailable_aux()
        if aux2 is None and enable_aux2:
            aux2 = _unavailable_aux()

        return OklynData(
            ph=ph,
            orp=orp,
            water=water,
            air=air,
            pump=pump,
            aux1=aux1,
            aux2=aux2,
            endpoint_errors=endpoint_errors,
        )

    async def async_refresh_after_command(self, delay: float = 6.0) -> None:
        """Immediate refresh + a delayed one to capture real state."""
        await self.async_refresh()
        async def _delayed():
            await asyncio.sleep(delay)
            await self.async_refresh()
        self.hass.async_create_task(_delayed())


async def _noop():
    return None


def _unavailable_aux() -> OklynAuxState:
    return OklynAuxState(
        command=None,
        status=None,
        changed_at=None,
        available=False,
    )
