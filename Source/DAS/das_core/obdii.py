#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       obdii.py
#

"""Purpose: the OBDII context manager used by the DAS API for the DashAR system."""

from das_core.data_connector import DataConnection

from das_core.helper import (
    SharedFunctions,
    ServiceMode,
    DefaultDataFormat,
    DatabaseStatements,
    DataSourceType
)

import obd
import random


class OBDIIContext:
    """
    A class for the OBDII context (vehicle information, captured data points, etc.).
    """

    _id: str
    _created_timestamp: float
    _service_mode: ServiceMode
    _vehicle_vin: str
    _obdii_interface_device_path: str
    _obdii_context: obd.OBD
    _database_context: DataConnection

    # Fuel Level Variables
    _vehicle_fuel_level_data_point_max: int
    _vehicle_fuel_level_last_computed: int
    _vehicle_fuel_level_temp_store: list
    _vehicle_fuel_level_temp_store_count: int

    def __init__(
        self,
        service_mode: ServiceMode,
        obdii_interface_device_path: str = "",
        database_path: str = "",
        fuel_level_max_data_points: int = 1000,
        auto_connect: bool = True,
    ) -> None:
        self._service_mode = service_mode
        successful_obdii_connection: bool = False

        if service_mode == ServiceMode.DEBUG:
            # Enable logging.
            obd.logger.setLevel(obd.logging.DEBUG)
        else:
            # Disable logging.
            obd.logger.removeHandler(obd.console_handler)

        self._id = SharedFunctions.generate_object_id()
        self._created_timestamp = (
            SharedFunctions.get_current_timestamp()
        )  # Store the current date/time (UTC) as a UNIX timestamp.
        self._obdii_interface_device_path = obdii_interface_device_path

        if self._service_mode in (ServiceMode.PRODUCTION, ServiceMode.DEBUG):
            # PRODUCTION or DEBUG Mode, attempt connection to ELM327 device.
            if auto_connect:
                successful_obdii_connection = self.establish_connection()
            else:
                # TODO: handle manual connect condition.
                pass

            if successful_obdii_connection:
                self._vehicle_vin = self._obdii_context.query(
                    obd.commands.VIN
                ).value.decode()

                self._database_context = DataConnection(
                    data_filename=database_path,
                    data_source_type=DataSourceType.DATABASE
                )

                self._database_context.insert_into_database(
                    DatabaseStatements.dashar_session_start(
                        self._id, self._vehicle_vin, self._created_timestamp
                    )
                )

                self._vehicle_fuel_level_data_point_max = fuel_level_max_data_points
                self._vehicle_fuel_level_last_computed = 0
                self._vehicle_fuel_level_temp_store_count = 0
                self._vehicle_fuel_level_temp_store = []

            else:
                # TODO: formalize the exception handling here.
                print("Error: the connection over OBDII failed.")

        else:
            # Test Mode. Randomized values will be generated per API call.
            print(
                f"No OBDII connection was established, as the system is in Service Mode {service_mode.name}."
            )

        return

    def __del__(self):
        # TODO: if not used, remove.
        pass

    def establish_connection(self) -> bool:
        obdii_device_port: str = self._obdii_interface_device_path

        try:
            if self._obdii_interface_device_path == "":
                # Determine the OBDII device automatically.
                # TODO: determine best method for figuring out which device is the OBDII device automatically.
                ports: list = obd.scan_serial()
                print(
                    ports
                )  # ['/dev/ttyUSB0', '/dev/ttyUSB1'] (Linux) or ['COM3', 'COM4'] (Windows)

                # Connect to the first port in the list, if the list exists.
                if ports:
                    obdii_device_port = ports[0]
                else:
                    # TODO: define a better, custom exception here.
                    raise ValueError("An OBDII connection could not be established.")

            # Attempt to establish the connection.
            self._obdii_context = obd.OBD(
                portstr=obdii_device_port,
                start_low_power=True,
                check_voltage=True,
                fast=False,
                baudrate=230400,
                timeout=1,
            )

        except Exception as e:
            # OBDII connection failed to be established.
            # TODO: be more specific with the exception here...
            print("Unable to establish OBDII connection.")
            print(e)

            # Set the service mode to INVALID.
            self._service_mode = ServiceMode.INVALID

            return False

        return bool(self._obdii_context.is_connected())

    def connection_status(self) -> str:
        # str-based status: Connected, Disconnected, etc.
        try:
            return str(self._obdii_context.status())
        except Exception as e:
            print(f"Exception: {e}")
            return "Unknown"

    def is_connected(self) -> bool:

        if self._service_mode in (ServiceMode.PRODUCTION, ServiceMode.DEBUG):
            try:
                return bool(self._obdii_context.is_connected())

            except Exception as e:
                print(f"Exception: {e}")
                return False
        else:
            return False

    def available_commands(self) -> set:
        self._obdii_context.print_commands()

        return set(self._obdii_context.supported_commands)

    def _get_speed(self, data_format=DefaultDataFormat.AMERICA) -> int:
        current_speed: int

        if self._service_mode == ServiceMode.TEST:
            # Test Mode, randomize the value.
            current_speed = random.randint(0, 120)

        else:
            try:
                # Ensure the connection is established before proceeding.
                if self._obdii_context.is_connected():
                    # Assume MPH.
                    if data_format == DefaultDataFormat.AMERICA:
                        current_speed = int(
                            self._obdii_context.query(obd.commands["SPEED"])
                            .value.to("mph")
                            .magnitude
                        )
                    else:
                        current_speed = int(
                            self._obdii_context.query(
                                obd.commands["SPEED"]
                            ).value.magnitude
                        )
                else:
                    # The OBDII device is not active.
                    current_speed = -1
            except Exception as e:
                print(f"Exception: {e}")
                current_speed = -1

        return current_speed

    def _get_rpms(self) -> int:
        current_rpm: int

        if self._service_mode == ServiceMode.TEST:
            # Test Mode, randomize the value.
            current_rpm = random.randint(500, 5000)

        else:
            try:
                # Ensure the connection is established before proceeding.
                if self._obdii_context.is_connected():
                    current_rpm = int(
                        self._obdii_context.query(obd.commands["RPM"]).value.magnitude
                    )
                else:
                    # The OBDII device is not active.
                    current_rpm = -1
            except Exception as e:
                print(f"Exception: {e}")
                current_rpm = -1

        return current_rpm

    def _get_fuel_level(self) -> int:
        if (
            self._service_mode in (ServiceMode.TEST, ServiceMode.DEBUG)
        ):  # NOTE: as of this writing (01/31/2025), the ELM327 emulator cannot emulate fuel level.
            # Test Mode, randomize the value.
            return random.randint(0, 100)

        else:
            try:
                # Ensure the connection is established before proceeding.
                if self._obdii_context.is_connected():
                    if (
                        self._vehicle_fuel_level_temp_store_count
                        <= self._vehicle_fuel_level_data_point_max
                    ):
                        self._vehicle_fuel_level_temp_store.append(
                            int(
                                self._obdii_context.query(
                                    obd.commands["FUEL_LEVEL"]
                                ).value.magnitude
                            )
                        )
                        self._vehicle_fuel_level_temp_store_count += 1
                    else:
                        self._vehicle_fuel_level_last_computed = int(
                            sum(self._vehicle_fuel_level_temp_store)
                            / self._vehicle_fuel_level_temp_store_count
                        )
                        self._vehicle_fuel_level_temp_store = [
                            self._vehicle_fuel_level_last_computed
                        ]
                        self._vehicle_fuel_level_temp_store_count = 1
                else:
                    # The OBDII device is not active.
                    return -1
            except Exception as e:
                print(f"Exception: {e}")
                return -1

            return self._vehicle_fuel_level_last_computed

    def capture_data_points(self) -> dict:
        current_speed: float = self._get_speed()
        current_rpms: float = self._get_rpms()
        current_fuel_level: float = self._get_fuel_level()

        # Insert the data point into the SQLite3 database (if not in test)
        if self._service_mode in (ServiceMode.PRODUCTION, ServiceMode.DEBUG):
            self._database_context.insert_into_database(
                DatabaseStatements.dashar_session_insert_data_point(
                    SharedFunctions.generate_object_id(),
                    self._id,
                    SharedFunctions.get_current_timestamp(),
                    current_speed,
                    current_rpms,
                    current_fuel_level,
                )
            )

        client_response_data_points: dict = {
            "speed": current_speed,
            "rpms": current_rpms,
            "fuel_level": f"{current_fuel_level}%",
        }

        return client_response_data_points

    def __str__(self) -> str:
        return (
            f"Object: OBDIIContext\n"
            f"ID: {self._id}\n"
            f"Date Created (Epoch): {self._created_timestamp}\n"
            f"Device Path: {self._obdii_interface_device_path}\n"
            f"Status: {self.connection_status()}"
        )


if __name__ == "__main__":
    print(f"This module ({__file__}) should be invoked as an import.")
