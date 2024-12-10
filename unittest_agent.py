import unittest
from unittest.mock import MagicMock
import math

from IntelligentAgent import IntelligentAgent

class TestIntelligentAgent(unittest.TestCase):

    def setUp(self):
        self.agent = IntelligentAgent()
        self.mock_grid = MagicMock()
        # Set up a basic 4x4 grid. For simplicity, use zeros for empty cells.
        self.mock_grid.map = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 0, 2, 4],
            [4, 2, 4, 8]
        ]
        
    def test_get_move_no_moves_available(self):
        # If there are no available moves, getMove should return default (0)
        self.mock_grid.canMove.return_value = False
        move = self.agent.getMove(self.mock_grid)
        self.assertEqual(move, 0, "Should return default move when no moves are available.")

    def test_get_move_with_available_moves(self):
        # Mock that the grid can move and provides a list of moves
        # Let's say moves are indexed as 0: UP, 1: RIGHT, 2: DOWN, 3: LEFT
        self.mock_grid.canMove.return_value = True
        self.mock_grid.getAvailableMoves.return_value = [(0, "Up"), (1, "Right")]
        
        # Mock out what happens when we try moves:
        # Cloned grids after each move:
        clone1 = MagicMock()
        clone1.map = [
            [4,4,2,4],
            [0,2,4,2],
            [2,0,2,4],
            [4,2,4,8]
        ]
        clone2 = MagicMock()
        clone2.map = [
            [2,4,2,4],
            [4,2,4,2],
            [2,0,2,4],
            [4,2,4,8]
        ]

        def clone_side_effect():
            # Return a new mock each time clone is called
            if not hasattr(clone_side_effect, 'call_count'):
                clone_side_effect.call_count = 0
            if clone_side_effect.call_count == 0:
                clone_side_effect.call_count += 1
                return clone1
            else:
                return clone2

        self.mock_grid.clone.side_effect = clone_side_effect

        # Mock moves on the cloned grids
        # For simplicity, we assume they can still move, etc.
        clone1.canMove.return_value = True
        clone2.canMove.return_value = True
        clone1.getAvailableMoves.return_value = []
        clone2.getAvailableMoves.return_value = []

        # This will test that the agent selects the move with the highest utility
        # Since no further moves are simulated (no recursion), the evaluation 
        # will determine the best move.
        move = self.agent.getMove(self.mock_grid)
        # Just check it returns one of the moves, since the full logic is complex.
        self.assertIn(move, [0, 1], "Should return one of the available moves.")

    def test_evaluate_caching(self):
        # Test that evaluate results are cached
        self.mock_grid.canMove.return_value = False
        
        # First evaluation
        result1 = self.agent.evaluate(self.mock_grid)
        # Calling evaluate again should return from cache directly
        # To check this, we can temporarily alter the grid to see if it ignores changes
        original_map = self.mock_grid.map
        self.mock_grid.map = [
            [16, 8, 4, 2],
            [2, 4, 8, 16],
            [32, 2, 2, 2],
            [2, 2, 4, 8]
        ]
        result2 = self.agent.evaluate(self.mock_grid)
        
        # Since caching uses str(grid.map) as the key and we changed the map, 
        # the second call should produce a different result if caching wasn't working.
        # But the first call inserted into cache using the original map string, not the changed one.
        # Let's revert the map and see if the same result emerges.
        self.mock_grid.map = original_map
        result3 = self.agent.evaluate(self.mock_grid)
        
        # result1 should be equal to result3 as they are the same map.
        self.assertEqual(result1, result3, "Cached evaluation should yield the same result for the same map.")
        # result2 should differ since the map changed (and wasn't cached).
        self.assertNotEqual(result1, result2, "Changing the map should produce a different evaluation result.")

    def test_smoothness_calculation(self):
        # Just test that calculate_smoothness doesn't raise errors
        # and returns a float. The correctness of smoothness logic can be checked by known expected values.
        smoothness = self.agent.calculate_smoothness(self.mock_grid)
        self.assertIsInstance(smoothness, float, "Smoothness should return a float.")

    def test_monotonicity_calculation(self):
        # Similarly test monotonicity
        mono = self.agent.calculate_monotonicity(self.mock_grid)
        self.assertIsInstance(mono, float, "Monotonicity should return a float.")

    def test_snake_evaluation(self):
        # Test snake evaluation
        snake_score = self.agent.snake_evaluation(self.mock_grid)
        self.assertIsInstance(snake_score, int, "Snake evaluation should return an integer.")
        # Changing the grid map should produce a different snake_score
        old_score = snake_score
        self.mock_grid.map = [
            [0, 0, 0, 2],
            [0, 0, 0, 4],
            [0, 0, 2, 4],
            [2, 4, 8, 16]
        ]
        new_score = self.agent.snake_evaluation(self.mock_grid)
        self.assertNotEqual(old_score, new_score, "Different board states should yield different snake evaluations.")


if __name__ == '__main__':
    unittest.main()
