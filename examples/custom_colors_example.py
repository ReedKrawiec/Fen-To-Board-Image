"""Example: Using custom board colors.

This example shows how to customize the light and dark square colors
to create different board themes.
"""

from fentoboardimage import fen_to_image, load_pieces_folder

# Create a board with custom brown/tan color scheme
board = fen_to_image(
    fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    square_length=100,
    piece_set=load_pieces_folder("pieces"),
    dark_color="#D18B47",  # Darker brown for dark squares
    light_color="#FFCE9E",  # Lighter tan for light squares
)

board.show()
