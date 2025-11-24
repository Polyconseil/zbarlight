ChangeLog
=========

4.0 (unreleased)
----------------

- Fix support of PIL (Pillow) 12.


3.0 (2020-01-02)
----------------

- Add Python 3.8 support
- Drop Python 2.7 support (end-of-life 2020-01-01) **breaking change**
- Drop Python 3.4 support (end-of-life 2019-03-18) **breaking change**


2.3 (2019-03-21)
----------------

- Support https://github.com/mchehab/zbar zbar fork (used by ArchLinux)


2.2 (2019-01-21)
----------------

- Add official support for Python 3.7
- Deprecate Python 3.4 (end-of-life 2019-03-16)


2.1 (2018-06-04)
----------------

- Allow to search for more than one kind of bar code at once
- **deprecate** scan_codes(str, Image) in favor of scan_codes(list, Image)


2.0 (2018-01-24)
----------------

- Drop deprecated qr_code_scanner() method
- Add helper to add background color on image


1.2 (2017-03-09)
----------------

- Only return asked symbologie

1.1.0 (2017-01-24)
------------------

- Officially support Python 3.6.
- Drop Python 2.6 support

1.0.2 (2016-08-03)
------------------

- Fix Install for setuptools < 22.0

1.0.1 (2016-06-17)
------------------

* Use zest.releaser
* Use tox
* Do not include tests and docs in package

1.0.0 (2015-09-25)
------------------

* Add generic ``scan_codes()`` function (which can scan multiple codes in the same image)
* Fix Python 2.6 tests
* Exclude tests from package

0.1.1 (2014-12-16)
------------------

* Minor fixes on Readme
* Include requirements-dev.txt in Manifest

0.1.0 (2014-12-12)
------------------

* First public version.
