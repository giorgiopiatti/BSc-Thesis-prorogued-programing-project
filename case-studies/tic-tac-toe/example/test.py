import unittest
from tic_tac_toe import TicTacToeGame


class TestTicTacToe(unittest.TestCase):

    def test_put_marker(self):
        game = TicTacToeGame()
        board = list('123456789')

        self.assertEqual(game.put_marker(board, 2, 'X'),  list('1X3456789'))
        self.assertEqual(game.put_marker(board, 2, 'O'),  list('1O3456789'))

    def test_is_cell_free(self):
        game = TicTacToeGame()

        self.assertTrue(game.is_cell_free(list('123456789'), 1))
        self.assertFalse(game.is_cell_free(list('X23456789'), 1))

    def test_get_player_marker(self):

        game = TicTacToeGame()
        self.assertEqual(game.get_player_marker(1), 'X')
        self.assertEqual(game.get_player_marker(0), 'O')

    def test_check_win(self):
        game = TicTacToeGame()
        self.assertEqual(game.check_win(list('XXX456789')), 'X')
        self.assertEqual(game.check_win(list('OOO456789')), 'O')
        self.assertIsNone(game.check_win(list('XOX456789')))
        self.assertIsNone(game.check_win(list('OXO456789')))

    def test_board_is_full(self):
        game = TicTacToeGame()
        self.assertTrue(game.board_is_full(list('XXOXXOOXX')))
        self.assertFalse(game.board_is_full(list('OOO456789')))


if __name__ == '__main__':
    unittest.main()
