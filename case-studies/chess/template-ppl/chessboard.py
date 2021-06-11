from copy import deepcopy
import pieces
from pieces import Colours
from ppl import PPLEnableProroguedCallsInstance

START_PATTERN = (pieces.Rook, pieces.Knight, pieces.Bishop, pieces.Queen,
                 pieces.King, pieces.Bishop, pieces.Knight, pieces.Rook)


class Board(dict, metaclass=PPLEnableProroguedCallsInstance):
    x_axis = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
    y_axis = (1, 2, 3, 4, 5, 6, 7, 8)
    player_turn = None

    def __init__(self):
        """
        Initialize the board with pieces at start position.
        First turn is always white.
        """
        for x, piece in list(zip(self.x_axis, START_PATTERN)):
            self[x+'8'] = piece(Colours.BLACK, self, x+'8')
            self[x+'1'] = piece(Colours.WHITE, self, x+'1')

        for x in self.x_axis:  # Initialize paws
            self[x+'7'] = pieces.Pawn(Colours.BLACK, self,  x+'7')
            self[x+'2'] = pieces.Pawn(Colours.WHITE, self, x+'2')

        self.player_turn = Colours.WHITE

    def shift(self, pos_src, pos_dst):
        """ 
        Shift one piece in pos_src to pos_dst if move is allowed according to chess rules.
        We check that:
        - current turn correspond to the piece's color
        - pos_dst is reachable_positions by performing a valid move
        - performing the move does not result in check 
        """
        piece_src = self[pos_src]
        if self.player_turn != piece_src.color:
            raise NotYourTurn("Not " + piece_src.color + "'s turn!")
        color_opponent = (Colours.WHITE if piece_src.color ==
                          Colours.BLACK else Colours.BLACK)
        moves_available = piece_src.reachable_positions()
        if pos_dst not in moves_available:
            raise InvalidMove
        if self.reachable_positions(color_opponent) and self.is_in_check_after_move(pos_src, pos_dst):
            raise Check
        else:
            self.update_piece_position(pos_src, pos_dst)
            self.player_turn = (Colours.WHITE if piece_src.color ==
                                Colours.BLACK else Colours.BLACK)

    def game_status(self, color):
        """
        Check if color is in checkmate or cannot do any move
        """
        moves_available = self.reachable_positions_do_not_check(color)
        if not moves_available and self.king_in_check(color):
            raise CheckMate
        elif not moves_available:
            raise Draw

    def update_piece_position(self, pos_src, pos_dst):
        """
        Give src position move the pieces to dst position, eating destination position if needed.
        """
        piece_src = self[pos_src]
        piece_dest = self.get(pos_dst)
        if piece_dest is not None:
            del piece_dest
        del self[pos_src]
        self[pos_dst] = piece_src
        self[pos_dst].update_coordinates(pos_dst)

    def position_of_king(self, color):
        """ 
        Return coordinate of king's position
        """
        for pos in self.keys():
            if isinstance(self[pos], pieces.King) and self[pos].color == color:
                return pos


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
