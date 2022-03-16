import argparse
import os
import sys
import traceback
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from threading import Lock
from typing import BinaryIO

from win2xcur import shadow
from win2xcur.parser import open_blob
from win2xcur.writer import to_x11


def main() -> None:
    parser = argparse.ArgumentParser(description='Converts Windows cursors to X11 cursors.')
    parser.add_argument('files', type=argparse.FileType('rb'), nargs='+',
                        help='Windows cursor files to convert (*.cur, *.ani)')
    parser.add_argument('-o', '--output', '--output-dir', default=os.curdir,
                        help='Directory to store converted cursor files.')
    parser.add_argument('-s', '--shadow', action='store_true',
                        help="Whether to emulate Windows's shadow effect")
    parser.add_argument('-O', '--shadow-opacity', type=int, default=50,
                        help='Opacity of the shadow (0 to 255)')
    parser.add_argument('-r', '--shadow-radius', type=float, default=0.1,
                        help='Radius of shadow blur effect (as fraction of width)')
    parser.add_argument('-S', '--shadow-sigma', type=float, default=0.1,
                        help='Sigma of shadow blur effect (as fraction of width)')
    parser.add_argument('-x', '--shadow-x', type=float, default=0.05,
                        help='x-offset of shadow (as fraction of width)')
    parser.add_argument('-y', '--shadow-y', type=float, default=0.05,
                        help='y-offset of shadow (as fraction of height)')
    parser.add_argument('-c', '--shadow-color', default='#000000',
                        help='color of the shadow')

    args = parser.parse_args()
    print_lock = Lock()

    def process(file: BinaryIO) -> None:
        name = file.name
        blob = file.read()
        try:
            cursor = open_blob(blob)
        except Exception:
            with print_lock:
                print(f'Error occurred while processing {name}:', file=sys.stderr)
                traceback.print_exc()
        else:
            if args.shadow:
                shadow.apply_to_frames(cursor.frames, color=args.shadow_color, radius=args.shadow_radius,
                                       sigma=args.shadow_sigma, xoffset=args.shadow_x, yoffset=args.shadow_y)
            result = to_x11(cursor.frames)
            output = os.path.join(args.output, os.path.splitext(os.path.basename(name))[0])
            with open(output, 'wb') as f:
                f.write(result)

    with ThreadPool(cpu_count()) as pool:
        pool.map(process, args.files)


if __name__ == '__main__':
    main()
