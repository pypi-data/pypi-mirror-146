# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_opeco17_test_plugin']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.0b1dev0,<2.0.0']

entry_points = \
{'poetry.application.plugin': ['poetry-audit-plugin = '
                               'poetry_opeco17_test_plugin.plugin:TestApplicationPlugin']}

setup_kwargs = {
    'name': 'poetry-opeco17-test-plugin',
    'version': '1.0.0',
    'description': '',
    'long_description': '',
    'author': 'opeco17',
    'author_email': 'opeco17@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
