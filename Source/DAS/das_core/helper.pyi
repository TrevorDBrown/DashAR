#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2026 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       helper.pyi
#

"""Purpose: the helper constants, variables, and functions used by the DAS API for the DashAR system."""

# pylint: skip-file

from enum import IntEnum
from typing import Final

class Constants:
    """
    Constants to be used throughout the DAS API. Constants are denoted through all uppercase variable names.
    """

    DASHAR_SPLASH: Final[str]
    DASHAR_COPYRIGHT: Final[str]
    EXPECTED_CONFIGURATION_VERSION: Final[str]
    EXPECTED_DASHAR_VERSION: Final[str]

class Variables:
    """
    Variables to be used throughout the DAS API. Not implemented.
    """

class SharedFunctions:
    """
    Functions that are used through the DAS API.
    """

    @staticmethod
    def generate_object_id() -> str: ...
    @staticmethod
    def get_current_timestamp() -> float: ...
    @staticmethod
    def convert_dict_to_json(dict_to_convert: dict) -> str: ...

class ServiceMode(IntEnum):
    """
    Special constants used to indicate the service mode of the system.
    """

    INVALID: int
    PRODUCTION: int
    EMULATE: int
    TEST: int
    BEAMNG: int

class SystemStatus(IntEnum):
    """
    Special constants used to indicate the status of the system.
    """

    FAILED: int
    NOT_STARTED: int
    STARTING: int
    READY: int
    BUSY: int

class DefaultDataFormat(IntEnum):
    """
    Special constants used to indicate the country where the system is being utilized.
    """

    AMERICA: int

class DataSourceType(IntEnum):
    """
    Special constants used to indicate the origin of metadata and configuration data for the system.
    """

    DATABASE: int
    DIRECT_FILE: int

class DatabaseStatements:
    """
    Prepared SQL that is used to interact with the SQLite database (when applicable).
    """

    @staticmethod
    def dashar_session_start(
        session_uuid: str, vin: str, session_start_timestamp: float
    ) -> str: ...
    @staticmethod
    def dashar_session_insert_data_point(
        session_data_point_uuid: str,
        session_uuid: str,
        session_data_point_timestamp: float,
        mph: float,
        rpm: float,
        fuel_level: float,
    ) -> str: ...
    @staticmethod
    def dashar_is_automobile_registered(vin: str) -> str: ...
    @staticmethod
    def dashar_register_automobile(
        vin: str,
        name: str,
        year: int,
        mileage: float,
        initial_capture_timestamp: float,
        last_modified_timestamp: float,
    ) -> str: ...
