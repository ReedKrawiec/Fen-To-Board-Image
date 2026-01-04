#!/usr/bin/env python
"""Chess board image generation from FEN strings.

This module provides functions to render chess positions as PIL images.
It supports custom piece sets, board colors, arrows, move highlighting,
and coordinate notation.

Example:
    Basic usage to render a chess position:

    ```python
    from fentoboardimage import fen_to_image, load_pieces_folder
    board = fen_to_image(
        fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        square_length=100,
        piece_set=load_pieces_folder("./pieces"),
        dark_color="#D18B47",
        light_color="#FFCE9E"
    )
    board.save("chess_position.png")
    ```
"""

from __future__ import annotations

import math
import os
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    TypedDict,
    Union,
)

from PIL import Image, ImageDraw, ImageFont

from .fen_parser import FenParser

# Type aliases for better readability
FontLoaderWithSize = Callable[[int], Union[ImageFont.ImageFont, ImageFont.FreeTypeFont]]
"""A callable that takes a font size and returns a PIL font object."""

FontLoader = Callable[[str], FontLoaderWithSize]
"""A callable that takes a font path and returns a FontLoaderWithSize."""

FontType = Union[ImageFont.ImageFont, ImageFont.FreeTypeFont]
"""A PIL font object, either bitmap or TrueType."""

BoardPosition = Tuple[int, int]
"""A tuple representing (x, y) coordinates on the board (0-7, 0-7)."""

PieceImages = Dict[str, Image.Image]
"""A dictionary mapping piece characters to their PIL Image objects."""

ArrowImages = Dict[str, Image.Image]
"""A dictionary mapping arrow types to their PIL Image objects."""


class CoordinateFnReturnType(TypedDict):
    """Return type for coordinate position functions.

    Attributes:
        coordinate: The (x, y) pixel coordinates where the text should be drawn.
        text: The text to draw (e.g., "a", "1", "e4").
    """

    coordinate: Tuple[float, float]
    text: str


CoordinateFn = Callable[
    [str, Tuple[float, float], float, FontType],
    Union[List[CoordinateFnReturnType], None],
]
"""A function that determines where to place coordinate text on the board.

Args:
    coordinate: The algebraic notation of the square (e.g., "a1", "e4").
    square_origin: The (x, y) pixel coordinates of the square's top-left corner.
    square_length: The length of each square in pixels.
    font: The PIL font object to use for measuring text.

Returns:
    A list of CoordinateFnReturnType dictionaries, or None to skip this square.
"""


def along_outer_rim(
    coordinate: str,
    square_origin: Tuple[float, float],
    square_length: float,
    font: FontType,
) -> List[CoordinateFnReturnType]:
    """Place coordinates along the outer rim of the board.

    Shows file letters (a-h) along the bottom edge and rank numbers (1-8)
    along the left edge. Only edge squares display coordinates.

    Args:
        coordinate: The algebraic notation of the square (e.g., "a1").
        square_origin: The (x, y) pixel coordinates of the square's top-left corner.
        square_length: The length of each square in pixels.
        font: The PIL font object for text measurement.

    Returns:
        A list containing coordinate specifications for edge squares.
    """
    box = font.getbbox(coordinate[1])
    height = box[3] - box[1]
    width = box[2] - box[0]
    collection: List[CoordinateFnReturnType] = []
    # Show rank numbers on the a-file (left edge), centered vertically
    if coordinate[0] == "a":
        collection.append(
            {
                "coordinate": (
                    square_origin[0] + 5,
                    square_origin[1] + (square_length - height) / 2,
                ),
                "text": coordinate[1],
            }
        )
    # Show file letters on the 1st rank (bottom edge), centered horizontally
    if coordinate[1] == "1":
        collection.append(
            {
                "coordinate": (
                    square_origin[0] + (square_length - width) / 2,
                    square_origin[1] + square_length - height - 5,
                ),
                "text": coordinate[0],
            }
        )
    return collection


