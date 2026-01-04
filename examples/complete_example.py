"""Example: Combining multiple features.

This example shows how to use multiple features together: coordinates,
arrows, last move highlighting, and custom colors all in one board.
"""

from fentoboardimage import (
    fen_to_image,
    load_pieces_folder,
    load_arrows_folder,
    load_font_file,
    coordinate_position_fn,
)

# Position after a tactical sequence with annotations
board = fen_to_image(
    fen="r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
    square_length=120,
    piece_set=load_pieces_folder("pieces"),
    dark_color="#769656",
    light_color="#eeeed2",
    arrow_set=load_arrows_folder("arrows"),
    arrows=[
        ["f3", "e5"],  # Knight can capture pawn
        ["c4", "f7"],  # Bishop attacks f7
    ],
    last_move={
        "before": "g1",
        "after": "f3",
        "darkColor": "#aaa23b",
        "lightColor": "#cdd26a",
    },
    coordinates={
        "font": load_font_file("fonts/Arial.ttf"),
        "size": 20,
        "dark_color": "#eeeed2",
        "light_color": "#769656",
        "position_fn": coordinate_position_fn["standard"],
    },
)

board.show()
