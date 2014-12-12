ZbarLight
=========

``zbarlight`` is a simple wrapper for zbar library compatible with Python 2 and Python 3.
For now, it only allows to read QR code but contributions, suggestions and pull requests are welcome.

``zbarlight`` is hosted on Github at <https://github.com/Polyconseil/zbarlight/>.

Installation
============

You need to install ZBar Bar Code Reader <http://zbar.sourceforge.net/> and its header to use ``zbarlight`` (``libzbar0`` and ``libzbar-dev`` on Debian),
then you should use ``pip``, or ``setuptools`` to install the ``zbarlight`` wrapper.

How to use ZbarLight
====================

.. code-block:: python

    from PIL import Image
    import zbarlight

    file_path = './tests/fixtures/one_qr_code.png'
    with open(file_path, 'rb') as image_file:
        image = Image.open(image_file)
        image.load()
    converted_image = image.convert('L')  # Convert image to grayscale (8-bit per pixel).
    image.close()

    raw = converted_image.tobytes()  # Get image data.
    width, height = converted_image.size  # Get image size.
    code = zbarlight.qr_code_scanner(raw, width, height)

    print('QR code: %s' % code.decode())
