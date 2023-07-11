'''
# Rules Functional Chess Game [BETA] v0.1.0

_Based on ziii chess script for graphics._

## Commands:
- 'Arrows' to move the cursor
- 'OK' to select a piece or move
- 'Backspace' to unselect
- 'Plus' to hide available moves

## Known issues:
- do not work on the online emulator

## Upcoming updates:
- checkmate rules
- stalemate rules
- points counter
- string code to save game
- current player board switcher
- color themes
'''

from ion import *
from time import sleep
from kandinsky import fill_rect, draw_string

SCREEN = (320, 222)
X, Y = 0, 1
COLUMN, ROW = 1, 0
SQUARE = (27, 27)
COLORS = {
    'black': (0,0,0),
    'yellow': (220,170,80),
    'white': (255,255,255),
    'blue': (75,115,153),
    'red': (220,70,0),
    'grey':(50,50,50),
    'green': (0,255,0)
}

class Board():
    def __init__(self, code="1urnbqkbnr8p8e8e8e8e8PRNBQKBNR"):
        self.board = []
        self.turn = int
        self.move = [None, None]
        self.moves_history = []
        self.valid_moves = []
        self.enpassant_move = []
        self.enpassant_target = []
        self.current_player = str
        self.display_valid_moves = True
        self.load(code)
        self.cursor = [0, 0]

    def new_turn(self):
        board.valid_moves = []
        board.move = [None, None]
        board.current_player = 'Black' if board.current_player == 'White' else 'White'
        self.turn += 1
        self.display_textboard()

    def display(self):
        fill_rect(0, 0, SCREEN[X], SCREEN[Y], COLORS['grey'])
        for row in range(8):
            for column in range(8):
                self.display_square(row, column)
        self.display_targets()
        self.display_textboard()

    def display_textboard(self):
        draw_string("Turn "+str(self.turn), 27*8+15, 5, COLORS['white'], COLORS['grey'])
        draw_string(">> "+self.current_player, 27*8+15, 5+20, COLORS['white'], COLORS['grey'])
        #draw_string("Menu:", 27*8+15, 200-5-20, COLORS['white'], COLORS['grey'])
        #draw_string("Minus", 27*8+15, 200-5, COLORS['white'], COLORS['grey'])

    def display_square(self, row, column):
        if (row%2==0 and column%2==0) or (row%2==1 and column%2==1):
            color = 'white'
        else:
            color = 'blue'
        fill_rect(column*SQUARE[X]+5, row*SQUARE[Y]+3, SQUARE[X], SQUARE[Y],COLORS[color])
        piece = self.board[row][column]
        if piece != None:
            color = 'yellow' if piece.player == 'White' else 'black'
            for i in piece.drawing:
                fill_rect(column*SQUARE[X]+7+i[0], row*SQUARE[Y]+5+i[1], i[2], 1, COLORS[color])

    def display_targets(self):
        for square in self.valid_moves:
            if square != self.cursor and self.display_valid_moves:
                fill_rect(square[COLUMN]*SQUARE[X]+5, square[ROW]*SQUARE[Y]+3, 27, 2, COLORS['green'])
                fill_rect(square[COLUMN]*SQUARE[X]+5, (1+square[ROW])*SQUARE[Y]+1, 27, 2, COLORS['green'])
                fill_rect(square[COLUMN]*SQUARE[X]+5, square[ROW]*SQUARE[Y]+5, 2, 23, COLORS['green'])
                fill_rect((1+square[COLUMN])*SQUARE[X]+3, square[ROW]*SQUARE[Y]+5, 2, 23, COLORS['green'])
        fill_rect(self.cursor[COLUMN]*SQUARE[X]+5, self.cursor[ROW]*SQUARE[Y]+3, 27, 2, COLORS['red'])
        fill_rect(self.cursor[COLUMN]*SQUARE[X]+5, (1+self.cursor[ROW])*SQUARE[Y]+1, 27, 2, COLORS['red'])
        fill_rect(self.cursor[COLUMN]*SQUARE[X]+5, self.cursor[ROW]*SQUARE[Y]+5, 2, 23, COLORS['red'])
        fill_rect((1+self.cursor[COLUMN])*SQUARE[X]+3, self.cursor[ROW]*SQUARE[Y]+5, 2, 23, COLORS['red'])

    def remove_targets(self):
        for square in self.valid_moves:
            if square != self.move[1] and square != self.move[0]:
                self.display_square(square[ROW], square[COLUMN])
                self.display_square(square[ROW], square[COLUMN])

    def is_valid_position(self, end_row, end_column):
        if self.cursor[ROW] == +end_row and self.cursor[COLUMN] == +end_column:
            return False
        if not 0 <= +end_row < 8 or not 0 <= +end_column < 8:
            return False
        return True

    def get_valid_moves(self, piece=None):
        self.valid_moves = []
        if not piece: piece = self.board[self.move[0][ROW]][self.move[0][COLUMN]]
        for row in range(8):
            for column in range(8):
                if piece.has_valid_move(row, column):
                    self.valid_moves.append([row, column])

    def is_check(self):
        return False

    def can_uncheck(self):
        return False

    def is_checkmate(self):
        return False
        '''if self.is_check():
            if not self.can_uncheck():
                return True
        return False'''

    def is_stealmate(self):
        return False
        '''if not self.is_check():
            if not self.can_uncheck():
                return True
        return False
'''


    def get_input(self, timer=0.1):
        if keydown(KEY_RIGHT) and self.is_valid_position(self.cursor[ROW], self.cursor[COLUMN]+1):
            self.cursor[COLUMN] += 1
            self.display_square(self.cursor[ROW], self.cursor[COLUMN]-1)
        elif keydown(KEY_LEFT) and self.is_valid_position(self.cursor[ROW], self.cursor[COLUMN]-1):
            self.cursor[COLUMN] -= 1
            self.display_square(self.cursor[ROW], self.cursor[COLUMN]+1)
        elif keydown(KEY_DOWN) and self.is_valid_position(self.cursor[ROW]+1, self.cursor[COLUMN]):
            self.cursor[ROW] += 1
            self.display_square(self.cursor[ROW]-1, self.cursor[COLUMN])
        elif keydown(KEY_UP) and self.is_valid_position(self.cursor[ROW]-1, self.cursor[COLUMN]):
            self.cursor[ROW] -= 1
            self.display_square(self.cursor[ROW]+1, self.cursor[COLUMN])
        elif keydown(KEY_OK):
            target = self.board[self.cursor[ROW]][self.cursor[COLUMN]]
            if not self.move[0] and not self.move[1] and target != None:
                self.move[0] = [self.cursor[ROW], self.cursor[COLUMN]]
                self.get_valid_moves()
                print(self.move[0])
                if not self.valid_moves:
                    self.move = [None, None]
            elif self.move[0] and not self.move[1] and target != None:
                if not self.move[1] and target.player != self.current_player:
                    self.move[1] = [self.cursor[ROW], self.cursor[COLUMN]]
                    print(self.move[1])
            elif self.move[0] and not self.move[1] and target == None:
                if not self.move[1]:
                    self.move[1] = [self.cursor[ROW], self.cursor[COLUMN]]
                    print(self.move[1])
        elif keydown(KEY_BACKSPACE):
            self.remove_targets()
            self.valid_moves = []
            self.move = [None, None]
        elif keydown(KEY_PLUS):
            if self.display_valid_moves == True:
                self.display_valid_moves = False
                self.remove_targets()
            else:
                self.display_valid_moves = True
        self.display_targets()
        sleep(timer)

    def display_move(self):
        piece = self.board[self.move[0][ROW]][self.move[0][COLUMN]]
        target = self.board[self.move[1][ROW]][self.move[1][COLUMN]]
        if self.enpassant_move:
            if self.move[1] == self.enpassant_move[0]:
                self.board[self.enpassant_target[0][ROW]][self.enpassant_target[0][COLUMN]] = None
                self.display_square(self.enpassant_target[0][ROW], self.enpassant_target[0][COLUMN])
        if target:
            target_piece, target_player = target.piece, target.player
        else:
            target_piece, target_player = None, None
        self.moves_history.append({'start_player':piece.player, 'start_piece':piece.piece, 'start_position':self.move[0],
                                   'end_player':target_player, 'end_piece':target_piece, 'end_position':self.move[1],})
        self.board[self.move[1][ROW]][self.move[1][COLUMN]] = self.board[self.move[0][ROW]][self.move[0][COLUMN]]
        self.board[self.move[0][ROW]][self.move[0][COLUMN]] = None
        self.remove_targets()
        self.valid_moves = []
        self.display_square(self.move[0][ROW], self.move[0][COLUMN])
        self.display_square(self.move[1][ROW], self.move[1][COLUMN])
        self.display_targets()

    def load_piece(self, char):
        player = 'Black' if char.islower() else 'White'
        char = char.lower()
        if char == 'p':
            piece = Pawn(player)
        elif char == 'n':
            piece = Knight(player)
        elif char == 'b':
            piece = Bishop(player)
        elif char == 'r':
            piece = Rook(player)
        elif char == 'q':
            piece = Queen(player)
        elif char == 'k':
            piece = King(player)
        else:
            return None
        return piece

    def load(self, code):
        code = code.replace('u', ' ').split()
        self.turn = int(code[0])
        self.current_player = 'White' if self.turn % 2 == 1 else 'Black'
        code = code[1]
        self.board = []
        row = []
        for char in range(0, len(code)):
            if code[char].isdigit():
                for _ in range(1, int(code[char])):
                    row.append(self.load_piece(code[char+1]))
            else:
                row.append(self.load_piece(code[char]))
            if len(row) == 8:
                self.board.append(row)
                row = []

    def save(self):
        code = str(self.turn)+'u'
        raw_code = []
        for row in self.board:
            for piece in row:
                if piece != None:
                    raw_code.append(piece.code)
                else:
                    raw_code.append('e')
        count = 1
        row_count = 1
        for i in range(len(raw_code)-1):
            if raw_code[i] == raw_code[i+1] and count < 8 and row_count%8 != 0:
                count += 1
                row_count += 1
            else:
                if count > 1:
                    code += str(count)
                code += raw_code[i]
                row_count += 1
                count = 1
        if count > 1:
            code += str(count)
        code += raw_code[-1]
        print("Match ID:", code)

