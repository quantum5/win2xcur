from typing import List

from win2xcur.cursor import CursorFrame


def apply_to_frames(frames: List[CursorFrame], *, scale: float) -> None:
    for frame in frames:
        for cursor in frame:
            cursor.image.scale(
                int(round(cursor.image.width * scale)),
                int(round(cursor.image.height * scale)),
            )
            cursor.nominal = int(cursor.nominal * scale)
            hx, hy = cursor.hotspot
            cursor.hotspot = (int(hx * scale), int(hy * scale))

def apply_to_frames_MS(frames: List[CursorFrame], *, scales: List[float]) -> List[CursorFrame]:
    frames_MS = []
    for scale in scales:
        frames_s = [frame.clone() for frame in frames]
        apply_to_frames(frames_s, scale=scale)
        frames_MS.extend(frames_s)
    return frames_MS