def every_square(
    coordinate: str,
    square_origin: Tuple[float, float],
    square_length: float,
    font: FontType,
) -> List[CoordinateFnReturnType]:
    """Place full coordinate notation on every square.

    Shows the complete algebraic notation (e.g., "e4", "a1") in the
    center of each square. Useful for learning or debugging.

    Args:
        coordinate: The algebraic notation of the square (e.g., "a1").
        square_origin: The (x, y) pixel coordinates of the square's top-left corner.
        square_length: The length of each square in pixels.
        font: The PIL font object for text measurement.

    Returns:
        A list containing a single coordinate specification with the full notation.
    """
    box = font.getbbox(coordinate)
    height = box[3] - box[1]
    width = box[2] - box[0]
    return [
        {
            "coordinate": (
                square_origin[0] + (square_length - width) / 2,
                square_origin[1] + (square_length - height) / 2,
            ),
            "text": coordinate,
        }
    ]


def standard(
    coordinate: str,
    square_origin: Tuple[float, float],
    square_length: float,
    font: FontType,
) -> List[CoordinateFnReturnType]:
    """Place coordinates in the corner of edge squares (chess.com/lichess style).

    This is the standard style used by most chess websites:
    - Rank numbers (1-8) appear in the top-left corner of a-file squares
    - File letters (a-h) appear in the bottom-right corner of 1st rank squares

    Args:
        coordinate: The algebraic notation of the square (e.g., "a1").
        square_origin: The (x, y) pixel coordinates of the square's top-left corner.
        square_length: The length of each square in pixels.
        font: The PIL font object for text measurement.

    Returns:
        A list of coordinate specifications. May contain 0, 1, or 2 items
        depending on whether the square is on the a-file and/or 1st rank.

    Example:
        For square "a1", returns both the rank number "1" and file letter "a".
        For square "a4", returns only the rank number "4".
        For square "e1", returns only the file letter "e".
        For square "e4", returns an empty list.
    """
    box = font.getbbox(coordinate[1])
    height = box[3] - box[1]
    width = box[2] - box[0]
    collection: List[CoordinateFnReturnType] = []
    if coordinate[0] == "a":
        collection.append(
            {
                "coordinate": (square_origin[0] + 5, square_origin[1] + 3),
                "text": coordinate[1],
            }
        )
    if coordinate[1] == "1":
        collection.append(
            {
                "coordinate": (
                    square_origin[0] + square_length - width - 5,
                    square_origin[1] + square_length - height - 13,
                ),
                "text": coordinate[0],
            }
        )
    return collection


coordinate_position_fn: Dict[str, CoordinateFn] = {
    "standard": standard,
    "every_square": every_square,
    "along_outer_rim": along_outer_rim,
}
"""Dictionary of available coordinate position functions.

Keys:
    - "standard": Chess.com/Lichess style - rank on a-file corner, file on 1st rank corner.
    - "every_square": Full coordinate notation (e.g., "e4") centered on every square.
    - "along_outer_rim": Coordinates along board edges - files on bottom, ranks on left.
"""


class Coordinates(TypedDict):
    """Configuration for drawing coordinates on the board.

    Attributes:
        font: A function that takes a size and returns a PIL font.
        size: The font size to use. If None, defaults to 1.
        dark_color: The color to use for coordinates on dark squares (hex string).
        light_color: The color to use for coordinates on light squares (hex string).
        position_fn: A function that determines where to place coordinate text.
    """

    font: FontLoaderWithSize
    size: Optional[int]
    dark_color: str
    light_color: str
    position_fn: CoordinateFn


class LastMove(TypedDict):
    """Configuration for highlighting the last move on the board.

    Attributes:
        before: The starting square in algebraic notation (e.g., "e2") or as indices.
        after: The ending square in algebraic notation (e.g., "e4") or as indices.
        darkColor: The highlight color for dark squares (hex string).
        lightColor: The highlight color for light squares (hex string).
    """

    before: Union[str, BoardPosition]
    after: Union[str, BoardPosition]
    darkColor: str
    lightColor: str


def _is_light_square(coord: BoardPosition) -> bool:
    """Check if a board coordinate is a light square.

    Args:
        coord: A tuple of (x, y) board coordinates.

    Returns:
        True if the square is light-colored, False if dark.
    """
    return (coord[0] + coord[1]) % 2 == 0


