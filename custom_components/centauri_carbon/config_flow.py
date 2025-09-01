from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, CONF_IP

@config_entries.HANDLERS.register(DOMAIN)
class CentauriCarbonConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="Centauri Carbon", data={
                CONF_IP: user_input[CONF_IP]
            })

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_IP): str
            }),
            errors=errors
        )
