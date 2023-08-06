# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['directbank', 'directbank.models']

package_data = \
{'': ['*']}

install_requires = \
['xsdata==22.4']

setup_kwargs = {
    'name': 'directbank',
    'version': '0.0.9',
    'description': '',
    'long_description': '# directbank\n### Test',
    'author': 'Toony',
    'author_email': 'kizyanov@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kizyanov/directbank',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
