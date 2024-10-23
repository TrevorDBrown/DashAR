#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024 Trevor D. Brown. All rights reserved.
#   This project is distributed under the MIT license.
#
#   File:       obdii_interpreter.py
#   Purpose:    This script manages the OBDII connection and context while the service is running.
#

from das_core.helper import Constants, SharedFunctions, ServiceMode, DefaultDataFormat, DatabaseStatements
from das_core.data_connector import DataConnection
import obd
import textwrap

class OBDIIContext:

    # Object Variables
    __id: str                                       # __id - a UUIDv4 value, used to uniquely identify the context.
    __created_timestamp: float                      # __created_timestamp - the Unix timestamp of when the object was created.
    __service_mode: ServiceMode                     # __service_mode - the current service mode of the system (PRODUCTION or DEBUG).
    __vehicle_vin: str                              # __vehicle_vin - the VIN of the current vehicle.
    __obdii_interface_device_path: str              # __obdii_interface_device_path - the manually defined file path (Unix-esque) or COM port (Windows) of the OBDII device.
    __obdii_context: obd.OBD                        # __obdii_context - the connection context for the current session.
    __database_context: DataConnection              # __database_context - the database context for storing current session data.

    # Fuel Level Variables
    __vehicle_fuel_level_data_point_max: int        # __vehicle_fuel_level_data_point_max - the max number of data points collected before recomputing the fuel level.
    __vehicle_fuel_level_last_computed: int         # __vehicle_fuel_level_last_computed - the last fuel level computed.
    __vehicle_fuel_level_temp_store: list           # __vehicle_fuel_level_temp_store - the fuel level points over a fixed frequency.
    __vehicle_fuel_level_temp_store_count: int      # __vehicle_fuel_level_temp_store_count - the number of data points collected in the fixed frequency for fuel level.


    def __init__(self, service_mode: ServiceMode, obdii_interface_device_path: str = "", database_path: str = "", fuel_level_max_data_points: int = 100, auto_connect: bool = True) -> None:

        # Store the Service Mode (PRODUCTION or DEBUG)
        self.__service_mode = service_mode

        if (service_mode == ServiceMode.DEBUG):
            # Enable logging.
            obd.logger.setLevel(obd.logging.DEBUG) # enables all debug information
        else:
            # Disable logging.
            obd.logger.removeHandler(obd.console_handler)

        self.__id = SharedFunctions.generate_object_id()
        self.__created_timestamp = SharedFunctions.get_current_timestamp()  # Store the current date/time (UTC) as a UNIX timestamp.
        self.__obdii_interface_device_path = obdii_interface_device_path

        if (auto_connect):
            successful_obdii_connection = self.establish_connection()
        else:
            # TODO: handle manual connect condition.
            None

        if (successful_obdii_connection):
            self.__vehicle_vin = self.__obdii_context.query(obd.commands.VIN).value.decode()
            self.__database_context = DataConnection(data_filename=database_path, service_mode=self.__service_mode)
            self.__database_context.insert_into_database(DatabaseStatements.dashar_session_start(self.__id, self.__vehicle_vin, self.__created_timestamp))

            self.__vehicle_fuel_level_data_point_max = fuel_level_max_data_points
            self.__vehicle_fuel_level_last_computed = 0
            self.__vehicle_fuel_level_temp_store_count = 0
            self.__vehicle_fuel_level_temp_store = []

        else:
            # TODO: formalize the exception handling here.
            print("Error: the connection over OBDII failed.")

        return

    def __del__(self):
        # TODO: if not used, remove.
        None

    def establish_connection(self) -> bool:
        try:
            if (self.__obdii_interface_device_path == ""):
                # TODO: determine best method for figuring out which device is the OBDII device automatically.
                # ports = obd.scan_serial()      # return list of valid USB or RF ports
                # print(ports)                    # ['/dev/ttyUSB0', '/dev/ttyUSB1']
                # connection = obd.OBD(ports[0]) # connect to the first port in the list

                self.__obdii_context = obd.OBD()
            else:
                self.__obdii_context = obd.OBD(self.__obdii_interface_device_path, start_low_power=True, check_voltage=True, fast=False)

            return bool(self.__obdii_context.is_connected())

        except:
            # Error - connection failed to be established.
            return False

    def connection_status(self) -> str:
        # str-based status: Connected, Disconnected, etc.
        try:
            return str(self.__obdii_context.status())
        except:
            return 'Unknown'

    def is_connected(self) -> bool:
        return bool(self.__obdii_context.is_connected())

    def available_commands(self) -> set:

        self.__obdii_context.print_commands()

        return set(self.__obdii_context.supported_commands)

    def __get_speed(self, data_format = DefaultDataFormat.AMERICA) -> int:
        current_speed: int

        try:
            # Ensure the connection is established before proceeding.
            if (self.__obdii_context.is_connected()):
                # Assume MPH, UNODIR.
                if (data_format == DefaultDataFormat.AMERICA):
                    current_speed = int(self.__obdii_context.query(obd.commands.SPEED).value.to("mph").magnitude)
                else:
                    current_speed = int(self.__obdii_context.query(obd.commands.SPEED).value.magnitude)
            else:
                # The OBDII device is not active.
                current_speed = -1
        except:
            current_speed = -1

        return current_speed

    def __get_rpms(self) -> int:
        current_rpm: int

        try:
            # Ensure the connection is established before proceeding.
            if (self.__obdii_context.is_connected()):
                current_rpm = int(self.__obdii_context.query(obd.commands.RPM).value.magnitude)
            else:
                # The OBDII device is not active.
                current_rpm = -1
        except:
            current_rpm = -1

        return current_rpm

    def __get_fuel_level(self) -> int:
        try:
            # Ensure the connection is established before proceeding.
            if (self.__obdii_context.is_connected()):
                if (self.__vehicle_fuel_level_temp_store_count < self.__vehicle_fuel_level_data_point_max):
                    self.__vehicle_fuel_level_temp_store.append(int(self.__obdii_context.query(obd.commands.FUEL_LEVEL).value.magnitude))
                    self.__vehicle_fuel_level_temp_store_count += 1
                else:
                    self.__vehicle_fuel_level_last_computed = int(sum(self.__vehicle_fuel_level_temp_store)/self.__vehicle_fuel_level_temp_store_count)
                    self.__vehicle_fuel_level_temp_store = []
                    self.__vehicle_fuel_level_temp_store_count = 0
            else:
                # The OBDII device is not active.
                return -1
        except:
            return -1

        return self.__vehicle_fuel_level_last_computed

    def capture_data_points(self) -> dict:
        current_speed: float = self.__get_speed()
        current_rpms: float = self.__get_rpms()
        current_fuel_level: float = self.__get_fuel_level()

        # Insert the data point into the SQLite3 database.
        self.__database_context.insert_into_database(DatabaseStatements.dashar_session_insert_data_point(SharedFunctions.generate_object_id(), self.__id, SharedFunctions.get_current_timestamp(), current_speed, current_rpms, current_fuel_level))

        client_response_data_points: dict = {
            "speed": current_speed,
            "rpms": current_rpms,
            "fuel_level": current_fuel_level
        }

        return client_response_data_points

    def __str__(self) -> str:
        return textwrap.dedent(f"""
                Object: OBDIIContext
                ID: {self.__id}
                Date Created (Epoch): {self.__created_timestamp}
                Device Path: {self.__obdii_interface_device_path}
                Status: {self.connection_status()}
                """)

def main() -> None:

    print(f"This module ({__file__}) should be invoked as an import.")

    return

if __name__ == "__main__":
    main()
