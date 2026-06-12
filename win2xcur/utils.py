from typing import Any

import numpy as np


def premultiply_alpha(source: bytes) -> bytes:
    buffer: np.ndarray[Any, np.dtype[np.double]] = np.frombuffer(source, dtype=np.uint8).astype(np.double)
    alpha = buffer[3::4] / 255.0
    buffer[0::4] *= alpha
    buffer[1::4] *= alpha
    buffer[2::4] *= alpha
    return buffer.astype(np.uint8).tobytes()

def unpremultiply_alpha(source: bytes) -> bytes:
    buffer: np.ndarray[Any, np.dtype[np.double]] = np.frombuffer(source, dtype=np.uint8).astype(np.double)
    alpha = buffer[3::4] / 255.0
    np.divide(buffer[0::4], alpha, out=buffer[0::4], where=alpha > 0)
    np.divide(buffer[1::4], alpha, out=buffer[1::4], where=alpha > 0)
    np.divide(buffer[2::4], alpha, out=buffer[2::4], where=alpha > 0)
    buffer = np.clip(buffer, 0, 255)
    return buffer.astype(np.uint8).tobytes()