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

    def reachable_positions_base(self, allow_orthogonal, allow_diagonal, max_allowed_distance):  # TODO
        return []


class King(Piece):

    def __init__(self, color, board, alpha_coordinate):
        super().__init__(color, board, alpha_coordinate, 'k')

    def reachable_positions(self):  # TODO
        return []


class Queen(Piece):
    def __init__(self, color, board, alpha_coordinate):
        super().__init__(color, board, alpha_coordinate, 'q')

    def reachable_positions(self):  # TODO
        return []


class Rook(Piece):
    def __init__(self, color, board, alpha_coordinate):
        super().__init__(color, board, alpha_coordinate, 'r')

    def reachable_positions(self):  # TODO
        return []


class Bishop(Piece):
    def __init__(self, color, board, alpha_coordinate):
        super().__init__(color, board, alpha_coordinate, 'b')

    def reachable_positions(self):  # TODO
        return []


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
