import curses
from .logic import MinesweeperLogic
from .ouija import Ouija, Tile
from pathlib import Path
import os

HOME = Path(os.environ["HOME"])
SWEEPY_ROOT = ".sweepy"
MY_SWEEPY_ROOT = HOME / SWEEPY_ROOT
MY_SWEEPY_WON = MY_SWEEPY_ROOT / "won"
MY_SWEEPY_LOST = MY_SWEEPY_ROOT / "lost"

def generate_tiles():

    tiles = []
    tiles.append(Tile("0", ""))
    tiles.append(Tile("1", "1", Ouija.COLORS["DEFAULT"], curses.A_BOLD))
    tiles.append(Tile("2", "2", Ouija.COLORS["BLUE"], curses.A_BOLD))
    tiles.append(Tile("3", "3", Ouija.COLORS["RED"], curses.A_BOLD))
    tiles.append(Tile("4", "4", Ouija.COLORS["GREEN"], curses.A_BOLD))
    tiles.append(Tile("5", "5", Ouija.COLORS["ORANGE"], curses.A_BOLD))
    tiles.append(Tile("6", "6", Ouija.COLORS["CYAN"], curses.A_BOLD))
    tiles.append(Tile("!", "#", Ouija.COLORS["YELLOW"]))
    tiles.append(Tile("_", "."))
    tiles.append(Tile("x", "x", Ouija.COLORS["BLACK_ON_YELLOW"]))
    tiles.append(Tile("-", ".", Ouija.COLORS["BLACK_ON_YELLOW"]))
    tiles.append(Tile("+", "#", Ouija.COLORS["BLACK_ON_YELLOW"]))
    return tiles

def env_setup():
    if not MY_SWEEPY_ROOT.exists():
        MY_SWEEPY_ROOT.mkdir()
    if not MY_SWEEPY_WON.exists():
        MY_SWEEPY_WON.mkdir()
    if not MY_SWEEPY_LOST.exists():
        MY_SWEEPY_LOST.mkdir()

def game_loop(stdscr, ob, ml):

    game_width = ml.WIDTH
    game_height = ml.HEIGHT
    game_bombs = ml.BOMBS
    cur_y, cur_x = ml.get_first_cell()

    while(True):

        if ml.has_won() or ml.has_lost():
            msg = "You won!" if ml.has_won() else "You lost :("
            base_fn = MY_SWEEPY_WON if ml.has_won() else MY_SWEEPY_LOST

            stdscr.addstr(4, 3, "{} [n]ew game, [r]eplay, or [q]uit?".format(msg))
            ob.draw_board(ml.get_board())

            fn = "{}.sweepy".format(ml.SEED)
            root_fn = MY_SWEEPY_ROOT / fn
            fn_fq = MY_SWEEPY_WON / fn
            if root_fn.exists():
                root_fn.unlink()
            
            ml.save(str(fn_fq))

            while(True):

                ik = stdscr.getkey()
                if ik == 'n':
                    # clear the line
                    stdscr.move(4, 3)
                    stdscr.clrtoeol()

                    ml = MinesweeperLogic()
                    ml.new_game(game_width, game_height, game_bombs)
                    cur_y, cur_x = ml.get_first_cell()
                    break

                elif ik == 'r':
                    stdscr.move(4, 3)
                    stdscr.clrtoeol()
                    ml.new_game(game_width, game_height, game_bombs)
                    cur_y, cur_x = ml.get_first_cell()
                    break
                
                elif ik == 'q':
                    exit()

        game_head(stdscr, ml)
        game_foot(stdscr)
        ob.draw_board(ml.get_board(), cur_y, cur_x)
        in_key = stdscr.getkey()

        # uncover a cell using the enter key
        if in_key == "\n":
            ml.do_move(cur_y, cur_x, "u")
            if ml.get_first_cell():
                cur_y, cur_x = ml.get_closest_cell(cur_y, cur_x)
                #cur_y, cur_x = ml.closest(cur_y, cur_x)

        # flag a cell using the "f" key
        elif in_key == "f":
            ml.do_move(cur_y, cur_x, "x")
            if ml.get_first_cell():
                cur_y, cur_x = ml.get_closest_cell(cur_y, cur_x)
                #cur_y, cur_x = ml.closest(cur_y, cur_x)

        # save a game (and exit) using the "s" key
        elif in_key == "s":
            ob.draw_board(ml.get_board())
            fn = "{}.sweepy".format(ml.SEED)
            root_fn = MY_SWEEPY_ROOT / fn
            ml.save(str(root_fn))
            stdscr.addstr(4, 3, "Game saved!")
            stdscr.getch()
            exit()

        # start a new game with the "n" key
        elif in_key == "n":
            ob.draw_board(ml.get_board())
            stdscr.addstr(4, 3, "new game? (y/n) ")
            choice = stdscr.getkey()
            stdscr.move(4, 3)
            stdscr.clrtoeol()

            if choice == 'y':
                ml = MinesweeperLogic()
                ml.new_game(game_width, game_height, game_bombs)
                cur_y, cur_x = ml.get_first_cell()

        # reset the current game with the "r" key
        elif in_key == "r":
            ob.draw_board(ml.get_board())
            stdscr.addstr(4, 3, "reset the current game? (y/n) ")
            choice = stdscr.getkey()
            stdscr.move(4, 3)
            stdscr.clrtoeol()

            if choice == 'y':
                ml.new_game(game_width, game_height, game_bombs)
                cur_y, cur_x = ml.get_first_cell()

        # quit without saving using the "q" key
        elif in_key == "q":
            ob.draw_board(ml.get_board())
            stdscr.addstr(4, 3, "Quit without saving? (y/n) ")
            choice = stdscr.getkey()
            if choice == 'y':
                exit()
            else:
                stdscr.move(4, 3)
                stdscr.clrtoeol()

        # navigation
        elif in_key == "KEY_LEFT":
            cur_y, cur_x, cost = ml.get_left(cur_y, cur_x)
        elif in_key == "KEY_RIGHT":
            cur_y, cur_x, cost = ml.get_right(cur_y, cur_x)
        elif in_key == "KEY_UP":
            cur_y, cur_x, cost = ml.get_up(cur_y, cur_x)
        elif in_key == "KEY_DOWN":
            cur_y, cur_x, cost = ml.get_down(cur_y, cur_x)
        elif in_key == "\t":
            cur_y, cur_x = ml.closest(cur_y, cur_x)

