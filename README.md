# `win2xcur`

`win2xcur` is a tool that converts cursors from Windows format (`*.cur`,
`*.ani`) to Xcursor format. This allows Windows cursor themes to be used on
Linux, for example.

`win2xcur` is more than a simple image conversion tool. It preserves the cursor
hotspot and animation delay, and has an optional mode to add shadows that
replicates Windows's cursor shadow effect.

## Installation

To install the latest stable version:

    pip install win2xcur

To install from GitHub:

    pip install -e git+https://github.com/quantum5/win2xcur.git

## Usage

For example, if you want to convert [the sample cursor](sample/crosshair.cur):

    mkdir output/
    win2xcur sample/crosshair.cur -o output/

`-s` can be specified to enable shadows.
Multiple cursors files can be specified on the command line.
For example, to convert a directory of cursors with shadows enabled:

    win2xcur input/*.{ani,cur} -o output/ 

For more information, run `win2xcur --help`.
