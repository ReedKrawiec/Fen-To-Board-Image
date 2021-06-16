#!/usr/bin/env python

from PIL import Image
from PIL import ImageDraw
import os
# http://wordaligned.org/articles/drawing-chessboards
# https://github.com/tlehman/fenparser

from unittest import TestCase
from itertools import chain
import re

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
    assert fp.parse_rank(rank8) == ["r","n","b","q","k","b","n","r"]
    assert fp.parse_rank(rank7) == ["p","p","p","p","p","p","p","p"]
    assert fp.parse_rank(rank6) == [" "," "," "," "," "," "," "," "]


  def test_parse_starting_position(self):
    start_pos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    fp = FenParser(start_pos)
    print(fp.parse())
    assert len(fp.parse()) == 8
    assert fp.parse() == [["r","n","b","q","k","b","n","r"],
                          ["p","p","p","p","p","p","p","p"],
                          [" "," "," "," "," "," "," "," "],
                          [" "," "," "," "," "," "," "," "],
                          [" "," "," "," "," "," "," "," "],
                          [" "," "," "," "," "," "," "," "],
                          ["P","P","P","P","P","P","P","P"],
                          ["R","N","B","Q","K","B","N","R"]]

def paintCheckerBoard(board, darkColor):
    height, width = board.size
    draw = ImageDraw.Draw(board)
    if height != width:
        raise Exception("Height unequal to width")
    for y in range(0, 8):
        for x in range(0, 8, 2):
            # Four pairs of dark then light must be painted per row
            squareSize = width/8
            firstIsColored = y % 2 == 0
            startSquareOffset = 1 if firstIsColored else 0
            start = ((x + startSquareOffset) * squareSize, y * squareSize)
            end = ((x + startSquareOffset) * squareSize +
                   squareSize - 1, y * squareSize + squareSize - 1)
            draw.rectangle([start, end], darkColor)
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
def fenToImage(fen, squarelength, pieceSet, darkColor, lightColor, flipped=False):
    board = Image.new("RGB", (squarelength * 8, squarelength * 8), lightColor)
    parsedBoard = FenParser(fen).parse()
    board = paintCheckerBoard(board, darkColor)
    if flipped:
        parsedBoard.reverse()
    board = paintAllPieces(board, parsedBoard, pieceSet(board))
    return board


