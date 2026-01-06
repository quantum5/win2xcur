import argparse
import os
import sys
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from pathlib import Path

from win2xcur import scale
from win2xcur.parser.xtheme import parse_xcursor_theme
from win2xcur.theme import ALL_CURSORS
from win2xcur.writer.inf import export_windows_theme


def main() -> None:
    parser = argparse.ArgumentParser(description='Converts Windows cursors to X11 cursors.')
    parser.add_argument('source', type=Path, help='X11 cursor files directory')
    parser.add_argument('-n', '--name', required=True, help='name of the cursor theme')
    parser.add_argument('-o', '--output', '--output-dir', type=Path, default=os.curdir,
                        help='Directory to store converted cursor files and install.inf.')
    parser.add_argument('-S', '--scale', default=None, type=float,
                        help='Scale the cursor by the specified factor.')

    args = parser.parse_args()

    if not args.source.is_dir():
        sys.exit(f'Source must be a directory: {args.source}')

    theme = parse_xcursor_theme(args.name, args.source)

    def process(name: str) -> None:
        cursor = getattr(theme, name)
        if args.scale:
            scale.apply_to_frames(cursor.frames, scale=args.scale)

    with ThreadPool(cpu_count()) as pool:
        pool.map(process, ALL_CURSORS)

    args.output.mkdir(exist_ok=True)
    export_windows_theme(theme, args.output)


if __name__ == '__main__':
    main()
