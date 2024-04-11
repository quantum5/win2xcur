from typing import List

from win2xcur.cursor import CursorFrame


def apply_to_frames(frames: List[CursorFrame], *, scale: float) -> None:
    for frame in frames:
        for cursor in frame:
            cursor.scale(
                int(round(cursor.image.width * scale)),
                int(round(cursor.image.height) * scale),
            )