class Piece():
    def __init__(self, piece, player):
        self.piece = piece
        self.player = player
        self.code = ''

    def is_valid_piece(self, end_row, end_column):
        global board
        enemy = board.board[end_row][end_column]
        piece = board.board[board.move[0][ROW]][board.move[0][COLUMN]]
        if piece and piece.player != board.current_player:
            return True
        if piece and enemy != None:
            if piece.player == 'White':
                return enemy.player == 'White'
            elif piece.player == 'Black':
                return enemy.player == 'Black'
        else:
            return False

class Pawn(Piece):
    def __init__(self, player):
        super().__init__(piece='Pawn', player=player)
        self.drawing = ((10,6,3),(9,7,5),(9,8,5),(9,9,5),(10,10,3),(10,13,3),(9,14,5),(8,15,7),(8,16,7),(8,17,7),(7,18,9),(5,19,13),(4,20,15),(4,21,15),(4,22,15))
        self.code = 'P' if self.player == 'White' else 'p'

    def has_valid_move(self, end_row, end_column):
        global board

        if not board.is_valid_position(end_row, end_column):
            return False

        if self.is_valid_piece(end_row, end_column):
            return False

        start_row = board.move[0][ROW]
        start_column = board.move[0][COLUMN]

        if self.is_enpassant(end_row, end_column):
            return True

        row_difference = end_row - start_row
        column_difference = end_column - start_column

        if board.current_player == 'White':
            if row_difference == -1 and column_difference == 0 and board.board[end_row][end_column] == None:
                return True
            elif start_row == 6 and row_difference == -2 and column_difference == 0 and board.board[5][end_column] == None and board.board[4][end_column] == None:
                return True
            elif row_difference == -1 and abs(column_difference) == 1 and board.board[end_row][end_column] != None and board.board[end_row][end_column].player == 'Black':
                return True
        elif board.current_player == 'Black':
            if row_difference == 1 and column_difference == 0 and board.board[end_row][end_column] == None:
                return True
            elif start_row == 1 and row_difference == 2 and column_difference == 0 and board.board[2][end_column] == None and board.board[3][end_column] == None:
                return True
            elif row_difference == 1 and abs(column_difference) == 1 and board.board[end_row][end_column] != None and board.board[end_row][end_column].player == 'White':
                return True
        return False

    def is_enpassant(self, end_row, end_column):
        global board
        if board.moves_history:
            target = board.moves_history[-1]
            if target['start_piece'] == 'Pawn':
                if abs(target['start_position'][ROW]-target['end_position'][ROW]) == 2:
                    if target['start_player'] == 'White':
                        if end_row == target['end_position'][ROW]+1 and abs(end_row-board.move[0][ROW]) == 1:
                            if end_column == target['end_position'][COLUMN]:
                                board.enpassant_move.append([end_row, end_column])
                                board.enpassant_target.append([target['end_position'][ROW], target['end_position'][COLUMN]])
                                return True
                    elif target['start_player'] == 'Black':
                        if end_row == target['end_position'][ROW]-1 and abs(end_row-board.move[0][ROW]) == 1:
                            if end_column == target['end_position'][COLUMN]:
                                board.enpassant_move.append([end_row, end_column])
                                board.enpassant_target.append(board.moves_history[-1]['end_position'])
                                return True
        return False

