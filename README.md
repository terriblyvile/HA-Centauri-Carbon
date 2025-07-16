# **I have sold my Centauri Carbon, so I will not be able to make updates to this integration.**

This is an integration into Home Assistant that will allow you to add sensors, controls, and the camera for the Elegoo Centauri Carbon into Home Assistant via your local network.

![image](https://github.com/user-attachments/assets/35b886d5-1a51-46b8-921e-33a7854503e6)

# **Installation**

1. Install through [HACS](https://hacs.xyz/) by adding this repository as a custom repository, **or** manually copy the `custom_components/centauri_carbon` folder into your Home Assistant `custom_components` directory.
2. Restart Home Assistant.
3. Once restarted, add the integration as you normally would and input your local IP for the Centauri Carbon. The accepted format is `192.168.x.xxx` with no prefixes or slashes.

# **Currently Supported Sensors:**

- Centauri Camera
- Current Layer
- Total Layers
- Elapsed Print Time
- Remaining Print Time
- Print Progress
- Print Status
- Current Layer
- Total Layers
- Print Speed
- Z Offset
- Temperature - Nozzle
- Temperature - Bed
- Temperature - Enclosure
- Temperature Target - Bed
- Temperature Target - Nozzle
- Fan Speed - Model
- Fan Speed - Auxilliary
- Fan Speed - Enclosure

# **Currently Supported Controls:**

- Chamber Light
- Fan Speed - Model
- Fan Speed - Auxilliary
- Fan Speed - Enclosure
- Print Speed
- Target Bed Temperature
- Target Nozzle Temperature

Here is an example entities card for what I use.

type: entities
entities:
  - entity: sensor.print_status
  - entity: sensor.print_progress
  - entity: sensor.remaining_print_time
  - entity: sensor.elapsed_print_time
  - entity: sensor.current_layer
  - entity: sensor.total_layers
  - entity: sensor.z_offset
  - entity: light.chamber_light
  - entity: select.print_speed
  - entity: number.target_bed_temp
  - entity: number.target_nozzle_temp
  - entity: fan.fan_speed_model
  - entity: fan.fan_speed_auxiliary
  - entity: fan.fan_speed_enclosure
