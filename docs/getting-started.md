# Getting Started

This guide will help you get started with FenToBoardImage.

## Installation

### Using pip

```bash
pip install fentoboardimage
```

### Using UV

```bash
uv add fentoboardimage
```

## Asset Setup

FenToBoardImage requires image assets for pieces, and optionally for arrows and fonts.
All paths are **relative to your current working directory** (where you run your script).

### Recommended Project Structure

```
your_project/
├── main.py              # Your script
├── pieces/              # Piece images
│   ├── white/
│   │   ├── King.png
│   │   ├── Queen.png
│   │   ├── Rook.png
│   │   ├── Bishop.png
│   │   ├── Knight.png
│   │   └── Pawn.png
│   └── black/
│       ├── King.png
│       ├── Queen.png
│       ├── Rook.png
│       ├── Bishop.png
│       ├── Knight.png
│       └── Pawn.png
├── arrows/              # Arrow images (optional)
│   ├── Knight.png       # L-shaped arrow sprite
│   └── Up.png           # Straight arrow sprite
└── fonts/               # Font files (optional)
    └── Arial.ttf
```

### Piece Sets

Piece sets require a folder with `white/` and `black/` subfolders, each containing 6 PNG files:

| File | Description |
|------|-------------|
| `King.png` | King piece |
| `Queen.png` | Queen piece |
| `Rook.png` | Rook piece |
| `Bishop.png` | Bishop piece |
| `Knight.png` | Knight piece |
| `Pawn.png` | Pawn piece |

```python
from fentoboardimage import load_pieces_folder

# Path relative to current working directory
piece_set = load_pieces_folder("pieces")

# Or use absolute path
piece_set = load_pieces_folder("/path/to/your/pieces")
```

### Arrow Sets (Optional)

Arrow sets require a folder with two PNG sprite files:

| File | Description |
|------|-------------|
| `Knight.png` | L-shaped arrow for knight moves |
| `Up.png` | Straight arrow sprite (head, body, tail stacked vertically) |

```python
from fentoboardimage import load_arrows_folder

arrow_set = load_arrows_folder("arrows")
```

#### Knight.png Specification

The knight arrow should be an L-shaped arrow with **3:2 aspect ratio** (width:height).

- **Dimensions**: 3 units wide × 2 units tall (e.g., 300×200 px or 150×100 px)
- **Direction**: Arrow points from **bottom-right to top-left**
- **Tail**: Starts at the bottom-right corner
- **Head**: Points toward the top-left corner

```
┌─────────────────────┐
│  ◄───────────────┐  │  ← arrowhead pointing left
│                  │  │
│                  │  │  ← tail at bottom-right
└─────────────────────┘
     3 units wide
```

The library rotates and flips this base image to create all 8 knight move directions.

#### Up.png Specification

The straight arrow should be a vertical arrow with **1:3 aspect ratio** (width:height).

- **Dimensions**: 1 unit wide × 3 units tall (e.g., 100×300 px)
- **Direction**: Arrow points **upward**
- **Structure** (top to bottom):
  1. **Head** (1×1): Arrowhead/triangle pointing up
  2. **Body** (1×1): Straight shaft (stretched for longer arrows)
  3. **Tail** (1×1): Rounded end or base

```
┌───┐
│ ▲ │  ← head (arrowhead)
├───┤
│ │ │  ← body (stretchable)
├───┤
│ ○ │  ← tail (rounded end)
└───┘
```

The library crops these three sections and reassembles them to create arrows of any length.

### Fonts (Optional)

For coordinates, provide a path to a TrueType font file (`.ttf`):

```python
from fentoboardimage import load_font_file

font = load_font_file("fonts/Arial.ttf")
```

### Path Resolution Examples

If your script is at `/home/user/chess/main.py` and you run it from `/home/user/chess/`:

```python
# These paths resolve relative to /home/user/chess/
load_pieces_folder("pieces")        # → /home/user/chess/pieces/
load_pieces_folder("./pieces")      # → /home/user/chess/pieces/
load_pieces_folder("assets/pieces") # → /home/user/chess/assets/pieces/
```

