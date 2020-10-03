import struct
from collections import defaultdict
from typing import Any, Dict, List, Tuple, cast

from win2xcur.cursor import CursorFrame, CursorImage
from win2xcur.parser.base import BaseParser
from win2xcur.utils import image_from_pixels


class XCursorParser(BaseParser):
    MAGIC = b'Xcur'
    VERSION = 0x1_0000
    FILE_HEADER = struct.Struct('<4sIII')
    TOC_CHUNK = struct.Struct('<III')
    CHUNK_IMAGE = 0xFFFD0002
    IMAGE_HEADER = struct.Struct('<IIIIIIIII')

    @classmethod
    def can_parse(cls, blob: bytes) -> bool:
        return blob[:len(cls.MAGIC)] == cls.MAGIC

    def __init__(self, blob: bytes) -> None:
        super().__init__(blob)
        self.frames = self._parse()

    def _unpack(self, struct_cls: struct.Struct, offset: int) -> Tuple[Any, ...]:
        return struct_cls.unpack(self.blob[offset:offset + struct_cls.size])

    def _parse(self) -> List[CursorFrame]:
        magic, header_size, version, toc_size = self._unpack(self.FILE_HEADER, 0)
        assert magic == self.MAGIC

        if version != self.VERSION:
            raise ValueError('Unsupported Xcursor version %r' % version)

        offset = self.FILE_HEADER.size
        chunks: List[Tuple[int, int, int]] = []
        for i in range(toc_size):
            chunk_type, chunk_subtype, position = self._unpack(self.TOC_CHUNK, offset)
            chunks.append((chunk_type, chunk_subtype, position))
            offset += self.TOC_CHUNK.size

        images_by_size: Dict[int, List[Tuple[CursorImage, int]]] = defaultdict(list)

        for chunk_type, chunk_subtype, position in chunks:
            if chunk_type != self.CHUNK_IMAGE:
                continue

            size, actual_type, nominal_size, version, width, height, x_offset, y_offset, delay = \
                self._unpack(self.IMAGE_HEADER, position)

            if size != self.IMAGE_HEADER.size:
                raise ValueError('Unexpected size: %r, expected %r' % (size, self.IMAGE_HEADER.size))

            if actual_type != chunk_type:
                raise ValueError('Unexpected chunk type: %r, expected %r' % (actual_type, chunk_type))

            if nominal_size != chunk_subtype:
                raise ValueError('Unexpected nominal size: %r, expected %r' % (nominal_size, chunk_subtype))

            if width > 0x7FFF:
                raise ValueError('Image width too large: %r' % width)

            if height > 0x7FFF:
                raise ValueError('Image height too large: %r' % height)

            if x_offset > width:
                raise ValueError('Hotspot x-coordinate too large: %r' % x_offset)

            if y_offset > height:
                raise ValueError('Hotspot x-coordinate too large: %r' % y_offset)

            image_start = position + self.IMAGE_HEADER.size
            image_size = width * height * 4
            blob = self.blob[image_start:image_start + image_size]
            if len(blob) != image_size:
                raise ValueError('Invalid image at %d: expected %d bytes, got %d bytes' %
                                 (image_size, image_size, len(blob)))

            images_by_size[nominal_size].append(
                (CursorImage(image_from_pixels(blob, width, height, 'ARGB', 'char'), (x_offset, y_offset)), delay)
            )

        if len(set(map(len, images_by_size.values()))) != 1:
            raise ValueError('win2xcur does not support animations where each size has different number of frames')

        result = []
        for sequence in cast(Any, zip(*images_by_size.values())):
            images: Tuple[CursorImage, ...]
            delays: Tuple[int, ...]
            images, delays = cast(Any, zip(*sequence))

            if len(set(delays)) != 1:
                raise ValueError('win2xcur does not support animations where each size has a different frame delay')

            result.append(CursorFrame(list(images), delays[0]))

        return result
