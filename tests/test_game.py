import unittest
from gomoku.game import Board

class TestWinDetection(unittest.TestCase):
    def test_horizontal_win(self):
        b = Board(size=15)
        player = 1
        y = 7
        for x in range(3,8):
            b.place_move(x,y,player)
        winner, line = b.check_win((7, y, player))
        self.assertEqual(winner, player)
        self.assertEqual(len(line), 5)

    def test_vertical_win(self):
        b = Board(size=15)
        player = 2
        x = 5
        for y in range(4,9):
            b.place_move(x,y,player)
        winner, line = b.check_win((x, 6, player))
        self.assertEqual(winner, player)
        self.assertEqual(len(line), 5)

    def test_diagonal_win(self):
        b = Board(size=15)
        player = 1
        coords = [(2,2),(3,3),(4,4),(5,5),(6,6)]
        for x,y in coords:
            b.place_move(x,y,player)
        winner, line = b.check_win((4,4,player))
        self.assertEqual(winner, player)
        self.assertEqual(len(line), 5)

    def test_illegal_move(self):
        b = Board(size=5)
        self.assertTrue(b.place_move(0,0,1))
        self.assertFalse(b.place_move(0,0,2))

if __name__ == '__main__':
    unittest.main()
