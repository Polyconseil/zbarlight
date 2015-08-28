Reference
=========

.. py:function:: qr_code_scanner(raw, width, height)

    Get QR code from a gray scale image ('Y800' mode)

    :param bytes raw: Image data
    :param int width: Image width
    :param int height: Image height
    :return: The QR code value or None


.. py:function:: scan_codes(symbology, image)

    Get *symbology* codes from a PIL Image

    :param str symbology: Symbology to search
    :param: PIL Image to scan

.. TODO find a better way to handle type validation
.. seealso:: Python types

    .. py:class:: int
    .. py:class:: bytes
