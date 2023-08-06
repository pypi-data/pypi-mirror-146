============
Contributing
============

.. _prs: https://github.com/nadime/datetime_formatter/pulls
.. _`beta branch`: https://github.com/nadime/datetime_formatter/tree/beta
.. |contributors| image:: https://img.shields.io/github/contributors/nadime/datetime_formatter
    :target: https://www.github.com/nadime/datetime_formatter
    :alt: contributors

|contributors|


Basics
------

When contributing with fixes and new features, please start forking/branching
from the `beta branch`_ to work on the latest code and reduce merging issues.

Contributed PRs_ are required to include valid test coverage **(99% minimum,
100% whenever possible)** in order to be merged.  Changes without 99% coverage
overall will be rejected by ``pre-commit`` hooks.

Thanks a lot for your support.

Running tests
-------------

First step is installing all the required dependencies with:

.. code-block:: bash

    $ pip install -r requirements.txt

The project provides automated tests and coverage checks with tox; just run:

.. code-block:: bash

    $ tox

Alternatively, you can run pytest to run tests and coverage:

.. code-block:: bash

    $ python -m pytest .
    # if you want to retrieve uncovered lines too:
    $ python -m pytest --cov-report term-missing .

In addition to pytest, you need to ensure that all staged files are up to
standard.

.. _pre-commit: https://github.com/nadime/datetime_formatter/issues

Install `pre-commit`_ and its git hook script so that the quality assurance
tests will run on all staged files before they are committed:

.. code-block:: bash

    $ pip install pre-commit
    $ pre-commit install

To manually run the quality assurance tests on all tracked files:

.. code-block:: bash

    $ pre-commit run -a


Build sphinx documentation
--------------------------

.. _readthedocs.io: https://datetime_formatter.readthedocs.io/

The project provides a Sphinx documentation source under ``./docs/source``,
published online on `readthedocs.io`_.

Great documentation is absolutely key in any a project. If you are not familiar
with reStructuredText for Sphinx you can read a primer
`here`__.

__ https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
