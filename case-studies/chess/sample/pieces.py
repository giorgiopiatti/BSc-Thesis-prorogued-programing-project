from enum import Enum
import sys


class Coordinate():
    """
    Represent a cordinate on the board place.
    Chess's notation is of the form LetterNumber, but to better calculate we save them as 
    number coordinates in the space [0,7]x[0,7]

    """
    x_axis = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
    y_axis = (1, 2, 3, 4, 5, 6, 7, 8)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_alpha(self):
        if not self.is_on_board():
            return None
        return self.x_axis[self.x] + str(self.y_axis[self.y])

    def __add__(self, coord):
        """
        Element-wise addition
        """
        x, y = coord
        return Coordinate(self.x + x, self.y + y)

    def __mul__(self, a):
        """
        Multiplication by a scalar
        """
        return Coordinate(self.x * a, self.y * a)

    def is_on_board(self):
        """
        Check if coordinate is on the board, i.e. part of the 
        subspace [0,7]x[0,7]
        """
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

    def __init__(self, color, board, alpha_coordinate, short_name):
        self.color = color
        self.board = board
        self.coordinate = Coordinate.init_from_alpha(alpha_coordinate)
        self.short_name = short_name

    def get_image_name(self):
        return self.short_name + self.color + '.png'

    def update_coordinates(self, coord):
        self.coordinate = Coordinate.init_from_alpha(coord)

    # SKELETON remove
    def reachable_positions_base(self, allow_orthogonal, allow_diagonal, max_allowed_distance):

        reachable_positions = []
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
                    reachable_positions.append(dest)
                elif dest.get_alpha() in self.board.occupied(
                        self.color):  # Same color
                    collision = True
                else:  # Can eat a piece
                    reachable_positions.append(dest)
                    collision = True
        reachable_positions = filter(
            lambda x: x.is_on_board(), reachable_positions)
        reachable_positions = list(
            map(lambda x: x.get_alpha(), reachable_positions))
        return reachable_positions


class King(Piece):

    def __init__(self, color, board, alpha_coordinate):
        super().__init__(color, board, alpha_coordinate, 'k')

    def reachable_positions(self):  # SKELETON remove
        return super(King, self).reachable_positions_base(allow_orthogonal=True, allow_diagonal=True, max_allowed_distance=1)


class Queen(Piece):
    def __init__(self, color, board, alpha_coordinate):
        super().__init__(color, board, alpha_coordinate, 'q')

    def reachable_positions(self):  # SKELETON remove
        return super(Queen, self).reachable_positions_base(allow_orthogonal=True, allow_diagonal=True, max_allowed_distance=8)


class Rook(Piece):
    def __init__(self, color, board, alpha_coordinate):
        super().__init__(color, board, alpha_coordinate, 'r')

    def reachable_positions(self):  # SKELETON remove
        return super(Rook, self).reachable_positions_base(allow_orthogonal=True, allow_diagonal=False, max_allowed_distance=8)


class Bishop(Piece):
    def __init__(self, color, board, alpha_coordinate):
        super().__init__(color, board, alpha_coordinate, 'b')

    def reachable_positions(self):  # SKELETON remove
        return super(Bishop, self).reachable_positions_base(allow_orthogonal=False, allow_diagonal=True, max_allowed_distance=8)


class Knight(Piece):
    def __init__(self, color, board, alpha_coordinate):
        super().__init__(color, board, alpha_coordinate, 'n')

    def reachable_positions(self):
        reachable_positions = []
        start_position = self.coordinate

        deltas = (
            (-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for x, y in deltas:
            dest = start_position + (x, y)
            if dest.get_alpha() not in self.board.occupied(self.color):
                reachable_positions.append(dest)
        reachable_positions = filter(
            lambda x: x.is_on_board(), reachable_positions)
        reachable_positions = list(
            map(lambda x: x.get_alpha(), reachable_positions))
        return reachable_positions


class Pawn(Piece):
    def __init__(self, color, board, alpha_coordinate):
        super().__init__(color, board, alpha_coordinate, 'p')

    def reachable_positions(self):

        if self.color == 'white':
            startpos, direction, enemy = 1, 1, 'black'
        else:
            startpos, direction, enemy = 6, -1, 'white'

        reachable_positions = []
        # Moving
        occupied_cells = self.board.occupied(
            'white') + self.board.occupied('black')
        start_position = self.coordinate

        forward = start_position + (0,  direction)

        if forward.get_alpha() not in occupied_cells:
            reachable_positions.append(forward)
            # Pawn is at the beginning, a movement of 2 cells is allowed
            if start_position.y == startpos:
                double_forward = forward + (0, direction)
                if double_forward.get_alpha() not in occupied_cells:
                    reachable_positions.append(double_forward)

        # Attacking (works diagonally)
        for a in [-1, 1]:
            attack = start_position + (a, direction)
            if attack.get_alpha() in self.board.occupied(enemy):
                reachable_positions.append(attack)
        reachable_positions = filter(
            lambda x: x.is_on_board(), reachable_positions)
        reachable_positions = list(
            map(lambda x: x.get_alpha(), reachable_positions))
        return reachable_positions


class Colours:
    WHITE = 'white'
    BLACK = 'black'
