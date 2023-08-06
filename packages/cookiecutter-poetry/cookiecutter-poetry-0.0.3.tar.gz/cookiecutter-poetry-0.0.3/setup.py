# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_cookiecutter']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=4.5.0,<5.0.0',
 'cookiecutter>=1.7.3,<2.0.0',
 'pytest-cookies>=0.6.1,<0.7.0',
 'sphinx-rtd-theme>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['pcc = poetry_cookiecutter.cli:main']}

setup_kwargs = {
    'name': 'cookiecutter-poetry',
    'version': '0.0.3',
    'description': 'A python cookiecutter application to create a new python project that uses poetry to manage its dependencies.',
    'long_description': None,
    'author': 'Florian Maas',
    'author_email': 'fpgmaas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fpgmaas/cookiecutter-poetry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
