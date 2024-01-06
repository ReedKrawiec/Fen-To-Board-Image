
<div align="center">
  <img src="https://raw.githubusercontent.com/reedkrawiec/fenToBoardImage/main/documentation/logo.png" />
</div>

# About

fentoboardimage takes a Fen string representing a Chess position, and renders a PIL image of the resulting position.

# Examples

Examples can be found under the `examples` folder in this repository. 
Further examples can be found within `tests/test.py`

###  You can customize:
- the size and color of the board
- piece sprites
- black or white perspective
- Board highlighting for last move
- Arrows

# Installation

Install the package using pip
```
$ pip install fentoboardimage
```

Then import the fenToImage and loadPiecesFolder functions and use them as follows:
```
from fentoboardimage import fenToImage, loadPiecesFolder

boardImage = fenToImage(
	fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
	squarelength=100,
	pieceSet=loadPiecesFolder("./pieces"),
	darkColor="#D18B47",
	lightColor="#FFCE9E"
)
```

In order to load a piece set, the pieces must follow this file structure, and must be a .png:
```
-piece_set_name
  -white
    - Knight.png
    - Rook.png
    - Pawn.png
    - Bishop.png
    - Queen.png
    - King.png
  -black
    - Knight.png
    - Rook.png
    - Pawn.png
    - Bishop.png
    - Queen.png
    - King.png
```

# Usage

The `fenToImage` function has these parameters:

- fen: `str`

	  Fen string representing a position

- squarelength: `int`

	  The length of one square on the board. Resulting board will be 8 * squarelength long

- pieceSet: `loadPiecesFolder`

	  the piece set, loaded using the `loadPiecesFolder` function

	- The loadPiecesFolder function has two parameters:

       path: `str`

          Loads piece set located at the path provided.

      cache: `boolean`

          Whether to internally cache the piece pngs to avoid reloading

- darkColor: `str`

	  dark square color on the board

- lightColor: `str`

	  light square color on the board

- flipped: `boolean` default = False

	  Whether to flip to board, and render it from black's perspective

- ArrowSet: `loadArrowsFolder()`

	  the arrow set, loaded using the `loadArrowsFolder` function

	- The loadArrowsFolder function has two parameters:

      - path: `str`

	        Loads arrow set located at the path provided.

	  - cache: `boolean`

	        Whether to internally cache the arrow pngs to avoid reloading

- Arrows: `list[(str,str)]`

	  A list of lists containing coordinates to place arrows. In the format
	  of [start, end] using standard chess notation for the squares.
- lastMove: `dict`
	
	  A dictionary containing the fields `before`, `after`, `darkColor` and `lightColor`. 
	  `before` and `after` using standard chess notation for the squares, and `darkColor`
	  and `lightColor` should be hex strings.

- coordinates: `dict`
     
      A dictionary containing the fields "font", "size", "darkColor", "lightColor", "positionFn",
      "padding", and "outsideBoardColor"
	   
	 - font: `loadFontFile()`
       
           The font file to use for coordinates, load using the loadFontFile function, with the
           file path to the ttf file or bitmap font file as its sole argument. 
   - size: int

         The font size for the coordinate
   - darkColor: `str`
    
         The color of the coordinate for dark squares
   -  lightColor: `str`
        
          The color of the coordinate for light squares
   -  posititionFn: `CoordinatePositionFn["outBorder"]` | `CoordinatePositionFn["innerBorder"]` | `CoordinatePositionFn["everySquare"]` | `function`
   
          The function used to determine what characters to draw and where for each square
          on the board. Can either be one of the three predefined functions from the
          CoordinatePositionFn dict, or a custom function. See the definitions for the
          builtin functions in "fentoboardimage/Coordinates.py" for examples to follow when
          writing a custom position fn.
   - padding: `int`
   
		 The padding between the square's edge and the resulting placement
		 of the coordinate character 
   - outsideBorderColor: `str` optional
   
         What color to paint the background if the coordinates end up outside the board
    

# Dependencies
- [Pillow](https://pypi.org/project/Pillow/)

