# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bedrockz', 'bedrockz.generator']

package_data = \
{'': ['*'], 'bedrockz.generator': ['templates/brownie/*']}

install_requires = \
['Jinja2>=3.1.1,<4.0.0',
 'addict>=2.4.0,<3.0.0',
 'anyio[all]>=3.5.0,<4.0.0',
 'auto-all>=1.4.1,<2.0.0',
 'blue>=0.8.0,<0.9.0',
 'cytoolz>=0.11.2,<0.12.0',
 'diskcache>=5.4.0,<6.0.0',
 'forbiddenfruit>=0.1.4,<0.2.0',
 'fs>=2.4.15,<3.0.0',
 'inflection>=0.5.1,<0.6.0',
 'loguru>=0.6.0,<0.7.0',
 'matplotlib>=3.5.1,<4.0.0',
 'maya>=0.6.1,<0.7.0',
 'networkx>=2.8,<3.0',
 'orjson>=3.6.7,<4.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'python-box[toml,msgpack,ruamel.yaml]==6.0.0',
 'questionary>=1.10.0,<2.0.0',
 'retworkx[all]>=0.11.0,<0.12.0',
 'typer[all]>=0.4.1,<0.5.0',
 'xxhash>=3.0.0,<4.0.0',
 'yapf>=0.32.0,<0.33.0']

entry_points = \
{'console_scripts': ['brockz = bedrockz.cli:app']}

setup_kwargs = {
    'name': 'bedrockz',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Kevin H.',
    'author_email': 'kevin@autoworkz.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
