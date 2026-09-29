#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2026 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       obdii_interpreter.pyi
#

from das_core.data_connector import DataConnection as DataConnection
from das_core.helper import (
    DatabaseStatements as DatabaseStatements,
    DefaultDataFormat as DefaultDataFormat,
    ServiceMode as ServiceMode,
    SharedFunctions as SharedFunctions,
)

class OBDIIContext:
    def __init__(
        self,
        service_mode: ServiceMode,
        obdii_interface_device_path: str = "",
        database_path: str = "",
        fuel_level_max_data_points: int = 1000,
        auto_connect: bool = True,
    ) -> None: ...
    def __del__(self) -> None: ...
    def establish_connection(self) -> bool: ...
    def connection_status(self) -> str: ...
    def is_connected(self) -> bool: ...
    def available_commands(self) -> set: ...
    def capture_data_points(self) -> dict: ...

def main() -> None: ...
