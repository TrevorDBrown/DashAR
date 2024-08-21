#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024 Trevor D. Brown. All rights reserved.
#   This project is distributed under the MIT license.
#
#   File:       dashar-das.py
#   Purpose:    This script is the backend/middleware service for the DashAR system.
#

import das_core.obdii_interpreter

def main() -> None:
    dasharOBDIIObject = das_core.obdii_interpreter.OBDIIContext('/path/to/obdii/interface')

    print(dasharOBDIIObject)

if (__name__ == "__main__"):
    main()
