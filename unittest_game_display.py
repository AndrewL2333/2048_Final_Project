import unittest
from game_display import Tile, Config, move_tiles, generate_tiles, main, end_move

class Test2048Game(unittest.TestCase):
    def setUp(self):
        # Create an initial set of tiles
        self.tiles = generate_tiles()
        self.window = Config.WINDOW  # Assuming this is a valid pygame window object

    def test_tile_initialization(self):
        # Ensure tiles are initialized with a value of 2 or 4
        for key, tile in self.tiles.items():
            self.assertIn(tile.value, [2, 4], "Tile should have a value of 2 or 4 at initialization.")

    def test_tile_color(self):
        # Verify that the correct color is assigned based on the tile's value
        tile = Tile(2, 0, 0)
        expected_color = (237, 229, 218)  # Expected color for tile value 2
        self.assertEqual(tile.get_color(), expected_color, "Color does not match expected value for tile.")

    def test_move_tiles(self):
        # This would require a more complex setup to simulate different board states
        # Here we test a simple movement to see if the function handles it without errors
        move_tiles(self.tiles, 'left')  # Move all tiles left
        # Check if any tile has moved or merged
        self.assertTrue(any(tile.col != col for (row, col), tile in self.tiles.items()), "Tiles should have moved after action.")

    def test_end_move_scenario(self):
        # Fill the grid to simulate a full board
        for row in range(Config.ROWS):
            for col in range(Config.COLS):
                self.tiles[f"{row}{col}"] = Tile(2, row, col)
        result = end_move(self.tiles)
        self.assertEqual(result, "lost", "Game should recognize loss when no moves are possible.")

    def test_generate_tiles(self):
        # Check if initial generation creates exactly two tiles
        self.assertEqual(len(self.tiles), 2, "Initial tile generation should create exactly two tiles.")

if __name__ == '__main__':
    unittest.main()
