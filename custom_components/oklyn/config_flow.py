"""Config flow for Oklyn."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .api import OklynApiClient, OklynAuthError, OklynConnectionError, OklynResponseError
from .const import (
    AUX_MODES,
    CONF_API_TOKEN,
    DEFAULT_AUX1_NAME,
    DEFAULT_AUX2_NAME,
    DEFAULT_AUX_MODE,
    DEFAULT_ENABLE_AUX1,
    DEFAULT_ENABLE_AUX2,
    DEFAULT_MODEL,
    DEFAULT_NAME,
    DEFAULT_SCAN_INTERVAL,
    DEVICE_ID,
    DOMAIN,
    OKLYN_MODELS,
    OPT_AUX1_MODE,
    OPT_AUX1_NAME,
    OPT_AUX2_MODE,
    OPT_AUX2_NAME,
    OPT_ENABLE_AUX1,
    OPT_ENABLE_AUX2,
    OPT_MODEL,
    OPT_SCAN_INTERVAL,
    SCAN_INTERVAL_OPTIONS,
    resolve_model,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
        vol.Required(CONF_API_TOKEN): str,
    }
)

MODEL_SELECTOR = SelectSelector(
    SelectSelectorConfig(
        options=OKLYN_MODELS,
        mode=SelectSelectorMode.DROPDOWN,
        translation_key="oklyn_model",
    )
)

STEP_OPTIONS_SCHEMA = vol.Schema(
    {
        vol.Optional(OPT_MODEL, default=DEFAULT_MODEL): MODEL_SELECTOR,
        vol.Optional(
            OPT_SCAN_INTERVAL, default=str(DEFAULT_SCAN_INTERVAL)
        ): vol.In([str(i) for i in SCAN_INTERVAL_OPTIONS]),
        vol.Optional(OPT_ENABLE_AUX1, default=DEFAULT_ENABLE_AUX1): bool,
        vol.Optional(OPT_AUX1_NAME, default=DEFAULT_AUX1_NAME): str,
        vol.Optional(OPT_AUX1_MODE, default=DEFAULT_AUX_MODE): vol.In(AUX_MODES),
        vol.Optional(OPT_ENABLE_AUX2, default=DEFAULT_ENABLE_AUX2): bool,
        vol.Optional(OPT_AUX2_NAME, default=DEFAULT_AUX2_NAME): str,
        vol.Optional(OPT_AUX2_MODE, default=DEFAULT_AUX_MODE): vol.In(AUX_MODES),
    }
)

REAUTH_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_TOKEN): str,
    }
)


class OklynConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle config flow for Oklyn."""

    VERSION = 1

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(DEVICE_ID)
            self._abort_if_unique_id_configured()

            user_input[CONF_API_TOKEN] = user_input[CONF_API_TOKEN].strip()
            error = await self._validate_token(user_input[CONF_API_TOKEN])
            if not error:
                self._data = user_input
                return await self.async_step_aux()
            errors["base"] = error

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_SCHEMA,
            errors=errors,
        )

    async def async_step_aux(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(
                title=self._data.get(CONF_NAME, DEFAULT_NAME),
                data={CONF_API_TOKEN: self._data[CONF_API_TOKEN]},
                options={
                    OPT_MODEL: user_input[OPT_MODEL],
                    OPT_SCAN_INTERVAL: int(user_input[OPT_SCAN_INTERVAL]),
                    OPT_ENABLE_AUX1: user_input[OPT_ENABLE_AUX1],
                    OPT_ENABLE_AUX2: user_input[OPT_ENABLE_AUX2],
                    OPT_AUX1_NAME: user_input[OPT_AUX1_NAME],
                    OPT_AUX2_NAME: user_input[OPT_AUX2_NAME],
                    OPT_AUX1_MODE: user_input[OPT_AUX1_MODE],
                    OPT_AUX2_MODE: user_input[OPT_AUX2_MODE],
                },
            )

        return self.async_show_form(
            step_id="aux",
            data_schema=STEP_OPTIONS_SCHEMA,
        )

    async def async_step_reauth(
        self, entry_data: dict[str, Any]
    ) -> ConfigFlowResult:
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            user_input[CONF_API_TOKEN] = user_input[CONF_API_TOKEN].strip()
            error = await self._validate_token(user_input[CONF_API_TOKEN])
            if not error:
                entry = self._get_reauth_entry()
                self.hass.config_entries.async_update_entry(
                    entry,
                    data={**entry.data, CONF_API_TOKEN: user_input[CONF_API_TOKEN]},
                )
                await self.hass.config_entries.async_reload(entry.entry_id)
                return self.async_abort(reason="reauth_successful")
            errors["base"] = error

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=REAUTH_SCHEMA,
            errors=errors,
        )

    async def _validate_token(self, api_token: str) -> str | None:
        """Return error key or None on success."""
        session = async_get_clientsession(self.hass)
        client = OklynApiClient(session, api_token)
        try:
            await client.async_validate_token()
        except OklynAuthError:
            return "invalid_auth"
        except OklynConnectionError:
            return "cannot_connect"
        except OklynResponseError:
            return "invalid_response"
        except Exception:
            _LOGGER.exception("Unexpected error during Oklyn token validation")
            return "unknown"
        return None

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OklynOptionsFlow:
        return OklynOptionsFlow(config_entry)


class OklynOptionsFlow(OptionsFlow):
    """Handle options flow for Oklyn."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        self._config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        options = self._config_entry.options

        if user_input is not None:
            user_input[OPT_SCAN_INTERVAL] = int(user_input[OPT_SCAN_INTERVAL])
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Optional(
                    OPT_MODEL,
                    default=resolve_model(options),
                ): MODEL_SELECTOR,
                vol.Optional(
                    OPT_SCAN_INTERVAL,
                    default=str(options.get(OPT_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)),
                ): vol.In([str(i) for i in SCAN_INTERVAL_OPTIONS]),
                vol.Optional(
                    OPT_ENABLE_AUX1,
                    default=options.get(OPT_ENABLE_AUX1, DEFAULT_ENABLE_AUX1),
                ): bool,
                vol.Optional(
                    OPT_ENABLE_AUX2,
                    default=options.get(OPT_ENABLE_AUX2, DEFAULT_ENABLE_AUX2),
                ): bool,
                vol.Optional(
                    OPT_AUX1_NAME,
                    default=options.get(OPT_AUX1_NAME, DEFAULT_AUX1_NAME),
                ): str,
                vol.Optional(
                    OPT_AUX1_MODE,
                    default=options.get(OPT_AUX1_MODE, DEFAULT_AUX_MODE),
                ): vol.In(AUX_MODES),
                vol.Optional(
                    OPT_AUX2_NAME,
                    default=options.get(OPT_AUX2_NAME, DEFAULT_AUX2_NAME),
                ): str,
                vol.Optional(
                    OPT_AUX2_MODE,
                    default=options.get(OPT_AUX2_MODE, DEFAULT_AUX_MODE),
                ): vol.In(AUX_MODES),
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)
