#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2026 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       configuration.pyi
#

import argparse
from das_core.das_extensions import DASExtensions as DASExtensions
from das_core.helper import (
    Constants as Constants,
    ServiceMode as ServiceMode,
    SystemStatus as SystemStatus,
)
from das_core.obdii_interpreter import OBDIIContext as OBDIIContext
from typing import Final

class ConfigurationConstants:
    CONFIGURATION_VERSION: str
    DASHAR_VERSION: str
    DATA_PATH: Final[str]
    CONFIGURATION_PATH: Final[str]
    HUD_CONFIGURATION_PATH: Final[str]
    def __init__(self) -> None: ...

class ConfigurationVariables:
    system_status: SystemStatus
    das_server_port: int
    fuel_level_refresh_frequency_data_points: int
    service_mode: ServiceMode
    verbose_operation: bool
    obdii_elm327_device_path: str
    private_data_path: str
    database_path: str
    hud_configuration_base_path: str
    hud_configuration_default_path: str
    hud_configuration_custom_path: str
    hud_configuration_target: str
    hud_configuration_base_json_content: dict
    hud_configuration_widgets_json_content: dict
    das_extensions_path: str
    das_extensions: DASExtensions
    def __init__(self) -> None: ...

class Configuration:
    configuration_constants: ConfigurationConstants
    configuration_variables: ConfigurationVariables
    obdii_context: OBDIIContext
    def __init__(self, arguments: argparse.Namespace) -> None: ...
    def load_configuration(self, arguments: argparse.Namespace) -> None: ...
    def load_hud_configuration(self) -> None: ...
    def set_default_configuration(self) -> None: ...
    def test_configuration(self) -> bool: ...
