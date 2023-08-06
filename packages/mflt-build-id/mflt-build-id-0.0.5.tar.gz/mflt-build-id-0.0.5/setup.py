# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mflt_build_id']

package_data = \
{'': ['*']}

install_requires = \
['pyelftools>=0.26,<=0.28']

entry_points = \
{'console_scripts': ['mflt_build_id = mflt_build_id:main']}

setup_kwargs = {
    'name': 'mflt-build-id',
    'version': '0.0.5',
    'description': 'Memfault Build Id injector',
    'long_description': None,
    'author': 'Memfault Inc',
    'author_email': 'hello@memfault.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/memfault/memfault-firmware-sdk',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
