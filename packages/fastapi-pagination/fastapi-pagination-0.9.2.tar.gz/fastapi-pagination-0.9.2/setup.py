# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_pagination', 'fastapi_pagination.ext', 'fastapi_pagination.links']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.61.2', 'pydantic>=1.7.2']

extras_require = \
{'all': ['gino[starlette]>=1.0.1',
         'SQLAlchemy>=1.3.20',
         'databases[postgresql,sqlite,mysql]>=0.4.0',
         'orm>=0.1.5',
         'tortoise-orm[asyncpg,aiomysql,aiosqlite]>=0.16.18,<0.19.0',
         'asyncpg>=0.24.0',
         'ormar>=0.10.5',
         'Django<3.3.0',
         'piccolo>=0.29,<0.35',
         'motor>=2.5.1,<3.0.0',
         'mongoengine>=0.23.1,<0.25.0'],
 'asyncpg': ['SQLAlchemy>=1.3.20', 'asyncpg>=0.24.0'],
 'databases': ['databases[postgresql,sqlite,mysql]>=0.4.0'],
 'django': ['databases[postgresql,sqlite,mysql]>=0.4.0', 'Django<3.3.0'],
 'gino': ['gino[starlette]>=1.0.1', 'SQLAlchemy>=1.3.20'],
 'mongoengine': ['mongoengine>=0.23.1,<0.25.0'],
 'motor': ['motor>=2.5.1,<3.0.0'],
 'orm': ['databases[postgresql,sqlite,mysql]>=0.4.0',
         'orm>=0.1.5',
         'typesystem>=0.2.0,<0.3.0'],
 'ormar': ['ormar>=0.10.5'],
 'piccolo': ['piccolo>=0.29,<0.35'],
 'sqlalchemy': ['SQLAlchemy>=1.3.20'],
 'tortoise': ['tortoise-orm[asyncpg,aiomysql,aiosqlite]>=0.16.18,<0.19.0']}

setup_kwargs = {
    'name': 'fastapi-pagination',
    'version': '0.9.2',
    'description': 'FastAPI pagination',
    'long_description': "# FastAPI Pagination\n\n[![License](https://img.shields.io/badge/License-MIT-lightgrey)](/LICENSE)\n[![codecov](https://github.com/uriyyo/fastapi-pagination/workflows/Test/badge.svg)](https://github.com/uriyyo/fastapi-pagination/actions)\n[![codecov](https://codecov.io/gh/uriyyo/fastapi-pagination/branch/main/graph/badge.svg?token=QqIqDQ7FZi)](https://codecov.io/gh/uriyyo/fastapi-pagination)\n[![Downloads](https://pepy.tech/badge/fastapi-pagination)](https://pepy.tech/project/fastapi-pagination)\n[![PYPI](https://img.shields.io/pypi/v/fastapi-pagination)](https://pypi.org/project/fastapi-pagination/)\n[![PYPI](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Support me on Patreon](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Fshieldsio-patreon.vercel.app%2Fapi%3Fusername%3Duriyyo%26type%3Dpatrons&style=flat)](https://patreon.com/uriyyo)\n\n## Installation\n\n```bash\n# Basic version\npip install fastapi-pagination\n\n# All available integrations\npip install fastapi-pagination[all]\n```\n\nAvailable integrations:\n\n* [sqlalchemy](https://github.com/sqlalchemy/sqlalchemy)\n* [gino](https://github.com/python-gino/gino)\n* [databases](https://github.com/encode/databases)\n* [ormar](http://github.com/collerek/ormar)\n* [orm](https://github.com/encode/orm)\n* [tortoise](https://github.com/tortoise/tortoise-orm)\n* [django](https://github.com/django/django)\n* [piccolo](https://github.com/piccolo-orm/piccolo)\n* [sqlmodel](https://github.com/tiangolo/sqlmodel)\n* [motor](https://github.com/mongodb/motor)\n* [mongoengine](https://github.com/MongoEngine/mongoengine)\n\n## Example\n\n```python\nfrom fastapi import FastAPI\nfrom pydantic import BaseModel\n\nfrom fastapi_pagination import Page, add_pagination, paginate\n\napp = FastAPI()\n\n\nclass User(BaseModel):\n    name: str\n    surname: str\n\n\nusers = [\n    User(name='Yurii', surname='Karabas'),\n    # ...\n]\n\n\n@app.get('/users', response_model=Page[User])\nasync def get_users():\n    return paginate(users)\n\n\nadd_pagination(app)\n```\n",
    'author': 'Yurii Karabas',
    'author_email': '1998uriyyo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/uriyyo/fastapi-pagination',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
