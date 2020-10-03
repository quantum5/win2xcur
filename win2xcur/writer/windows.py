from io import BytesIO
from itertools import chain
from typing import List, Tuple

from win2xcur.cursor import CursorFrame
from win2xcur.parser import ANIParser, CURParser


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


def get_ani_cur_list(frames: List[CursorFrame]) -> bytes:
    io = BytesIO()
    for frame in frames:
        cur_file = to_cur(frame)
        io.write(ANIParser.CHUNK_HEADER.pack(ANIParser.ICON_CHUNK, len(cur_file)))
        io.write(cur_file)
        if len(cur_file) & 1:
            io.write(b'\0')
    return io.getvalue()


def get_ani_rate_chunk(frames: List[CursorFrame]) -> bytes:
    io = BytesIO()
    io.write(ANIParser.CHUNK_HEADER.pack(ANIParser.RATE_CHUNK, ANIParser.UNSIGNED.size * len(frames)))
    for frame in frames:
        io.write(ANIParser.UNSIGNED.pack(int(round(frame.delay * 60))))
    return io.getvalue()


def to_ani(frames: List[CursorFrame]) -> bytes:
    ani_header = ANIParser.ANIH_HEADER.pack(
        ANIParser.ANIH_HEADER.size, len(frames), len(frames), 0, 0, 32, 1, 1, ANIParser.ICON_FLAG
    )

    cur_list = get_ani_cur_list(frames)
    chunks = [
        ANIParser.CHUNK_HEADER.pack(ANIParser.HEADER_CHUNK, len(ani_header)),
        ani_header,
        ANIParser.RIFF_HEADER.pack(ANIParser.LIST_CHUNK, len(cur_list) + 4, ANIParser.FRAME_TYPE),
        cur_list,
        get_ani_rate_chunk(frames),
    ]
    body = b''.join(chunks)
    riff_header: bytes = ANIParser.RIFF_HEADER.pack(ANIParser.SIGNATURE, len(body) + 4, ANIParser.ANI_TYPE)
    return riff_header + body


def to_smart(frames: List[CursorFrame]) -> Tuple[str, bytes]:
    if len(frames) == 1:
        return '.cur', to_cur(frames[0])
    else:
        return '.ani', to_ani(frames)
