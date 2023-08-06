# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['backend_utils',
 'backend_utils.http',
 'backend_utils.server',
 'backend_utils.server.app',
 'backend_utils.tools']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.75.0,<0.76.0', 'httpx>=0.22.0,<0.23.0']

setup_kwargs = {
    'name': 'backend-utils',
    'version': '0.2.0',
    'description': 'backend utils',
    'long_description': "# backend-utils\nUseful python tools for backend services\n\n\n## Documentation\n\n### Tools\n\n* `Singleton` - metaclass to make singletons\n```python\nfrom backend_utils.tools import Singleton\n\nclass A(metaclass=Singleton):\n    pass\n\nprint(id(A()) == id(A())) # True\n```\n\n* `StrEnum` - subclasses that create variants using `auto()` will have values equal to their names\n```python\nfrom enum import auto\n\nfrom backend_utils.tools import StrEnum\n\nclass Bit(StrEnum):\n    one = auto()\n    two = auto()\n\nprint(Bit.one.value) # 'one'\nprint(Bit.two.value) # 'two'\n```\n\n### Server\n\n* `Router`, `compile_routers`, `register_routers` - build routers \nfor fastapi app\n\n```python\nfrom fastapi import FastAPI, APIRouter\n\nfrom backend_utils.server import (\n    Router, compile_routers, register_routers\n)\nrouter = APIRouter()\n\nrouters = [\n    Router(router=router, tags=['Users'], prefix='/users'),\n]\n\n\ncompiled_routers = compile_routers(\n    routers=routers,\n    root_prefix='/api/v1'\n)\n\napp = FastAPI()\nregister_routers(\n    app=app,\n    routers=[*compiled_routers]\n)\n```\nThis code will compile routers:\n`/api/v1/users/*`\n\n### Http\n* `RequestMethods` - enum for http methods\n  \n* `BaseRequester` - base class for http clients. You can specify `URL`, `TIMEOUT`, `MIDDLEWARE`.\nUse `self.make_request()` to make http requests\n  \n```python\nimport os\nimport asyncio\nfrom typing import Optional\n\nimport httpx\nfrom backend_utils.http import BaseRequester, RequestMethods\n\n\nclass JsonPlaceholder(BaseRequester):\n    URL = os.getenv('JSONPLACEHOLDER_URL', 'https://jsonplaceholder.typicode.com')\n    TIMEOUT = 10\n\n    async def get_todo(self, todo_id: int) -> Optional[httpx.Response]:\n        return await self.make_request(\n            method=RequestMethods.GET,\n            uri=f'/todos/{todo_id}',\n        )\n\n    \nif __name__ == '__main__':\n    jp = JsonPlaceholder()\n    asyncio.run(jp.get_todo(todo_id=1))\n```\n\nYou also can validate response with pydantic models\n```python\nimport os\nimport asyncio\nfrom typing import Optional\n\nfrom pydantic import BaseModel, Field\nfrom backend_utils.http import BaseRequester, RequestMethods\n\nclass GetTodo(BaseModel):\n    user_id: int = Field(..., alias='userId')\n    id: int\n    title: str\n    completed: bool\n\nclass JsonPlaceholder(BaseRequester):\n    async def get_todo_model(self, todo_id: int) -> Optional[GetTodo]:\n        url = os.getenv('JSONPLACEHOLDER_URL', 'https://jsonplaceholder.typicode.com')\n        return await self.make_request(\n            method=RequestMethods.GET,\n            url=f'{url}/todos/{todo_id}',\n            response_model=GetTodo,\n            timeout=5.5\n        )\n\n    \nif __name__ == '__main__':\n    jp = JsonPlaceholder()\n    asyncio.run(jp.get_todo_model(todo_id=1))\n```\nSo it will return `GetTodo` model or `None` if request failed\n\n* `BaseMiddleware` - base class for http request middleware.\nAvailable methods:\n  - `before_request(self, request: httpx.Request)`\n  - `after_request(self, request: httpx.Request, response: httpx.Response):`\n  - `on_request_error(self, request: httpx.Request, error: httpx.HTTPError)`\n  - `on_request_status_error(self, request: httpx.Request)`\n  - `on_validation_error(self, response: httpx.Response, error: [ValidationError, json.decoder.JSONDecodeError])`\n    \nFor example middleware to print request time\n```python\nimport os\nimport time\nimport asyncio\nfrom typing import Optional\n\nimport httpx\nfrom backend_utils.http import BaseRequester, RequestMethods, BaseMiddleware\n\n\nclass PrintRequestTime(BaseMiddleware):\n    async def before_request(self, request: httpx.Request):\n        request.start_time = time.perf_counter()\n\n    async def after_request(self, request: httpx.Request, response: httpx.Response):\n        request_time = time.perf_counter() - request.start_time\n        print(request_time)\n\n\nclass JsonPlaceholder(BaseRequester):\n    URL = os.getenv('JSONPLACEHOLDER_URL', 'https://jsonplaceholder.typicode.com')\n    MIDDLEWARES = [PrintRequestTime()]\n    \n    async def get_todo(self, todo_id: int) -> Optional[httpx.Response]:\n        return await self.make_request(\n            method=RequestMethods.GET,\n            uri=f'/todos/{todo_id}',\n        )\n\n    \nif __name__ == '__main__':\n    jp = JsonPlaceholder()\n    asyncio.run(jp.get_todo(todo_id=1))\n```\n",
    'author': 'Mark Antipin',
    'author_email': 'antipinsuperstar@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Sistemka/backend-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
