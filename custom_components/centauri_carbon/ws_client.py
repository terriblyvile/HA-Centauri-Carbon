import aiohttp
import json
import logging
import uuid
import time

_LOGGER = logging.getLogger(__name__)

class CentauriWebSocketClient:
    def __init__(self, hass, ip_address):
        self._hass = hass
        self._ws = None
        self.data = {}
        self.ip = ip_address
        self.url = f"ws://{ip_address}:3030/websocket"

    async def connect(self):
        session = aiohttp.ClientSession()
        try:
            self._ws = await session.ws_connect(self.url)
            _LOGGER.info("Connected to Centauri WebSocket")

            async for msg in self._ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    payload = json.loads(msg.data)
                    _LOGGER.debug(f"Received WS payload: {payload}")
                    self._handle_message(payload)
        except Exception as e:
            _LOGGER.error(f"WebSocket connection failed: {e}")
        finally:
            await session.close()

    async def send_command(self, data: dict):
        if not self._ws or self._ws.closed:
            _LOGGER.warning("WebSocket is not connected. Cannot send command.")
            return

        command = {
            "Id": "",
            "Data": {
                "Cmd": 403,
                "Data": data,
                "RequestID": uuid.uuid4().hex,
                "MainboardID": "",
                "TimeStamp": int(time.time() * 1000),
                "From": 1
            }
        }

        try:
            await self._ws.send_json(command)
            _LOGGER.debug(f"Sent command: {command}")
        except Exception as e:
            _LOGGER.error(f"Failed to send command: {e}")

    def _handle_message(self, payload):
        try:
            status = payload.get("Status", {})
            print_info = status.get("PrintInfo", {})
            fan_speeds = status.get("CurrentFanSpeed", {})

            if not status and not print_info:
                _LOGGER.warning("Received payload missing expected status fields.")
                return

            progress = round(print_info.get("Progress", 0), 1)
            status_code = print_info.get("Status", 0)

            if status_code in [1, 16, 21]:
                printable_status = "Preparing"
            elif status_code == 13:
                printable_status = "Printing"
            elif status_code == 9:
                printable_status = "Print Complete"
            elif status_code == 0:
                printable_status = "Idle"
            else:
                printable_status = f"Unknown ({status_code})"

            elapsed_seconds = int(print_info.get("CurrentTicks", 0))
            total_seconds = int(print_info.get("TotalTicks", 0))
            remaining_seconds = max(0, total_seconds - elapsed_seconds)

            def format_duration(seconds):
                minutes, sec = divmod(seconds, 60)
                hours, min = divmod(minutes, 60)
                days, hr = divmod(hours, 24)
                if days > 0:
                    return f"{days}d {hr}h {min}m"
                elif hr > 0:
                    return f"{hr}h {min}m"
                else:
                    return f"{min}m"

            self.data.update({
                "nozzle_temp": round(status.get("TempOfNozzle", self.data.get("nozzle_temp", 0)), 1),
                "bed_temp": round(status.get("TempOfHotbed", self.data.get("bed_temp", 0)), 1),
                "enclosure_temp": round(status.get("TempOfBox", self.data.get("enclosure_temp", 0)), 1),
                "target_bed_temp": round(status.get("TempTargetHotbed", self.data.get("target_bed_temp", 0)), 1),
                "target_nozzle_temp": round(status.get("TempTargetNozzle", self.data.get("target_nozzle_temp", 0)), 1),
                "z_offset": round(status.get("ZOffset", self.data.get("z_offset", 0)), 3),
                "model_fan_speed": fan_speeds.get("ModelFan", self.data.get("model_fan_speed", 0)),
                "aux_fan_speed": fan_speeds.get("AuxiliaryFan", self.data.get("aux_fan_speed", 0)),
                "box_fan_speed": fan_speeds.get("BoxFan", self.data.get("box_fan_speed", 0)),
                "progress": progress,
                "print_status": printable_status,
                "current_layer": print_info.get("CurrentLayer", self.data.get("current_layer", 0)),
                "total_layers": print_info.get("TotalLayer", self.data.get("total_layers", 0)),
                "print_speed_pct": print_info.get("PrintSpeedPct", self.data.get("print_speed_pct", 100)),
                "elapsed_time": format_duration(elapsed_seconds),
                "remaining_time": format_duration(remaining_seconds),
            })

            _LOGGER.debug(f"Parsed data: {self.data}")
        except Exception as e:
            _LOGGER.warning(f"Error parsing WebSocket message: {e}")
