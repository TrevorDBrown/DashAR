#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2026 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       pyvin-wrap.py
#

"""
Purpose: A DAS Extension that captures automobile details from a VIN number.
Essentially, a wrapper for the pyvin library.
"""

import pyvin

class PyVIN:

    """
    The primary class for the VIN DAS extension.
    """

    def __init__(self) -> None:
        return

    @staticmethod
    def decode_vin(vin: str) -> dict:
        decoded_vin: dict = {}

        results: pyvin.DecodedVIN = pyvin.VIN(vin, error_handling="RAISE")
                                                        # Example: 2013 Hyundai Sonata
        decoded_vin["year"] = results.ModelYear         # 2013
        decoded_vin["make"] = results.Make.title()      # Hyundai (decoded as HYUNDAI)
        decoded_vin["model"] = results.Model            # Sonata

        return decoded_vin

if (__name__ == "__main__"):
    print("This extension should be used as an import for the DashAR System.")
