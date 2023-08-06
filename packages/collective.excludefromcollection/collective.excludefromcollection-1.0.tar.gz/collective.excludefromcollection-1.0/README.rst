.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://github.com/collective/collective.excludefromcollection/actions/workflows/plone-package.yml/badge.svg
    :target: https://github.com/collective/collective.excludefromcollection/actions/workflows/plone-package.yml

.. image:: https://coveralls.io/repos/github/collective/collective.excludefromcollection/badge.svg?branch=main
    :target: https://coveralls.io/github/collective/collective.excludefromcollection?branch=main
    :alt: Coveralls

.. image:: https://codecov.io/gh/collective/collective.excludefromcollection/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/collective/collective.excludefromcollection

.. image:: https://img.shields.io/pypi/v/collective.excludefromcollection.svg
    :target: https://pypi.python.org/pypi/collective.excludefromcollection/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/collective.excludefromcollection.svg
    :target: https://pypi.python.org/pypi/collective.excludefromcollection
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/collective.excludefromcollection.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/collective.excludefromcollection.svg
    :target: https://pypi.python.org/pypi/collective.excludefromcollection/
    :alt: License


================================
collective.excludefromcollection
================================

Provides a behavior to conditionally exclude an object from a Plone Collection.

Usage
-----

A user can check `exclude_from_collection` in settings tab of a any content type who has the `exclude_from_collection` behavior enabled.
In any Plone Collection one can then add a `Exclude from Collection` filter to filter for that flag.


Translations
------------

This product has been translated into:

- english
- german


Installation
------------

Install collective.excludefromcollection by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.excludefromcollection


and then running ``bin/buildout``


Authors
-------

Provided with love by `Derico <https://derico.de>`_


Contributors
------------

Put your name here, you deserve it!

- ?


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.excludefromcollection/issues
- Source Code: https://github.com/collective/collective.excludefromcollection


Support
-------

If you are having issues, please let us know and open a issue or contact us on Plone Discord channel.


License
-------

The project is licensed under the GPLv2.
