import argparse
import os
import sys
import traceback

from win2xcur.parser import open_blob
from win2xcur.writer.x11 import check_xcursorgen, to_x11


def main() -> None:
    parser = argparse.ArgumentParser(description='Converts Windows cursors to X11 cursors.')
    parser.add_argument('files', type=argparse.FileType('rb'), nargs='+',
                        help='Windows cursor files to convert (*.cur, *.ani)')
    parser.add_argument('-o', '--output', '--output-dir', default=os.curdir,
                        help='Directory to store converted cursor files.')

    args = parser.parse_args()

    check_xcursorgen()

    for file in args.files:
        name = file.name
        blob = file.read()
        try:
            cursor = open_blob(blob)
        except Exception:
            print('Error occurred while processing %s:' % (name,), file=sys.stderr)
            traceback.print_exc()
        else:
            result = to_x11(cursor.frames)
            output = os.path.join(args.output, os.path.splitext(os.path.basename(name))[0])
            with open(output, 'wb') as f:
                f.write(result)


if __name__ == '__main__':
    main()
