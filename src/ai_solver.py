"""Choose Minesweeper moves with simple rules based only on visible information.

Easy guesses among covered, unflagged cells. Medium applies direct clue rules,
and Hard adds a carefully checked 1-2-1 pattern. The solver returns one action
at a time; the game applies it through its existing reveal and flag methods.
"""

from dataclasses import dataclass
from enum import Enum
from random import Random
from typing import Optional, Sequence


class Difficulty(str, Enum):
    """Available levels of reasoning for the solver."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class AIMode(str, Enum):
    """Game turn modes; the game loop, not the solver, controls these turns."""

    HUMAN_ONLY = "human"
    INTERACTIVE = "interactive"
    AUTOMATIC = "automatic"


class ActionType(str, Enum):
    """Board operation requested by one solver action."""

    REVEAL = "reveal"
    FLAG = "flag"


@dataclass(frozen=True)
class CellKnowledge:
    """What the solver may know about one cell, without its hidden type."""

    revealed: bool = False
    flagged: bool = False
    number: Optional[int] = None

    def __post_init__(self):
        """Reject clue information that could not be visible to the solver."""
        if not self.revealed and self.number is not None:
            raise ValueError("Covered cells cannot expose a clue number.")
        if self.number is not None and not 0 <= self.number <= 8:
            raise ValueError("A Minesweeper clue must be between 0 and 8.")


@dataclass(frozen=True)
class AIAction:
    """One requested move and its zero-based column and row coordinates.

    The game translates this request into its shared reveal or flag handler;
    the solver never changes a board tile directly.
    """

    action_type: ActionType
    col: int
    row: int


Observation = Sequence[Sequence[CellKnowledge]]


def observation_from_board(board) -> tuple[tuple[CellKnowledge, ...], ...]:
    """Build a row-major view of visible clues, flags, and cell states.

    Args:
        board: The game board whose visible state is being copied.

    Returns:
        Immutable rows of CellKnowledge; covered cells expose no clue number.
    """
    width = len(board.board_list)
    height = len(board.board_list[0]) if width else 0
    view = []

    for row in range(height):
        visible_row = []
        for col in range(width):
            tile = board.board_list[col][row]
            visible_row.append(
                CellKnowledge(
                    revealed=tile.revealed,
                    flagged=tile.flagged,
                    number=tile.clue_num if tile.revealed else None,
                )
            )
        view.append(tuple(visible_row))

    return tuple(view)


class MinesweeperSolver:
    """Choose one reveal-or-flag action using the requested rule set.

    The solver reasons from an Observation rather than inspecting hidden mines.
    """

    def __init__(self, difficulty=Difficulty.EASY, seed=None):
        """Set the rule level and optional seed for repeatable random choices.

        Args:
            difficulty: Easy, Medium, or Hard solver rules.
            seed: Optional random seed; omit it for ordinary random play.
        """
        self.difficulty = Difficulty(difficulty)
        self._seed = seed
        self._random = Random(seed)

    def reset(self):
        """Reset random-choice state when a new board starts; returns nothing."""
        self._random = Random(self._seed)

    def next_action(self, observation: Observation, can_flag=True):
        """Return one legal-looking move based on the current visible board.

        Args:
            observation: Visible cell information arranged by row, then column.
            can_flag: Whether the game's flag limit allows another flag.

        Returns:
            An AIAction, or None when there are no eligible cells to act on.
        """
        if not observation or not observation[0]:
            return None

        if self.difficulty in (Difficulty.MEDIUM, Difficulty.HARD):
            # Try direct clue deductions before making a guess.
            action = self._medium_action(observation, can_flag)
            if action is not None:
                return action

        if self.difficulty is Difficulty.HARD:
            # Hard adds its pattern rule only after direct clues give no move.
            action = self._one_two_one_action(observation, can_flag)
            if action is not None:
                return action

        return self._random_reveal(observation)

    @staticmethod
    def _neighbors(observation, col, row):
        """Yield valid neighboring (column, row) pairs, excluding this cell.

        Args:
            observation: Row-major visible board information.
            col: Column of the cell whose neighbors are requested.
            row: Row of that cell.

        Yields:
            Coordinates for each in-bounds neighboring cell.
        """
        height = len(observation)
        width = len(observation[0])
        for neighbor_row in range(max(0, row - 1), min(height, row + 2)):
            for neighbor_col in range(max(0, col - 1), min(width, col + 2)):
                if (neighbor_col, neighbor_row) != (col, row):
                    yield neighbor_col, neighbor_row

    def _medium_action(self, observation, can_flag):
        """Apply single-clue rules and return the first certain move, if any.

        Args:
            observation: Visible cells and clue numbers.
            can_flag: Whether the game permits another flag.

        Returns:
            A reveal/flag action when a clue proves one, otherwise None.
        """
        for row, cells in enumerate(observation):
            for col, cell in enumerate(cells):
                if not cell.revealed or cell.number is None or cell.number == 0:
                    continue

                neighbors = list(self._neighbors(observation, col, row))
                flagged = [
                    (x, y) for x, y in neighbors if observation[y][x].flagged
                ]
                covered = [
                    (x, y)
                    for x, y in neighbors
                    if not observation[y][x].revealed
                    and not observation[y][x].flagged
                ]
                # Flags count toward the clue, so subtract them first.
                remaining = cell.number - len(flagged)

                # No mines remain for these covered neighbors: reveal one.
                if covered and remaining == 0:
                    x, y = covered[0]
                    return AIAction(ActionType.REVEAL, x, y)

                # Every covered neighbor must be a mine: flag one if allowed.
                if can_flag and covered and remaining == len(covered):
                    x, y = covered[0]
                    return AIAction(ActionType.FLAG, x, y)

        return None

    def _one_two_one_action(self, observation, can_flag):
        """Search straight 1-2-1 patterns horizontally and vertically.

        Args:
            observation: Visible cells and clue numbers.
            can_flag: Whether the game permits another flag.

        Returns:
            A proven pattern action, or None if no pattern is conclusive.
        """
        height = len(observation)
        width = len(observation[0])

        for row in range(height):
            for start_col in range(width - 2):
                clue_cells = [(start_col + offset, row) for offset in range(3)]
                for offset_row in (-1, 1):
                    target_row = row + offset_row
                    if 0 <= target_row < height:
                        candidates = [
                            (start_col + offset, target_row) for offset in range(3)
                        ]
                        action = self._resolve_one_two_one(
                            observation, clue_cells, candidates, can_flag
                        )
                        if action is not None:
                            return action

        for col in range(width):
            for start_row in range(height - 2):
                clue_cells = [(col, start_row + offset) for offset in range(3)]
                for offset_col in (-1, 1):
                    target_col = col + offset_col
                    if 0 <= target_col < width:
                        candidates = [
                            (target_col, start_row + offset) for offset in range(3)
                        ]
                        action = self._resolve_one_two_one(
                            observation, clue_cells, candidates, can_flag
                        )
                        if action is not None:
                            return action

        return None

    def _resolve_one_two_one(
        self, observation, clue_cells, candidates, can_flag
    ):
        """Check whether one proposed 1-2-1 pattern is fully constrained.

        Args:
            observation: Visible cells and clue numbers.
            clue_cells: Coordinates of the three revealed 1-2-1 clues.
            candidates: Coordinates of the three cells beside those clues.
            can_flag: Whether the game permits another flag.

        Returns:
            One proven reveal/flag action, or None if the pattern is ambiguous.
        """
        clue_numbers = tuple(
            observation[row][col].number for col, row in clue_cells
        )
        if clue_numbers != (1, 2, 1):
            return None

        if any(
            not observation[row][col].revealed
            for col, row in clue_cells
        ):
            return None

        if any(
            observation[row][col].revealed
            for col, row in candidates
        ):
            return None

        expected_mines = (True, False, True)
        if any(
            observation[row][col].flagged and not expected_mines[index]
            for index, (col, row) in enumerate(candidates)
        ):
            return None

        for (clue_col, clue_row), clue_number in zip(clue_cells, clue_numbers):
            neighbor_cells = set(
                self._neighbors(observation, clue_col, clue_row)
            )
            flags = {
                (col, row)
                for col, row in neighbor_cells
                if observation[row][col].flagged
            }
            covered = {
                (col, row)
                for col, row in neighbor_cells
                if not observation[row][col].revealed
                and not observation[row][col].flagged
            }
            expected_covered = {
                candidate
                for index, candidate in enumerate(candidates)
                if candidate in neighbor_cells
                and not observation[candidate[1]][candidate[0]].flagged
            }
            if covered != expected_covered:
                # Extra covered neighbors make this pattern ambiguous.
                return None

            remaining = clue_number - len(flags)
            predicted_remaining = sum(
                1
                for index, candidate in enumerate(candidates)
                if candidate in neighbor_cells
                and expected_mines[index]
                and not observation[candidate[1]][candidate[0]].flagged
            )
            if remaining != predicted_remaining:
                return None

        for index, (col, row) in enumerate(candidates):
            cell = observation[row][col]
            if expected_mines[index]:
                if can_flag and not cell.flagged:
                    return AIAction(ActionType.FLAG, col, row)
            else:
                return AIAction(ActionType.REVEAL, col, row)

        return None

    def _random_reveal(self, observation):
        """Choose a random covered, unflagged cell as a reveal guess.

        Args:
            observation: Visible cells and their revealed/flagged states.

        Returns:
            A reveal action, or None when no eligible cell remains.
        """
        candidates = [
            (col, row)
            for row, cells in enumerate(observation)
            for col, cell in enumerate(cells)
            if not cell.revealed and not cell.flagged
        ]
        if not candidates:
            return None

        col, row = self._random.choice(candidates)
        return AIAction(ActionType.REVEAL, col, row)
