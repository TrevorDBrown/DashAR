#
#   DashAR - An AR-based HUD for Automobiles.
#   (c)2024-2026 Trevor D. Brown. Distributed under the MIT license.
#
#   File:       das_service.pyi
#

"""Purpose: the backend/middleware service (Data Aggregator and Server) for the DashAR system."""

# pylint: skip-file

import argparse
import asyncio
import tornado
from das_core.configuration import Configuration

class DashARWelcomeHandler(tornado.web.RequestHandler):
    """
    A class for handling requests on endpoint: /dashar/welcome.
    """

    def initialize(self) -> None: ...
    def get(self) -> None: ...

class DashARStatusHandler(tornado.web.RequestHandler):
    """
    A class for handling requests on endpoint: /dashar/status.
    """

    dashar_configuration: Configuration
    def initialize(self, dashar_configuration: Configuration) -> None: ...
    def get(self) -> None: ...

class DashARHUDHandler(tornado.web.RequestHandler):
    """
    A class for handling requests on endpoint: /dashar/hud/config
    """

    dashar_configuration: Configuration
    def initialize(self, dashar_configuration: Configuration) -> None: ...
    def get(self) -> None: ...

class OBDIIHandler(tornado.web.RequestHandler):
    """
    A class for handling requests on endpoint: /dashar/data/obdii
    """

    dashar_configuration: Configuration
    def initialize(self, dashar_configuration: Configuration) -> None: ...
    def get(self) -> None: ...

class TerminateHandler(tornado.web.RequestHandler):
    """
    A class for handling requests on endpoint: /dashar/quit
    """

    dashar_configuration: Configuration
    shutdown_event: asyncio.Event
    def initialize(
        self, shutdown_event: asyncio.Event, dashar_configuration: Configuration
    ) -> None: ...
    def get(self) -> None: ...

class UnimplementedHandler(tornado.web.RequestHandler):
    """
    A class for handling requests on unimplemented endpoints.
    """

    def initialize(self) -> None: ...
    def get(self) -> None: ...

class NotFoundHandler(tornado.web.RequestHandler):
    """
    A class for handling requests for non-existent endpoints.
    """

    def initialize(self) -> None: ...
    def get(self) -> None: ...

class FailedInitHandler(tornado.web.RequestHandler):
    """
    A class for handling initialization failures.
    """
    def initialize(self) -> None: ...
    def get(self) -> None: ...

def make_app(
    dashar_configuration: Configuration, shutdown_event: asyncio.Event
) -> tornado.web.Application: ...
def make_app_failed_init(
    dashar_configuration: Configuration, shutdown_event: asyncio.Event
) -> tornado.web.Application: ...
def check_for_arguments() -> argparse.Namespace: ...
async def main() -> None: ...
