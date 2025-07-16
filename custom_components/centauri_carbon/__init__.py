from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .ws_client import CentauriWebSocketClient
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    ws_client = CentauriWebSocketClient(hass, entry.data["ip"])
    hass.data[DOMAIN] = ws_client
    hass.loop.create_task(ws_client.connect())

    await hass.config_entries.async_forward_entry_setups(
        entry, ["sensor", "camera", "fan", "light", "number", "select"]
    )
    return True