class Knight(Piece):
    def __init__(self, player):
        super().__init__(piece='Knight', player=player)
        self.drawing = ((8,0,2),(8,1,3),(7,2,7),(6,3,10),(6,4,11),(5,5,13),(5,6,14),(4,7,15),(4,8,16),(3,9,18),(2,10,9),(12,10,9),(2,11,7),(11,11,10),(2,12,5),(11,12,10),(3,13,3),(10,13,11),(9,14,12),(8,15,13),(7,16,14),(7,17,13),(7,18,13),(6,19,15),(5,20,16),(5,21,16),(5,22,16))
        self.code = 'N' if self.player == 'White' else 'n'

    def has_valid_move(self, end_row, end_column):
        global board

        if not board.is_valid_position(end_row, end_column):
            return False

        if self.is_valid_piece(end_row, end_column):
            return False

        start_row = board.move[0][ROW]
        start_column = board.move[0][COLUMN]

        row_difference = abs(end_row - start_row)
        column_difference = abs(end_column - start_column)

        if (row_difference == 2 and column_difference == 1) or (row_difference == 1 and column_difference == 2):
            return True

        return False

class Bishop(Piece):
    def __init__(self, player):
        super().__init__(piece='Bishop', player=player)
        self.drawing = ((10,0,3),(9,1,5),(9,2,5),(10,3,3),(9,4,3),(14,4,1),(8,5,4),(13,5,3),(7,6,4),(13,6,4),(6,7,5),(13,7,4),(6,8,5),(12,8,6),(5,9,6),(12,9,6),(5,10,13),(5,11,12),(6,12,11),(6,13,11),(7,14,9),(8,16,8),(7,17,10),(0,18,23),(0,19,23),(0,20,11),(12,20,11),(1,21,9),(13,21,10),(1,22,8),(14,22,8))
        self.code = 'B' if self.player == 'White' else 'b'

    def has_valid_move(self, end_row, end_column):
        global board

        if not board.is_valid_position(end_row, end_column):
            return False

        if self.is_valid_piece(end_row, end_column):
            return False

        start_row = board.move[0][ROW]
        start_column = board.move[0][COLUMN]

        row_difference = end_row - start_row
        column_difference = end_column - start_column

        if abs(row_difference) == abs(column_difference):
            row_step = 1 if row_difference > 0 else -1
            col_step = 1 if column_difference > 0 else -1
            row = start_row + row_step
            column = start_column + col_step
            while row != end_row and column != end_column:
                if board.board[row][column] != None:
                    return False
                row += row_step
                column += col_step

            return True

        return False

