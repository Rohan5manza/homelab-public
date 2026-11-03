"""A pure-Python teaching model of the published room-aware thermostat logic.

This is NOT an equipment controller. It cannot observe the Honeywell's actual
state, enforce minimum furnace runtime, or account for every Home Assistant
rule. Never attach this script to HVAC without proper safety engineering.
"""
from math import isfinite


def example_setpoint(living_f: float, bedroom_f: float, roommate_f: float):
    """Return (weighted_temp_F or None, requested_setpoint_F or None, explanation)."""
    temps = (living_f, bedroom_f, roommate_f)
    if not all(isinstance(t, (int, float)) and isfinite(t) and 32 <= t <= 110 for t in temps):
        return None, 68.0, 'Missing or implausible measurement: fallback setpoint'

    weighted = 0.20 * living_f + 0.40 * bedroom_f + 0.40 * roommate_f
    if bedroom_f >= 72.0:
        return weighted, 68.0, 'Bedroom overheat limit takes priority'
    if weighted < 68.5:
        return weighted, max(68.0, min(72.0, living_f + 2.0)), 'Request more heat'
    if weighted > 69.5:
        return weighted, 68.0, 'Request less heat'
    return weighted, None, 'Hold current setpoint'


if __name__ == '__main__':
    print(example_setpoint(living_f=69.0, bedroom_f=71.0, roommate_f=65.0))
    print(example_setpoint(living_f=69.0, bedroom_f=73.0, roommate_f=65.0))
