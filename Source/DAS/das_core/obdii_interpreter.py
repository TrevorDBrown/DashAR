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

import obd.elm327

class OBDIIContext:

    # Variables
    __id: str
    __timestampCreated: float
    __obdiiInterfaceDevicePath: str
    __obdiiContext: obd.OBD
    __obdiiAvailableCommands: dict

    def __init__(self, newOBDIIInterfaceDevicePath: str = "", autoConnect: bool = True) -> None:
        # Disable logging.
        obd.logger.removeHandler(obd.console_handler)

        self.__id = uuid4()   # Generate a unique identifier for the interpreter object.
        self.__timestampCreated = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()      # Store the current date/time (UTC) as a UNIX timestamp.
        self.__obdiiInterfaceDevicePath = newOBDIIInterfaceDevicePath

        if (autoConnect):
            self.establishConnection()

    def establishConnection(self) -> bool:
        if (self.__obdiiInterfaceDevicePath == ""):
            # ports = obd.scan_serial()      # return list of valid USB or RF ports
            # print(ports)                    # ['/dev/ttyUSB0', '/dev/ttyUSB1']
            # connection = obd.OBD(ports[0]) # connect to the first port in the list

            self.__obdiiContext = obd.Async()
        else:
            self.__obdiiContext = obd.Async(self.__obdiiInterfaceDevicePath)

        if (self.connectionStatus() == 'Connected'):
            return True
        else:
            return False

    def learnConnection(self) -> bool:
        # TODO: loop through OBDII commands, verify they exist. If they do, store in "available commands" dict.
        return False

    def connectionStatus(self) -> str:
        try:
            return self.__obdiiContext.status()
        except:
            return 'Unknown'

    def __str__(self) -> str:
        return textwrap.dedent(f"""
                Object: OBDIIContext
                ID: {self.__id}
                Date Created (Epoch): {self.__timestampCreated}
                Device Path: {self.__obdiiInterfaceDevicePath}
                Status: {self.connectionStatus()}
                """)


def main() -> None:

    print("DashAR OBDII Interpreter Module")
    print("This should be invoked as an import.")

    return

if __name__ == "__main__":
    main()
