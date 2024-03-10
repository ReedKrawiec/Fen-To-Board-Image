from typing import Tuple, Union, cast
from typing_extensions import Literal, TypedDict
from PIL import ImageDraw, ImageFont
from PIL import Image
import math
from .Utils import flippedCheck, indicesToSquare

Coordinate = Literal[
    "a1", "a2", "a3", "a4", "a5", "a6","a7", "a8",
    "b1", "b2", "b3", "b4", "b5", "b6","b7", "b8",
    "c1", "c2", "c3", "c4", "c5", "c6","c7", "c8",
    "d1", "d2", "d3", "d4", "d5", "d6","d7", "d8",
    "e1", "e2", "e3", "e4", "e5", "e6","e7", "e8",
    "f1", "f2", "f3", "f4", "f5", "f6","f7", "f8",
    "g1", "g2", "g3", "g4", "g5", "g6","g7", "g8",
    "h1", "h2", "h3", "h4", "h5", "h6","h7", "h8",
]

def get_size(font, s):
    left, top, right, bottom = font.getbbox(s)
    width, height = right - left, bottom
    return width, height

class PositionFnType:
    coordinate: Coordinate
    squareOrigin: Tuple[int, int]
    squarelength: int
    font: Union[ImageFont.ImageFont, ImageFont.FreeTypeFont]
    flipped: bool
    padding: int

def OuterBorderFn(coordinate, squareOrigin, squarelength, font, flipped, padding):
    collection = []
    padding = padding if padding != None else 0

    if flippedCheck(flipped, coordinate[0], "a", "h"):
        width, height = get_size(font, coordinate[1])
        collection.append({
            "coordinate": (squareOrigin[0] - padding - width, squareOrigin[1] + squarelength/2 - height/2),
            "text": coordinate[1]
        })
    if flippedCheck(flipped, coordinate[0], "h", "a"):
        width, height = get_size(font, coordinate[1])
        collection.append({
            "coordinate": (squareOrigin[0] + padding + squarelength, squareOrigin[1] + squarelength/2 - height/2),
            "text": coordinate[1]})
    if flippedCheck(flipped, coordinate[1], "1", "8"):
        width, height = get_size(font, coordinate[0])
        collection.append({
            "coordinate": (squareOrigin[0] + squarelength/2 - width/2, squareOrigin[1] + squarelength + padding),
            "text": coordinate[0]
        })
    if flippedCheck(flipped, coordinate[1], "8", "1"):
        width, height = get_size(font, coordinate[0])
        collection.append({
            "coordinate": (squareOrigin[0] + squarelength/2 - width/2, squareOrigin[1] - height - padding),
            "text": coordinate[0]
        })
    return collection


def InnerBorderFn(coordinate, squareOrigin, squarelength, font, flipped, padding):
    collection = []
    padding = padding if padding != None else squarelength/20
    if flippedCheck(flipped, coordinate[0], "a", "h"):
        collection.append({
            "coordinate": (squareOrigin[0] + padding, squareOrigin[1] + padding),
            "text": coordinate[1]
        })
    if flippedCheck(flipped, coordinate[1], "1", "8"):
        width, height = get_size(font, coordinate[0])
        collection.append({
            "coordinate": (squareOrigin[0] + squarelength - width - padding, squareOrigin[1] + squarelength - height - padding),
            "text": coordinate[0]
        })
    return collection


def EverySquare(coordinate, squareOrigin, squarelength, font, flipped, padding):
    width, height = get_size(font, coordinate[0])
    padding = padding if padding != None else squarelength/20
    collection = []
    collection.append({
        "coordinate": (squareOrigin[0] + padding, squareOrigin[1] + padding),
        "text": coordinate[1]
    })
    collection.append({
        "coordinate": (squareOrigin[0] + squarelength - width - padding, squareOrigin[1] + squarelength - height - padding),
        "text": coordinate[0]
    })
    return collection

CoordinatePositionFn= {
    "outerBorder": cast(PositionFnType, OuterBorderFn),
    "innerBorder": cast(PositionFnType, InnerBorderFn),
    "everySquare": cast(PositionFnType, EverySquare)
}


def paintCoordinateOverlay(board, coordinates, squarelength, flipped):
    draw = ImageDraw.Draw(board)
    size = 1 if coordinates["size"] == None else coordinates["size"]
    font = coordinates["font"](size)
    padding = coordinates["padding"]
    dark = True
    offset = (
        0, 0) if "offset" not in coordinates else coordinates["offset"]
    textObjects = []
    maxX, minX, maxY, minY = squarelength * 8, 0, squarelength * 8, 0
    for x in range(0, 8):
        for y in range(0, 8):
            coordStr = indicesToSquare((x, y), flipped)
            locations = coordinates["positionFn"](
                coordStr, (x * squarelength + offset[0], y * squarelength + offset[1]), squarelength, font, flipped, padding)
            dark = not dark
            if locations != None:
                for text in locations:
                    textObjects.append({
                        "position": text["coordinate"],
                        "text": text["text"],
                        "fill": coordinates["darkColor" if dark else "lightColor"]
                    })
                    width, height = get_size(font, text["text"])
                    maxX = max(maxX, text["coordinate"][0] + width)
                    minX = min(minX, text["coordinate"][0])
                    maxY = max(maxY, text["coordinate"][1] + height)
                    minY = min(minY, text["coordinate"][1])
        dark = not dark
    paintOffset = (math.ceil(abs(minX)), math.ceil(abs(minY)))
    coordOverlayWidth, coordOverlayHeight = (
        math.ceil(maxX + paintOffset[0]), math.ceil(maxY + paintOffset[1]))
    coordOverlay = None
    if "outsideBoardColor" in coordinates:
        coordOverlay = Image.new(
            "RGBA", (coordOverlayWidth, coordOverlayHeight), coordinates["outsideBoardColor"])
    else:
        coordOverlay = Image.new(
            "RGBA", (coordOverlayWidth, coordOverlayHeight))
    coordOverlay.paste(board, paintOffset)
    draw = ImageDraw.Draw(coordOverlay)

    for text in textObjects:
        draw.text((text["position"][0] + paintOffset[0], text["position"][1] + paintOffset[1]),
                  text["text"], font=font, fill=text["fill"])
    return coordOverlay, paintOffset

