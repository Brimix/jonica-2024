import sys
import tty
import termios
import select

fd = None
old_settings = None

def init():
    global fd, old_settings
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)

def stop():
    global fd, old_settings
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def get_stroke():
    global fd
    if select.select([sys.stdin], [], [], 0)[0]:  # Check if input is waiting
        return sys.stdin.read(1)
    else:
        return None
