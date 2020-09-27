import struct
from copy import copy
from typing import Any, Iterable, List, Tuple

from win2xcur.cursor import CursorFrame
from win2xcur.parser.base import BaseParser
from win2xcur.parser.cur import CURParser


class ANIParser(BaseParser):
    SIGNATURE = b'RIFF'
    ANI_TYPE = b'ACON'
    FRAME_TYPE = b'fram'
    RIFF_HEADER = struct.Struct('<4sI4s')
    CHUNK_HEADER = struct.Struct('<4sI')
    ANIH_HEADER = struct.Struct('<IIIIIIIII')
    UNSIGNED = struct.Struct('<I')
    SEQUENCE_FLAG = 0x2
    ICON_FLAG = 0x1

    @classmethod
    def can_parse(cls, blob: bytes) -> bool:
        signature, size, subtype = cls.RIFF_HEADER.unpack(blob[:cls.RIFF_HEADER.size])
        return signature == cls.SIGNATURE and size == len(blob) - 8 and subtype == cls.ANI_TYPE

    def __init__(self, blob: bytes) -> None:
        super().__init__(blob)
        if not self.can_parse(blob):
            raise ValueError('Not a .ani file')
        self.frames = self._parse(self.RIFF_HEADER.size)

    def _unpack(self, struct_cls: struct.Struct, offset: int) -> Tuple[Any, ...]:
        return struct_cls.unpack(self.blob[offset:offset + struct_cls.size])

    def _read_chunk(self, offset: int, expected: Iterable[bytes]) -> Tuple[int, int]:
        name, size = self._unpack(self.CHUNK_HEADER, offset)
        if name not in expected:
            raise ValueError('Expected chunk %r, found %r' % (expected, name))
        return size, offset + self.CHUNK_HEADER.size

    def _parse(self, offset: int) -> List[CursorFrame]:
        size, offset = self._read_chunk(offset, expected=[b'anih'])

        if size != self.ANIH_HEADER.size:
            raise ValueError('Unexpected anih header size %d, expected %d' % (size, self.ANIH_HEADER.size))

        size, frame_count, step_count, width, height, bit_count, planes, display_rate, flags = self.ANIH_HEADER.unpack(
            self.blob[offset:offset + self.ANIH_HEADER.size])

        if not flags & self.ICON_FLAG:
            raise NotImplementedError('Raw BMP images not supported.')

        offset += self.ANIH_HEADER.size
        list_size, offset = self._read_chunk(offset, expected=[b'LIST'])
        list_end = list_size + offset

        if self.blob[offset:offset + 4] != self.FRAME_TYPE:
            raise ValueError('Unexpected RIFF list type: %r, expected %r' %
                             (self.blob[offset:offset + 4], self.FRAME_TYPE))
        offset += 4

        frames = []
        for i in range(frame_count):
            size, offset = self._read_chunk(offset, expected=[b'icon'])
            frames.append(CURParser(self.blob[offset:offset + size]).frames[0])
            offset += size

        if offset != list_end:
            raise ValueError('Wrong RIFF list size: %r, expected %r' % (offset, list_end))

        sequence = frames
        if flags & self.SEQUENCE_FLAG:
            size, offset = self._read_chunk(offset, expected=[b'seq '])
            sequence = [copy(frames[i]) for i, in self.UNSIGNED.iter_unpack(self.blob[offset:offset + size])]
            if len(sequence) != step_count:
                raise ValueError('Wrong animation sequence size: %r, expected %r' % (len(sequence), step_count))
            offset += size

        delays = [display_rate for _ in range(step_count)]
        if offset < len(self.blob):
            size, offset = self._read_chunk(offset, expected=[b'rate'])
            delays = [i for i, in self.UNSIGNED.iter_unpack(self.blob[offset:offset + size])]
            if len(sequence) != step_count:
                raise ValueError('Wrong animation rate size: %r, expected %r' % (len(delays), step_count))

        for frame, delay in zip(sequence, delays):
            frame.delay = delay / 60

        return sequence
