# FIXME: this could probably be removed by properly typing
# `zbarlight.scan_codes()`.
try:
    from PIL import Image
    is_image = Image.isImageType
except AttributeError:
    # Image.isImageType has been removed from PIL 12.0
    def is_image(im):
        return isinstance(im, Image.Image)
