from win2xcur.writer.windows import to_ani, to_cur, to_smart
from win2xcur.writer.x11 import to_x11

__all__ = ['to_ani', 'to_cur', 'to_smart', 'to_x11']

CONVERTERS = {
    'x11': (to_x11, ''),
    'ani': (to_ani, '.ani'),
    'cur': (to_cur, '.cur'),
}