If you run the same script from a different directory (e.g., `/home/user/`):

```python
# Paths resolve relative to /home/user/ (your cwd)
load_pieces_folder("pieces")        # → /home/user/pieces/ (probably wrong!)

# Use absolute paths to avoid issues
load_pieces_folder("/home/user/chess/pieces")  # Always works
```

**Tip:** For portable scripts, use `__file__` to get paths relative to your script:

```python
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
pieces_path = os.path.join(script_dir, "pieces")

piece_set = load_pieces_folder(pieces_path)
```

## Basic Usage

### Rendering a Board

```python
from fentoboardimage import fen_to_image, load_pieces_folder

# Starting position
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

board = fen_to_image(
    fen=fen,
    square_length=100,
    piece_set=load_pieces_folder("pieces"),
    dark_color="#79a65d",
    light_color="#daf2cb",
)

# Save to file
board.save("board.png")

# Or display
board.show()
```

### Customizing Colors

```python
board = fen_to_image(
    fen=fen,
    square_length=100,
    piece_set=load_pieces_folder("pieces"),
    dark_color="#b58863",    # Brown dark squares
    light_color="#f0d9b5",   # Tan light squares
)
```

### Flipping the Board

To view from black's perspective:

```python
board = fen_to_image(
    fen=fen,
    square_length=100,
    piece_set=load_pieces_folder("pieces"),
    dark_color="#79a65d",
    light_color="#daf2cb",
    flipped=True,
)
```

### Adding Highlighted Squares

```python
board = fen_to_image(
    fen=fen,
    square_length=100,
    piece_set=load_pieces_folder("pieces"),
    dark_color="#79a65d",
    light_color="#daf2cb",
    highlighting={
        "dark": "#aaa23a",   # Dark square highlight color
        "light": "#cdd26a",  # Light square highlight color
        "squares": ["e4", "e5"],  # Squares to highlight
    },
)
```

## Arrow Overlays

You can add arrows to show moves or annotations.

### Loading Arrow Assets

```python
from fentoboardimage import load_arrows_folder

arrow_set = load_arrows_folder("path/to/arrows")
```

### Drawing Arrows

```python
from fentoboardimage import fen_to_image, load_pieces_folder, load_arrows_folder

board = fen_to_image(
    fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    square_length=100,
    piece_set=load_pieces_folder("pieces"),
    arrow_set=load_arrows_folder("arrows"),
    dark_color="#79a65d",
    light_color="#daf2cb",
    arrows=[["e2", "e4"], ["d7", "d5"]],
)
```

## Coordinates

Display rank and file labels on the board:

```python
from fentoboardimage import (
    fen_to_image,
    load_pieces_folder,
    load_font_file,
    coordinate_position_fn,
)

board = fen_to_image(
    fen=fen,
    square_length=100,
    piece_set=load_pieces_folder("pieces"),
    dark_color="#769656",
    light_color="#eeeed2",
    coordinates={
        "font": load_font_file("fonts/Arial.ttf"),
        "size": 18,
        "dark_color": "#eeeed2",   # Text color on dark squares
        "light_color": "#769656",  # Text color on light squares
        "position_fn": coordinate_position_fn["standard"],
    },
)
```

### Coordinate Styles

| Style | Description |
|-------|-------------|
| `"standard"` | Chess.com/Lichess style: rank numbers in corner of a-file, file letters in corner of 1st rank |
| `"every_square"` | Full notation (e.g., "e4") centered on every square |
| `"along_outer_rim"` | Coordinates centered along board edges |

You can also import the functions directly:

```python
from fentoboardimage import standard, every_square, along_outer_rim

coordinates={
    "font": load_font_file("fonts/Arial.ttf"),
    "size": 18,
    "dark_color": "#eeeed2",
    "light_color": "#769656",
    "position_fn": standard,  # Use function directly
}
```
