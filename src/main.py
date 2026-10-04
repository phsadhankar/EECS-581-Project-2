"""
Module: main.py

Description: 
    Controls the main Minesweeper game, including the Pygame window,
    game state, player input, and interaction with the game board.

Inputs:
    - Number of mines selected by the user (10-20)
    - Mouse input

Outputs:
    A playable Pygame Minesweeper game window

Editors: John Pannell and Jake Crawford

Creation Date: 09/19/26

External Sources: 
    - ChatGPT (GPT-5.6 Luna): Used for explanations and integration assistance. See AI Use Disclosure below.
    - Tech & Gaming, "How to make Minesweeper in Pygame - Step-by-Step Tutorial for beginner":
      https://www.youtube.com/watch?v=n0jZRlhLtt0
      Used as the starting point for the Minesweeper Pygame implementation.

AI Use Disclosure:

    AI Tool: ChatGPT (GPT-5.6 Luna)

    Use of AI: AI was used to assist with the integration and revision of existing 'main.py' code with other project components and
    existing functions. The AI was also used to help understand Pygame-specific syntax and how 'main.py' interacts with functions and data
    from other source files.

    Prompt: The following prompt is representative of the prompts used to assist with integration between components:
        "Given our architectural components and other source files, assist in editing the Game class to ensure integration, correct logic, 
        and reducing complexity. Any suggested changes must be explained so they can be reviewed and understood."

    Changes After AI Assistance: All suggested code changes were reviewed and understood by the editors before being used. One change that was implemented 
    was the use of 'continue' statements in the 'events()' method to reduce unnecessary nested 'if' statements. AI assistance was also used to explain Pygame
    syntax related to initializing the screen, display, title, clock, and event handling. The editors verified the logic and made final decisions about which
    changes were incorporated into the file.
"""

import sys
import pygame
from settings import *
from sprites import Board
from ai_solver import (
    AIMode,
    ActionType,
    Difficulty,
    MinesweeperSolver,
    observation_from_board,
)

AI_STEP_DELAY_MS = 850

