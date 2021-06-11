from ppl import PPLEnableProroguedCallsStatic


class TicTacToeGame(metaclass=PPLEnableProroguedCallsStatic):

    def print_board(self, board: 'board'):
        print('\n'.join(' '.join(board[x:x+3]) for x in (0, 3, 6)))

    def turn(self, board, xo) -> 'board':
        while True:
            choice = int(input(f'Put {xo} in a cell: '))

            if choice in range(1, 10) and self.is_cell_free(board, choice):
                break
            print("Wrong input!")
        return self.put_marker(board, choice, xo)

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
