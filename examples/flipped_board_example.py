"""Example: Rendering the board from black's perspective.

This example demonstrates the flipped parameter which rotates the board
180 degrees to show black's perspective.
"""

from fentoboardimage import fen_to_image, load_pieces_folder

# Sicilian Defense position from black's perspective
board = fen_to_image(
    fen="rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2",
    square_length=100,
    piece_set=load_pieces_folder("pieces"),
    dark_color="#b58863",
    light_color="#f0d9b5",
    flipped=True,
)

board.show()
