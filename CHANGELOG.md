# Changelog

All notable changes to this project will be documented in this file.

## [1.3.0] - 2026-01-01

### Added

- **Coordinate drawing support** - Display file letters and rank numbers on the board
  - Three built-in position functions: `standard`, `every_square`, `along_outer_rim`
  - Custom position functions supported for full control
  - Works with flipped boards
- **New snake_case API** - More Pythonic function names
  - `fen_to_image()` (replaces `fenToImage`)
  - `load_pieces_folder()` (replaces `loadPiecesFolder`)
  - `load_arrows_folder()` (replaces `loadArrowsFolder`)
  - `load_font_file()` (replaces `loadFontFile`)
  - `coordinate_position_fn` dict (replaces `CoordinatePositionFn`)
- **Utility functions exposed** for advanced usage
  - `square_to_indices()` - Convert algebraic notation to board indices
  - `indices_to_square()` - Convert board indices to algebraic notation
  - `flip_coord_tuple()` - Flip coordinates for black's perspective
- **FenParser class** now publicly exported
- **Type hints** throughout the codebase
- **Piece and arrow image caching** for improved performance
- **New example files** demonstrating all features:
  - `coordinates_example.py` - Coordinate notation styles
  - `complete_example.py` - Full-featured example
  - `custom_colors_example.py` - Board color customization
  - `flipped_board_example.py` - Black's perspective
  - `last_move_example.py` - Move highlighting
  - `complex_position_example.py` - Advanced positions

### Changed

- **Migrated from Poetry to UV** for dependency management
- **Build system changed to hatchling** (PEP 517/518 compliant)
- **GitHub Actions updated** to use UV and test matrix (Python 3.8-3.13)

### Deprecated

- camelCase function names (`fenToImage`, `loadPiecesFolder`, etc.) - still work but prefer snake_case
- `CoordinatePositionFn` dict - use `coordinate_position_fn` instead

### Removed

- Poetry configuration and lock file

## [1.2.0] - Previous release

- Square highlighting with custom colors
- Last move highlighting improvements
- Arrow drawing support
