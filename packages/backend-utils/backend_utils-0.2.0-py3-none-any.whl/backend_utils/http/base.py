import asyncio
import json
from enum import auto
from typing import List, Optional

import httpx
from pydantic import BaseModel, ValidationError, parse_obj_as

from backend_utils.tools import Singleton, StrEnum
from backend_utils.http.middleware import BaseMiddleware


_DEFAULT_TIMEOUT = 30


class RequestMethods(StrEnum):
    GET = auto()
    POST = auto()
    PUT = auto()
    PATCH = auto()
    DELETE = auto()


class BaseRequester(metaclass=Singleton):
    """
    Base class for all http clients
    The child class must have the following: self.URL

    This class is Singleton for keeping http session

    URL: used as base url to make requests it will be combined with uri in self.make_request method
    TIMEOUT: used as default timeout if there is no timeout param in self.make_request method
    MIDDLEWARE: list of middlewares to perform on different requests stages
    """

    URL: str = ''
    TIMEOUT: float = _DEFAULT_TIMEOUT
    MIDDLEWARES: List[BaseMiddleware] = []

    def __init__(self):
        self.client = httpx.AsyncClient()

    @property
    def url(self) -> str:
        return self.URL.strip('/')

    @property
    def timeout(self) -> float:
        return self.TIMEOUT

    @property
    def middlewares(self) -> List[BaseMiddleware]:
        return self.MIDDLEWARES

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def _compile_url(
            self,
            url: Optional[str] = None,
            uri: Optional[str] = None,
    ):
        if not url:
            url = self.url + '/' + uri.strip('/')
        return url

    async def make_request(
            self,
            method: RequestMethods,
            url: Optional[str] = None,
            uri: Optional[str] = None,
            payload: Optional[dict] = None,
            params: Optional[dict] = None,
            headers: Optional[dict] = None,
            timeout: Optional[float] = None,
            response_model: [BaseModel, None] = None
    ) -> [httpx.Response, BaseModel, None]:
        """Base method to make requests
        :param method: request method
        :param url: full endpoint url; if None uri with self.url will be used
        :param uri: endpoint uri; it will combine with self.url if url is None
        :param payload: request json body
        :param params: request params
        :param headers: request headers
        :param timeout: request timeout; if None self.timeout will be used
        :param response_model: if you want to validate your response with pydantic model and return it
        :return:
        """

        url = self._compile_url(url=url, uri=uri)
        request = self.client.build_request(
            method=method,
            url=url,
            json=payload,
            params=params,
            headers=headers,
            timeout=timeout or self.timeout
        )
        await asyncio.gather(*[m.before_request(request=request) for m in self.middlewares])

        try:
            response = await self.client.send(request)
        except httpx.HTTPError as e:
            await asyncio.gather(*[m.on_request_error(request=request, error=e) for m in self.middlewares])
            return

        if response.is_error:
            await asyncio.gather(*[m.on_request_status_error(request=request) for m in self.middlewares])
            return

        await asyncio.gather(*[m.after_request(request=request, response=response) for m in self.middlewares])
        if response_model:
            response = await self._validate_response(
                response_model=response_model,
                response=response
            )
        return response

    async def _validate_response(self, response_model, response: httpx.Response) -> [BaseModel, None]:
        """Validate response json with pydantic validator
        """
        try:
            resp = parse_obj_as(response_model, response.json())
        except (ValidationError, json.decoder.JSONDecodeError) as e:
            await asyncio.gather(*[m.on_validation_error(response=response, error=e) for m in self.middlewares])
            return
        return resp
