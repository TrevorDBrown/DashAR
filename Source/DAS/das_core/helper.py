#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024 Trevor D. Brown. All rights reserved.
#   This project is distributed under the MIT license.
#
#   File:       helper.py
#   Purpose:    This script contains helpers (constants, enums, functions, etc.) shared amongst multiple modules.
#

from enum import Enum, IntEnum
from uuid import uuid4
import datetime
import json

class Constants():
    EXPECTED_CONFIGURATION_VERSION: str = "0.1"
    EXPECTED_DASHAR_VERSION: str = "0.1"
    EXPECTED_DAS_VERSION: str = "0.1"
    EXPECTED_HUD_VERSION: str = "0.1"
    EXPECTED_COMPANION_APP_VERSION: str = "0"

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
    PRODUCTION: int = 1
    DEBUG: int = 2
    TEST: int = 3

class DefaultDataFormat(Enum):
    AMERICA: int = 1

class DataSourceType(Enum):
    DATABASE: int = 1
    DIRECT_FILE: int = 2

class DatabaseStatements():
    @staticmethod
    def dashar_session_start(session_uuid: str, vin: str, session_start_timestamp: float) -> str:
        return f"INSERT INTO DASHAR_SESSION VALUES ('{session_uuid}', '{vin}', {session_start_timestamp})"

    @staticmethod
    def dashar_session_insert_data_point(session_data_point_uuid: str, session_uuid: str, session_data_point_timestamp: float, mph: float, rpm: float, fuel_level: float) -> str:
        return f"INSERT INTO DASHAR_SESSION_DATA VALUES ('{session_data_point_uuid}', '{session_uuid}', {session_data_point_timestamp}, {mph}, {rpm}, {fuel_level})"