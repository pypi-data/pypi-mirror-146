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
    'version': '0.14.1',
    'description': 'Stubs package for Clang Python bindings',
    'long_description': '###########\ntypes-clang\n###########\n==========================================\nType Information for Clang Python Bindings\n==========================================\n\nHave you used the `Clang Python Bindings <https://pypi.org/project/clang/>`_, but wanted type hints in your IDE?\nHave you ever wanted to use `mypy <http://mypy-lang.org/>`_ tools on a project that uses Clang but gotten errors due to\nlack of type annotations?\nThis package is a `PEP 561 <https://www.python.org/dev/peps/pep-0561>`_ stub package which provides type information for\nClang.\n\nIn other words, transform your IDE from:\n\n.. image:: https://raw.githubusercontent.com/tgockel/types-clang/trunk/doc/before.png\n\nto:\n\n.. image:: https://raw.githubusercontent.com/tgockel/types-clang/trunk/doc/after.png\n\nTo utilize this, add it globally with::\n\n    pip3 install types-clang\n\nOr add ``types-clang`` to ``dev-requirements.txt`` or ``pyproject.toml`` or whatever you use for dependency management.\n\nVersioning\n==========\n\n.. note::\n    This project is still ``0.x``, so this section is more about the *plans* for how to version.\n\nThe published ``types-clang`` packages correspond with the type information of the ``{major}.{minor}`` of the ``clang``\npackage.\nThe patch version of ``types-clang`` does not correspond with any patch version of ``clang``, as they use semantic\nversioning correctly and will not add functionality in a patch release.\nSo, if you install ``clang==13.0.1``, then ``types-clang>=13.0, <13.1`` will have the appropriate stubs.\n\nBest practice is to write the version specification for ``types-clang`` to be the same as the ``clang`` package, but\nwithout the patch.\nFor `Poetry <https://python-poetry.org/>`_::\n\n    [tool.poetry.dependencies]\n    clang = "14.0"\n\n    [tool.poetry.dev-dependencies]\n    types-clang = "14.0"\n\nDeveloping\n==========\n\nDevelopment utilizes `Poetry <https://python-poetry.org/>`_ for dependency fetching and package publishing and\n`tox <https://tox.wiki/en/latest/>`_ for testing.\nThe ``clang-stubs/cindex.py`` file is generated with the ``generate_cindex.py`` script, which reads the installed\n``clang.cindex`` module and generates code with `Jinja <https://palletsprojects.com/p/jinja/>`_.\n\nMy personal workflow looks like this::\n\n    $> poetry shell\n    (env-py3.9) $> poetry install\n    (env-py3.9) $> ./generate_cindex.py --output clang-stubs/cindex.py\n    (env-py3.9) $> ^D\n    $> tox\n',
    'author': 'Travis Gockel',
    'author_email': 'travis@gockelhut.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tgockel/types-clang',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
