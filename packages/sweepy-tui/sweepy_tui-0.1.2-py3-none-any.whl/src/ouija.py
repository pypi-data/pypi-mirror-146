import curses
from functools import reduce
from enum import Enum
import math

class Ouija:

    class Align(Enum):
        LEFT = 0
        RIGHT = 1
        CENTER = 2

    DEFAULT_VERT_EDGE = "|"
    DEFAULT_HORIZ_EDGE = "~"
    DEFAULT_CORNER = ":"
    DEFAULT_HORIZ_PAD = 1
    DEFAULT_VERT_PAD = 0
    DEFAULT_HORIZ_MARGIN = 0
    DEFAULT_VERT_MARGIN = 0
    DEFAULT_UNIFORM_WIDTH = True
    DEFAULT_ALIGN = Align.LEFT

    class _OuijaColor:
        
        DEFAULT = -1
        BLACK = 0
        RED = 1
        GREEN = 2
        BLUE = 4
        CYAN = 6
        WHITE = 7
        ORANGE = 9
        YELLOW = 11

        def __init__(self, fg=DEFAULT, bg=DEFAULT):
            self.fg = fg
            self.bg = bg

        def color_pair(self):
            # start with an offset of 1 (can't do negatives)
            out = 1

            # hacky bitwise operator for different fg/bg colors
            white_bg = 16
            white_fg = 32
            black_fg = 64

            if self.bg == self.DEFAULT:
                return out + self.fg
            elif self.bg == self.WHITE:
                return out + white_bg + self.fg
            elif self.fg == self.WHITE:
                return out + white_fg + self.bg
            else:
                return out + black_fg + self.bg

    COLORS = {
        "DEFAULT" : _OuijaColor(),
        "BLACK" : _OuijaColor(_OuijaColor.BLACK),
        "RED" : _OuijaColor(_OuijaColor.RED),
        "GREEN" : _OuijaColor(_OuijaColor.GREEN),
        "BLUE" : _OuijaColor(_OuijaColor.BLUE),
        "CYAN" : _OuijaColor(_OuijaColor.CYAN),
        "WHITE" : _OuijaColor(_OuijaColor.WHITE),
        "ORANGE" : _OuijaColor(_OuijaColor.ORANGE),
        "YELLOW" : _OuijaColor(_OuijaColor.YELLOW),

        "RED_ON_WHITE" : _OuijaColor(_OuijaColor.RED, _OuijaColor.WHITE),
        "GREEN_ON_WHITE" : _OuijaColor(_OuijaColor.GREEN, _OuijaColor.WHITE),
        "BLUE_ON_WHITE" : _OuijaColor(_OuijaColor.BLUE, _OuijaColor.WHITE),
        "CYAN_ON_WHITE" : _OuijaColor(_OuijaColor.CYAN, _OuijaColor.WHITE),
        "ORANGE_ON_WHITE" : _OuijaColor(_OuijaColor.ORANGE, _OuijaColor.WHITE),
        "YELLOW_ON_WHITE" : _OuijaColor(_OuijaColor.YELLOW, _OuijaColor.WHITE),

        "WHITE_ON_BLACK" : _OuijaColor(_OuijaColor.WHITE, _OuijaColor.BLACK),
        "WHITE_ON_RED" : _OuijaColor(_OuijaColor.WHITE, _OuijaColor.RED),
        "WHITE_ON_GREEN" : _OuijaColor(_OuijaColor.WHITE, _OuijaColor.GREEN),
        "WHITE_ON_BLUE" : _OuijaColor(_OuijaColor.WHITE, _OuijaColor.BLUE),
        "WHITE_ON_CYAN" : _OuijaColor(_OuijaColor.WHITE, _OuijaColor.CYAN),
        "WHITE_ON_ORANGE" : _OuijaColor(_OuijaColor.WHITE, _OuijaColor.ORANGE),
        "WHITE_ON_YELLOW" : _OuijaColor(_OuijaColor.WHITE, _OuijaColor.YELLOW),

        "BLACK_ON_WHITE" : _OuijaColor(_OuijaColor.BLACK, _OuijaColor.WHITE),
        "BLACK_ON_RED" : _OuijaColor(_OuijaColor.BLACK, _OuijaColor.RED),
        "BLACK_ON_GREEN" : _OuijaColor(_OuijaColor.BLACK, _OuijaColor.GREEN),
        "BLACK_ON_BLUE" : _OuijaColor(_OuijaColor.BLACK, _OuijaColor.BLUE),
        "BLACK_ON_CYAN" : _OuijaColor(_OuijaColor.BLACK, _OuijaColor.CYAN),
        "BLACK_ON_ORANGE" : _OuijaColor(_OuijaColor.BLACK, _OuijaColor.ORANGE),
        "BLACK_ON_YELLOW" : _OuijaColor(_OuijaColor.BLACK, _OuijaColor.YELLOW),
    }

    def _setup_curses_colors():
        
        # initialize colors for curses
        curses.start_color()
        curses.use_default_colors()

        for c in Ouija.COLORS.keys():
            color = Ouija.COLORS[c]
            curses.init_pair(color.color_pair(), color.fg, color.bg)

    def __init__(self, stdscr, y, x):
        self.stdscr = stdscr
        self.y = y
        self.x = x

        # setup default styles
        self.style()

        # setup the curses colors
        Ouija._setup_curses_colors()

    # helper method to access style variables
    def style(self,
              vert_edge=DEFAULT_VERT_EDGE,
              horiz_edge=DEFAULT_HORIZ_EDGE, 
              corner=DEFAULT_CORNER,
              horiz_pad=DEFAULT_HORIZ_PAD,
              vert_pad=DEFAULT_VERT_PAD,
              horiz_margin=DEFAULT_HORIZ_MARGIN,
              vert_margin=DEFAULT_VERT_MARGIN,
              uniform_width=DEFAULT_UNIFORM_WIDTH,
              align=DEFAULT_ALIGN):
        self.vert_edge = vert_edge
        self.horiz_edge = horiz_edge
        self.corner = corner
        self.horiz_pad = horiz_pad
        self.vert_pad = vert_pad
        self.horiz_margin = horiz_margin
        self.vert_margin = vert_margin
        self.uniform_width = uniform_width
        self.align = align

    # setup the tiles
    def setup_tiles(self, ts):
        if type(ts) != list:
            return False
        self.tiles = {}
        for t in ts:
            if type(t) != Tile:
                return False
            self.tiles[t.in_val] = t
        print(str(self.tiles))
        return True

    def calc_cell_width(self, cell_value):
        edges = 2 if self.vert_edge is not None else 0
        return len(cell_value) + (2 * self.horiz_pad) + edges

    def calc_row_width(self, row):
        width = 0
        for cell in row:

            # if there's a cooresponding display value, use its length
            # if not, just take the width directly
            if cell in self.tiles:
                width += self.calc_cell_width(self.tiles[cell].out_val)
            else:
                width += self.calc_cell_width(cell)

        # if there's no margin, we double counted some dividers
        if self.horiz_margin == 0:
            width -= len(row) - 1
        elif self.horiz_margin > 1:
            width += (self.horiz_margin - 1) * (len(row) - 1)

        return width

    # draw the board, optionally highlighting a cell
    def draw_board(self, board, hy=-1, hx=-1):

        # calculate the longest row
        max_row_length = max([len(row) for row in board])

        if self.uniform_width:
            # get the widest possible cell
            out_vals = [i.out_val for i in self.tiles.values()]
            max_cell_width = max([len(x) for x in out_vals])

            # the max row width is the longest row of the widest cells
            max_row_width = self.calc_row_width(["." * max_cell_width] * max_row_length)
        else:
            max_row_width = max([self.calc_row_width(row) for row in board])

        # if specified, make every key as wide as the widest key
        if self.uniform_width:
            out_vals = [i.out_val for i in self.tiles.values()]
            max_width = max([len(x) for x in out_vals])

        # keep track of y-coordinate, and board y-index
        cur_y = self.y
        iy = 0

        # loop through all columns in board
        for col in board:

            if self.uniform_width:
                cur_row_width = self.calc_row_width(["." * max_cell_width] * len(col))
            else:
                cur_row_width = self.calc_row_width(col)
            
            # keep track of x-coordinate, and board x-index
            cur_x = self.x
            ix = 0

            # loop through all cells in the column
            for cell in col:

                tile = self.tiles[cell]

                if self.uniform_width:
                    cell_width = self.calc_cell_width("." * max_cell_width)
                else:
                    cell_width = self.calc_cell_width(tile.out_val)

                target_x = cur_x
                if self.align == Ouija.Align.RIGHT:
                    target_x += max_row_width - cur_row_width
                if self.align == Ouija.Align.CENTER:
                    target_x += math.floor(max_row_width / 2) - math.floor(cur_row_width / 2)


                # create the format string with the appropriate width
                target_width = max_width if self.uniform_width else len(tile.out_val)
                fmt_string = "{:^" + str(target_width) + "}"

                # add A_STANDOUT if the cell needs to be highlighted
                target_style = tile.style
                if hx == ix and hy == iy:
                    target_style = target_style | curses.A_STANDOUT

                # draw the key
                #self.draw_rect_key(cur_y, cur_x, fmt_string.format(tile.out_val), tile.color, target_style)
                self.draw_rect_key(cur_y, target_x, fmt_string.format(tile.out_val), tile.color, target_style)

                # update the x-coordinate, based on width, padding, and margin
                # if there's a vertical edge, add an additional position
                #cur_x += target_width + (2 * self.horiz_pad) + self.horiz_margin
                cur_x += cell_width - 1 + self.horiz_margin

                # update the board x-index
                ix += 1

            # update the y-coordinate, based on padding and margin
            # if there's a horizontal edge, add an additional position
            cur_y += 1 + (2 * self.vert_pad) + self.vert_margin
            if self.horiz_edge is not None:
                cur_y += 1

            # update the board x-index
            iy += 1

    # draw a rectangular key, with the top corner at the given (y, x),
    # the specified text, color, and style
    def draw_rect_key(self, y, x, text, color, style):
        # calculate the inner width, including padding
        iw = len(text) + (2 * self.horiz_pad)

        # outer width and horizontal offset are defaults
        ow = iw
        h_off = 0
        v_off = 1

        # if we have a vertical edge, adjust the outer width and horizontal offset
        if self.vert_edge is not None:
            ow += 2
            h_off += 1

        # create format strings for the inner and outer widths
        owf = "{:^" + str(ow) + "}" 
        iwf = "{:^" + str(iw) + "}" 

        # calculate how tall each cell should be,
        # and where in the cell the text should appear
        max_y = y + 2 + (2 * self.vert_pad)
        mid_y = math.ceil((max_y - y) / 2)

        # draw the horizontal edges, if defined 
        if self.horiz_edge is not None:

            # top edge begins at (y, x), 
            # is 'iw' long, 
            # centered within the 'ow' length
            self.stdscr.addstr(y, x, owf.format(self.horiz_edge * iw))

            # bottom edge takes into account vertical offset 
            # and vertical padding
            self.stdscr.addstr(y + (2 * v_off) + (2 * self.vert_pad), x, owf.format(self.horiz_edge * iw))

        # draw the vertical edges, if defined
        if self.vert_edge is not None:

            # loop through each row we need to draw 
            for iy in range(y + 1, max_y):
                self.stdscr.addstr(iy, x, self.vert_edge)
                self.stdscr.addstr(iy, x + ow - 1, self.vert_edge)

        # draw the corners, if defined
        if self.corner is not None:
            self.stdscr.addstr(y, x, self.corner)
            self.stdscr.addstr(y, x + ow - 1, self.corner)
            self.stdscr.addstr(max_y, x, self.corner)
            self.stdscr.addstr(max_y, x + ow - 1, self.corner)

        # draw the inside
        for iy in range(y + 1, max_y):
            
            # if we're at the mid-point of the cell, draw the text
            # otherwise, don't draw anything
            target_text = text if iy == (y + mid_y) else ""
            self.stdscr.addstr(iy, x + h_off, iwf.format(target_text), style | curses.color_pair(color.color_pair()))

class Tile:

    def __init__(self, in_val, out_val, color=Ouija.COLORS["DEFAULT"], style=0):
        self.in_val = in_val
        self.out_val = out_val
        self.color = color
        self.style = style

    def __str__(self):
        return "[{},{},{}]".format(self.in_val, self.out_val, str(self.color))

# helper function, not sure where it goes yet
def biggest_cell(board):
    return max([max(list(map(lambda x: len(x), row))) for row in board])    

