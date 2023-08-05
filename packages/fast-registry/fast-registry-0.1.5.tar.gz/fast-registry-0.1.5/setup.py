# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_registry']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fast-registry',
    'version': '0.1.5',
    'description': 'A generic class that can be used to register classes or functions.',
    'long_description': '# Fast Registry\n[![](https://img.shields.io/pypi/v/fast-registry.svg)](https://pypi.python.org/pypi/fast-registry/)\n[![](https://github.com/danialkeimasi/fast-registry/workflows/tests/badge.svg)](https://github.com/danialkeimasi/fast-registry/actions)\n[![](https://img.shields.io/github/license/danialkeimasi/fast-registry.svg)](https://github.com/danialkeimasi/fast-registry/blob/master/LICENSE)\n\nA generic class that can be used to register classes or functions, with type hints support.\n# Installation\n\n```bash\npip install fast-registry\n```\n\n# Register Classes\nYou can enforce types on your concrete classes, and also use type hints on your text editors:\n\n```py\nfrom fast_registry import FastRegistry\n\n\nclass Animal:\n    def talk(self):\n        raise NotImplementedError\n\n\n# create a registry that requires registered items to implement the Animal interface:\nanimal_registry = FastRegistry(Animal)\n\n@animal_registry("dog")\nclass Dog:\n    def talk(self):\n        return "woof"\n```\n\n```sh\n>> animal_registry["dog"]\n<class \'__main__.Dog\'>\n\n>> animal_registry["dog"]()\n<__main__.Dog object at 0x7fda96d3b310>\n\n>> animal_registry["dog"]().talk()\n\'woof\'\n```\n\n# Register Functions\n\nYou can also use this tool to register functions:\n```py\nfrom fast_registry import FastRegistry\n\n\nregistry = FastRegistry()\n\n\n@registry("foo")\ndef foo():\n    return "bar"\n```\n\n```sh\n>>> registry["foo"]\n<function foo at 0x7f803c989fc0>\n\n>>> registry["foo"]()\n\'bar\'\n```\n',
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
