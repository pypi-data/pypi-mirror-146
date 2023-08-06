======================
PyScaffold-Interactive
======================
.. image:: https://travis-ci.org/SarthakJariwala/PyScaffold-Interactive.svg?branch=master
    :target: https://travis-ci.org/SarthakJariwala/PyScaffold-Interactive
.. image:: https://badge.fury.io/py/PyScaffold-Interactive.svg
    :target: https://badge.fury.io/py/PyScaffold-Interactive
.. image:: https://readthedocs.org/projects/pyscaffold-interactive/badge/?version=latest
    :target: https://pyscaffold-interactive.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://coveralls.io/repos/github/SarthakJariwala/PyScaffold-Interactive/badge.svg?branch=master
    :target: https://coveralls.io/github/SarthakJariwala/PyScaffold-Interactive?branch=master
.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT

An interactive Python/DataScience project template generator based on `PyScaffold <https://pyscaffold.org/en/latest/>`_

.. image:: demo/pyscaffold_interactive.gif

Installation
============
Recommended (using pipx)
------------------------
``pipx install pyscaffold-interactive``

Refer to `pipx documentation <https://pipxproject.github.io/pipx/>`_ for information on how to get pipx

Alternatively (using pip)
-------------------------
``pip install pyscaffold-interactive``

Usage
==========
As simple as :
``putup-interactive``

Description
===========

Interactively create a python package or datascience project template using PyScaffold

- Setup a new python project and interactively add details like project name, author name, email, url, description
- Choose from a selection of licenses
- Configure automated testing using `tox <https://tox.readthedocs.io/en/latest/index.html>`_
- Setup continuous integration using `Travis-CI <https://travis-ci.org/>`_
- Option to add pre-commit file during project setup
- Create DataScience projects interactively (using the same command)
- In addition, you get all of PyScaffold's native commands! Just do ``putup --help``
