import pathlib

import pytest
from PIL import Image

import zbarlight


def get_image(name, ext='png'):
    directory = pathlib.Path(__file__).parent
    file_path = directory / 'fixtures' / '{}.{}'.format(name, ext)
    with open(str(file_path), 'rb') as image_file:
        image = Image.open(image_file)
        image.load()
    return image


def test_no_qr_code():
    image = get_image('no_qr_code')
    assert zbarlight.scan_codes(['qrcode'], image) is None


def compute_parametrize_id(value):
    if isinstance(value, list):
        if all(isinstance(element, bytes) for element in value):
            return '<bytes>'

        return ','.join(value)

    return value


@pytest.mark.parametrize(
    argnames='image_name, symbologies, excepted_codes',
    argvalues=(
        pytest.param(
            'one_qr_code',
            ['qrcode'],
            [b"zbarlight test qr code"],
            id='one-qrcode',
        ),
        pytest.param(
            'two_qr_codes',
            ['qrcode'],
            [b'second zbarlight test qr code', b'zbarlight test qr code'],
            id='two-qrcodes',
        ),
        pytest.param(
            'one_qr_code_and_one_ean',
            ['qrcode'],
            [b'zbarlight test qr code'],
            id='only-detect-qrcodes',
        ),
        pytest.param(
            'one_qr_code_and_one_ean',
            ['ean13'],
            [b'0012345678905'],
            id='only-detect-ean13',
        ),
        pytest.param(
            'one_qr_code_and_one_ean',
            ['qrcode', 'ean13'],
            [b'zbarlight test qr code', b'0012345678905'],
            id='detect-both-qrcodes-and-ean13',
        ),
    ),
    ids=compute_parametrize_id,
)
def test_scan_codes(image_name, symbologies, excepted_codes):
    image = get_image(image_name)
    detected_codes = zbarlight.scan_codes(symbologies, image)
    assert sorted(detected_codes) == sorted(excepted_codes)


def test_unknown_symbology():
    image = get_image('no_qr_code')
    with pytest.raises(zbarlight.UnknownSymbologieError):
        zbarlight.scan_codes(['not-a-zbar-symbologie'], image)


def test_need_white_background():
    """User submitted sample that can only be decoded after add a white background."""
    image = get_image('sample_need_white_background')
    excepted_codes = [b'http://en.m.wikipedia.org']

    # No code is detected on the original image
    original_codes = zbarlight.scan_codes(['qrcode'], image)
    assert original_codes is None

    # But code is detected when adding a white background
    image_with_background = zbarlight.copy_image_on_background(image)
    background_codes = zbarlight.scan_codes(['qrcode'], image_with_background)
    assert background_codes == excepted_codes


def test_code_type_deprecation():
    image = get_image('one_qr_code_and_one_ean')
    expected_codes = [b'zbarlight test qr code']

    with pytest.deprecated_call():
        detected_codes = zbarlight.scan_codes('qrcode', image)

    assert detected_codes == expected_codes


@pytest.mark.xfail
def test_only_thumbnail_works():
    """User submitted sample that can only be decoded after thumbnail or after adding a black border of at least 5px."""
    expected_codes = [b"It's great! Your app works!"]

    # Codes are detected on thumbnail
    image = get_image('sample_only_thumbnail_works', ext='jpg')
    image.thumbnail((image.size[0] / 8, image.size[1] / 8))
    thumbnail_codes = zbarlight.scan_codes(['qrcode'], image)
    assert thumbnail_codes == expected_codes

    # Codes are detected by adding a black border of 5px
    image = get_image('sample_only_thumbnail_works', ext='jpg')
    bordered = Image.new("RGB", (image.size[0] + 10, image.size[1] + 10), zbarlight.BLACK)
    bordered.paste(image, box=(5, 5))
    bordered_codes = zbarlight.scan_codes(['qrcode'], bordered)
    assert bordered_codes == expected_codes

    # Codes are detected on the original image
    image = get_image('sample_only_thumbnail_works', ext='jpg')
    original_codes = zbarlight.scan_codes(['qrcode'], image)
    assert original_codes == expected_codes
