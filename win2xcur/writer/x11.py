import os
import subprocess
import sys
from tempfile import TemporaryDirectory
from typing import List

from wand.image import Image

from win2xcur.cursor import CursorFrame

xcursorgen_checked = False


def check_xcursorgen() -> None:
    global xcursorgen_checked
    if xcursorgen_checked:
        return

    try:
        subprocess.check_call(['xcursorgen', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        raise RuntimeError('xcursorgen must be installed to create X11 cursors!')
    else:
        xcursorgen_checked = True


def to_x11(frames: List[CursorFrame]) -> bytes:
    check_xcursorgen()

    counter = 0
    configs = []
    with TemporaryDirectory() as png_dir:
        for frame in frames:
            for cursor in frame:
                name = '%d.png' % (counter,)
                hx, hy = cursor.hotspot
                configs.append('%d %d %d %s %d' % (cursor.image.width, hx, hy, name, int(frame.delay * 1000)))

                image = Image(image=cursor.image)
                image.save(filename=os.path.join(png_dir, name))
                counter += 1

        output_file = os.path.join(png_dir, 'cursor')
        process = subprocess.Popen(['xcursorgen', '-p', png_dir, '-', output_file], stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        _, error = process.communicate('\n'.join(configs).encode(sys.getfilesystemencoding()))
        if process.wait() != 0:
            raise RuntimeError('xcursorgen failed: %r' % error)

        with open(output_file, 'rb') as f:
            result = f.read()

    return result
