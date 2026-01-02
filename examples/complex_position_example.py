"""Example: Rendering complex chess positions.

This example demonstrates rendering interesting chess positions beyond
the starting position, including tactical positions and endgames.
"""

from fentoboardimage import fen_to_image, load_pieces_folder

# Scholar's Mate position - a classic checkmate pattern
scholars_mate = fen_to_image(
    fen="r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4",
    square_length=100,
    piece_set=load_pieces_folder("pieces"),
    dark_color="#769656",
    light_color="#eeeed2",
)

scholars_mate.save("scholars_mate.png")
print("Saved Scholar's Mate position to scholars_mate.png")

# King and pawn endgame
endgame = fen_to_image(
    fen="8/8/8/4k3/8/8/4K3/8 w - - 0 1",
    square_length=100,
    piece_set=load_pieces_folder("pieces"),
    dark_color="#b58863",
    light_color="#f0d9b5",
)

endgame.save("endgame.png")
print("Saved endgame position to endgame.png")
