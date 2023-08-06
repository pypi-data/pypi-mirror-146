==================
datetime_formatter
==================

``datetime_formatter`` provides a *DSL (domain-specific language)* for formatting
``datetimes`` inline to strings.  ``datetime_formatter`` is also capable of translating
the ``datetime`` by most intervals, including some that are not supported by
``timedelta`` like "business_day" (skip weekends and holidays).

For example (see `Available Output Formats`_ for full details)

Use ``datetime_formatter`` to format dates effectively, including translations
and holiday/weekend management using easy-to-remember shortcuts
instead of esoteric ``strftime`` shortcuts, i.e.
having to memorize that ``%m`` is month, while ``%M"`` is minute.
For example, use ``YMD`` to refer to a ``YYYYMMDD`` formatting of a date.

``datetime_formatter`` is especially useful for ingestion of configuration files
where complicated date logic either has to be handled outside of the file itself,
making understanding logic harder, or by making all configuration actual
Python code -- which again makes reading harder and interoperability with
non-Python much harder or impossible.  ``datetime_formatter`` allows all of this
formatting to be done inline, making configuration files easier to comprehend.

.. image:: https://github.com/nadime/datetime_formatter/workflows/Tests/badge.svg
    :target: actions

.. image:: https://coveralls.io/repos/github/nadime/datetime_formatter/badge.svg?branch=main
    :target: https://coveralls.io/repos/github/nadime/datetime_formatter/badge.svg?branch=main

.. .. image:: http://img.shields.io/pypi/v/holidays.svg
    :target: https://pypi.python.org/pypi/holidays

.. image:: https://img.shields.io/badge/license-MIT-black
    :target: LICENSE

.. image:: https://readthedocs.org/projects/datetime_formatter/badge/?version=latest
    :target: https://datetime_formatter.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


Install
-------

The latest stable version can always be installed or updated via pip:

.. code-block:: bash

    $ pip install --update datetime_formatter


Documentation
-------------

.. _Read the Docs: https://datetime_formatter.readthedocs.io/

The documentation is hosted on `Read the Docs`_.


Quick Start
-----------

.. code-block:: python3

  from datetime import datetime
  from datetime_formatter import dtfmt

  dtfmt(20050301, "YYYYMMDD") == "20050301"  # True
  dtfmt("2005-03-01", "MMDDYY") == "030105"  # True
  dtfmt("2005-03-01 08:30:00", "HHMMSS") == "083000" # True

You can use the ``dtfmt`` shortcut, intended for use within ``f-strings``, or
you can instantiate a ``DateTimeFormatter`` object and use its ``.format`` method
(or take advantage of the fact that ``__call__`` forwards to ``.format``)

.. code-block:: python3

  dtf = DateTimeFormatter(datetime(2005, 3, 1))
  dtf.format("%YYYYMMDD%") == "20050301"

You can also translate dates and/or times using inline translation syntax, e.g.:

.. code-block:: python3

  dtfmt(20050301, "YMD-M1D") == "20050228"
  dtfmt(20050301, "YMD-M1Y") == "20040301"
  dtfmt("20050301 08:30:00", "DATETIME-P1H") == "2005-03-01 09:30:00"

You can also convert to a new timezone on the fly, but only if you
your ``datetime`` object is not timezone-naive.

.. code-block:: python3

  from dateutil import tz

  utc = tz.gettz("UTC")
  est = tz.gettz("EST")
  dt = datetime(2005, 3, 1, 8, 30, 0, 0, est)
  dtfmt(dt, "ISODT", output_tz=utc) == "2005-03-01T13:30:00+00:00"

The full list of supported output shortcuts and translations are provided
below.  You can also use the ``holidays`` module with translations to skip
well-known holidays, much like you can skip weekends using the ``business_day``
translation size.

.. code-block:: python3

  import holidays
  dtfmt(20061229, "DATE-P2B", holidays=holidays.US()) == "2007-01-03"


Please see the `documentation`_ for additional examples and detailed
information.

Available Output Formats
------------------------

These shortcuts are used either as the ``fmtstr`` argument to ``dtfmt`` or
within a string passed to ``DateTimeFormatter.format`` - in the latter case,
the fields to be replaced must be surrounded by ``%``, e.g. ``%YYYYMMDD%``.

