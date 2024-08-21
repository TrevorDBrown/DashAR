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

class OBDIIContext:

    __id: str
    __dateCreated: float
    __obdiiInterfaceDevicePath: str
    __obdiiContext: obd.OBD
    __obdiiAvailableCommands: dict

    def __init__(self, newOBDIIInterfaceDevicePath: str, autoConnect: bool = True) -> None:
        self.__id = uuid4()   # Generate a unique identifier for the interpreter object.
        self.__dateCreated = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()      # Store the current date/time (UTC) as a UNIX timestamp.
        self.__obdiiInterfaceDevicePath = newOBDIIInterfaceDevicePath

        if (autoConnect):
            self.establishConnection()

    def establishConnection(self) -> bool:
        self.__obdiiContext = obd.OBD(self.__obdiiInterfaceDevicePath)

        if (self.connectionStatus() == 'Connected'):
            return True
        else:
            return False

    def learnConnection(self) -> bool:
        # TODO: loop through OBDII commands, verify they exist. If they do, store in "available commands" dict.
        return False

    def connectionStatus(self) -> str:
        try:
            return 'Connected' if self.__obdiiContext.is_connected() else 'Disconnected'
        except:
            return 'Unknown'

    def __str__(self) -> str:
        return f"\nObject: OBDIIContext\nID: {self.__id}\nDate Created (Epoch): {self.__dateCreated}\nDevice Path: {self.__obdiiInterfaceDevicePath}\nStatus: {self.connectionStatus()}\n"


def main() -> None:

    print("DashAR OBDII Interpreter Module")
    print("This should be invoked as an import.")

    return

if __name__ == "__main__":
    main()
