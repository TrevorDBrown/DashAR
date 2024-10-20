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
import json
import argparse

from das_core.helper import Constants, SharedFunctions, ServiceMode
from das_core.obdii_interpreter import OBDIIContext

class ConfigurationConstants():
    CONFIGURATION_VERSION: str
    CONFIGURATION_PATH: Final[str] = os.path.join(os.getcwd(), "config.json")

    def __init__(self) -> None:
        return

class ConfigurationVariables():
    fuel_level_refresh_frequency_data_points: int = 200
    data_path: str = os.path.join(os.getcwd(), "data")
    database_path: str = os.path.join(data_path, "dashar-data.sqlite3")
    service_mode: ServiceMode
    headless_operation: bool = False
    verbose_operation: bool = False
    single_run_operation: bool = False

    obdii_elm327_device_path: str

    def __init__(self) -> None:
        return

class Configuration():
    configuration_constants: ConfigurationConstants
    configuration_variables: ConfigurationVariables

    obdii_context: OBDIIContext

    def __init__(self, arguments: argparse.Namespace) -> None:
        # Initialize Variables and Constants classes.
        self.configuration_variables = ConfigurationVariables()
        self.configuration_constants = ConfigurationConstants()

        # Splash Message.
        print(f"DashAR Automotive HUD System")
        print(f"DAS version {Constants.DASHAR_VERSION}")
        print(f"HUD version {Constants.HUD_VERSION}")
        print(f"Companion App version {Constants.COMPANION_APP_VERSION}")
        print(f"(c)2024 Trevor D. Brown. All rights reserved.\n")

        # Set defaults ahead of time.
        self.set_default_configuration()

        # Load configuration from file.
        # self.load_configuration(arguments)

        return

    def load_configuration(self, arguments: argparse.Namespace) -> None:

        # Check the arguments passed in.
        # Headless Mode.
        if (arguments.headless):
            self.configuration_variables.headless_operation = True
        else:
            self.configuration_variables.headless_operation = False

        if (arguments.verbose):
            self.configuration_variables.verbose_operation = True
        else:
            self.configuration_variables.verbose_operation = False

        if (arguments.single_run):
            self.configuration_variables.single_run_operation = True
        else:
            self.configuration_variables.single_run_operation = False

        # Load the configuration from JSON.
        json_configuration_content: dict

        with open(self.configuration_constants.CONFIGURATION_PATH, "r") as json_configuration:
            json_configuration_content = json.load(json_configuration)

        if (not json_configuration_content["config_version"]):
            print("No configuration file found. Using defaults.")

        else:
            if (json_configuration_content["config_version"]):
                self.configuration_constants.CONFIGURATION_VERSION = json_configuration_content["config_version"]

            if (json_configuration_content["service_mode"]):
                config_service_mode: str = json_configuration_content["service_mode"]

                #TODO: verify service mode from string into Enum.
                self.configuration_variables.service_mode = json_configuration_content["service_mode"]

            if (json_configuration_content["data_path"]):
                data_path_content: str = json_configuration_content["data_path"]

                if (data_path_content.find("{DAS_ROOT}") != -1):
                    data_path_content = data_path_content.replace("{DAS_ROOT}", os.getcwd())

                self.configuration_variables.data_path = os.path.abspath(data_path_content)

            if (json_configuration_content["database_path"]):
                database_path_content: str = json_configuration_content["database_path"]

                if (database_path_content.find("{DATA_PATH}") != -1):
                    database_path_content = database_path_content.replace("{DATA_PATH}", self.configuration_variables.data_path)

                self.configuration_variables.database_path = os.path.abspath(database_path_content)

            if (json_configuration_content["variables"]):
                for configuration_variable in json_configuration_content["variables"]:
                    if (configuration_variable["name"] == "FUEL_LEVEL_REFRESH_FREQUENCY_DATA_POINTS"):
                        self.configuration_variables.fuel_level_refresh_frequency_data_points = configuration_variable["value"]
                        continue

                    elif (configuration_variable["name"] == "OBDII_ELM327_DEVICE_PATH"):
                        self.configuration_variables.obdii_elm327_device_path = configuration_variable["value"]
                        continue

                    else:
                        print(f"Unknown variable: {configuration_variable['name']}. Skipping.")
                        continue

        # Validate the configuration provided.
        valid_configuration: bool = self.test_configuration()

        if (not valid_configuration):
            print("Error: invalid configuration provided. Resetting all values to defaults.")
            self.set_default_configuration()

        # Initialize the OBDII context.
        self.obdii_context = OBDIIContext(obdii_interface_device_path=self.configuration_variables.obdii_elm327_device_path, database_path=self.configuration_variables.database_path, service_mode=self.configuration_variables.service_mode)

        return

    def set_default_configuration(self) -> None:
        # Set default configuration, to be overwritten by the JSON config load process.
        self.configuration_constants.CONFIGURATION_VERSION = Constants.EXPECTED_CONFIGURATION_VERSION
        self.configuration_variables.fuel_level_refresh_frequency_data_points = 200
        self.configuration_variables.service_mode = ServiceMode.TEST
        self.configuration_variables.obdii_elm327_device_path = "/dev/tty.usbserial-D395GRKM"

    def test_configuration(self) -> bool:
        error_count: int = 0
        warning_count: int = 0

        print("Testing Configuration...")

        # Service Mode Verification
        print(f"Service Mode is: {self.configuration_variables.service_mode}")

        # Configuration Version Test
        if (self.configuration_constants.CONFIGURATION_VERSION == Constants.EXPECTED_CONFIGURATION_VERSION):
            print(f"Configuration Version ({self.configuration_constants.CONFIGURATION_VERSION}) is valid.")
        else:
            print(f"Warning: configuration version of file ({self.configuration_constants.CONFIGURATION_VERSION}) is older than the expected configuration version ({Constants.EXPECTED_CONFIGURATION_VERSION}). Please review configuration specification for changes.")
            warning_count += 1

        # Data Path Test
        if (os.path.isdir(self.configuration_variables.data_path)):
            print(f"Data Path ({self.configuration_variables.data_path}) exists.")
        else:
            print(f"Error: Data Path ({self.configuration_variables.data_path}) does not exist.")
            error_count += 1

        # Database Path Test
        if (os.path.isfile(self.configuration_variables.database_path)):
            print(f"SQLite Database ({self.configuration_variables.database_path}) exists.")
        else:
            print(f"Error: SQLite Database ({self.configuration_variables.database_path}) does not exist.")
            error_count += 1

        if (error_count > 0):
            # TODO: return value added values.
            print("Some tests failed.\n")
            return False

        print("All tests passed!\n")
        return True