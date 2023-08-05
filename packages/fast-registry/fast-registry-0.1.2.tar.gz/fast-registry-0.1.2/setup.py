# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_registry']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fast-registry',
    'version': '0.1.2',
    'description': 'A generic class that can be used to register classes or functions.',
    'long_description': '# Fast Registry\nA generic class that can be used to register classes or functions, with type hints support.\n\n![Fast Registry Demo](https://raw.githubusercontent.com/danialkeimasi/fast-registry/main/demo.png)\n\n# Installation\n\n```bash\npip install fast-registry\n```\n',
    'author': 'Danial Keimasi',
    'author_email': 'danialkeimasi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/danialkeimasi/fast-registry',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
