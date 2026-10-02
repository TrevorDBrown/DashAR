#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2026 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       das_extensions.pyi
#

"""Purpose: the extensions manager used by the DAS API for the DashAR system."""

# pylint: skip-file

class DASExtension:
    """
    The core DAS API extension class.
    """

    def __init__(
        self, name: str, description: str, path: str, module: str, functions: dict
    ) -> None: ...
    def is_functional(self) -> bool: ...

class DASExtensions:
    """
    The bundle of DAS extensions that were imported, regardless of functionality.
    """

    extensions_list: list
    disabled_extensions_list: list
    def __init__(self) -> None: ...
    def register_extension(
        self, name: str, description: str, path: str, module: str, functions: dict
    ) -> bool: ...
    def import_extensions(self) -> bool: ...
