# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['bundler']
entry_points = \
{'console_scripts': ['bundlerpy = bundler:main']}

setup_kwargs = {
    'name': 'bundler.py',
    'version': '0.1.1',
    'description': 'A simple tool for packing shippable virtualenvs',
    'long_description': "bundler.py\n==========\n\nA simple tool for packing shippable virtualenvs\n\n### bundler.py bundle [-h] [--output OUTPUT] [--compression {gz,bz2,xz} | --gz | --bz2 | --xz] [venv]\n\nBundle a virtualenv folder into a tarball, ready for caching or shipping between environments\n\nOutput files are just compressed tar files, with an additional metadata file (currently unused, but \nintended for future validation post-unpacking)\n\n### bundler.py unpack [-h] [--shebang SHEBANG] [--python PYTHON] [--no-repair] bundle_path [output]\n\nUnpack and optionally repair a bundle into a usable virtualenv\n\n### bundler.py repair [-h] [--shebang SHEBANG] [--python PYTHON] path\n\nRepair a virtualenv, rewriting `venv/bin` script shebangs, and updating `bin/python` symlinks to point\nto the correct path.\n\nFuture versions will inspect shebangs before rewriting, so as not to break potential shell scripts\nand other files that get stuck in `venv/bin`\n\n## Development\n\nThis project uses poetry for development dependency management, although it's not strictly necessary.\n\n`py.test` is used for testing, `flakeheaven` for linting, and `black` for formatting.\n",
    'author': 'Franklyn Tackitt',
    'author_email': 'frank@comanage.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DisruptiveLabs/bundler.py',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
