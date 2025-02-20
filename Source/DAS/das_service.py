#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2025 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       das_service.py
#

"""Purpose: the backend/middleware service (Data Aggregator and Server) for the DashAR system."""

# pylint: disable=W0223,C0325,R1711
# For linting purposes, the above lint codes have been ignored:
#   - W0223 - abstract methods not needed.
#   - C0325 - prefer parentheses around if conditions every time.
#   - R1711 - prefer return statements every time, regardless if anything is returned.

import argparse
import asyncio
import tornado

from das_core.configuration import Configuration
from das_core.helper import SharedFunctions, ServiceMode, SystemStatus

class DashARWelcomeHandler(tornado.web.RequestHandler):
    """
    A class for handling requests on endpoint: /dashar/welcome.
    """

    def initialize(self) -> None:
        """
        Initializes the class.

        Args:
            None

        Returns:
            None
        """

        return

    def get(self) -> None:
        """
        GET request handler for /dashar/welcome.

        Args:
            None

        Returns:
            None
        """

        client_response_json = SharedFunctions.convert_dict_to_json({
            "current_timestamp": SharedFunctions.get_current_timestamp(),
            "status": "Welcome",
            "message": "The configuration will be retrieved momentarily."
        })

        self.set_header("Content-Type", "application/json")
        self.set_status(200, "OK")
        self.write(f"{client_response_json}")

        return

class DashARStatusHandler(tornado.web.RequestHandler):
    """
    A class for handling requests on endpoint: /dashar/status.
    """

    dashar_configuration: Configuration

    def initialize(self, dashar_configuration: Configuration) -> None:
        """
        Initializes the class. Stores the DashAR configuration.

        Args:
            dashar_configuration (Configuration): the instance of the Configuration class.

        Returns:
            None
        """

        self.dashar_configuration = dashar_configuration

        return

    def get(self) -> None:
        """
        GET request handler for /dashar/status.

        Args:
            None

        Returns:
            None
        """

        client_response_json = SharedFunctions.convert_dict_to_json({
            "current_timestamp": SharedFunctions.get_current_timestamp(),
            "status": self.dashar_configuration.configuration_variables.system_status.name,
            "message": ""
        })

        self.set_header("Content-Type", "application/json")
        self.set_status(200, "OK")
        self.write(f"{client_response_json}")

        return

class DashARHUDHandler(tornado.web.RequestHandler):
    """
    A class for handling requests on endpoint: /dashar/hud/config
    """

    dashar_configuration: Configuration

    def initialize(self, dashar_configuration: Configuration) -> None:
        """
        Initializes the class. Stores the DashAR configuration.

        Args:
            dashar_configuration (Configuration): the instance of the Configuration class.

        Returns:
            None
        """

        self.dashar_configuration = dashar_configuration

        return

    def get(self) -> None:
        """
        GET request handler for /dashar/hud/config.

        Args:
            None

        Returns:
            None
        """

        client_response_json = SharedFunctions.convert_dict_to_json({
            "current_timestamp": SharedFunctions.get_current_timestamp(),
            "hud_configuration_base": self.dashar_configuration.configuration_variables.\
                hud_configuration_base_json_content,
            "hud_configuration_widgets": self.dashar_configuration.configuration_variables.\
                hud_configuration_widgets_json_content
        })

        self.set_header("Content-Type", "application/json")
        self.set_status(200, "OK")
        self.write(f"{client_response_json}")

        return

class OBDIIHandler(tornado.web.RequestHandler):
    """
    A class for handling requests on endpoint: /dashar/data/obdii
    """

    dashar_configuration: Configuration

    def initialize(self, dashar_configuration: Configuration) -> None:
        """
        Initializes the class. Stores the DashAR Configuration.

        Args:
            dashar_configuration (Configuration): the instance of the Configuration class.

        Returns:
            None
        """

        self.dashar_configuration = dashar_configuration

        return

    def get(self) -> None:
        """
        GET request handler for /dashar/data/obdii.

        Args:
            None

        Returns:
            None
        """

        client_response_json: str
        current_obdii_data_snapshot: dict

        if (self.dashar_configuration.configuration_variables.service_mode == ServiceMode.TEST):
            current_obdii_data_snapshot = self.dashar_configuration.\
                obdii_context.capture_data_points()

            client_response_json = SharedFunctions.convert_dict_to_json({
                "current_timestamp": SharedFunctions.get_current_timestamp(),
                "obdii_data": current_obdii_data_snapshot,
                "message": "Test Mode. Value are randomized."
            })

            self.set_header("Content-Type", "application/json")
            self.set_status(200, "OK")
            self.write(f"{client_response_json}")


        elif (self.dashar_configuration.obdii_context.is_connected()):
            current_obdii_data_snapshot = self.dashar_configuration.obdii_context.\
                capture_data_points()

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

        return

class TerminateHandler(tornado.web.RequestHandler):
    """
    A class for handling requests on endpoint: /dashar/quit
    """

    dashar_configuration: Configuration
    event_loop: tornado.locks.Event

    def initialize(self, \
                   event_loop: tornado.locks.Event, \
                   dashar_configuration: Configuration \
                    ) -> None:
        """
        Initializes the class.

        Args:
            None

        Returns:
            None
        """

        self.event_loop = event_loop
        self.dashar_configuration = dashar_configuration

    def _terminate(self) -> None:
        """
        Performs the termination process for the system.

        Args:
            None

        Returns:
            None
        """

        print("Terminate functionality not implemented.")

        return

    def get(self) -> None:
        """
        GET request handler for /dashar/quit.

        Args:
            None

        Returns:
            None
        """

        client_response_json = SharedFunctions.convert_dict_to_json({
                "current_timestamp": SharedFunctions.get_current_timestamp(),
                "obdii_data": {},
                "message": "Termination signal received."
            })

        self.set_header("Content-Type", "application/json")
        self.set_status(202, "Termination signal received.")
        self.write(f"{client_response_json}")

        self._terminate()

        return

