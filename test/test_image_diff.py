import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fentoboardimage import (
    fen_to_image,
    load_pieces_folder,
    load_arrows_folder,
)
from PIL import Image
from PIL import ImageChops

# Get the directory containing this test file
TEST_DIR = os.path.dirname(os.path.abspath(__file__))


def _test_path(relative_path):
    """Convert a relative path to be relative to the test directory."""
    return os.path.join(TEST_DIR, relative_path)


def images_are_close(img1, img2, tolerance=2, max_diff_pixels=0.001):
    """Check if two images are close enough, allowing for anti-aliasing differences.

    Args:
        img1, img2: PIL Images to compare
        tolerance: Max allowed difference per color channel (0-255)
        max_diff_pixels: Max fraction of pixels that can differ (0.0-1.0)
    """
    if img1.size != img2.size or img1.mode != img2.mode:
        return False

    diff = ImageChops.difference(img1, img2)
    diff_data = list(diff.getdata())
    total_pixels = len(diff_data)

    # Count pixels that exceed tolerance
    exceeds_tolerance = sum(
        1 for pixel in diff_data
        if any(c > tolerance for c in (pixel if isinstance(pixel, tuple) else (pixel,)))
    )

    return exceeds_tolerance <= (total_pixels * max_diff_pixels)


