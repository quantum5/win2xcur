from typing import List
import bisect

from wand.color import Color

from win2xcur.cursor import CursorFrame

def apply_to_frames(frames: List[CursorFrame]) -> None:
    sizes = [32, 48, 64, 96, 128, 256]
    
    for frame in frames:
        for cursor in frame:
            size_index = bisect.bisect_left(sizes, cursor.image.width)

            if size_index < len(sizes):
                next_size = sizes[size_index]
                cursor.image.background_color = Color("transparent")
                cursor.image.extent(width=next_size, height=next_size)

