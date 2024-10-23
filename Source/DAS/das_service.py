#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024 Trevor D. Brown. All rights reserved.
#   This project is distributed under the MIT license.
#
#   File:       das_service.py
#   Purpose:    This script is the backend/middleware service (Data Aggregator and Server) for the DashAR system.
#
from das_core.configuration import Configuration
from das_core.helper import Constants, SharedFunctions, ServiceMode
from das_core.obdii_interpreter import OBDIIContext

import argparse
import asyncio
import tornado
import time
import random

class OBDIIHandler(tornado.web.RequestHandler):
    dashar_configuration: Configuration

    def initialize(self, dashar_configuration: Configuration) -> None:
        self.dashar_configuration = dashar_configuration

    def get(self) -> None:
        client_response_json: str

        if (self.dashar_configuration.configuration_variables.service_mode == ServiceMode.TEST):
            client_response_json = SharedFunctions.convert_dict_to_json({
                "current_timestamp": SharedFunctions.get_current_timestamp(),
                "obdii_data": {"speed": random.randint(0, 100), "rpm": random.randint(500, 5000), "fuel_level": random.randint(0,100)}
            })

            self.set_header("Content-Type", "application/json")
            self.set_status(200, "OK")
            self.write(f"{client_response_json}")


        elif (self.dashar_configuration.obdii_context.is_connected()):
            current_obdii_data_snapshot: dict = self.dashar_configuration.obdii_context.capture_data_points()

            client_response_json = SharedFunctions.convert_dict_to_json({
                "current_timestamp": SharedFunctions.get_current_timestamp(),
                "obdii_data": current_obdii_data_snapshot
            })

            self.set_header("Content-Type", "application/json")
            self.set_status(200, "OK")
            self.write(f"{client_response_json}")

        else:
            client_response_json = SharedFunctions.convert_dict_to_json({
                "current_timestamp": SharedFunctions.get_current_timestamp(),
                "obdii_data": {"Message": "Not Available."}
            })

            self.set_header("Content-Type", "application/json")
            self.set_status(503, "OBDII is not available.")
            self.write(f"{client_response_json}")

class ThirdPartyAPIHandler(tornado.web.RequestHandler):
    dashar_configuration: Configuration

    def initialize(self, dashar_configuration: Configuration) -> None:
        self.dashar_configuration = dashar_configuration

    def get(self) -> None:
        self.write("This endpoint is for third-party API calls.")

class InitHandler(tornado.web.RequestHandler):
    dashar_configuration: Configuration

    def initialize(self, dashar_configuration: Configuration) -> None:
        self.dashar_configuration = dashar_configuration

    def get(self) -> None:
        self.write("Initializing...")

class TerminateHandler(tornado.web.RequestHandler):
    dashar_configuration: Configuration

    def initialize(self, dashar_configuration: Configuration) -> None:
        self.dashar_configuration = dashar_configuration

    def _terminate(self) -> None:
        print("Termination signal received from /quit endpoint.")

        # event_loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

        # event_loop.stop()
        # event_loop.close()

        return

    def get(self) -> None:
        self.write("Termination signal received.")
        self._terminate()

def make_app(dashar_configuration: Configuration) -> tornado.web.Application:
    return tornado.web.Application([
        (r"/init", InitHandler, {"dashar_configuration": dashar_configuration}),
        (r"/quit", TerminateHandler, {"dashar_configuration": dashar_configuration}),
        (r"/data/obdii", OBDIIHandler, {"dashar_configuration": dashar_configuration}),
        (r"/data/tpapi", ThirdPartyAPIHandler, {"dashar_configuration": dashar_configuration})
    ])

def check_for_arguments():
    # Check for arguments.
    argument_parser = argparse.ArgumentParser(  prog='das_service.py',
                                                description='The Data Aggregator and Server Component of the DashAR System.')

    argument_parser.add_argument("-v", "--verbose", action="store_true", help="Output additional information at runtime.")
    argument_parser.add_argument("--headless", action="store_true", help="Capture data points without external requests.")

    return argument_parser.parse_args()

async def main() -> None:

    # Check for arguments.
    arguments: argparse.Namespace = check_for_arguments()

    # Initialization
    dashar_configuration: Configuration = Configuration(arguments)

    http_port: int = 3832

    if (not dashar_configuration.configuration_variables.headless_operation):

        app: tornado.web.Application = make_app(dashar_configuration)

        print(f"\nSystem ready on port {http_port}.\n")

        app.listen(http_port)
        await asyncio.Event().wait()
        await asyncio.Event().wait()

    else:

        sleep_time: float = 0.5

        print(f"DAS is running headless mode. Data will be captured over set time frequency (currently {sleep_time} seconds between calls).")


        while True:
            if (dashar_configuration.obdii_context.is_connected()):
                # Capture OBDII data points.
                obdii_response: dict = dashar_configuration.obdii_context.capture_data_points()

                print(obdii_response)

                # Wait specified time before trying again.
                time.sleep(sleep_time)

            else:
                print("OBDII is not connected. Exiting.")
                break

    print("System has terminated.")


if (__name__ == "__main__"):
    asyncio.run(main())
