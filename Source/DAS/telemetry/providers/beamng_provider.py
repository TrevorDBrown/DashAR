#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2026 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       beamng_provider.py
#

"""Purpose: provides BeamNG telemetry, accessed by the DAS vehicle manager for the DashAR system."""

from telemetry.telemetry_provider import TelemetryProvider


class BeamNGTelemetryProvider:
    def __init__(self):
        pass


if __name__ == "__main__":
    print(
        f"This module ({__file__}) should be accessed through das_core/vehicle_manager.py."
    )
