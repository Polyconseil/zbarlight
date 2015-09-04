import os.path
import unittest

from PIL import Image

import zbarlight


def zbarlight_image(file_path):
    with open(file_path, 'rb') as image_file:
        image = Image.open(image_file)
        image.load()
    converted_image = image.convert('L')
    image.close()
    return converted_image.tobytes(), converted_image.size


class QRCodeScannerTestCase(unittest.TestCase):
    def assertIsNone(self, obj, msg=None):  # Python 2.6 compatibility
        return self.assertTrue(obj is None, '%s is not None' % repr(obj))

    def get_image(self, name):
        return zbarlight_image(
            os.path.join(os.path.dirname(__file__), 'fixtures', '{0}.png'.format(name))
        )

    def test_no_qr_code(self):
        raw, (width, height) = self.get_image('no_qr_code')
        self.assertIsNone(zbarlight.qr_code_scanner(raw, width, height))

    def test_one_qr_code(self):
        raw, (width, height) = self.get_image('one_qr_code')
        code = zbarlight.qr_code_scanner(raw, width, height)
        self.assertEqual(code, b"zbarlight test qr code")

    def test_two_qr_code(self):
        raw, (width, height) = self.get_image('two_qr_codes')
        self.assertIsNone(zbarlight.qr_code_scanner(raw, width, height))
