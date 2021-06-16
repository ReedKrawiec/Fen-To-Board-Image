<div align="center">
  <img src="https://raw.githubusercontent.com/reedkrawiec/fenToBoardImage/main/documentation/logo.png" />
</div>

# About

FenToBoardImage takes a Fen string representing a Chess position, and renders a PIL image of the resulting position.

###  You can customize:
- the size and color of the board
- piece sprites
- black or white perspective

# Installation

Install the package using pip
```
$ pip install fenToBoardImage
```

Then import the fenToImage and loadPiecesFolder functions and use them as follows:
```
from fenToBoardImage import fenToImage, loadPiecesFolder

boardImage = fenToImage(
	fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
	squarelength=100,
	pieceSet=loadPiecesFolder("./pieces"),
	darkColor="#D18B47",
	lightColor="#FFCE9E"
)
```
# Usage

The fenToBoardImage has these parameters:

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

The loadPiecesFolder has one parameter:

path: str

	Loads piece set located at the path provided.


# Dependencies
- [Pillow](https://pypi.org/project/Pillow/)