def paint_checker_board(
    board: Image.Image,
    dark_color: str,
    last_move: Optional[LastMove] = None,
) -> Image.Image:
    """Paint the checkerboard pattern on the board image.

    Creates the alternating light/dark square pattern and optionally
    highlights squares involved in the last move.

    Args:
        board: The PIL Image to paint on. Must be a square image.
        dark_color: The color for dark squares as a hex string (e.g., "#D18B47").
        last_move: Optional dictionary containing last move highlighting info.

    Returns:
        The modified board image with the checkerboard pattern.

    Raises:
        Exception: If the board image is not square.
    """
    height, width = board.size
    draw = ImageDraw.Draw(board)
    if height != width:
        raise Exception("Height unequal to width")

    square_size: float = width / 8

    # Draw dark squares using direct coordinate calculation
    for y in range(8):
        # Offset alternates: 1 for even rows, 0 for odd rows
        start_offset = 1 if y % 2 == 0 else 0
        for x in range(0, 8, 2):
            actual_x = x + start_offset
            x0 = actual_x * square_size
            y0 = y * square_size
            draw.rectangle(
                [(x0, y0), (x0 + square_size - 1, y0 + square_size - 1)],
                dark_color
            )

    if last_move is not None:
        before = last_move["before"]
        after = last_move["after"]
        before_color = last_move["lightColor"] if _is_light_square(before) else last_move["darkColor"]  # type: ignore
        after_color = last_move["lightColor"] if _is_light_square(after) else last_move["darkColor"]  # type: ignore

        # Highlight last move squares
        bx, by = before[0] * square_size, before[1] * square_size  # type: ignore
        ax, ay = after[0] * square_size, after[1] * square_size  # type: ignore
        draw.rectangle([(bx, by), (bx + square_size - 1, by + square_size - 1)], before_color)
        draw.rectangle([(ax, ay), (ax + square_size - 1, ay + square_size - 1)], after_color)

    return board


# Module-level caches for piece and arrow images
piece_cache: Dict[str, PieceImages] = {}
resized_cache: Dict[str, PieceImages] = {}
# Cache for pre-extracted alpha channels (avoids repeated image.split() calls)
alpha_cache: Dict[str, Dict[str, Image.Image]] = {}


def load_pieces_folder(
    path: str,
    cache: bool = True,
) -> Callable[[Image.Image], PieceImages]:
    """Load chess piece images from a folder.

    Loads piece images from the specified folder structure and returns
    a function that can resize them for a specific board size.

    The folder must have the following structure::

        path/
        ├── white/
        │   ├── King.png
        │   ├── Queen.png
        │   ├── Rook.png
        │   ├── Bishop.png
        │   ├── Knight.png
        │   └── Pawn.png
        └── black/
            ├── King.png
            ├── Queen.png
            ├── Rook.png
            ├── Bishop.png
            ├── Knight.png
            └── Pawn.png

    Args:
        path: Path to the folder containing piece images.
        cache: Whether to cache loaded images for reuse. Defaults to True.

    Returns:
        A function that takes a board image and returns a dictionary
        mapping piece characters to appropriately sized PIL Images.

    Example:
        ```python
        pieces = load_pieces_folder("./pieces")
        board = Image.new("RGB", (800, 800), "white")
        piece_images = pieces(board)
        king_image = piece_images["K"]  # White king
        ```
    """
    if path in piece_cache:
        piece_images = piece_cache[path]
    else:
        white_path = os.path.join(path, "white")
        black_path = os.path.join(path, "black")

        def w_path(piece: str) -> str:
            return os.path.join(white_path, piece + ".png")

        def b_path(piece: str) -> str:
            return os.path.join(black_path, piece + ".png")

        piece_images: PieceImages = {
            "p": Image.open(b_path("Pawn")).convert("RGBA"),
            "P": Image.open(w_path("Pawn")).convert("RGBA"),
            "r": Image.open(b_path("Rook")).convert("RGBA"),
            "R": Image.open(w_path("Rook")).convert("RGBA"),
            "n": Image.open(b_path("Knight")).convert("RGBA"),
            "N": Image.open(w_path("Knight")).convert("RGBA"),
            "b": Image.open(b_path("Bishop")).convert("RGBA"),
            "B": Image.open(w_path("Bishop")).convert("RGBA"),
            "q": Image.open(b_path("Queen")).convert("RGBA"),
            "Q": Image.open(w_path("Queen")).convert("RGBA"),
            "k": Image.open(b_path("King")).convert("RGBA"),
            "K": Image.open(w_path("King")).convert("RGBA"),
        }
        if cache:
            piece_cache[path] = piece_images

    def load(board: Image.Image) -> PieceImages:
        cache_key = f"{path}-{board.size[0]}"
        if cache_key in resized_cache:
            return resized_cache[cache_key]
        else:
            piece_size = int(board.size[0] / 8)
            resized: PieceImages = {}
            alphas: Dict[str, Image.Image] = {}
            for piece in piece_images:
                resized_img = piece_images[piece].resize((piece_size, piece_size))
                resized[piece] = resized_img
                # Pre-extract alpha channel to avoid repeated split() calls
                _, _, _, alphas[piece] = resized_img.split()
            if cache:
                resized_cache[cache_key] = resized
                alpha_cache[cache_key] = alphas
            return resized

    return load


