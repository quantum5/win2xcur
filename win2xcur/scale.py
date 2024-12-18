from typing import List

from win2xcur.cursor import CursorFrame


def apply_to_frames(frames: List[CursorFrame], *, scale: float) -> None:
    for frame in frames:
        for cursor in frame:
            cursor.image.scale(
                int(round(cursor.image.width * scale)),
                int(round(cursor.image.height) * scale),
            )
            cursor.nominal = int(cursor.nominal * scale)
            hx,hy = cursor.hotspot
            cursor.hotspot = (int(hx * scale),int(hy*scale))

