*This project has been created as part of the 42 curriculum by pcordero, nlicot-d.*

# A-Maze-ing

## Description
**A-Maze-ing** is a random maze generator developed in Python 3.10+. The project's main objective is to apply concepts from graph theory, generation algorithms, and resource management to create mazes (which can be configured to be "perfect," guaranteeing a single path between the entrance and exit). Furthermore, the system includes unique features such as the visual insertion of a hidden pattern "42," automatic optimal path resolution, and a modular design that allows the logic engine to be packaged and reused.

### Implemented features

#### Mandatory functionality

- Reads one configuration file passed to `a_maze_ing.py`.
- Validates required keys: `WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`, `OUTPUT_FILE`, and `PERFECT`.
- Generates random mazes with DFS.
- Supports perfect mazes (`PERFECT=True`) with exactly one path between any two cells.
- Supports imperfect mazes (`PERFECT=False`) by opening extra internal walls while keeping all cells connected and avoiding forbidden 3x3 open areas.
- Uses `SEED` when provided so the same configuration can reproduce the same maze.
- Keeps all outer borders closed and validates that entry and exit are inside the maze and different.
- Places the "42" wall pattern when the maze is large enough; otherwise it displays a clear warning and continues without the pattern.
- Writes the generated maze to `OUTPUT_FILE` using hexadecimal wall encoding, followed by entry, exit, and the shortest path solution.
- Finds the shortest path with BFS, including in imperfect mazes where several routes can exist.
- Displays the maze in the terminal with visible entry (`S`), exit (`E`), walls, optional path, and the "42" pattern.

``REVISAR``
- Provides a reusable `mazegen` Python package buildable with `make build`.

#### Mandatory user interactive controls

- Re-generate a new maze and display it.
- Show/Hide a valid shortest path from the entrance to the exit.
- Change maze wall colours.
- Quit the program.

#### Additional robustness

- Maze dimensions are capped at `50x50` to keep terminal rendering practical.

## Configuration file format

The configuration file uses `KEY=VALUE` pairs, one per line. Lines starting with `#` are comments and are ignored.

Maze dimensions are limited to `50x50` cells to keep terminal rendering practical and fail gracefully on unreasonable inputs.

| Key | Description | Example |
|-----|-------------|---------|
| `WIDTH` | Maze width in cells (integer from 1 to 100) | `WIDTH=20` |
| `HEIGHT` | Maze height in cells (integer from 1 to 100) | `HEIGHT=15` |
| `ENTRY` | Entry cell coordinates as x,y | `ENTRY=0,0` |
| `EXIT` | Exit cell coordinates as x,y | `EXIT=19,14` |
| `OUTPUT_FILE` | Path to the output file | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Whether the maze is perfect | `PERFECT=True` |
| `SEED` | Optional integer seed for reproducibility | `SEED=42` |

Example `config.txt`:

```
# A-Maze-ing default configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True

# Optional seed for reproducible generation.
# SEED=42
```
---

## Instructions
``REVISAR``
``CAMBIA COSAS DESDE AQUI PCORDERO``
### Requirements

- Python 3.10 or later
- `pip` or another package manager

### Installation

```bash
make install
```

This installs all required dependencies.

### Running the program

```bash
make run
```

Or directly:

```bash
python3 a_maze_ing.py config.txt
```

Where `config.txt` is your configuration file (see format below).

### Other Makefile targets

```bash
make debug       # Run with Python's pdb debugger
make lint        # Run flake8 and mypy checks
make lint-strict # Run mypy with --strict flag
make clean       # Remove __pycache__, .mypy_cache and build artifacts
```

### Building the mazegen package

```bash
make build
```

This generates a `.whl` file at the project root, installable via:

```bash
pip install mazegen-*.whl
```

---

``HASTA AQUÍ PCORDERO``

---

## Maze generation algorithm

We chose **Depth-First Search (DFS) with iterative backtracking**, also known as the recursive backtracker algorithm.

### How it works

1. Start from the entry cell, mark it as visited.
2. Randomly pick an unvisited neighbor, remove the wall between them, and move to it.
3. If no unvisited neighbors exist, backtrack to the previous cell.
4. Repeat until all cells have been visited.

The result is always a **perfect maze** (a spanning tree): exactly one path exists between any two cells.

### Why DFS

- It is simple to implement iteratively with a stack, avoiding Python's recursion limit.
- It produces mazes with long, winding corridors and relatively few dead ends, which are visually interesting and challenging to solve.
- It naturally guarantees full connectivity with no isolated cells.
- It is well-suited for embedding the "42" pattern by pre-marking those cells as visited before generation starts — the DFS simply routes around them.

