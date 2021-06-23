class TicTacToeGame():

    def put_marker(self, board: 'board', cell: int, marker: 'O|X') -> 'board': # TODO
        return board

    def is_cell_free(self, board: 'board', cell: int) -> bool:  # TODO
        return True

    def get_player_marker(self, player_id: '1|0') -> 'X|0':  # TODO
        return 'X'
       

    def check_win(self, board: 'board') -> 'X|O|None':  # TODO
        return 'X'

    def board_is_full(self, board):  # TODO
        return False

    def turn(self, board, xo) -> 'board': # TODO
        return None

    def print_board(self, board: 'board'):
        print('\n'.join(' '.join(board[x:x+3]) for x in (0, 3, 6)))

    def play(self):
        board = list('123456789')
        player_id = 0
        while not self.board_is_full(board):
            self.print_board(board)
            xo = self.get_player_marker(player_id)
            board = self.turn(board, xo)

            win = self.check_win(board)
            if win is not None:
                print(f'Win with marker {win}')
                break
            else:
                player_id = (player_id + 1) % 2

if __name__ == '__main__':
    t = TicTacToeGame()
    t.play()
