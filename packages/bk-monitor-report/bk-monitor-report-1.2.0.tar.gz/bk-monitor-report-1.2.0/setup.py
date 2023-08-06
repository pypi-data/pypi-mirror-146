# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bk_monitor_report', 'bk_monitor_report.contrib']

package_data = \
{'': ['*']}

install_requires = \
['prometheus-client>=0.9.0,<0.10.0', 'requests>=2.20.0,<3.0.0']

setup_kwargs = {
    'name': 'bk-monitor-report',
    'version': '1.2.0',
    'description': 'custom reporter python sdk for bk-monitor',
    'long_description': None,
    'author': 'homholueng',
    'author_email': 'homholueng@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.0,<4.0.0',
}


setup(**setup_kwargs)
