# Python Packages imports
import sys
import time
import math

# Custom module imports
from board import Board
from piece import Piece
from Constants import possible_moves, first_player, second_player


class ChineseCheckers:

    def __init__(self, depth=1, rows_size=17, cols_size=25, t_limit=60, c_player=Piece.P_RED):
        # Create initial board
        board = [[[None] * rows_size for __ in range(cols_size)] for _ in range(rows_size)]

        # Initialize every part in the board
        self.first_player = first_player
        self.second_player = second_player
        self.possible_moves = possible_moves

        for row in range(rows_size):
            for col in range(cols_size):
                if [row, col] in self.first_player:
                    element = Piece(2, 2, 0, row, col)
                elif [row, col] in self.second_player:
                    element = Piece(1, 1, 0, row, col)
                elif [row, col] in self.possible_moves:
                    element = Piece(0, 0, 0, row, col)
                else:
                    element = Piece(3, 0, 0, row, col)

                board[row][col] = element

        self.rows_size = rows_size
        self.cols_size = cols_size

        self.t_limit = t_limit
        self.c_player = c_player
        self.board_view = Board(board)
        self.board = board
        # Our Player
        self.current_player = Piece.P_GREEN
        self.selected_piece = None
        self.valid_moves = []
        self.computing = False
        self.total_plies = 0

        self.ply_depth = depth
        self.ab_enabled = True

        self.r_goals = [t for row in board
                        for t in row if t.tile == Piece.T_RED]
        self.g_goals = [t for row in board
                        for t in row if t.tile == Piece.T_GREEN]

        self.board_view.Status_color("#E50000" if
                                         self.current_player == Piece.P_RED else "#007F00")

        if self.c_player == self.current_player:
            self.ComputerMove()

        self.board_view.Click_handler(self.TileClicked)
        self.board_view.Pieces(board=self.board)  # Refresh the board

        # Print initial program info
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("Turn time limit:", self.t_limit)
        print("Max play depth:", self.ply_depth)
        print()

        self.board_view.mainloop()  # Begin tkinter main loop

    def TileClicked(self, row, col):

        if self.computing:  # Block clicks while computing
            return

        new_tile = self.board[row][col]

        # If we are selecting a friendly piece
        if new_tile.piece == self.current_player:

            self.OutlineTile(None)  # Reset outlines

            # Outline the new and valid move tiles
            new_tile.outline = Piece.O_MOVED
            self.valid_moves = self.MovesAtTile(new_tile,
                                                      self.current_player)
            self.OutlineTile(self.valid_moves)

            # Update status and save the new tile
            self.board_view.Status("Tile " + str(new_tile) + " selected")
            self.selected_piece = new_tile

            self.board_view.Pieces(board=self.board)  # Refresh the board

        # If we already had a piece selected and we are moving a piece
        elif self.selected_piece and new_tile in self.valid_moves:

            self.OutlineTile(None)  # Reset outlines
            self.MovePiece(self.selected_piece, new_tile)  # Move the piece

            # Update status and reset tracking variables
            self.selected_piece = None
            self.valid_moves = []
            self.current_player = (Piece.P_RED
                                   if self.current_player == Piece.P_GREEN else Piece.P_GREEN)

            self.board_view.Pieces(board=self.board)  # Refresh the board

            # If there is a winner to the game
            winner = self.isWinner()
            if winner:
                self.board_view.Status("The " + ("green"
                                                     if winner == Piece.P_GREEN else "red") + " player has won!")
                self.current_player = None

            elif self.c_player is not None:
                self.ComputerMove()
        """""
        else:
            self.board_view.set_status("Invalid move attempted")"""

    def minimax(self, depth, maximizingPlayer, max_time, maxValue=float("-inf"),
                minValue=float("inf"), maxing=True, prunes=0, boards=0):

        # Bottomed out base case
        if depth == 0 or self.isWinner() or time.time() > max_time:
            return self.Distance(maximizingPlayer), None, prunes, boards

        # Setup initial variables and find moves
        best_move = None
        if maxing:
            best_val = float("-inf")
            moves = self.NextMoves(maximizingPlayer)
        else:
            best_val = float("inf")
            moves = self.NextMoves((Piece.P_RED
                                         if maximizingPlayer == Piece.P_GREEN else Piece.P_GREEN))

        # For each move
        for move in moves:
            for to in move["to"]:

                # Bail out when we're out of time
                if time.time() > max_time:
                    return best_val, best_move, prunes, boards

                # Move piece to the move outlined
                piece = move["from"].piece
                move["from"].piece = Piece.P_NONE
                to.piece = piece
                boards += 1

                # Recursively call self
                val, _, new_prunes, new_boards = self.minimax(depth - 1,
                                                              maximizingPlayer, max_time, maxValue, minValue,
                                                              not maxing, prunes, boards)
                prunes = new_prunes
                boards = new_boards

                # Move the piece back
                to.piece = Piece.P_NONE
                move["from"].piece = piece

                if maxing and val > best_val:
                    best_val = val
                    best_move = (move["from"].loc, to.loc)
                    maxValue = max(maxValue, val)

                if not maxing and val < best_val:
                    best_val = val
                    best_move = (move["from"].loc, to.loc)
                    minValue = min(minValue, val)

                if self.ab_enabled and minValue <= maxValue:
                    return best_val, best_move, prunes + 1, boards

        return best_val, best_move, prunes, boards

    def ComputerMove(self):

        # Print out search information
        current_turn = (self.total_plies // 2) + 1
        print("Turn", current_turn, "Computation")
        print(">>>>>>>>>" + (">" * len(str(current_turn))))
        print("Executing search ...", end=" ")
        sys.stdout.flush()

        self.board_view.Status("Computing next move...")
        self.computing = True
        self.board_view.update()
        max_time = time.time() + self.t_limit

        # Execute minimax search
        start = time.time()
        _, move, prunes, boards = self.minimax(self.ply_depth,
                                               self.c_player, max_time)
        end = time.time()

        # Print search result stats
        print("complete")
        print("Time to compute:", round(end - start, 4))
        print("Total boards generated:", boards)
        print("Total prune events:", prunes)

        # Move the resulting piece
        self.OutlineTile(None)  # Reset outlines
        move_from = self.board[move[0][0]][move[0][1]]
        move_to = self.board[move[1][0]][move[1][1]]
        self.MovePiece(move_from, move_to)

        self.board_view.Pieces(board=self.board)  # Refresh the board

        winner = self.isWinner()
        if winner:
            self.board_view.Status("The " + ("green"
                                                 if winner == Piece.P_GREEN else "red") + " player has won!")
            self.board_view.Status_color("#212121")
            self.current_player = None
            self.current_player = None

            print()
            print("Final Stats")
            print(">>>>>>>>>>")
            print("Final winner:", "green"
            if winner == Piece.P_GREEN else "red")
            print("Total # of plies:", self.total_plies)

        else:  # Toggle the current player
            self.current_player = (Piece.P_RED
                                   if self.current_player == Piece.P_GREEN else Piece.P_GREEN)

        self.computing = False
        print()

    def NextMoves(self, player=1):

        moves = []  # All possible moves
        for col in range(self.cols_size):
            for row in range(self.rows_size):

                curr_tile = self.board[row][col]

                # Skip board elements that are not the current player
                if curr_tile.piece != player:
                    continue

                # Restrictions

                move = {
                    "from": curr_tile,
                    "to": self.MovesAtTile(curr_tile, player)
                }
                moves.append(move)

        return moves

    def MovesAtTile(self, tile, player, moves=None, adj=True):

        if moves is None:
            moves = []

        row = tile.loc[0]
        col = tile.loc[1]

        # List of valid tile types to move to
        valid_tiles = [Piece.T_NONE, Piece.T_GREEN, Piece.T_RED]
        if tile.tile != player:
            valid_tiles.remove(player)  # Moving back into your own goal
        if tile.tile != Piece.T_NONE and tile.tile != player:
            valid_tiles.remove(Piece.T_NONE)  # Moving out of the enemy's goal

        # Find and save immediately adjacent moves
        for i in [[-1, -1], [-1, 1], [0, 2], [1, 1], [1, -1], [0, -2], [2, 0]]:
            row_delta, col_delta = i

            # Check adjacent pieces
            new_row = row + row_delta
            new_col = col + col_delta

            # Skip checking degenerate values
            if ((new_row == row and new_col == col) or
                    new_row < 0 or new_col < 0 or
                    new_row >= self.rows_size or new_col >= self.cols_size):
                continue

            # Handle moves out of/in to goals
            new_piece = self.board[new_row][new_col]
            if new_piece.tile not in valid_tiles:
                continue

            if new_piece.piece == Piece.P_NONE:
                if adj:  # Don't consider adjacent on subsequent calls
                    moves.append(new_piece)
                continue

            # Check jump tiles

            new_row = new_row + row_delta
            new_col = new_col + col_delta

            # Skip checking degenerate values
            if (new_row < 0 or new_col < 0 or
                    new_row >= self.rows_size or new_col >= self.cols_size):
                continue

            # Handle returning moves and moves out of/in to goals
            new_piece = self.board[new_row][new_col]
            if new_piece in moves or (new_piece.tile not in valid_tiles):
                continue

            if new_piece.piece == Piece.P_NONE:
                moves.insert(0, new_piece)  # Prioritize jumps
                self.MovesAtTile(new_piece, player, moves, False)

        return moves

    def MovePiece(self, from_tile, to_tile):

        # Handle trying to move a non-existent piece and moving into a piece
        if from_tile.piece == Piece.P_NONE or to_tile.piece != Piece.P_NONE:
            self.board_view.Status("Invalid move")
            return

        # Move piece
        to_tile.piece = from_tile.piece
        from_tile.piece = Piece.P_NONE

        # Update outline
        to_tile.outline = Piece.O_MOVED
        from_tile.outline = Piece.O_MOVED

        self.total_plies += 1

        self.board_view.Status_color("#007F00" if
                                         self.current_player == Piece.P_RED else "#E50000")
        from_tile.tile = 0
        if self.current_player == Piece.P_GREEN:
            to_tile.tile = 1
        else:
            to_tile.tile = 2
        self.board_view.Status("Piece moved from " + str(from_tile) +
                                   " to " + str(to_tile) + ", " + ("green's" if
                                                                      self.current_player == Piece.P_RED else "red's") + " turn...")

    def isWinner(self):

        if all(g.piece == Piece.P_GREEN for g in self.r_goals):
            return Piece.P_GREEN
        elif all(g.piece == Piece.P_RED for g in self.g_goals):
            return Piece.P_RED
        else:
            return None

    def OutlineTile(self, tiles=[], outline_type=Piece.O_SELECT):

        if tiles is None:
            tiles = [j for i in self.board for j in i]
            outline_type = Piece.O_NONE

        for tile in tiles:
            tile.outline = outline_type

    def Distance(self, player):

        def PointDistance(p0, p1):
            return math.sqrt((p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2)

        value = 0

        for col in range(self.cols_size):
            for row in range(self.rows_size):

                tile = self.board[row][col]

                if tile.piece == Piece.P_GREEN:
                    distances = [PointDistance(tile.loc, g.loc) for g in
                                 self.r_goals if g.piece != Piece.P_GREEN]
                    value -= max(distances) if len(distances) else -50

                elif tile.piece == Piece.P_RED:
                    distances = [PointDistance(tile.loc, g.loc) for g in
                                 self.g_goals if g.piece != Piece.P_RED]
                    value += max(distances) if len(distances) else -50

        if player == Piece.P_RED:
            value *= -1

        return value
