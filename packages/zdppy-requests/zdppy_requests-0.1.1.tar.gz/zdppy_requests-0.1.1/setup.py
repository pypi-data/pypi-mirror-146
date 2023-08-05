# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zdppy_requests',
 'zdppy_requests.libs',
 'zdppy_requests.libs.certifi',
 'zdppy_requests.libs.charset_normalizer',
 'zdppy_requests.libs.charset_normalizer.assets',
 'zdppy_requests.libs.charset_normalizer.cli',
 'zdppy_requests.libs.idna',
 'zdppy_requests.libs.requests',
 'zdppy_requests.libs.urllib3',
 'zdppy_requests.libs.urllib3.contrib',
 'zdppy_requests.libs.urllib3.contrib._securetransport',
 'zdppy_requests.libs.urllib3.packages',
 'zdppy_requests.libs.urllib3.packages.backports',
 'zdppy_requests.libs.urllib3.util']

package_data = \
{'': ['*']}

install_requires = \
['zdppy-log>=0.1.7,<0.2.0']

setup_kwargs = {
    'name': 'zdppy-requests',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'zhangdapeng',
    'author_email': 'pygosuperman@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
