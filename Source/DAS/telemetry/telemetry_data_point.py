#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2026 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       telemetry_data_point.py
#

"""Purpose:"""

import enum


class TelemetryDataPoint(enum.Enum):
    SPEED = "speed"
    RPMS = "rpms"
    FUEL_PERCENTAGE = "fuel_percentage"
