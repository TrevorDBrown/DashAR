#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       data_connector.py
#

"""Purpose: the data manager used by the DAS API for the DashAR system."""

from das_core.helper import SharedFunctions, DataSourceType
import sqlite3


class DataConnection:
    """
    A class for specifying a data connection.
    """

    _id: str  # __id - a UUIDv4 value, used to uniquely identify the data connection context.
    _created_timestamp: float  # __created_timestamp - the Unix timestamp of when the object was created.
    _data_source: DataSourceType  # __data_source - the type of data source being used (e.g. DATABASE, DIRECT_FILE)
    _data_filename: str  # __data_filename - the filename of the data source.

    # Data Source-specific Variables
    # Database (SQLite3)
    _database_connection: (
        sqlite3.Connection
    )  # __database_connection - a Database connection.

    # Direct File
    _direct_file: str  # TODO: determine best data type hint for this.

    def __init__(
        self,
        data_filename: str,
        data_source_type: DataSourceType,
    ) -> None:
        self._id = SharedFunctions.generate_object_id()
        self._created_timestamp = SharedFunctions.get_current_timestamp()

        try:
            self._data_source = data_source_type
            self._data_filename = data_filename

        except FileNotFoundError as fnfe:
            print(f"Error: File Not Found - {data_filename}")
            print(fnfe)

        except Exception as e:
            print("An exception occurred.")
            print(e)

    # Database (SQLite3) functions
    def _connect_to_database(self) -> bool:
        self.__database_connection = sqlite3.connect(self.__data_filename)
        return True

    def _disconnect_from_database(self) -> bool:
        self.__database_connection.close()
        return True

    def insert_into_database(self, insert_statement: str) -> bool:
        successful_connection: bool = self._connect_to_database()

        if successful_connection:
            database_cursor: sqlite3.Cursor = self._database_connection.cursor()
            database_cursor.execute(insert_statement)
            self._database_connection.commit()
            self._disconnect_from_database()
        else:
            return False

        return True

    def select_from_database(self, select_statement: str) -> str:
        successful_connection: bool = self._connect_to_database()

        if successful_connection:
            database_cursor: sqlite3.Cursor = self._database_connection.cursor()
            results: sqlite3.Cursor = database_cursor.execute(select_statement)
            self.__disconnect_from_database()

            # TODO: implement results retrieval.
            return results

        else:
            # No connection to database.
            return ""

if __name__ == "__main__":
    print(f"This module ({__file__}) should be invoked as an import.")
