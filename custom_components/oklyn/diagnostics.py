"""Diagnostics support for Oklyn."""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_API_TOKEN, DOMAIN
from .coordinator import OklynDataUpdateCoordinator


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator: OklynDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    data = coordinator.data

    redacted_entry_data = {
        k: "**REDACTED**" if k == CONF_API_TOKEN else v
        for k, v in entry.data.items()
    }

    coordinator_data: dict[str, Any] = {}
    if data is not None:
        coordinator_data = {
            "ph": _measure_diag(data.ph),
            "orp": _measure_diag(data.orp),
            "water": _measure_diag(data.water),
            "air": _measure_diag(data.air),
            "pump": _pump_diag(data.pump),
            "aux1": _aux_diag(data.aux1),
            "aux2": _aux_diag(data.aux2),
            "endpoint_errors": data.endpoint_errors,
        }

    return {
        "entry": {
            "title": entry.title,
            "domain": entry.domain,
            "data": redacted_entry_data,
            "options": dict(entry.options),
            "version": entry.version,
        },
        "coordinator": coordinator_data,
    }


def _measure_diag(m: Any) -> dict[str, Any] | None:
    if m is None:
        return None
    return {
        "value": m.value,
        "measured_at": m.measured_at_iso,
    }


def _pump_diag(p: Any) -> dict[str, Any] | None:
    if p is None:
        return None
    return {
        "command": p.command,
        "status": p.status,
        "running": p.running,
        "in_transition": p.in_transition,
        "changed_at": p.changed_at_iso,
    }


def _aux_diag(a: Any) -> dict[str, Any] | None:
    if a is None:
        return None
    return {
        "command": a.command,
        "status": a.status,
        "in_transition": a.in_transition if a.available else None,
        "available": a.available,
        "changed_at": a.changed_at_iso,
    }