.. list-table::
   :widths: 23 35 23
   :header-rows: 1
   :class: tight-table

   * - FormatShortcut
     - ``datetime`` equivalent (``strftime`` or function)
     - Output format example
   * - ``DATE``
     - ``%Y-%m-%d``
     - 2005-03-01
   * - ``DATETIME``
     - ``%Y-%m-%d %H:%M:%S``
     -  2005-03-01 13:30:00
   * - ``USDATE``
     - ``%x``
     - 03/01/05
   * - ``USDATETIME``
     - ``%x %X``
     - 03/01/05 13:30:00
   * - ``TIME``
     - ``%X``
     - 13:30:00
   * - ``YEAR``
     - ``%Y``
     - 2005
   * - ``YMD``
     - ``%Y%m%d``
     - 20050301
   * - ``YYYYMM``
     - ``%Y%m``
     - 200503
   * - ``MMYYYY``
     - ``%m%Y``
     - 032005
   * - ``YYMM``
     - ``%y%m``
     - 0503
   * - ``MMYY``
     - ``%m%y``
     - 0305
   * - ``YYYYMMDD``
     - ``%Y%m%d``
     - 20050301
   * - ``MMDDYY``
     - ``%m%d%y``
     - 030105
   * - ``MMDDYYYY``
     - ``%m%d%Y``
     - 03012005
   * - ``ISODATE``
     - ``%Y-%m-%d``
     - 2005-03-01
   * - ``ISODATETIME``
     - ``datetime.isoformat``
     - 2005-03-01T13:30:00.200Z-05:00
   * - ``MONTH``
     - ``%m``
     - 03
   * - ``MON``
     - ``%m``
     - 03
   * - ``MONTHABV``
     - ``%b``
     - Mar
   * - ``MONTHNAME``
     - ``%B``
     - March
   * - ``DAYABV``
     - ``%a``
     - Tues
   * - ``DAYNAME``
     - ``%A``
     - Tuesday
   * - ``DAYNUM``
     - ``%w``
     - 2
   * - ``DAYYEAR``
     - ``%j``
     - 060
   * - ``TZOFF``
     - ``%z``
     - -0500
   * - ``TZNAME``
     - ``%Z``
     - EST
   * - ``WEEKNUM``
     - ``%W``
     - 09
   * - ``DAY``
     - ``%d``
     - 01
   * - ``DD``
     - ``%d``
     - 01
   * - ``MM``
     - ``%m``
     - 03
   * - ``YY``
     - ``%y``
     - 05
   * - ``YYYY``
     - ``%Y``
     - 2005
   * - ``LOCALE_DT``
     - ``%c``
     - Tue Mar  1 13:30:00 2005
   * - ``HHMMSS``
     - ``%H:%M:%S``
     - 13:30:00
   * - ``HHMMSSZZ``
     - ``%H:%M:%S.%f``
     - 13:30:00.200000
   * - ``AMPM``
     - ``%p``
     - PM
   * - ``HH``
     - ``%H``
     - 13
   * - ``HH12``
     - ``%I``
     - 01
   * - ``HOUR``
     - ``%H``
     - 13
   * - ``MIN``
     - ``%M``
     - 30
   * - ``SECOND``
     - ``%S``
     - 00
   * - ``SS``
     - ``%S``
     - 00
   * - ``MICROSECOND``
     - ``%f``
     - 200000
   * - ``ZZ``
     - ``%f``
     - 200000



Available Translations
----------------------

Translations are made up of three parts.  The ``direction`` (``M`` or ``P``)
determines whether to go forward/backward (plus/minus).  The ``unit``
(see table below for ``unit``-types) determines how far each step takes us
foward or backward.  Finally the ``size`` is a non-negative integer that tells
us how far to move in the provided ``units``.

.. list-table::
   :widths: 20 10 50
   :header-rows: 1
   :class: tight-table

   * - Part name
     - Possible Values
     - Description
   * - Direction
     - ``[ "M","P","m","p" ]``
     - M = minus, P = plus
   * - Number
     - Integer >= 0
     - The number of units to translate the date by
   * - Size/Unit
     - ``[ "Y","m","D","W","H","M","S","Z","B" ]``
     - .. list-table::
          :widths: 10 40
          :header-rows: 1
          :class: tight-table

          * - Size
            - Meaning
          * - ``Y``
            - Year(s)
          * - ``m``
            - Month(s)
          * - ``D``
            - Day(s)
          * - ``W``
            - Week(s)
          * - ``H``
            - Hour(s)
          * - ``M``
            - Minute(s)
          * - ``S``
            - Second(s)
          * - ``Z``
            - Microsecond(s)
          * - ``B``
            - Business day(s)
          * - ``F``
            - Business week(s)
          * - ``P``
            - Business month(s)
          * - ``K``
            - Business year(s)

You can string together any combination of these three translation parts, e.g.:

.. code-block:: python

  dtfmt(20050301, "YMD-M1B")      # 20050301 minus 2 business days (20050225)
  dtfmt(20050301, "YMD-P1Y")      # 20050301 plus 1 year (20060301)
  dtfmt(20050301, "DATETIME-P1H") # 20050301 00:00:00 plus 1 hour: (2005-03-01 01:00:00)

Beta Version
------------

The latest development (beta) version can be installed directly from GitHub:

.. code-block:: bash

    $ pip install --upgrade https://github.com/nadime/datetime_formatter/tarball/beta

All new features are always first pushed to beta branch, then released on
master branch upon official version upgrades.


Contributions
-------------

.. _Issues: https://github.com/nadime/datetime_formatter/issues
.. _pull requests: https://github.com/nadime/datetime_formatter/pulls
.. _here: CONTRIBUTING.rst

Issues_ and `pull requests`_ are always welcome.  Please see
`here`_ for more information.

License
-------

.. __: LICENSE

Code and documentation are available according to the MIT License
(see LICENSE__).
