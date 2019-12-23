ZbarLight
=========

``zbarlight`` is a simple wrapper for the zbar library. For now, it can read all zbar supported codes. Contributions,
suggestions and pull requests are welcome.

``zbarlight`` is hosted on Github at <https://github.com/Polyconseil/zbarlight/>.

Installation
============

You need to install ZBar Bar Code Reader <http://zbar.sourceforge.net/> and its headers before installing ``zbarlight``.

On Debian
~~~~~~~~~

.. code-block:: console

    $ apt-get install libzbar0 libzbar-dev
    $ pip install zbarlight  # you can also use setuptools directly

On Mac OS X
~~~~~~~~~~~

.. code-block:: console

    $ brew install zbar
    $ export LDFLAGS="-L$(brew --prefix zbar)/lib"
    $ export CFLAGS="-I$(brew --prefix zbar)/include"
    $ pip install zbarlight

On Windows
~~~~~~~~~~

Instruction can be found on <https://gist.github.com/Zephor5/aea563808d80f488310869b69661f330>.

How To use ZbarLight
====================

.. code-block:: python

    from PIL import Image
    import zbarlight

    file_path = './tests/fixtures/two_qr_codes.png'
    with open(file_path, 'rb') as image_file:
        image = Image.open(image_file)
        image.load()

    codes = zbarlight.scan_codes(['qrcode'], image)
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
    codes = zbarlight.scan_codes(['qrcode'], new_image)
    print('QR codes: %s' % codes)

Some other cases without known solutions are show in the ``scan_codes()`` tests (search for the expected failures). Any
clues on these cases is welcome.
