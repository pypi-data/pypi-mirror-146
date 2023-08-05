# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['knife']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0', 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['knife = knife:app']}

setup_kwargs = {
    'name': 'mvadkert-knife',
    'version': '0.1.0',
    'description': 'Swiss army knife with various useful utilities.',
    'long_description': None,
    'author': 'Miroslav Vadkerti',
    'author_email': 'mvadkert@redhat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
