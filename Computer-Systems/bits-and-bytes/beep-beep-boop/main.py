import time
import sys
import tty
import termios


def make_sound(n):
    for _ in range(n):
        sys.stdout.buffer.write(b'\x07')
        sys.stdout.buffer.flush()
        time.sleep(0.5)


def wait_for_input():
    try:
        times = int(sys.stdin.read(1))
        if (times < 1 or times > 9):
            raise ValueError
        return times
    except ValueError:
        print("This is not a valid value. Please try again.")
        return wait_for_input()


def main():
    print("Just enter the number of times you would like to hear the beep.")
    while True:
        times = wait_for_input()
        make_sound(times)
        raise Exception


if (__name__ == '__main__'):
    tty_attrs = termios.tcgetattr(0)
    tty.setcbreak(0)
    try:
        main()
    finally:
        pass
        # termios.tcsetattr(0, termios.TCSADRAIN, tty_attrs)
