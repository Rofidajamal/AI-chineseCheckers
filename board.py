# Python Standard Library imports
import tkinter as tk


class Board(tk.Tk):

    def __init__(self, init_board, *args, **kwargs):

        # Initialize parent tk class to create empty window
        tk.Tk.__init__(self, *args, **kwargs)

        # Setting Title
        self.title("Chinese Checkers")
        # self.wm_iconbitmap("")
        self.resizable(False, False)
        # Setting Background
        self.configure(bg="#fff")

        # Save tracking variables
        self.pieces = {}
        self.board = init_board
        self.r_size = len(init_board)
        self.c_size = len(init_board[0])

        # Create grid canvas
        self.canvas = tk.Canvas(self, width=550, height=550, bg="#fff",
                                highlightthickness=0)
        self.canvas.grid(row=1, column=1,
                         columnspan=self.c_size, rowspan=self.r_size)

        # Create status label
        self.status = tk.Label(self, anchor="c", font=(None, 16),
                               bg="#212121", fg="#fff", text="Green player's turn")
        self.status.grid(row=self.r_size + 3, column=0,
                         columnspan=self.c_size + 3, sticky="ewns")

        # ---------------------------------------------
        # Shape Initializing
        # ---------------------------------------------
        # Game Shape
        self.canvas.bind("<Configure>", self.Pieces)

        # Shape Around the game
        self.columnconfigure(0, minsize=48)
        self.rowconfigure(0, minsize=48)
        self.columnconfigure(self.c_size + 2, minsize=48)
        self.rowconfigure(self.r_size + 2, minsize=48)
        self.rowconfigure(self.r_size + 3, minsize=48)

    # Methods
    def Click_handler(self, func):
        self.click_handler = func

    def Status(self, text):
        self.status.configure(text=text)

    def Status_color(self, color):
        self.status.configure(bg=color)

    def Pieces(self, event=None, board=None):

        if board is not None:
            self.board = board

        # Delete old rectangles and save properties
        self.canvas.delete("tile")

        # Can Change Width and Height From here
        cell_width = int(self.canvas.winfo_width() / self.c_size)
        cell_height = int(self.canvas.winfo_height() / self.r_size)
        border_size = 5

        # Recreate each rectangle
        for col in range(self.c_size):
            for row in range(self.r_size):
                board_tile = self.board[row][col]
                tile_color, outline_color = board_tile.TileColors()

                # Calculate pixel positions
                x1 = col * cell_width + border_size / 2
                y1 = row * cell_height + border_size / 2
                x2 = (col + 1) * cell_width - border_size / 2
                y2 = (row + 1) * cell_height - border_size / 2

                # Render tile
                tile = self.canvas.create_oval(x1, y1, x2, y2,
                                               tags="tile", width=border_size, fill=tile_color,
                                               outline=outline_color)
                self.pieces[row, col] = tile

                # if some event happened
                self.canvas.tag_bind(tile, "<1>", lambda event, row=row,
                                                         col=col: self.click_handler(row, col))

        self.update()
