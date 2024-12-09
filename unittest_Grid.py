import unittest
from Grid import Grid, UP, DOWN, LEFT, RIGHT

class TestGrid(unittest.TestCase):

    def setUp(self):
        self.grid = Grid()

    def test_initialization(self):
        # Test if the grid is initialized correctly
        self.assertEqual(len(self.grid.map), 4)
        self.assertEqual(len(self.grid.map[0]), 4)
        for row in self.grid.map:
            self.assertTrue(all(cell == 0 for cell in row))

    def test_set_and_get_cell_value(self):
        # Test setting and getting cell value
        self.grid.setCellValue((0, 0), 2)
        self.assertEqual(self.grid.getCellValue((0, 0)), 2)
        self.grid.setCellValue((3, 3), 4)
        self.assertEqual(self.grid.getCellValue((3, 3)), 4)
        self.assertIsNone(self.grid.getCellValue((4, 4)), "Out of bounds should return None")

    def test_can_insert(self):
        # Test canInsert method
        self.assertTrue(self.grid.canInsert((0, 0)))
        self.grid.setCellValue((0, 0), 2)
        self.assertFalse(self.grid.canInsert((0, 0)))

    def test_get_available_cells(self):
        # Test getAvailableCells method
        self.grid.setCellValue((0, 0), 2)
        self.grid.setCellValue((1, 1), 4)
        cells = self.grid.getAvailableCells()
        self.assertEqual(len(cells), 14)
        self.assertNotIn((0, 0), cells)
        self.assertNotIn((1, 1), cells)

    def test_get_max_tile(self):
        # Test getMaxTile method
        self.assertEqual(self.grid.getMaxTile(), 0)
        self.grid.setCellValue((0, 0), 2)
        self.assertEqual(self.grid.getMaxTile(), 2)
        self.grid.setCellValue((1, 1), 4)
        self.assertEqual(self.grid.getMaxTile(), 4)

    def test_move_up(self):
        # Test move method in UP direction
        self.grid.setCellValue((1, 0), 2)
        self.grid.setCellValue((2, 0), 2)
        self.grid.move(UP)
        self.assertEqual(self.grid.getCellValue((0, 0)), 4)
        self.assertEqual(self.grid.getCellValue((1, 0)), 0)

    def test_move_down(self):
        # Test move method in DOWN direction
        self.grid.setCellValue((0, 0), 2)
        self.grid.setCellValue((1, 0), 2)
        self.grid.move(DOWN)
        self.assertEqual(self.grid.getCellValue((3, 0)), 4)
        self.assertEqual(self.grid.getCellValue((2, 0)), 0)

    def test_move_left(self):
        # Test move method in LEFT direction
        self.grid.setCellValue((0, 1), 2)
        self.grid.setCellValue((0, 2), 2)
        self.grid.move(LEFT)
        self.assertEqual(self.grid.getCellValue((0, 0)), 4)
        self.assertEqual(self.grid.getCellValue((0, 1)), 0)

    def test_move_right(self):
        # Test move method in RIGHT direction
        self.grid.setCellValue((0, 1), 2)
        self.grid.setCellValue((0, 2), 2)
        self.grid.move(RIGHT)
        self.assertEqual(self.grid.getCellValue((0, 3)), 4)
        self.assertEqual(self.grid.getCellValue((0, 2)), 0)

    def test_can_move(self):
        # Test canMove method
        self.assertTrue(self.grid.canMove())
        self.grid.setCellValue((0, 0), 2)
        self.grid.setCellValue((0, 1), 4)
        self.grid.setCellValue((0, 2), 8)
        self.grid.setCellValue((0, 3), 16)
        self.grid.setCellValue((1, 0), 32)
        self.grid.setCellValue((1, 1), 64)
        self.grid.setCellValue((1, 2), 128)
        self.grid.setCellValue((1, 3), 256)
        self.grid.setCellValue((2, 0), 512)
        self.grid.setCellValue((2, 1), 1024)
        self.grid.setCellValue((2, 2), 2048)
        self.grid.setCellValue((2, 3), 4096)
        self.grid.setCellValue((3, 0), 8192)
        self.grid.setCellValue((3, 1), 16384)
        self.grid.setCellValue((3, 2), 32768)
        self.grid.setCellValue((3, 3), 65536)
        self.assertFalse(self.grid.canMove())

    def test_get_available_moves(self):
        # Test getAvailableMoves method
        self.grid.setCellValue((0, 0), 2)
        self.grid.setCellValue((1, 0), 2)
        moves = self.grid.getAvailableMoves()
        self.assertGreater(len(moves), 0)
        move_dirs = [move[0] for move in moves]
        self.assertIn(UP, move_dirs)

if __name__ == '__main__':
    unittest.main()