def game_head(stdscr, ml):
    stdscr.addstr(1, 3, "~ sweepy ~")
    stdscr.addstr(2, 3, "{} bombs, seed: {}".format(str(ml.BOMBS),str(ml.SEED)))
    stdscr.addstr(3, 3, "flags: {:>2}".format(str(ml.get_flag_count())))
    stdscr.refresh()

def game_foot(stdscr):
    stdscr.addstr(24, 3, "u/d/l/r/tab navigation")
    stdscr.addstr(25, 3, "enter: uncover cell")
    stdscr.addstr(26, 3, "'f': (un)flag cell")
    stdscr.addstr(27, 3, "'n': new game")
    stdscr.addstr(28, 3, "'r': reset game")
    stdscr.addstr(29, 3, "'s': save and quit game")
    stdscr.addstr(30, 3, "'q': quit game (without saving)")

def main(stdscr):

    stdscr.clear()
    curses.curs_set(False)

    env_setup()

    # blocks are 2 tall and 4 wide
    ml = MinesweeperLogic()
    board = Ouija(stdscr, 6, 5)
    board.style(corner=None, horiz_edge="=")

    if not board.setup_tiles(generate_tiles()):
        return False

    # print some info
    stdscr.addstr(1, 3, "~ sweepy ~")
    stdscr.addstr(2, 3, "[n]ew game, or [r]esume a game")

    # initial loop
    while(True):
        in_key = stdscr.getkey()

        if in_key == "q":
            exit()
        elif in_key == "n":
            stdscr.addstr(3, 3, "choose a size")
            stdscr.addstr(4, 3, "[0] 8 x 8 (10 bombs)")
            stdscr.addstr(5, 3, "[1] 16 x 8 (25 bombs)")
            while True:
                choice = stdscr.getkey()
                if choice == '0':
                    ml.new_game(8, 8, 10)
                    break
                elif choice == '1':
                    ml.new_game(8, 16, 25)
                    break
                else:
                    stdscr.addstr(6, 3, "invalid choice, choose again")
            break
        elif in_key == "l":
            stdscr.addstr(3, 3, "what game do you want to load? ")
            fn = stdscr.getstr()
            stdscr.addstr(4, 3, fn)
            stdscr.getch()
            ml.SEED = fn.decode('utf-8')
            ml.new_game(8, 16, 25)
            break
        elif in_key == "r":
            current_games = sorted(MY_SWEEPY_ROOT.glob("*.sweepy"))
            stdscr.addstr(3, 3, "there are " + str(len(current_games)) + " games in progress")
            for idx, game in enumerate(current_games):
                stdscr.addstr(4 + idx, 3, "[{}] {}".format(str(idx), str(game.name)))

            if len(current_games) != 0:
                stdscr.addstr(4 + len(current_games), 3, "choose a game")
                while True:
                    r_key = stdscr.getkey()
                    if r_key.isdigit() and int(r_key) in range(len(current_games)):
                        r_game = current_games[int(r_key)]
                        ml.load(str(r_game))
                        break
                    else:
                        stdscr.addstr(4 + len(current_games), 3, "invalid choice, choose a game")
                break

    stdscr.clear()
    game_loop(stdscr, board, ml)

