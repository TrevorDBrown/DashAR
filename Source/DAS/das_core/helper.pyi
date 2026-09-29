#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2026 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       helper.pyi
#

from enum import IntEnum

class Constants:
    EXPECTED_CONFIGURATION_VERSION: str
    EXPECTED_DASHAR_VERSION: str

class Variables: ...

class SharedFunctions:
    @staticmethod
    def generate_object_id() -> str: ...
    @staticmethod
    def get_current_timestamp() -> float: ...
    @staticmethod
    def convert_dict_to_json(dict_to_convert: dict) -> str: ...

class ServiceMode(IntEnum):
    PRODUCTION: int
    DEBUG: int
    TEST: int
    INVALID: int

class SystemStatus(IntEnum):
    NOT_STARTED: int
    STARTING: int
    FAILED: int
    READY: int

class DefaultDataFormat(IntEnum):
    AMERICA: int

class DataSourceType(IntEnum):
    DATABASE: int
    DIRECT_FILE: int

class DatabaseStatements:
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
