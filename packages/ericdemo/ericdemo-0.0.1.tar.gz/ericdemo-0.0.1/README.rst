========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |github-actions| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/ericdemo/badge/?style=flat
    :target: https://ericdemo.readthedocs.io/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/ericchagnon15/ericdemo/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/ericchagnon15/ericdemo/actions

.. |requires| image:: https://requires.io/github/ericchagnon15/ericdemo/requirements.svg?branch=main
    :alt: Requirements Status
    :target: https://requires.io/github/ericchagnon15/ericdemo/requirements/?branch=main

.. |codecov| image:: https://codecov.io/gh/ericchagnon15/ericdemo/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://codecov.io/github/ericchagnon15/ericdemo

.. |version| image:: https://img.shields.io/pypi/v/ericdemo.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/ericdemo

.. |wheel| image:: https://img.shields.io/pypi/wheel/ericdemo.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/ericdemo

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/ericdemo.svg
    :alt: Supported versions
    :target: https://pypi.org/project/ericdemo

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/ericdemo.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/ericdemo

.. |commits-since| image:: https://img.shields.io/github/commits-since/ericchagnon15/ericdemo/v0.0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/ericchagnon15/ericdemo/compare/v0.0.1...main



.. end-badges

Demo of creating and uploading a package

* Free software: MIT license

Installation
============

::

    pip install ericdemo

You can also install the in-development version with::

    pip install https://github.com/ericchagnon15/ericdemo/archive/main.zip


Documentation
=============


https://ericdemo.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
