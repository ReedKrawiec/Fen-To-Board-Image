# FEN Parser

The FEN parser module provides the `FenParser` class for parsing FEN (Forsyth-Edwards Notation) strings into board representations.

## FenParser Class

::: fentoboardimage.FenParser
    options:
      members:
        - __init__
        - parse
        - parse_rank
        - expand_or_noop
        - expand
        - flatten

## FEN String Format

FEN (Forsyth-Edwards Notation) is a standard notation for describing chess positions. A FEN string consists of 6 space-separated fields:

1. **Piece placement**: Ranks separated by `/`, from rank 8 to rank 1
2. **Active color**: `w` for white, `b` for black
3. **Castling availability**: `KQkq` or `-`
4. **En passant target square**: e.g., `e3` or `-`
5. **Halfmove clock**: Number of halfmoves since last capture or pawn advance
6. **Fullmove number**: Starts at 1, incremented after black's move

### Piece Notation

| Character | Piece |
|-----------|-------|
| `K` / `k` | King (white / black) |
| `Q` / `q` | Queen (white / black) |
| `R` / `r` | Rook (white / black) |
| `B` / `b` | Bishop (white / black) |
| `N` / `n` | Knight (white / black) |
| `P` / `p` | Pawn (white / black) |

### Examples

**Starting position:**
```
rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
```

**Empty board:**
```
8/8/8/8/8/8/8/8 w - - 0 1
```

**Sicilian Defense (after 1.e4 c5):**
```
rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2
```

## Usage Example

```python
from fentoboardimage import FenParser

# Parse starting position
parser = FenParser("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
board = parser.parse()

# board is a list of 8 lists (ranks), each containing 8 strings (pieces)
print(board[0])  # ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
print(board[7])  # ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']

# Empty squares are represented by ' ' (space)
empty_board = FenParser("8/8/8/8/8/8/8/8 w - - 0 1").parse()
print(empty_board[0])  # [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
```
