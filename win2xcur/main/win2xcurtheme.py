import argparse
import os
import shutil
import sys
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from pathlib import Path

from win2xcur import scale, shadow
from win2xcur.parser.inf import parse_inf
from win2xcur.theme import XCURSOR_ALIASES
from win2xcur.writer import to_x11


def main() -> None:
    parser = argparse.ArgumentParser(description='Converts Windows cursor themes to X11 cursors.')
    parser.add_argument('inf', type=Path, help='Windows cursor theme to convert (*.inf)')
    parser.add_argument('-o', '--output', '--output-dir', type=Path, default=os.curdir,
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
    parser.add_argument('--scale', default=None, type=float,
                        help='Scale the cursor by the specified factor.')

    args = parser.parse_args()

    if not args.inf.is_file():
        sys.exit(f'INF file not found: {args.inf}')

    theme = parse_inf(args.inf)

    def process(name: str, aliases: list[str]) -> None:
        cursor = getattr(theme, name)
        if cursor is None:
            return

        if args.scale:
            scale.apply_to_frames(cursor.frames, scale=args.scale)

        if args.shadow:
            shadow.apply_to_frames(cursor.frames, color=args.shadow_color, radius=args.shadow_radius,
                                   sigma=args.shadow_sigma, xoffset=args.shadow_x, yoffset=args.shadow_y)

        result = to_x11(cursor.frames)
        canonical = aliases[0]
        with open(args.output / canonical, 'wb') as f:
            f.write(result)

        for alias in aliases[1:]:
            if os.name == 'posix':
                output = args.output / alias
                try:
                    os.symlink(canonical, output)
                except FileExistsError:
                    os.remove(output)
                    os.symlink(canonical, output)
            else:
                shutil.copyfile(args.output / canonical, args.output / alias)

    with ThreadPool(cpu_count()) as pool:
        pool.starmap(process, XCURSOR_ALIASES.items())


if __name__ == '__main__':
    main()
