#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2026 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       data_connector.pyi
#

"""Purpose: the data manager used by the DAS API for the DashAR system."""

# pylint: skip-file

from das_core.helper import (
    DataSourceType as DataSourceType,
    SharedFunctions as SharedFunctions,
)

class DataConnection:
    """
    A class for specifying a data connection.
    """

    def __init__(
        self,
        data_filename: str,
        data_source_type: DataSourceType = ...,
    ) -> None: ...
    def insert_into_database(self, insert_statement: str) -> bool: ...
    def select_from_database(self, select_statement: str) -> str: ...

def main() -> None: ...
