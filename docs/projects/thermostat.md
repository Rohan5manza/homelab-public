# The Thermostat Wars: a room-aware heating controller

**Field:** Embedded systems · local IoT · home automation · feedback control

**Original article:** [The Thermostat Wars: Revenge of the Engineer](https://rohanmarar.substack.com/p/the-thermostat-wars-revenge-of-the), published October 22, 2026. This page is a technical summary of that complete first-person build story.

## The problem: one thermostat, very different rooms

My house had uneven heating. The living-room thermostat could only measure its immediate surroundings, while one bedroom became excessively hot and another stayed relatively cold.

I wanted the heating system to consider room-level measurements—not just the temperature near a single thermostat—without making the house dependent on experimental software for basic furnace operation.

## What I built

- **Honeywell T6 Pro Z-Wave thermostat** installed on an existing two-wire R/W heating circuit.
- **Zooz 800 Series Z-Wave USB controller** connected to my Ubuntu workstation, with **Z-Wave JS UI** bridging the thermostat to Home Assistant.
- **Two DIY sensing nodes**, each combining an **ESP8266 D1 Mini** and a **BME280** temperature/humidity/pressure sensor.
- **ESPHome**, hosted on Buffy, for firmware, sensor reporting and integration with Home Assistant over Wi-Fi.
- **Home Assistant**, also running on Buffy, to calculate a weighted room temperature and send thermostat setpoint requests.

There are **three temperature inputs**: living room (from the Honeywell itself), my bedroom, and my roommate's bedroom.

## The engineering chain

```text
Bedroom #1: BME280 → ESP8266 ── Wi-Fi / ESPHome ──┐
Bedroom #2: BME280 → ESP8266 ── Wi-Fi / ESPHome ──┤
                                                   ├→ Home Assistant
Living room: Honeywell T6 Pro ── Z-Wave JS UI ──────┘
                                                       │
                                                       ↓
                                                Weighted temperature
                                                + threshold rules
                                                       │
                                                       ↓
                                            Thermostat setpoint request
                                                       │
                                                       ↓
                                             Honeywell's own HVAC control
```

## Debugging the physical sensors

My early assemblies connected to Wi-Fi but failed to detect their BME280 sensors. ESPHome logs reported `BME280: Communication failed`; the I²C scanner initially found no devices. After replacing unreliable pin connections with proper soldered wiring, the scanner discovered the BME280 at address `0x76` and sensor readings appeared.

That failure taught me to debug hardware and software separately: working firmware and Wi-Fi do not guarantee a reliable electrical connection.

## The actual weighted-temperature design

I used the following weights:

| Room | Weight |
| --- | ---: |
| Living room | **20%** |
| My bedroom | **40%** |
| Roommate's bedroom | **40%** |

The calculation is:

`T_weighted = 0.20 × T_living + 0.40 × T_bedroom + 0.40 × T_roommate`

For **69°F**, **71°F** and **65°F**, respectively, this produces **68.2°F**. All inputs are converted to consistent units before the calculation.

## Heating decisions, hysteresis and boundaries

The starting target was **69°F** with a lower threshold of **68.5°F** and an upper threshold of **69.5°F**.

- Below the lower threshold, the automation can request a higher setpoint.
- Above the upper threshold, it requests the lower setpoint.
- Within the band, it generally leaves the requested setpoint unchanged.
- **If my bedroom reaches 72°F**, a higher-priority rule asks the system to reduce heating even when the weighted temperature is low.
- Requested setpoints in the initial design were bounded to **68–72°F**.
- The supervisory automation evaluates conditions approximately **every ten minutes**; this is not a guaranteed minimum furnace runtime.

The command is sent through Home Assistant's `climate.set_temperature` action, which changes the Honeywell thermostat's target. **The Honeywell still decides when to call for heat.** Lowering its target does not guarantee that the furnace instantly stops in every room.

## What happens if something fails?

The thermostat retains standalone operation without Buffy or Home Assistant. Home Assistant validates sensor values and, when running but given invalid measurements, can request a **68°F fallback setpoint**. This cannot substitute for a hardware safety system or guarantee that a thermostat will reset itself when the server goes offline.

## The completed result

The sensors, ESPHome, Z-Wave integration, weighted calculation and setpoint automation worked together. I confirmed commands through Home Assistant automation traces and the thermostat's reported state. This is a functioning **end-to-end integration**, not a claim of independently controlled HVAC zones or measured comfort improvements.

**Try it:** [Interactive thermostat controller](../../site/lab/index.html#control-lab) — change the room temperatures and inspect the resulting example decision.

**Read the full story:** [The Thermostat Wars: Revenge of the Engineer](https://rohanmarar.substack.com/p/the-thermostat-wars-revenge-of-the) includes the complete process, soldering failures, system setup and reflections.
