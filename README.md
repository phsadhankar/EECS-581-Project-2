<a id="readme-top"></a>

<h3 align="center">EECS 581 - Group 20 Project 2</h3>

<p align="center">
  Minesweeper System Enhancement
  <br />
  Software Maintenance and AI Solver Extension
  <br />
  <a href="https://github.com/phsadhankar/EECS-581-Project-2/tree/feature-branch/docs"><strong>Explore the docs »</strong></a>
  <br />
  <a href="https://github.com/phsadhankar/EECS-581-Project-2/tree/feature-branch/src"><strong>See the code »</strong></a>
  <br />
  <a href="https://github.com/phsadhankar/EECS-581-Project-2/tree/feature-branch/test"><strong>Check out tests »</strong></a>
  <br />
</p>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#inherited-system">Inherited System</a>
    </li>
    <li>
      <a href="#project-2-enhancements">Project 2 Enhancements</a>
      <ul>
        <li><a href="#ai-solver">AI Solver</a></li>
        <li><a href="#custom-addition">Custom Addition</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#repository-structure">Repository Structure</a></li>
    <li><a href="#system-documentation">System Documentation</a></li>
    <li><a href="#testing">Testing</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This project is developed as part of EECS 581 – Software Engineering II at the University of Kansas.

For Project 2, Group 20 inherited the Minesweeper system originally developed by Group 18 during Project 1. The purpose of this project is to practice software maintenance by understanding, maintaining, and extending an existing software system.

Group 20 is responsible for ensuring that all required Project 1 functionality remains operational while extending the system with an Artificial Intelligence (AI) Minesweeper solver and a custom game enhancement.

The inherited system is written in Python and uses Pygame for its graphical interface.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- INHERITED SYSTEM -->
## Inherited System

The original Group 18 system provides a single-player Minesweeper game played on a 10x10 grid.

The inherited system includes:

- 10x10 Minesweeper grid
- Configurable mine count between 10 and 20
- Random mine placement
- Guaranteed safe first click and surrounding cells
- Recursive uncovering of empty cells
- Cell flagging and unflagging
- Remaining flag tracking
- Win and loss detection
- Game restart functionality
- Graphical interface using Pygame

As part of Project 2, Group 20 will maintain and test the inherited functionality to ensure that all required Project 1 features remain operational.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- PROJECT 2 ENHANCEMENTS -->
## Project 2 Enhancements

Project 2 extends the inherited Minesweeper system with an AI solver and one custom game enhancement.

### AI Solver

The AI solver supports three difficulty levels: **Easy, Medium, and Hard**.

#### Easy

The Easy AI:

- Randomly selects covered cells.
- Avoids cells that have already been uncovered.
- Avoids cells that have been flagged.

#### Medium

The Medium AI applies two basic Minesweeper deduction rules before selecting a cell randomly.

**Rule 1 – Flagging Mines**

If the number of hidden neighbors of a revealed cell equals the number displayed on that cell, the AI flags all of those hidden neighbors.

**Rule 2 – Uncovering Safe Cells**

If the number of flagged neighbors of a revealed cell equals the number displayed on that cell, the AI uncovers all remaining hidden neighbors.

If neither rule can determine a move, the AI selects a valid hidden cell randomly.

#### Hard

The Hard AI applies all rules used by the Medium AI and additionally recognizes the **1-2-1 pattern**.

When three appropriate side-by-side revealed cells form a 1-2-1 pattern, the AI can logically determine which neighboring cells should be flagged as mines and which cell can safely be uncovered.

If no logical rule can determine a move, the AI selects a valid hidden cell randomly.

### Custom Addition

**Feature:** Hint Feature

The Hint System allows the player to request a limited number of hints during a game. When a hint is used, the system identifies and reveals a safe, non-mine cell on the board. The limited number of uses provides assistance to the player while maintaining the challenge of the game.

The design of the custom feature will be documented using a UML diagram based on concepts from EECS 348.

See the [docs](docs) folder for the UML diagram and additional design information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Follow these steps to run the enhanced Minesweeper system locally.

### Prerequisites

- Python 3.13
- Pygame
- Git

### Installation

1. Clone the repository

   - git clone https://github.com/phsadhankar/EECS-581-Project-2/tree/feature-branch

