from typing import List

from wand.color import Color
from wand.image import BaseImage, Image

from win2xcur.cursor import CursorFrame


def apply_to_image(image: BaseImage, *, color: str, radius: float, sigma: float, xoffset: float,
                   yoffset: float) -> Image:
    xoffset = round(xoffset * image.width)
    yoffset = round(yoffset * image.height)
    new_width = image.width + 3 * xoffset
    new_height = image.height + 3 * yoffset

    opacity = Image(width=new_width, height=new_height, pseudo='xc:white')
    opacity.composite(image.channel_images['opacity'], left=xoffset, top=yoffset)
    opacity.gaussian_blur(radius * image.width, sigma * image.width)
    opacity.negate()
    opacity.modulate(50)

    shadow = Image(width=new_width, height=new_height, pseudo='xc:' + color)
    shadow.composite(opacity, operator='copy_opacity')

    result = Image(width=new_width, height=new_height, pseudo='xc:transparent')
    result.composite(image)
    result.composite(shadow, operator='difference')

    trimmed = result.clone()
    trimmed.trim(color=Color('transparent'))
    result.crop(width=max(image.width, trimmed.width), height=max(image.height, trimmed.height))
    return result


def apply_to_frames(frames: List[CursorFrame], *, color: str, radius: float,
                    sigma: float, xoffset: float, yoffset: float) -> None:
    for frame in frames:
        for cursor in frame:
            cursor.image = apply_to_image(cursor.image, color=color, radius=radius,
                                          sigma=sigma, xoffset=xoffset, yoffset=yoffset)
