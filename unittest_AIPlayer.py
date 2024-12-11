import unittest
from AIPlayer import AIPlayer

class TestAIPlayer(unittest.TestCase):
    def setUp(self):
        # Initialize the AIPlayer with a known state
        self.game = AIPlayer(size=4)

    def test_insert_random_tiles(self):
        # Test if the correct number of initial tiles are placed
        self.game.insertRandomTiles(2)
        num_non_empty = sum(1 for row in self.game.grid.map for value in row if value != 0)
        self.assertEqual(num_non_empty, 2, "Should have exactly 2 tiles inserted at start.")

    def test_get_new_tile_value(self):
        # Testing the probability distribution of the new tile value
        # This requires multiple runs to statistically verify the distribution
        results = {2: 0, 4: 0}
        for _ in range(1000):
            tile = self.game.getNewTileValue()
            results[tile] += 1
        self.assertTrue(results[2] > 700 and results[4] < 300, "Distribution of tiles does not match expected probabilities.")

    # Additional tests can be written for animate_move, reset_game, etc.

if __name__ == '__main__':
    unittest.main()
