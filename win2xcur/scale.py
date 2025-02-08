from typing import List

from win2xcur.cursor import CursorFrame


def apply_to_frames(frames: List[CursorFrame], *, scale: float = None, size: int = None) -> None:
    for frame in frames:
        for cursor in frame:
            if size:
                scale = size / cursor.image.width
            cursor.image.scale(
                size or int(round(cursor.image.width * scale)),
                size or int(round(cursor.image.height * scale)),
            )
            cursor.nominal = int(cursor.nominal * scale)
            hx, hy = cursor.hotspot
            cursor.hotspot = (int(hx * scale), int(hy * scale))


def apply_to_frames_MS(frames: List[CursorFrame], *, scales: List[float] = None,
                       sizes: List[int] = None) -> List[CursorFrame]:
    frames_MS = []
    if scales is not None:
        for scale in scales:
            frames_s = [frame.clone() for frame in frames]
            apply_to_frames(frames_s, scale=scale)
            frames_MS.extend(frames_s)
    else:
        for size in sizes:
            frames_s = [frame.clone() for frame in frames]
            apply_to_frames(frames_s, size=size)
            frames_MS.extend(frames_s)
    return frames_MS
