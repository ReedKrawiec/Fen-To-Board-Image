# Main API

The main module provides functions for rendering chess board images from FEN strings.

## Core Functions

::: fentoboardimage.fen_to_image

::: fentoboardimage.load_pieces_folder

::: fentoboardimage.load_arrows_folder

::: fentoboardimage.load_font_file

## Coordinate Position Functions

These functions control how coordinate labels (a-h, 1-8) are displayed on the board.
Pass one of these to the `position_fn` key in the `coordinates` parameter of `fen_to_image`.

### Importing

```python
from fentoboardimage import (
    coordinate_position_fn,  # Dictionary of all position functions
    standard,                # Or import individual functions
    every_square,
    along_outer_rim,
)
```

### Usage

Use the dictionary lookup:
```python
coordinates={
    "font": load_font_file("fonts/Arial.ttf"),
    "size": 18,
    "dark_color": "#eeeed2",
    "light_color": "#769656",
    "position_fn": coordinate_position_fn["standard"],
}
```

Or use the function directly:
```python
from fentoboardimage import standard

coordinates={
    "font": load_font_file("fonts/Arial.ttf"),
    "size": 18,
    "dark_color": "#eeeed2",
    "light_color": "#769656",
    "position_fn": standard,
}
```

### Available Functions

#### `standard`

The chess.com/Lichess style. Places rank numbers (1-8) in the top-left corner of
a-file squares and file letters (a-h) in the bottom-right corner of 1st rank squares.
This is the most common coordinate style used by major chess websites.

```
  ┌────┬────┬────┬────┬────┬────┬────┬────┐
8 │    │    │    │    │    │    │    │    │
  ├────┼────┼────┼────┼────┼────┼────┼────┤
7 │    │    │    │    │    │    │    │    │
  ├────┼────┼────┼────┼────┼────┼────┼────┤
  ...
  ├────┼────┼────┼────┼────┼────┼────┼────┤
1 │    │   a│   b│   c│   d│   e│   f│   g│   h│
  └────┴────┴────┴────┴────┴────┴────┴────┘
```

::: fentoboardimage.standard

#### `every_square`

Shows the full algebraic notation (e.g., "e4", "a1") centered on every square.
Useful for learning chess notation or debugging.

```
  ┌────┬────┬────┬────┬────┬────┬────┬────┐
  │ a8 │ b8 │ c8 │ d8 │ e8 │ f8 │ g8 │ h8 │
  ├────┼────┼────┼────┼────┼────┼────┼────┤
  │ a7 │ b7 │ c7 │ d7 │ e7 │ f7 │ g7 │ h7 │
  ├────┼────┼────┼────┼────┼────┼────┼────┤
  ...
```

::: fentoboardimage.every_square

#### `along_outer_rim`

Places file letters (a-h) centered along the bottom edge and rank numbers (1-8)
centered along the left edge. Only edge squares display coordinates.

```
     a    b    c    d    e    f    g    h
  ┌────┬────┬────┬────┬────┬────┬────┬────┐
8 │    │    │    │    │    │    │    │    │
  ├────┼────┼────┼────┼────┼────┼────┼────┤
7 │    │    │    │    │    │    │    │    │
  ...
```

::: fentoboardimage.along_outer_rim
