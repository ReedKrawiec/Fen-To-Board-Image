# FenToBoardImage

**FenToBoardImage** takes a FEN string representing a chess position and renders a PIL image of the resulting board.

## Features

- Convert any FEN string to a chess board image
- Customizable board colors (light and dark squares)
- Custom piece sets support
- Arrow overlays for move visualization
- Coordinate display options (ranks and files)
- Board flipping for black's perspective
- Highlighted squares support

## Quick Example

```python
from fentoboardimage import fen_to_image, load_pieces_folder

board = fen_to_image(
    fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    square_length=100,
    piece_set=load_pieces_folder("path/to/pieces"),
    dark_color="#79a65d",
    light_color="#daf2cb",
)

board.save("chess_board.png")
```

## Installation

```bash
pip install fentoboardimage
```

Or using UV:

```bash
uv add fentoboardimage
```

## License

This project is licensed under the GPL-3.0 License.
