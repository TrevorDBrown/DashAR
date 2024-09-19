#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024 Trevor D. Brown. All rights reserved.
#   This project is distributed under the MIT license.
#
#   File:       data_connector.py
#   Purpose:    This script manages the data connections, such as the database and to any files.
#

from das_core.helper import Constants, SharedFunctions, ServiceMode, DataSourceType
import sqlite3

class DataConnection:

    # Object Variables
    __id: str                                   # __id - a UUIDv4 value, used to uniquely identify the data connection context.
    __created_timestamp: float                  # __created_timestamp - the Unix timestamp of when the object was created.
    __data_source: DataSourceType               # __data_source - the type of data source being used (e.g. DATABASE, DIRECT_FILE)
    __data_filename: str                        # __data_filename - the filename of the data source.

    # Data Source-specific Variables
    # Database (SQLite3)
    __database_connection: sqlite3.Connection   # __database_connection - a Database connection.

    # Direct File
    __direct_file: str  # TODO: determine best data type hint for this.

    def __init__(self, data_filename: str, data_source_type: DataSourceType = DataSourceType.DIRECT_FILE, service_mode: ServiceMode = ServiceMode.DEBUG) -> None:

        self.__id = SharedFunctions.generate_object_id()
        self.__created_timestamp = SharedFunctions.get_current_timestamp()

        try:
            self.__data_source = data_source_type
            self.__data_filename = data_filename

        except FileNotFoundError as fnfe:
            print(f"Error: File Not Found - {data_filename}")
            print(fnfe)

        except Exception as e:
            print("An exception occurred.")
            print(e)

    # Database (SQLite3) functions
    def __connect_to_database(self) -> bool:
        self.__database_connection = sqlite3.connect(self.__data_filename)
        return True

    def __disconnect_from_database(self) -> bool:
        self.__database_connection.close()
        return True

    def insert_into_database(self, insert_statement: str) -> bool:
        successful_connection: bool = self.__connect_to_database()

        if (successful_connection):
            database_cursor: sqlite3.Cursor = self.__database_connection.cursor()
            database_cursor.execute(insert_statement)
            self.__database_connection.commit()
            self.__disconnect_from_database()
        else:
            return False

        return True


def main() -> None:

    print(f"This module ({__file__}) should be invoked as an import.")

    return

if __name__ == "__main__":
    main()
