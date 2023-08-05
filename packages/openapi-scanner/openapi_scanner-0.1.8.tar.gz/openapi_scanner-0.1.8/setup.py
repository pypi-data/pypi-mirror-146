# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openapi_scanner']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'aiodns>=3.0.0,<4.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'aiolimiter>=1.0.0,<2.0.0',
 'cchardet>=2.1.7,<3.0.0',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['openapi-scan = openapi_scanner.cli:main']}

setup_kwargs = {
    'name': 'openapi-scanner',
    'version': '0.1.8',
    'description': 'OpenAPI Vulnerability Scanner',
    'long_description': "# OpenAPI Vulnerability Scanner\n\nТекущеее состояние: пока сломан (`$ref`).\n\nCommand-line tool for pentesting [OpenAPI](https://swagger.io/specification/), formerly known as Swagger.\n\n用于渗透测试 OpenAPI 的命令行工具 以前称为 Swagger。\n\n```bash\n$ pipx install openapi_scanner\n$ openapi-scan https://polon.nauka.gov.pl/opi-ws/api/swagger.json --header 'Authorization: Bearer XXX'\n$ openapi-scan --help\n```\n\nUse [asdf](https://github.com/asdf-vm/asdf) or [pyenv](https://github.com/pyenv/pyenv) to install the latest python version.\n",
    'author': 'Sergey M',
    'author_email': 'tz4678@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tz4678/openapi-sqli-scanner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
