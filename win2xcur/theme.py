from dataclasses import dataclass
from typing import Optional

from win2xcur.parser.base import BaseParser


@dataclass
class CursorTheme:
    name: str

    # Standard Windows cursors
    arrow: Optional[BaseParser] = None
    help: Optional[BaseParser] = None
    working: Optional[BaseParser] = None
    wait: Optional[BaseParser] = None
    crosshair: Optional[BaseParser] = None
    text: Optional[BaseParser] = None
    pen: Optional[BaseParser] = None
    unavailable: Optional[BaseParser] = None
    size_ns: Optional[BaseParser] = None
    size_ew: Optional[BaseParser] = None
    size_nwse: Optional[BaseParser] = None
    size_nesw: Optional[BaseParser] = None
    move: Optional[BaseParser] = None
    up_arrow: Optional[BaseParser] = None
    link: Optional[BaseParser] = None
    location: Optional[BaseParser] = None
    person: Optional[BaseParser] = None

    # TODO: add some generated cursors here


XCURSOR_ALIASES = {
    'arrow': [
        # Actual arrows
        'default', 'arrow', 'left_ptr', 'top_left_arrow',

        # Other directional cursors
        # TODO: consider rotating up-arrow
        'left-arrow', 'right-arrow', 'down-arrow',
        'sb_left_arrow', 'sb_right_arrow', 'sb_down_arrow',

        # Grab
        'grab', 'openhand',

        # Alias/link
        'alias', 'link', 'dnd-link', '3085a0e285430894940527032f8b26df', '640fb0e74195791501fd1ed57b41487f',
        'a2a266d0498c3104214a47bd64ab0fc8',

        # Sides and corners
        'top_left_corner', 'top_right_corner', 'bottom_left_corner', 'bottom_right_corner',
        'top_side', 'bottom_side', 'left_side', 'right_side',
        'ul_angle', 'ur_angle', 'll_angle', 'lr_angle',

        # Right pointer
        # TODO: consider mirroring left cursor
        'right_ptr', 'draft_large', 'draft_small',

        # Vertical text
        # TODO: consider rotating text
        'vertical-text',

        # Copy
        'copy', 'dnd-copy', '1081e37283d90000800003c07f3ef6bf', '6407b0e94181790501fd1e167b474872',
        'b66166c04f8c3109214a4fbd64a50fc8',

        # Zooming
        'zoom-in', 'zoom-out',

        # Dotbox
        'dotbox', 'dot_box_mask', 'draped_box', 'icon', 'target',

        # Miscellaneous cursors
        'context-menu', 'center_ptr', 'color-picker', 'X_cursor', 'x-cursor', 'wayland-cursor', 'pirate',
        'top_tee', 'bottom_tee', 'left_tee', 'right_tee',
    ],
    'help': ['help', 'left_ptr_help', 'question_arrow', 'whats_this', '5c6cd98b3f3ebcb1f9c7f1c204630408',
             'd9ce0ab605698f320427677b458ad60b'],
    'working': ['progress', 'half-busy', 'left_ptr_watch', '00000000000000020006000e7e9ffc3f',
                '08e8e1c95fe2fc01f976f1e063a24ccd', '3ecb610c1bf2410f44200f48c40d3599'],
    'wait': ['wait', 'watch'],
    'crosshair': [
        # Regular crosshair
        'crosshair', 'cross', 'tcross', 'cross_reverse', 'diamond_cross',

        # Cell selector
        'cell', 'plus',
    ],
    'text': ['text', 'ibeam', 'xterm'],
    'pen': ['pencil', 'draft'],
    'unavailable': [
        # Regular unavailable
        'not-allowed', 'circle', 'crossed_circle', '03b6e0fcb3499374a867c041f52298f0',

        # Drag and drop
        'forbidden', 'no-drop', 'dnd-no-drop',
    ],
    'size_ns': ['size_ver', 'size-ver', 'ns-resize', 'n-resize', 's-resize', 'v_double_arrow', 'sb_v_double_arrow',
                'row-resize', 'split_v', 'double_arrow', '00008160000006810000408080010102',
                '2870a09082c103050810ffdffffe0204'],
    'size_ew': ['size_hor', 'size-hor', 'ew-resize', 'e-resize', 'w-resize', 'h_double_arrow', 'sb_h_double_arrow',
                'col-resize', 'split_h', '14fef782d02440884392942c11205230', '028006030e0e7ebffc7f7070c0600140'],
    'size_nwse': ['size_fdiag', 'size-fdiag', 'nwse-resize', 'nw-resize', 'se-resize', 'bd_double_arrow',
                  'c7088f0f3e6c8088236ef8e1e3e70000'],
    'size_nesw': ['size_bdiag', 'size-bdiag', 'nesw-resize', 'ne-resize', 'sw-resize', 'fd_double_arrow',
                  'fcf1c3c7cd4491d801f1e1c78f100000'],
    'move': [
        # Regular moves
        'fleur', 'size_all', 'all-scroll',

        # Drag and drop
        'move', 'grabbing', 'closedhand', 'dnd-move', 'dnd-none', 'dnd-ask', '4498f0e0c1937ffe01fd06f973665830',
        '9081237383d90e509aa00f00170e968f', 'fcf21c00b30f7e3f83fe0dfd12e71cff',
    ],
    'up_arrow': ['up-arrow', 'sb_up_arrow'],
    'link': ['pointer', 'pointing_hand', 'hand', 'hand1', 'hand2', '9d800788f1b08800ae810202380a0822',
             'e29285e634086352946a0e7090d73106'],
}