def paint_piece(
    board: Image.Image,
    coord: BoardPosition,
    image: Image.Image,
) -> Image.Image:
    """Paint a single piece on the board.

    Args:
        board: The PIL Image of the board to paint on.
        coord: The (x, y) board coordinates (0-7, 0-7) where x=0 is the a-file.
        image: The PIL Image of the piece to paint.

    Returns:
        The modified board image with the piece painted.
    """
    height, width = board.size
    piece_size = int(width / 8)
    x = coord[0]
    y = coord[1]

    def position(val: int) -> int:
        return int(val * piece_size)

    box = (position(x), position(y), position(x + 1), position(y + 1))

    _, _, _, alpha = image.split()
    Image.Image.paste(board, image, box, alpha)

    return board


def paint_all_pieces(
    board: Image.Image,
    parsed: List[List[str]],
    piece_images: PieceImages,
    piece_alphas: Optional[Dict[str, Image.Image]] = None,
) -> Image.Image:
    """Paint all pieces from a parsed FEN position onto the board.

    Args:
        board: The PIL Image of the board to paint on.
        parsed: A 2D list of piece characters from FenParser.parse().
        piece_images: A dictionary mapping piece characters to PIL Images.
        piece_alphas: Optional pre-extracted alpha channels for efficiency.

    Returns:
        The modified board image with all pieces painted.
    """
    height, width = board.size
    piece_size = int(width / 8)

    for y in range(len(parsed)):
        for x in range(len(parsed[y])):
            piece = parsed[y][x]
            if piece != " ":
                image = piece_images[piece]
                # Use cached alpha if available, otherwise extract it
                if piece_alphas is not None and piece in piece_alphas:
                    alpha = piece_alphas[piece]
                else:
                    _, _, _, alpha = image.split()
                box = (x * piece_size, y * piece_size,
                       (x + 1) * piece_size, (y + 1) * piece_size)
                board.paste(image, box, alpha)
    return board


# Module-level caches for arrow images
arrows_cache: Dict[str, ArrowImages] = {}
resized_arrows_cache: Dict[str, ArrowImages] = {}


