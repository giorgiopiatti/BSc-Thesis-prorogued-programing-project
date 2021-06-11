from chessboard import Board
import chessboard
import tkinter as tk
import sys
from pieces import Coordinate
import pieces

COLOR1 = "#DDB88C"
COLOR2 = "#A66D4F"
HIGHLIGHT_COLOR = "khaki"
ROWS = 8
COLUMNS = 8

DIM_SQUARE = 64

# adapted from https://github.com/saavedra29/chess_tk


class GUI:
    selected_piece = None
    focused = None
    images = {}

    def __init__(self, parent):
        """
        Initialize user interface
        """
        self.parent = parent
        # Adding Top Menu
        self.menubar = tk.Menu(parent)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New Game", command=self.new_game)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.parent.config(menu=self.menubar)

        # Adding Frame
        self.board_frame = tk.Frame(parent, height=DIM_SQUARE)
        self.info_label = tk.Label(self.board_frame,
                                   text="   White to Start the Game  ",
                                   fg=COLOR2)
        self.info_label.pack(side=tk.RIGHT, padx=8, pady=5)
        self.board_frame.pack(fill="x", side=tk.BOTTOM)

        self.canvas = tk.Canvas(parent, width=COLUMNS * DIM_SQUARE,
                                height=ROWS * DIM_SQUARE)
        self.canvas.pack(padx=8, pady=8)
        self.draw_board()
        self.canvas.bind("<Button-1>", self.square_clicked)

        self.new_game()

    def new_game(self):
        self.chessboard = Board()
        self.draw_board()
        self.draw_pieces()
        self.info_label.config(text="   White to Start the Game  ", fg=COLOR2)

    def square_clicked(self, event):
        selected_column = int(event.x / DIM_SQUARE)
        selected_row = 7 - int(event.y / DIM_SQUARE)
        coord = Coordinate(selected_column, selected_row)
        pos = coord.get_alpha()

        if self.selected_piece:
            self.shift(self.selected_piece, pos)
            self.selected_piece = None
            self.focused = None
            self.draw_board()
            self.draw_pieces()
        self.focus(pos)
        self.draw_board()

    def shift(self, p1, p2):
        piece = self.chessboard[p1]
        dest_piece = self.chessboard.get(p2)

        if dest_piece is None or dest_piece.color != piece.color:
            try:
                self.chessboard.shift(p1, p2)
            except chessboard.ChessError as error:
                self.info_label["text"] = error.__class__.__name__
                raise error
            else:
                turn = ('white' if piece.color == 'black' else 'black')
                self.info_label["text"] = f'{piece.color.capitalize()} : {p1}{p2} {turn.capitalize()}\'s turn.'

    def focus(self, pos):
        piece = self.chessboard.get(pos)
        if piece is not None and (piece.color == self.chessboard.player_turn):
            self.selected_piece = pos

            try:
                self.chessboard.game_status(piece.color)
            except chessboard.ChessError as error:
                self.info_label["text"] = error.__class__.__name__
                raise error
            focused = set(self.chessboard[pos].reachable_positions()) & set(
                self.chessboard.reachable_positions_do_not_check(piece.color))  # perform intersection
            self.focused = list(map(self.get_screen_coordinates,
                                focused))

    def create_rectangle(self, row, col, colour):
        x1 = (col * DIM_SQUARE)
        y1 = ((7 - row) * DIM_SQUARE)
        x2 = x1 + DIM_SQUARE
        y2 = y1 + DIM_SQUARE
        self.canvas.create_rectangle(x1, y1, x2, y2,
                                     fill=colour,
                                     tags="area")

    def draw_board(self):
        color = COLOR2
        for row in range(ROWS):
            color = COLOR1 if color == COLOR2 else COLOR2
            for col in range(COLUMNS):
                if (self.focused is not None and (row, col) in self.focused):
                    self.create_rectangle(row, col, HIGHLIGHT_COLOR)
                else:
                    self.create_rectangle(row, col, color)

                color = COLOR1 if color == COLOR2 else COLOR2
        self.canvas.tag_raise("occupied")
        self.canvas.tag_lower("area")

    def draw_pieces(self):
        self.canvas.delete("occupied")
        for coord, piece in self.chessboard.items():
            x, y = self.get_screen_coordinates(coord)
            if piece is not None:
                filename = "pieces_image/" + piece.get_image_name()
                piecename = piece.short_name + str(x) + str(y)
                if filename not in self.images:
                    self.images[filename] = tk.PhotoImage(
                        file=sys.path[0]+'/' + filename)
                self.canvas.create_image(0, 0, image=self.images[filename],
                                         tags=(piecename, "occupied"),
                                         anchor="c")
                x0 = (y * DIM_SQUARE) + int(DIM_SQUARE / 2)
                y0 = ((7 - x) * DIM_SQUARE) + int(DIM_SQUARE / 2)
                self.canvas.coords(piecename, x0, y0)

    def get_screen_coordinates(self, coord):
        x, y = coord[0], coord[1]
        return Coordinate.y_axis.index(int(y)), Coordinate.x_axis.index(x)


def main():
    root = tk.Toplevel()
    root.title("Chess")
    GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
