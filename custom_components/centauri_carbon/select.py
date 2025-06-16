from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN

PRINT_SPEED_PRESETS = {
    "Silent": 50,
    "Balanced": 100,
    "Sport": 130,
    "Ludicrous": 160
}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    ws_client = hass.data[DOMAIN]
    async_add_entities([CentauriPrintSpeedSelect(ws_client)])

class CentauriPrintSpeedSelect(SelectEntity):
    def __init__(self, ws_client):
        self._client = ws_client
        self._attr_name = "Print Speed"
        self._attr_unique_id = "centauri_print_speed_mode"
        self._attr_options = list(PRINT_SPEED_PRESETS.keys())
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, "printer")},
            name="Elegoo Centauri Carbon",
            manufacturer="Elegoo",
            model="Centauri Carbon",
            configuration_url=f"http://{ws_client.ip}/network-device-manager/network/control"
        )

    @property
    def current_option(self):
        current_pct = self._client.data.get("print_speed_pct", 100)
        for name, value in PRINT_SPEED_PRESETS.items():
            if current_pct == value:
                return name
        return None

    async def async_select_option(self, option: str):
        value = PRINT_SPEED_PRESETS.get(option)
        if value is not None:
            await self._client.send_command({"PrintSpeedPct": value})