#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024 Trevor D. Brown. All rights reserved.
#   This project is distributed under the MIT license.
#
#   File:       das_service.py
#   Purpose:    This script is the backend/middleware service (Data Aggregator and Server) for the DashAR system.
#

from das_core.obdii_interpreter import OBDIIContext
import datetime
import sys
import signal
import asyncio
import tornado

class OBDIIHandler(tornado.web.RequestHandler):
    def get(self):
        if (dashar_object_obdii.is_connected()):
            currentSpeed = dashar_object_obdii.get_speed()
            self.write(f"Current Speed: {currentSpeed} - Time: {datetime.datetime.now()}")
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
    global dashar_object_obdii
    dashar_object_obdii = OBDIIContext()

    app = make_app()
    app.listen(3000)
    await asyncio.Event().wait()

if (__name__ == "__main__"):
    asyncio.run(main())
