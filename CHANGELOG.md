# Changelog

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
