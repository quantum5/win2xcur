import argparse

from win2xcur.cursor import CursorImage
from win2xcur.parser import open_blob


def print_images(images: list[CursorImage], prefix: str = '') -> None:
    for i, image in enumerate(images, 1):
        dimensions = f'{image.image.width}x{image.image.height}'
        print(f'{prefix}{i}. nominal size {image.nominal}, {dimensions}, hotspot: {image.hotspot}')


def main() -> None:
    parser = argparse.ArgumentParser(description='Converts Windows cursors to X11 cursors.')
    parser.add_argument('files', type=argparse.FileType('rb'), nargs='+',
                        help='Cursor files to inspect (*.cur, *.ani, or any X11 cursor)')
    args = parser.parse_args()

    for i, file in enumerate(args.files):
        if i:
            print()

        cursor = open_blob(file.read())
        print(f'Cursor file: {file.name}')

        if len(cursor.frames) > 1:
            for j, frame in enumerate(cursor.frames):
                print(f'  - Frame {j}, delay {frame.delay * 1000} ms')
                print_images(frame.images, prefix='    ')
        else:
            print_images(cursor.frames[0].images)


if __name__ == '__main__':
    main()
