# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyscaffold_interactive']

package_data = \
{'': ['*']}

install_requires = \
['PyScaffold[all]>=4.2.1,<5.0.0', 'click>=8.1.2,<9.0.0']

entry_points = \
{'console_scripts': ['putup-interactive = pyscaffold_interactive.cli:run']}

setup_kwargs = {
    'name': 'pyscaffold-interactive',
    'version': '0.3.0',
    'description': 'Interactive PyScaffold - An interactive Python project template generator based on PyScaffold',
    'long_description': "======================\nPyScaffold-Interactive\n======================\n.. image:: https://travis-ci.org/SarthakJariwala/PyScaffold-Interactive.svg?branch=master\n    :target: https://travis-ci.org/SarthakJariwala/PyScaffold-Interactive\n.. image:: https://badge.fury.io/py/PyScaffold-Interactive.svg\n    :target: https://badge.fury.io/py/PyScaffold-Interactive\n.. image:: https://readthedocs.org/projects/pyscaffold-interactive/badge/?version=latest\n    :target: https://pyscaffold-interactive.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n.. image:: https://coveralls.io/repos/github/SarthakJariwala/PyScaffold-Interactive/badge.svg?branch=master\n    :target: https://coveralls.io/github/SarthakJariwala/PyScaffold-Interactive?branch=master\n.. image:: https://img.shields.io/badge/License-MIT-yellow.svg\n    :target: https://opensource.org/licenses/MIT\n\nAn interactive Python/DataScience project template generator based on `PyScaffold <https://pyscaffold.org/en/latest/>`_\n\n.. image:: demo/pyscaffold_interactive.gif\n\nInstallation\n============\nRecommended (using pipx)\n------------------------\n``pipx install pyscaffold-interactive``\n\nRefer to `pipx documentation <https://pipxproject.github.io/pipx/>`_ for information on how to get pipx\n\nAlternatively (using pip)\n-------------------------\n``pip install pyscaffold-interactive``\n\nUsage\n==========\nAs simple as :\n``putup-interactive``\n\nDescription\n===========\n\nInteractively create a python package or datascience project template using PyScaffold\n\n- Setup a new python project and interactively add details like project name, author name, email, url, description\n- Choose from a selection of licenses\n- Configure automated testing using `tox <https://tox.readthedocs.io/en/latest/index.html>`_\n- Setup continuous integration using `Travis-CI <https://travis-ci.org/>`_\n- Option to add pre-commit file during project setup\n- Create DataScience projects interactively (using the same command)\n- In addition, you get all of PyScaffold's native commands! Just do ``putup --help``\n",
    'author': 'Sarthak Jariwala',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
