from __future__ import absolute_import, division, print_function, unicode_literals
import warnings

from PIL import Image
import pkg_resources

from ._zbarlight import Symbologies, zbar_code_scanner


__version__ = pkg_resources.get_distribution('zbarlight').version
__ALL__ = ['Symbologies', 'UnknownSymbologieError', 'scan_codes', 'qr_code_scanner']


class UnknownSymbologieError(Exception):
    pass


def scan_codes(code_type, image):
    """Get *code_type* codes from a PIL Image

    *code_type* can be any of zbar supported code type [#zbar_symbologies]_:

    - **EAN/UPC**: EAN-13 (`ean13`), UPC-A (`upca`), EAN-8 (`ean8`) and UPC-E (`upce`)
    - **Linear barcode**: Code 128 (`code128`), Code 93 (`code93`), Code 39 (`code39`), Interleaved 2 of 5 (`i25`),
      DataBar (`databar`) and DataBar Expanded (`databar-exp`)
    - **2D**: QR Code (`qrcode`)
    - **Undocumented**: `ean5`, `ean2`, `composite`, `isbn13`, `isbn10`, `codabar`, `pdf417`

    .. [#zbar_symbologies] http://zbar.sourceforge.net/iphone/userguide/symbologies.html

    Args:
        code_type (str): Code type to search (see ``zbarlight.Symbologies`` for supported values)
        image (PIL.Image.Image): Image to scan

    returns:
        A list of *code_type* code values or None
    """
    assert Image.isImageType(image)
    converted_image = image.convert('L')  # Convert image to gray scale (8 bits per pixel).
    raw = converted_image.tobytes()  # Get image data.
    width, height = converted_image.size  # Get image size.
    symbologie = Symbologies.get(code_type.upper())
    if not symbologie:
        raise UnknownSymbologieError('Unknown Symbologie: %s' % code_type)
    return zbar_code_scanner(symbologie, raw, width, height)


def qr_code_scanner(image, width, height):
    """Get QR code from a gray scale image ('Y800' mode)

    If the image has more than one QR code, ``None`` is returned.

    This function is deprecated, use ``scan_codes()`` instead.

    Args:
        image (bytes): Image data
        width (int): Image width
        height (int): Image height

    Returns:
        The QR code value or None
    """
    warnings.warn('qr_code_scanner() is deprecated use scan_codes() instead.', DeprecationWarning)
    result = zbar_code_scanner(Symbologies['QRCODE'], image, width, height)
    if isinstance(result, list) and len(result) == 1:
        return result[0]
    return None
