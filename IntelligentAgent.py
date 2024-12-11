from BaseAI import BaseAI
import math

# Set maximum search depth for the expectiminimax algorithm
MAX_DEPTH = 4

class IntelligentAgent(BaseAI):

     # The Monte Carlo method referenced YouTube Video "Game AI: Solving the Game of 2048! (Monte Carlo - Solved)" by John Tan Chong Min.
    
    def __init__(self):
    def __init__(self):
        # Cache stores previously computed game board evaluations for efficiency
        self.cache = {}

    def getMove(self, grid):
        """
        Determines the next move for the agent.
        Uses expectiminimax with alpha-beta pruning to find the best move.
        """
        _, move = self.expectiminimax(grid, MAX_DEPTH, True)
        return move if move is not None else 0  # Default to "Up" if no move is available

    def expectiminimax(self, grid, depth, is_max, alpha=-math.inf, beta=math.inf):
        """
        Recursive function implementing the expectiminimax algorithm with alpha-beta pruning.
        Considers both maximizing (player's move) and chance (random tiles) nodes.
        """
        # Generate a unique key for caching based on the grid state and depth
        cache_key = str(grid.map) + str(depth)
        if cache_key in self.cache:
            return self.cache[cache_key], None  # Return cached value if available

        # Base case: return evaluation score if maximum depth is reached or no moves left
        if depth == 0 or not grid.canMove():
            return self.evaluate(grid), None

        if is_max:  # Maximizing player's turn
            max_utility = -math.inf
            best_move = None
            for move_idx, move_vec in grid.getAvailableMoves():
                # Simulate the move
                child = grid.clone()
                child.move(move_idx)
                # Recursive call to evaluate the result of the move
                utility = self.expectiminimax(child, depth - 1, False, alpha, beta)[0]
                if utility > max_utility:
                    max_utility, best_move = utility, move_idx
                alpha = max(alpha, utility)  # Update alpha
                if beta <= alpha:  # Beta cut-off
                    break
            return max_utility, best_move
        else:  # Chance node (new tiles appear)
            avg_utility = 0
            possible_new_tiles = [2, 4]  # New tiles can have values 2 or 4
            cells = grid.getAvailableCells()  # Empty cells where tiles can appear
            num_cells = len(cells)
            for cell in cells:
                for tile_value in possible_new_tiles:
                    # Simulate placing a new tile
                    child = grid.clone()
                    child.setCellValue(cell, tile_value)
                    # Assign probabilities for each tile value
                    probability = 0.9 if tile_value == 2 else 0.1
                    # Recursive call to evaluate resulting board state
                    avg_utility += probability * self.expectiminimax(child, depth - 1, True, alpha, beta)[0]
            avg_utility /= num_cells  # Average utility over all possibilities
            return avg_utility, None

    def evaluate(self, grid):
        """
        Heuristic evaluation function to assign a score to the current grid.
        Considers smoothness, monotonicity, and a snake-pattern heuristic.
        """
        # Check if the evaluation is already cached
        cache_key = str(grid.map)
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Assign weights to different heuristics
        smoothWeight = 0.001
        monoWeight = 0.001
        snakeWeight = 0.2
        # Calculate heuristic values
        smoothness = self.calculate_smoothness(grid)
        monotonicity = self.calculate_monotonicity(grid)
        snake_score = self.snake_evaluation(grid)

        # Combine weighted heuristics into a single score
        score = (smoothWeight * smoothness) + (monoWeight * monotonicity) + (snakeWeight * snake_score)
        self.cache[cache_key] = score  # Cache the computed score
        return score

    def snake_evaluation(self, grid):
        """
        Evaluate the grid based on a "snake-like" pattern to maximize tile merging potential.
        """
        # Snake-pattern weight matrix
        snake_pattern = [
            [90, 80, 70, 60],
            [30, 38, 44, 52],
            [22, 18, 14, 10],
            [0, 2, 4, 6]
        ]
        score = 0
        for x in range(4):
            for y in range(4):
                if grid.map[x][y]:
                    score += grid.map[x][y] * snake_pattern[x][y]
        return score

    def calculate_smoothness(self, grid):
        """
        Compute smoothness of the grid, which minimizes large differences between adjacent tiles.
        """
        smoothness = 0
        for x in range(4):
            for y in range(4):
                if grid.map[x][y]:
                    value = math.log(grid.map[x][y], 2)  # Logarithmic value for comparison
                    for direction in [(1, 0), (0, 1)]:  # Check horizontal and vertical neighbors
                        target_x = x + direction[0]
                        target_y = y + direction[1]
                        if target_x < 4 and target_y < 4:
                            target_value = math.log(grid.map[target_x][target_y], 2) if grid.map[target_x][target_y] else 0
                            smoothness -= abs(value - target_value)  # Penalize large differences
        return smoothness

    def calculate_monotonicity(self, grid):
        """
        Calculate monotonicity of the grid, preferring rows and columns with consistently increasing or decreasing values.
        """
        totals = [0, 0, 0, 0]  # Totals for left/right and up/down directions

        # Check left/right monotonicity
        for x in range(4):
            current = 0
            next = current + 1
            while next < 4:
                while next < 4 and not grid.map[x][next]:
                    next += 1
                if next >= 4:
                    break
                current_value = math.log(grid.map[x][current], 2) if grid.map[x][current] else 0
                next_value = math.log(grid.map[x][next], 2) if grid.map[x][next] else 0
                if current_value > next_value:
                    totals[0] += next_value - current_value
                elif next_value > current_value:
                    totals[1] += current_value - next_value
                current = next
                next += 1

        # Check up/down monotonicity
        for y in range(4):
            current = 0
            next = current + 1
            while next < 4:
                while next < 4 and not grid.map[next][y]:
                    next += 1
                if next >= 4:
                    break
                current_value = math.log(grid.map[current][y], 2) if grid.map[current][y] else 0
                next_value = math.log(grid.map[next][y], 2) if grid.map[next][y] else 0
                if current_value > next_value:
                    totals[2] += next_value - current_value
                elif next_value > current_value:
                    totals[3] += current_value - next_value
                current = next
                next += 1

        # Return the maximum monotonicity score
        return max(totals[0], totals[1]) + max(totals[2], totals[3])
