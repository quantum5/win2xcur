from dataclasses import dataclass
from typing import Optional

from win2xcur.parser import BaseParser


@dataclass
class CursorTheme:
    name: str

    arrow: Optional[BaseParser] = None
    help: Optional[BaseParser] = None
    working: Optional[BaseParser] = None
    wait: Optional[BaseParser] = None
    crosshair: Optional[BaseParser] = None
    text: Optional[BaseParser] = None
    pen: Optional[BaseParser] = None
    unavailable: Optional[BaseParser] = None
    size_ns: Optional[BaseParser] = None
    size_ew: Optional[BaseParser] = None
    size_nwse: Optional[BaseParser] = None
    size_nesw: Optional[BaseParser] = None
    move: Optional[BaseParser] = None
    up_arrow: Optional[BaseParser] = None
    link: Optional[BaseParser] = None
    location: Optional[BaseParser] = None
    person: Optional[BaseParser] = None