def load_arrows_folder(
    path: str,
    cache: bool = True,
) -> Callable[[Image.Image], ArrowImages]:
    """Load arrow images from a folder.

    Loads arrow sprite images for drawing arrows on the board.
    The folder must contain Knight.png and Up.png files.

    Args:
        path: Path to the folder containing arrow images.
        cache: Whether to cache loaded images for reuse. Defaults to True.

    Returns:
        A function that takes a board image and returns a dictionary
        of appropriately sized arrow images.

    Example:
        ```python
        arrows = load_arrows_folder("./arrows")
        board = Image.new("RGB", (800, 800), "white")
        arrow_images = arrows(board)
        ```
    """
    if path in arrows_cache:
        arrows = arrows_cache[path]
    else:

        def arrow_path(name: str) -> str:
            return os.path.join(path, name + ".png")

        arrows: ArrowImages = {
            "one": Image.open(arrow_path("Knight")).convert("RGBA"),
            "up": Image.open(arrow_path("Up")).convert("RGBA"),
        }

    def load(board: Image.Image) -> ArrowImages:
        cache_key = f"{path}-{board.size[0]}"
        if cache_key in resized_arrows_cache:
            return resized_arrows_cache[cache_key]
        else:
            square_size = int(board.size[0] / 8)
            resized: ArrowImages = {}
            base_one = arrows["one"].resize((square_size * 3, square_size * 2))
            resized["one"] = base_one
            resized["up"] = arrows["up"].resize((square_size, square_size * 3))

            # Pre-compute all 8 knight arrow variants with alpha channels
            # This avoids repeated transpose() and split() calls in paint_all_arrows
            resized["knight_-2_1"] = base_one.transpose(Image.FLIP_TOP_BOTTOM)
            resized["knight_-1_2"] = (
                base_one.transpose(Image.ROTATE_270)
                .transpose(Image.FLIP_LEFT_RIGHT)
                .transpose(Image.FLIP_TOP_BOTTOM)
            )
            resized["knight_1_2"] = (
                base_one.transpose(Image.ROTATE_270)
                .transpose(Image.FLIP_LEFT_RIGHT)
                .transpose(Image.ROTATE_180)
            )
            resized["knight_2_1"] = base_one.transpose(Image.ROTATE_180)
            resized["knight_2_-1"] = base_one.transpose(Image.FLIP_LEFT_RIGHT)
            resized["knight_1_-2"] = base_one.transpose(Image.ROTATE_270)
            resized["knight_-1_-2"] = (
                base_one.transpose(Image.ROTATE_270)
                .transpose(Image.FLIP_LEFT_RIGHT)
            )
            resized["knight_-2_-1"] = base_one

            if cache:
                resized_arrows_cache[cache_key] = resized
            return resized

    return load


# Cache for generated arrows by (arrow_id, length, piece_size)
_generated_arrow_cache: Dict[Tuple[int, float, int], Image.Image] = {}


def _generate_arrow(
    arrow: Image.Image,
    length: float,
    piece_size: int,
) -> Image.Image:
    """Generate an arrow image of a specific length.

    Internal function used to create arrows of varying lengths
    by combining head, body, and tail segments. Results are cached.

    Args:
        arrow: The base arrow sprite image.
        length: The length of the arrow in squares.
        piece_size: The size of one square in pixels.

    Returns:
        A PIL Image of the generated arrow.
    """
    # Use arrow's id as cache key component (same arrow object = same cache)
    cache_key = (id(arrow), length, piece_size)
    if cache_key in _generated_arrow_cache:
        return _generated_arrow_cache[cache_key]

    image = arrow
    resized = Image.new("RGBA", (piece_size, int(piece_size * length)))
    head = image.crop((0, 0, piece_size, piece_size)).convert("RGBA")
    tail = image.crop((0, piece_size * 2, piece_size, piece_size * 3)).convert("RGBA")

    body = image.crop((0, piece_size, piece_size, piece_size * 2)).convert("RGBA")
    resized.paste(head)
    resized.paste(tail, (0, int(piece_size * (length - 1))))
    if length > 2:
        body = body.resize((piece_size, int(piece_size * (length - 2))))
        resized.paste(body, (0, piece_size))

    _generated_arrow_cache[cache_key] = resized
    return resized


Arrow = Tuple[BoardPosition, BoardPosition]
"""A tuple of (start, end) board positions representing an arrow."""

ArrowInput = Union[Tuple[str, str], Tuple[BoardPosition, BoardPosition], List[Any]]
"""Arrow input can be algebraic notation strings or board position tuples."""


