from pathlib import Path

from win2xcur.theme import CursorTheme, WIN_CURSORS
from win2xcur.writer import to_smart

INSTALL_INF_TEMPLATE = """\
; Right click on this file in Windows Explorer and select "Install".
; Then, run `main.cpl` and select the cursor theme "{name}".

[Version]
Signature = "$CHICAGO$"

[DefaultInstall]
CopyFiles = Scheme.Cur
AddReg    = Scheme.Reg

[DestinationDirs]
Scheme.Cur = {root},"%CUR_DIR%"

[Scheme.Reg]
{hive},"{key}","%SCHEME_NAME%",,"{list}"

[Scheme.Cur]
{files}

[Strings]
CUR_DIR = "Cursors\\{name}"
SCHEME_NAME = "{name}"
{mapping}
"""

UNINSTALL_INF_TEMPLATE = """\
; Right click on this file in Windows Explorer and select "Install" to
; delete this cursor theme from your computer fully.

[Version]
Signature = "$CHICAGO$"

[DefaultInstall]
DelFiles = Scheme.Cur
DelReg   = Scheme.Reg

[DestinationDirs]
Scheme.Cur = {root},"%CUR_DIR%"

[Scheme.Reg]
{hive},"{key}","%SCHEME_NAME%"

[Scheme.Cur]
{files}

[Strings]
CUR_DIR = "Cursors\\{name}"
SCHEME_NAME = "{name}"
"""


def export_windows_theme(theme: CursorTheme, directory: Path, user: bool = False) -> None:
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

    # 16410 is %AppData%, 10 is %SystemRoot%
    root = 16410 if user else 10
    cursor_list = ','.join((f'%{root}%\\%CUR_DIR%\\%{name}%' if name in mapping else '') for name in WIN_CURSORS)
    inf_mapping = '\n'.join(f'{key} = "{value}"' for key, value in mapping.items())

    format_args = {
        'root': root,
        'hive': 'HKCU' if user else 'HKLM',
        'key': (r'Control Panel\Cursors\Schemes' if user
                else r'SOFTWARE\Microsoft\Windows\CurrentVersion\Control Panel\Cursors\Schemes'),
        'name': theme.name,
        'list': cursor_list,
        'mapping': inf_mapping,
        'files': '\n'.join(files),
    }

    with open(directory / 'install.inf', 'w') as f:
        f.write(INSTALL_INF_TEMPLATE.format(**format_args))

    with open(directory / 'uninstall.inf', 'w') as f:
        f.write(UNINSTALL_INF_TEMPLATE.format(**format_args))
