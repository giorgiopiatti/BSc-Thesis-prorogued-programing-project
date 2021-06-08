from enum import Enum
import sys


class Coordinate():
    x_axis = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
    y_axis = (1, 2, 3, 4, 5, 6, 7, 8)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_alpha(self):
        if not self.is_on_board():
            return None
        return self.x_axis[self.x] + str(self.y_axis[self.y])

    def get_num_coordinates(self):
        if not self.is_on_board():
            return None
        return self.x, self.y

    def __add__(self, coord):
        x, y = coord
        return Coordinate(self.x + x, self.y + y)

    def __mul__(self, a):
        return Coordinate(self.x * a, self.y * a)

    def is_on_board(self):
        x = self.x
        y = self.y
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        else:
            return True

    @staticmethod
    def init_from_alpha(a):
        return Coordinate(Coordinate.x_axis.index(a[0]), int(a[1])-1)


class Piece(object):
    coordinate = None

    def __init__(self, color, board, alpha_coordinates, short_name):
        self.color = color
        self.board = board
        self.coordinate = Coordinate.init_from_alpha(alpha_coordinates)
        self.short_name = short_name

    def get_image_name(self):
        return self.short_name + self.color + '.png'

    def update_coordinates(self, coord):
        self.coordinate = Coordinate.init_from_alpha(coord)

    # SKELETON remove
    def allowed_moves_base(self, allow_orthogonal, allow_diagonal, max_allowed_distance):

        allowed_moves = []
        orth = ((-1, 0), (0, -1), (0, 1), (1, 0))
        diag = ((-1, -1), (-1, 1), (1, -1), (1, 1))

        start_position = self.coordinate

        if allow_orthogonal and allow_diagonal:
            directions = diag + orth
        elif allow_diagonal:
            directions = diag
        elif allow_orthogonal:
            directions = orth

        for x, y in directions:
            collision = False
            for step in range(1, max_allowed_distance + 1):
                if collision:
                    break
                dest = start_position + (step*x, step*y)
                if dest.get_alpha() not in self.board.occupied(
                        'white') + self.board.occupied('black'):
                    allowed_moves.append(dest)
                elif dest.get_alpha() in self.board.occupied(
                        self.color):  # Same color
                    collision = True
                else:  # Can eat a piece
                    allowed_moves.append(dest)
                    collision = True
        allowed_moves = filter(lambda x: x.is_on_board(), allowed_moves)
        allowed_moves = list(map(lambda x: x.get_alpha(), allowed_moves))
        return allowed_moves


class King(Piece):

    def __init__(self, color, board, num_coordinates):
        super().__init__(color, board, num_coordinates, 'k')

    def allowed_moves(self):  # SKELETON remove
        return super(King, self).allowed_moves_base(allow_orthogonal=True, allow_diagonal=True, max_allowed_distance=1)


class Queen(Piece):
    def __init__(self, color, board, num_coordinates):
        super().__init__(color, board, num_coordinates, 'q')

    def allowed_moves(self):  # SKELETON remove
        return super(Queen, self).allowed_moves_base(allow_orthogonal=True, allow_diagonal=True, max_allowed_distance=8)


class Rook(Piece):
    def __init__(self, color, board, num_coordinates):
        super().__init__(color, board, num_coordinates, 'r')

    def allowed_moves(self):  # SKELETON remove
        return super(Rook, self).allowed_moves_base(allow_orthogonal=True, allow_diagonal=False, max_allowed_distance=8)


class Bishop(Piece):
    def __init__(self, color, board, num_coordinates):
        super().__init__(color, board, num_coordinates, 'b')

    def allowed_moves(self):  # SKELETON remove
        return super(Bishop, self).allowed_moves_base(allow_orthogonal=False, allow_diagonal=True, max_allowed_distance=8)


class Knight(Piece):
    def __init__(self, color, board, num_coordinates):
        super().__init__(color, board, num_coordinates, 'n')

    def allowed_moves(self):
        allowed_moves = []
        start_position = self.coordinate

        deltas = (
            (-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for x, y in deltas:
            dest = start_position + (x, y)
            if dest.get_alpha() not in self.board.occupied(self.color):
                allowed_moves.append(dest)
        allowed_moves = filter(lambda x: x.is_on_board(), allowed_moves)
        allowed_moves = list(map(lambda x: x.get_alpha(), allowed_moves))
        return allowed_moves


class Pawn(Piece):
    def __init__(self, color, board, num_coordinates):
        super().__init__(color, board, num_coordinates, 'p')

    def allowed_moves(self):

        if self.color == 'white':
            startpos, direction, enemy = 1, 1, 'black'
        else:
            startpos, direction, enemy = 6, -1, 'white'

        allowed_moves = []
        # Moving
        occupied_cells = self.board.occupied(
            'white') + self.board.occupied('black')
        start_position = self.coordinate

        forward = start_position + (0,  direction)

        if forward.get_alpha() not in occupied_cells:
            allowed_moves.append(forward)
            # Pawn is at the beginning, a movement of 2 cells is allowed
            if start_position.y == startpos:
                double_forward = forward + (0, direction)
                if double_forward.get_alpha() not in occupied_cells:
                    allowed_moves.append(double_forward)

        # Attacking (works diagonally)
        for a in [-1, 1]:
            attack = start_position + (a, direction)
            if attack.get_alpha() in self.board.occupied(enemy):
                allowed_moves.append(attack)
        allowed_moves = filter(lambda x: x.is_on_board(), allowed_moves)
        allowed_moves = list(map(lambda x: x.get_alpha(), allowed_moves))
        return allowed_moves


class Colours:
    WHITE = 'white'
    BLACK = 'black'
