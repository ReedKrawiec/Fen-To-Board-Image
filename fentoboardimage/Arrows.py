import math
from PIL import Image


def _generateArrow(arrow, length, pieceSize):
    image = arrow
    _, _, _, alpha = image.split()
    resized = Image.new("RGBA", (pieceSize, int(pieceSize*length)))
    head = image.crop((0, 0, pieceSize, pieceSize)).convert("RGBA")
    tail = image.crop((0, pieceSize*2, pieceSize,
                       pieceSize*3)).convert("RGBA")

    body = image.crop(
        (0, pieceSize, pieceSize, pieceSize*2)).convert("RGBA")
    resized.paste(head)
    resized.paste(tail, (0, int(pieceSize * (length - 1))))
    if length > 2:
        body = body.resize((pieceSize, int(pieceSize * (length - 2))))
        resized.paste(body, (0, pieceSize))
    return resized

# TODO Separate the different arrow types into their own functions


def paintAllArrows(board, arrowConfiguration, arrowSet):
    height, width = board.size
    pieceSize = int(width/8)
    def position(val): return int(val * pieceSize)
    for arrow in arrowConfiguration:
        start = arrow[0]
        end = arrow[1]
        delta = (end[0] - start[0], end[1] - start[1])
        start_x = position(start[0])
        start_y = position(start[1])
        target_x = position(end[0])
        target_y = position(end[1])
        if delta == (-2, 1):
            image = arrowSet["one"].transpose(Image.FLIP_TOP_BOTTOM)
            _, _, _, alpha = image.split()
            Image.Image.paste(board, image, (target_x, start_y), alpha)
        elif delta == (-1, 2):
            image = arrowSet["one"].transpose(Image.ROTATE_270).transpose(
                Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
            _, _, _, alpha = image.split()
            Image.Image.paste(board, image, (target_x, start_y), alpha)
        elif delta == (1, 2):
            image = arrowSet["one"].transpose(Image.ROTATE_270).transpose(
                Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_180)
            _, _, _, alpha = image.split()
            Image.Image.paste(board, image, (start_x, start_y), alpha)
        elif delta == (2, 1):
            image = arrowSet["one"].transpose(Image.ROTATE_180)
            _, _, _, alpha = image.split()
            Image.Image.paste(board, image, (start_x, start_y), alpha)
        elif delta == (2, -1):
            image = arrowSet["one"].transpose(Image.FLIP_LEFT_RIGHT)
            _, _, _, alpha = image.split()
            Image.Image.paste(board, image, (start_x, target_y), alpha)
        elif delta == (1, -2):
            image = arrowSet["one"].transpose(Image.ROTATE_270).transpose(
                Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_LEFT_RIGHT)
            _, _, _, alpha = image.split()
            Image.Image.paste(board, image, (start_x, target_y), alpha)
        elif delta == (-1, -2):
            image = arrowSet["one"].transpose(
                Image.ROTATE_270).transpose(Image.FLIP_LEFT_RIGHT)
            _, _, _, alpha = image.split()
            Image.Image.paste(board, image, (target_x, target_y), alpha)
        elif delta == (-2, -1):
            image = arrowSet["one"]
            _, _, _, alpha = image.split()
            Image.Image.paste(board, image, (target_x, target_y), alpha)
        elif delta[0] == 0:
            image = _generateArrow(
                arrowSet["up"], abs(delta[1]) + 1, pieceSize)
            if delta[1] > 0:
                image = image.transpose(Image.ROTATE_180)
                _, _, _, alpha = image.split()
                Image.Image.paste(board, image, (start_x, start_y), alpha)
            else:
                _, _, _, alpha = image.split()
                Image.Image.paste(board, image, (target_x, target_y), alpha)
        elif delta[1] == 0:
            image = _generateArrow(arrowSet["up"], abs(
                delta[0]) + 1, pieceSize).transpose(Image.ROTATE_270)
            if delta[0] < 0:
                image = image.transpose(Image.ROTATE_180)
                _, _, _, alpha = image.split()
                Image.Image.paste(board, image, (target_x, target_y), alpha)
            else:
                _, _, _pass, alpha = image.split()
                Image.Image.paste(board, image, (start_x, start_y), alpha)
        elif abs(delta[0]) == abs(delta[1]):
            arrow = _generateArrow(arrowSet["up"], (math.sqrt(
                (abs(delta[0]) + 0.5)**2 + (abs(delta[1]) + 0.5)**2)), pieceSize).rotate(45, expand=True)
            if delta[0] > 0 and delta[1] > 0:
                arrow = arrow.transpose(Image.ROTATE_180)
                _, _, _, alpha = arrow.split()
                Image.Image.paste(board, arrow, (start_x, start_y), alpha)
            elif delta[0] > 0 and delta[1] < 0:
                arrow = arrow.transpose(Image.ROTATE_270)
                _, _, _, alpha = arrow.split()
                Image.Image.paste(board, arrow, (start_x, target_y), alpha)
            elif delta[0] < 0 and delta[1] > 0:
                arrow = arrow.transpose(Image.ROTATE_90)
                _, _, _, alpha = arrow.split()
                Image.Image.paste(board, arrow, (target_x, start_y), alpha)
            elif delta[0] < 0 and delta[1] < 0:
                _, _, _, alpha = arrow.split()
                Image.Image.paste(board, arrow, (target_x, target_y), alpha)

        else:
            raise ValueError("Invalid arrow target: start(" +
                             str(start) + ") end(" + str(end) + ")")
    return board
