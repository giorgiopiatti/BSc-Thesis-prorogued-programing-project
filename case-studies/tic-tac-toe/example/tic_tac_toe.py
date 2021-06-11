from ppl import PPLEnableProroguedCallsStatic


class TicTacToeGame(metaclass=PPLEnableProroguedCallsStatic):

    # Skeleton: to be prorogued
    def put_marker(self, board: 'board', cell: int, marker: 'O|X') -> 'board':
        board[cell - 1] = marker
        return board

    def is_cell_free(self, board: 'board', cell: int) -> bool:  # Skeleton: to be prorogued
        return board[cell - 1] not in 'XO'

    def get_player_marker(self, player_id: '1|0') -> 'X|0':  # Skeleton: to be prorogued
        if player_id == 1:
            return 'X'
        elif player_id == 0:
            return 'O'

    def check_win(self, board: 'board') -> 'X|O|None':  # Skeleton: to be prorogued
        wins = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                (0, 4, 8), (2, 4, 6))

        for win in wins:
            m = board[win[0]]
            if m in 'XO' and all(board[i] == m for i in win):
                return m
        return None

    def board_is_full(self, board):  # Skeleton: to be prorogued
        return all(b in 'XO' for b in board)

    # Skeleton: already implemented

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
