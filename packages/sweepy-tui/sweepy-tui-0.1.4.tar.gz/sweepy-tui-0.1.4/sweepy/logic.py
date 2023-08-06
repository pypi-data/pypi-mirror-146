import random

# 8x8_10
# 16x16_40
# 16x30_99

# under variables
UNDER_DEFAULT = 0
UNDER_BOMB = -1

# over variables
OVER_DEFAULT = '_'
OVER_FLAGGED = 'x'
OVER_UNCOVERED = 'u'
OVER_MOVES = [OVER_FLAGGED, OVER_UNCOVERED]

# board variables
BOARD_COVERED = '_'
BOARD_FLAGGED = '!'
BOARD_BOMB_UNCOVERED = 'x'
BOARD_BOMB_COVERED = '-'
BOARD_BOMB_FLAGGED = '+'

DELIMITER = '|'

# get a random seed value
def get_seed():
    return random.randint(1,1000000)

class MinesweeperLogic:

    # field is the bombs and the values
    # board is uncovered/flagged
    UNDER = []
    OVER = []

    # other variables
    WIDTH = 0
    HEIGHT = 0
    BOMBS = 0
    SEED = 0

    def __init__(self):
        self.MOVES = []

    def do_all_moves(self):
        for move in self.MOVES:
            self.do_move(int(move[0]), int(move[1]), move[2])

    def load(self, filename):
        # get a handle to the global variables
        #global WIDTH, HEIGHT, BOMBS, SEED, MOVES

        # grab the lines from the file
        with open(filename, 'r') as fil:
            istr = fil.readline().strip()
            moves = fil.readlines()

        # the first line must have 4 numeric values
        try:
            ilist = [int(i) for i in istr.split('|')]
        except ValueError as e:
            return False
        if len(ilist) == 4:

            # set up global variables
            self.WIDTH = ilist[0]
            self.HEIGHT = ilist[1]
            self.BOMBS = ilist[2]
            self.SEED = ilist[3]

            self.setup()

            # validate moves
            for m in moves:
                vm = self.validate_move(m.strip())
                if not vm:
                    return False    
                #self.MOVES.append(vm)
                self.do_move(vm[0], vm[1], vm[2])

            # if all the moves are valid, do them
            #self.do_all_moves()
            #for move in self.MOVES:
                #self.do_move(int(move[0]), int(move[1]), move[2])

            return True
        return False

    def save(self, filename=None):
        # set a filename, if missing
        if filename is None:
            filename = "{}.sweepy".format(str(self.SEED))

        with open(filename, "w") as fn:

            # write the header information
            fn.write("{}|{}|{}|{}\n".format(str(self.WIDTH), 
                                            str(self.HEIGHT), 
                                            str(self.BOMBS), 
                                            str(self.SEED)))

            # write the moves
            for move in self.MOVES:
                fn.write("{}\n".format(str(move)))

    def new_game(self, width=8, height=8, bombs=10):
        self.WIDTH = width
        self.HEIGHT = height
        self.BOMBS = bombs
        self.MOVES = []
        self.setup()
        self.do_first_move()

    # handle interactive highlighting
    def get_first_cell(self):
        for y, col in enumerate(self.OVER):
            for x, cell in enumerate(col):
                if cell == OVER_DEFAULT:
                    return y, x

    def get_covered_cells(self):
        out = []
        for y, col in enumerate(self.OVER):
            for x, cell in enumerate(col):
                if cell == OVER_DEFAULT:
                    out.append([y,x])
        return out

    def closest(self, y, x):
        covered_cells = self.get_covered_cells()
        for point in covered_cells:
            if point[0] == y and point[1] > x:
                return point[0], point[1]
            elif point[0] > y:
                return point[0], point[1]
        return covered_cells[0][0], covered_cells[0][1]
                

    def get_closest_cell(self, y, x):
        # set some defaults that will be overwritten
        min_off = self.WIDTH + self.HEIGHT
        ny = -1
        nx = -1

        # go through the directions
        ry, rx, ro = self.get_right(y, x)
        if 0 < ro < min_off:
            min_off = ro
            ny = ry
            nx = rx

        dy, dx, do = self.get_down(y, x)
        if 0 < do < min_off:
            min_off = do
            ny = dy
            nx = dx

        ly, lx, lo = self.get_left(y, x)
        if 0 < lo < min_off:
            min_off = lo
            ny = ly
            nx = lx

        uy, ux, uo = self.get_up(y, x)
        if 0 < uo < min_off:
            min_off = uo
            ny = uy
            nx = ux

        # if we found something, return it
        if min_off < self.WIDTH + self.HEIGHT:
            return ny, nx
        else:
            return self.get_first_cell()

    def get_left(self, y, x):
        col = self.OVER[y]
        for ix in range(1,x+1):
            adj_x = x - ix
            if col[adj_x] in (OVER_DEFAULT, OVER_FLAGGED):
                return y, adj_x, abs(adj_x - x)
        return y, x, 0

    def get_right(self, y, x):
        col = self.OVER[y]
        for ix in range(x+1,len(col)):
            if col[ix] in (OVER_DEFAULT, OVER_FLAGGED):
                return y, ix, abs(ix - x)
        return y, x, 0

    def get_up(self, y, x):
        row = [self.OVER[i][x] for i in range(len(self.OVER))]
        for iy in range(1,y+1):
            adj_y = y - iy
            if row[adj_y] in (OVER_DEFAULT, OVER_FLAGGED):
                return adj_y, x, abs(adj_y - y)
        return y, x, 0

    def get_down(self, y, x):
        row = [self.OVER[i][x] for i in range(len(self.OVER))]
        for iy in range(y+1, len(row)):
            if row[iy] in (OVER_DEFAULT, OVER_FLAGGED):
                return iy, x, abs(iy - y)
        return y, x, 0

    def do_first_move(self):
        for y, col in enumerate(self.UNDER):
            for x, cell in enumerate(self.UNDER[y]):
                if cell == UNDER_DEFAULT:
                    self.do_move(y, x, OVER_UNCOVERED)
                    return

    def validate_move(self, move):

        if type(move) is list:
            mlist = move
        else:
            mlist = move.split(DELIMITER)

        try:
            if not 0 <= int(mlist[0]) < self.WIDTH:
                return None
            mlist[0] = int(mlist[0])

            if not 0 <= int(mlist[1]) < self.HEIGHT:
                return None
            mlist[1] = int(mlist[1])

            if mlist[2] in OVER_MOVES:
                return mlist
        except ValueError as e:
            return None

    # returns true if move is successful/valid
    # returns false otherwise
    def do_move(self, col, row, move, propagated=False):

        # if the cell hasn't been uncovered, try to uncover it
        if self.OVER[col][row] == OVER_DEFAULT:
            if move == OVER_FLAGGED:
                if not propagated:
                    self.MOVES.append("{}|{}|{}".format(str(col), str(row), move))
                self.OVER[col][row] = move
            elif move == OVER_UNCOVERED:

                # uncover the targeted cell
                if not propagated:
                    self.MOVES.append("{}|{}|{}".format(str(col), str(row), move))
                self.OVER[col][row] = move

                # if the uncovered cell is the default,
                # uncover neighboring cells
                if self.UNDER[col][row] == UNDER_DEFAULT:
                    neighbors = self.get_valid_neighbors(col, row)
                    for n in neighbors:
                        n.extend(move) # add the move to the neighbor
                        vm = self.validate_move(n)
                        if vm and self.UNDER[vm[0]][vm[1]] != UNDER_BOMB:
                            self.do_move(vm[0], vm[1], vm[2], True)
        elif self.OVER[col][row] == OVER_FLAGGED and move == OVER_FLAGGED:
            if not propagated:
                self.MOVES.append("{}|{}|{}".format(str(col), str(row), move))
            self.OVER[col][row] = OVER_DEFAULT
        else:
            return False
            
    def setup(self):

        # grab a handle to the global variables 
        if self.SEED == 0:
            self.SEED = get_seed()

        # initialize with the width
        # use None objects, as these will be ultimately be lists
        self.UNDER = [None] * self.WIDTH
        self.OVER = [None] * self.WIDTH

        # add the height rows (use the defaults)
        for i in range(self.WIDTH):
            under_row = [UNDER_DEFAULT] * self.HEIGHT
            self.UNDER[i] = under_row

            over_row = [OVER_DEFAULT] * self.HEIGHT
            self.OVER[i] = over_row

        # generate and place the bombs
        random.seed(self.SEED)
        for i in range(self.BOMBS):
            while True:
                w = random.randint(0, self.WIDTH - 1)
                h = random.randint(0, self.HEIGHT - 1)
                if self.UNDER[w][h] == UNDER_DEFAULT:
                    self.UNDER[w][h] = UNDER_BOMB
                    break
    
        # calculate the values next to the bombs
        for w in range(self.WIDTH):
            for h in range(self.HEIGHT):
                if self.UNDER[w][h] == UNDER_BOMB:
                    neighbors = self.get_valid_neighbors(w, h)
                    for n in neighbors:
                        if self.UNDER[n[0]][n[1]] != UNDER_BOMB:
                            self.UNDER[n[0]][n[1]] += 1

    def get_valid_neighbors(self, col, row):

        # calculate the values
        col_left = col - 1
        col_right = col + 1
        row_up = row - 1
        row_down = row + 1

        # calculate which directions we can go
        left = True if col_left >= 0 else False
        right = True if col_right < self.WIDTH else False
        up = True if row_up >= 0 else False
        down = True if row_down < self.HEIGHT else False

        # valid neighbors
        vns = []
        if left and up:
            vns.append([col_left, row_up])
        if left:
            vns.append([col_left, row])
        if left and down:
            vns.append([col_left, row_down])
        if right and up:
            vns.append([col_right, row_up])
        if right:
            vns.append([col_right, row])
        if right and down:
            vns.append([col_right, row_down])
        if up:
            vns.append([col, row_up])
        if down:
            vns.append([col, row_down])

        return vns

    def has_won(self):
        # win condition: all non-bombs are uncovered
        for w in range(0,self.WIDTH):
            for h in range(0,self.HEIGHT):
                if self.UNDER[w][h] != UNDER_BOMB and self.OVER[w][h] != OVER_UNCOVERED:
                    return False
        return True

    def has_lost(self):
        # lose condition: at least one bomb is uncovered
        for w in range(0,self.WIDTH):
            for h in range(0,self.HEIGHT):
                if self.UNDER[w][h] == UNDER_BOMB and self.OVER[w][h] == OVER_UNCOVERED:
                    return True
        return False

    def get_board(self):
        # this will be what the user sees

        lost = self.has_lost()

        out = [] 
        for c in range(self.WIDTH):
            col = self.OVER[c]
            inner = []
            for r in range(self.HEIGHT):
                row = col[r]

                under_cell = self.UNDER[c][r]

                if row == OVER_UNCOVERED and under_cell >= 0:
                    inner.append(str(under_cell))
                elif row == OVER_UNCOVERED:
                    inner.append(BOARD_BOMB_UNCOVERED)
                elif row == OVER_FLAGGED:
                    if lost and under_cell == UNDER_BOMB:
                        inner.append(BOARD_BOMB_FLAGGED)
                    else:
                        inner.append(BOARD_FLAGGED)
                else:
                    if lost and under_cell == UNDER_BOMB:
                        inner.append(BOARD_BOMB_COVERED)
                    else:
                        inner.append(BOARD_COVERED)
            out.append(inner)
        return out

    def get_flag_count(self):
        total = 0
        for col in self.OVER:
            for cell in col:
                if cell == OVER_FLAGGED:
                    total += 1
        return total
