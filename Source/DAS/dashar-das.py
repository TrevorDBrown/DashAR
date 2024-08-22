#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024 Trevor D. Brown. All rights reserved.
#   This project is distributed under the MIT license.
#
#   File:       dashar-das.py
#   Purpose:    This script is the backend/middleware service for the DashAR system.
#

import das_core.obdii_interpreter
import datetime
import sys
import signal

def ctrl_c_pressed(sig, frame):
    # Set the active loop flag to False.
    global flagActiveLoop
    flagActiveLoop = False

def main() -> None:

    # Initialization
    global flagActiveLoop
    flagActiveLoop = True

    # Register CTRL+C signal.
    signal.signal(signal.SIGINT, ctrl_c_pressed)

    dasharOBDIIObject = das_core.obdii_interpreter.OBDIIContext()

    # Main Loop
    while (flagActiveLoop):
        # print(dasharOBDIIObject, end="\033[F\033[A\033[A\033[A\033[A\033[A")
        print(f"Date Fetched (Epoch): {datetime.datetime.now(tz=datetime.timezone.utc).timestamp()}", end="\033[F\033[A")

if (__name__ == "__main__"):
    main()
