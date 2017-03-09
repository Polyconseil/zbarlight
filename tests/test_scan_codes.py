import os.path
import unittest

from PIL import Image

import zbarlight


def pil_image(file_path):
    with open(file_path, 'rb') as image_file:
        image = Image.open(image_file)
        image.load()
    return image


class ScanCodeTestCase(unittest.TestCase):
    def assertIsNone(self, obj, msg=None):  # Python 2.6 hack
        return self.assertTrue(obj is None, '%s is not None' % repr(obj))

    def get_image(self, name):
        return pil_image(
            os.path.join(os.path.dirname(__file__), 'fixtures', '{0}.png'.format(name))
        )

    def test_no_qr_code(self):
        image = self.get_image('no_qr_code')
        self.assertIsNone(zbarlight.scan_codes('qrcode', image))

    def test_one_qr_code(self):
        image = self.get_image('one_qr_code')
        code = zbarlight.scan_codes('qrcode', image)
        self.assertEqual(code, [b"zbarlight test qr code"])

    def test_two_qr_code(self):
        image = self.get_image('two_qr_codes')
        self.assertEqual(
            sorted(zbarlight.scan_codes('qrcode', image)),
            sorted([b'second zbarlight test qr code', b'zbarlight test qr code']),
        )

    def test_one_qr_code_and_one_ean(self):
        image = self.get_image('one_qr_code_and_one_ean')

        # Only read QRcode
        self.assertEqual(
            sorted(zbarlight.scan_codes('qrcode', image)),
            sorted([b'zbarlight test qr code']),
        )

        # Only read EAN code
        self.assertEqual(
            sorted(zbarlight.scan_codes('ean13', image)),
            sorted([b'0012345678905']),
        )

    def test_unknown_symbology(self):
        image = self.get_image('no_qr_code')
        self.assertRaises(
            zbarlight.UnknownSymbologieError,
            zbarlight.scan_codes, 'not-a-zbar-symbologie', image,
        )
