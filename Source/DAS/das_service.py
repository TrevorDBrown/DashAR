#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024 Trevor D. Brown. All rights reserved.
#   This project is distributed under the MIT license.
#
#   File:       das_service.py
#   Purpose:    This script is the backend/middleware service (Data Aggregator and Server) for the DashAR system.
#

from das_core.helper import Constants, SharedFunctions, ServiceMode
from das_core.obdii_interpreter import OBDIIContext
import datetime
import sys
import signal
import asyncio
import tornado

class OBDIIHandler(tornado.web.RequestHandler):
    def get(self):
        if (dashar_object_obdii.is_connected()):
            obdii_data: dict = dashar_object_obdii.capture_data_points()

            client_response_json: dict = {
                "response_id": SharedFunctions.generate_object_id(),
                "current_timestamp": SharedFunctions.get_current_timestamp(),
                "obdii_data": obdii_data
            }

            self.write(f"{client_response_json}")

        else:
            self.write("OBDII is not connected.")

class ThirdPartyAPIHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("This is a test!")

def make_app() -> None:
    return tornado.web.Application([
        (r"/data/obdii", OBDIIHandler),
        (r"/data/api/google-maps", ThirdPartyAPIHandler)
    ])

async def main() -> None:

    # Initialization
    global service_mode
    global dashar_object_obdii

    service_mode = ServiceMode.DEBUG

    dashar_object_obdii = OBDIIContext(obdii_interface_device_path='/dev/tty.usbserial-D395GRKM', service_mode=service_mode)

    app = make_app()
    app.listen(3000)
    await asyncio.Event().wait()

if (__name__ == "__main__"):
    asyncio.run(main())
