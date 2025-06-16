from homeassistant.components.fan import FanEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.components.fan import FanEntity, FanEntityFeature
from .const import DOMAIN

FAN_CONFIGS = {
    "model_fan_speed": {
        "name": "Fan Speed - Model",
        "key": "ModelFan",
    },
    "aux_fan_speed": {
        "name": "Fan Speed - Auxiliary",
        "key": "AuxiliaryFan",
    },
    "box_fan_speed": {
        "name": "Fan Speed - Enclosure",
        "key": "BoxFan",
    },
}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    ws_client = hass.data[DOMAIN]
    entities = []

    for entity_key, config in FAN_CONFIGS.items():
        entities.append(CentauriFan(ws_client, entity_key, config["key"], config["name"]))

    async_add_entities(entities)

class CentauriFan(FanEntity):
    def __init__(self, ws_client, data_key, control_key, name):
        self._client = ws_client
        self._data_key = data_key
        self._control_key = control_key
        self._attr_name = name
        self._attr_unique_id = f"centauri_fan_{data_key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, "printer")},
            name="Elegoo Centauri Carbon",
            manufacturer="Elegoo",
            model="Centauri Carbon",
            configuration_url=f"http://{ws_client.ip}/network-device-manager/network/control"
        )

    @property
    def is_on(self):
        return self._client.data.get(self._data_key, 0) > 0

    @property
    def percentage(self):
        return self._client.data.get(self._data_key, 0)

    @property
    def supported_features(self):
        return FanEntityFeature.SET_SPEED

    @property
    def percentage_step(self):
        return 1

    async def async_turn_on(self, percentage: int = 100, **kwargs):
        await self._client.send_command({
            "TargetFanSpeed": {self._control_key: percentage}
        })

    async def async_turn_off(self, **kwargs):
        await self._client.send_command({
            "TargetFanSpeed": {self._control_key: 0}
        })

    async def async_set_percentage(self, percentage: int):
        await self._client.send_command({
            "TargetFanSpeed": {self._control_key: percentage}
        })