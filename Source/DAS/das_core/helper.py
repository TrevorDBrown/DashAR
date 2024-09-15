#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024 Trevor D. Brown. All rights reserved.
#   This project is distributed under the MIT license.
#
#   File:       helper.py
#   Purpose:    This script contains helpers (constants, enums, functions, etc.) shared amongst multiple modules.
#

import os
from pathlib import Path
from enum import Enum
from uuid import uuid4
import datetime

class Constants():
    DATABASE_PATH: str = os.path.join(os.getcwd(), "data", "dashar-data.sqlite3")

class SharedFunctions():
    def generate_object_id() -> str:
        # Generate a UUIDv4 for the calling object.
        return uuid4()

    def get_current_timestamp() -> float:
        return datetime.datetime.now(tz=datetime.timezone.utc).timestamp()

class ServiceMode(Enum):
    PRODUCTION: int = 1
    DEBUG: int = 2

class DefaultDataFormat(Enum):
    AMERICA: int = 1

class DataSourceType(Enum):
    DATABASE: int = 1
    DIRECT_FILE: int = 2

class DatabaseStatements():
    def dashar_session_start(session_uuid: str, vin: str, session_start_timestamp: float) -> str:
        return f"INSERT INTO DASHAR_SESSION VALUES ('{session_uuid}', '{vin}', {session_start_timestamp})"

    def dashar_session_insert_data_point(session_data_point_uuid: str, session_uuid: str, session_data_point_timestamp: float, mph: float, rpm: float, fuel_level: float) -> str:
        return f"INSERT INTO DASHAR_SESSION_DATA VALUES ('{session_data_point_uuid}', '{session_uuid}', {session_data_point_timestamp}, {mph}, {rpm}, {fuel_level})"

class DebugConstants():
    TEST_VIN: str = ""