For `PERFECT=False`, after the selected perfect algorithm we remove a random subset of internal walls (avoiding the 42 pattern and ensuring no 3×3 open areas are created), introducing cycles and multiple valid paths.

### Terminal interactions

``Explain HERE PCORDERO``

---

## Reusable module
``AQUI ES TODO UN EJEMPLO PORQUE NO LO TENEMOS HECHO``
The `mazegen` package exposes the maze generation logic as a standalone, importable library with no dependency on the main program.

### Installation

```bash
pip install mazegen-*.whl
```

### Basic usage

```python
from mazegen import MazeGenerator, MazeConfig

config = MazeConfig(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    output_file="maze.txt",
    perfect=True,
    seed=42,
    algorithm="DFS",
)

generator = MazeGenerator(config)
generator.generate()

# Access the maze grid (list of lists of Cell objects)
maze = generator.maze

# Access the 42 pattern cell positions
pattern = generator.pattern_42
```

### Passing custom parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `width` | `int` | Number of columns |
| `height` | `int` | Number of rows |
| `entry` | `tuple[int, int]` | Entry cell as (x, y) |
| `exit` | `tuple[int, int]` | Exit cell as (x, y) |
| `output_file` | `str` | Output filename |
| `perfect` | `bool` | Perfect maze if True |
| `seed` | `int \| None` | Seed for reproducibility |

### Accessing the solution

```python
from mazegen import MazeGenerator, MazeConfig
from mazegen.pathfinding import find_shortest_path

config = MazeConfig(
    width=10, height=10,
    entry=(0, 0), exit=(9, 9),
    output_file="maze.txt",
    perfect=True,
    algorithm="DFS",
)

generator = MazeGenerator(config)
generator.generate()

path = find_shortest_path(generator.maze, config.entry, config.exit)
print("Solution:", "".join(path))  # e.g. "SSEENNESSS..."
```

---

## Resources

### Algorithm references

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Depth-first search — Wikipedia](https://en.wikipedia.org/wiki/Depth-first_search)
- [Breadth-first search — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Think Labyrinth: Maze algorithms](http://www.astrolog.org/labyrnth/algrithm.htm)

### Python references

- [Python `random` module](https://docs.python.org/3/library/random.html)
- [mypy documentation](https://mypy.readthedocs.io/)
- [flake8 documentation](https://flake8.pycqa.org/)
- [Python packaging guide](https://packaging.python.org/en/latest/)

### AI usage

AI tools, including Claude, Gemini and ChatGPT, were used during this project for the following tasks:

- Reviewing and debugging the maze generation logic, particularly the 3×3 open area constraint in imperfect mode.
- Reviewing error handling, type hints, and edge cases in the Python modules.
- Drafting and structuring parts of this README.
- Suggesting test scenarios (seed=0, entry/exit at corners, small mazes without room for the 42 pattern).

All AI-generated suggestions were reviewed, tested, adapted, and understood before being included in the project.

---
``REVISAR``
``Notas del subject que hay que tener, ELIMINAR:``
The complete structure and format of your config file.
• The maze generation algorithm you chose.
• Why you chose this algorithm.
• What part of your code is reusable, and how.
• Your team and project management with:
◦ The roles of each team member.
14
A-Maze-ing This is the way
◦ Your anticipated planning and how it evolved until the end
◦ What worked well and what could be improved
◦ Have you used any specific tools? Which ones?
``HASTA AQUI``

## Team and project management

### Roles
- **pcordero**: configuration parsing, terminal rendering, , interactive CLI, packaging and Makefile.
- **nlicot-d**: maze generation algorithm (DFS, imperfect mode, 42 pattern), pathfinding (BFS), output file format.


### Planning
``REVISAR``
Our initial plan was to split the project into two parallel tracks: core generation logic and visual/output layer. This worked well in practice — the `Cell` and `MazeConfig` data structures served as a clear contract between both parts.

The main adjustment during development was adding the 3×3 open area constraint for imperfect mazes, which was not anticipated in the initial plan and required revisiting the generation logic.

### What worked well

- The DFS algorithm was easy to reason about and debug visually.
- ``REVISAR Y RELLENAR``

### What could be improved
``REVISAR``
- The imperfect mode could offer more control over the density of added cycles.
- Additional bonus algorithms could be added in their own files following the same structure as `bonus_prim.py`.

### Tools used

- Python 3.10+
- `mypy` for static type checking
- `flake8` for code style
- `build` for packaging ???? ``REVISAR``
- Claude, Gemini and ChatGPT for code review and debugging assistance