class Rook(Piece):
    def __init__(self, player):
        super().__init__(piece='Rook', player=player)
        self.drawing = ((9,0,5),(3,1,4),(9,1,5),(16,1,4),(3,2,4),(9,2,5),(16,2,4),(3,3,5),(9,3,5),(15,3,5),(3,4,17),(3,5,17),(4,6,15),(4,7,15),(5,8,13),(5,9,13),(5,10,13),(5,11,13),(5,12,13),(5,13,13),(4,14,15),(4,15,15),(4,16,15),(4,17,15),(3,18,17),(2,19,19),(2,20,19),(2,21,19),(2,22,19))
        self.code = 'R' if self.player == 'White' else 'r'


    def has_valid_move(self, end_row, end_column):
        global board

        if not board.is_valid_position(end_row, end_column):
            return False

        if self.is_valid_piece(end_row, end_column):
            return False

        start_row = board.move[0][ROW]
        start_column = board.move[0][COLUMN]

        row_difference = end_row - start_row
        column_difference = end_column - start_column

        if row_difference == 0 or column_difference == 0:
            if row_difference == 0:
                step = 1 if column_difference > 0 else -1
                for column in range(start_column + step, end_column, step):
                    if board.board[start_row][column] != None:
                        return False
                return True
            elif column_difference == 0:
                step = 1 if row_difference > 0 else -1
                for row in range(start_row + step, end_row, step):
                    if board.board[row][start_column] != None:
                        return False
                return True
        return False

