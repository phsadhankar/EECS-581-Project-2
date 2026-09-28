<div align="right">

# Group 20

</div>

# Minesweeper
**Version:** 1.1  
**Date:** 09/28/2026  
**Document Identifier:** MS-SAP2-1.1

# Software Architecture Document
## Version 1.1

| Date | Version | Description | Author |
|------|---------|-------------|--------|
| 09/27/2026 | 1.0 | Initial creation of Project 2 Software Architecture Document | Ivan Kullaya |
| 09/28/2026 | 1.1 | Expanded initial architecture draft based on inherited Group 18 implementation and current Easy AI implementation | Ivan Kullaya |

# Table of Contents

1. Introduction
   - 1.1 Purpose
   - 1.2 Scope
   - 1.3 Definitions, Acronyms, and Abbreviations
   - 1.4 References
   - 1.5 Overview
2. Architectural Representation
3. Architectural Goals and Constraints
   - 3.1 Architectural Goals
   - 3.2 Architectural Constraints
   - 3.3 Design Rationale
4. Use-Case View
   - 4.1 Use-Case Realizations
5. Logical View
   - 5.1 Overview
   - 5.2 Architecturally Significant Components
   - 5.3 Relationships Between Components
6. AI Solver Architecture
   - 6.1 Easy AI
   - 6.2 Medium AI
   - 6.3 Hard AI
7. Hint System Architecture
8. Data Flow
   - 8.1 Player Cell Reveal Data Flow
   - 8.2 Flag Data Flow
   - 8.3 AI Solver Data Flow
   - 8.4 Hint System Data Flow
   - 8.5 Game Reset Data Flow
9. Key Data Structures
   - 9.1 Board Representation
   - 9.2 AI-Related Data
   - 9.3 Relationship Between Data Structures
10. Interface Description
   - 10.1 Game Board
   - 10.2 Player Input
   - 10.3 AI Controls
   - 10.4 Hint Controls
   - 10.5 Game Information
11. Quality and Extensibility

# 1. Introduction

## 1.1 Purpose

This document describes the software architecture of the Minesweeper application maintained and extended by Group 20 for EECS 581 Project 2.

The original Minesweeper system was developed by Group 18 for Project 1 and inherited by Group 20 for Project 2. This document describes the organization of the inherited system as well as the architectural changes made by Group 20 to support the Project 2 requirements.

The inherited system is organized into separate modules responsible for game management, board and tile management, graphical configuration, and user interaction. Project 2 extends this architecture with an Artificial Intelligence (AI) solver supporting Easy, Medium, and Hard difficulty levels and a custom Hint System.

The purpose of this document is to provide developers with an understanding of the system's major components, interactions, data flow, key data structures, and design decisions so that the application can be maintained and extended in future development.

## 1.2 Scope

The Minesweeper application is a graphical implementation of Minesweeper developed using Python and the Pygame library. The inherited system uses a fixed 10x10 game board and allows the player to select between 10 and 20 mines when starting the application.

The inherited Project 1 system provides the following core functionality:
- A 10x10 Minesweeper board with columns labeled A-J and rows labeled 1-10.
- Random placement of the number of mines selected by the player.
- First-click safety that prevents mines from being placed on the first selected cell or its surrounding cells.
- Left-click cell revealing.
- Recursive revealing of empty regions.
- Right-click placement and removal of flags.
- Prevention of flagged cells from being uncovered.
- Calculation and display of adjacent mine counts.
- Detection of victory and loss conditions.
- Display of all mine locations after a loss.
- Restarting the game after a game has ended.
- Display of game status and remaining flags through the Pygame interface.

Project 2 extends the inherited system with three levels of AI behavior and a Hint System. At the current stage of development, the Easy AI has been integrated into the system. The Easy AI selects randomly from cells that have not already been revealed or flagged. Medium and Hard AI behavior and the Hint System will be documented further as their implementations are completed.

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

## 1.3 Definitions, Acronyms, and Abbreviations

