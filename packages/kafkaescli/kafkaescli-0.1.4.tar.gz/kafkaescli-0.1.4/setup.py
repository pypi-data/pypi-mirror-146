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
    'version': '0.1.4',
    'description': 'A magical kafka command line interface.',
    'long_description': '\ufeff\n![Kafkaescli](docs/images/kafkaescli-repository-open-graph-template.png)\n\n[![CircleCI](https://circleci.com/gh/jonykalavera/kafkaescli/tree/main.svg?style=svg)](https://circleci.com/gh/jonykalavera/kafkaescli/tree/main)\n\n# Install\n\nInstall from [pypi](https://pypi.org/project/kafkaescli/)\n\n```sh\npip install kafkaescli\n```\n\n# Usage\n\n```bash\n# consume from `hello`\nkafkaescli consume hello\n# consume from `hello` showing metadata\nkafkaescli consume hello --metadata\n# produce topic `hello`\nkafkaescli produce hello world\n# produce longer strings\nkafkaescli produce hello "world of kafka"\n# produce from stdin per line\necho "hello world of kfk" | kafkaescli produce hello --stdin\n# produce to topic `world` form the output of a consumer of topic `hello`\nkafkaescli consume hello | kafkaescli produce world --stdin\n# produce `world` to `hello`, with middleware\nkafkaescli produce hello json --middleware examples.json.JSONMiddleware\n# consume from hello with middleware\nkafkaescli consume hello --middleware examples.json.JSONMiddleware\n# run the web api http://localhost:8000/docs\nkafkaescli runserver\n# POST consumed messages to WEBHOOK\nkafkaescli consume hello --metadata --webhook https://myendpoint.example.com\n# For more details see\nkafkaescli --help\n```\n\n# Contributions\n\n* [Jony Kalavera](https://github.com/jonykalavera)\n\nPull-requests are welcome and will be processed on a best-effort basis.\nFollow the [contributing guide](CONTRIBUTING.md).\n',
    'author': 'Jony Kalavera',
    'author_email': 'mr.jony@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jonykalavera/kafkaescli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
