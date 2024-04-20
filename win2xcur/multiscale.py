from win2xcur.cursor import CursorFrame, CursorImage

MULTSCALE = [16, 24, 32, 48, 64, 96, 128, 192, 256]

def generates_frames(cursor, min_size: int) -> None:
    """Generates multiple sizes for each cursor.

    Args:
        cursor (Cursor): The cursor to generate sizes for.
        min_size (int): The minimum size to generate.

    Returns:
        List[Cursor]: The generated cursors.
    """
    frames = cursor.frames
    new_frames = []
    image_size = frames[0].images[0].nominal
    for size in MULTSCALE:
        if size > image_size:
            continue
        if size < min_size:
            break
        for frame in frames:
            new_images = []
            for cur in frame:
                new_cur = CursorImage(cur.image.clone(), cur.hotspot, cur.nominal)
                new_cur.scale(size, size)
                new_images.append(new_cur)
            new_frame = CursorFrame(new_images, frame.delay)
            new_frames.append(new_frame)
    del cursor.frames[:]
    cursor.frames.extend(new_frames)