- **AI**: Artificial Intelligence
- **Cell/Tile**: An individual position on the Minesweeper board
- **Covered Cell**: A cell that has not yet been uncovered
- **Flag**: A marker indicating a cell believed to contain a mine
- **GUI**: Graphical User Interface
- **Hint**: A limited-use feature that reveals a safe, non-mine cell
- **Mine**: A hidden game element that results in a loss when uncovered
- **MVP**: Minimum Viable Product
- **Pygame**: Python library used to implement the graphical interface
- **1-2-1 Pattern**: A Minesweeper pattern used by the Hard AI to logically determine mine and safe-cell locations

## 1.4 References

- EECS 581 Project 2 – Enhance Another Team's Minesweeper System, Professor Hossein Saiedian, Fall 2026
- Group 18 Project 1 Minesweeper implementation
- Project source code (`src/`)
- External sources and generative AI assistance identified in individual source-file prologue comments.

## 1.5 Overview

The inherited Minesweeper application uses a modular, event-driven architecture. Pygame events are processed by the Game class in main.py, which coordinates player input, overall game state, board operations, win/loss detection, and screen updates.

Board-specific behavior is separated into sprites.py. The Board class maintains the collection of Tile objects and provides operations for mine placement, clue calculation, cell revealing, and drawing the board. Each Tile object maintains the state of one board location, including its coordinates, type, clue number, revealed state, and flagged state.

Configuration values are stored separately in settings.py, including board dimensions, tile size, window dimensions, frame rate, interface colors, and AI configuration values.

Project 2 additionally introduces ai_solver.py, which separates AI decision-making from the main game and board-management code. The current Easy AI implementation identifies valid covered cells and randomly selects one to reveal. The Game class coordinates when an AI turn occurs, while the Board class executes the AI's requested action.

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

# 2. Architectural Representation

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

# 3. Architectural Goals and Constraints

## 3.1 Architectural Goals

The primary architectural goals of the Project 2 Minesweeper system are:

- **Correctness:** All Project 1 Minesweeper functionality and Project 2 additions should operate according to the project requirements.
- **Maintainability:** Components should be organized so that functionality can be modified without unnecessarily affecting unrelated parts of the system.
- **Reliability:** The system should handle valid and invalid player/AI actions without crashing.
- **Usability:** The graphical interface should clearly communicate the board state, game status, AI controls, and Hint System.
- **Extensibility:** The system should support future additions to game logic, AI behavior, and interface features.
- **Modularity:** Major responsibilities should remain divided among separate modules and classes rather than being combined into a single source file.

## 3.2 Architectural Constraints

### Project 1 Constraints

The inherited system must continue satisfying the original Minesweeper requirements:
- The board contains exactly 10 rows and 10 columns.
- Columns are labeled A-J and rows are labeled 1-10.
- The player selects between 10 and 20 mines.
- Mines are placed randomly.
- Mine placement occurs after the player's first valid selection.
- The first selected tile and the eight surrounding positions are excluded from mine placement when those positions are within the board.
- Covered cells may be flagged and unflagged.
- Flagged cells cannot be uncovered.
- Empty cells recursively reveal neighboring cells.
- The game detects victory when all non-mine cells have been revealed.
- Uncovering a mine results in a loss and causes all mines to be displayed.
- The game can be restarted after completion.

### Project 2 Constraints

Project 2 adds the following architectural requirements:
- The inherited system must continue using Python and Pygame.
- All required Project 1 functionality must remain operational.
- Easy AI must randomly uncover valid hidden cells while avoiding revealed and flagged cells.
- Medium AI must apply the two required logical deduction rules before falling back to a random selection.
- Hard AI must include the Medium rules and additionally recognize the required 1-2-1 pattern.
- AI actions must operate on the same game board as player actions.
- Random AI selections must exclude revealed and flagged cells.
- The custom Hint System must identify and reveal a safe cell.
- Hint usage must be limited.

## 3.3 Design Rationale

