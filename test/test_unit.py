import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fentoboardimage import (
    FenParser,
    square_to_indices,
    indices_to_square,
    flip_coord_tuple,
    standard,
    every_square,
    along_outer_rim,
    coordinate_position_fn,
    # Deprecated aliases
    fenToImage,
    loadPiecesFolder,
    loadArrowsFolder,
    loadFontFile,
    CoordinatePositionFn,
)
from fentoboardimage.main import (
    fen_to_image,
    load_pieces_folder,
    load_arrows_folder,
    load_font_file,
    squareToIndices,
    indicesToSquare,
    flipCoordTuple,
)


class TestFenParser:
    """Tests for the FenParser class."""

    def test_parse_starting_position(self):
        """Test parsing the standard starting position."""
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        fp = FenParser(fen)
        result = fp.parse()

        assert len(result) == 8
        assert result[0] == ["r", "n", "b", "q", "k", "b", "n", "r"]
        assert result[1] == ["p", "p", "p", "p", "p", "p", "p", "p"]
        assert result[6] == ["P", "P", "P", "P", "P", "P", "P", "P"]
        assert result[7] == ["R", "N", "B", "Q", "K", "B", "N", "R"]

    def test_parse_empty_board(self):
        """Test parsing an empty board."""
        fen = "8/8/8/8/8/8/8/8 w - - 0 1"
        fp = FenParser(fen)
        result = fp.parse()

        assert len(result) == 8
        for rank in result:
            assert rank == [" ", " ", " ", " ", " ", " ", " ", " "]

    def test_parse_rank_with_pieces(self):
        """Test parsing a rank with pieces."""
        fp = FenParser("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

        assert fp.parse_rank("rnbqkbnr") == ["r", "n", "b", "q", "k", "b", "n", "r"]
        assert fp.parse_rank("pppppppp") == ["p", "p", "p", "p", "p", "p", "p", "p"]
        assert fp.parse_rank("RNBQKBNR") == ["R", "N", "B", "Q", "K", "B", "N", "R"]

    def test_parse_rank_with_empty_squares(self):
        """Test parsing ranks with empty squares."""
        fp = FenParser("8/8/8/8/8/8/8/8 w - - 0 1")

        assert fp.parse_rank("8") == [" ", " ", " ", " ", " ", " ", " ", " "]
        assert fp.parse_rank("4p3") == [" ", " ", " ", " ", "p", " ", " ", " "]
        assert fp.parse_rank("r6R") == ["r", " ", " ", " ", " ", " ", " ", "R"]

    def test_parse_mixed_rank(self):
        """Test parsing a rank with mixed pieces and empty squares."""
        fp = FenParser("8/8/8/8/8/8/8/8 w - - 0 1")

        assert fp.parse_rank("r1bqkb1r") == ["r", " ", "b", "q", "k", "b", " ", "r"]
        assert fp.parse_rank("2p2p2") == [" ", " ", "p", " ", " ", "p", " ", " "]
        assert fp.parse_rank("1P2P2K") == [" ", "P", " ", " ", "P", " ", " ", "K"]

    def test_parse_sicilian_defense(self):
        """Test parsing a Sicilian Defense position."""
        fen = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"
        fp = FenParser(fen)
        result = fp.parse()

        # c5 pawn is on rank 5 (index 3 from top: 8,7,6,5)
        assert result[3] == [" ", " ", "p", " ", " ", " ", " ", " "]
        # e4 pawn is on rank 4 (index 4 from top)
        assert result[4] == [" ", " ", " ", " ", "P", " ", " ", " "]
        assert result[6] == ["P", "P", "P", "P", " ", "P", "P", "P"]

    def test_parse_complex_middlegame(self):
        """Test parsing a complex middlegame position."""
        fen = "r1bq1rk1/ppp2ppp/2np1n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQ1RK1 w - - 0 7"
        fp = FenParser(fen)
        result = fp.parse()

        assert len(result) == 8
        # Check black's back rank
        assert result[0] == ["r", " ", "b", "q", " ", "r", "k", " "]
        # Check white's back rank
        assert result[7] == ["R", "N", "B", "Q", " ", "R", "K", " "]

    def test_parse_endgame_position(self):
        """Test parsing an endgame position with few pieces."""
        fen = "8/8/8/4k3/8/8/4K3/8 w - - 0 1"
        fp = FenParser(fen)
        result = fp.parse()

        # Check kings are in correct positions
        assert result[3][4] == "k"  # Black king on e5
        assert result[6][4] == "K"  # White king on e2

    def test_expand_numbers(self):
        """Test the expand method converts numbers to spaces."""
        fp = FenParser("8/8/8/8/8/8/8/8 w - - 0 1")

        assert fp.expand("1") == " "
        assert fp.expand("2") == "  "
        assert fp.expand("3") == "   "
        assert fp.expand("8") == "        "

    def test_flatten(self):
        """Test the flatten method."""
        fp = FenParser("8/8/8/8/8/8/8/8 w - - 0 1")

        assert fp.flatten([["a", "b"], ["c", "d"]]) == ["a", "b", "c", "d"]
        assert fp.flatten([["r"], ["n"], ["b"]]) == ["r", "n", "b"]
        assert fp.flatten([]) == []

    def test_expand_or_noop_with_pieces(self):
        """Test expand_or_noop returns pieces unchanged."""
        fp = FenParser("8/8/8/8/8/8/8/8 w - - 0 1")

        for piece in "kqbnrpKQBNRP":
            assert fp.expand_or_noop(piece) == piece

    def test_expand_or_noop_with_numbers(self):
        """Test expand_or_noop expands numbers to spaces."""
        fp = FenParser("8/8/8/8/8/8/8/8 w - - 0 1")

        assert fp.expand_or_noop("1") == " "
        assert fp.expand_or_noop("3") == "   "
        assert fp.expand_or_noop("8") == "        "


class TestSquareConversion:
    """Tests for square conversion functions."""

    def test_square_to_indices_corners(self):
        """Test corner squares conversion."""
        assert square_to_indices("a8") == (0, 0)
        assert square_to_indices("h8") == (7, 0)
        assert square_to_indices("a1") == (0, 7)
        assert square_to_indices("h1") == (7, 7)

    def test_square_to_indices_center(self):
        """Test center squares conversion."""
        assert square_to_indices("d4") == (3, 4)
        assert square_to_indices("e4") == (4, 4)
        assert square_to_indices("d5") == (3, 3)
        assert square_to_indices("e5") == (4, 3)

    def test_square_to_indices_edges(self):
        """Test edge squares conversion."""
        assert square_to_indices("a4") == (0, 4)
        assert square_to_indices("h4") == (7, 4)
        assert square_to_indices("d1") == (3, 7)
        assert square_to_indices("d8") == (3, 0)

    def test_indices_to_square_corners(self):
        """Test corner indices conversion."""
        assert indices_to_square((0, 0)) == "a8"
        assert indices_to_square((7, 0)) == "h8"
        assert indices_to_square((0, 7)) == "a1"
        assert indices_to_square((7, 7)) == "h1"

    def test_indices_to_square_center(self):
        """Test center indices conversion."""
        assert indices_to_square((3, 4)) == "d4"
        assert indices_to_square((4, 4)) == "e4"
        assert indices_to_square((3, 3)) == "d5"
        assert indices_to_square((4, 3)) == "e5"

    def test_round_trip_conversion(self):
        """Test that converting back and forth gives the same result."""
        squares = ["a1", "a8", "h1", "h8", "e4", "d5", "c3", "f6"]
        for square in squares:
            indices = square_to_indices(square)
            result = indices_to_square(indices)
            assert result == square, f"Round trip failed for {square}"

    def test_all_squares(self):
        """Test conversion for all 64 squares."""
        files = "abcdefgh"
        for file_idx, file in enumerate(files):
            for rank in range(1, 9):
                square = f"{file}{rank}"
                indices = square_to_indices(square)
                result = indices_to_square(indices)
                assert result == square, f"Conversion failed for {square}"


class TestFlipCoordTuple:
    """Tests for the flip_coord_tuple function."""

    def test_flip_corners(self):
        """Test flipping corner coordinates."""
        assert flip_coord_tuple((0, 0)) == (7, 7)
        assert flip_coord_tuple((7, 7)) == (0, 0)
        assert flip_coord_tuple((0, 7)) == (7, 0)
        assert flip_coord_tuple((7, 0)) == (0, 7)

    def test_flip_center(self):
        """Test flipping center coordinates."""
        assert flip_coord_tuple((3, 3)) == (4, 4)
        assert flip_coord_tuple((4, 4)) == (3, 3)
        assert flip_coord_tuple((3, 4)) == (4, 3)
        assert flip_coord_tuple((4, 3)) == (3, 4)

    def test_flip_twice_returns_original(self):
        """Test that flipping twice returns the original coordinates."""
        coords = [(0, 0), (7, 7), (3, 5), (1, 6), (4, 2)]
        for coord in coords:
            flipped = flip_coord_tuple(coord)
            double_flipped = flip_coord_tuple(flipped)
            assert double_flipped == coord, f"Double flip failed for {coord}"

    def test_flip_all_squares(self):
        """Test flipping all squares on the board."""
        for x in range(8):
            for y in range(8):
                original = (x, y)
                flipped = flip_coord_tuple(original)
                assert flipped == (7 - x, 7 - y)


class TestCoordinatePositionFunctions:
    """Tests for coordinate position functions."""

    def test_coordinate_position_fn_dict(self):
        """Test that coordinate_position_fn contains all expected functions."""
        assert "standard" in coordinate_position_fn
        assert "every_square" in coordinate_position_fn
        assert "along_outer_rim" in coordinate_position_fn

    def test_standard_fn_returns_list(self):
        """Test that standard returns a list for edge squares."""
        from PIL import ImageFont

        font = ImageFont.load_default()
        # a1 is on both a-file and 1st rank, so should return 2 items
        result = standard("a1", (0, 0), 100, font)
        assert isinstance(result, list)
        assert len(result) == 2
        assert "coordinate" in result[0]
        assert "text" in result[0]

    def test_every_square_fn_returns_list(self):
        """Test that every_square returns a list with full notation."""
        from PIL import ImageFont

        font = ImageFont.load_default()
        result = every_square("e4", (0, 0), 100, font)
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["text"] == "e4"

    def test_along_outer_rim_fn_returns_list(self):
        """Test that along_outer_rim returns a list for edge squares."""
        from PIL import ImageFont

        font = ImageFont.load_default()
        # a1 is on both a-file and 1st rank, so should return 2 items
        result = along_outer_rim("a1", (0, 0), 100, font)
        assert isinstance(result, list)
        assert len(result) == 2


class TestFenParserEdgeCases:
    """Edge case tests for FenParser."""

    def test_fen_with_castling_rights(self):
        """Test that castling rights don't affect board parsing."""
        fen_kq = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        fen_none = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1"

        result_kq = FenParser(fen_kq).parse()
        result_none = FenParser(fen_none).parse()

        assert result_kq == result_none

    def test_fen_with_en_passant(self):
        """Test that en passant square doesn't affect board parsing."""
        fen_ep = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
        fp = FenParser(fen_ep)
        result = fp.parse()

        assert result[4] == [" ", " ", " ", " ", "P", " ", " ", " "]

    def test_fen_with_move_counters(self):
        """Test that move counters don't affect board parsing."""
        fen1 = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        fen2 = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 50 100"

        result1 = FenParser(fen1).parse()
        result2 = FenParser(fen2).parse()

        assert result1 == result2

    def test_fen_scholars_mate(self):
        """Test parsing a Scholar's Mate position."""
        fen = "r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4"
        fp = FenParser(fen)
        result = fp.parse()

        # White queen on f7
        assert result[1][5] == "Q"
        # White bishop on c4
        assert result[4][2] == "B"

    def test_fen_promotion_position(self):
        """Test parsing a position with potential promotion."""
        fen = "8/P7/8/8/8/8/p7/8 w - - 0 1"
        fp = FenParser(fen)
        result = fp.parse()

        assert result[1][0] == "P"  # White pawn on a7
        assert result[6][0] == "p"  # Black pawn on a2

    def test_all_piece_types(self):
        """Test that all piece types are parsed correctly."""
        # Position with all piece types
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        fp = FenParser(fen)
        result = fp.parse()

        # Check all black pieces
        assert "r" in result[0]
        assert "n" in result[0]
        assert "b" in result[0]
        assert "q" in result[0]
        assert "k" in result[0]
        assert "p" in result[1]

        # Check all white pieces
        assert "R" in result[7]
        assert "N" in result[7]
        assert "B" in result[7]
        assert "Q" in result[7]
        assert "K" in result[7]
        assert "P" in result[6]


class TestDeprecatedAliases:
    """Tests for deprecated backwards compatibility aliases."""

    def test_fenToImage_is_alias_for_fen_to_image(self):
        """Test that fenToImage is an alias for fen_to_image."""
        assert fenToImage is fen_to_image

    def test_loadPiecesFolder_is_alias_for_load_pieces_folder(self):
        """Test that loadPiecesFolder is an alias for load_pieces_folder."""
        assert loadPiecesFolder is load_pieces_folder

    def test_loadArrowsFolder_is_alias_for_load_arrows_folder(self):
        """Test that loadArrowsFolder is an alias for load_arrows_folder."""
        assert loadArrowsFolder is load_arrows_folder

    def test_loadFontFile_is_alias_for_load_font_file(self):
        """Test that loadFontFile is an alias for load_font_file."""
        assert loadFontFile is load_font_file

    def test_squareToIndices_is_alias_for_square_to_indices(self):
        """Test that squareToIndices is an alias for square_to_indices."""
        assert squareToIndices is square_to_indices

    def test_indicesToSquare_is_alias_for_indices_to_square(self):
        """Test that indicesToSquare is an alias for indices_to_square."""
        assert indicesToSquare is indices_to_square

    def test_flipCoordTuple_is_alias_for_flip_coord_tuple(self):
        """Test that flipCoordTuple is an alias for flip_coord_tuple."""
        assert flipCoordTuple is flip_coord_tuple

    def test_CoordinatePositionFn_is_alias_for_coordinate_position_fn(self):
        """Test that CoordinatePositionFn is an alias for coordinate_position_fn."""
        assert CoordinatePositionFn is coordinate_position_fn

    def test_squareToIndices_works_correctly(self):
        """Test that deprecated squareToIndices works correctly."""
        assert squareToIndices("a8") == (0, 0)
        assert squareToIndices("h1") == (7, 7)
        assert squareToIndices("e4") == (4, 4)

    def test_indicesToSquare_works_correctly(self):
        """Test that deprecated indicesToSquare works correctly."""
        assert indicesToSquare((0, 0)) == "a8"
        assert indicesToSquare((7, 7)) == "h1"
        assert indicesToSquare((4, 4)) == "e4"

    def test_flipCoordTuple_works_correctly(self):
        """Test that deprecated flipCoordTuple works correctly."""
        assert flipCoordTuple((0, 0)) == (7, 7)
        assert flipCoordTuple((7, 7)) == (0, 0)
        assert flipCoordTuple((3, 4)) == (4, 3)

    def test_CoordinatePositionFn_contains_expected_keys(self):
        """Test that deprecated CoordinatePositionFn has expected entries."""
        assert "standard" in CoordinatePositionFn
        assert "every_square" in CoordinatePositionFn
        assert "along_outer_rim" in CoordinatePositionFn
