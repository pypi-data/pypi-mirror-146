# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alpaca', 'alpaca.common', 'alpaca.data']

package_data = \
{'': ['*']}

install_requires = \
['furo>=2022.2.14,<2023.0.0',
 'msgpack>=1.0.3,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'websockets>=10.2,<11.0']

setup_kwargs = {
    'name': 'alpaca-py',
    'version': '0.1.0',
    'description': 'The new official Python SDK for the https://alpaca.markets/ API',
    'long_description': "# AlpacaPy\n\n\n### Dev setup\n\nThis project is managed via poetry so setup should be just running `poetry install`.\n\nThis repo is using [`pre-commit`](https://pre-commit.com/) to setup some checks to happen at commit time\nto keep the repo clean. To set these up after you've run `poetry install` just run `poetry run pre-commit\ninstall` to have pre-commit setup these hooks\n",
    'author': 'Rahul Chowdhury',
    'author_email': 'rahul.chowdhury@alpaca.markets',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alpacahq/alpaca-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
