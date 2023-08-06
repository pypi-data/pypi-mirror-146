# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['senka']

package_data = \
{'': ['*']}

install_requires = \
['bscscan-python>=2.0.0,<3.0.0',
 'pandas>=1.4.1,<2.0.0',
 'senkalib',
 'toml>=0.10.2,<0.11.0',
 'web3>=5.28.0,<6.0.0']

setup_kwargs = {
    'name': 'senka',
    'version': '0.1.1',
    'description': 'making journal for transactions on blockchain',
    'long_description': 'None',
    'author': 'settler',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
