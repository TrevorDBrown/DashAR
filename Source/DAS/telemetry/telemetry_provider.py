#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2026 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       vehicle_telemetry_provider.py
#

"""Purpose: generic interface for vehicle telemetry, accessed by the DAS vehicle manager for the DashAR system."""

import abc


class TelemetryProvider(abc.ABC):
    """An abstract class representing vehicle telemetry data sources."""

    @abc.abstractmethod
    def connect(self):
        """Connect to the vehicle telemetry source."""
        ...

    @abc.abstractmethod
    def disconnect(self):
        """Disconnect from the vehicle telemetry source."""
        ...

    def get_speed(self) -> int:
        """Return the vehicle's current speed."""
        raise NotImplementedError("Speed is not supported by this provider.")

    def get_rpms(self) -> int:
        """Return the vehicle's current engine rotation speed."""
        raise NotImplementedError(
            "Engine Rotation Speed (RPMs) is not supported by this provider."
        )

    def get_fuel_level(self) -> float:
        """Return the vehicle's current fuel level."""
        raise NotImplementedError("Fuel level is not supported by this provider.")

    def get_gear(self):
        """Return the vehicle's current gear position."""
        raise NotImplementedError("Gear position is not supported by this provider.")


if __name__ == "__main__":
    print(
        f"This module ({__file__}) should be accessed through das_core/vehicle_manager.py."
    )
