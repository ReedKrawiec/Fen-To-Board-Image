import unittest
import os
os.sys.path.append(os.path.abspath("../fenToBoardImage"))
from main import fenToImage, loadPiecesFolder
from PIL import Image
from PIL import ImageDraw
from operator import itemgetter
from PIL import ImageChops


class FenToBoardImageTest(unittest.TestCase):
    def test_outputs(self):
        image1 = fenToImage(
            fen="8/5N2/4p2p/5p1k/1p4rP/1P2Q1P1/P4P1K/5q2 w - - 15 44",
            squarelength=125,
            pieceSet=loadPiecesFolder(
                "./pieces"),
            darkColor="#79a65d",
            lightColor="#daf2cb"
        )
        image2 = Image.open("./boards/board1.png")
        diff = ImageChops.difference(image1, image2)
        self.assertEqual(diff.getbbox(),None)
        
    def test_board_colors(self):
        image1 = fenToImage(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            squarelength=100,
            pieceSet=loadPiecesFolder("./pieces"),
            darkColor="#D18B47",
            lightColor="#FFCE9E"
        )
        image2 = Image.open("./boards/board2.png")
        diff = ImageChops.difference(image1, image2)
        self.assertEqual(diff.getbbox(),None)

    def test_pieces(self):
        image1 = fenToImage(
            fen="rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2 ",
            squarelength=100,
            pieceSet=loadPiecesFolder("./pieces2"),
            darkColor="#909090",
            lightColor="#fffefe"
	    )
        image2 = Image.open("./boards/board3.png")
        diff = ImageChops.difference(image1, image2)
        self.assertEqual(diff.getbbox(),None)
    
    def test_flip(self):
        original = fenToImage(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            squarelength=100,
            pieceSet=loadPiecesFolder("./pieces2"),
            darkColor="#909090",
            lightColor="#fffefe"
        )
        flipped = fenToImage(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            squarelength=100,
            pieceSet=loadPiecesFolder("./pieces2"),
            darkColor="#909090",
            lightColor="#fffefe",
            flipped=True
        )
        original_image = Image.open("./boards/board4.png")
        flipped_image = Image.open("./boards/board5.png")
        self.assertEqual(ImageChops.difference(original,original_image).getbbox(),None)
        self.assertEqual(ImageChops.difference(flipped,flipped_image).getbbox(),None)

if __name__ == '__main__':
    unittest.main()