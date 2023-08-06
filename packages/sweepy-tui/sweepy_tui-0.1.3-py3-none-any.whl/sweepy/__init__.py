import sweepy
import curses


def startup():
    curses.wrapper(sweepy.main)


if __name__ == "__main__":
    startup()
