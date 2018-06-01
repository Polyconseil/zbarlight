import os.path
import unittest

import pytest
from PIL import Image

import zbarlight


def pil_image(file_path):
    with open(file_path, 'rb') as image_file:
        image = Image.open(image_file)
        image.load()
    return image


class ScanCodeTestCase(unittest.TestCase):
    def get_image(self, name, ext='png'):
        return pil_image(
            os.path.join(os.path.dirname(__file__), 'fixtures', '{0}.{1}'.format(name, ext)),
        )

    def test_no_qr_code(self):
        image = self.get_image('no_qr_code')
        self.assertIsNone(zbarlight.scan_codes(['qrcode'], image))

    def test_one_qr_code(self):
        image = self.get_image('one_qr_code')
        code = zbarlight.scan_codes(['qrcode'], image)
        self.assertEqual(code, [b"zbarlight test qr code"])

    def test_two_qr_code(self):
        image = self.get_image('two_qr_codes')
        self.assertEqual(
            sorted(zbarlight.scan_codes(['qrcode'], image)),
            sorted([b'second zbarlight test qr code', b'zbarlight test qr code']),
        )

    def test_one_qr_code_and_one_ean(self):
        image = self.get_image('one_qr_code_and_one_ean')

        # Only read QRcode
        self.assertEqual(
            sorted(zbarlight.scan_codes(['qrcode'], image)),
            sorted([b'zbarlight test qr code']),
        )

        # Only read EAN code
        self.assertEqual(
            sorted(zbarlight.scan_codes(['ean13'], image)),
            sorted([b'0012345678905']),
        )

    def test_one_qr_code_and_one_ean_at_once(self):
        image = self.get_image('one_qr_code_and_one_ean')
        self.assertEqual(
            sorted(zbarlight.scan_codes(['qrcode', 'ean13'], image)),
            sorted([b'zbarlight test qr code', b'0012345678905']),
        )

    def test_unknown_symbology(self):
        image = self.get_image('no_qr_code')
        self.assertRaises(
            zbarlight.UnknownSymbologieError,
            zbarlight.scan_codes, ['not-a-zbar-symbologie'], image,
        )

    def test_need_white_background(self):
        """User submitted sample that can only be decoded after add a white background."""
        # Not working
        image = self.get_image('sample_need_white_background')

        self.assertEqual(
            sorted(zbarlight.scan_codes(['qrcode'], image) or []),
            [],
        )

        # Working when adding white background
        image_with_background = zbarlight.copy_image_on_background(image)
        self.assertEqual(
            sorted(zbarlight.scan_codes(['qrcode'], image_with_background) or []),
            sorted([b'http://en.m.wikipedia.org']),
        )

    def test_code_type_deprecation(self):
        image = self.get_image('one_qr_code_and_one_ean')
        with pytest.deprecated_call():
            self.assertEqual(
                sorted(zbarlight.scan_codes('qrcode', image)),
                sorted([b'zbarlight test qr code']),
            )

    @unittest.expectedFailure
    def test_only_thumbnail_works(self):  # noqa: D200
        """
        User submitted sample that can only be decoded after thumbnail or after adding a black border of at least 5px.
        """
        # thumbnail
        image = self.get_image('sample_only_thumbnail_works', ext='jpg')
        image.thumbnail((image.size[0] / 8, image.size[1] / 8))
        self.assertEqual(
            sorted(zbarlight.scan_codes(['qrcode'], image) or []),
            sorted([b"It's great! Your app works!"]),
        )

        # black border of 5px
        image = self.get_image('sample_only_thumbnail_works', ext='jpg')
        bordered = Image.new("RGB", (image.size[0] + 10, image.size[1] + 10), zbarlight.BLACK)
        bordered.paste(image, box=(5, 5))
        self.assertEqual(
            sorted(zbarlight.scan_codes(['qrcode'], bordered) or []),
            sorted([b"It's great! Your app works!"]),
        )

        # original image
        image = self.get_image('sample_only_thumbnail_works', ext='jpg')
        self.assertEqual(
            sorted(zbarlight.scan_codes(['qrcode'], image) or []),
            sorted([b"It's great! Your app works!"]),
        )
