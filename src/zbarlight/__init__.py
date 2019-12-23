import warnings

import pkg_resources
from PIL import Image

from ._zbarlight import Symbologies
from ._zbarlight import zbar_code_scanner

__version__ = pkg_resources.get_distribution('zbarlight').version
__ALL__ = [
    'Symbologies',
    'UnknownSymbologieError',
    'scan_codes',
    'copy_image_on_background',
    'BLACK',
    'WHITE',
]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class UnknownSymbologieError(Exception):
    pass


def scan_codes(code_types, image):
    """
    Get *code_type* codes from a PIL Image.

    *code_type* can be any of zbar supported code type [#zbar_symbologies]_:

    - **EAN/UPC**: EAN-13 (`ean13`), UPC-A (`upca`), EAN-8 (`ean8`) and UPC-E (`upce`)
    - **Linear barcode**: Code 128 (`code128`), Code 93 (`code93`), Code 39 (`code39`), Interleaved 2 of 5 (`i25`),
      DataBar (`databar`) and DataBar Expanded (`databar-exp`)
    - **2D**: QR Code (`qrcode`)
    - **Undocumented**: `ean5`, `ean2`, `composite`, `isbn13`, `isbn10`, `codabar`, `pdf417`

    .. [#zbar_symbologies] http://zbar.sourceforge.net/iphone/userguide/symbologies.html

    Args:
        code_types (list(str)): Code type(s) to search (see ``zbarlight.Symbologies`` for supported values).
        image (PIL.Image.Image): Image to scan

    returns:
        A list of *code_type* code values or None

    """
    if isinstance(code_types, str):
        code_types = [code_types]
        warnings.warn(
            'Using a str for code_types is deprecated, please use a list of str instead',
            DeprecationWarning,
        )

    # Translate symbologies
    symbologies = [
        Symbologies.get(code_type.upper())
        for code_type in set(code_types)
    ]

    # Check that all symbologies are known
    if None in symbologies:
        bad_code_types = [code_type for code_type in code_types if code_type.upper() not in Symbologies]
        raise UnknownSymbologieError('Unknown Symbologies: %s' % bad_code_types)

    # Convert the image to be used by c-extension
    if not Image.isImageType(image):
        raise RuntimeError('Bad or unknown image format')
    converted_image = image.convert('L')  # Convert image to gray scale (8 bits per pixel).
    raw = converted_image.tobytes()  # Get image data.
    width, height = converted_image.size  # Get image size.

    return zbar_code_scanner(symbologies, raw, width, height)


def copy_image_on_background(image, color=WHITE):
    """
    Create a new image by copying the image on a *color* background.

    Args:
        image (PIL.Image.Image): Image to copy
        color (tuple): Background color usually WHITE or BLACK

    Returns:
        PIL.Image.Image

    """
    background = Image.new("RGB", image.size, color)
    background.paste(image, mask=image.split()[3])
    return background
