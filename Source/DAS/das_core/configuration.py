#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       configuration.py
#   Purpose:    This script contains the DashAR configuration shared amongst multiple modules.
#

from typing import Final
import os
import json
import argparse

from das_core.helper import Constants, ServiceMode, SystemStatus
from das_core.obdii_interpreter import OBDIIContext
from das_core.das_extensions import DASExtensions

class ConfigurationConstants():
    CONFIGURATION_VERSION: str
    DASHAR_VERSION: str

    DATA_PATH: Final[str] = os.path.join(os.getcwd(), "data")
    CONFIGURATION_PATH: Final[str] = os.path.join(DATA_PATH, "config.json")
    HUD_CONFIGURATION_PATH: Final[str] = os.path.join(DATA_PATH, "hud")

    def __init__(self) -> None:
        return

class ConfigurationVariables():
    system_status: SystemStatus = SystemStatus.NOT_STARTED
    das_server_port: int = 8000
    fuel_level_refresh_frequency_data_points: int = 200
    service_mode: ServiceMode = ServiceMode.TEST
    verbose_operation: bool = False

    obdii_elm327_device_path: str = ""

    private_data_path: str = os.path.join(os.getcwd(), "private")
    database_path: str = os.path.join(private_data_path, "dashar-data.sqlite3")

    hud_configuration_base_path: str = os.path.join(ConfigurationConstants.HUD_CONFIGURATION_PATH, "base.json")
    hud_configuration_default_path: str = os.path.join(ConfigurationConstants.HUD_CONFIGURATION_PATH, "default.json")
    hud_configuration_custom_path: str = os.path.join(ConfigurationConstants.HUD_CONFIGURATION_PATH, "custom")

    hud_configuration_target: str = hud_configuration_default_path

    # hud_configuration_base_json_content: str = ""
    # hud_configuration_widgets_json_content: str = ""

    hud_configuration_base_json_content: dict = {}
    hud_configuration_widgets_json_content: dict = {}

    das_extensions_path: str = os.path.join(os.getcwd(), "extensions")
    das_extensions: DASExtensions = DASExtensions()

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

        # # Splash Message.
        print(f"DashAR Automotive HUD System")
        print(f"(c)2024-2025 Trevor D. Brown. Distributed under the MIT license.\n")

        # Set defaults ahead of time.
        self.set_default_configuration()

        # Load configuration from file.
        self.load_configuration(arguments)

        # Print remaining splash screen information.
        print(f"\nDashAR System version {self.configuration_constants.DASHAR_VERSION}")
        print(f"Configuration version {self.configuration_constants.CONFIGURATION_VERSION}")

        if (self.configuration_variables.system_status == SystemStatus.FAILED):
            print("\nError: configuration not loaded.")

        else:
            self.configuration_variables.system_status = SystemStatus.READY

        return

    def load_configuration(self, arguments: argparse.Namespace) -> None:

        print("Loading DAS configuration...")

        # Check the arguments passed in.
        # Verbose Output - output all information.
        if (arguments.verbose):
            self.configuration_variables.verbose_operation = True
        else:
            self.configuration_variables.verbose_operation = False

        # Load the DashAR DAS configuration from JSON.
        json_configuration_content: dict

        with open(self.configuration_constants.CONFIGURATION_PATH, "r") as json_configuration:
            json_configuration_content = json.load(json_configuration)

        if (not json_configuration_content["versioning"]["configuration"]):
            print("No configuration file found. Using defaults.")

        else:
            if (json_configuration_content["versioning"]):
                try:
                    self.configuration_constants.DASHAR_VERSION = json_configuration_content["versioning"]["dashar"]
                    self.configuration_constants.CONFIGURATION_VERSION = json_configuration_content["versioning"]["configuration"]

                except Exception as e:
                    print("Error: invalid versioning provided.")
                    self.configuration_constants.DASHAR_VERSION = "-1"
                    self.configuration_constants.CONFIGURATION_VERSION = "-1"

            if (json_configuration_content["service_mode"]):
                try:
                    self.configuration_variables.service_mode = ServiceMode[str(json_configuration_content["service_mode"]).upper()]
                except Exception as e:
                    print(f"Error: Service Mode '{json_configuration_content['service_mode']}' is not a valid service mode. Setting to default mode.")
                    self.configuration_variables.service_mode = ServiceMode.TEST
            else:
                self.configuration_variables.service_mode = ServiceMode["TEST"]

            if (json_configuration_content["private_data_path"]):
                private_data_path_content: str = json_configuration_content["private_data_path"]

                if (private_data_path_content.find("{DAS_ROOT}") != -1):
                    private_data_path_content = private_data_path_content.replace("{DAS_ROOT}", os.getcwd())

                self.configuration_variables.private_data_path = os.path.abspath(private_data_path_content)

            if (json_configuration_content["database_path"]):
                database_path_content: str = json_configuration_content["database_path"]

                if (database_path_content.find("{PRIVATE_DATA_PATH}") != -1):
                    database_path_content = database_path_content.replace("{PRIVATE_DATA_PATH}", self.configuration_variables.private_data_path)

                self.configuration_variables.database_path = os.path.abspath(database_path_content)

            if (json_configuration_content["extensions"]):
                for extension in json_configuration_content["extensions"]:
                    self.configuration_variables.das_extensions.register_extension(name=extension["name"], description=extension["description"], path=extension["path"], module=extension["module"], functions=extension["functions"])

            if (json_configuration_content["variables"]):
                for configuration_variable in json_configuration_content["variables"]:
                    if (configuration_variable["name"] == "FUEL_LEVEL_REFRESH_FREQUENCY_DATA_POINTS"):
                        self.configuration_variables.fuel_level_refresh_frequency_data_points = configuration_variable["value"]
                        continue

                    elif (configuration_variable["name"] == "OBDII_ELM327_DEVICE_PATH"):
                        self.configuration_variables.obdii_elm327_device_path = configuration_variable["value"]
                        continue

                    elif (configuration_variable["name"] == "DAS_SERVER_PORT"):
                        self.configuration_variables.das_server_port = configuration_variable["value"]
                        continue

                    else:
                        print(f"Unknown variable: {configuration_variable['name']}. Skipping.")
                        continue

        # Validate the configuration provided.
        valid_configuration: bool = self.test_configuration()

        if (not valid_configuration):
            print("\nError: invalid configuration provided. Resetting all values to defaults.")
            self.set_default_configuration()

        # Read in the HUD Configuration files.
        self.load_hud_configuration()

        # Initialize the OBDII context.
        self.obdii_context = OBDIIContext(obdii_interface_device_path=self.configuration_variables.obdii_elm327_device_path, database_path=self.configuration_variables.database_path, service_mode=self.configuration_variables.service_mode)

        if ((not self.obdii_context.is_connected()) and (not self.configuration_variables.service_mode == ServiceMode.TEST)):
            self.configuration_variables.service_mode = ServiceMode.INVALID
            self.configuration_variables.system_status = SystemStatus.FAILED
            return

        # Configuration is good, and the OBDII connection is established.
        self.configuration_variables.system_status = SystemStatus.READY

        return

    def load_hud_configuration(self) -> None:

        # HUD Configuration (Base)
        # Load the content of the HUD Configuration Base file.
        with open(self.configuration_variables.hud_configuration_base_path, "r") as f:
            self.configuration_variables.hud_configuration_base_json_content = json.load(f)

        # Verify if the "default.json" widgets configuration should be used, or a custom configuration.
        if (not self.configuration_variables.hud_configuration_base_json_content["targetConfiguration"]):
            print('Error: missing "targetConfiguration" in base.json. Using "default.json"')
            self.configuration_variables.hud_configuration_target = self.configuration_variables.hud_configuration_default_path

        if (self.configuration_variables.hud_configuration_base_json_content["targetConfiguration"] == "default.json"):
            # TODO: use a better method for making this determination.
            self.configuration_variables.hud_configuration_target = self.configuration_variables.hud_configuration_default_path
        else:
            self.configuration_variables.hud_configuration_target = os.path.join(self.configuration_variables.hud_configuration_custom_path, self.configuration_variables.hud_configuration_base_json_content["targetConfiguration"])

        # HUD Configuration (Widgets)
        with open(self.configuration_variables.hud_configuration_target, "r") as f:
            self.configuration_variables.hud_configuration_widgets_json_content = json.load(f)

        return

    def set_default_configuration(self) -> None:
        # Set default configuration, to be overwritten by the JSON config load process.
        self.configuration_constants.CONFIGURATION_VERSION = Constants.EXPECTED_CONFIGURATION_VERSION
        self.configuration_constants.DASHAR_VERSION = Constants.EXPECTED_DASHAR_VERSION
        self.configuration_variables.system_status = SystemStatus.STARTING
        self.configuration_variables.fuel_level_refresh_frequency_data_points = 200
        self.configuration_variables.service_mode = ServiceMode.TEST
        self.configuration_variables.obdii_elm327_device_path = "COM4"

    def test_configuration(self) -> bool:
        error_count: int = 0
        warning_count: int = 0

        print("\nTesting DAS Configuration...")

        # Service Mode Verification
        print(f"Service Mode is {self.configuration_variables.service_mode.name}.")

        # Configuration Version Test
        if (self.configuration_constants.CONFIGURATION_VERSION == Constants.EXPECTED_CONFIGURATION_VERSION):
            print(f"Configuration Version ({self.configuration_constants.CONFIGURATION_VERSION}) is valid.")
        else:
            print(f"Warning: configuration version of file ({self.configuration_constants.CONFIGURATION_VERSION}) differs from the expected configuration version ({Constants.EXPECTED_CONFIGURATION_VERSION}). Please review configuration specification for changes.")
            warning_count += 1

        # Data Path Test
        if (os.path.isdir(self.configuration_constants.DATA_PATH)):
            print(f"Data Path ({self.configuration_constants.DATA_PATH}) exists.")
        else:
            print(f"Error: Data Path ({self.configuration_constants.DATA_PATH}) does not exist.")
            error_count += 1

        # Private Data Path Test
        if (os.path.isdir(self.configuration_variables.private_data_path)):
            print(f"Private Data Path ({self.configuration_variables.private_data_path}) exists.")
        else:
            print(f"Error: Private Data Path ({self.configuration_variables.private_data_path}) does not exist.")
            error_count += 1

        # Database Path Test
        if (os.path.isfile(self.configuration_variables.database_path)):
            print(f"SQLite Database ({self.configuration_variables.database_path}) exists.")
        else:
            print(f"Error: SQLite Database ({self.configuration_variables.database_path}) does not exist.")
            error_count += 1

        # HUD Configuration Path Test
        if (os.path.isdir(self.configuration_constants.HUD_CONFIGURATION_PATH)):
            print(f"HUD Configuration Path ({self.configuration_constants.HUD_CONFIGURATION_PATH}) exists.")
        else:
            print(f"Error: HUD Configuration Path ({self.configuration_constants.HUD_CONFIGURATION_PATH}) does not exist.")
            error_count += 1

        # HUD Base Configuration Test
        if (os.path.isfile(self.configuration_variables.hud_configuration_base_path)):
            print(f"HUD Base Configuration ({self.configuration_variables.hud_configuration_base_path}) exists.")
        else:
            print(f"Error: HUD Base Configuration ({self.configuration_variables.hud_configuration_base_path}) does not exist.")
            error_count += 1

        # HUD Default Configuration Test
        if (os.path.isfile(self.configuration_variables.hud_configuration_default_path)):
            print(f"HUD Default Configuration ({self.configuration_variables.hud_configuration_default_path}) exists.")
        else:
            print(f"Error: HUD Default Configuration ({self.configuration_variables.hud_configuration_default_path}) does not exist.")
            error_count += 1

        # HUD Custom Configuration Path Test
        if (os.path.isdir(self.configuration_variables.hud_configuration_custom_path)):
            print(f"HUD Custom Configuration Path ({self.configuration_variables.hud_configuration_custom_path}) exists.")
        else:
            print(f"Error: HUD Custom Configuration Path ({self.configuration_variables.hud_configuration_custom_path}) does not exist.")
            error_count += 1

        # If any errors were found, report them.
        if (error_count > 0):
            # TODO: return value-added error values.
            print("Some tests failed.\n")
            return False

        print("All tests passed!\n")
        return True
