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

Troubleshooting
===============

In some case ``zbarlight`` will not be able to detect the 1D or 2D code in an image, one of the known cause is that the
image background color is the same as the foreground color after conversion to grey scale (it's happen on images with
alpha channel). You can use the ``copy_image_on_background`` function to add a background color on your image.

.. code-block:: python

    from PIL import Image
    import zbarlight

    file_path = './tests/fixtures/two_qr_codes.png'
    with open(file_path, 'rb') as image_file:
        image = Image.open(image_file)
        image.load()

    new_image = zbarlight.copy_image_on_background(image, color=zbarlight.WHITE)  # <<<<<<<<<<<<<<<< Add this line <<<<
    codes = zbarlight.scan_codes('qrcode', new_image)
    print('QR codes: %s' % codes)
