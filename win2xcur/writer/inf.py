from pathlib import Path

from win2xcur.theme import CursorTheme, WIN_CURSORS
from win2xcur.writer import to_smart

INF_TEMPLATE = """\
; Right click on this file in Windows Explorer and select "Install".
; Then, run `main.cpl` and select the cursor theme "{name}".

[Version]
Signature = "$CHICAGO$"

[DefaultInstall]
CopyFiles = Scheme.Cur
AddReg    = Scheme.Reg

[DestinationDirs]
Scheme.Cur = 10,"%CUR_DIR%"

[Scheme.Reg]
HKLM,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Control Panel\\Cursors\\Schemes","%SCHEME_NAME%",,"{list}"

[Scheme.Cur]
{files}

[Strings]
CUR_DIR = "Cursors\\{name}"
SCHEME_NAME = "{name}"
{mapping}
"""


def export_windows_theme(theme: CursorTheme, directory: Path) -> None:
    files = []
    mapping = {}

    for name in WIN_CURSORS:
        cursor = getattr(theme, name)
        if cursor is None:
            continue

        ext, result = to_smart(cursor.frames)
        filename = f'{name}{ext}'

        with open(directory / filename, 'wb') as f:
            f.write(result)

        files.append(filename)
        mapping[name] = filename

    cursor_list = ','.join((f'%10%\\%CUR_DIR%\\%{name}%' if name in mapping else '') for name in WIN_CURSORS)
    inf_mapping = '\n'.join(f'{key} = "{value}"' for key, value in mapping.items())

    with open(directory / 'install.inf', 'w') as f:
        f.write(INF_TEMPLATE.format(name=theme.name, list=cursor_list, mapping=inf_mapping, files='\n'.join(files)))
