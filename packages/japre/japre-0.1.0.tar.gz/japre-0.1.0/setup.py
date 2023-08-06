# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['japre']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=4.0.1,<5.0.0',
 'fugashi>=1.1.2,<2.0.0',
 'ipadic>=1.0.0,<2.0.0',
 'pytextspan>=0.5.4,<0.6.0',
 'tokenizers>=0.12.1,<0.13.0']

setup_kwargs = {
    'name': 'japre',
    'version': '0.1.0',
    'description': 'Custom pretokenizers for Japanese language models',
    'long_description': '# japre',
    'author': 'Kaito Sugimoto',
    'author_email': 'kaito_sugimoto@is.s.u-tokyo.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Alab-NII/japre',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
