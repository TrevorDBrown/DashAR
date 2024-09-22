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
import sys
import signal
import asyncio
import tornado

class OBDIIHandler(tornado.web.RequestHandler):
    dashar_configuration: Configuration

    def initialize(self, dashar_configuration: Configuration) -> None:
        self.dashar_configuration = dashar_configuration

    def get(self) -> None:
        client_response_json: str

        if (self.dashar_configuration.obdii_context.is_connected()):
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
                "obdii_data": "Not Available"
            })

            self.set_header("Content-Type", "application/json")
            self.set_status(503, "OBDII is not available.")
            self.write(f"{client_response_json}")

class ThirdPartyAPIHandler(tornado.web.RequestHandler):
    def get(self) -> None:
        self.write("This is a test!")

def make_app(dashar_configuration: Configuration) -> tornado.web.Application:
    return tornado.web.Application([
        (r"/data/obdii", OBDIIHandler, {"dashar_configuration": dashar_configuration}),
        (r"/data/api/google-maps", ThirdPartyAPIHandler, {"dashar_configuration": dashar_configuration})
    ])

async def main() -> None:

    # Initialization
    dashar_configuration: Configuration = Configuration()

    app: tornado.web.Application = make_app(dashar_configuration)
    app.listen(3000)
    await asyncio.Event().wait()

if (__name__ == "__main__"):
    asyncio.run(main())
