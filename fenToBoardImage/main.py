#!/usr/bin/env python

from PIL import Image
from PIL import ImageDraw
import os
import math
from itertools import chain
import re
from unittest import TestCase

# https://github.com/tlehman/fenparser


class FenParser():
    def __init__(self, fen_str):
        self.fen_str = fen_str

    def parse(self):
        ranks = self.fen_str.split(" ")[0].split("/")
        pieces_on_all_ranks = [self.parse_rank(rank) for rank in ranks]
        return pieces_on_all_ranks

    def parse_rank(self, rank):
        rank_re = re.compile("(\d|[kqbnrpKQBNRP])")
        piece_tokens = rank_re.findall(rank)
        pieces = self.flatten(map(self.expand_or_noop, piece_tokens))
        return pieces

    def flatten(self, lst):
        return list(chain(*lst))

    def expand_or_noop(self, piece_str):
        piece_re = re.compile("([kqbnrpKQBNRP])")
        retval = ""
        if piece_re.match(piece_str):
            retval = piece_str
        else:
            retval = self.expand(piece_str)
        return retval

    def expand(self, num_str):
        return int(num_str)*" "


class FenParserTest(TestCase):
    def test_parse_rank(self):
        start_pos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        rank8 = "rnbqkbnr"
        rank7 = "pppppppp"
        rank6 = "8"
        fp = FenParser(start_pos)
        assert fp.parse_rank(rank8) == ["r", "n", "b", "q", "k", "b", "n", "r"]
        assert fp.parse_rank(rank7) == ["p", "p", "p", "p", "p", "p", "p", "p"]
        assert fp.parse_rank(rank6) == [" ", " ", " ", " ", " ", " ", " ", " "]

    def test_parse_starting_position(self):
        start_pos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        fp = FenParser(start_pos)
        print(fp.parse())
        assert len(fp.parse()) == 8
        assert fp.parse() == [["r", "n", "b", "q", "k", "b", "n", "r"],
                              ["p", "p", "p", "p", "p", "p", "p", "p"],
                              [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]]


def paintCheckerBoard(board, darkColor, lastMove=None):
    height, width = board.size
    draw = ImageDraw.Draw(board)
    if height != width:
        # Require a square board, any stretching / transformations
        # should be handled afterwards through PIL
        raise Exception("Height unequal to width")

    def getRectanglePositionTuples(tup):
        return [((tup[0] + startSquareOffset) * squareSize, tup[1] * squareSize),
                ((tup[0] + startSquareOffset) * squareSize + squareSize - 1, tup[1] * squareSize + squareSize - 1)]

    def isLightSquare(tup):
        if tup[0] % 2 == 0:
            if tup[1] % 2 == 0:
                return True
            return False
        else:
            if tup[1] % 2 == 0:
                return False
            return True
    for y in range(0, 8):
        for x in range(0, 8, 2):
            # Four pairs of dark then light must be painted per row
            squareSize = width/8

            firstIsColored = y % 2 == 0
            # If the first square is colored, offset
            # the pattern of dark then light by one
            startSquareOffset = 1 if firstIsColored else 0
            draw.rectangle(getRectanglePositionTuples((x, y)), darkColor)
    if lastMove != None:
        beforeColor = lastMove["darkColor"]
        afterColor = lastMove["darkColor"]
        if isLightSquare(lastMove["before"]):
            beforeColor = lastMove["lightColor"]
        if isLightSquare(lastMove["after"]):
            afterColor = lastMove["lightColor"]
        draw.rectangle(getRectanglePositionTuples(
            lastMove["before"]), beforeColor)
        draw.rectangle(getRectanglePositionTuples(
            lastMove["after"]), afterColor)
    return board


"""
Loads the sprites for a piece set, and prepares it for the fenToBoardImage function

Parameters
----------
path: str
    Loads piece set located at the path provided.

"""


def loadPiecesFolder(path):
    whitePath = os.path.join(path, "white")
    blackPath = os.path.join(path, "black")
    # Generates the path for the requested piece
    def wPath(piece): return os.path.join(whitePath, piece + ".png")
    def bPath(piece): return os.path.join(blackPath, piece + ".png")
    pieceImages = {
        "p": Image.open(bPath("Pawn")).convert("RGBA"),
        "P": Image.open(wPath("Pawn")).convert("RGBA"),
        "r": Image.open(bPath("Rook")).convert("RGBA"),
        "R": Image.open(wPath("Rook")).convert("RGBA"),
        "n": Image.open(bPath("Knight")).convert("RGBA"),
        "N": Image.open(wPath("Knight")).convert("RGBA"),
        "b": Image.open(bPath("Bishop")).convert("RGBA"),
        "B": Image.open(wPath("Bishop")).convert("RGBA"),
        "q": Image.open(bPath("Queen")).convert("RGBA"),
            "Q": Image.open(wPath("Queen")).convert("RGBA"),
            "k": Image.open(bPath("King")).convert("RGBA"),
            "K": Image.open(wPath("King")).convert("RGBA")
    }

    def load(board):
        pieceSize = int(board.size[0]/8)
        for piece in pieceImages:
            pieceImages[piece] = pieceImages[piece].resize(
                (pieceSize, pieceSize))
        return pieceImages
    return load


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
                board = paintPiece(board, (x, y), pieceImages[piece])
    return board


