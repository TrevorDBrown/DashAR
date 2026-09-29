#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2026 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       data_connector.pyi
#

from das_core.helper import (
    DataSourceType as DataSourceType,
    ServiceMode as ServiceMode,
    SharedFunctions as SharedFunctions,
)

class DataConnection:
    def __init__(
        self,
        data_filename: str,
        data_source_type: DataSourceType = ...,
        service_mode: ServiceMode = ...,
    ) -> None: ...
    def insert_into_database(self, insert_statement: str) -> bool: ...
    def select_from_database(self, select_statement: str) -> str: ...

def main() -> None: ...
