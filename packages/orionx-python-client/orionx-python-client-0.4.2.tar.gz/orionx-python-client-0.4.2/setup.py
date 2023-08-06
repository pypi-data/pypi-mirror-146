# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['orionx_python_client',
 'orionx_python_client.async_client',
 'orionx_python_client.client']

package_data = \
{'': ['*']}

install_requires = \
['aiodns>=3.0.0,<4.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'cchardet>=2.1.7,<3.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'python-dotenv>=0.19.1,<0.20.0',
 'requests>=2.25.0']

setup_kwargs = {
    'name': 'orionx-python-client',
    'version': '0.4.2',
    'description': '',
    'long_description': None,
    'author': 'adolfrodeno',
    'author_email': 'amvillalobos@uc.cl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
