#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       das_service.py
#   Purpose:    This script is the backend/middleware service (Data Aggregator and Server) for the DashAR system.
#

from das_core.configuration import Configuration
from das_core.helper import Constants, SharedFunctions, ServiceMode, SystemStatus

import argparse
import asyncio
import tornado

class DashARWelcomeHandler(tornado.web.RequestHandler):
    def initialize(self):
        None

    def get(self) -> None:
        client_response_json = SharedFunctions.convert_dict_to_json({
            "current_timestamp": SharedFunctions.get_current_timestamp(),
            "status": "Welcome",
            "message": "The configuration will be retrieved momentarily."
        })

        self.set_header("Content-Type", "application/json")
        self.set_status(200, "OK")
        self.write(f"{client_response_json}")

class DashARStatusHandler(tornado.web.RequestHandler):
    dashar_configuration: Configuration

    def initialize(self, dashar_configuration: Configuration) -> None:
        self.dashar_configuration = dashar_configuration

    def get(self) -> None:
        client_response_json = SharedFunctions.convert_dict_to_json({
            "current_timestamp": SharedFunctions.get_current_timestamp(),
            "status": self.dashar_configuration.configuration_variables.system_status.name,
            "message": ""
        })

        self.set_header("Content-Type", "application/json")
        self.set_status(200, "OK")
        self.write(f"{client_response_json}")

class DashARHUDHandler(tornado.web.RequestHandler):
    dashar_configuration: Configuration

    def initialize(self, dashar_configuration: Configuration) -> None:
        self.dashar_configuration = dashar_configuration

    def get(self) -> None:

        client_response_json = SharedFunctions.convert_dict_to_json({
            "current_timestamp": SharedFunctions.get_current_timestamp(),
            "hud_configuration_base": self.dashar_configuration.configuration_variables.hud_configuration_base_json_content,
            "hud_configuration_widgets": self.dashar_configuration.configuration_variables.hud_configuration_widgets_json_content
        })

        self.set_header("Content-Type", "application/json")
        self.set_status(200, "OK")
        self.write(f"{client_response_json}")

class OBDIIHandler(tornado.web.RequestHandler):
    dashar_configuration: Configuration

    def initialize(self, dashar_configuration: Configuration) -> None:
        self.dashar_configuration = dashar_configuration

    def get(self) -> None:
        client_response_json: str

        if (self.dashar_configuration.configuration_variables.service_mode == ServiceMode.TEST):
            current_obdii_data_snapshot: dict = self.dashar_configuration.obdii_context.capture_data_points()

            client_response_json = SharedFunctions.convert_dict_to_json({
                "current_timestamp": SharedFunctions.get_current_timestamp(),
                "obdii_data": current_obdii_data_snapshot,
                "message": "Test Mode. Value are randomized."
            })

            self.set_header("Content-Type", "application/json")
            self.set_status(200, "OK")
            self.write(f"{client_response_json}")


        elif (self.dashar_configuration.obdii_context.is_connected()):
            current_obdii_data_snapshot: dict = self.dashar_configuration.obdii_context.capture_data_points()

            client_response_json = SharedFunctions.convert_dict_to_json({
                "current_timestamp": SharedFunctions.get_current_timestamp(),
                "obdii_data": current_obdii_data_snapshot,
                "message": ""
            })

            self.set_header("Content-Type", "application/json")
            self.set_status(200, "OK")
            self.write(f"{client_response_json}")

        else:
            client_response_json = SharedFunctions.convert_dict_to_json({
                "current_timestamp": SharedFunctions.get_current_timestamp(),
                "obdii_data": {},
                "message": "Not Available."
            })

            self.set_header("Content-Type", "application/json")
            self.set_status(503, "OBDII is not available.")
            self.write(f"{client_response_json}")

class TerminateHandler(tornado.web.RequestHandler):
    # This is currently not implemented.
    dashar_configuration: Configuration
    event_loop: tornado.locks.Event

    def initialize(self, event_loop: tornado.locks.Event, dashar_configuration: Configuration) -> None:
        self.event_loop = event_loop
        self.dashar_configuration = dashar_configuration

    def _terminate(self) -> None:
        print("Terminate functionality not implemented.")
        return

    def get(self) -> None:

        client_response_json = SharedFunctions.convert_dict_to_json({
                "current_timestamp": SharedFunctions.get_current_timestamp(),
                "obdii_data": {},
                "message": "Termination signal received."
            })

        self.set_header("Content-Type", "application/json")
        self.set_status(202, "Termination signal received.")
        self.write(f"{client_response_json}")

        self._terminate()

