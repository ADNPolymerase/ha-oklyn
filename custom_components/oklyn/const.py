"""Constants for the Oklyn integration."""
from __future__ import annotations

DOMAIN = "oklyn"

DEFAULT_NAME = "Oklyn"
DEFAULT_BASE_URL = "https://api.oklyn.fr/public/v1"
DEFAULT_TIMEOUT = 10
DEFAULT_SCAN_INTERVAL = 60

DEVICE_ID = "my"

CONF_API_TOKEN = "api_token"

OPT_SCAN_INTERVAL = "scan_interval"
OPT_ENABLE_AUX1 = "enable_aux1"
OPT_ENABLE_AUX2 = "enable_aux2"
OPT_AUX1_NAME = "aux1_name"
OPT_AUX2_NAME = "aux2_name"

DEFAULT_ENABLE_AUX1 = True
DEFAULT_ENABLE_AUX2 = True
DEFAULT_AUX1_NAME = "Auxiliaire 1"
DEFAULT_AUX2_NAME = "Auxiliaire 2"

SCAN_INTERVAL_OPTIONS = [30, 60, 120, 300]

PUMP_MODES = ["auto", "on", "off"]
AUX_STATES = ["on", "off"]

PLATFORMS = ["sensor", "select", "switch"]

MANUFACTURER = "Oklyn"
MODEL = "Oklyn Pool Controller"
CONFIGURATION_URL = "https://app.oklyn.fr"
