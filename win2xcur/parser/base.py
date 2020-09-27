from abc import ABCMeta, abstractmethod
from typing import List

from win2xcur.cursor import CursorFrame


class BaseParser(metaclass=ABCMeta):
    blob: bytes
    frames: List[CursorFrame]

    @abstractmethod
    def __init__(self, blob: bytes) -> None:
        self.blob = blob

    @classmethod
    @abstractmethod
    def can_parse(cls, blob: bytes) -> bool:
        raise NotImplementedError()
