from PIL import Image


def paintPiece(board, cord, image):
    height, width = board.size
    pieceSize = int(width/8)
    x = cord[0]
    y = cord[1]
    def position(val): return int(val * pieceSize)
    box = (position(x), position(y), position(x + 1), position(y + 1))

    # Extract the alpha layer to use as a mask
    # when pasting, to not overwrite the board
    _, _, _, alpha = image.split()
    Image.Image.paste(board, image, box, alpha)

    return board


def paintAllPieces(board, parsed, pieceImages):
    for y in range(0, len(parsed)):
        for x in range(0, len(parsed[y])):
            piece = parsed[y][x]
            if piece != " ":
                board = paintPiece(
                    board, (x, y), pieceImages[piece])
    return board
