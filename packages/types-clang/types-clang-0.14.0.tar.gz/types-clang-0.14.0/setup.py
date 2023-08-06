# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['clang-stubs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'types-clang',
    'version': '0.14.0',
    'description': 'Stubs package for Clang Python bindings',
    'long_description': '###########\ntypes-clang\n###########\n==========================================\nType Information for Clang Python Bindings\n==========================================\n\nHave you used the `Clang Python Bindings <https://pypi.org/project/clang/>`_, but wanted type hints in your IDE?\nHave you ever wanted to use `mypy <http://mypy-lang.org/>`_ tools on a project that uses Clang but gotten errors due to\nlack of type annotations?\nThis package is a `PEP 561 <https://www.python.org/dev/peps/pep-0561>`_ stub package which provides type information for\nClang.\n\nIn other words, transform your IDE from:\n\n.. image:: https://raw.githubusercontent.com/tgockel/types-clang/trunk/doc/before.png\n\nto:\n\n.. image:: https://raw.githubusercontent.com/tgockel/types-clang/trunk/doc/after.png\n\nTo utilize this, add it globally with::\n\n    pip3 install types-clang\n\nOr add ``types-clang`` to ``dev-requirements.txt`` or ``pyproject.toml`` or whatever you use for dependency management.\n',
    'author': 'Travis Gockel',
    'author_email': 'travis@gockelhut.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tgockel/clang-stubs',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
