ZbarLight
=========

``zbarlight`` is a simple wrapper for the zbar library. For now, it only allows to read QR codes but contributions,
suggestions and pull requests are welcome.

``zbarlight`` is compatible with Python 2 and Python 3.

``zbarlight`` is hosted on Github at <https://github.com/Polyconseil/zbarlight/>.

Installation
============

You need to install ZBar Bar Code Reader <http://zbar.sourceforge.net/> and its headers to use ``zbarlight``:

- on Debian, ``apt-get install libzbar0 libzbar-dev``
- on Mac OS X, ``brew install zbar``

Then you should use ``pip`` or ``setuptools`` to install the ``zbarlight`` wrapper.

**For Windows installation** Instruction For Windows <https://gist.github.com/Zephor5/aea563808d80f488310869b69661f330>.

How To use ZbarLight
====================

.. code-block:: python

    from PIL import Image
    import zbarlight

    file_path = './tests/fixtures/two_qr_codes.png'
    with open(file_path, 'rb') as image_file:
        image = Image.open(image_file)
        image.load()

    codes = zbarlight.scan_codes('qrcode', image)
    print('QR codes: %s' % codes)