class TestFenToBoardImage(unittest.TestCase):
    def test_outputs(self):
        image1 = fen_to_image(
            fen="8/5N2/4p2p/5p1k/1p4rP/1P2Q1P1/P4P1K/5q2 w - - 15 44",
            square_length=125,
            piece_set=load_pieces_folder(_test_path("pieces")),
            dark_color="#79a65d",
            light_color="#daf2cb",
        )
        image2 = Image.open(_test_path("boards/board1.png"))
        diff = ImageChops.difference(image1, image2)
        self.assertEqual(diff.getbbox(), None)

    def test_board_colors(self):
        image1 = fen_to_image(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            square_length=100,
            piece_set=load_pieces_folder(_test_path("pieces")),
            dark_color="#D18B47",
            light_color="#FFCE9E",
        )
        image2 = Image.open(_test_path("boards/board2.png"))
        diff = ImageChops.difference(image1, image2)
        self.assertEqual(diff.getbbox(), None)

    def test_pieces(self):
        image1 = fen_to_image(
            fen="rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2 ",
            square_length=100,
            piece_set=load_pieces_folder(_test_path("pieces2")),
            dark_color="#909090",
            light_color="#fffefe",
        )
        image2 = Image.open(_test_path("boards/board3.png"))
        diff = ImageChops.difference(image1, image2)
        self.assertEqual(diff.getbbox(), None)

    def test_flip(self):
        original = fen_to_image(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            square_length=100,
            piece_set=load_pieces_folder(_test_path("pieces2")),
            dark_color="#909090",
            light_color="#fffefe",
        )
        flipped = fen_to_image(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            square_length=100,
            piece_set=load_pieces_folder(_test_path("pieces2")),
            dark_color="#909090",
            light_color="#fffefe",
            flipped=True,
        )
        original_image = Image.open(_test_path("boards/board4.png"))
        flipped_image = Image.open(_test_path("boards/board5.png"))
        self.assertEqual(
            ImageChops.difference(original, original_image).getbbox(), None
        )
        self.assertEqual(ImageChops.difference(flipped, flipped_image).getbbox(), None)

    def test_lastMove(self):
        lastMoveDrawn = fen_to_image(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            square_length=100,
            piece_set=load_pieces_folder(_test_path("pieces")),
            dark_color="#909090",
            light_color="#fffefe",
            last_move={
                "before": "a1",
                "after": "g7",
                "darkColor": "#a9a238",
                "lightColor": "#cdd269",
            },
        )
        lastMoveDrawnFlipped = fen_to_image(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            square_length=100,
            piece_set=load_pieces_folder(_test_path("pieces")),
            dark_color="#909090",
            light_color="#fffefe",
            flipped=True,
            last_move={
                "before": "a1",
                "after": "g7",
                "darkColor": "#a9a238",
                "lightColor": "#cdd269",
            },
        )
        i = Image.open(_test_path("boards/board6.png"))
        flipped = Image.open(_test_path("boards/board7.png"))
        self.assertEqual(ImageChops.difference(lastMoveDrawn, i).getbbox(), None)
        self.assertEqual(
            ImageChops.difference(lastMoveDrawnFlipped, flipped).getbbox(), None
        )

    def test_KnightArrows(self):
        arrows = fen_to_image(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            square_length=100,
            piece_set=load_pieces_folder(_test_path("pieces")),
            dark_color="#909090",
            light_color="#fffefe",
            arrow_set=load_arrows_folder(_test_path("arrows1")),
            arrows=[
                ((3, 3), (1, 4)),
                ((3, 3), (2, 5)),
                ((3, 3), (4, 5)),
                ((3, 3), (5, 4)),
                ((3, 3), (5, 2)),
                ((3, 3), (4, 1)),
                ((3, 3), (2, 1)),
                ((3, 3), (1, 2)),
            ],
        )
        flipped = fen_to_image(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            square_length=100,
            piece_set=load_pieces_folder(_test_path("pieces")),
            dark_color="#909090",
            light_color="#fffefe",
            arrow_set=load_arrows_folder(_test_path("arrows1")),
            flipped=True,
            arrows=[
                ((3, 3), (1, 4)),
                ((3, 3), (2, 5)),
                ((3, 3), (4, 5)),
                ((3, 3), (5, 4)),
                ((3, 3), (5, 2)),
                ((3, 3), (4, 1)),
                ((3, 3), (2, 1)),
                ((3, 3), (1, 2)),
            ],
        )
        i = Image.open(_test_path("boards/board8.png"))
        i_2 = Image.open(_test_path("boards/board9.png"))
        self.assertTrue(images_are_close(arrows, i))
        self.assertTrue(images_are_close(flipped, i_2))

    def test_HorizontalArrows(self):
        arrows = fen_to_image(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            square_length=100,
            piece_set=load_pieces_folder(_test_path("pieces")),
            dark_color="#909090",
            light_color="#fffefe",
            arrow_set=load_arrows_folder(_test_path("arrows1")),
            arrows=[
                ((0, 0), (7, 0)),
                ((1, 1), (6, 1)),
                ((2, 2), (5, 2)),
                ((3, 3), (4, 3)),
                ((4, 4), (3, 4)),
                ((5, 5), (2, 5)),
                ((6, 6), (1, 6)),
                ((7, 7), (0, 7)),
            ],
        )
        arrows_flipped = fen_to_image(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            square_length=100,
            piece_set=load_pieces_folder(_test_path("pieces")),
            dark_color="#909090",
            light_color="#fffefe",
            arrow_set=load_arrows_folder(_test_path("arrows1")),
            flipped=True,
            arrows=[
                ((0, 0), (7, 0)),
                ((1, 1), (6, 1)),
                ((2, 2), (5, 2)),
                ((3, 3), (4, 3)),
                ((4, 4), (3, 4)),
                ((5, 5), (2, 5)),
                ((6, 6), (1, 6)),
                ((7, 7), (0, 7)),
            ],
        )
        i = Image.open(_test_path("boards/board10.png"))
        self.assertTrue(images_are_close(arrows, i))
        i2 = Image.open(_test_path("boards/board11.png"))
        self.assertTrue(images_are_close(arrows_flipped, i2))

    def test_VerticalArrows(self):
        arrows = fen_to_image(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            square_length=100,
            piece_set=load_pieces_folder(_test_path("pieces")),
            dark_color="#909090",
            light_color="#fffefe",
            arrow_set=load_arrows_folder(_test_path("arrows1")),
            arrows=[
                ((0, 0), (0, 7)),
                ((1, 1), (1, 6)),
                ((2, 2), (2, 5)),
                ((3, 3), (3, 4)),
                ((4, 4), (4, 3)),
                ((5, 5), (5, 2)),
                ((6, 6), (6, 1)),
                ((7, 7), (7, 0)),
            ],
        )
        arrows_flipped = fen_to_image(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            square_length=100,
            piece_set=load_pieces_folder(_test_path("pieces")),
            dark_color="#909090",
            light_color="#fffefe",
            arrow_set=load_arrows_folder(_test_path("arrows1")),
            flipped=True,
            arrows=[
                ((0, 0), (0, 7)),
                ((1, 1), (1, 6)),
                ((2, 2), (2, 5)),
                ((3, 3), (3, 4)),
                ((4, 4), (4, 3)),
                ((5, 5), (5, 2)),
                ((6, 6), (6, 1)),
                ((7, 7), (7, 0)),
            ],
        )
        i = Image.open(_test_path("boards/board12.png"))
        i2 = Image.open(_test_path("boards/board13.png"))
        self.assertTrue(images_are_close(arrows, i))
        self.assertTrue(images_are_close(arrows_flipped, i2))

    def test_DiagArrows(self):
        arrows = fen_to_image(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            square_length=100,
            piece_set=load_pieces_folder(_test_path("pieces")),
            dark_color="#909090",
            light_color="#fffefe",
            arrow_set=load_arrows_folder(_test_path("arrows1")),
            arrows=[
                ((0, 0), (7, 7)),
                ((1, 0), (7, 6)),
                ((2, 0), (7, 5)),
                ((3, 0), (7, 4)),
                ((4, 0), (7, 3)),
                ((5, 0), (7, 2)),
                ((6, 0), (7, 1)),
                ((6, 7), (0, 1)),
                ((0, 2), (5, 7)),
                ((0, 7), (2, 5)),
                ((7, 2), (2, 7)),
                ((0, 5), (2, 7)),
                ((0, 6), (1, 7)),
            ],
        )
        arrows_flipped = fen_to_image(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            square_length=100,
            piece_set=load_pieces_folder(_test_path("pieces")),
            dark_color="#909090",
            light_color="#fffefe",
            flipped=True,
            arrow_set=load_arrows_folder(_test_path("arrows1")),
            arrows=[
                ((0, 0), (7, 7)),
                ((1, 0), (7, 6)),
                ((2, 0), (7, 5)),
                ((3, 0), (7, 4)),
                ((4, 0), (7, 3)),
                ((5, 0), (7, 2)),
                ((6, 0), (7, 1)),
                ((6, 7), (0, 1)),
                ((0, 2), (5, 7)),
                ((0, 7), (2, 5)),
                ((7, 2), (2, 7)),
                ((0, 5), (2, 7)),
                ((0, 6), (1, 7)),
            ],
        )
        i = Image.open(_test_path("boards/board14.png"))
        i2 = Image.open(_test_path("boards/board15.png"))
        self.assertTrue(images_are_close(arrows, i))
        self.assertTrue(images_are_close(arrows_flipped, i2))


if __name__ == "__main__":
    unittest.main()
