from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

NUMBER_CONFIG = {
    "target_nozzle_temp": {
        "name": "Target Nozzle Temp",
        "unit": "°C",
        "min": 0,
        "max": 320,
        "step": 1,
        "field": "TempTargetNozzle",
        "mode": "box",
    },
    "target_bed_temp": {
        "name": "Target Bed Temp",
        "unit": "°C",
        "min": 0,
        "max": 110,
        "step": 1,
        "field": "TempTargetHotbed",
        "mode": "box",
    },
}

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
) -> None:
    ws_client = hass.data[DOMAIN]
    entities = []

    for key, config in NUMBER_CONFIG.items():
        entities.append(CentauriTempTarget(ws_client, key, config))

    async_add_entities(entities)

class CentauriTempTarget(NumberEntity):
    def __init__(self, ws_client, key, config):
        self._client = ws_client
        self._key = key
        self._field = config["field"]

        self._attr_name = config["name"]
        self._attr_unique_id = f"centauri_number_{key}"
        self._attr_native_unit_of_measurement = config["unit"]
        self._attr_min_value = config["min"]
        self._attr_max_value = config["max"]
        self._attr_step = config["step"]
        self._attr_mode = config.get("mode", "auto")

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, "printer")},
            name="Elegoo Centauri Carbon",
            manufacturer="Elegoo",
            model="Centauri Carbon",
            configuration_url=f"http://{ws_client.ip}/network-device-manager/network/control"
        )

    @property
    def native_value(self):
        return self._client.data.get(self._key)

    async def async_set_native_value(self, value: float) -> None:
        await self._client.send_command({
            self._field: int(value)
        })