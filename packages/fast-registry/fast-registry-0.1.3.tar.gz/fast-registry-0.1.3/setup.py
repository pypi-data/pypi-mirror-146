# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_registry']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fast-registry',
    'version': '0.1.3',
    'description': 'A generic class that can be used to register classes or functions.',
    'long_description': '# Fast Registry\nA generic class that can be used to register classes or functions, with type hints support.\n\n# Example\n```py\nfrom fast_registry import FastRegistry\n\n\nclass Animal:\n    def talk(self):\n        raise NotImplementedError\n\n\n# create a registry that requires registered items to implement the Animal interface.\nanimal_registry = FastRegistry(Animal)\n\n@animal_registry("dog")\nclass Dog:\n    def talk(self):\n        return "woof"\n```\n\n```sh\n>> animal_registry["dog"]\n<class \'__main__.Dog\'>\n\n>> animal_registry["dog"]()\n<__main__.Dog object at 0x7fda96d3b310>\n\n>> animal_registry["dog"]().talk()\n\'woof\'\n```\n\n\n# Installation\n\n```bash\npip install fast-registry\n```\n',
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
