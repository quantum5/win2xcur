import ntpath
import re
from configparser import ConfigParser, ParsingError
from csv import DictReader
from io import StringIO
from itertools import chain
from pathlib import Path
from typing import Any

from win2xcur.parser import open_blob
from win2xcur.theme import CursorTheme, WIN_CURSORS

reexpand = re.compile(r'%(\w*)%')


def expand_registry(text: str, names: dict[str, str]) -> str:
    def replacer(match: re.Match[str]) -> str:
        name = match.group(1)
        if not name:
            return '%'
        elif name in names:
            return names[name].strip('"')
        else:
            return match.group(0)

    return reexpand.sub(replacer, text)


def parse_inf(inf: Path) -> CursorTheme:
    parser = ConfigParser(allow_no_value=True, strict=False)

    try:
        parser.read(inf)
    except ParsingError as e:
        raise ValueError(e.args[0])

    try:
        reg_sections = parser['DefaultInstall']['AddReg'].split(',')
    except KeyError:
        raise ValueError('Unable to find registry update section in INF')

    try:
        updates = list(chain.from_iterable(list(parser[section.strip()]) for section in reg_sections))
    except KeyError as e:
        raise ValueError(f'Registry update section does not exist in INF: {e.args[0]}')

    updates = [update for update in updates if update.startswith((
        'hkcu,"control panel\\cursors\\schemes",',
        'hklm,"software\\microsoft\\windows\\currentversion\\control panel\\cursors\\schemes",',
    ))]

    if len(updates) == 0:
        raise ValueError('No cursor installs found in INF')
    elif len(updates) > 1:
        raise ValueError('Multiple cursor installs found in INF')

    try:
        strings = dict(parser['Strings'])
    except KeyError:
        strings = {}

    parsed = next(DictReader(StringIO(updates[0]), fieldnames=['root', 'path', 'name', 'flags', 'value']))

    params: dict[str, Any] = {'name': expand_registry(parsed['name'], strings)}
    cursor_paths = expand_registry(parsed['value'], strings).split(',')

    casefolded = {file.name.casefold(): file for file in inf.parent.iterdir() if file.is_file()}

    for name, filename in zip(WIN_CURSORS, cursor_paths):
        if not filename:
            continue

        basename = ntpath.basename(filename)
        try:
            with open(casefolded[basename.casefold()], 'rb') as f:
                params[name] = open_blob(f.read())
        except FileNotFoundError:
            raise ValueError(f'Expected cursor file in same directory as INF: {basename}')

    return CursorTheme(**params)