def loadArrows(path):
    def arrowP(name): return os.path.join(path, name + ".png")
    arrows = {
        "one": Image.open(arrowP("Knight")).convert("RGBA"),
        "up": Image.open(arrowP("Up")).convert("RGBA")
    }

    def load(board):
        squareSize = int(board.size[0]/8)
        arrows["one"] = arrows["one"].resize((squareSize*3, squareSize*2))
        arrows["up"] = arrows["up"].resize((squareSize, squareSize*3))
        return arrows
    return load


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
        body = body.resize((pieceSize,int(pieceSize * (length - 2))))
        resized.paste(body,(0,pieceSize))
    return resized

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
            image = _generateArrow(arrowSet["up"], abs(delta[1]) + 1, pieceSize)
            if delta[1] > 0:
                image = image.transpose(Image.ROTATE_180)
                _, _, _, alpha = image.split()
                Image.Image.paste(board, image, (start_x, start_y), alpha)
            else:
                _, _, _, alpha = image.split()
                Image.Image.paste(board, image, (target_x, target_y), alpha)
        elif delta[1] == 0:
            image = _generateArrow(arrowSet["up"], abs(delta[0]) + 1, pieceSize).transpose(Image.ROTATE_270)
            if delta[0] < 0:
                image = image.transpose(Image.ROTATE_180)
                _, _, _, alpha = image.split()
                Image.Image.paste(board, image, (target_x, target_y), alpha)
            else:
                _, _, _pass, alpha = image.split()
                Image.Image.paste(board, image, (start_x, start_y), alpha)
        elif abs(delta[0]) == abs(delta[1]):
            arrow = _generateArrow(arrowSet["up"], (math.sqrt((abs(delta[0]) + 0.5)**2 + (abs(delta[1]) + 0.5)**2)), pieceSize).rotate(45,expand=True)
            if delta[0] > 0 and delta[1] > 0:
                arrow = arrow.transpose(Image.ROTATE_180)
                _, _, _, alpha = arrow.split()
                Image.Image.paste(board, arrow, (start_x,start_y),alpha)
            elif delta[0] > 0 and delta[1] < 0:
                arrow = arrow.transpose(Image.ROTATE_270)
                _, _, _, alpha = arrow.split()
                Image.Image.paste(board, arrow, (start_x,target_y),alpha)
            elif delta[0] < 0 and delta[1] > 0:
                arrow = arrow.transpose(Image.ROTATE_90)
                _, _, _, alpha = arrow.split()
                Image.Image.paste(board, arrow, (target_x,start_y),alpha)
            elif delta[0] < 0 and delta[1] < 0:
                _, _, _, alpha = arrow.split()
                Image.Image.paste(board, arrow, (target_x,target_y),alpha)
                
        else:
            raise ValueError("Invalid arrow target: start(" +
                             str(start) + ") end(" + str(end) + ")")
    return board


"""
Takes given parameters and returns a PIL
image of the resulting chess position

Parameters
----------
fen: str
    Fen string representing a position
squarelength: int
    the length of one square on the board
    resulting board will be 8 * squarelength long
pieceSet: loadPiecesFolder
    the piece set, loaded using the loadPiecesFolder function
darkColor: str
    dark square color on the board
lightColor: str
    light square color on the board
flipped: boolean
    default = False
    Whether to flip to board, and render it from black's perspective

"""


def fenToImage(fen, squarelength, pieceSet, darkColor, lightColor, ArrowSet=None, Arrows=None, flipped=False, lastMove=None):
    board = Image.new("RGB", (squarelength * 8, squarelength * 8), lightColor)
    parsedBoard = FenParser(fen).parse()
    board = paintCheckerBoard(board, darkColor, lastMove)
    # Flip the list to reverse the position, and
    # render from black's POV.
    if flipped:
        parsedBoard.reverse()
    board = paintAllPieces(board, parsedBoard, pieceSet(board))
    if ArrowSet != None and Arrows != None:
        board = paintAllArrows(board, Arrows, ArrowSet(board))
    return board
