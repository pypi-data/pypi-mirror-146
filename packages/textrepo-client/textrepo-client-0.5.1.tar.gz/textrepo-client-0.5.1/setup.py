# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['textrepo']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json>=0.5.7,<0.6.0',
 'marshmallow>=3.15.0,<4.0.0',
 'python-dateutil==2.8.1',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['version = poetry_scripts:version']}

setup_kwargs = {
    'name': 'textrepo-client',
    'version': '0.5.1',
    'description': 'A Python client to access a textrepo server',
    'long_description': '# textrepo-client\n\n[![GitHub Actions](https://github.com/knaw-huc/textrepo-client-python/workflows/tests/badge.svg)](https://github.com/knaw-huc/textrepo-client-python/actions)\n[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)\n![PyPI](https://img.shields.io/pypi/v/textrepo-client)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/textrepo-client)\n\nA Python client for accessing a [textrepo](https://github.com/knaw-huc/textrepo) server\n\n# installing\n\n### using poetry\n\n```commandline\npoetry add annorepo-client\n```\n\n### using pip\n\n```commandline\npip install annorepo-client\n```\n\n----\n\n[USAGE](USAGE.md) |\n[CONTRIBUTING](CONTRIBUTING.md)',
    'author': 'Bram Buitendijk',
    'author_email': 'bram.buitendijk@di.huc.knaw.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/knaw-huc/textrepo-client-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
