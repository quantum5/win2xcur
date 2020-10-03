import ctypes

from wand.api import library
from wand.image import Image
from wand.sequence import SingleImage

MagickImportImagePixels = library['MagickImportImagePixels']
MagickImportImagePixels.argtypes = (
    ctypes.c_void_p, ctypes.c_ssize_t, ctypes.c_ssize_t, ctypes.c_size_t,
    ctypes.c_size_t, ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p
)
StorageType = ('undefined', 'char', 'double', 'float',
               'integer', 'long', 'quantum', 'short')


def image_from_pixels(blob: bytes, width: int, height: int, pixel_format: str, pixel_size: str) -> SingleImage:
    image = Image(width=width, height=height)
    MagickImportImagePixels(image.wand, 0, 0, width, height, pixel_format.encode('ascii'),
                            StorageType.index(pixel_size), blob)
    return image.sequence[0]
