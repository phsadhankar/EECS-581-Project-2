"""
AI Use Disclosure:

    AI Tool: ChatGPT -5.6 Luna. 
    Use of the tool: to help debug 'solve()' when the AI opponent did not fall
    back to 'guess()'. It also suggested a better way to scan the neighbors of the cells
    using a looping method.

    Prompt 1: 
    "solve() is flagging more than it should. Here is my source file and my requirements
    listed under the medium task for the AI solver."
    Prompt 2:
    "After adding some test print statements, I seem to only get flagged and revealed output but
    not 'guess' statements." 
    "
    Changes after AI assitance:
    The lines of code after the for loops for col & row was consolidated and indented correctly.

"""
import random

# Action an opponent move can ask the board to perform
REVEAL = 'REVEAL'
FLAG = 'FLAG'


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
        # go through ever revealed clue until one of the rules is used to make a move
        for i in range(len(board.board_list)):
            for j in range(len(board.board_list[i])):
                cell = board.board_list[i][j]

                # if cell is not revealed or of type 'C' then we continue (no information)
                if not cell.revealed or cell.type != 'C':
                    continue

                # sort the number's neighbors into two groups, hidden and flagged
                # Revealed neighbors are ignored
                hidden_neighbors = []
                flagged_neighbors = []

                # col and row are offsets that gives the 3x3 block around the middle cell
                for col in (-1, 0, 1):
                    for row in (-1, 0, 1):
                        c, r = i + col, j + row
                        # if the cell and neighbors fall off the edge of the board then we continue/skip it
                        if (col, row) == (0, 0) or not (0 <= c < len(board.board_list) and 0 <= r < len(board.board_list[c])):
                            continue

                        neighbor = board.board_list[c][r]

                        # check if neighbor is flagged since it is unrevealed and would land in the wrong list (hidden)
                        if neighbor.flagged:
                            flagged_neighbors.append((c, r))
                        elif not neighbor.revealed:
                            hidden_neighbors.append((c, r))

                # if nothing around this numbered cell is hidden then we move to the next number
                if not hidden_neighbors:
                    continue

                # rule 1: every hidden neighbor must be a mine, 
                # therefore if the number of hidden neighbors of a revealed
                # cell equals that cell's number then the AI should flag those hidden neighbors
                if len(hidden_neighbors) + len(flagged_neighbors) == cell.clue_num:
                    print('flag')
                    return (*hidden_neighbors[0], FLAG)

                # rule 2: the clue is satisfied, so the rest are safe,
                # if the number of flagged neighbors equals the revealed cells number,
                # the AI should uncover all other hidden neighbors
                if len(flagged_neighbors) == cell.clue_num:
                    print('reveal') 
                    return (*hidden_neighbors[0], REVEAL)

        # no rule applies, so fall back to a random pick
        print('guess')
        return self.guess(board)

    """RANDOM GUESS"""
    def guess(self, board):

        candidates = board.get_unrevealed_cells()

        # Every cell is covered, already revealed, or already flagged.
        if not candidates:
            return None

        x, y = self.rng.choice(candidates)

        return (x, y, REVEAL)
