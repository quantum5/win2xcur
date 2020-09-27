from typing import List

from wand.image import BaseImage, Image

from win2xcur.cursor import CursorFrame


def apply_to_image(image: BaseImage, *, color: str, radius: float, sigma: float, xoffset: float,
                   yoffset: float) -> Image:
    opacity = Image(width=image.width, height=image.height, pseudo='xc:white')
    opacity.composite(image.channel_images['opacity'], left=round(xoffset * image.width),
                      top=round(yoffset * image.height))
    opacity.gaussian_blur(radius * image.width, sigma * image.width)
    opacity.negate()
    opacity.modulate(50)

    shadow = Image(width=image.width, height=image.height, pseudo='xc:' + color)
    shadow.composite(opacity, operator='copy_opacity')

    result = image.clone()
    result.composite(shadow, operator='difference')
    return result


def apply_to_frames(frames: List[CursorFrame], *, color: str, radius: float,
                    sigma: float, xoffset: float, yoffset: float) -> None:
    for frame in frames:
        for cursor in frame:
            cursor.image = apply_to_image(cursor.image, color=color, radius=radius,
                                          sigma=sigma, xoffset=xoffset, yoffset=yoffset)
