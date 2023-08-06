# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jitproxy']

package_data = \
{'': ['*']}

install_requires = \
['clearcut>=0.1.2,<0.2.0']

setup_kwargs = {
    'name': 'jitproxy',
    'version': '0.1.1',
    'description': 'JIT Lazy-loading Proxies for synch and AIO objects',
    'long_description': '# jitproxy\n\nJust-in-time, lazy-loading Proxies for standard (synchronous) and AIO objects.',
    'author': 'Austin Howard',
    'author_email': 'austin@tangibleintelligence.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
