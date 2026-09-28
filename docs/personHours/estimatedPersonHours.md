# Estimated Person-Hours

## Estimation Methodology

The team used a combination of the **Use Case Points (UCP)** and **analogy-based estimation** methodologies discussed in the EECS 581 course lecture notes to estimate the person-hours required for Project 2.

Use Case Points is a quantitative estimation method that estimates development effort based on the number and complexity of a system's use cases and actors. The team used UCP to evaluate the relative complexity of the new functional requirements being added to the inherited Minesweeper system.

The lecture defines the following use-case complexity weights:

- **Simple:** 3 or fewer steps = 5 points
- **Average:** 4-7 steps = 10 points
- **Complex:** More than 7 steps = 15 points

Supporting activities such as documentation, testing, UML creation, integration, and meetings are not user-facing system use cases. These activities were therefore estimated separately using **analogy-based estimation**, which compares the expected work of a new project to actual effort from a previously completed project of similar scope.

Project 1 provides historical data from the same seven-member team. The team estimated 26 total person-hours for Project 1 and recorded 24.70 actual person-hours. Because the Project 1 estimate differed from the actual effort by only 1.30 person-hours, or approximately 5%, the team used its Project 1 experience as a reference when estimating comparable Project 2 activities.

---

## Step 1: Unadjusted Use Case Weight (UUCW)

The new functional requirements for Project 2 were divided into four primary use cases: Easy AI, Medium AI, Hard AI, and the custom Hint System.

| Use Case | Assigned Member | Complexity | Weight | Estimation Reasoning |
|:---------|:----------------|:----------:|:------:|:---------------------|
| Easy AI Solver | Pruthviraj Sadhankar | Simple | 5 | The Easy AI identifies eligible hidden cells, excludes flagged and already uncovered cells, randomly selects an eligible cell, and uncovers the selected cell. |
| Medium AI Solver | Gabriel Haro-Villa | Complex | 15 | The Medium AI evaluates revealed cells and their neighbors, applies two logical deduction rules for flagging mines and revealing safe cells, performs a resulting action when possible, and falls back to a random move when neither rule applies. |
| Hard AI Solver | Carter Ruff | Complex | 15 | The Hard AI includes the Medium AI behavior while additionally searching for and applying the required 1-2-1 pattern before falling back to a random valid move. |
| Hint System | Liam Kinghouser | Average | 10 | The Hint System verifies that hints remain, identifies an eligible safe cell, reveals the cell, decreases the remaining hint count, and updates the game state and interface. |
| **Total UUCW** | | | **45** | |

Therefore:

**UUCW = 5 + 15 + 15 + 10 = 45 points**

---

## Step 2: Unadjusted Actor Weight (UAW)

The primary actor for the Project 2 functionality is the **Player**.

The player interacts directly with the Minesweeper application through the graphical Pygame interface. Under the Use Case Points methodology, a graphical-interface user is classified as a Complex actor with a weight of 3.

| Actor | Complexity | Weight | Estimation Reasoning |
|:------|:----------:|:------:|:---------------------|
| Player | Complex | 3 | The player interacts directly with the Minesweeper system through its graphical Pygame interface. |
| **Total UAW** | | **3** | |

Therefore:

**UAW = 3 points**

---

## Step 3: Unadjusted Use Case Points (UUCP)

The Unadjusted Use Case Points are calculated by adding the Unadjusted Use Case Weight and Unadjusted Actor Weight:

**UUCP = UUCW + UAW**

**UUCP = 45 + 3**

**UUCP = 48 points**

The UCP calculation indicates that the Medium and Hard AI tasks represent the largest portions of the new functional development because they require substantially more decision logic than the Easy AI and Hint System.

Because this is a small academic maintenance project and the team does not have a previously established productivity rate measured in person-hours per UCP, the team used the UCP values primarily to determine the **relative development effort** of the four functional requirements rather than applying an unsupported productivity factor.

---

## Step 4: Functional Development Estimate

The 48 calculated Use Case Points were used to distribute the expected functional development effort according to each use case's proportion of the total UUCW.