class UnimplementedHandler(tornado.web.RequestHandler):
    """
    A class for handling requests on unimplemented endpoints.
    """

    def initialize(self):
        """
        Initializes the class.

        Args:
            None

        Returns:
            None
        """

        return

    def get(self) -> None:
        """
        GET request handler for unimplemented endpoints.

        Args:
            None

        Returns:
            None
        """

        client_response_json = SharedFunctions.convert_dict_to_json({
            "current_timestamp": SharedFunctions.get_current_timestamp(),
            "obdii_data": {},
            "message": "Unimplemented endpoint."
        })

        self.set_header("Content-Type", "application/json")
        self.set_status(501, "Unimplemented endpoint.")
        self.write(f"{client_response_json}")

        return

class NotFoundHandler(tornado.web.RequestHandler):
    """
    A class for handling requests for non-existent endpoints.
    """

    def initialize(self) -> None:
        """
        Initializes the class.

        Args:
            None

        Returns:
            None
        """

        return

    def get(self) -> None:
        """
        GET request handler for non-existent endpoints.

        Args:
            None

        Returns:
            None
        """

        client_response_json = SharedFunctions.convert_dict_to_json({
            "current_timestamp": SharedFunctions.get_current_timestamp(),
            "obdii_data": {},
            "message": "Resource not found."
        })

        self.set_header("Content-Type", "application/json")
        self.set_status(404, "Resource not found.")
        self.write(f"{client_response_json}")

        return

class FailedInitHandler(tornado.web.RequestHandler):
    """
    A class for handling initialization failures.
    """

    def initialize(self) -> None:
        """
        Initializes the class.

        Args:
            None

        Returns:
            None
        """

        return

    def get(self) -> None:
        """
        GET request handler for initialization failures endpoint.

        Args:
            None

        Returns:
            None
        """

        client_response_json = SharedFunctions.convert_dict_to_json({
            "current_timestamp": SharedFunctions.get_current_timestamp(),
            "obdii_data": {},
            "message": "Failed to initialize system. Please restart ICS."
        })

        self.set_header("Content-Type", "application/json")
        self.set_status(503, "Failed to initialize system.")
        self.write(f"{client_response_json}")

        return

def make_app(dashar_configuration: Configuration) -> tornado.web.Application:

    """
    Generates the Data Aggregator and Server (DAS) API application.

    Args:
        dashar_configuration (Configuration): the instance of the Configuration class.

    Returns:
        tornado.web.Application: an instance of a Tornado web application.
    """

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

def make_app_failed_init(dashar_configuration: Configuration) -> tornado.web.Application:

    """
    Generates a bare-bones Tornado application for errors.

    Args:
        dashar_configuration (Configuration): the instance of the Configuration class.

    Returns:
        tornado.web.Application: an instance of a Tornado web application.
    """

    routes: list = [
        (r"/dashar/status", DashARStatusHandler, {"dashar_configuration": dashar_configuration}),
        (r"/dashar/data/obdii", FailedInitHandler),
        (r"/.*", NotFoundHandler)
    ]

    return tornado.web.Application(routes)

def check_for_arguments() -> argparse.Namespace:
    """
    Checks sys.argv for any arguments passed into the application.

    Args:
        None

    Returns:
        argparse.Namespace
    """

    argument_parser = argparse.ArgumentParser(  prog='das_service.py', \
                        description='The Data Aggregator and Server Service of the DashAR System.')

    argument_parser.add_argument("-v", "--verbose", \
                                    action="store_true", \
                                    help="Output additional information at runtime.")

    return argument_parser.parse_args()

async def main() -> None:
    """
    The main function of the script.

    Args:
        None

    Returns:
        None
    """

    # Check for arguments.
    arguments: argparse.Namespace = check_for_arguments()

    # Initialization
    dashar_configuration: Configuration = Configuration(arguments)

    # Establish an event loop.
    event_loop: tornado.locks.Event = tornado.locks.Event()

    # Create the App Instance.
    app: tornado.web.Application

    # If DashAR failed to initialize, set up the system to respond accordingly to request.
    print(f"\nSystem Status is {dashar_configuration.configuration_variables.system_status.name}.")

    if (dashar_configuration.configuration_variables.system_status == SystemStatus.FAILED):
        print("\nError: DashAR unable to initialize successfully. Please manually restart service.")
        app = make_app_failed_init(dashar_configuration)

    # Otherwise, have fun!
    else:
        print(f"Access on port {dashar_configuration.configuration_variables.das_server_port}.\n")
        app = make_app(dashar_configuration)

    # In both instances, listen for a response on the defined port.
    app.listen(dashar_configuration.configuration_variables.das_server_port)

    # Wait for requests.
    await event_loop.wait()

    # TODO: find a graceful way to terminate the script.
    print("System has terminated.")
    return

if (__name__ == "__main__"):
    asyncio.run(main())
