#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       pyvin-wrap.py
#   Purpose:    A wrapper for the pyvin library, designed for the DashAR system.
#

import pyvin

class PyVIN:

    def __init__(self) -> None:
        return

    @staticmethod
    def decode_vin(vin: str) -> dict:
        decoded_vin: dict = {}

        results: dict = pyvin.VIN(vin)
                                                        # Example: 2013 Hyundai Sonata
        decoded_vin['year'] = results.ModelYear         # 2013
        decoded_vin['make'] = results.Make.title()      # Hyundai (decoded as HYUNDAI)
        decoded_vin['model'] = results.Model            # Sonata

if (__name__ == "__main__"):
    print("This extension should be used as an import for the DashAR System.")
