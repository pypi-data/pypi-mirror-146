# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zohavi',
 'zohavi.zbase',
 'zohavi.zcelery',
 'zohavi.zcommon',
 'zohavi.zemailer',
 'zohavi.zmembers',
 'zohavi.zwebui']

package_data = \
{'': ['*'],
 'zohavi.zbase': ['templates/zbase/*'],
 'zohavi.zcelery': ['templates/_def/*'],
 'zohavi.zemailer': ['templates/zemail/*'],
 'zohavi.zmembers': ['templates/zmembers/*'],
 'zohavi.zwebui': ['static/zcss/*', 'static/zjs/*', 'static/zwc/*']}

setup_kwargs = {
    'name': 'zohavi',
    'version': '0.1.22',
    'description': 'Web widgets',
    'long_description': '# Hello World 123456789',
    'author': 'pub12',
    'author_email': 'pubudu79@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
