#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       das_extensions.py
#   Purpose:    This script manages the extensions for DashAR.
#

import json
import importlib

import textwrap

import pythonping as pp

class DASExtension:
    __functional: bool = True
    __name: str = ""
    __description: str = ""
    __path: str = ""
    __module: str = ""
    __functions: list = []

    def __init__(self, name: str, description: str, path: str, module: str, functions: dict) -> None:
        # Basic Information
        self.__name = name
        self.__description = description
        self.__path = path
        self.__module = module

        for function in functions:
            new_function: dict = {}

            new_function["function_name"] = function["function_name"]
            new_function["static_function"] = function["static_function"]
            new_function["parameters"] = function["parameters"]
            new_function["return_type"] = function["return_type"]
            new_function["requirements"] = self.__validate_requirements(function["requirements"])

            if (not self.__functional):
                print("Error: Requirement(s) failed to validate. Extension will not be loaded.")

            self.__functions.append(new_function)

        return

    def __validate_requirements(self, requirements: list) -> dict:

        requirements_validation: bool = True

        # Possible values in checklist:
        # - "N/A" (str) - requirement was not tested.
        # - True (bool) - requirement tested and available.
        # - False (bool) - requirement test and unavailable.
        requirements_checklist: dict = {
            "Internet": "N/A"
        }

        for requirement in requirements:
            if requirement in requirements_checklist:

                # For Internet requirement, validate the Internet is accessible.
                if (requirement == "Internet"):
                    try:
                        pp.ping('8.8.8.8')     # Beacuse Google DNS never goes down... right?! (to make fail, use 169.254.254.254)
                        requirements_checklist["Internet"] = True

                    except:
                        requirements_checklist["Internet"] = False
                        requirements_validation = False

        if (requirements_validation and self.__functional):
            self.__functional = True
        else:
            self.__functional = False

        return requirements_checklist

    def is_functional(self) -> bool:
        return self.__functional

    def __str__(self) -> str:
        returned_extension_str: str = ""

        returned_extension_str += textwrap.dedent(f"""
                Extension: {self.__name}
                    Description: {self.__description}
                    Path: {self.__path}
                    Module Name: {self.__module}
                    Functions:
                        {self.__functions}
        """)

        return returned_extension_str

class DASExtensions:

    # Object Variables
    extensions_list: list = []              # Functional, ready-to-use extensions.
    disabled_extensions_list: list = []     # Non-functional extensions.

    def __init__(self) -> None:
        self.extensions_list = []
        self.disabled_extensions_list = []
        return

    def register_extension(self, name: str, description: str, path: str, module: str, functions: dict) -> bool:

        # Register the extension.
        new_das_extension: DASExtension = DASExtension(name=name, description=description, path=path, module=module, functions=functions)

        # Store the extension, if it is functional.
        if (new_das_extension.is_functional()):
            self.extensions_list.append(new_das_extension)
        else:
            self.disabled_extensions_list.append(new_das_extension)

    def import_extensions(self) -> bool:
        None
        # TODO: implement import functionality.

    def __str__(self) -> str:
        returned_extensions_str: str = ""

        active_extensions_count: int = len(self.extensions_list)
        disable_extensions_count: int = len(self.disabled_extensions_list)
        total_extensions_count: int = active_extensions_count + disable_extensions_count

        returned_extensions_str += f"Active Extensions ({active_extensions_count}/{total_extensions_count}): \n"

        if (active_extensions_count <= 0):
            returned_extensions_str += "\tN/A"

        for i, extension in enumerate(self.extensions_list):
            returned_extensions_str += str(extension)

        returned_extensions_str += f"\nDisabled Extensions ({disable_extensions_count}/{total_extensions_count}): \n"

        if (disable_extensions_count <= 0):
            returned_extensions_str += "\tN/A\n"

        for i, extension in enumerate(self.disabled_extensions_list):
            returned_extensions_str += str(extension)

        return returned_extensions_str

if __name__ == "__main__":
    print(f"This module ({__file__}) should be invoked as an import.")
