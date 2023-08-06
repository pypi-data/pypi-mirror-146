# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kafkaescli',
 'kafkaescli.app',
 'kafkaescli.app.commands',
 'kafkaescli.domain',
 'kafkaescli.infra',
 'kafkaescli.lib']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'aiokafka>=0.7.2,<0.8.0',
 'fastapi>=0.75.1,<0.76.0',
 'pydantic>=1.9.0,<2.0.0',
 'pytest-cov>=3.0.0,<4.0.0',
 'result>=0.7.0,<0.8.0',
 'typer>=0.4.1,<0.5.0',
 'uvicorn>=0.17.6,<0.18.0']

setup_kwargs = {
    'name': 'kafkaescli',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Jony Kalavera',
    'author_email': 'mr.jony@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
