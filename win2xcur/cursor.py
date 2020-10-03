from typing import Iterator, List, Tuple

from wand.sequence import SingleImage


class CursorImage:
    image: SingleImage
    hotspot: Tuple[int, int]

    def __init__(self, image: SingleImage, hotspot: Tuple[int, int]) -> None:
        self.image = image
        self.hotspot = hotspot

    def __repr__(self) -> str:
        return 'CursorImage(image=%r, hotspot=%r)' % (self.image, self.hotspot)


class CursorFrame:
    images: List[CursorImage]
    delay: int

    def __init__(self, images: List[CursorImage], delay: int = 0) -> None:
        self.images = images
        self.delay = delay

    def __getitem__(self, item: int) -> CursorImage:
        return self.images[item]

    def __len__(self) -> int:
        return len(self.images)

    def __iter__(self) -> Iterator[CursorImage]:
        return iter(self.images)

    def __repr__(self) -> str:
        return 'CursorFrame(images=%r, delay=%r)' % (self.images, self.delay)
