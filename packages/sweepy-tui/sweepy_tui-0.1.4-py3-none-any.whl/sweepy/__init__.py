import game
import curses


def startup():
    curses.wrapper(game.main)

