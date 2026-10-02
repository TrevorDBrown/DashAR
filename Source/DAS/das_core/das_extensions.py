#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       das_extensions.py
#

"""Purpose: the extensions manager used by the DAS API for the DashAR system."""

# import json
# import importlib

import textwrap
import pythonping as pp

class DASExtension:
    """
    The core DAS API extension class.
    """

    _functional: bool = True
    _name: str = ""
    _description: str = ""
    _path: str = ""
    _module: str = ""
    _functions: list = []

    def __init__(self, name: str, description: str, path: str, module: str, functions: dict) -> None:
        # Basic Information
        self._name = name
        self._description = description
        self._path = path
        self._module = module

        for function in functions:
            new_function: dict = {}

            new_function["function_name"] = function["function_name"]
            new_function["static_function"] = function["static_function"]
            new_function["parameters"] = function["parameters"]
            new_function["return_type"] = function["return_type"]
            new_function["requirements"] = self._validate_requirements(function["requirements"])

            if (not self._functional):
                print("Error: Requirement(s) failed to validate. Extension will not be loaded.")

            self._functions.append(new_function)

        return

    def _validate_requirements(self, requirements: list) -> dict:

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
                        # Ping Google's DNS server, beacuse Google DNS never goes down... right?!
                        # To force a failure, use 169.254.254.254.
                        pp.ping("8.8.8.8")
                        requirements_checklist["Internet"] = True

                    except Exception as e:
                        requirements_checklist["Internet"] = False
                        requirements_validation = False

                        print("Error: unable to validate internet connectivity.")
                        print(f"Exception: {e}")

        if (requirements_validation and self._functional):
            self._functional = True
        else:
            self._functional = False

        return requirements_checklist

    def is_functional(self) -> bool:
        return self._functional

    def __str__(self) -> str:
        returned_extension_str: str = ""

        returned_extension_str += textwrap.dedent(f"""
                Extension: {self._name}
                    Description: {self._description}
                    Path: {self._path}
                    Module Name: {self._module}
                    Functions:
                        {self._functions}
        """)

        return returned_extension_str

class DASExtensions:
    """
    The bundle of DAS extensions that were imported, regardless of functionality.
    """

    extensions_list: list = []              # Extensions that are functional and ready-to-use.
    disabled_extensions_list: list = []     # Extensions with issues.

    def __init__(self) -> None:
        self.extensions_list = []
        self.disabled_extensions_list = []
        return

    def register_extension(self, name: str, description: str, path: str, module: str, functions: dict) -> bool:

        # Register the extension.
        new_das_extension: DASExtension = DASExtension(
            name=name,
            description=description,
            path=path,
            module=module,
            functions=functions
        )

        # Store the extension, if it is functional.
        if (new_das_extension.is_functional()):
            self.extensions_list.append(new_das_extension)
        else:
            self.disabled_extensions_list.append(new_das_extension)
            return False

        return True

    def import_extensions(self) -> bool:
        return False
        # TODO: implement import functionality.

    def __str__(self) -> str:
        returned_extensions_str: str = ""

        active_extensions_count: int = len(self.extensions_list)
        disable_extensions_count: int = len(self.disabled_extensions_list)
        total_extensions_count: int = active_extensions_count + disable_extensions_count

        returned_extensions_str += f"Active Extensions ({active_extensions_count}/{total_extensions_count}): \n"

        if (active_extensions_count <= 0):
            returned_extensions_str += "\tN/A"

        for extension in self.extensions_list:
            returned_extensions_str += str(extension)

        returned_extensions_str += f"\nDisabled Extensions ({disable_extensions_count}/{total_extensions_count}): \n"

        if (disable_extensions_count <= 0):
            returned_extensions_str += "\tN/A\n"

        for extension in self.disabled_extensions_list:
            returned_extensions_str += str(extension)

        return returned_extensions_str

if __name__ == "__main__":
    print(f"This module ({__file__}) should be invoked as an import.")