The inherited Group 18 architecture was retained and extended rather than replaced. Project 2 requires Group 20 to use the same programming language and platform as the inherited Project 1 team. Because Group 18 implemented the Minesweeper system using Python and Pygame, Group 20 continued development using Python and Pygame.

The existing modular structure was also retained where possible to reduce unnecessary changes to working Project 1 functionality. The inherited system separates major responsibilities among main.py, sprites.py, and settings.py. main.py manages the overall game and player interaction, sprites.py manages the board and individual tiles, and settings.py contains shared configuration values.

For Project 2, the architecture was extended with ai_solver.py to separate AI decision-making from the existing game and board logic. This allows the AI strategies to be developed without placing all AI logic directly into the inherited Project 1 components. The AI determines which action should occur, while the existing game and board components remain responsible for executing actions and updating the game state.

This separation also supports the three required AI difficulty levels. Easy AI uses random selection, while Medium and Hard AI can add additional decision-making rules while continuing to interact with the same board and game components.

The Hint System will also be integrated into the inherited architecture while minimizing changes to existing Project 1 behavior. Its final architectural design and interactions will be documented after the feature is completed.

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

# 4. Use-Case View

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED AND COLLABORATE WITH GAEL FOR UML DIAGRAM`)

## 4.1 Use-Case Realizations

### Start or Reset Game

### Uncover Cell

### Place or Remove Flag

### Use AI Solver

### Easy AI Turn

### Medium AI Turn

### Hard AI Turn

### Request Hint

### Victory

### Loss

# 5. Logical View

## 5.1 Overview

The current Project 2 implementation consists primarily of the following source files:

### `main.py`

Responsible for:

- Initializing Pygame.
- Creating and controlling the application window.
- Creating and resetting the Board.
- Processing player mouse input.
- Managing first-click behavior.
- Coordinating player and AI turns.
- Maintaining overall game state.
- Tracking flags.
- Detecting win and loss conditions.
- Updating the graphical display.
- Restarting the game after completion.

### `settings.py`

Responsible for:

- Board dimensions.
- Tile dimensions.
- Window dimensions and margins.
- Frame-rate settings.
- Window title.
- Interface colors.
- Clue-number colors.
- AI autoplay configuration.
- AI move delay.

### `sprites.py`

Responsible for:

- Defining the Tile class.
- Defining the Board class.
- Creating the collection of Tile objects.
- Random mine placement.
- Creating the first-click safe area.
- Calculating clue values.
- Revealing cells.
- Recursive revealing of empty areas.
- Tracking Tile reveal and flag states.
- Drawing the board.
- Identifying valid cells for AI actions.
- Executing AI reveal and flag actions.

### `ai_solver.py`

Responsible for:

- Defining the MinesweeperAI class.
- Determining AI actions.
- Selecting valid random cells for Easy AI.
- Providing the decision-making location for Medium and Hard AI strategies.

### Hint System

The location and organization of the Hint System will be documented after its final implementation is integrated into the inherited
system.

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

## 5.2 Architecturally Significant Components

### User Interface

The user interface is implemented using Pygame. The Game class manages the overall display while the Board class draws the individual tiles.

The interface communicates the current state of the game by displaying the board, coordinate labels, covered and revealed cells, flags, clue numbers, mines, remaining flags, and game status.

### Board Management

The Board class maintains the Minesweeper board as a two-dimensional collection of Tile objects.

The Board is responsible for creating tiles, placing mines, creating the safe region around the first selected cell, calculating clue numbers, uncovering cells, recursively uncovering empty areas, and rendering the board.

### Tile Management

Each location on the board is represented by a Tile object. A Tile stores its board coordinates, underlying type, clue number, revealed state, and flagged state.

The Tile representation allows the different parts of the application to obtain the complete state of a board location through one object.

### Game State Management

The Game class manages the overall state of the current game. This includes whether gameplay is active, whether the first click has occurred, the selected number of mines, number of flags placed, game-over status, victory status, and winner.

Project 2 additionally tracks whether the player has performed an action requiring an AI response.

### AI Solver

AI decision-making is separated into the MinesweeperAI class in ai_solver.py.

The AI receives the current Board and determines an action. The current Easy AI selects randomly among valid covered and unflagged cells.

The same AI component will be extended with the logical rules required by Medium and Hard difficulty without requiring the core Board representation to be replaced.

### Hint System

The Hint System will provide limited assistance by selecting a covered safe tile and revealing it for the player.

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

### Win/Loss Management

Win and loss conditions are coordinated by the Game class.

A win occurs when no safe tiles remain covered. A loss occurs when a mine is uncovered. Project 2 additionally identifies whether a completed game resulted from the player's or AI's actions.

### Game Reset

A new game creates a new Board and resets the relevant game-state values. Mine placement is delayed until the player's first valid selection so the first-click safe region can be established.

## 5.3 Relationships Between Components

main.py acts as the primary coordinator between the player, Pygame interface, Board, and AI solver.

Player mouse events are received by the Game. Valid board coordinates are then used to modify Tile state through the Board.

On the first valid reveal, the Game requests mine placement and clue calculation before revealing the selected tile. Later reveals use the existing Board state.

The AI receives the Board so that it can determine which cells are eligible for an action. After making a decision, the AI returns an action to the Game. The Game then passes that action to the Board, which modifies the appropriate Tile.

settings.py provides shared configuration values used by the other components. This prevents constants such as board dimensions, colors, and AI settings from being repeatedly defined throughout the application.

The Board and Game display their current state through Pygame. As Tile and game-state values change, subsequent screen updates reflect those changes.

The final relationship between the Hint System and these components will be documented after the feature has been implemented.

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

# 6. AI Solver Architecture

## 6.1 Easy AI

### Purpose

The Easy AI provides the simplest automated Minesweeper behavior.

### Behavior

- Identifies valid hidden cells.
- Excludes uncovered cells.
- Excludes flagged cells.
- Randomly selects one remaining valid cell.
- Returns a REVEAL action for the selected cell.
- The Board executes the action using the existing cell-reveal functionality.

### Relevant Functions/Classes

| Function/Class | Purpose |
|:---:|:---:|
| MinesweeperAI | Encapsulates AI decision-making. |
| take_turn() | Requests an AI move and returns the action to the Game. |
| solve() | Main decision point for selecting an AI action. |
| guess() | Randomly selects an eligible covered cell. |
| Board.get_unrevealed_cells() | Returns cells that are neither revealed nor flagged. |
| Board.execute_ai_action() | Executes a reveal or flag action requested by the AI. |
| Game.play_ai_turn() | Coordinates the AI turn and handles the resulting game state. |

## 6.2 Medium AI

### Purpose

The Medium AI attempts to make logical moves using information visible on the board before falling back to a random selection.

### Rule 1 – Flag Mines

If the number of hidden neighbors of a revealed cell equals the cell's displayed number, all hidden neighbors are flagged.

### Rule 2 – Reveal Safe Cells

If the number of flagged neighbors equals the displayed number, all other hidden neighbors are safe and may be uncovered.

### Random Fallback

If neither rule produces a valid action, the AI performs the same random selection behavior used by Easy AI.

### Relevant Functions/Classes

| Function/Class | Purpose |
|---|---|
| `[NAME]` | [DESCRIPTION] |
| `[NAME]` | [DESCRIPTION] |

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

## 6.3 Hard AI

### Purpose

The Hard AI extends Medium AI behavior by recognizing the required 1-2-1 Minesweeper pattern.

### Behavior

1. Attempt Medium AI rules.
2. Search for a valid 1-2-1 pattern.
3. Determine mine and safe-cell positions from the pattern.
4. Flag logically identified mines.
5. Uncover logically identified safe cells.
6. If no logical move exists, perform a random valid selection.

### Relevant Functions/Classes

| Function/Class | Purpose |
|:---::---:|
| `[NAME]` | [DESCRIPTION] |
| `[NAME]` | [DESCRIPTION] |

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

# 7. Hint System Architecture

## 7.1 Purpose

The Hint System provides limited assistance to the player during a Minesweeper game.

When the player requests a hint, the system identifies a covered cell that does not contain a mine and safely reveals that cell.

The number of hints available during a game is limited so that the feature provides assistance without removing the challenge of the game.

## 7.2 Behavior

1. The player requests a hint.
2. The system determines whether any hints remain.
3. Eligible covered cells are identified.
4. Mine cells are excluded.
5. A safe eligible cell is selected.
6. The selected cell is revealed.
7. The remaining hint count is decreased.
8. The interface is updated.

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

## 7.3 Relevant Functions/Classes

| Function/Class | Purpose |
|:---:|:---:|
| `[NAME]` | [DESCRIPTION] |
| `[NAME]` | [DESCRIPTION] |

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

## 7.4 UML Diagram

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED AND COLLABORATE WITH GAEL FOR UML DIAGRAM`)

