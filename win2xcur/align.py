import bisect
import sys
from typing import List

from wand.color import Color

from win2xcur.cursor import CursorFrame


def apply_to_frames(frames: List[CursorFrame], name: str) -> None:
    sizes = [32, 48, 64, 96, 128, 256]

    for frame in frames:
        for cursor in frame:
            width = cursor.image.width
            height = cursor.image.height

            size_index = bisect.bisect_left(sizes, width)
            if size_index >= len(sizes):
                continue

            next_size = sizes[size_index]
            if next_size == width and next_size == height:
                continue

            if next_size < height:
                print(f'Warning: aligning {width}x{height} cursor would crop content: {name}', file=sys.stderr)

            cursor.image.background_color = Color('transparent')
            cursor.image.extent(width=next_size, height=next_size)
