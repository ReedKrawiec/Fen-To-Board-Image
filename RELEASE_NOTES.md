# v1.3.0 Release Notes

## Highlights

**Coordinate Drawing** - Display file letters (a-h) and rank numbers (1-8) on your chess boards with three built-in styles or create your own custom positioning.

**New Pythonic API** - All functions now use snake_case naming (`fen_to_image`, `load_pieces_folder`, etc.) with full backwards compatibility for existing code.

**Performance Improvements** - Piece and arrow images are now cached, significantly speeding up generation of multiple boards.

## New Features

### Coordinate Display
```python
from fentoboardimage import fen_to_image, load_pieces_folder, load_font_file, coordinate_position_fn

board = fen_to_image(
    fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    square_length=100,
    piece_set=load_pieces_folder("./pieces"),
    dark_color="#D18B47",
    light_color="#FFCE9E",
    coordinates={
        "font": load_font_file("./fonts/Roboto-Bold.ttf"),
        "size": 14,
        "dark_color": "#8B4513",
        "light_color": "#FFFFFF",
        "position_fn": coordinate_position_fn["standard"]  # or "every_square", "along_outer_rim"
    }
)
```

### Snake Case API
| New (Preferred)       | Old (Still Works)     |
|-----------------------|-----------------------|
| `fen_to_image()`      | `fenToImage()`        |
| `load_pieces_folder()`| `loadPiecesFolder()`  |
| `load_arrows_folder()`| `loadArrowsFolder()`  |
| `load_font_file()`    | `loadFontFile()`      |

### Utility Functions
- `square_to_indices("e4")` → `(4, 4)`
- `indices_to_square((4, 4))` → `"e4"`
- `flip_coord_tuple((0, 0))` → `(7, 7)`

## Development Changes

- Migrated from Poetry to [UV](https://docs.astral.sh/uv/) for dependency management
- Build system changed to hatchling (PEP 517/518)
- CI now tests Python 3.8, 3.9, 3.10, 3.11, 3.12, and 3.13

## Installation

```bash
pip install fentoboardimage==1.3.0
```

## Full Changelog

See [CHANGELOG.md](./CHANGELOG.md) for complete details.