class UnimplementedHandler(tornado.web.RequestHandler):

    def get(self) -> None:
        client_response_json = SharedFunctions.convert_dict_to_json({
            "current_timestamp": SharedFunctions.get_current_timestamp(),
            "obdii_data": {},
            "message": "Unimplemented endpoint."
        })

        self.set_header("Content-Type", "application/json")
        self.set_status(501, "Unimplemented endpoint.")
        self.write(f"{client_response_json}")

class NotFoundHandler(tornado.web.RequestHandler):
    def get(self) -> None:
        client_response_json = SharedFunctions.convert_dict_to_json({
            "current_timestamp": SharedFunctions.get_current_timestamp(),
            "obdii_data": {},
            "message": "Resource not found."
        })

        self.set_header("Content-Type", "application/json")
        self.set_status(404, "Resource not found.")
        self.write(f"{client_response_json}")

class FailedInitHandler(tornado.web.RequestHandler):
    def get(self) -> None:
        client_response_json = SharedFunctions.convert_dict_to_json({
            "current_timestamp": SharedFunctions.get_current_timestamp(),
            "obdii_data": {},
            "message": "Failed to initialize system. Please restart ICS."
        })

        self.set_header("Content-Type", "application/json")
        self.set_status(503, "Failed to initialize system.")
        self.write(f"{client_response_json}")

def make_app(event_loop: tornado.locks.Event, dashar_configuration: Configuration) -> tornado.web.Application:

    routes: list = [
        (r"/dashar/welcome", DashARWelcomeHandler),
        (r"/dashar/status", DashARStatusHandler, {"dashar_configuration": dashar_configuration}),
        (r"/dashar/hud/config", DashARHUDHandler, {"dashar_configuration": dashar_configuration}),
        (r"/dashar/data/obdii", OBDIIHandler, {"dashar_configuration": dashar_configuration}),
        (r"/dashar/quit", UnimplementedHandler),
        (r"/dashar/data/tpapi", UnimplementedHandler),
        (r"/.*", NotFoundHandler)
    ]

    return tornado.web.Application(routes)

def make_app_failed_init(event_loop: tornado.locks.Event, dashar_configuration: Configuration) -> tornado.web.Application:

    routes: list = [
        (r"/dashar/status", DashARStatusHandler, {"dashar_configuration": dashar_configuration}),
        (r"/dashar/data/obdii", FailedInitHandler),
        (r"/.*", NotFoundHandler)
    ]

    return tornado.web.Application(routes)

def check_for_arguments():
    # Check for arguments.
    argument_parser = argparse.ArgumentParser(  prog='das_service.py',
                                                description='The Data Aggregator and Server Service of the DashAR System.')

    argument_parser.add_argument("-v", "--verbose", action="store_true", help="Output additional information at runtime.")

    return argument_parser.parse_args()

async def main() -> None:

    # Check for arguments.
    arguments: argparse.Namespace = check_for_arguments()

    # Initialization
    dashar_configuration: Configuration = Configuration(arguments)

    # Establish an event loop.
    event_loop: tornado.locks.Event = tornado.locks.Event()

    # If DashAR failed to initialize, set up the system to respond accordingly to request.
    print(f"System Status is {dashar_configuration.configuration_variables.system_status.name}.")

    if (dashar_configuration.configuration_variables.system_status == SystemStatus.FAILED):
        print("\nError: DashAR unable to initialize successfully. Please manually restart service.")
        app: tornado.web.Application = make_app_failed_init(event_loop, dashar_configuration)

    # Otherwise, have fun!
    else:
        print(f"\nDashAR ready on port {dashar_configuration.configuration_variables.das_server_port}.\n")
        app: tornado.web.Application = make_app(event_loop, dashar_configuration)

    # In both instances, listen for a response on the defined port.
    app.listen(dashar_configuration.configuration_variables.das_server_port)

    # Wait for requests.
    await event_loop.wait()

    # TODO: find a graceful way to terminate the script.
    print("System has terminated.")
    return

if (__name__ == "__main__"):
    asyncio.run(main())
