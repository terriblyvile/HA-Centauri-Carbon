from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN

SCAN_INTERVAL = timedelta(seconds=1)

SENSOR_TYPES = {
    "nozzle_temp": ["Temperature - Nozzle", "°C"],
    "bed_temp": ["Temperature - Bed", "°C"],
    "enclosure_temp": ["Temperature - Enclosure", "°C"],
#    "target_bed_temp": ["Temperature Target - Bed", "°C"],
#    "target_nozzle_temp": ["Temperature Target - Nozzle", "°C"],
    "z_offset": ["Z Offset", "mm"],
    "model_fan_speed": ["Fan Speed - Model", "%"],
    "aux_fan_speed": ["Fan Speed - Auxilliary", "%"],
    "box_fan_speed": ["Fan Speed - Enclosure", "%"],
    "progress": ["Print Progress", "%"],
    "print_status": ["Print Status", None],
    "current_layer": ["Current Layer", None],
    "total_layers": ["Total Layers", None],
    "print_speed_pct": ["Print Speed", "%"],
    "elapsed_time": ["Elapsed Print Time", None],
    "remaining_time": ["Remaining Print Time", None],
}

STATUS_ICONS = {
    "Idle": "mdi:printer",
    "Preparing": "mdi:printer-settings",
    "Printing": "mdi:printer-3d",
    "Print Complete": "mdi:check-circle",
}

STATUS_COLORS = {
    "Idle": "grey",
    "Preparing": "orange",
    "Printing": "blue",
    "Print Complete": "green",
}

SENSOR_ICONS = {
    "nozzle_temp": "mdi:thermometer",
    "bed_temp": "mdi:thermometer",
    "enclosure_temp": "mdi:home-thermometer",
    "target_bed_temp": "mdi:thermometer-lines",
    "target_nozzle_temp": "mdi:thermometer-lines",
    "z_offset": "mdi:arrow-expand-vertical",
    "model_fan_speed": "mdi:fan",
    "aux_fan_speed": "mdi:fan",
    "box_fan_speed": "mdi:fan",
    "progress": "mdi:progress-clock",
    "print_status": "mdi:printer-3d",
    "current_layer": "mdi:layers",
    "total_layers": "mdi:layers-outline",
    "print_speed_pct": "mdi:speedometer",
    "elapsed_time": "mdi:timer-sand",
    "remaining_time": "mdi:timer-sand-complete",
}

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
) -> None:
    ws_client = hass.data[DOMAIN]
    entities = []

    for sensor_key, (name, unit) in SENSOR_TYPES.items():
        entities.append(CentauriSensor(ws_client, sensor_key, name, unit))

    async_add_entities(entities, True)

class CentauriSensor(SensorEntity):
    def __init__(self, ws_client, key, name, unit):
        self._client = ws_client
        self._key = key
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._attr_unique_id = f"centauri_{key}"
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

    @property
    def icon(self):
        if self._key == "print_status":
            return STATUS_ICONS.get(self.native_value, "mdi:printer-alert")
        return SENSOR_ICONS.get(self._key, "mdi:information")

    @property
    def extra_state_attributes(self):
        if self._key == "print_status":
            return {"status_color": STATUS_COLORS.get(self.native_value, "red")}
        return None