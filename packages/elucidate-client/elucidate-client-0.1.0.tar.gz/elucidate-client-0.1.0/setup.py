# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elucidate']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['version = poetry_scripts:version']}

setup_kwargs = {
    'name': 'elucidate-client',
    'version': '0.1.0',
    'description': 'Python client to interact with an elicidate server',
    'long_description': '## elucidate-client\n\n[![GitHub Actions](https://github.com/knaw-huc/elucidate-python-client/workflows/tests/badge.svg)](https://github.com/knaw-huc/elucidate-python-client/actions)\n[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)\n[![Documentation Status](https://readthedocs.org/projects/elucidate-python-client/badge/?version=latest)](https://elucidate-python-client.readthedocs.io/en/latest/?badge=latest)\n![PyPI](https://img.shields.io/pypi/v/elucidate-client)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/eluciate-client)\n\nA Python client for accessing an [elucidate](https://github.com/knaw-huc/elucidate) server (knaw-huc fork)\n\n## installing\n\n### using poetry\n\n```commandline\npoetry add elucidate-client\n```\n\n### using pip\n\n```commandline\npip install elucidate-client\n```\n\n# documentation\n\nSee [USAGE](https://elucidate-python-client.readthedocs.io/en/latest/)\nand [the notebooks](https://github.com/knaw-huc/elucidate-python-client/tree/main/notebooks)\n\n----\n\n[USAGE](https://elucidate-python-client.readthedocs.io/en/latest/) |\n[CONTRIBUTING](CONTRIBUTING.md) |\n[LICENSE](LICENSE)\n',
    'author': 'Bram Buitendijk',
    'author_email': 'bram.buitendijk@di.huc.knaw.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/knaw-huc/elucidate-python-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
