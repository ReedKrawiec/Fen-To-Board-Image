"""Example: Rendering a board with coordinates.

This example demonstrates how to add coordinate labels (a-h, 1-8) to the board
using the coordinate_position_fn feature.

Available styles:
  - "standard": Chess.com/Lichess style (rank on a-file, file on 1st rank)
  - "every_square": Full notation (e.g., "e4") on every square
  - "along_outer_rim": Coordinates centered along board edges
"""

from fentoboardimage import (
    fen_to_image,
    load_pieces_folder,
    load_font_file,
    coordinate_position_fn,
)

board = fen_to_image(
    fen="rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
    square_length=100,
    piece_set=load_pieces_folder("pieces"),
    dark_color="#769656",
    light_color="#eeeed2",
    coordinates={
        "font": load_font_file("fonts/Arial.ttf"),
        "size": 18,
        "dark_color": "#eeeed2",
        "light_color": "#769656",
        "position_fn": coordinate_position_fn["standard"],
    },
)

board.show()
