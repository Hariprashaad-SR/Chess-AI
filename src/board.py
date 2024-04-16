from const import *
from square import Square
from piece import *
from move import Move

class Board:
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]    # creating the board representing [ is_piece_there() -> bool ]
        self._create()
        self.last_move = None

        self._add_pieces('white')
        self._add_pieces('black')

    
    def calc_moves(self, piece, row, col):

        def straight_line_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:

                    # empty
                    if Square.in_range(possible_move_row, possible_move_col):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)

                        if self.squares[possible_move_row][possible_move_col].is_empty(): 
                            piece.add_move(move)
                    
                    # has_enemy_piece
                        elif self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                            piece.add_move(move)
                            break

                    # has_team_piece
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    
                    else : break

                    possible_move_row += row_incr
                    possible_move_col += col_incr
                        
        def pawn_moves():
            # straight
            steps = 1 if piece.moved else 2

            start = row + piece.dir
            end = row + (piece.dir * (1+steps))

            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].is_empty():
                        initial = Square(row, col)
                        final = Square(move_row, col)
                        move = Move(initial, final)
                        piece.add_move(move)
                    else:
                        break  #blocked
                else:
                    break   # out of range

            # diagonal
            possible_move_row = row + piece.dir
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        piece.add_move(move)

        def knight_moves():
            possible_moves = [
                    (row - 2, col + 1),
                    (row - 1, col + 2),
                    (row + 1, col + 2),
                    (row + 2, col + 1),
                    (row + 2, col - 1),
                    (row + 1, col - 2),
                    (row - 1, col - 2),
                    (row - 2, col - 1)
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        piece.add_move(move)

        def king_moves():
            # normal moves
            possible_moves = [
                    (row , col + 1),
                    (row, col - 1),
                    (row + 1, col + 1),
                    (row + 1, col - 1),
                    (row + 1, col),
                    (row - 1, col + 1),
                    (row - 1, col - 1),
                    (row - 1, col)
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        piece.add_move(move)

            # castling moves


        if piece.name == 'pawn': 
            pawn_moves()
        
        elif isinstance(piece, Knight): knight_moves()

        elif isinstance(piece, Bishop):
            straight_line_moves([
                (-1,1),     #up-right
                (-1,-1),    # up-left
                (1,1),      # down-right
                (1, -1)     # down- left
            ])

        elif isinstance(piece, Rook): 
            straight_line_moves([
                (-1, 0),    # up
                (1, 0),     # down
                (0, 1),     # right
                (0, -1)     # left
            ])

        elif isinstance(piece, Queen):
            straight_line_moves(
                [(-1,1),     #up-right
                (-1,-1),    # up-left
                (1,1),      # down-right
                (1, -1),    # down- left
                (-1, 0),    # up
                (1, 0),     # down
                (0, 1),     # right
                (0, -1) ]    # left
            )
        
        elif isinstance(piece, King): king_moves()

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        piece.moved = True
        piece.clear_moves()

        self.last_move = move


    def valid_move(self, piece, move):
        return move in piece.moves


    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)  # standard piece placements
        
        #pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
        self.squares[5][3] = Square(5, 3, King(color))
        #knights
        self.squares[row_other][6] = Square(row_pawn, 1, Knight(color))
        self.squares[row_other][1] = Square(row_pawn, 6, Knight(color))

        #bishops
        self.squares[row_other][5] = Square(row_pawn, 5, Bishop(color))
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))

        #rooks
        self.squares[row_other][0] = Square(row_pawn, 0, Rook(color))
        self.squares[row_other][7] = Square(row_pawn, 7, Rook(color))

        #queen
        self.squares[row_other][3] = Square(row_pawn, 3, Queen(color))

        #king
        self.squares[row_other][4] = Square(row_pawn, 4, King(color))

