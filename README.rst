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

How To use ZbarLight
====================

*The new way:*

.. code-block:: python

    from PIL import Image
    import zbarlight

    file_path = './tests/fixtures/two_qr_codes.png'
    with open(file_path, 'rb') as image_file:
        image = Image.open(image_file)
        image.load()

    codes = zbarlight.scan_codes('qrcode', image)
    print('QR codes: %s' % codes)


*The deprecated way:*

.. code-block:: python

    from PIL import Image
    import zbarlight

    file_path = './tests/fixtures/one_qr_code.png'
    with open(file_path, 'rb') as image_file:
        image = Image.open(image_file)
        image.load()
    converted_image = image.convert('L')  # Convert image to gray scale (8 bits per pixel).
    image.close()

    raw = converted_image.tobytes()  # Get image data.
    width, height = converted_image.size  # Get image size.
    code = zbarlight.qr_code_scanner(raw, width, height)

    print('QR code: %s' % code.decode())
