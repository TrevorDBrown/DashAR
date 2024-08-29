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

    # Variables
    __id: str
    __created_timestamp: float
    __obdii_interface_device_path: str
    __obdii_context: obd.OBD
    __obdii_available_commands: dict

    def __init__(self, new_obdii_interface_device_path: str = "", auto_connect: bool = True) -> None:
        # Disable logging.
        obd.logger.removeHandler(obd.console_handler)

        self.__id = uuid4()   # Generate a unique identifier for the interpreter object.
        self.__created_timestamp = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()      # Store the current date/time (UTC) as a UNIX timestamp.
        self.__obdii_interface_device_path = new_obdii_interface_device_path

        if (auto_connect):
            self.establish_connection()

    def establish_connection(self) -> bool:
        if (self.__obdii_interface_device_path == ""):
            # ports = obd.scan_serial()      # return list of valid USB or RF ports
            # print(ports)                    # ['/dev/ttyUSB0', '/dev/ttyUSB1']
            # connection = obd.OBD(ports[0]) # connect to the first port in the list

            self.__obdii_context = obd.Async()
        else:
            self.__obdii_context = obd.Async(self.__obdii_interface_device_path)

        return self.__obdii_context.is_connected()

    def learn_connection(self) -> bool:
        # TODO: loop through OBDII commands, verify they exist. If they do, store in "available commands" dict.
        return False

    def connection_status(self) -> str:
        try:
            return self.__obdii_context.status()
        except:
            return 'Unknown'

    def is_connected(self) -> bool:
        return self.__obdii_context.is_connected()

    def get_speed(self) -> str:
        return str(self.__obdii_context.query(obd.commands.SPEED).value.to("mph"))

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