# 8. Data Flow

The Project 2 Minesweeper application uses event-driven data flow. Player actions originate through the Pygame interface and are processed by the Game. The Game coordinates Board operations and AI actions, while changes to Tile and game-state data are reflected during subsequent display updates.

## 8.1 Player Cell Reveal Data Flow

When the player left-clicks a valid covered tile, the Pygame event handler determines the corresponding board coordinates.

On the first valid reveal, the Board places mines while excluding the safe region surrounding the selected cell. Clue values are then calculated before the cell is revealed.

Board.dig() processes the selected tile. Empty tiles may cause neighboring cells to be recursively uncovered. After the reveal, the Game checks for a loss or victory and updates the display.

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

## 8.2 Flag Data Flow

When the player right-clicks a covered cell, the Game determines the corresponding Tile and verifies that the cell is eligible to be flagged.

If the cell is currently unflagged and additional flags are available, its flagged state is set to true. If it is already flagged, the flag is removed.

The Game recounts the number of flags currently placed and the Board's next display update reflects the new Tile state.

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

## 8.3 AI Solver Data Flow

An AI turn begins after the Game determines that the player has completed a valid action and AI autoplay is enabled.

The Game requests an action from MinesweeperAI. The selected AI strategy examines the current Board and returns one or more actions.

