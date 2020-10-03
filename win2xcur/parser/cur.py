import struct
from typing import List, Tuple

from wand.image import Image

from win2xcur.cursor import CursorFrame, CursorImage
from win2xcur.parser.base import BaseParser


class CURParser(BaseParser):
    MAGIC = b'\0\0\02\0'
    ICO_TYPE_CUR = 2
    ICON_DIR = struct.Struct('<HHH')
    ICON_DIR_ENTRY = struct.Struct('<BBBBHHII')

    @classmethod
    def can_parse(cls, blob: bytes) -> bool:
        return blob[:len(cls.MAGIC)] == cls.MAGIC

    def __init__(self, blob: bytes) -> None:
        super().__init__(blob)
        self._image = Image(blob=blob, format='cur')
        self._hotspots = self._parse_header()
        self.frames = [CursorFrame([
            CursorImage(image, hotspot) for image, hotspot in zip(self._image.sequence, self._hotspots)
        ])]

    def _parse_header(self) -> List[Tuple[int, int]]:
        reserved, ico_type, image_count = self.ICON_DIR.unpack(self.blob[:self.ICON_DIR.size])
        assert reserved == 0
        assert ico_type == self.ICO_TYPE_CUR
        assert image_count == len(self._image.sequence)

        offset = self.ICON_DIR.size
        hotspots = []
        for i in range(image_count):
            width, height, palette, reserved, hx, hy, size, file_offset = self.ICON_DIR_ENTRY.unpack(
                self.blob[offset:offset + self.ICON_DIR_ENTRY.size])
            hotspots.append((hx, hy))
            offset += self.ICON_DIR_ENTRY.size

        return hotspots
