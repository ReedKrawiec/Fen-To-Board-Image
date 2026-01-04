#!/usr/bin/env python
"""FEN string parser for chess positions.

This module provides the FenParser class for parsing FEN (Forsyth-Edwards Notation)
strings into board representations that can be used for rendering chess positions.

Example:
    ```python
    from fentoboardimage import FenParser
    parser = FenParser("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    board = parser.parse()
    print(board[0])  # First rank (black's back rank)
    # Output: ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
    ```
"""

from __future__ import annotations

from typing import List

# Valid piece characters (faster set lookup than regex)
_PIECES = frozenset('kqbnrpKQBNRP')

# Pre-computed space lists for digits 1-8 (avoids repeated list creation)
_SPACES = {
    '1': [' '],
    '2': [' ', ' '],
    '3': [' ', ' ', ' '],
    '4': [' ', ' ', ' ', ' '],
    '5': [' ', ' ', ' ', ' ', ' '],
    '6': [' ', ' ', ' ', ' ', ' ', ' '],
    '7': [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    '8': [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
}


class FenParser:
    """Parses FEN strings into board representations.

    FEN (Forsyth-Edwards Notation) is a standard notation for describing
    chess positions. This parser extracts the piece placement from a FEN
    string and converts it into a 2D list representation.

    Attributes:
        fen_str: The FEN string to parse.

    Example:
        ```python
        parser = FenParser("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        board = parser.parse()
        len(board)  # 8 ranks
        # Output: 8
        board[0]  # Black's back rank
        # Output: ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        ```
    """

    __slots__ = ('fen_str',)

    def __init__(self, fen_str: str) -> None:
        """Initialize the FEN parser with a FEN string.

        Args:
            fen_str: A valid FEN string representing a chess position.
                The string should contain piece placement data separated
                by slashes, followed by additional game state information.
        """
        self.fen_str: str = fen_str

    def parse(self) -> List[List[str]]:
        """Parse the FEN string into a 2D board representation.

        Returns:
            A list of 8 lists, each containing 8 strings representing
            the pieces on that rank. Empty squares are represented by
            a space character ' '. Pieces are represented by their
            standard algebraic notation:
            - 'K'/'k': King (white/black)
            - 'Q'/'q': Queen (white/black)
            - 'R'/'r': Rook (white/black)
            - 'B'/'b': Bishop (white/black)
            - 'N'/'n': Knight (white/black)
            - 'P'/'p': Pawn (white/black)

        Example:
            >>> parser = FenParser("8/8/8/8/8/8/8/8 w - - 0 1")
            >>> board = parser.parse()
            >>> board[0]  # All empty squares
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        """
        # Extract board part (before first space) and split by rank
        board_str = self.fen_str.split(" ", 1)[0]
        return [self._parse_rank(rank) for rank in board_str.split("/")]

    def _parse_rank(self, rank: str) -> List[str]:
        """Parse a single rank from FEN notation (optimized single-pass).

        Args:
            rank: A string representing one rank of the board in FEN notation.

        Returns:
            A list of 8 strings representing the pieces on that rank.
        """
        result: List[str] = []
        for char in rank:
            if char in _PIECES:
                result.append(char)
            elif char in _SPACES:
                result.extend(_SPACES[char])
        return result

    # Keep old methods for backwards compatibility
    def parse_rank(self, rank: str) -> List[str]:
        """Parse a single rank from FEN notation.

        Args:
            rank: A string representing one rank of the board in FEN notation.
                For example, "rnbqkbnr" or "8" or "4p3".

        Returns:
            A list of 8 strings representing the pieces on that rank.
            Empty squares are represented by space characters.

        Example:
            >>> parser = FenParser("8/8/8/8/8/8/8/8 w - - 0 1")
            >>> parser.parse_rank("rnbqkbnr")
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
            >>> parser.parse_rank("4p3")
            [' ', ' ', ' ', ' ', 'p', ' ', ' ', ' ']
        """
        return self._parse_rank(rank)

    def flatten(self, lst) -> List[str]:
        """Flatten an iterator of strings into a single list of characters.

        Args:
            lst: An iterator of strings to flatten.

        Returns:
            A flattened list of individual characters.
        """
        return [char for s in lst for char in s]

    def expand_or_noop(self, piece_str: str) -> str:
        """Expand a number to spaces or return the piece character unchanged.

        Args:
            piece_str: Either a piece character (kqbnrpKQBNRP) or a digit (1-8).

        Returns:
            The original piece character if it's a piece, or a string of
            spaces if it's a number.
        """
        if piece_str in _PIECES:
            return piece_str
        return self.expand(piece_str)

    def expand(self, num_str: str) -> str:
        """Expand a digit string into the corresponding number of spaces.

        Args:
            num_str: A string containing a single digit (1-8).

        Returns:
            A string of spaces with length equal to the digit value.
        """
        return ' ' * int(num_str)
