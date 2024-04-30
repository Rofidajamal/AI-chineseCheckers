class Piece:
    T_NONE = 0
    T_GREEN = 1
    T_RED = 2

    P_NONE = 0
    P_GREEN = 1
    P_RED = 2

    O_NONE = 0
    O_SELECT = 1
    O_MOVED = 2

    def __init__(self, tile=0, pieceType=0, outline=0, row=0, col=0):
        self.tile = tile
        self.piece = pieceType
        self.outline = outline

        self.row = row
        self.col = col
        self.loc = (row, col)

    def TileColors(self):
        tile_colors = [
            ("#EAEBFF", "#EAEBFF"),
            ("#71b651", "#a6ce9d"),
            ("#ba6262", "#ce9d9d"),
            ("#FFFFFF", "#FFFFFF"),
            ("#EAEBFF", "#EAEBFF")
        ]
        tile_color = tile_colors[self.tile][(self.loc[0] + self.loc[1]) % 2]

        piece_outline_colors = [
            tile_color,
            "yellow",
            "#1100BB"
        ]
        outline_color = piece_outline_colors[self.outline]

        return tile_color, outline_color

    def __str__(self):
        return chr(self.loc[1] + 97) + str(self.loc[0] + 1)

    def __repr__(self):
        return chr(self.loc[1] + 97) + str(self.loc[0] + 1)

