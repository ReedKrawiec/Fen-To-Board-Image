"""Example: Highlighting the last move on the board.

This example shows how to highlight the squares involved in the last move
with custom colors, similar to popular chess websites.
"""

from fentoboardimage import fen_to_image, load_pieces_folder

# Position after 1.e4 - highlight the e2-e4 move
board = fen_to_image(
    fen="rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
    square_length=100,
    piece_set=load_pieces_folder("pieces"),
    dark_color="#769656",
    light_color="#eeeed2",
    last_move={
        "before": "e2",
        "after": "e4",
        "darkColor": "#aaa23b",
        "lightColor": "#cdd26a",
    },
)

board.show()
