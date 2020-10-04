import numpy


def premultiply_alpha(source: bytes) -> bytes:
    buffer = numpy.frombuffer(source, dtype=numpy.uint8).astype(numpy.double)
    alpha = buffer[3::4] / 255.0
    buffer[0::4] *= alpha
    buffer[1::4] *= alpha
    buffer[2::4] *= alpha
    return buffer.astype(numpy.uint8).tobytes()