Based on the complexity of the new functionality and the team's experience from Project 1, approximately **12 person-hours** were allocated to functional development.

Each use case received a portion of those hours proportional to its UUCW weight.

| Functional Task | UCP Weight | Estimated Person-Hours | Assigned Member | Estimation Reasoning |
|:----------------|:----------:|:----------------------:|:----------------|:---------------------|
| Easy AI Solver | 5 | 1.5 | Pruthviraj Sadhankar | Lowest-complexity AI task because it primarily requires random selection among eligible hidden cells. |
| Medium AI Solver | 15 | 4 | Gabriel Haro-Villa | Higher effort due to implementation and testing of two logical deduction rules and random fallback behavior. |
| Hard AI Solver | 15 | 4 | Carter Ruff | Higher effort because it incorporates the Medium logic and adds detection and handling of the 1-2-1 pattern. |
| Hint System | 10 | 2.5 | Liam Kinghouser | Moderate effort due to safe-cell selection, limited uses, game-state updates, and integration with the existing interface. |
| **Total Functional Development** | **45** | **12** | | |

---

## Step 5: Supporting Project Activities

Project activities that do not represent functional system use cases were estimated separately using Project 1 as a historical reference.

| Supporting Task | Estimated Person-Hours | Assigned Member(s) | Estimation Reasoning |
|:----------------|:----------------------:|:--------------------|:---------------------|
| MVP / Initial Project 2 Integration | 2 | Pruthviraj Sadhankar | Project 1 required approximately 1.5 actual hours for the initial MVP. Project 2 adds the additional challenge of understanding and extending an inherited codebase, so 2 hours were allocated. |
| Bug Testing | 2 | Joshua Fakunmoju | Allows dedicated time to test newly developed Project 2 functionality, identify defects, verify fixes, and ensure new changes do not break inherited functionality. |
| Documentation | 4 | Ivan Kullaya | Project 1 required significant documentation effort. Project 2 again requires person-hour records, meeting logs, system architecture documentation, README maintenance, and final documentation review, but existing Project 1 documentation provides a reusable structural reference. |
| Custom Feature UML | 2 | Gael Salazar-Morales | Provides time to create and review the required UML diagram for the custom Hint System after its implementation is established. |
| Final Integration and Testing | 2 | All Members | Allows time for combining individual contributions and verifying that the Easy, Medium, and Hard AI, Hint System, and inherited Minesweeper functionality operate correctly together. |
| **Total Supporting Effort** | **12** | | |

---

## Step 6: Meetings and Project Planning

Meeting effort was estimated separately because meeting time contributes to total team person-hours.

The team anticipates approximately four 30-minute meetings involving all seven team members during Project 2.

**Meeting Person-Hours = Number of Meetings × Meeting Length × Number of Team Members**

**Meeting Person-Hours = 4 × 0.5 hours × 7 members**

**Meeting Person-Hours = 14 person-hours**

These meetings include team and GTA meetings used for requirement review, task allocation, development coordination, progress evaluation, and discussion of project questions or issues.

---

## Final Estimated Person-Hours

| Effort Category | Estimated Person-Hours |
|:----------------|:----------------------:|
| Functional Development | 12 |
| MVP / Initial Integration | 2 |
| Bug Testing | 2 |
| Documentation | 5 |
| Custom Feature UML | 1 |
| Final Integration and Testing | 2 |
| Meetings and Project Planning | 14 |
| **Total Estimated Project Effort** | **38 person-hours** |

The team therefore estimates that Project 2 will require approximately **38 total person-hours**.

This estimate is slightly higher than the team's 26-person-hour Project 1 estimate because Project 2 requires the team to understand and modify an unfamiliar inherited codebase and implement increasingly complex AI behavior. At the same time, the existing Minesweeper implementation reduces the amount of foundational game development required. The estimate combines Use Case Points for evaluating the relative complexity of the new functional requirements with the team's actual Project 1 effort as a historical reference for estimating supporting project activities.
