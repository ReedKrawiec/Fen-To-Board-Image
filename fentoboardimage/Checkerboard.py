from PIL import ImageDraw


def paintCheckerBoard(board, darkColor, lastMove=None, highlighting=None):
    height, width = board.size
    draw = ImageDraw.Draw(board)
    if height != width:
        # Require a square board, any stretching / transformations
        # should be handled afterwards through PIL
        raise Exception("Height unequal to width")

    def getRectanglePositionTuples(tup):
        return (((tup[0] + startSquareOffset) * squareSize, tup[1] * squareSize),
                ((tup[0] + startSquareOffset) * squareSize + squareSize - 1, tup[1] * squareSize + squareSize - 1))

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

            squareSize: int = width/8

            firstIsColored = y % 2 == 0
            # If the first square is colored, offset
            # the pattern of dark then light by one
            startSquareOffset = 1 if firstIsColored else 0
            draw.rectangle(getRectanglePositionTuples((x, y)), darkColor)
    if lastMove != None:
        beforeColor: str = lastMove["darkColor"]
        afterColor: str = lastMove["darkColor"]
        if isLightSquare(lastMove["before"]):
            beforeColor = lastMove["lightColor"]
        if isLightSquare(lastMove["after"]):
            afterColor = lastMove["lightColor"]
        draw.rectangle(getRectanglePositionTuples(
            lastMove["before"]), beforeColor)
        draw.rectangle(getRectanglePositionTuples(
            lastMove["after"]), afterColor)
    if highlighting != None:
        colors = highlighting["colors"]
        squares = highlighting["squares"]
        for square in squares:
            selectedColor = squares[square]
            colorDef = colors[selectedColor]
            draw.rectangle(getRectanglePositionTuples(
                square), colorDef["light"] if isLightSquare(square) else colorDef["dark"])
    return board
