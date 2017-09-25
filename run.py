
import argparse
from PIL import Image
import zbarlight


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('image', default='./tests/fixtures/two_qr_codes.png', help='input image')
    args = parser.parse_args()
    with open(args.image, 'rb') as image_file:
        image = Image.open(image_file)
        image.load()
        codes = zbarlight.scan_codes('qrcode', image)
        print('QR codes: %s' % codes)

if __name__ == '__main__':
    main()
