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

    def __init__(self, difficulty, rng=None):

        # Accepting a generator makes the opponent's randomness testable.
        self.rng = rng if rng is not None else random.Random()
        self.difficulty = difficulty

    """OPPONENT TURN"""
    def take_turn(self, board):

        move = self.solve(board)

        return [move] if move is not None else []


    def helper_121(self, board, pos_1, pos_2, pos_3, clue_positions):

        x1,y1 = pos_1
        x2,y2 = pos_2
        x3,y3 = pos_3

        print("Testing: ")
        print(pos_1)
        print(pos_2)
        print(pos_3)

        cell1 = board.board_list[x1][y1]
        cell2 = board.board_list[x2][y2]
        cell3 = board.board_list[x3][y3]

        if cell1.revealed or cell2.revealed or cell3.revealed:
            return None

        if cell2.flagged:
            return None

        candidate_positions = (pos_1, pos_2, pos_3)
        pattern_mines = (1, 0, 1)
        expected_clues = (1, 2, 1)

        for clue_index, (clue_x, clue_y) in enumerate(clue_positions):
            clue = board.board_list[clue_x][clue_y]
            if not clue.revealed or clue.type != "C" or clue.clue_num != expected_clues[clue_index]:
                return None

            candidate_neighbors = {
                position
                for position in candidate_positions
                if max(abs(position[0] - clue_x), abs(position[1] - clue_y)) == 1
            }
            hidden_neighbors = set()
            flagged_neighbors = 0

            for neighbor_x in range(max(0, clue_x - 1), min(len(board.board_list) - 1, clue_x + 1) + 1):
                for neighbor_y in range(max(0, clue_y - 1), min(len(board.board_list[neighbor_x]) - 1, clue_y + 1) + 1):
                    if (neighbor_x, neighbor_y) == (clue_x, clue_y):
                        continue

                    neighbor = board.board_list[neighbor_x][neighbor_y]
                    if neighbor.flagged:
                        flagged_neighbors += 1
                    elif not neighbor.revealed:
                        hidden_neighbors.add((neighbor_x, neighbor_y))

            if not hidden_neighbors.issubset(candidate_neighbors):
                return None

            expected_remaining_mines = sum(
                pattern_mines[index]
                for index, position in enumerate(candidate_positions)
                if position in candidate_neighbors
                and not board.board_list[position[0]][position[1]].flagged
            )
            if clue.clue_num - flagged_neighbors != expected_remaining_mines:
                return None

        if not cell1.flagged:
            return(x1, y1, FLAG)

        if not cell3.flagged:
            return(x3, y3, FLAG)

        return (x2, y2, REVEAL)

    def move_121(self, board):

        cols = len(board.board_list)
        rows = len(board.board_list[0])

        # Checking horizontal possiblities

        # Loop through all
        for col in range(cols - 2):
            for row in range(rows):

                start = board.board_list[col][row]
                down1 = board.board_list[col + 1][row]
                down2 = board.board_list[col + 2][row]

                if not (start.revealed and down1.revealed and down2.revealed):
                    continue

                if not (start.type == "C" and down1.type == "C" and down2.type == "C"):
                    continue

                if not (start.clue_num == 1 and down1.clue_num == 2 and down2.clue_num == 1):
                    continue

                print("Horizontal Found at: ", col, row)
                # Check Above
                if row > 0:
                    move = self.helper_121(
                        board,
                        (col, row - 1),
                        (col + 1, row - 1),
                        (col + 2, row - 1),
                        ((col, row), (col + 1, row), (col + 2, row)),
                    )

                    if move is not None:
                        return move

                # Check Below
                if row < rows - 1:
                    move = self.helper_121(
                        board,
                        (col, row + 1),
                        (col + 1, row + 1),
                        (col + 2, row + 1),
                        ((col, row), (col + 1, row), (col + 2, row)),
                    )
                    
                    if move is not None:
                        return move

        # Check Vertical
        for col in range(cols):
            for row in range(rows - 2):

                start = board.board_list[col][row]
                down1 = board.board_list[col][row + 1]
                down2 = board.board_list[col][row + 2]
                
                if not (start.revealed and down1.revealed and down2.revealed):
                    continue
                
                if not (start.type == "C" and down1.type == "C" and down2.type == "C"):
                    continue
                
                if not (start.clue_num == 1 and down1.clue_num == 2 and down2.clue_num == 1):
                    continue

                print("Vertical Found at: ", col, row)

                if col > 0:
                    move = self.helper_121(
                        board,
                        (col - 1, row),
                        (col - 1, row + 1),
                        (col - 1, row + 2),
                        ((col, row), (col, row + 1), (col, row + 2)),
                    )
                    
                    if move is not None:
                        return move

                if col < cols - 1:
                    move = self.helper_121(
                        board,
                        (col + 1, row),
                        (col + 1, row + 1),
                        (col + 1, row + 2),
                        ((col, row), (col, row + 1), (col, row + 2)),
                    )
                                        
                    if move is not None:
                        return move

        return None
                
    def medium_move(self, board):
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
                
        return None

    """SINGLE BEST MOVE"""
    def solve(self, board):

        if self.difficulty == "Hard":
            move = self.move_121(board)
            if move is not None:
                return move

            move = self.medium_move(board)
                        
            if move is not None:
                return move
                        
            
            return self.guess(board)

        if self.difficulty == "Medium":
            move = self.medium_move(board)

            if move is not None:
                return move

            return self.guess(board)
        

        if self.difficulty == "Easy":
            return self.guess(board)

    """RANDOM GUESS"""
    def guess(self, board):

        candidates = board.get_unrevealed_cells()

        # Every cell is covered, already revealed, or already flagged.
        if not candidates:
            return None

        x, y = self.rng.choice(candidates)

        return (x, y, REVEAL)
