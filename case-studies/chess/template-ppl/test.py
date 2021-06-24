import unittest
import pieces
from pieces import Colours
from chessboard import Board, Check, CheckMate


class TestChess(unittest.TestCase):

    def test_game_status_check_mate(self):

        board = Board()
        board.clear()
        board.player_turn = Colours.BLACK

        board['G8'] = pieces.Knight(Colours.BLACK, board, 'G8')
        board['H8'] = pieces.Rook(Colours.BLACK, board, 'H8')
        board['H7'] = pieces.King(Colours.BLACK, board, 'H7')
        board['F7'] = pieces.Pawn(Colours.BLACK, board, 'F7')
        board['G5'] = pieces.Pawn(Colours.BLACK, board, 'G5')
        board['H5'] = pieces.Pawn(Colours.BLACK, board, 'H5')

        board['D7'] = pieces.Bishop(Colours.WHITE, board, 'D7')
        board['C3'] = pieces.Bishop(Colours.WHITE, board, 'C3')
        board['E6'] = pieces.Rook(Colours.WHITE, board, 'E6')
        board['F5'] = pieces.Queen(Colours.WHITE, board, 'F5')

        board['A1'] = pieces.King(Colours.WHITE, board, 'A1')

        with self.assertRaises(CheckMate):
            board.game_status(Colours.BLACK)

        board.pop('C3')
        board.game_status(Colours.BLACK)  # Do not raise error

    def test_is_in_check_after_move(self):
        board = Board()
        board.clear()
        board.player_turn = Colours.BLACK

        board['H7'] = pieces.King(Colours.BLACK, board, 'H7')
        board['G6'] = pieces.Pawn(Colours.BLACK, board, 'G6')
        board['F5'] = pieces.Queen(Colours.WHITE, board, 'F5')

        self.assertTrue(board.is_in_check_after_move('G6', 'G5'))

        self.assertFalse(board.is_in_check_after_move('H7', 'H8'))

    def test_reachable_positions_pawn(self):
        board = Board()
        board.clear()
        piece = pieces.Pawn(Colours.BLACK, board, 'C7')
        board['C7'] = piece
        self.assertListEqual(
            sorted(piece.reachable_positions()), sorted(['C6', 'C5']))

        piece = pieces.Pawn(Colours.BLACK, board, 'C6')
        board['C6'] = piece
        self.assertListEqual(piece.reachable_positions(), ['C5'])

    def test_reachable_positions_rook(self):
        board = Board()
        board.clear()
        piece = pieces.Rook(Colours.BLACK, board, 'C7')
        board['C7'] = piece
        self.assertListEqual(sorted(piece.reachable_positions()), sorted([
                             'C8', 'C6', 'C5', 'C4', 'C3', 'C2', 'C1', 'A7', 'B7', 'D7', 'E7', 'F7', 'G7', 'H7']))

    def test_reachable_positions_bishop(self):
        board = Board()
        board.clear()
        piece = pieces.Bishop(Colours.BLACK, board, 'C7')
        board['C7'] = piece
        self.assertListEqual(sorted(piece.reachable_positions()), sorted(
            ['B8', 'D6', 'E5', 'F4', 'G3', 'H2', 'B6', 'A5', 'D8']))

    def test_reachable_positions_knight(self):
        board = Board()
        board.clear()
        piece = pieces.Knight(Colours.BLACK, board, 'C7')
        board['C7'] = piece
        self.assertListEqual(sorted(piece.reachable_positions()), sorted(
            ['A8', 'A6', 'B5', 'D5', 'E6', 'E8']))

    def test_reachable_positions_queen(self):
        board = Board()
        board.clear()
        piece = pieces.Queen(Colours.BLACK, board, 'C7')
        board['C7'] = piece
        self.assertListEqual(sorted(piece.reachable_positions()), sorted(
            ['A5', 'A7', 'B6', 'B7', 'B8', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C8', 'D6', 'D7', 'D8', 'E5', 'E7', 'F4', 'F7', 'G3', 'G7', 'H2', 'H7']))

    def test_reachable_positions_king(self):
        board = Board()
        board.clear()
        piece = pieces.King(Colours.BLACK, board, 'C7')
        board['C7'] = piece
        self.assertListEqual(sorted(piece.reachable_positions()), sorted(
            ['C8', 'C6', 'B7', 'D7', 'B8', 'D8', 'D6', 'B6']))


if __name__ == '__main__':
    unittest.main()
