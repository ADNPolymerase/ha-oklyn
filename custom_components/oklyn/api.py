"""Oklyn API client."""
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal

import aiohttp

from .const import DEFAULT_BASE_URL, DEFAULT_TIMEOUT, DEVICE_ID

_LOGGER = logging.getLogger(__name__)

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class OklynError(Exception):
    """Base Oklyn error."""


class OklynAuthError(OklynError):
    """Authentication error (401/403)."""


class OklynConnectionError(OklynError):
    """Connection / network error."""


class OklynResponseError(OklynError):
    """Unexpected response from the API."""


class OklynEndpointUnavailable(OklynError):
    """Endpoint not available on this device (404 on optional endpoints)."""


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


def _parse_dt(raw: str | None) -> datetime | None:
    if not raw:
        return None
    try:
        return datetime.strptime(raw, DATETIME_FORMAT)
    except (ValueError, TypeError):
        return None


@dataclass
class OklynMeasure:
    value: float | None
    measured_at: datetime | None
    measured_at_raw: str | None = None

    @property
    def measured_at_iso(self) -> str | None:
        if self.measured_at:
            return self.measured_at.isoformat()
        return self.measured_at_raw


@dataclass
class OklynPumpState:
    command: Literal["auto", "on", "off"] | None
    status: Literal["on", "off"] | None
    changed_at: datetime | None
    changed_at_raw: str | None = None

    @property
    def running(self) -> bool:
        return self.status == "on"

    @property
    def in_transition(self) -> bool:
        if self.command == "auto":
            return False
        return self.command != self.status

    @property
    def changed_at_iso(self) -> str | None:
        if self.changed_at:
            return self.changed_at.isoformat()
        return self.changed_at_raw


@dataclass
class OklynAuxState:
    command: Literal["on", "off"] | None
    status: Literal["on", "off"] | None
    changed_at: datetime | None
    changed_at_raw: str | None = None
    available: bool = True

    @property
    def in_transition(self) -> bool:
        return self.command != self.status

    @property
    def changed_at_iso(self) -> str | None:
        if self.changed_at:
            return self.changed_at.isoformat()
        return self.changed_at_raw


@dataclass
class OklynData:
    ph: OklynMeasure | None
    orp: OklynMeasure | None
    water: OklynMeasure | None
    air: OklynMeasure | None
    salt: OklynMeasure | None
    pump: OklynPumpState | None
    aux1: OklynAuxState | None
    aux2: OklynAuxState | None
    endpoint_errors: dict[str, str] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# API client
# ---------------------------------------------------------------------------


class OklynApiClient:
    """Async client for the Oklyn public API."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        api_token: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        self._session = session
        self._api_token = api_token
        self._base_url = base_url.rstrip("/")
        self._timeout = aiohttp.ClientTimeout(total=timeout)

    # ------------------------------------------------------------------
    # Internal request helper
    # ------------------------------------------------------------------

    async def _async_request(
        self,
        method: str,
        endpoint: str,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        url = f"{self._base_url}/{endpoint.lstrip('/')}"
        headers = {"X-Api-Token": self._api_token}

        try:
            async with self._session.request(
                method,
                url,
                headers=headers,
                json=json,
                timeout=self._timeout,
            ) as resp:
                if resp.status in (401, 403):
                    raise OklynAuthError(f"Authentication failed: HTTP {resp.status}")

                if resp.status in (400, 404):
                    raise OklynEndpointUnavailable(
                        f"Endpoint not available (HTTP {resp.status}): {endpoint}"
                    )

                if resp.status in (408, 429, 500, 502, 503, 504):
                    raise OklynConnectionError(
                        f"Server error: HTTP {resp.status} on {endpoint}"
                    )

                if resp.status != 200:
                    raise OklynResponseError(
                        f"Unexpected HTTP {resp.status} on {endpoint}"
                    )

                try:
                    return await resp.json(content_type=None)
                except Exception as exc:
                    raise OklynResponseError(
                        f"Invalid JSON response from {endpoint}"
                    ) from exc

        except OklynError:
            raise
        except asyncio.TimeoutError as exc:
            raise OklynConnectionError(f"Timeout connecting to Oklyn API") from exc
        except aiohttp.ClientError as exc:
            raise OklynConnectionError(f"Network error: {exc}") from exc

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    async def async_validate_token(self) -> None:
        """Validate the API token by fetching pump state."""
        await self._async_request("GET", f"/device/{DEVICE_ID}/pump")

    # ------------------------------------------------------------------
    # Measures
    # ------------------------------------------------------------------

    async def async_get_measure(
        self,
        measure_type: Literal["ph", "orp", "water", "air", "salt"],
    ) -> OklynMeasure:
        data = await self._async_request(
            "GET", f"/device/{DEVICE_ID}/data/{measure_type}"
        )
        raw_ts = data.get("measured_at")
        return OklynMeasure(
            value=_safe_float(data.get("value")),
            measured_at=_parse_dt(raw_ts),
            measured_at_raw=raw_ts,
        )

    # ------------------------------------------------------------------
    # Pump
    # ------------------------------------------------------------------

    async def async_get_pump(self) -> OklynPumpState:
        data = await self._async_request("GET", f"/device/{DEVICE_ID}/pump")
        return _parse_pump(data)

    async def async_set_pump(
        self,
        mode: Literal["auto", "on", "off"],
    ) -> OklynPumpState:
        data = await self._async_request(
            "PUT", f"/device/{DEVICE_ID}/pump", json={"pump": mode}
        )
        return _parse_pump(data)

    # ------------------------------------------------------------------
    # Auxiliaries
    # ------------------------------------------------------------------

    async def async_get_aux(self, aux_id: Literal[1, 2]) -> OklynAuxState:
        endpoint = f"/device/{DEVICE_ID}/aux" if aux_id == 1 else f"/device/{DEVICE_ID}/aux2"
        data = await self._async_request("GET", endpoint)
        return _parse_aux(data)

    async def async_set_aux(
        self,
        aux_id: Literal[1, 2],
        state: Literal["on", "off"],
    ) -> OklynAuxState:
        endpoint = f"/device/{DEVICE_ID}/aux" if aux_id == 1 else f"/device/{DEVICE_ID}/aux2"
        key = "aux"
        data = await self._async_request("PUT", endpoint, json={key: state})
        return _parse_aux(data)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _safe_float(val: Any) -> float | None:
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def _parse_pump(data: dict[str, Any]) -> OklynPumpState:
    raw_ts = data.get("changed_at")
    return OklynPumpState(
        command=data.get("pump"),
        status=data.get("status"),
        changed_at=_parse_dt(raw_ts),
        changed_at_raw=raw_ts,
    )


def _parse_aux(data: dict[str, Any]) -> OklynAuxState:
    raw_ts = data.get("changed_at")
    return OklynAuxState(
        command=data.get("aux"),
        status=data.get("status"),
        changed_at=_parse_dt(raw_ts),
        changed_at_raw=raw_ts,
        available=True,
    )
