from PIL import ImageDraw
from PIL import Image
import math
from .Utils import flippedCheck, indicesToSquare


def OuterBorderFn(coordinate, squareOrigin, squarelength, font, flipped, padding):
    collection = []
    padding = padding if padding != None else 0

    if flippedCheck(flipped, coordinate[0], "a", "h"):
        size = font.getsize(coordinate[1])
        width, height = size
        collection.append({
            "coordinate": (squareOrigin[0] - padding - width, squareOrigin[1] + squarelength/2 - height/2),
            "text": coordinate[1]
        })
    if flippedCheck(flipped, coordinate[0], "h", "a"):
        size = font.getsize(coordinate[1])
        width, height = size
        collection.append({
            "coordinate": (squareOrigin[0] + padding + squarelength, squareOrigin[1] + squarelength/2 - height/2),
            "text": coordinate[1]})
    if flippedCheck(flipped, coordinate[1], "1", "8"):
        size = font.getsize(coordinate[0])
        width, height = size
        collection.append({
            "coordinate": (squareOrigin[0] + squarelength/2 - width/2, squareOrigin[1] + squarelength + padding),
            "text": coordinate[0]
        })
    if flippedCheck(flipped, coordinate[1], "8", "1"):
        size = font.getsize(coordinate[0])
        width, height = size
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
        size = font.getsize(coordinate[0])
        width, height = size
        collection.append({
            "coordinate": (squareOrigin[0] + squarelength - width - padding, squareOrigin[1] + squarelength - height - padding),
            "text": coordinate[0]
        })
    return collection


def EverySquare(coordinate, squareOrigin, squarelength, font, flipped, padding):
    size = font.getsize(coordinate[0])
    width, height = size
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


CoordinatePositionFn = {
    "outerBorder": OuterBorderFn,
    "innerBorder": InnerBorderFn,
    "everySquare": EverySquare
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
                    size = font.getsize(text["text"])
                    width, height = size
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
