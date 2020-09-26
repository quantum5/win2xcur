from win2xcur.parser.ani import ANIParser
from win2xcur.parser.cur import CURParser

PARSERS = [CURParser, ANIParser]


def open_blob(blob):
    for parser in PARSERS:
        if parser.can_parse(blob):
            return parser(blob)
    raise ValueError('Unsupported file format')
