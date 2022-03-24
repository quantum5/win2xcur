# `win2xcur` and `x2wincur` [![Build Status](https://img.shields.io/github/workflow/status/quantum5/win2xcur/Python%20package)](https://github.com/quantum5/win2xcur/actions) [![PyPI](https://img.shields.io/pypi/v/win2xcur.svg)](https://pypi.org/project/win2xcur/) [![PyPI - Format](https://img.shields.io/pypi/format/win2xcur.svg)](https://pypi.org/project/win2xcur/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/win2xcur.svg)](https://pypi.org/project/win2xcur/)

`win2xcur` is a tool that converts cursors from Windows format (`*.cur`,
`*.ani`) to Xcursor format. This allows Windows cursor themes to be used on
Linux, for example.

`win2xcur` is more than a simple image conversion tool. It preserves the cursor
hotspot and animation delay, and has an optional mode to add shadows that
replicates Windows's cursor shadow effect.

`x2wincur` is a tool that does the opposite: it converts cursors in the Xcursor
format to Windows format (`*.cur`, `*.ani`), allowing to use your favourite
Linux cursor themes on Windows.

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

## Troubleshooting

`win2xcur` and `x2wincur` should work out of the box on most systems. If you
are using unconventional distros (e.g. Alpine) and are getting errors related
to `wand`, please see the [Wand documentation on installation][wand-install].

  [wand-install]: https://docs.wand-py.org/en/0.6.7/guide/install.html
