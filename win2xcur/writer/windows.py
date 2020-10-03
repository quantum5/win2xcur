from itertools import chain
from typing import List

from win2xcur.cursor import CursorFrame
from win2xcur.parser import CURParser


def to_cur(frame: CursorFrame) -> bytes:
    header = CURParser.ICON_DIR.pack(0, CURParser.ICO_TYPE_CUR, len(frame))
    directory: List[bytes] = []
    image_data: List[bytes] = []
    offset = CURParser.ICON_DIR.size + len(frame) * CURParser.ICON_DIR_ENTRY.size

    for image in frame:
        clone = image.image.clone()
        if clone.width > 256 or clone.height > 256:
            raise ValueError(f'Image too big for CUR format: {clone.width}x{clone.height}')
        blob = clone.make_blob('png')
        image_data.append(blob)
        x_offset, y_offset = image.hotspot
        directory.append(CURParser.ICON_DIR_ENTRY.pack(
            clone.height & 0xFF, clone.height & 0xFF, 0, 0, x_offset, y_offset, len(blob), offset
        ))
        offset += len(blob)

    return b''.join(chain([header], directory, image_data))