2. Navigate into the project directory

   - cd EECS-581-Project-2/src

3. Install Pygame (if needed)

   - python3 -m pip install pygame

4. Run the program

   - python3 main.py

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

When the game begins, the player selects the number of mines to place on the board. The number of mines must be between **10 and 20**.

The game is played on a **10x10 grid**, with columns labeled **A–J** and rows numbered **1–10**.

Players can:

- Uncover a covered cell
- Place a flag on a suspected mine
- Remove a previously placed flag
- View the number of remaining flags
- View the current game status

The first selected cell and its surrounding cells are guaranteed to be mine-free.

When a mine-free cell is uncovered, the cell displays a number representing the number of mines in the surrounding cells. Empty cells automatically uncover neighboring safe cells until numbered boundary cells are reached.

Project 2 additionally introduces an AI solver capable of playing Minesweeper at Easy, Medium, and Hard difficulty levels.

### Winning

The game is won when all non-mine cells have been uncovered.

### Losing

If a mine is uncovered, the game ends and the mines are revealed.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

### Project 1 Functionality

- [x] Verify game setup functionality
- [x] Verify gameplay functionality
- [x] Verify mine flagging
- [x] Verify player interface
- [x] Verify win/loss detection
- [x] Fix inherited bugs if necessary

### AI Solver

- [x] Easy AI
- [x] Medium AI
- [ ] Hard AI
- [ ] Random fallback behavior
- [ ] AI testing

### Custom Addition

- [x] Select custom feature
- [ ] Design custom feature
- [ ] Create UML diagram
- [ ] Implement custom feature
- [ ] Test custom feature

### Documentation and Testing

- [x] Person-hours estimate
- [ ] Actual person-hours accounting
- [ ] System architecture overview
- [ ] System architecture diagram
- [ ] Code documentation and comments
- [ ] Final testing
- [ ] Final demonstration

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- REPOSITORY STRUCTURE -->
## Repository Structure

* `/docs` – Project documentation, including person-hour estimates, actual person-hour records, system architecture, diagrams, and custom feature UML documentation
* `/src` – Minesweeper source code and AI implementation
* `/test` – Test cases and validation files
* `README.md` – Project overview, setup instructions, and repository navigation

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- SYSTEM DOCUMENTATION -->
## System Documentation

Project documentation is stored in the [`/docs`](docs) folder as required by the Project 2 specifications.

### Person-Hours Estimate

The person-hours estimate documents the expected development effort for the project and the methodology used to determine the estimates.

The estimate considers:

- Evaluation and maintenance of the inherited system
- AI solver development
- Custom feature development
- Testing
- Documentation
- Integration and debugging

### Actual Person-Hours

Actual person-hours are recorded on a day-by-day basis for each team member.

Recorded activities include:

- Coding
- Testing
- Team meetings
- Documentation
- Integration and debugging

EECS 581 lecture time is not included.

### System Architecture

The system architecture documentation provides a high-level description of the Minesweeper system, including:

- Major system components
- Relationships between components
- Data flow
- Key data structures
- System architecture diagrams
- Information necessary for future teams to understand and extend the system

### Custom Feature UML

The custom addition is documented using a UML diagram based on concepts from EECS 348.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- TESTING -->
## Testing

Testing is performed throughout development to verify both inherited and newly implemented functionality.

Testing includes:

- Project 1 functionality
- Easy AI behavior
- Medium AI deduction rules
- Hard AI deduction rules
- 1-2-1 pattern recognition
- Random AI fallback behavior
- Custom feature functionality
- Flagging and uncovering behavior
- Win and loss conditions
- Game resets
- Invalid or unexpected user interactions
- System stability

Testing also ensures that Project 2 modifications do not introduce unintended regressions into the inherited Minesweeper system.

See the [`/test`](test) directory for test cases and validation files.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

The original Minesweeper system was developed by **Group 18** for Project 1 of EECS 581 – Software Engineering II.

Group 20 inherited the Group 18 system for Project 2 and is responsible for maintaining and extending the original implementation.

The team acknowledges Professor Hossein Saiedian for defining the project objectives and providing instructional guidance within EECS 581 – Software Engineering II at the University of Kansas.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
