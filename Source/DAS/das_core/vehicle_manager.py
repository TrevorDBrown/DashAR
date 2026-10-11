#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2026 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       vehicle_manager.py
#

"""Purpose: manages vehicle-specific configurations and access to vehicle telemetry for the DashAR system."""

from telemetry.telemetry_provider import (
    TelemetryProvider,
)

from telemetry.telemetry_data_point import TelemetryDataPoint


class VehicleManager:
    _vehicle_telemetry_provider: TelemetryProvider

    def __init__(self, provider: TelemetryProvider):
        self._vehicle_telemetry_provider = provider

    def get_data(self, requested_data_points: list[str]) -> list[]:
        pass


if __name__ == "__main__":
    print(f"This module ({__file__}) should be invoked as an import.")
