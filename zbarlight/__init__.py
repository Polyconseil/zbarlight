from __future__ import absolute_import, division, print_function, unicode_literals
from ._zbarlight import zbar_code_scanner

from PIL import Image

__version__ = '0.1.1'
__ALL__ = ['code_scanner', 'qr_code_scanner']


def qr_code_scanner(image, width, height):
    """Specific QR code scanner (deprecated)"""
    return zbar_code_scanner(b'qr.enable', image, width, height)


def code_scanner(symbology, image):
    """Generic code scanner"""
    assert Image.isImageType(image)
    converted_image = image.convert('L')  # Convert image to gray scale (8 bits per pixel).
    raw = converted_image.tobytes()  # Get image data.
    width, height = converted_image.size  # Get image size.
    return zbar_code_scanner('{0}.enable'.format(symbology).encode(), raw, width, height)
