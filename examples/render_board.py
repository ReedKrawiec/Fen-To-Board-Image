from fentoboardimage import fen_to_image, load_pieces_folder

board = fen_to_image(
    fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    square_length=200,
    piece_set=load_pieces_folder("pieces"),
    dark_color="#79a65d",
    light_color="#daf2cb",
)

board.show()
