# `win2xcur` and `x2wincur` [![Build Status](https://img.shields.io/github/actions/workflow/status/quantum5/win2xcur/build.yml)](https://github.com/quantum5/win2xcur/actions) [![PyPI](https://img.shields.io/pypi/v/win2xcur.svg)](https://pypi.org/project/win2xcur/) [![PyPI - Format](https://img.shields.io/pypi/format/win2xcur.svg)](https://pypi.org/project/win2xcur/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/win2xcur.svg)](https://pypi.org/project/win2xcur/)

`win2xcur` is a tool that converts cursors from Windows format (`*.cur`,
`*.ani`) to Xcursor format. This allows Windows cursor themes to be used on
Linux, for example.

`win2xcur` is more than a simple image conversion tool. It preserves the cursor
hotspot and animation delay, and has an optional mode to add shadows that
replicates Windows's cursor shadow effect.

`x2wincur` is a tool that does the opposite: it converts cursors in the Xcursor
format to Windows format (`*.cur`, `*.ani`), allowing to use your favourite
Linux cursor themes on Windows.

`win2xcurtheme` converts a packaged Windows cursor theme with an INF installer
into a directory of Xcursors, which can be used to construct your own cursor
theme on Linux.

Conversely, `x2wincurtheme` converts a directory of Xcursors into Windows, while
generating the complementary `install.inf` for easy installation.

## Installation

To install the latest stable version:

    pip install win2xcur

To install from GitHub:

    pip install -e git+https://github.com/quantum5/win2xcur.git

## Usage: `win2xcur`

For example, if you want to convert [the sample cursor](sample/crosshair.cur)
to Linux format:

    mkdir output/
    win2xcur sample/crosshair.cur -o output/

`-s` can be specified to enable shadows.
Multiple cursors files can be specified on the command line.
For example, to convert a directory of cursors with shadows enabled:

    win2xcur input/*.{ani,cur} -o output/ 

For more information, run `win2xcur --help`.

## Usage: `x2wincur`

For example, if you want to convert DMZ-White to Windows:

    mkdir dmz-white/
    x2wincur /usr/share/icons/DMZ-White/cursors/* -o dmz-white/

## Usage: `win2xcurtheme`

To convert an example Windows cursor theme in `example` with an INF installer
`install.inf`:

    mkdir -p example-linux/cursors
    win2xcurtheme example/install.inf -o example-linux/cursors

You can then create `example-linux/index.theme` as follows:

```ini
[Icon Theme]
Name=example
Comment=My example cursor theme.
Example=default
```

## Usage: `x2wincurtheme`

To convert a whole Xcursor theme to Windows format, run `x2wincurtheme` on the
`cursors` subdirectory of an Xcursor theme, then specify a name with `-n`.
For example, for DMZ-White:

    x2wincurtheme /usr/share/icons/DMZ-White/cursors -n DMZ-White -o dmz-white/

## Troubleshooting

`win2xcur`, `x2wincur`, `win2xcurtheme`, and `x2wincurtheme` should work out of
the box on most systems. If you are using unconventional distros (e.g. Alpine)
and are getting errors related to `wand`, please see the
[Wand documentation on installation][wand-install].

  [wand-install]: https://docs.wand-py.org/en/0.6.7/guide/install.html