class Queen(Piece):
    def __init__(self, player):
        super().__init__(piece='Queen', player=player)
        self.drawing = ((10,0,3),(9,1,5),(9,2,5),(1,3,3),(9,3,5),(19,3,3),(0,4,5),(10,4,3),(18,4,5),(0,5,5),(11,5,1),(18,5,5),(0,6,5),(11,6,1),(18,6,5),(1,7,3),(10,7,3),(19,7,3),(3,8,2),(10,8,3),(18,8,2),(4,9,2),(10,9,3),(17,9,2),(4,10,4),(10,10,3),(15,10,4),(5,11,13),(5,12,13),(5,13,13),(6,14,11),(6,15,11),(7,16,9),(7,17,9),(7,18,9),(6,19,11),(3,20,17),(2,21,19),(2,22,19))
        self.code = 'Q' if self.player == 'White' else 'q'
    def has_valid_move(self, end_row, end_column):
        global board

        if not board.is_valid_position(end_row, end_column):
            return False

        if self.is_valid_piece(end_row, end_column):
            return False

        start_row = board.move[0][ROW]
        start_column = board.move[0][COLUMN]

        row_difference = end_row - start_row
        column_difference = end_column - start_column

        if row_difference == 0 or column_difference == 0 or abs(row_difference) == abs(column_difference):
            if row_difference == 0:
                step = 1 if column_difference > 0 else -1
                for column in range(start_column + step, end_column, step):
                    if board.board[start_row][column] != None:
                        return False
            elif column_difference == 0:
                step = 1 if row_difference > 0 else -1
                for row in range(start_row + step, end_row, step):
                    if board.board[row][start_column] != None:
                        return False
            else:
                row_step = 1 if row_difference > 0 else -1
                col_step = 1 if column_difference > 0 else -1
                row = start_row + row_step
                column = start_column + col_step
                while row != end_row and column != end_column:
                    if board.board[row][column] != None:
                        return False
                    row += row_step
                    column += col_step
            return True
        return False

class King(Piece):
    def __init__(self, player):
        super().__init__(piece='King', player=player)
        self.drawing = ((10,0,3),(9,1,5),(9,2,5),(10,3,3),(11,4,1),(3,5,5),(11,5,1),(15,5,5),(2,6,7),(10,6,3),(14,6,7),(1,7,21),(0,8,23),(0,9,23),(0,10,5),(7,10,9),(18,10,5),(0,11,5),(8,11,7),(18,11,5),(0,12,6),(8,12,7),(17,12,6),(1,13,6),(8,13,7),(16,13,6),(2,14,19),(3,15,17),(4,16,15),(5,17,13),(5,18,13),(4,19,15),(3,20,17),(2,21,19),(2,22,19))
        self.code = 'K' if self.player == 'White' else 'k'

    def has_valid_move(self, end_row, end_column):
        global board

        if not board.is_valid_position(end_row, end_column):
            return False

        if self.is_valid_piece(end_row, end_column):
            return False

        start_row = board.move[0][ROW]
        start_column = board.move[0][COLUMN]

        row_difference = abs(end_row - start_row)
        column_difference = abs(end_column - start_column)

        if row_difference <= 1 and column_difference <= 1:
            return True
        return False

def play():
    global board
    board = Board()
    board.display()

    while True:
        while not board.move[0] or not board.move[1]:
            board.get_input()

        if board.move[0] and board.move[1]:
            if board.move[1] in board.valid_moves:
                board.display_move()

                if board.is_checkmate():
                    break
                elif board.is_stealmate():
                    break
                else:
                    board.new_turn()
                    board.save()

play()