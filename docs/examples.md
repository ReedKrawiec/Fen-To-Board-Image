# Examples

This page contains practical examples for common use cases.

## Basic Board Rendering

### Standard Starting Position

```python
from fentoboardimage import fen_to_image, load_pieces_folder

board = fen_to_image(
    fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    square_length=100,
    piece_set=load_pieces_folder("pieces"),
    dark_color="#79a65d",
    light_color="#daf2cb",
)

board.save("starting_position.png")
```

### Famous Positions

#### Scholar's Mate

```python
from fentoboardimage import fen_to_image, load_pieces_folder

# Scholar's Mate - White wins
fen = "r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4"

board = fen_to_image(
    fen=fen,
    square_length=100,
    piece_set=load_pieces_folder("pieces"),
    dark_color="#b58863",
    light_color="#f0d9b5",
)

board.save("scholars_mate.png")
```

#### Italian Game

```python
from fentoboardimage import fen_to_image, load_pieces_folder

# Italian Game - Giuoco Piano
fen = "r1bqk1nr/pppp1ppp/2n5/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4"

board = fen_to_image(
    fen=fen,
    square_length=100,
    piece_set=load_pieces_folder("pieces"),
    dark_color="#769656",
    light_color="#eeeed2",
)

board.save("italian_game.png")
```

## Board Perspectives

### Black's Perspective

```python
from fentoboardimage import fen_to_image, load_pieces_folder

board = fen_to_image(
    fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    square_length=100,
    piece_set=load_pieces_folder("pieces"),
    dark_color="#79a65d",
    light_color="#daf2cb",
    flipped=True,
)

board.save("black_perspective.png")
```

## Move Visualization

### Highlighting Squares

Highlight the squares involved in the last move:

```python
from fentoboardimage import fen_to_image, load_pieces_folder

# Position after 1.e4
fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"

board = fen_to_image(
    fen=fen,
    square_length=100,
    piece_set=load_pieces_folder("pieces"),
    dark_color="#79a65d",
    light_color="#daf2cb",
    highlighting={
        "dark": "#aaa23a",
        "light": "#cdd26a",
        "squares": ["e2", "e4"],  # From and to squares
    },
)

board.save("highlighted_move.png")
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
    arrows=[
        ["e2", "e4"],  # King's pawn opening
        ["d2", "d4"],  # Queen's pawn opening
    ],
)

board.save("opening_arrows.png")
```

## Coordinates

### Inner Border Coordinates

Coordinates displayed inside the board on the edges:

```python
from PIL import ImageFont
from fentoboardimage import fen_to_image, load_pieces_folder

font = ImageFont.truetype("arial.ttf", 16)

board = fen_to_image(
    fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    square_length=100,
    piece_set=load_pieces_folder("pieces"),
    dark_color="#79a65d",
    light_color="#daf2cb",
    coordinates={
        "font": font,
        "dark_color": "#4a7a3d",
        "light_color": "#c4e8b4",
        "position_fn": "inner_border",
    },
)

board.save("inner_coordinates.png")
```

### Outer Border Coordinates

Coordinates displayed in a border outside the board:

```python
from PIL import ImageFont
from fentoboardimage import fen_to_image, load_pieces_folder

font = ImageFont.truetype("arial.ttf", 20)

board = fen_to_image(
    fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    square_length=100,
    piece_set=load_pieces_folder("pieces"),
    dark_color="#79a65d",
    light_color="#daf2cb",
    coordinates={
        "font": font,
        "dark_color": "#000000",
        "light_color": "#000000",
        "position_fn": "outer_border",
    },
)

board.save("outer_coordinates.png")
```

## Batch Processing

### Generating Multiple Boards

```python
from fentoboardimage import fen_to_image, load_pieces_folder

positions = {
    "starting": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "sicilian": "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2",
    "french": "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2",
    "caro_kann": "rnbqkbnr/pp1ppppp/2p5/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2",
}

# Load pieces once for efficiency (caching is enabled by default)
piece_set = load_pieces_folder("pieces")

for name, fen in positions.items():
    board = fen_to_image(
        fen=fen,
        square_length=100,
        piece_set=piece_set,
        dark_color="#79a65d",
        light_color="#daf2cb",
    )
    board.save(f"{name}.png")
```

## Custom Styling

### Chess.com Style

```python
from fentoboardimage import fen_to_image, load_pieces_folder

board = fen_to_image(
    fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    square_length=100,
    piece_set=load_pieces_folder("pieces"),
    dark_color="#769656",
    light_color="#eeeed2",
)
```

### Lichess Style

```python
from fentoboardimage import fen_to_image, load_pieces_folder

board = fen_to_image(
    fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    square_length=100,
    piece_set=load_pieces_folder("pieces"),
    dark_color="#b58863",
    light_color="#f0d9b5",
)
```

### Blue Theme

```python
from fentoboardimage import fen_to_image, load_pieces_folder

board = fen_to_image(
    fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    square_length=100,
    piece_set=load_pieces_folder("pieces"),
    dark_color="#4b7399",
    light_color="#eae9d2",
)
```
