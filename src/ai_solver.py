import random

# Action an opponent move can ask the board to perform
REVEAL = 'REVEAL'


class MinesweeperAI:

    def __init__(self, rng=None):

        # Accepting a generator makes the opponent's randomness testable.
        self.rng = rng if rng is not None else random.Random()

    """OPPONENT TURN"""
    def take_turn(self, board):

        move = self.solve(board)

        return [move] if move is not None else []

    """SINGLE BEST MOVE"""
    def solve(self, board):

        return self.guess(board)

    """RANDOM GUESS"""
    def guess(self, board):

        candidates = board.get_unrevealed_cells()

        # Every cell is covered, already revealed, or already flagged.
        if not candidates:
            return None

        x, y = self.rng.choice(candidates)

        return (x, y, REVEAL)