Easy AI selects randomly among eligible cells. Medium AI will first attempt its required logical rules, while Hard AI will additionally attempt the 1-2-1 pattern. If no logical action is available, Medium and Hard fall back to random selection.

The resulting action is sent to Board.execute_ai_action(), which modifies the Board. The Game then updates flag counts if necessary and checks the resulting win/loss state.

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

## 8.4 Hint System Data Flow

The Hint System data flow begins when the player requests a hint. The system verifies that a hint remains available and then identifies eligible covered safe cells.

A safe cell is selected and revealed, the remaining hint count is reduced, and the new state is displayed.

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

## 8.5 Game Reset Data Flow

A new game begins by creating a new Board and resetting game-state information.

The reset process clears the previous board, mines, revealed states, flags, game result, first-click status, AI-turn state, and other information associated with the previous round. Project 2 Hint System state will also be reset once that feature is integrated.

The new game then waits for the player's first valid reveal before placing mines.

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

# 9. Key Data Structures

The Project 2 Minesweeper system uses an object-based representation of the game board. A Board contains a two-dimensional collection of Tile objects, and each Tile stores the state associated with an individual board position.

| Structure / Variable | Type | Description |
|:---:|:---:|:---:|
| board_list | 2D list of Tile objects | Represents the Minesweeper board. |
| Tile.type | String | Identifies the underlying tile as empty, mine, or clue. |
| Tile.revealed | Boolean | Records whether a tile has been uncovered. |
| Tile.flagged | Boolean | Records whether a tile is currently flagged. |
| Tile.clue_num | Integer | Stores the number of adjacent mines for a clue tile. |
| Board.dug | Set | Stores coordinates visited during recursive revealing. |
| Game.num_mines | Integer | Stores the selected number of mines. |
| Game.flags_placed | Integer | Stores the current number of placed flags. |
| Game.first_click | Boolean | Records whether mine placement is still required. |
| Game.playing | Boolean | Records whether active gameplay is occurring. |
| Game.game_over | Boolean | Records whether the game has ended. |
| Game.win | Boolean | Records whether a victory has occurred. |
| Game.winner | String/None | Identifies the player or AI as the winner. | 
| Game.player_moved | Boolean | Determines whether an AI response should occur. |