def paint_all_arrows(
    board: Image.Image,
    arrow_configuration: List[Arrow],
    arrow_set: ArrowImages,
) -> Image.Image:
    """Paint all arrows on the board.

    Supports knight-move arrows, straight arrows (horizontal, vertical),
    and diagonal arrows of any length.

    Args:
        board: The PIL Image of the board to paint on.
        arrow_configuration: A list of (start, end) position tuples.
        arrow_set: A dictionary of arrow images from load_arrows_folder.

    Returns:
        The modified board image with all arrows painted.

    Raises:
        ValueError: If an arrow has an invalid start/end combination.
    """
    height, width = board.size
    piece_size = int(width / 8)

    def position(val: int) -> int:
        return int(val * piece_size)

    # Knight move cache keys: maps delta to (cache_key, use_target_x, use_target_y)
    # Boolean flags indicate whether to use target coords instead of start coords
    knight_deltas = {
        (-2, 1): ("knight_-2_1", True, False),
        (-1, 2): ("knight_-1_2", True, False),
        (1, 2): ("knight_1_2", False, False),
        (2, 1): ("knight_2_1", False, False),
        (2, -1): ("knight_2_-1", False, True),
        (1, -2): ("knight_1_-2", False, True),
        (-1, -2): ("knight_-1_-2", True, True),
        (-2, -1): ("knight_-2_-1", True, True),
    }

    for arrow in arrow_configuration:
        start = arrow[0]
        end = arrow[1]
        delta = (end[0] - start[0], end[1] - start[1])
        start_x = position(start[0])
        start_y = position(start[1])
        target_x = position(end[0])
        target_y = position(end[1])

        if delta in knight_deltas:
            # Use pre-computed knight arrow variant
            cache_key, use_target_x, use_target_y = knight_deltas[delta]
            paste_x = target_x if use_target_x else start_x
            paste_y = target_y if use_target_y else start_y
            image = arrow_set[cache_key]
            _, _, _, alpha = image.split()
            Image.Image.paste(board, image, (paste_x, paste_y), alpha)
        elif delta[0] == 0:
            image = _generate_arrow(arrow_set["up"], abs(delta[1]) + 1, piece_size)
            if delta[1] > 0:
                image = image.transpose(Image.ROTATE_180)
                _, _, _, alpha = image.split()
                Image.Image.paste(board, image, (start_x, start_y), alpha)
            else:
                _, _, _, alpha = image.split()
                Image.Image.paste(board, image, (target_x, target_y), alpha)
        elif delta[1] == 0:
            image = _generate_arrow(
                arrow_set["up"], abs(delta[0]) + 1, piece_size
            ).transpose(Image.ROTATE_270)
            if delta[0] < 0:
                image = image.transpose(Image.ROTATE_180)
                _, _, _, alpha = image.split()
                Image.Image.paste(board, image, (target_x, target_y), alpha)
            else:
                _, _, _, alpha = image.split()
                Image.Image.paste(board, image, (start_x, start_y), alpha)
        elif abs(delta[0]) == abs(delta[1]):
            length = math.sqrt((abs(delta[0]) + 0.5) ** 2 + (abs(delta[1]) + 0.5) ** 2)
            arrow_img = _generate_arrow(arrow_set["up"], length, piece_size).rotate(
                45, expand=True
            )
            if delta[0] > 0 and delta[1] > 0:
                arrow_img = arrow_img.transpose(Image.ROTATE_180)
                _, _, _, alpha = arrow_img.split()
                Image.Image.paste(board, arrow_img, (start_x, start_y), alpha)
            elif delta[0] > 0 and delta[1] < 0:
                arrow_img = arrow_img.transpose(Image.ROTATE_270)
                _, _, _, alpha = arrow_img.split()
                Image.Image.paste(board, arrow_img, (start_x, target_y), alpha)
            elif delta[0] < 0 and delta[1] > 0:
                arrow_img = arrow_img.transpose(Image.ROTATE_90)
                _, _, _, alpha = arrow_img.split()
                Image.Image.paste(board, arrow_img, (target_x, start_y), alpha)
            elif delta[0] < 0 and delta[1] < 0:
                _, _, _, alpha = arrow_img.split()
                Image.Image.paste(board, arrow_img, (target_x, target_y), alpha)
        else:
            raise ValueError(
                f"Invalid arrow target: start({start}) end({end})"
            )
    return board


