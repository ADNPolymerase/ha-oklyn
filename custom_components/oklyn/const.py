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
OPT_ENABLE_SALT = "enable_salt"  # legacy (v0.2.5-beta.1), migrated to OPT_MODEL
OPT_MODEL = "model"
OPT_AUX1_NAME = "aux1_name"
OPT_AUX2_NAME = "aux2_name"
OPT_AUX1_MODE = "aux1_mode"
OPT_AUX2_MODE = "aux2_mode"

MODEL_FILTRATION = "filtration"
MODEL_ANALYSIS = "analysis"
MODEL_ANALYSIS_SALT = "analysis_salt"
OKLYN_MODELS = [MODEL_FILTRATION, MODEL_ANALYSIS, MODEL_ANALYSIS_SALT]
DEFAULT_MODEL = MODEL_ANALYSIS

AUX_MODE_SWITCH = "switch"
AUX_MODE_REGULATOR = "regulator"
AUX_MODES = [AUX_MODE_SWITCH, AUX_MODE_REGULATOR]
DEFAULT_AUX_MODE = AUX_MODE_SWITCH

DEFAULT_ENABLE_AUX1 = True
DEFAULT_ENABLE_AUX2 = True
DEFAULT_AUX1_NAME = "Auxiliaire 1"
DEFAULT_AUX2_NAME = "Auxiliaire 2"


def resolve_model(options) -> str:
    """Return the configured Oklyn model, migrating legacy enable_salt."""
    model = options.get(OPT_MODEL)
    if model in OKLYN_MODELS:
        return model
    if options.get(OPT_ENABLE_SALT):
        return MODEL_ANALYSIS_SALT
    return DEFAULT_MODEL

SCAN_INTERVAL_OPTIONS = [30, 60, 120, 300]

PUMP_MODES = ["auto", "on", "off"]
AUX_STATES = ["on", "off"]

PLATFORMS = ["sensor", "select", "switch"]

MANUFACTURER = "Oklyn"
MODEL = "Oklyn Pool Controller"
CONFIGURATION_URL = "https://app.oklyn.fr"