class Game:
    """
    Manages the overall Minesweeper game.

    The Game class initializes the Pygame window, manages the game state,
    processes player input, coordinates the game board and game logic,
    and controls the main game loop to ensure efficient gameplay.

    Inputs:
        num_mines: The number of mines selected by the user, from 10 to 20
        
    Member Variables:
        - screen: The Pygame window used to display the game.
        - clock: Controls the game's frame rate.
        - font: Font used to display text in the game window.
        - num_mines: The number of mines the user selects.
        - flags_placed: The number of flags on the board currently.
        - board: The current Minesweeper board.
        - playing: Indicates whether the game is being played or not currently.
        - first_click: Indicates whether the game is waiting for the first click.
        - game_over: Indicates whether the game has ended.
        - win: Indicates if the player has won the game.

    Outputs:
        An interactive Pygame Minesweeper game.
    """

    def __init__(
        self,
        num_mines,
        ai_mode=AIMode.HUMAN_ONLY,
        difficulty=Difficulty.EASY,
    ):
        """
        Initializes the Minesweeper game and the Pygame components.

        Inputs:
            num_mines: The number of mines selected by the user, 10 to 20.

        Outputs:
            None. Initializes the Game object's attributes and Pygame components.
        """

        # Combined: Syntax for Pygame initialization assistance necessary
        pygame.init() # initialize Pygame
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # create the Pygame window using width/height from settings.py
        pygame.display.set_caption(TITLE) # set the title of the Pygame window
        self.clock = pygame.time.Clock() # create a clock to control frame rate
        self.font = pygame.font.SysFont("Arial", 18, bold=True) # create font used to display text

        # Combined: Initialize the member variables
        self.num_mines = num_mines
        self.flags_placed = 0
        self.board = None
        self.playing = False
        self.first_click = True
        self.game_over = False
        self.win = False
        self.ai_mode = AIMode(ai_mode)
        self.difficulty = Difficulty(difficulty)
        self.solver = MinesweeperSolver(self.difficulty)
        self.ai_turn = False
        self.ai_paused = False
        self.next_ai_step = 0

    def run(self):
        """
        Runs the main Minesweeper loop for the game to take place.

        A new game board is created, the game state is reset, player input is processed,
        the game display is updated, and the game-over screen is handled.

        Inputs:
            None.
        
        Outputs:
            None. Runs the game and manages the game and game-over loops.
        """

        # Combined: Outer loop that allows a new game to start after reset occurs
        while True:
            self.board = Board()
            self.playing = True
            self.first_click = True
            self.game_over = False
            self.win = False
            self.flags_placed = 0
            self.solver.reset()
            self.ai_turn = self.ai_mode is AIMode.AUTOMATIC
            self.ai_paused = False
            self.next_ai_step = pygame.time.get_ticks() + AI_STEP_DELAY_MS

            # The main gameplay loop that keeps the game running while the player is still in progress
            while self.playing:
                self.events() # process inputs and game events
                self.advance_ai()
                self.draw() # update the display of the game
                self.clock.tick(FPS) # Combined: syntax to control the game loop speed necessary

            # Game-over loop that displays the end screen until restart
            while self.game_over:
                self.end_screen() # display the game-over or victory screen and wait for input
                self.clock.tick(FPS) # Combined: syntax to control the game-over loop speed necessary       

    def events(self):
        """
        Handles game events and player inputs.

        The following method handles closing the game window, left mouse click for uncovering cells,
        and right mouse click for placing or removing flags. It also handles the first-click mine placement
        and updates the state of the game when a mine is uncovered.

        Inputs:
            None. Receives player input from Pygame event.

        Outputs:
            None. Updates the game board and game state.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type != pygame.MOUSEBUTTONDOWN:
                continue

            if self.game_over or not self.playing:
                continue
            if self.ai_mode is AIMode.AUTOMATIC:
                continue
            if self.ai_mode is AIMode.INTERACTIVE and self.ai_turn:
                continue

            mouse_x, mouse_y = event.pos

            if mouse_x < MARGIN_LEFT or mouse_y < MARGIN_TOP:
                continue

            col = (mouse_x - MARGIN_LEFT) // TILESIZE
            row = (mouse_y - MARGIN_TOP) // TILESIZE
        
            if not (0 <= col < COLS and 0 <= row < ROWS):
                continue

            tile = self.board.board_list[col][row]
            changed = False

            if event.button == 1:
                changed = self.reveal_cell(col, row)
            elif event.button == 3:
                changed = self.toggle_flag(col, row)

            if (
                changed
                and self.playing
                and self.ai_mode is AIMode.INTERACTIVE
            ):
                self.ai_turn = True

    def reveal_cell(self, col, row):
        """Reveal through the same Board logic for both the player and AI."""
        tile = self.board.board_list[col][row]
        if self.game_over or tile.revealed or tile.flagged:
            return False

        if self.first_click:
            self.board.place_mines(col, row, self.num_mines)
            self.board.place_clues()
            self.first_click = False

        safe = self.board.dig(col, row)
        if not safe:
            self.playing = False
            self.game_over = True
            self.reveal_all_mines()
            return True

        self.check_win()
        return True

    def toggle_flag(self, col, row):
        """Apply a flag change and keep the counter within the mine limit."""
        tile = self.board.board_list[col][row]
        if self.game_over or tile.revealed:
            return False

        if tile.flagged:
            tile.flagged = False
            self.flags_placed -= 1
            return True

        if self.flags_placed >= self.num_mines:
            return False

        tile.flagged = True
        self.flags_placed += 1
        return True

    def advance_ai(self):
        """Perform at most one scheduled AI action through game logic."""
        if self.game_over or not self.playing or self.ai_paused:
            return
        if self.ai_mode is AIMode.HUMAN_ONLY:
            return
        if self.ai_mode is AIMode.INTERACTIVE and not self.ai_turn:
            return

        now = pygame.time.get_ticks()
        if self.ai_mode is AIMode.AUTOMATIC and now < self.next_ai_step:
            return

        self.next_ai_step = now + AI_STEP_DELAY_MS
        observation = observation_from_board(self.board)
        action = self.solver.next_action(
            observation,
            can_flag=self.flags_placed < self.num_mines,
        )

        if action is None:
            self.ai_paused = True
            self.ai_turn = False
            return

        if action.action_type is ActionType.REVEAL:
            self.reveal_cell(action.col, action.row)
        else:
            self.toggle_flag(action.col, action.row)

        if self.ai_mode is AIMode.INTERACTIVE and self.playing:
            self.ai_turn = False

    """REVEAL ALL MINES FUNCTION"""
    def reveal_all_mines(self):
        """
        This function is used when the player loses. It loops through every
        tile on the board, checks whether the tile is a mine by looking for an X,
        and if it is a mine, it changes its revealed value to true so that all the mines
        become visible. 
        """

        # Show where all mines were once the player loses

        # This will go through every column and row on the board.
        for x in range(COLS):
            for y in range(ROWS):

                # If the tile is a mine, reveal it
                if self.board.board_list[x][y].type == 'X':
                    self.board.board_list[x][y].revealed = True

    """Check for a win condition"""
    def check_win(self):
        """ 
        This funciton checks whether the player has won. That it will go through
        the entire board and counts any tiles that are still covered but aren't mines.
        If that count reaches zero, there aren't safe tiles left to uncover, so
        the game ends and the player is marked as the winner. 
        """

        # Count remaining non-mine tiles
        # This function will check if the player has revealed every non-mine tile.

        # This is the initial start number of the unrevealed safe tiles at zero. 
        unrevealed_safe = 0

        # This will search every tile on the board to see if it is a mine or not. 
        # If it is not a mine and it is not revealed, it will add to the unrevealed safe count.
        for x in range(COLS):
            for y in range(ROWS):
                if not self.board.board_list[x][y].revealed and self.board.board_list[x][y].type != 'X':
                    unrevealed_safe += 1
        
        #The winning declaration will be made as soon as the unrevealed safe count is equal to zero.    
        # If all safe cells are revealed, you win
        if unrevealed_safe == 0:
            self.playing = False
            self.game_over = True
            self.win = True



    """DRAW THE GAME SCREEN """
    # This function will update everything the player will see on the screen.
    # It will display the game status, such as the flags left, board labels
    # and the actual Minesweeper board.
    def draw(self):
        """
        The draw funciton controls the overall game display. It clears the previous
        Screen determines whether the status should say Playing, Game Over, or Victory,
        displays the number of flags remaining, creates the A through J and 1 through 10 labels,
        tells the board to draw the tiles, and then updates the Pygame window. 
        """

        # This will clear the old screen by filling it in with a background color.
        self.screen.fill(BG_COLOR)
        
        # The Game status!
        # This will display the current status on the game at the top of the screen.

        if self.win:
            status_msg = "Victory! (Click to Restart)"

        elif self.game_over:
            status_msg = "Game Over (Click to Restart)"

        else:
            if self.ai_mode is AIMode.INTERACTIVE:
                turn_status = "AI turn" if self.ai_turn else "Your turn"
                status_msg = f"{self.difficulty.value.title()}: {turn_status}"
            elif self.ai_mode is AIMode.AUTOMATIC:
                status_msg = f"Auto: {self.difficulty.value.title()}"
            else:
                status_msg = "Playing"


        # HUD TEXT

        # Create the status and remaining-flags text.
        status = self.font.render(f"Status: {status_msg}", True, TEXT_COLOR)

        # Flags left = total mines - flags already placed.
        mines = self.font.render(f"Flags Left: {self.num_mines - self.flags_placed}", True, TEXT_COLOR)

        # This will put the text onto the game window.
        self.screen.blit(status, (20, 15))
        self.screen.blit(mines, (WIDTH - 150, 15))

        # Render column headers A through J
        cols_text = "ABCDEFGHIJ"
        for i in range(COLS):
            lbl = self.font.render(cols_text[i], True, TEXT_COLOR)
            self.screen.blit(lbl, (MARGIN_LEFT + (i * TILESIZE) + 14, MARGIN_TOP - 25))

        # Render row numbers 1 through 10
        for i in range(ROWS):
            lbl = self.font.render(str(i + 1), True, TEXT_COLOR)
            offset = 25 if i < 9 else 32  # Extra padding for "10"
            self.screen.blit(lbl, (MARGIN_LEFT - offset, MARGIN_TOP + (i * TILESIZE) + 8))

        # Draw actual tiles
        self.board.draw(self.screen, self.font)
        pygame.display.flip()

    def end_screen(self):
        """
        The end-screen function handles the game after a win or loss. It still checks
        whether the player closes the window, and if they click the mouse, it leaves the 
        game-over state so another round can begin. While waiting, it continues drawing the 
        finished board. 
        """

        # This function will handle what happens after the player wins or loses.

        # Freeze frame; reset game state on click
        for event in pygame.event.get():

            # If the player closes the window, exit the game.
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # If the player clicks the mouse, leave the game over state and start a new round.
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.game_over = False  # Break out to start a new round

    # Keep displaying the finished baord while the game is over.
        self.draw()


if __name__ == "__main__":
    """
    This is the starting point of the program. It asks the player to select between
    10 and 20 mines and validates the input. Once a valid number is entered, it creates
    the Game object using that mine count and calls game.run() to start Minesweeper. 
    """

    # This is where the Minesweeper program starts.
    print("=== EECS 581: Minesweeper ===")

    mode_choices = {
        "1": AIMode.HUMAN_ONLY,
        "2": AIMode.INTERACTIVE,
        "3": AIMode.AUTOMATIC,
    }
    print("1) Player only")
    print("2) Player and AI (take turns)")
    print("3) AI automatic play")
    while True:
        mode_choice = input("Choose a mode (1-3): ").strip()
        if mode_choice in mode_choices:
            ai_mode = mode_choices[mode_choice]
            break
        print("Please enter 1, 2, or 3.")

    difficulty = Difficulty.EASY
    if ai_mode is not AIMode.HUMAN_ONLY:
        difficulty_choices = {
            "1": Difficulty.EASY,
            "2": Difficulty.MEDIUM,
            "3": Difficulty.HARD,
        }
        print("1) Easy: random covered cell")
        print("2) Medium: direct clue deductions, otherwise random")
        print("3) Hard: Medium plus a constrained 1-2-1 rule")
        while True:
            difficulty_choice = input("Choose AI difficulty (1-3): ").strip()
            if difficulty_choice in difficulty_choices:
                difficulty = difficulty_choices[difficulty_choice]
                break
            print("Please enter 1, 2, or 3.")
    
    # Keep asking until the player enters a valid number of mines between 10 and 20.
    while True:
        try:

            #Ask the player to choose between 10 and 20 mines for the game.
            val = input("Enter number of mines (10 to 20): ").strip()

            #covert the player's input into an integer.
            num = int(val)

            # If the number is between 10 and 20, then accept it. 
            if 10 <= num <= 20:
                break
            print("Please enter a number between 10 and 20.")

            # If the player did not enter an integer, show an error message.
        except ValueError:
            print("Invalid input, must be an integer.")

    # Create the game using the players selected number of mines.
    game = Game(num, ai_mode=ai_mode, difficulty=difficulty)

    # Start running the Minesweeper game loop.
    game.run()
