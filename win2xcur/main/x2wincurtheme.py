import argparse
import os
import sys
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from pathlib import Path

from win2xcur import align, scale
from win2xcur.parser.xtheme import parse_xcursor_theme
from win2xcur.theme import ALL_CURSORS
from win2xcur.writer.inf import export_windows_theme


def main() -> None:
    parser = argparse.ArgumentParser(description='Converts X11 cursor themes to Windows ones.')
    parser.add_argument('source', type=Path, help='X11 cursor files directory')
    parser.add_argument('-n', '--name', required=True, help='name of the cursor theme')
    parser.add_argument('-o', '--output', '--output-dir', type=Path, default=os.curdir,
                        help='Directory to store converted cursor files and install.inf.')
    parser.add_argument('-S', '--scale', default=None, type=float,
                        help='Scale the cursor by the specified factor.')
    parser.add_argument('-u', '--user', '--hkcu', default=False, action='store_true',
                        help='Install cursors for the current user only.')
    parser.add_argument('--align-sizes', default=False, action='store_true',
                        help='Align image sizes to Windows default cursor sizes.')

    args = parser.parse_args()

    if not args.source.is_dir():
        sys.exit(f'Source must be a directory: {args.source}')

    theme = parse_xcursor_theme(args.name, args.source)

    if not theme.arrow:
        sys.exit(f'Basic pointer cursor not found in theme: {args.source}')

    def process(name: str) -> None:
        cursor = getattr(theme, name)
        if not cursor:
            return

        if args.scale:
            scale.apply_to_frames(cursor.frames, scale=args.scale)
        if args.align_sizes:
            align.apply_to_frames(cursor.frames, name)

    with ThreadPool(cpu_count()) as pool:
        pool.map(process, ALL_CURSORS)

    args.output.mkdir(exist_ok=True)
    export_windows_theme(theme, args.output, user=args.user)


if __name__ == '__main__':
    main()
