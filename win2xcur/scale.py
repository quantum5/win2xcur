from typing import List

from win2xcur.cursor import CursorFrame

def apply_to_frames_by_scales(frames: List[CursorFrame], *, scales: List[float] = None) -> List[CursorFrame]:
    all_frames = []
    for scale in scales:
        for frame in frames:
            frame = frame.clone()
            for cursor in frame:
                cursor.image.scale(
                    int(round(cursor.image.width * scale)),
                    int(round(cursor.image.height * scale)),
                )
                cursor.nominal = int(cursor.nominal * scale)
                hx, hy = cursor.hotspot
                cursor.hotspot = (int(hx * scale), int(hy * scale))
            all_frames.append(frame)
    return all_frames

def apply_to_frames_to_sizes(frames: List[CursorFrame], *, sizes: List[int] = None) -> List[CursorFrame]:
    all_frames = []
    for size in sizes:
        for frame in frames:
            frame = frame.clone()
            for cursor in frame:
                scale = size / cursor.image.width
                cursor.image.scale(
                    size,
                    size,
                )
                cursor.nominal = int(cursor.nominal * scale)
                hx, hy = cursor.hotspot
                cursor.hotspot = (int(hx * scale), int(hy * scale))
            all_frames.append(frame)
    return all_frames
