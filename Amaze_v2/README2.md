``
README PARA COGER IDEAS
``

*Este proyecto ha sido creado como parte del currículo de 42 por pcordero[, nlicot-d].*

# A-Maze-Ing
## Descripción
- Objetivo y breve descripción general.

## Instrucciones
- información relevante sobre compilación, instalación y/o ejecución
## Recursos
- Referencias, uso de la IA.

- Explicación detallada y la justificación del algoritmo
seleccionado para este proyecto.


*This project has been created as part of the 42 curriculum by pcordero[, nlicot-d].*

*This project has been created as part of the 42 curriculum by <tu_login_aquí>.*

# Maze Generator and Solver

## 📝 Description
This project focuses on the algorithmic generation and resolution of mazes. The main goal is to build a robust system capable of creating randomized, valid, and fully connected mazes from a set of configurations, and subsequently finding the optimal path from an entry point to an exit point.

The project enforces software engineering constraints typical of the 42 network: error handling, strict validation of grid coordinates, algorithmic efficiency, and a dual visual representation — an ASCII terminal interface and a fully interactive 2D graphical display powered by **MiniLibX (mlx)**.

---

## ⚙️ Instructions

### Prerequisites
* **Python 3.10+**
* **MiniLibX Dependencies** (X11 and AppKit/OpenGL libraries depending on whether you are running on macOS or Linux).

### Execution
To run the complete pipeline (generation, solving, and graphical rendering), execute the main script from the root of the repository:

```bash
python3 main.py
```

# 🛠️ Configuration File Format

The project utilizes a custom configuration file (config.cfg) to ensure modularity and ease of evaluation. Lines starting with # are ignored as comments.Ini, TOML# Core Dimensions
WIDTH=15
HEIGHT=11

# Navigation Points
START_X=0
START_Y=0
EXIT_X=14
EXIT_Y=10

# Structural Properties
PERFECT=FALSE
IMPERFECT_PROBABILITY=0.08
SEED=43

🤖 Maze Generation Algorithm
Algorithm Chosen
We implemented the Depth-First Search (DFS) with Backtracking algorithm for the core layout generation, complemented by a Wall Braiding (Post-Generation Rupture) phase for imperfect mazes.Why this algorithm?Guaranteed Connectivity: DFS naturally ensures that there are no isolated cells (meeting the "full connectivity" constraint), as it visits every cell in the matrix before finishing.Perfect Baseline: Standard DFS creates a "Perfect Maze" (a tree-like structure with a single definitive path and no loops). This provides a predictable baseline.Controlled Imperfection: By setting PERFECT=FALSE, we scan the completed DFS maze and selectively tear down internal walls based on an exact probability loop. This introduces cycles (multiple paths) safely without risking large open areas ($3 \times 3$ zones), which are strictly forbidden by the subject.

♻️ Reusable Components

The architecture was built following Object-Oriented Programming (OOP) principles to allow maximum reusability:The Cell Bitwise Logic: The representation of walls using bitwise flags (NORTH=1, EAST=2, SOUTH=4, WEST=8) is encapsulated. This module can be reused in any 2D tile-based game or grid simulation.The config_loader Module: The parser built to extract data from config.cfg ignores comments and converts strings to proper types dynamically, making it a drop-in utility for any future Python projects at 42.

👥 Team and Project Management

Roles of Each Team Member nlicot-d: Lead Backend Developer — Focused on the Maze architecture, bitwise wall logic, validation/error management (e.g., verifying start/exit bounds relative to the '42' pattern), and the make_imperfect deterministic seeding.
pcordero: Frontend UI Developer — Focused on the graphical integration with MiniLibX (mlx), window lifecycle hooks, event handling (keyboard inputs), rendering the tile grid sprites, and visually animating the path from start to exit.

Planning and Evolution

Anticipated Planning:
- Week 1: Parse config files and set up the grid bitmask structure.
- Week 2: Implement DFS generation and embed the static '42' cell pattern.
- Week 3: Build the BFS solver, tie it to the MiniLibX window framework, and handle live asset rendering.

Evolution: Integrating MiniLibX required transforming our grid loop data into absolute coordinate pixels ($X \times \text{TILE\_SIZE}$) to ensure the windows scaled fluidly based on the WIDTH and HEIGHT values parsed from the configuration.

Retrospective

What worked well: The decision to track cell positions using Python dictionaries with coordinate tuples (x, y) allowed for instant $O(1)$ lookups and clean spatial validation checks.
What could be improved: The recursive nature of standard DFS can hit depth limits on massive grid sizes. For future scalability, switching to an iterative DFS using an explicit stack array would prevent potential stack overflows.
Tools used: Git/GitHub for version control, MiniLibX bindings, Python built-in unittest for validating maze connectivity, and standard text editors (VS Code / Vim).

📚 Resources & AI Usage

Classic References
Introduction to Algorithms (Cormen et al.) — For foundational graph traversal theories (BFS/DFS).
Jamis Buck's "Mazes for Programmers" — An excellent guideline for understanding cell connectivity and wall braiding techniques.
42 Docs MiniLibX Graphics Programming Fundamentals.

Artificial Intelligence Statement

AI (Large Language Models) was used responsibly during the development of this project for the following specific milestones:
1. Refining the Bitwise Masks: Assisting in drafting clear bitwise operations (&= ~EAST) to safely tear down walls simultaneously between neighboring cells.
2. Seed Determinism Debugging: Brainstorming why a fixed seed might yield different results across separate machines, which led to substituting unordered .keys() dictionary iterations with strict coordinate loops utilizing range(height) and range(width).

---
Readme Requirements
A README.md file must be provided at the root of your Git repository. Its purpose is
to allow anyone unfamiliar with the project (peers, staff, recruiters, etc.) to quickly
understand what the project is about, how to run it, and where to find more information
on the topic.
The README.md must include at least:
• The very first line must be italicized and read: This project has been created as part
of the 42 curriculum by <login1>[, <login2>[, <login3>[...]]].
• A ``“Description”`` section that clearly presents the project, including its goal and a
brief overview.
• An ``“Instructions”`` section containing any relevant information about compilation,
installation, and/or execution.
• A ``“Resources”`` section listing classic references related to the topic (documentation, articles, tutorials, etc.), as well as a description of how AI was used —
specifying for which tasks and which parts of the project.
➠ Additional sections may be required depending on the project (e.g., usage
examples, feature list, technical choices, etc.).
Any required additions will be explicitly listed below.
• The complete structure and format of your config file.
• The maze generation algorithm you chose.
• Why you chose this algorithm.
• What part of your code is reusable, and how.
• Your team and project management with:
◦ The roles of each team member.
◦ Your anticipated planning and how it evolved until the end
◦ What worked well and what could be improved
◦ Have you used any specific tools? Which ones?
If you implement advanced features (multiple algorithms, display options), describe them in this README.md file