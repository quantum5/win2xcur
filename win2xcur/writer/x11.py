from itertools import chain
from operator import itemgetter
from typing import List

from win2xcur.cursor import CursorFrame
from win2xcur.parser import XCursorParser
from win2xcur.utils import premultiply_alpha


def to_x11(frames: List[CursorFrame]) -> bytes:
    chunks = []

    for frame in frames:
        for cursor in frame:
            hx, hy = cursor.hotspot
            header = XCursorParser.IMAGE_HEADER.pack(
                XCursorParser.IMAGE_HEADER.size,
                XCursorParser.CHUNK_IMAGE,
                cursor.nominal,
                1,
                cursor.image.width,
                cursor.image.height,
                hx,
                hy,
                int(frame.delay * 1000),
            )
            chunks.append((
                XCursorParser.CHUNK_IMAGE,
                cursor.nominal,
                header + premultiply_alpha(bytes(cursor.image.export_pixels(channel_map='BGRA')))
            ))

    header = XCursorParser.FILE_HEADER.pack(
        XCursorParser.MAGIC,
        XCursorParser.FILE_HEADER.size,
        XCursorParser.VERSION,
        len(chunks),
    )

    offset = XCursorParser.FILE_HEADER.size + len(chunks) * XCursorParser.TOC_CHUNK.size
    toc = []
    for chunk_type, chunk_subtype, chunk in chunks:
        toc.append(XCursorParser.TOC_CHUNK.pack(
            chunk_type,
            chunk_subtype,
            offset,
        ))
        offset += len(chunk)

    return b''.join(chain([header], toc, map(itemgetter(2), chunks)))
