#!/usr/bin/python
import sys
from PIL import Image
import zbarlight


def main():
    if len(sys.argv) < 2:
        print 'Please input an image file !'
        exit()
    with open(sys.argv[1], 'rb') as image_file:
        image = Image.open(image_file)
        image.load()
        codes = zbarlight.scan_codes('qrcode', image)
        print('QR codes: %s' % codes)

if __name__ == '__main__':
    main()