def indices_to_square(indices: BoardPosition) -> str:
    """Convert board indices to algebraic notation.

    Args:
        indices: A tuple of (x, y) where x is the file (0-7, a-h)
            and y is the rank from the top (0-7, 8-1).

    Returns:
        The square in algebraic notation (e.g., "a8", "e4", "h1").

    Example:
        >>> indices_to_square((0, 0))
        'a8'
        >>> indices_to_square((4, 4))
        'e4'
        >>> indices_to_square((7, 7))
        'h1'
    """
    return f"{chr(indices[0] + 97)}{7 - indices[1] + 1}"


def square_to_indices(square: str) -> BoardPosition:
    """Convert algebraic notation to board indices.

    Args:
        square: A square in algebraic notation (e.g., "a8", "e4", "h1").

    Returns:
        A tuple of (x, y) where x is the file index (0-7)
        and y is the rank index from the top (0-7).

    Example:
        >>> square_to_indices("a8")
        (0, 0)
        >>> square_to_indices("e4")
        (4, 4)
        >>> square_to_indices("h1")
        (7, 7)
    """
    return (ord(square[0]) - 97, 7 - int(square[1]) + 1)


def flip_coord_tuple(coord: BoardPosition) -> BoardPosition:
    """Flip coordinates for black's perspective.

    Transforms coordinates as if the board were rotated 180 degrees.

    Args:
        coord: A tuple of (x, y) board coordinates.

    Returns:
        The flipped coordinates.

    Example:
        >>> flip_coord_tuple((0, 0))
        (7, 7)
        >>> flip_coord_tuple((4, 4))
        (3, 3)
    """
    return (7 - coord[0], 7 - coord[1])


def paint_coordinates_inside_board(
    board: Image.Image,
    coordinates: Coordinates,
) -> Image.Image:
    """Paint coordinates on the board (placeholder function).

    Note:
        This function is currently a placeholder and does not
        actually paint coordinates. Use the coordinates parameter
        in fen_to_image instead.

    Args:
        board: The PIL Image of the board.
        coordinates: The coordinate configuration.

    Returns:
        The unmodified board image.
    """
    for x in range(0, 8):
        for y in range(0, 8):
            coord_str = indices_to_square((x, y))
    return board


def load_font_file(path: str) -> FontLoaderWithSize:
    """Load a font file for use with coordinates.

    Supports both TrueType (.ttf) fonts and PIL bitmap fonts.

    Args:
        path: Path to the font file.

    Returns:
        A function that takes a font size and returns a PIL font object.

    Example:
        >>> font_loader = load_font_file("./fonts/Roboto-Bold.ttf")
        >>> font = font_loader(24)  # Get font at size 24
    """

    def loader(size: int) -> FontType:
        if ".ttf" in path:
            return ImageFont.truetype(path, size=size)
        return ImageFont.load(path)

    return loader