## 9.1 Board Representation

The game board is stored in Board.board_list as a two-dimensional collection of Tile objects.

Each Tile contains its x- and y-coordinates as well as the state needed to represent that board location.

Mines are represented by a Tile type of 'X'. Empty tiles initially use '.'. Non-mine cells adjacent to one or more mines are represented as clue cells, with their adjacent mine count stored in Tile.clue_num.

A Tile's revealed state is represented by Tile.revealed, while its flag state is represented independently by Tile.flagged.

This representation allows the Board, Game, display logic, and AI to access information about a board position through the same Tile object.

## 9.2 AI-Related Data

The Easy AI does not maintain a separate copy of the board. Instead, the current Board object is supplied to the AI when a decision is requested.

Board.get_unrevealed_cells() creates a temporary list of coordinates representing cells that are neither revealed nor flagged. MinesweeperAI.guess() randomly selects from these coordinates.

An AI action contains an x-coordinate, y-coordinate, and action type. The current Easy AI returns a REVEAL action. The Board's AI-action interface also supports FLAG, allowing Medium and Hard AI strategies to perform logical flagging.

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

## 9.3 Relationship Between Data Structures

The Board owns the collection of Tile objects representing the current game. Each Tile stores its own mine/clue type, reveal state, flag state, and clue number.

The Game owns the Board and maintains information about the overall game state. The AI reads the Board when selecting an action but does not currently maintain an independent copy of the board.

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

# 10. Interface Description

## 10.1 Game Board

The graphical game board is displayed using Pygame and consists of a 10x10 collection of tiles.

Columns are labeled A through J and rows are labeled 1 through 10 to identify board coordinates.

Covered tiles are displayed without exposing their underlying contents. Revealed clue tiles display their number of adjacent mines, while revealed empty tiles display no clue number. Flagged tiles display a flag indicator.

When a mine is revealed, the mine locations are displayed to indicate the loss condition.

## 10.2 Player Input

| Input | Result |
|:---:|:---:|
| Left-click covered cell | Attempts to reveal the selected tile. |
| Right-click covered cell | Places or removes a flag when the action is valid. |
| Left-click after game over | Starts a new game according to the current restart behavior. |

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

## 10.3 AI Controls

The current Project 2 implementation uses an AI autoplay setting stored in settings.py.

When AI autoplay is enabled, the AI receives a turn after a valid player action. Game.play_ai_turn() requests the AI action and applies it to the same Board used by the player.

The current Easy AI automatically uses random selection.

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

## 10.4 Hint Controls

The final player control for requesting a hint and the display of remaining hints will be documented after the Hint System is integrated.

The interface should communicate the number of hints remaining and prevent additional hints after the allowed number has been used.

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

## 10.5 Game Information

The interface currently displays information necessary for the player to understand the current game state, including:

- Remaining flags.
- Game status.
- Board coordinates.
- Revealed clue values.
- Flagged tiles.
- Win/loss information.
- Player/AI result information when AI autoplay is active.

The final interface documentation should additionally identify the selected AI difficulty and remaining Hint System uses if those values are displayed in the completed implementation.


# 11. Quality and Extensibility

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

### Maintainability

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

### Reliability

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

### AI Extensibility

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

### Feature Extensibility

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

### Known Architectural Limitations

(`AUTHORS NOTE TO FINISH SECTION WHEN CODE FINISHED`)

---

© Group 20, 2026
