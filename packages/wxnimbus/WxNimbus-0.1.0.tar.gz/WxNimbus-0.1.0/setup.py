# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nimbus', 'nimbus.sinks', 'nimbus.sources', 'nimbus.transformers']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.1,<10.0.0',
 'PyAudio>=0.2.11,<0.3.0',
 'PySDL2>=0.9.11,<0.10.0',
 'numpy>=1.22.3,<2.0.0',
 'pyrtlsdr>=0.2.92,<0.3.0',
 'scipy>=1.8.0,<2.0.0']

entry_points = \
{'console_scripts': ['nimbus = nimbus.__main__:main']}

setup_kwargs = {
    'name': 'wxnimbus',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Brianna Witherell',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
