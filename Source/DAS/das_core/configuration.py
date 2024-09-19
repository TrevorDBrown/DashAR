#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024 Trevor D. Brown. All rights reserved.
#   This project is distributed under the MIT license.
#
#   File:       configuration.py
#   Purpose:    This script contains the DashAR configuration shared amongst multiple modules.
#

from typing import Final
import os

from das_core.helper import SharedFunctions, ServiceMode
from das_core.obdii_interpreter import OBDIIContext

class Constants():
    def __init__(self) -> None:
        return

class Variables():
    fuel_level_refresh_frequency_data_points: int = 200
    database_path: str = os.path.join(os.getcwd(), "data", "dashar-data.sqlite3")
    service_mode: ServiceMode
    obdii_elm327_device_path: str

    def __init__(self) -> None:
        return

class Configuration():
    CONFIG_PATH: Final[str] = os.path.join(os.getcwd(), "config.json")
    configuration_constants: Constants
    configuration_variables: Variables

    obdii_context: OBDIIContext

    def __init__(self) -> None:
        return

    def load_configuration(self) -> None:
        self.configuration_variables = Variables()

        self.configuration_variables.fuel_level_refresh_frequency_data_points = 200
        self.configuration_variables.service_mode = ServiceMode["DEBUG"]
        self.configuration_variables.obdii_elm327_device_path = "/dev/tty.usbserial-D395GRKM"

        print(f"The database path is: {self.configuration_variables.database_path}")

        self.obdii_context = OBDIIContext(obdii_interface_device_path=self.configuration_variables.obdii_elm327_device_path, database_path=self.configuration_variables.database_path, service_mode=self.configuration_variables.service_mode)

        return