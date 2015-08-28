from __future__ import absolute_import, division, print_function, unicode_literals
from ._zbarlight import zbar_code_scanner

from PIL import Image

__version__ = '0.1.1'
__ALL__ = ['scan_codes', 'qr_code_scanner']


def qr_code_scanner(image, width, height):
    """Specific QR code scanner (deprecated)"""
    result = zbar_code_scanner(b'qr.enable', image, width, height)
    if isinstance(result, list) and len(result) != 1:
        return None
    return result[0] if result is not None else None


def scan_codes(symbology, image):
    """Generic code scanner"""
    assert Image.isImageType(image)
    converted_image = image.convert('L')  # Convert image to gray scale (8 bits per pixel).
    raw = converted_image.tobytes()  # Get image data.
    width, height = converted_image.size  # Get image size.
    return zbar_code_scanner('{0}.enable'.format(symbology).encode(), raw, width, height)
