#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       helper.py
#

"""Purpose: the helper constants, variables, and functions used by the DAS API for the DashAR system."""

import datetime
import json
from enum import IntEnum
from typing import Final
from uuid import uuid4


class Constants:
    """
    Constants to be used throughout the DAS API. Constants are denoted through all uppercase variable names.
    """

    DASHAR_SPLASH: Final[str] = "The DashAR Automotive HUD System"
    DASHAR_COPYRIGHT: Final[str] = (
        f"(c)2024-{datetime.date.today().year} Trevor D. Brown. "
        f"Distributed under the MIT License."
    )
    EXPECTED_CONFIGURATION_VERSION: Final[str] = "0.2"
    EXPECTED_DASHAR_VERSION: Final[str] = "0.2"


class Variables:
    """
    Variables to be used throughout the DAS API. Not implemented.
    """
    pass


class SharedFunctions:
    """
    Functions that are used through the DAS API.
    """

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
    """
    Special constants used to indicate the service mode of the system.
    """

    INVALID: int = -1  # INVALID: an error state where the system cannot be used.
    PRODUCTION: int = 1  # PRODUCTION: live data provided via OBDII.
    DEBUG: int = 2  # DEBUG: like PRODUCTION, just more verbose.
    EMULATE: int = 3  # EMULATE: similar to PRODUCTION, except an ELM327 emulator emits the OBDII data.
    TEST: int = 4  # TEST: OBDII override. Values are generated using RNG.
    BEAMNG: int = 5  # BEAMNG: utilizes BeamNGpy to fetch equivalent values from a running instance of the game.


class SystemStatus(IntEnum):
    """
    Special constants used to indicate the status of the system.
    """

    FAILED: int = -1  # FAILED: the system failed to initialize.
    NOT_STARTED: int = 1  # NOT_STARTED: the system has yet to be initialized.
    STARTING: int = 2  # STARTING: the system is initializing.
    READY: int = 3  # READY: the system is ready to run.
    BUSY: int = 4  # BUSY: the system is processing.


class DefaultDataFormat(IntEnum):
    """
    Special constants used to indicate the country where the system is being utilized.
    """

    AMERICA: int = 1


class DataSourceType(IntEnum):
    """
    Special constants used to indicate the origin of metadata and configuration data for the system.
    """

    DATABASE: int = 1
    DIRECT_FILE: int = 2


class DatabaseStatements:
    """
    Prepared SQL that is used to interact with the SQLite database (when applicable).
    """

    @staticmethod
    def dashar_session_start(
        session_uuid: str, vin: str, session_start_timestamp: float
    ) -> str:
        return f"INSERT INTO DASHAR_SESSION VALUES ('{session_uuid}', '{vin}', {session_start_timestamp})"

    @staticmethod
    def dashar_session_insert_data_point(
        session_data_point_uuid: str,
        session_uuid: str,
        session_data_point_timestamp: float,
        mph: float,
        rpm: float,
        fuel_level: float,
    ) -> str:
        return (
            f"INSERT INTO DASHAR_SESSION_DATA VALUES "
            f"('{session_data_point_uuid}', '{session_uuid}', {session_data_point_timestamp}, "
            f"{mph}, {rpm}, {fuel_level})"
        )

    @staticmethod
    def dashar_is_automobile_registered(vin: str) -> str:
        return (
            f"SELECT AUTOMOBILE_ID, AUTOMOBILE_YEAR, AUTOMOBILE_NAME, AUTOMOBILE_MILEAGE, INITIAL_CAPTURE_TIMESTAMP "
            f"FROM DASHAR_AUTOMOBILE WHERE AUTOMOBILE_VIN = '{vin}'"
        )

    @staticmethod
    def dashar_register_automobile(
        vin: str,
        name: str,
        year: int,
        mileage: float,
        initial_capture_timestamp: float,
        last_modified_timestamp: float,
    ) -> str:
        return (
            f"INSERT INTO DASHAR_AUTOMOBILE VALUES "
            f"('{vin}', '{name}', '{year}', '{mileage}', '{initial_capture_timestamp}', '{last_modified_timestamp}')"
        )
