from copy import deepcopy
import pieces
from pieces import Colours

START_PATTERN = (pieces.Rook, pieces.Knight, pieces.Bishop, pieces.Queen,
                 pieces.King, pieces.Bishop, pieces.Knight, pieces.Rook)


class Board(dict):
    x_axis = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
    y_axis = (1, 2, 3, 4, 5, 6, 7, 8)
    player_turn = None

    def __init__(self):
        for x, p in list(zip(self.x_axis, START_PATTERN)):
            self[x+'8'] = p(Colours.BLACK, self, x+'8')
            self[x+'1'] = p(Colours.WHITE, self, x+'1')

        for x in self.x_axis:
            self[x+'7'] = pieces.Pawn(Colours.BLACK, self,  x+'7')
            self[x+'2'] = pieces.Pawn(Colours.WHITE, self, x+'2')

        self.player_turn = Colours.WHITE

    def shift(self, p1, p2):
        piece = self[p1]
        if self.player_turn != piece.color:
            raise NotYourTurn("Not " + piece.color + "'s turn!")
        enemy = (Colours.WHITE if piece.color ==
                 Colours.BLACK else Colours.BLACK)
        moves_available = piece.allowed_moves()
        if p2 not in moves_available:
            raise InvalidMove
        if self.allowed_moves(enemy) and self.is_in_check_after_move(p1, p2):
            raise Check
        if not moves_available and self.king_in_check(piece.color):
            raise CheckMate
        elif not moves_available:
            raise Draw
        else:
            self.update_piece_position(p1, p2)

    def update_piece_position(self, p1, p2):
        piece = self[p1]
        dest = self.get(p2)
        if dest is not None:
            del dest
        del self[p1]
        self[p2] = piece
        self[p2].update_coordinates(p2)

        self.player_turn = (Colours.WHITE if piece.color ==
                            Colours.BLACK else Colours.BLACK)

    def position_of_king(self, color):
        for pos in self.keys():
            if isinstance(self[pos], pieces.King) and self[pos].color == color:
                return pos

    def is_in_check_after_move(self, p1, p2):  # SKELETON remove
        tmp = deepcopy(self)
        tmp.update_piece_position(p1, p2)
        return tmp.king_in_check(self[p1].color)

    def allowed_moves(self, color):  # SKELETON remove
        result = []
        for coord in self.keys():
            if (self[coord] is not None) and self[coord].color == color:
                moves = self[coord].allowed_moves()
                if moves:
                    result += moves
        return result

    def occupied(self, color):  # SKELETON remove
        result = []
        for coord in self.keys():
            if self[coord].color == color:
                result.append(coord)
        return result

    def king_in_check(self, color):  # SKELETON remove
        kingpos = self.position_of_king(color)
        opponent = (Colours.BLACK if color == Colours.WHITE else Colours.WHITE)
        moves_opponent = self.allowed_moves(opponent)
        if kingpos in moves_opponent:
            return True
        else:
            return False


class ChessError(Exception):
    pass


class Check(ChessError):
    pass


class InvalidMove(ChessError):
    pass


class CheckMate(ChessError):
    pass


class Draw(ChessError):
    pass


class NotYourTurn(ChessError):
    pass


class InvalidCoord(ChessError):
    pass
