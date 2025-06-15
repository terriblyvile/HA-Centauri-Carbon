from homeassistant.components.light import LightEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
) -> None:
    ws_client = hass.data[DOMAIN]
    async_add_entities([CentauriLightSwitch(ws_client)])


class CentauriLightSwitch(LightEntity):
    def __init__(self, ws_client):
        self._client = ws_client
        self._attr_name = "Chamber Light"
        self._attr_unique_id = "centauri_light"
        self._attr_is_on = False
        self._attr_supported_color_modes = {"onoff"}
        self._attr_color_mode = "onoff"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, "printer")},
            name="Elegoo Centauri Carbon",
            manufacturer="Elegoo",
            model="Centauri Carbon",
            configuration_url=f"http://{ws_client.ip}/network-device-manager/network/control"
        )

    @property
    def is_on(self):
        return self._attr_is_on

    async def async_turn_on(self, **kwargs):
        await self._client.send_command({
            "LightStatus": {
                "SecondLight": True,
                "RgbLight": [0, 0, 0]
            }
        })
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self._client.send_command({
            "LightStatus": {
                "SecondLight": False,
                "RgbLight": [0, 0, 0]
            }
        })
        self._attr_is_on = False
        self.async_write_ha_state()