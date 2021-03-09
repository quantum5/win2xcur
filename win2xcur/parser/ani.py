import struct
from copy import copy
from typing import Any, Iterable, List, Tuple

from win2xcur.cursor import CursorFrame
from win2xcur.parser.base import BaseParser
from win2xcur.parser.cur import CURParser


class ANIParser(BaseParser):
    SIGNATURE = b'RIFF'
    ANI_TYPE = b'ACON'
    HEADER_CHUNK = b'anih'
    LIST_CHUNK = b'LIST'
    SEQ_CHUNK = b'seq '
    RATE_CHUNK = b'rate'
    FRAME_TYPE = b'fram'
    ICON_CHUNK = b'icon'
    RIFF_HEADER = struct.Struct('<4sI4s')
    CHUNK_HEADER = struct.Struct('<4sI')
    ANIH_HEADER = struct.Struct('<IIIIIIIII')
    UNSIGNED = struct.Struct('<I')
    SEQUENCE_FLAG = 0x2
    ICON_FLAG = 0x1

    @classmethod
    def can_parse(cls, blob: bytes) -> bool:
        signature: bytes
        size: int
        subtype: bytes
        try:
            signature, size, subtype = cls.RIFF_HEADER.unpack(blob[:cls.RIFF_HEADER.size])
        except struct.error:
            return False
        return signature == cls.SIGNATURE and subtype == cls.ANI_TYPE

    def __init__(self, blob: bytes) -> None:
        super().__init__(blob)
        if not self.can_parse(blob):
            raise ValueError('Not a .ani file')
        self.frames = self._parse(self.RIFF_HEADER.size)

    def _unpack(self, struct_cls: struct.Struct, offset: int) -> Tuple[Any, ...]:
        return struct_cls.unpack(self.blob[offset:offset + struct_cls.size])

    def _read_chunk(self, offset: int, expected: Iterable[bytes]) -> Tuple[bytes, int, int]:
        found = []
        while True:
            name, size = self._unpack(self.CHUNK_HEADER, offset)
            offset += self.CHUNK_HEADER.size
            if name in expected:
                break
            found += [name]
            offset += size
            if offset >= len(self.blob):
                raise ValueError(f'Expected chunk {expected!r}, found {found!r}')
        return name, size, offset

    def _parse(self, offset: int) -> List[CursorFrame]:
        _, size, offset = self._read_chunk(offset, expected=[self.HEADER_CHUNK])

        if size != self.ANIH_HEADER.size:
            raise ValueError(f'Unexpected anih header size {size}, expected {self.ANIH_HEADER.size}')

        size, frame_count, step_count, width, height, bit_count, planes, display_rate, flags = self.ANIH_HEADER.unpack(
            self.blob[offset:offset + self.ANIH_HEADER.size])

        if size != self.ANIH_HEADER.size:
            raise ValueError(f'Unexpected size in anih header {size}, expected {self.ANIH_HEADER.size}')

        if not flags & self.ICON_FLAG:
            raise NotImplementedError('Raw BMP images not supported.')

        offset += self.ANIH_HEADER.size

        frames = []
        order = list(range(frame_count))
        delays = [display_rate for _ in range(step_count)]

        while offset < len(self.blob):
            name, size, offset = self._read_chunk(offset, expected=[self.LIST_CHUNK, self.SEQ_CHUNK, self.RATE_CHUNK])
            if name == self.LIST_CHUNK:
                list_end = offset + size
                if self.blob[offset:offset + 4] != self.FRAME_TYPE:
                    raise ValueError(
                        f'Unexpected RIFF list type: {self.blob[offset:offset + 4]!r}, expected {self.FRAME_TYPE!r}')
                offset += 4

                for i in range(frame_count):
                    _, size, offset = self._read_chunk(offset, expected=[self.ICON_CHUNK])
                    frames.append(CURParser(self.blob[offset:offset + size]).frames[0])
                    offset += size
                    if offset & 1:
                        offset += 1

                if offset != list_end:
                    raise ValueError(f'Wrong RIFF list size: {offset}, expected {list_end}')
            elif name == self.SEQ_CHUNK:
                order = [i for i, in self.UNSIGNED.iter_unpack(self.blob[offset:offset + size])]
                if len(order) != step_count:
                    raise ValueError(f'Wrong animation sequence size: {len(order)}, expected {step_count}')
                offset += size
            elif name == self.RATE_CHUNK:
                delays = [i for i, in self.UNSIGNED.iter_unpack(self.blob[offset:offset + size])]
                if len(delays) != step_count:
                    raise ValueError(f'Wrong animation rate size: {len(delays)}, expected {step_count}')
                offset += size

        if len(order) != step_count:
            raise ValueError('Required chunk "seq " not found.')

        sequence = [copy(frames[i]) for i in order]
        for frame, delay in zip(sequence, delays):
            frame.delay = delay / 60

        return sequence
