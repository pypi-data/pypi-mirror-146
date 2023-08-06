# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdc_bot_updater',
 'pdc_bot_updater.client',
 'pdc_bot_updater.core',
 'pdc_bot_updater.publisher']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-storage>=2.2.1,<3.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'pdc-bot-updater',
    'version': '0.1.0',
    'description': 'pdc shipment aplication bot',
    'long_description': None,
    'author': 'kampretcode',
    'author_email': 'manorder123@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
