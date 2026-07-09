<p align="center">
  <img src="https://raw.githubusercontent.com/ADNPolymerase/ha-oklyn/main/custom_components/oklyn/brand/logo.png" alt="Oklyn" height="80">
</p>

# Oklyn for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/ADNPolymerase/ha-oklyn)
[![GitHub Release](https://badgen.net/github/release/ADNPolymerase/ha-oklyn)](https://github.com/ADNPolymerase/ha-oklyn/releases)
[![Hassfest](https://github.com/ADNPolymerase/ha-oklyn/actions/workflows/hassfest.yml/badge.svg)](https://github.com/ADNPolymerase/ha-oklyn/actions/workflows/hassfest.yml)
[![HA Version](https://img.shields.io/badge/Home%20Assistant-2024.1%2B-blue.svg)](https://www.home-assistant.io/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/ADNPolymerase/ha-oklyn/blob/main/LICENSE)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-support-yellow.svg?logo=buy-me-a-coffee)](https://buymeacoffee.com/adnpolymerase)

<a href="https://buymeacoffee.com/adnpolymerase" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-orange.png" alt="Buy Me A Coffee" height="60"></a>
<a href="https://adnpolymerase.github.io/HA/" target="_blank"><img src="https://raw.githubusercontent.com/ADNPolymerase/HA/main/assets/site-button.svg" alt="Link to my github.io for my other projects" height="60"></a>

Custom integration for the **Oklyn** pool controller, published via HACS.

> 🇫🇷 [Lire en français](README.fr.md)

> 🎴 **Companion card available:** [Oklyn Card](https://github.com/ADNPolymerase/oklyn-card) — a dedicated Lovelace card with pH/RedOx thresholds, pump control, auxiliaries and pH calibration. No dependency, full visual editor.
> [![Open in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ADNPolymerase&repository=oklyn-card&category=plugin)

---

## Features

- **pH, ORP/RedOx (mV), water & air temperature, salt (g/L, Salt model)** sensors — with an Oklyn alert `status` attribute (`normal` / `low` / `high`) used by [Oklyn Card](https://github.com/ADNPolymerase/oklyn-card) for color coding.
- **Pump mode** select (`auto` / `on` / `off`) and **pump running** binary sensor (real electrical state, independent from the command).
- **Auxiliary 1 and 2** switches.
- Full UI configuration, cloud polling (`api.oklyn.fr`), re-authentication flow, diagnostics support (token never exposed), French/English/Russian translations.

---

## Installation (HACS)

1. HACS → **⋮** → **Custom repositories** → `https://github.com/ADNPolymerase/ha-oklyn`, category **Integration**.
2. Download **Oklyn**, restart Home Assistant.
3. **Settings → Devices & Services → Add Integration** → search for **Oklyn**.

Manual alternative: copy `custom_components/oklyn/` into `config/custom_components/`, restart, then add the integration.

---

## Configuration

Setup asks for a device name (optional) and your **API token** — found in the Oklyn app under **My Account → API Key**. The device ID is always `my`.

---

## Options

After setup, go to **Settings → Devices & Services → Oklyn → Configure** to adjust:

| Option | Default | Description |
|---|---|---|
| Oklyn model | Filtration + Analysis | Your controller model — determines which sensors are created (see below) |
| Polling interval | 60 s | How often the API is queried (30 / 60 / 120 / 300 s) |
| Enable Auxiliary 1 | Yes | Create the Aux 1 switch entity |
| Enable Auxiliary 2 | Yes | Create the Aux 2 switch entity |
| Auxiliary 1 name | Auxiliaire 1 | Custom name for the Aux 1 switch |
| Auxiliary 2 name | Auxiliaire 2 | Custom name for the Aux 2 switch |

The three models match the [official lineup](https://www.oklyn.fr/assistant-piscine-connecte/): **Filtration** (temperatures, pump, auxiliaries), **+ Analysis** (adds pH, RedOx), **+ Salt** (adds salt g/L). Changes take effect immediately.

---

## Entities

| Entity | Type | Description |
|---|---|---|
| `sensor.oklyn_ph` | Sensor | pH value (Analysis models) — `status` attribute: `normal` / `low` / `high` |
| `sensor.oklyn_redox` | Sensor | ORP / RedOx in mV (Analysis models) — `status` attribute |
| `sensor.oklyn_water_temperature` | Sensor | Water temperature in °C — `status` attribute |
| `sensor.oklyn_air_temperature` | Sensor | Air temperature in °C |
| `sensor.oklyn_salt` | Sensor | Salt level in g/L (Salt model only) — `status` attribute |
| `binary_sensor.oklyn_pump_running` | Binary sensor | Real pump running state (device class `running`) |
| `select.oklyn_pump_mode` | Select | Pump command: auto / on / off |
| `switch.oklyn_auxiliaire_1` | Switch | Auxiliary output 1 |
| `switch.oklyn_auxiliaire_2` | Switch | Auxiliary output 2 |

---

## Screenshot

![Oklyn Card](https://raw.githubusercontent.com/ADNPolymerase/ha-oklyn/main/docs/oklyn-card.png)

---

## Example dashboard

The recommended way is the dedicated **[Oklyn Card](https://github.com/ADNPolymerase/oklyn-card)** (see above). Two ready-to-use YAML examples are also provided: [`examples/dashboard.yaml`](examples/dashboard.yaml) (native cards only) and [`examples/dashboard-bubble.yaml`](examples/dashboard-bubble.yaml) (requires Bubble Card + Pool Monitor Card from HACS). Paste them via **Dashboard → ✏️ Edit → ⋮ → Raw configuration editor** and adjust entity IDs if needed.

---

## Important behavior

The Oklyn API distinguishes the **command** (`pump` = `auto`/`on`/`off`, `aux` = `on`/`off`) from the **real state** (`status`). In `auto` mode the controller manages the schedule internally, so `status` can differ from the command — this is normal. The pump select shows the command and exposes `status` / `running` / `in_transition` as attributes; the aux switches reflect the real state, with brief command/status discrepancies exposed as `in_transition`. After each command, data is refreshed immediately, then again ~6 s later to capture the transition.

---

## Troubleshooting

- **Invalid auth** — token rejected: **Settings → Devices & Services → Oklyn → ⋮ → Re-authenticate**.
- **Cannot connect** — the Oklyn API is unreachable; check your connection and the Oklyn service status.
- **Auxiliary 2 unavailable** — some models have no second output (404 → entity marked unavailable); disable it in Options.
- **Entities stuck on "Unavailable"** — check the logs (filter on `oklyn`), or enable debug logging: `logger: logs: custom_components.oklyn: debug`.

---

## Privacy & limitations

The API token is stored encrypted, never logged, never exposed in attributes, and redacted in diagnostics. Single device only (`/device/my`), cloud polling (no local API or push), Aux 2 not present on all hardware revisions, API timestamps are timezone-naive.

---

## Contributing

Issues and pull requests welcome at <https://github.com/ADNPolymerase/ha-oklyn/issues>.
