#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2026 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       obdii_provider.py
#

"""Purpose: provides OBDII telemetry, accessed by the DAS vehicle manager for the DashAR system."""

import obd

from telemetry.telemetry_provider import (
    TelemetryProvider,
)


class OBDIITelemetryProvider(TelemetryProvider):
    """Vehicle telemetry provider using an OBDII data source."""

    def __init__(self):
        pass


if __name__ == "__main__":
    print(
        f"This module ({__file__}) should be accessed through das_core/vehicle_manager.py."
    )
