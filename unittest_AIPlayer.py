import unittest
from AIPlayer import AIPlayer

class TestAIPlayer(unittest.TestCase):
    def setUp(self):
        # Set up an AIPlayer instance before each test
        self.ai_player = AIPlayer()

    def test_initialization(self):
        # Test if the AIPlayer initializes correctly
        self.assertIsNotNone(self.ai_player.grid)
        self.assertEqual(self.ai_player.initTiles, 2)
        self.assertFalse(self.ai_player.over)

    def test_move(self):
        # Test if move functionalities are correctly updating the game state
        initial_state = self.ai_player.grid.clone()
        self.ai_player.move(0)  # Simulate an 'UP' move
        self.assertNotEqual(self.ai_player.grid.map, initial_state.map)

    def test_game_over(self):
        # You would typically have a method to check if the game is over
        # This is a placeholder for such a test
        self.ai_player.over = True
        self.assertTrue(self.ai_player.over)

if __name__ == '__main__':
    unittest.main()
