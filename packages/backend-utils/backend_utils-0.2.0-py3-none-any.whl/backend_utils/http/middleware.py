import json

import httpx
from pydantic import ValidationError


class BaseMiddleware:
    """Base class for http requester middleware.
    Implement any of them
    """

    async def before_request(self, request: httpx.Request): # noqa U100
        """Runs before request
        """

    async def after_request(self, request: httpx.Request, response: httpx.Response): # noqa U100
        """Runs after request
        """

    async def on_request_error(self, request: httpx.Request, error: httpx.HTTPError): # noqa U100
        """Runs on any http error like timeout or protocol error
        """

    async def on_request_status_error(self, request: httpx.Request): # noqa U100
        """Runs on bad status code (status_code > 400)
        """

    async def on_validation_error(
            self, response: httpx.Response, error: [ValidationError, json.decoder.JSONDecodeError] # noqa U100
    ):
        """Runs on response validation error
        """
