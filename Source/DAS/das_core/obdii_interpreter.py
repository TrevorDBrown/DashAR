#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       obdii_interpreter.py
#   Purpose:    This script manages the OBDII connection and context while the service is running.
#

from das_core.helper import SharedFunctions, ServiceMode, DefaultDataFormat, DatabaseStatements
from das_core.data_connector import DataConnection

import obd
import random

class OBDIIContext:

    # Object Variables
    __id: str                                       # __id - a UUIDv4 value, used to uniquely identify the context.
    __created_timestamp: float                      # __created_timestamp - the Unix timestamp of when the object was created.
    __service_mode: ServiceMode                     # __service_mode - the current service mode of the system (PRODUCTION, DEBUG, or TEST (valid), or INVALID).
    __vehicle_vin: str                              # __vehicle_vin - the VIN of the current vehicle.
    __obdii_interface_device_path: str              # __obdii_interface_device_path - the manually defined file path (Unix-esque) or COM port (Windows) of the OBDII device.
    __obdii_context: obd.OBD                        # __obdii_context - the connection context for the current session.
    __database_context: DataConnection              # __database_context - the database context for storing current session data.

    # Fuel Level Variables
    __vehicle_fuel_level_data_point_max: int        # __vehicle_fuel_level_data_point_max - the max number of data points collected before recomputing the fuel level.
    __vehicle_fuel_level_last_computed: int         # __vehicle_fuel_level_last_computed - the last fuel level computed.
    __vehicle_fuel_level_temp_store: list           # __vehicle_fuel_level_temp_store - the fuel level points over a fixed frequency.
    __vehicle_fuel_level_temp_store_count: int      # __vehicle_fuel_level_temp_store_count - the number of data points collected in the fixed frequency for fuel level.


    def __init__(self, service_mode: ServiceMode, obdii_interface_device_path: str = "", database_path: str = "", fuel_level_max_data_points: int = 1000, auto_connect: bool = True) -> None:

        # Store the Service Mode (PRODUCTION, DEBUG, or TEST)
        self.__service_mode = service_mode
        successful_obdii_connection: bool = False

        if (service_mode == ServiceMode.DEBUG):
            # Enable logging.
            obd.logger.setLevel(obd.logging.DEBUG)
        else:
            # Disable logging.
            obd.logger.removeHandler(obd.console_handler)

        self.__id = SharedFunctions.generate_object_id()
        self.__created_timestamp = SharedFunctions.get_current_timestamp()  # Store the current date/time (UTC) as a UNIX timestamp.
        self.__obdii_interface_device_path = obdii_interface_device_path

        if (self.__service_mode in (ServiceMode.PRODUCTION, ServiceMode.DEBUG)):
            # PRODUCTION or DEBUG Mode, attempt connection to ELM327 device.
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

        else:
            # Test Mode. Randomized values will be generated per API call.
            print(f"No OBDII connection was established, as the system is in Service Mode {service_mode.name}.")

        return

    def __del__(self):
        # TODO: if not used, remove.
        None

    def establish_connection(self) -> bool:
        obdii_device_port: str = self.__obdii_interface_device_path

        try:
            if (self.__obdii_interface_device_path == ""):
                # Determine the OBDII device automatically.
                # TODO: determine best method for figuring out which device is the OBDII device automatically.
                ports: list = obd.scan_serial()
                print(ports)                   # ['/dev/ttyUSB0', '/dev/ttyUSB1'] (Linux) or ['COM3', 'COM4'] (Windows)

                # Connect to the first port in the list, if the list exists.
                if (ports):
                    obdii_device_port = ports[0]
                else:
                    # TODO: define custom exception here.
                    raise Exception

            # Attempt to establish the connection.
            self.__obdii_context = obd.OBD(portstr=obdii_device_port, start_low_power=True, check_voltage=True, fast=False, baudrate=230400, timeout=1)

        except Exception as e:
            # OBDII connection failed to be established.
            # TODO: be more specific with the exception here...
            print("Unable to establish OBDII connection.")
            print(e)

            # Set the service mode to INVALID.
            self.__service_mode = ServiceMode.INVALID

            return False

        return bool(self.__obdii_context.is_connected())

    def connection_status(self) -> str:
        # str-based status: Connected, Disconnected, etc.
        try:
            return str(self.__obdii_context.status())
        except:
            return 'Unknown'

    def is_connected(self) -> bool:
        # boolean-based status
        try:
            return bool(self.__obdii_context.is_connected())
        except:
            return False

    def available_commands(self) -> set:
        self.__obdii_context.print_commands()

        return set(self.__obdii_context.supported_commands)

    def __get_speed(self, data_format = DefaultDataFormat.AMERICA) -> int:
        current_speed: int

        if (self.__service_mode == ServiceMode.TEST):
            # Test Mode, randomize the value.
            current_speed = random.randint(0, 120)

        else:
            try:
                # Ensure the connection is established before proceeding.
                if (self.__obdii_context.is_connected()):
                    # Assume MPH.
                    if (data_format == DefaultDataFormat.AMERICA):
                        current_speed = int(self.__obdii_context.query(obd.commands["SPEED"]).value.to("mph").magnitude)
                    else:
                        current_speed = int(self.__obdii_context.query(obd.commands["SPEED"]).value.magnitude)
                else:
                    # The OBDII device is not active.
                    current_speed = -1
            except:
                current_speed = -1

        return current_speed

    def __get_rpms(self) -> int:
        current_rpm: int

        if (self.__service_mode == ServiceMode.TEST):
            # Test Mode, randomize the value.
            current_rpm = random.randint(500, 5000)

        else:
            try:
                # Ensure the connection is established before proceeding.
                if (self.__obdii_context.is_connected()):
                    current_rpm = int(self.__obdii_context.query(obd.commands["RPM"]).value.magnitude)
                else:
                    # The OBDII device is not active.
                    current_rpm = -1
            except:
                current_rpm = -1

        return current_rpm

    def __get_fuel_level(self) -> int:

        if (self.__service_mode in (ServiceMode.TEST, ServiceMode.DEBUG)):  # NOTE: as of this writing (01/31/2025), the ELM327 emulator cannot emulate fuel level.
            # Test Mode, randomize the value.
            return random.randint(0, 100)

        else:
            try:
                # Ensure the connection is established before proceeding.
                if (self.__obdii_context.is_connected()):
                    if (self.__vehicle_fuel_level_temp_store_count <= self.__vehicle_fuel_level_data_point_max):
                        self.__vehicle_fuel_level_temp_store.append(int(self.__obdii_context.query(obd.commands["FUEL_LEVEL"]).value.magnitude))
                        self.__vehicle_fuel_level_temp_store_count += 1
                    else:
                        self.__vehicle_fuel_level_last_computed = int(sum(self.__vehicle_fuel_level_temp_store)/self.__vehicle_fuel_level_temp_store_count)
                        self.__vehicle_fuel_level_temp_store = [self.__vehicle_fuel_level_last_computed]
                        self.__vehicle_fuel_level_temp_store_count = 1
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

        # Insert the data point into the SQLite3 database (if not in test)
        if (self.__service_mode in (ServiceMode.PRODUCTION, ServiceMode.DEBUG)):
            self.__database_context.insert_into_database(DatabaseStatements.dashar_session_insert_data_point(SharedFunctions.generate_object_id(), self.__id, SharedFunctions.get_current_timestamp(), current_speed, current_rpms, current_fuel_level))

        client_response_data_points: dict = {
            "speed": current_speed,
            "rpms": current_rpms,
            "fuel_level": f"{current_fuel_level}%"
        }

        return client_response_data_points

    def __str__(self) -> str:
        return f"Object: OBDIIContext\nID: {self.__id}\nDate Created (Epoch): {self.__created_timestamp}\nDevice Path: {self.__obdii_interface_device_path}\nStatus: {self.connection_status()}"

def main() -> None:

    print(f"This module ({__file__}) should be invoked as an import.")

    return

if __name__ == "__main__":
    main()
