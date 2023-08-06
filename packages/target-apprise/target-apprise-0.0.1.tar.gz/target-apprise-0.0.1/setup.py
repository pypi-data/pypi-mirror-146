# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['target_apprise', 'target_apprise.tests']

package_data = \
{'': ['*']}

install_requires = \
['apprise==0.9.7', 'requests>=2.25.1,<3.0.0', 'singer-sdk>=0.4.5,<0.5.0']

entry_points = \
{'console_scripts': ['target-apprise = '
                     'target_apprise.target:TargetApprise.cli']}

setup_kwargs = {
    'name': 'target-apprise',
    'version': '0.0.1',
    'description': '`target-apprise` is a Singer target for Apprise, built with the Meltano SDK for Singer Targets.',
    'long_description': None,
    'author': 'AutoIDM',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
