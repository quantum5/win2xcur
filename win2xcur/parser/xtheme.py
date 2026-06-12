from pathlib import Path
from typing import Any

from win2xcur.parser import open_blob
from win2xcur.theme import CursorTheme, XCURSOR_ALIASES


def parse_xcursor_theme(name: str, directory: Path) -> CursorTheme:
    params: dict[str, Any] = {'name': name}

    for name, candidates in XCURSOR_ALIASES.items():
        for candidate in candidates:
            path = directory / candidate
            if path.is_file():
                with open(path, 'rb') as f:
                    params[name] = open_blob(f.read())
                break

    return CursorTheme(**params)
