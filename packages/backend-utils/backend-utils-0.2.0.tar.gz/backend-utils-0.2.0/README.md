# backend-utils
Useful python tools for backend services


## Documentation

### Tools

* `Singleton` - metaclass to make singletons
```python
from backend_utils.tools import Singleton

class A(metaclass=Singleton):
    pass

print(id(A()) == id(A())) # True
```

* `StrEnum` - subclasses that create variants using `auto()` will have values equal to their names
```python
from enum import auto

from backend_utils.tools import StrEnum

class Bit(StrEnum):
    one = auto()
    two = auto()

print(Bit.one.value) # 'one'
print(Bit.two.value) # 'two'
```

### Server

* `Router`, `compile_routers`, `register_routers` - build routers 
for fastapi app

```python
from fastapi import FastAPI, APIRouter

from backend_utils.server import (
    Router, compile_routers, register_routers
)
router = APIRouter()

routers = [
    Router(router=router, tags=['Users'], prefix='/users'),
]


compiled_routers = compile_routers(
    routers=routers,
    root_prefix='/api/v1'
)

app = FastAPI()
register_routers(
    app=app,
    routers=[*compiled_routers]
)
```
This code will compile routers:
`/api/v1/users/*`

### Http
* `RequestMethods` - enum for http methods
  
* `BaseRequester` - base class for http clients. You can specify `URL`, `TIMEOUT`, `MIDDLEWARE`.
Use `self.make_request()` to make http requests
  
```python
import os
import asyncio
from typing import Optional

import httpx
from backend_utils.http import BaseRequester, RequestMethods


class JsonPlaceholder(BaseRequester):
    URL = os.getenv('JSONPLACEHOLDER_URL', 'https://jsonplaceholder.typicode.com')
    TIMEOUT = 10

    async def get_todo(self, todo_id: int) -> Optional[httpx.Response]:
        return await self.make_request(
            method=RequestMethods.GET,
            uri=f'/todos/{todo_id}',
        )

    
if __name__ == '__main__':
    jp = JsonPlaceholder()
    asyncio.run(jp.get_todo(todo_id=1))
```

You also can validate response with pydantic models
```python
import os
import asyncio
from typing import Optional

from pydantic import BaseModel, Field
from backend_utils.http import BaseRequester, RequestMethods

class GetTodo(BaseModel):
    user_id: int = Field(..., alias='userId')
    id: int
    title: str
    completed: bool

class JsonPlaceholder(BaseRequester):
    async def get_todo_model(self, todo_id: int) -> Optional[GetTodo]:
        url = os.getenv('JSONPLACEHOLDER_URL', 'https://jsonplaceholder.typicode.com')
        return await self.make_request(
            method=RequestMethods.GET,
            url=f'{url}/todos/{todo_id}',
            response_model=GetTodo,
            timeout=5.5
        )

    
if __name__ == '__main__':
    jp = JsonPlaceholder()
    asyncio.run(jp.get_todo_model(todo_id=1))
```
So it will return `GetTodo` model or `None` if request failed

* `BaseMiddleware` - base class for http request middleware.
Available methods:
  - `before_request(self, request: httpx.Request)`
  - `after_request(self, request: httpx.Request, response: httpx.Response):`
  - `on_request_error(self, request: httpx.Request, error: httpx.HTTPError)`
  - `on_request_status_error(self, request: httpx.Request)`
  - `on_validation_error(self, response: httpx.Response, error: [ValidationError, json.decoder.JSONDecodeError])`
    
For example middleware to print request time
```python
import os
import time
import asyncio
from typing import Optional

import httpx
from backend_utils.http import BaseRequester, RequestMethods, BaseMiddleware


class PrintRequestTime(BaseMiddleware):
    async def before_request(self, request: httpx.Request):
        request.start_time = time.perf_counter()

    async def after_request(self, request: httpx.Request, response: httpx.Response):
        request_time = time.perf_counter() - request.start_time
        print(request_time)


class JsonPlaceholder(BaseRequester):
    URL = os.getenv('JSONPLACEHOLDER_URL', 'https://jsonplaceholder.typicode.com')
    MIDDLEWARES = [PrintRequestTime()]
    
    async def get_todo(self, todo_id: int) -> Optional[httpx.Response]:
        return await self.make_request(
            method=RequestMethods.GET,
            uri=f'/todos/{todo_id}',
        )

    
if __name__ == '__main__':
    jp = JsonPlaceholder()
    asyncio.run(jp.get_todo(todo_id=1))
```
