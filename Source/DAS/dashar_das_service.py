#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024 Trevor D. Brown. All rights reserved.
#   This project is distributed under the MIT license.
#
#   File:       dashar_das_service.py
#   Purpose:    This script is the backend/middleware service for the DashAR system.
#

from das_core.obdii_interpreter import OBDIIContext
import datetime
import sys
import signal
import asyncio
import tornado

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if (dashar_object_obdii.is_connected()):
            currentSpeed = dashar_object_obdii.getSpeed()
            self.write("The current speed is: %s" % currentSpeed)
        else:
            self.write("No data available from OBDII.")

def make_app() -> None:
    return tornado.web.Application([
        (r"/", MainHandler)
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
