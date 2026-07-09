# Changelog

## [0.5.2] - 2026-07-09

### Added
- Russian translation (`translations/ru.json`).

## [0.4.0] - 2026-06-29

### Added
- **Pump running binary sensor** (`binary_sensor.oklyn_pump_running`, device class `running`):
  exposes the real pump state (is it actually filtering?) independently from the commanded
  mode (`select`). Useful for automations and dashboards — e.g. mode=`auto` but pump stopped.
- **Oklyn range status on sensors** (`status` attribute): the Oklyn API alert field
  (`"normal"` / `"high"` / `"low"`) is now exposed as an attribute on pH, RedOx,
  temperature and salt sensors.
- `integration_type: "device"` added to `manifest.json` (HA modern pattern).

### Fixed
- **Measurement timestamp was always `None`**: the Oklyn API returns the timestamp
  under the key `"recorded"`, not `"measured_at"`. The `measured_at` attribute on
  sensors now returns the correct value.

## [0.2.2] - 2026-06-10

### Fixed
- Scan interval dropdown now preselects the current value in the options flow
  (previously appeared empty) and defaults to 60 s at setup

## [0.2.1] - 2026-06-10

### Fixed
- Removed invalid "pH" unit on the pH sensor (device_class `ph` requires no unit;
  fixes the warning in Home Assistant logs)

## [0.2.0] - 2026-06-10

### Added
- Auxiliary type option: **switch** (controllable) or **regulator** (read-only,
  e.g. chlorine or temperature regulator)
- In regulator mode the auxiliary is exposed as a `binary_sensor` (running)
  instead of a `switch`
- Type selectable per auxiliary, at setup and in the options flow

## [0.1.3] - 2026-06-10

### Added
- Scan interval selectable during initial setup
- Aux 1/2 enable + custom names asked during initial setup
- Brand icon and logo (brands proxy API)

### Fixed
- HTTP 400 on unavailable aux endpoints no longer breaks the integration
- scan_interval validation error in options flow ("value must be one of [30, 60, 120, 300]")
- API token whitespace is now stripped before validation
- manifest version now matches the released version

## [0.1.0] - 2024-06-10

### Added
- Initial release
- pH sensor
- ORP / RedOx sensor
- Water temperature sensor
- Air temperature sensor
- Pump mode select (auto / on / off)
- Auxiliary 1 switch
- Auxiliary 2 switch
- Config flow UI (no YAML)
- Options flow (scan interval, aux enable/name)
- Re-authentication flow
- Diagnostics support
- French and English translations
