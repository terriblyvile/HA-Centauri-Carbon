from homeassistant.components.mjpeg.camera import MjpegCamera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

CAMERA_NAME = "Centauri Camera"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    ip_address = entry.data["ip"]
    stream_url = f"http://{ip_address}:3031/video"

    async_add_entities([
        CentauriCamera(ip_address=ip_address, stream_url=stream_url)
    ])

class CentauriCamera(MjpegCamera):
    def __init__(self, ip_address: str, stream_url: str):
        super().__init__(
            mjpeg_url=stream_url,
            still_image_url=stream_url  # fallback to same stream for preview
        )

        self._attr_name = CAMERA_NAME
        self._attr_unique_id = "centauri_camera"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, "printer")},
            name="Elegoo Centauri Carbon",
            manufacturer="Elegoo",
            model="Centauri Carbon",
            configuration_url=f"http://{ip_address}/network-device-manager/network/control"
        )