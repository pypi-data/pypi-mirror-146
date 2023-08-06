=======
CHANGES
=======

1.2.0 (2022-04-11)
------------------

- Add support for Python 3.6, 3.7, 3.8, 3.9, 3.10, PyPy3.

- Drop support for Python 3.3 and 3.4.

- Drop support for ``python setup.py test``.


1.1.0 (2016-09-19)
------------------

- Fixed credit card industry validation to check the first number, not
  the second.

- Added support for Python 3.4, 3.5 and PyPy.

- Dropped support for Python 2.6.

- Achieve 100% code test coverage.

- Moved documentation to http://z3cschema.readthedocs.io (see :pr:`11`).

1.0.0 (2013-03-01)
------------------

- Added support for Python 3.3.

- Replaced deprecated ``zope.interface.implements`` usage with equivalent
  ``zope.interface.implementer`` decorator.

- Dropped support for Python 2.4 and 2.5.


0.7.2 (2011-04-03)
------------------

- Fixed i18n files after something injected 'fuzzy' into the PO files.


0.7.1 (2011-04-03)
------------------

- Add nl translations.


0.7.0 (2010-10-18)
------------------

- Updated tests to run with ``zope.schema`` >= 3.6, thus requiring at least
  this version.

- Using Python's ``doctest`` module instead of depreacted
  ``zope.testing.doctest[unit]``.


0.6.1 (2010-10-18)
------------------

- Added french translations.

- Added doctests to ``long_description`` so they appear on PyPI.


0.6.0 (2009-01-26)
------------------

- Humanized exception's doc strings.
- Added translations support.
- Added german translations.
- Added russian translations.
- Changed mailing list address to zope-dev at zope.org, as
  zope3-dev is retired now.

0.5.0 (2008-10-21)
------------------

- Initial release on PyPI.


0.2.0 (2007-09-21)
------------------

- Feature: Added ``DateSelect`` field.


0.1.0 (2007-06-04)
------------------

- Initial release.
