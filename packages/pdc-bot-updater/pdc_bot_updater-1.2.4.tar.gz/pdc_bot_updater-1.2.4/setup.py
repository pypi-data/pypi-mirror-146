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
 'requests>=2.27.1,<3.0.0',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'pdc-bot-updater',
    'version': '1.2.4',
    'description': 'pdc shipment aplication bot',
    'long_description': "# pdc_updater\nimplementasi auto updater dengan memakai cloud storage google\n\n### set environtment\nset GOOGLE_APPLICATION_CREDENTIALS=credentials.json\n\n\n# Example\n### Publising Aplication\n```\nfrom pdc_bot_updater.publisher.publish import configure_client, AppArchiver\n\nbucket_id = 'artifact'\nfolder_app = 'aplikasi_bot'\n\nconfigure_client(bucket_id)\n\n\narchiver = AppArchiver(folder_app)\narchiver.get_meta()\narchiver.upload_archive(f'dist/aplication.zip', version='1.0.0')\n```\n\n### Updating App\n```\nfrom pdc_bot_updater.client.updater import Updater\n\nbucket_id = 'artifact'\nfolder_app = 'aplikasi_bot'\n\nupdater = Updater(folder_app, bucket_id)\nupdater.check_update()\nupdater.detach_process(['application.exe'])\n\n```\n\n\n",
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
