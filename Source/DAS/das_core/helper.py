#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       helper.py
#   Purpose:    This script contains helpers (constants, enums, functions, etc.) shared amongst multiple modules.
#

from enum import IntEnum
from uuid import uuid4
import datetime
import json

class Constants():
    EXPECTED_CONFIGURATION_VERSION: str = "0.2"
    EXPECTED_DASHAR_VERSION: str = "0.2"

class Variables():
    None

class SharedFunctions():
    @staticmethod
    def generate_object_id() -> str:
        # Generate a UUIDv4 for the calling object.
        return str(uuid4())

    @staticmethod
    def get_current_timestamp() -> float:
        return datetime.datetime.now(tz=datetime.timezone.utc).timestamp()

    @staticmethod
    def convert_dict_to_json(dict_to_convert: dict) -> str:
        return json.dumps(dict_to_convert)

class ServiceMode(IntEnum):
    PRODUCTION: int = 1     # PRODUCTION - the live system environment.
    DEBUG: int = 2          # DEBUG - like PRODUCTION, except an ELM327 emulator is attached.
    TEST: int = 3           # TEST - not a live system environment, values are generated using RNG.
    INVALID: int = 4        # INVALID - an error state where the system cannot be used.

class SystemStatus(IntEnum):
    NOT_STARTED: int = 1    # NOT_STARTED - the system has yet to initialize.
    STARTING: int = 2       # STARTING - the system is initializing.
    FAILED: int = 3         # FAILED - the system failed to initialize.
    READY: int = 4          # READY - the system is ready to run.

class DefaultDataFormat(IntEnum):
    AMERICA: int = 1

class DataSourceType(IntEnum):
    DATABASE: int = 1
    DIRECT_FILE: int = 2

class DatabaseStatements():
    @staticmethod
    def dashar_session_start(session_uuid: str, vin: str, session_start_timestamp: float) -> str:
        return f"INSERT INTO DASHAR_SESSION VALUES ('{session_uuid}', '{vin}', {session_start_timestamp})"

    @staticmethod
    def dashar_session_insert_data_point(session_data_point_uuid: str, session_uuid: str, session_data_point_timestamp: float, mph: float, rpm: float, fuel_level: float) -> str:
        return f"INSERT INTO DASHAR_SESSION_DATA VALUES ('{session_data_point_uuid}', '{session_uuid}', {session_data_point_timestamp}, {mph}, {rpm}, {fuel_level})"

    @staticmethod
    def dashar_is_automobile_registered(vin: str) -> str:
        return f"SELECT AUTOMOBILE_ID, AUTOMOBILE_YEAR, AUTOMOBILE_NAME, AUTOMOBILE_MILEAGE, INITIAL_CAPTURE_TIMESTAMP FROM DASHAR_AUTOMOBILE WHERE AUTOMOBILE_VIN = '{vin}'"

    @staticmethod
    def dashar_register_automobile(vin: str, name: str, year: int, mileage: float, initial_capture_timestamp: float, last_modified_timestamp: float) -> str:
        return f"INSERT INTO DASHAR_AUTOMOBILE VALUES ('{vin}', '{name}', '{year}', '{mileage}', '{initial_capture_timestamp}', '{last_modified_timestamp}')"