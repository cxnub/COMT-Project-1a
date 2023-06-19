import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
import time


def main(stdscr):
    height, width = stdscr.getmaxyx()
    x, y = 1, 1
    stdscr.nodelay(True)
    def _handle_arrow_keys(key):
        nonlocal x, y
        if key == curses.KEY_LEFT and x > 1:
            x -= 1
        elif key == curses.KEY_RIGHT and x < width - 2:
            x += 1
        elif key == curses.KEY_UP and y > 1:
            y -= 1
        elif key == curses.KEY_DOWN and y < height - 2:
            y += 1

    while True:
        height, width = stdscr.getmaxyx()
        try:
            key = stdscr.getch()
        except:
            key = None
        if key in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN]:
            _handle_arrow_keys(key)
        stdscr.clear()
        stdscr.border()
        stdscr.addstr(y, x, "0")
        stdscr.addstr(0, 0, f"coordinates: {x}, {y}")
        stdscr.refresh()

wrapper(main)
