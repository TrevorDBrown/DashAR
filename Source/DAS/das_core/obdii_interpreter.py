#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024 Trevor D. Brown. All rights reserved.
#   This project is distributed under the MIT license.
#
#   File:       obdii_interpreter.py
#   Purpose:    This script manages the OBDII connection and context while the service is running.
#

import obd
import datetime
from uuid import uuid4
import textwrap

class OBDIIContext:

    # Object Variables
    __id: str                               # __id - a UUIDv4 value, used to uniquely identify the context.
    __created_timestamp: float              # __created_timestamp - the Unix timestamp of when the object was created.
    __obdii_interface_device_path: str      # __obdii_interface_device_path - the manually defined file path (Unix-esque) or COM port (Windows) of the OBDII device.
    __obdii_context: obd.OBD                # __obdii_context - the connection context for the current session.

    def __init__(self, obdii_interface_device_path: str = "", auto_connect: bool = True, debug_mode = False) -> None:

        if (debug_mode):
            # Enable logging.
            obd.logger.setLevel(obd.logging.DEBUG) # enables all debug information
        else:
            # Disable logging.
            obd.logger.removeHandler(obd.console_handler)

        self.__id = uuid4()   # Generate a unique identifier for the interpreter object.
        self.__created_timestamp = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()      # Store the current date/time (UTC) as a UNIX timestamp.
        self.__obdii_interface_device_path = obdii_interface_device_path

        if (auto_connect):
            self.establish_connection()
        else:
            # TODO: handle manual connect condition.
            None

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

            return self.__obdii_context.is_connected()

        except:
            # Error - connection failed to be established.
            return False

    def connection_status(self) -> str:
        # str-based status: Connected, Disconnected, etc.
        try:
            return self.__obdii_context.status()
        except:
            return 'Unknown'

    def is_connected(self) -> bool:
        return self.__obdii_context.is_connected()

    def available_commands(self) -> set:

        self.__obdii_context.print_commands()

        return self.__obdii_context.supported_commands

    def get_speed(self, in_kph = False) -> int:
        try:
            # Ensure the connection is established before proceeding.
            if (self.__obdii_context.is_connected()):
                # Assume MPH, UNODIR.
                if (in_kph):
                    currentSpeed: int = int(self.__obdii_context.query(obd.commands.SPEED).value.magnitude)
                else:
                    currentSpeed: int = int(self.__obdii_context.query(obd.commands.SPEED).value.to("mph").magnitude)
            else:
                # The OBDII device is not active.
                currentSpeed: int = -1
        except:
            currentSpeed: int = -1

        print(f"Current Speed: {currentSpeed}")

        return currentSpeed

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
