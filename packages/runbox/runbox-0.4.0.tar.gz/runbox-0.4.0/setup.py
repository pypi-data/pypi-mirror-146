# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['runbox', 'runbox.docker', 'runbox.scoring', 'runbox.testing']

package_data = \
{'': ['*'], 'runbox': ['.pytest_cache/*', '.pytest_cache/v/cache/*']}

install_requires = \
['aiodocker>=0.21.0,<0.22.0', 'aiohttp>=3.8.1,<4.0.0', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'runbox',
    'version': '0.4.0',
    'description': 'Compile and run untrusted code in docker',
    'long_description': None,
    'author': 'Burenin Artem',
    'author_email': 'burenotti@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