def fen_to_image(
    fen: str,
    square_length: int,
    piece_set: Callable[[Image.Image], PieceImages],
    dark_color: str,
    light_color: str,
    arrow_set: Optional[Callable[[Image.Image], ArrowImages]] = None,
    arrows: Optional[List[ArrowInput]] = None,
    flipped: bool = False,
    last_move: Optional[LastMove] = None,
    coordinates: Optional[Coordinates] = None,
) -> Image.Image:
    """Generate a chess board image from a FEN string.

    This is the main function for rendering chess positions. It creates
    a PIL Image of the specified chess position with customizable colors,
    pieces, arrows, and move highlighting.

    Args:
        fen: A FEN string representing the chess position.
        square_length: The length of each square in pixels.
            The resulting image will be 8 * square_length pixels square.
        piece_set: A piece loader function from load_pieces_folder().
        dark_color: The color for dark squares as a hex string (e.g., "#D18B47").
        light_color: The color for light squares as a hex string (e.g., "#FFCE9E").
        arrow_set: Optional arrow loader function from load_arrows_folder().
        arrows: Optional list of arrows to draw. Each arrow is a tuple of
            (start, end) where start and end can be algebraic notation
            (e.g., "e2", "e4") or board position tuples (e.g., (4, 6), (4, 4)).
        flipped: If True, render the board from black's perspective.
            Defaults to False (white's perspective).
        last_move: Optional dictionary for highlighting the last move.
            Should contain 'before', 'after', 'darkColor', and 'lightColor' keys.
        coordinates: Optional configuration for drawing coordinates on the board.

    Returns:
        A PIL Image of the rendered chess position.

    Example:
        Basic usage:

        ```python
        board = fen_to_image(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            square_length=100,
            piece_set=load_pieces_folder("./pieces"),
            dark_color="#D18B47",
            light_color="#FFCE9E"
        )
        board.save("starting_position.png")
        ```

        With arrows and last move highlighting:

        ```python
        board = fen_to_image(
            fen="rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
            square_length=100,
            piece_set=load_pieces_folder("./pieces"),
            dark_color="#D18B47",
            light_color="#FFCE9E",
            arrow_set=load_arrows_folder("./arrows"),
            arrows=[("e2", "e4")],
            last_move={
                "before": "e2",
                "after": "e4",
                "darkColor": "#aaa23a",
                "lightColor": "#cdd269"
            }
        )
        ```
    """
    board = Image.new("RGB", (square_length * 8, square_length * 8), light_color)
    parsed_board = FenParser(fen).parse()

    # Convert arrow coordinates from algebraic notation to indices
    if arrows is not None:
        for arrow in arrows:
            if isinstance(arrow[0], str):
                arrow[0] = square_to_indices(arrow[0])  # type: ignore
            if isinstance(arrow[1], str):
                arrow[1] = square_to_indices(arrow[1])  # type: ignore

    # Convert last move coordinates from algebraic notation to indices
    if last_move is not None:
        if isinstance(last_move["before"], str):
            last_move["before"] = square_to_indices(last_move["before"])
        if isinstance(last_move["after"], str):
            last_move["after"] = square_to_indices(last_move["after"])

    # Flip the board for black's perspective
    if flipped:
        parsed_board.reverse()
        for row in parsed_board:
            row.reverse()
        if last_move is not None:
            last_move["before"] = flip_coord_tuple(last_move["before"])  # type: ignore
            last_move["after"] = flip_coord_tuple(last_move["after"])  # type: ignore
        if arrows is not None:
            for index, arrow in enumerate(arrows):
                arrows[index] = (
                    flip_coord_tuple(arrow[0]),  # type: ignore
                    flip_coord_tuple(arrow[1]),  # type: ignore
                )

    board = paint_checker_board(board, dark_color, last_move)

    # Draw coordinates if configured
    if coordinates is not None:
        draw = ImageDraw.Draw(board)
        size = 1 if coordinates["size"] is None else coordinates["size"]
        font = coordinates["font"](size)
        for x in range(0, 8):
            for y in range(0, 8):
                coord_str = indices_to_square((x, y))
                text_objects = coordinates["position_fn"](
                    coord_str,
                    (x * square_length, y * square_length),
                    square_length,
                    font,
                )
                if text_objects is not None:
                    for text in text_objects:
                        draw.text(
                            text["coordinate"],
                            text["text"],
                            font=font,
                            fill=coordinates["dark_color"],
                        )

    piece_images = piece_set(board)
    # Look up cached alpha channels by finding the matching resized_cache entry
    piece_alphas = None
    for cache_key, cached_images in resized_cache.items():
        if cached_images is piece_images:
            piece_alphas = alpha_cache.get(cache_key)
            break
    board = paint_all_pieces(board, parsed_board, piece_images, piece_alphas)

    if arrow_set is not None and arrows is not None:
        board = paint_all_arrows(board, arrows, arrow_set(board))  # type: ignore

    return board


# Backwards compatibility aliases (deprecated, use snake_case versions)
fenToImage = fen_to_image
loadPiecesFolder = load_pieces_folder
loadArrowsFolder = load_arrows_folder
loadFontFile = load_font_file
squareToIndices = square_to_indices
indicesToSquare = indices_to_square
flipCoordTuple = flip_coord_tuple
CoordinatePositionFn = coordinate_position_fn
