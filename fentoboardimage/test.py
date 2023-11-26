import unittest
import os
from main import fenToImage, loadPiecesFolder, loadArrowsFolder, CoordinatePositionFn, loadFontFile
from PIL import ImageChops
from operator import itemgetter
from PIL import ImageDraw
from PIL import Image


class FenToBoardImageTest(unittest.TestCase):

    def test_outputs(self):
        image1 = fenToImage(
            fen="8/5N2/4p2p/5p1k/1p4rP/1P2Q1P1/P4P1K/5q2 w - - 15 44",
            squarelength=125,
            pieceSet=loadPiecesFolder(
                "./test/pieces"),
            darkColor="#79a65d",
            lightColor="#daf2cb",
            flipped=True,
            coordinates={
                "font": loadFontFile("./test/fonts/Roboto-Bold.ttf"),
                "size": 28,
                "darkColor": "#79a65d",
                "lightColor": "#daf2cb",
                "positionFn": CoordinatePositionFn["everySquare"],
                "padding": 5,
                "outsideBoardColor": "#000000"
            }
        )
        image1.show()
        # image2 = Image.open("./test/boards/board1.png")
        # diff = ImageChops.difference(image1, image2)
        # self.assertEqual(diff.getbbox(), None)

    def test_board_colors(self):
        image1 = fenToImage(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            squarelength=100,
            pieceSet=loadPiecesFolder("./test/pieces"),
            darkColor="#D18B47",
            lightColor="#FFCE9E"
        )
        image2 = Image.open("./test/boards/board2.png")
        diff = ImageChops.difference(image1, image2)
        self.assertEqual(diff.getbbox(), None)

    def test_pieces(self):
        image1 = fenToImage(
            fen="rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2 ",
            squarelength=100,
            pieceSet=loadPiecesFolder("./test/pieces2"),
            darkColor="#909090",
            lightColor="#fffefe"
        )
        image2 = Image.open("./test/boards/board3.png")
        diff = ImageChops.difference(image1, image2)
        self.assertEqual(diff.getbbox(), None)

    def test_flip(self):
        original = fenToImage(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            squarelength=100,
            pieceSet=loadPiecesFolder("./test/pieces2"),
            darkColor="#909090",
            lightColor="#fffefe"
        )
        flipped = fenToImage(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            squarelength=100,
            pieceSet=loadPiecesFolder("./test/pieces2"),
            darkColor="#909090",
            lightColor="#fffefe",
            flipped=True
        )
        original_image = Image.open("./test/boards/board4.png")
        flipped_image = Image.open("./test/boards/board5.png")
        self.assertEqual(ImageChops.difference(
            original, original_image).getbbox(), None)
        self.assertEqual(ImageChops.difference(
            flipped, flipped_image).getbbox(), None)

    def test_lastMove(self):
        lastMoveDrawn = fenToImage(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            squarelength=100,
            pieceSet=loadPiecesFolder("./test/pieces"),
            darkColor="#909090",
            lightColor="#fffefe",
            lastMove={
                "before": "a1",
                "after": "g7",
                "darkColor": "#a9a238",
                "lightColor": "#cdd269"
            }
        )
        lastMoveDrawnFlipped = fenToImage(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            squarelength=100,
            pieceSet=loadPiecesFolder("./test/pieces"),
            darkColor="#909090",
            lightColor="#fffefe",
            flipped=True,
            lastMove={
                "before": "a1",
                "after": "g7",
                "darkColor": "#a9a238",
                "lightColor": "#cdd269"
            }
        )
        i = Image.open("./test/boards/board6.png")
        flipped = Image.open("./test/boards/board7.png")
        self.assertEqual(ImageChops.difference(
            lastMoveDrawn, i).getbbox(), None)
        self.assertEqual(ImageChops.difference(
            lastMoveDrawnFlipped, flipped).getbbox(), None)

    def test_KnightArrows(self):
        arrows = fenToImage(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            squarelength=100,
            pieceSet=loadPiecesFolder("./test/pieces"),
            darkColor="#909090",
            lightColor="#fffefe",
            ArrowSet=loadArrowsFolder("./test/arrows1"),
            Arrows=[
                ((3, 3), (1, 4)),
                ((3, 3), (2, 5)),
                ((3, 3), (4, 5)),
                ((3, 3), (5, 4)),
                ((3, 3), (5, 2)),
                ((3, 3), (4, 1)),
                ((3, 3), (2, 1)),
                ((3, 3), (1, 2)),
            ]
        )
        flipped = fenToImage(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            squarelength=100,
            pieceSet=loadPiecesFolder("./test/pieces"),
            darkColor="#909090",
            lightColor="#fffefe",
            ArrowSet=loadArrowsFolder("./test/arrows1"),
            flipped=True,
            Arrows=[
                ((3, 3), (1, 4)),
                ((3, 3), (2, 5)),
                ((3, 3), (4, 5)),
                ((3, 3), (5, 4)),
                ((3, 3), (5, 2)),
                ((3, 3), (4, 1)),
                ((3, 3), (2, 1)),
                ((3, 3), (1, 2)),
            ]
        )
        i = Image.open("./test/boards/board8.png")
        i_2 = Image.open("./test/boards/board9.png")
        self.assertEqual(ImageChops.difference(arrows, i).getbbox(), None)
        self.assertEqual(ImageChops.difference(flipped, i_2).getbbox(), None)

    def test_HorizontalArrows(self):
        arrows = fenToImage(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            squarelength=100,
            pieceSet=loadPiecesFolder("./test/pieces"),
            darkColor="#909090",
            lightColor="#fffefe",
            ArrowSet=loadArrowsFolder("./test/arrows1"),
            Arrows=[
                ((0, 0), (7, 0)),
                ((1, 1), (6, 1)),
                ((2, 2), (5, 2)),
                ((3, 3), (4, 3)),
                ((4, 4), (3, 4)),
                ((5, 5), (2, 5)),
                ((6, 6), (1, 6)),
                ((7, 7), (0, 7)),
            ]
        )
        arrows_flipped = fenToImage(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            squarelength=100,
            pieceSet=loadPiecesFolder("./test/pieces"),
            darkColor="#909090",
            lightColor="#fffefe",
            ArrowSet=loadArrowsFolder("./test/arrows1"),
            flipped=True,
            Arrows=[
                ((0, 0), (7, 0)),
                ((1, 1), (6, 1)),
                ((2, 2), (5, 2)),
                ((3, 3), (4, 3)),
                ((4, 4), (3, 4)),
                ((5, 5), (2, 5)),
                ((6, 6), (1, 6)),
                ((7, 7), (0, 7)),
            ]
        )
        i = Image.open("./test/boards/board10.png")
        self.assertEqual(ImageChops.difference(arrows, i).getbbox(), None)
        i2 = Image.open("./test/boards/board11.png")
        self.assertEqual(ImageChops.difference(
            arrows_flipped, i2).getbbox(), None)

    def test_VerticalArrows(self):
        arrows = fenToImage(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            squarelength=100,
            pieceSet=loadPiecesFolder("./test/pieces"),
            darkColor="#909090",
            lightColor="#fffefe",
            ArrowSet=loadArrowsFolder("./test/arrows1"),
            Arrows=[
                ((0, 0), (0, 7)),
                ((1, 1), (1, 6)),
                ((2, 2), (2, 5)),
                ((3, 3), (3, 4)),
                ((4, 4), (4, 3)),
                ((5, 5), (5, 2)),
                ((6, 6), (6, 1)),
                ((7, 7), (7, 0))
            ]
        )
        arrows_flipped = fenToImage(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            squarelength=100,
            pieceSet=loadPiecesFolder("./test/pieces"),
            darkColor="#909090",
            lightColor="#fffefe",
            ArrowSet=loadArrowsFolder("./test/arrows1"),
            flipped=True,
            Arrows=[
                ((0, 0), (0, 7)),
                ((1, 1), (1, 6)),
                ((2, 2), (2, 5)),
                ((3, 3), (3, 4)),
                ((4, 4), (4, 3)),
                ((5, 5), (5, 2)),
                ((6, 6), (6, 1)),
                ((7, 7), (7, 0))
            ]
        )
        i = Image.open("./test/boards/board12.png")
        i2 = Image.open("./test/boards/board13.png")
        self.assertEqual(ImageChops.difference(arrows, i).getbbox(), None)
        self.assertEqual(ImageChops.difference(
            arrows_flipped, i2).getbbox(), None)

    def test_DiagArrows(self):
        arrows = fenToImage(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            squarelength=100,
            pieceSet=loadPiecesFolder("./test/pieces"),
            darkColor="#909090",
            lightColor="#fffefe",
            ArrowSet=loadArrowsFolder("./test/arrows1"),
            Arrows=[
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
            ]
        )
        arrows_flipped = fenToImage(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            squarelength=100,
            pieceSet=loadPiecesFolder("./test/pieces"),
            darkColor="#909090",
            lightColor="#fffefe",
            flipped=True,
            ArrowSet=loadArrowsFolder("./test/arrows1"),
            Arrows=[
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
            ]
        )
        i = Image.open("./test/boards/board14.png")
        i2 = Image.open("./test/boards/board15.png")
        self.assertEqual(ImageChops.difference(arrows, i).getbbox(), None)
        self.assertEqual(ImageChops.difference(
            arrows_flipped, i2).getbbox(), None)


if __name__ == '__main__':
    unittest.main()
