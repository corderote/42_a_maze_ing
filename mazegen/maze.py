from __future__ import annotations
import random
import sys
from mazegen.cell import Cell
from mazegen.config import get_config, ConfigError
from mazegen.constants import NORTH, EAST, SOUTH, WEST, OPPOSITE, MOVE, STAMP


class Maze:
    """
    A class to handle the generation, structure, and reproducibility of
    a perfect maze.

    It initializes a grid of cells, handles random seed management for
    reproducibility,
    protects specific patterns from being overwritten, and runs the generation
    algorithm.

    Attributes:
        seed (int): The pseudo-random number generator seed used for
            replication.
        width (int): The horizontal dimension (number of columns) of the maze.
        height (int): The vertical dimension (number of rows) of the maze.
        start (tuple[int, int]): The starting coordinates (X, Y) of the maze.
        exit (tuple[int, int]): The exit coordinates (X, Y) of the maze.
        output_file (str): The path to the file where the maze data will
            be saved.
        grid (dict[tuple[int, int], Cell]): A map binding coordinates to Cell
            objects.
        path (list[tuple[int, int]]): A list holding the coordinates of the
            solved path.
    """
    def __init__(self, width: int, height: int,
                 start: tuple[int, int], exit: tuple[int, int],
                 output_file: str, seed: int | None = None) -> None:
        """
        Initializes the maze properties, manages the seeding, and builds the
        initial grid.

        Args:
            width (int): Total number of columns.
            height (int): Total number of rows.
            start (tuple[int, int]): Starting position coordinates as (x, y).
            exit (tuple[int, int]): Exit/destination coordinates as (x, y).
            output_file (str): Filename or path to export the maze results.
            seed (int | None, optional):
                Specific seed for generation reproducibility.
                Defaults to None, which generates a random seed.

        Raises:
            ValueError: If either the start or exit position overlaps with a
                        fixed cell defined by the protected '42' pattern.
        """
        if seed is not None:
            self.seed = seed
            print(f"🌱 Seed successfully planted: {seed}"
                  "(The maze will be reproducible)")
        else:
            self.seed = random.randint(1, 1000000)
            print(f"Seed: {self.seed}")
        random.seed(self.seed)
        self.width = width
        self.height = height
        self.start = start
        self.exit = exit
        self.output_file = output_file
        self.grid: dict[tuple[int, int], Cell] = {}
        for y in range(height):
            for x in range(width):
                self.grid[(x, y)] = Cell()
        self.path: list[tuple[int, int]] = []
        self._ft_pattern()
        if self.grid[self.start].fixed:
            raise ValueError("The ENTRY position in '42' pattern!")
        if self.grid[self.exit].fixed:
            raise ValueError("The EXIT position in pattern '42'!")
        self.generate()

    def connect_cells(self, x: int, y: int, direction: int) -> None:
        """
        Carves a path between the current cell and its neighbor in a given
        direction.

        This method breaks the specified wall of the current cell at (x, y) and
        simultaneously knocks down the complementary/opposite wall of the
        adjacent neighbor cell using bitwise NOT (`~`) and AND (`&=`) operators

        Args:
            x (int): The horizontal coordinate of the current cell.
            y (int): The vertical coordinate of the current cell.
            direction (int): The bitmask representing the wall direction to
                            break (e.g., North, East, South, West).
        """
        # Get the current cell
        current_cell = self.grid[(x, y)]

        # Calculate the neighbor's coordinates using the MOVE dictionary
        dx, dy = MOVE[direction]
        neighbor_x = x + dx
        neighbor_y = y + dy

        # Get the neighbor's cell
        neighbor_cell = self.grid[(neighbor_x, neighbor_y)]

        # Break our wall (applying the mask)
        current_cell.walls &= ~direction

        neighbor_cell.walls &= ~OPPOSITE[direction]

    def is_valid_cell(self, x: int, y: int) -> bool:
        """
        Determines whether a cell coordinate is a viable candidate for
        exploration.

        A cell is considered valid if it resides entirely within the physical
        boundaries of the maze grid and has not been locked/protected as
        part of the immutable "42" pattern layout.

        Args:
            x (int): The horizontal coordinate of the cell to validate.
            y (int): The vertical coordinate of the cell to validate.

        Returns:
            bool: True if the cell is within bounds and not fixed;
                False otherwise.
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        current_cell = self.grid[(x, y)]
        if current_cell.fixed:
            return False
        return True

    def _ft_pattern(self) -> None:
        """
        Centers and imprints the protected '42' logo pattern onto the maze
        grid.

        This method calculates the necessary horizontal and vertical offsets
        to center a pre-defined 7x5 binary matrix (`STAMP`) within the maze
        boundaries. Cells matching the pattern structure are flagged as
        `fixed = True`, transforming them into immutable obstacles that
        the maze generation algorithm is restricted from altering.

        If the maze dimensions are insufficient to safely accommodate the
        stamp along with a mandatory structural outer aisle margin, the
        process is safely bypassed.

        Note:
            The minimum practical dimensions required to successfully mount
            the pattern are 9 columns by 7 rows.
        """
        # 1. We define the mini stamp as 7 columns wide x 5 high
        # 1 = Wall of number '42' (blocked cell)
        # 0 = Free space for aisle
        stamp = STAMP
        stamp_w = 7
        stamp_h = 5

        # 2. If the maze is too small
        # we don't put the seal on to avoid crashes
        if self.width < stamp_w + 2 or self.height < stamp_h + 2:
            print("Maze too small to stamp the '42' pattern"
                  "\nMin size 9x7")
            return

        # 3. We calculate the mathematical coordinate of the center
        offset_x = (self.width - stamp_w) // 2
        offset_y = (self.height - stamp_h) // 2

        # 4. We stamped the seal on our grid of cells
        for sy in range(stamp_h):
            for sx in range(stamp_w):
                if stamp[sy][sx] == 1:
                    # We translate the local position of the stamp to the
                    # global coordinate of the labyrinth
                    target_x = offset_x + sx
                    target_y = offset_y + sy

                    # We mark the cell as fixed so that
                    # DFS completely avoids it
                    self.grid[(target_x, target_y)].fixed = True

    def generate(self) -> None:
        """
        Carves a perfect maze across the grid using Depth-First Search (DFS)
        with Backtracking.

        This method implements an iterative DFS loop backed by an explicit
        stack to simulate recursion safely without risk of maximum recursion
        depth exceptions. It begins at `self.start`, marks cells as visited,
        and randomly knocks down matching wall boundaries between adjacent
        available neighbors.

        When the path encounters a dead end (a cell with zero unvisited,
        valid neighbors), the algorithm backtracks by popping items off the
        stack until it encounters a previously traversed cell containing
        untouched avenues of exploration.

        Note:
            Because the grid guarantees a single path to every cell without
            cyclical loops, this process yields a 'perfect' maze topology.
        """
        visited = set()
        stack = [self.start]
        visited.add(self.start)

        # The main loop: as long as the backpack (stack) is not empty
        while stack:
            # We look at the cell where we are currently standing
            # (the last one in the stack)
            x, y = stack[-1]

            # List to save which neighboring addresses are valid to go to
            unvisited_neighbors = []

            # We explored the four directions around us
            for direction in [NORTH, EAST, SOUTH, WEST]:
                dx, dy = MOVE[direction]
                nx, ny = x + dx, y + dy
                # Is the neighbor cell within the map and has NOT been visited?
                if self.is_valid_cell(nx, ny) and (nx, ny) not in visited:
                    unvisited_neighbors.append((direction, nx, ny))

            # Decision making
            if unvisited_neighbors:
                # We choose a random direction from the available ones
                direction, nx, ny = random.choice(unvisited_neighbors)

                # We break the walls between the current cell and its neighbor
                self.connect_cells(x, y, direction)

                # We move to the new cell:
                # we add it to the stack and the visited cell
                stack.append((nx, ny))
                visited.add((nx, ny))
            else:
                # Dead end! No free neighbors.
                # We remove the current cell from the stack to backtrack.
                stack.pop()

    def make_imperfect(self, probability: float = 0.07) -> None:
        """
        Degrades the perfect maze into an imperfect maze by selectively
        breaking internal walls.

        A perfect maze contains exactly one unique path between any two
        points and zero loops.
        This method introduces braid characteristics (loops and alternative
        routes) by scanning the grid and tearing down walls sharing boundaries
        with valid neighbors based on a configured probability.

        To preserve structural consistency and protect required features,
        the method enforces the following constraints:
        1. Outer Edges Protection: Guarantees that exterior boundary walls are
           never destroyed, preventing paths from spilling outside the maze
           grid.
        2. Immutability Protection: Skips any cells flagged as `fixed` to
           prevent tampering with the centered "42" pattern layout.
        3. Density Threshold Constraint: Only attempts to tear down a shared
           wall if both the current cell and its respective neighbor have at
           least 3 walls intact (calculated via `bin().count('1')`). This
           prevents excessive space dilation and ensures the structural
           corridor layout remains recognizable.

        Args:
            probability (float, optional):
                The statistical odds (0.0 to 1.0) of destroying a qualifying
                wall barrier. Defaults to 0.07 (7%).
        """

        # We scan all cells except the outer edges so as not to break the map
        for y in range(self.height):
            for x in range(self.width):
                current_cell = self.grid[(x, y)]

                # We skip cells in pattern 42, they remain completely closed.
                if current_cell.fixed:
                    continue

                # --- Attempt to break out to the EAST ---
                if x < self.width - 1:  # It's not the right outer edge
                    neighbor_east = self.grid[(x + 1, y)]
                    # If there's a wall between them, they're not from '42,
                    # and luck decides it...
                    if (current_cell.walls & EAST) and not neighbor_east.fixed:
                        if (bin(current_cell.walls).count('1') >= 2 and
                           bin(neighbor_east.walls).count('1') >= 2):
                            if random.random() < probability:
                                # We break consistently on both sides
                                current_cell.walls &= ~EAST

                                neighbor_east.walls &= ~WEST

                # --- Attempt to break through to the SOUTH ---
                if y < self.height - 1:  # It is not the lower outer edge
                    neighb_south = self.grid[(x, y + 1)]
                    # If there's a wall between them, they're not from '42,
                    # and luck decides it...
                    if (current_cell.walls & SOUTH) and not neighb_south.fixed:
                        if (bin(current_cell.walls).count('1') >= 2 and
                           bin(neighb_south.walls).count('1') >= 2):
                            if random.random() < probability:
                                # We break consistently on both sides
                                current_cell.walls &= ~SOUTH

                                neighb_south.walls &= ~NORTH

    def solve(self) -> list[tuple[int, int]]:
        """
        Finds the shortest path from the entrance to the exit using
        Breadth-First Search (BFS).

        Unlike Depth-First Search, BFS explores the maze layer by layer,
        spreading out equidistantly like a wave from the starting node. This
        tracking property mathematically guarantees that the first path to
        successfully reach `self.exit` is the shortest valid path possible.

        The method handles traversal by matching individual cell bitmasks
        against directional constants.
        A bit value of 0 (`not (walls & direction)`) indicates an open
        passageway, allowing the queue to branch into that neighboring
        coordinate.

        Returns:
            list[tuple[int, int]]:
                A sequential list of coordinate pairs (x, y) tracing
                the shortest route from entry to exit. Returns an empty
                list if no viable route exists.
        """
        # The list of addresses to check, using your constants
        directions_to_check = [NORTH, EAST, SOUTH, WEST]

        # The exploration queue stores: (current_position, path_traveled)
        queue = [(self.start, [self.start])]

        # Set to avoid revisiting cells already visited by the BFS
        visited = {self.start}

        while queue:
            current_pos, path = queue.pop(0)
            x, y = current_pos

            # If we reach the exit, we're done! We return the optimal path
            if current_pos == self.exit:
                return path

            # We look at what walls the current cell has in the matrix
            walls = self.grid[(x, y)].walls

            # We checked the 4 possible directions using your constants
            for direction in directions_to_check:
                # If the wall bit is 0, it means the path is OPEN
                if not (walls & direction):
                    # We use the MOVE dictionary to calculate the
                    # neighbor's position
                    dx, dy = MOVE[direction]
                    nx, ny = x + dx, y + dy
                    neighbor = (nx, ny)

                    # If the neighbor has not been visited and exists
                    # on the map, we proceed
                    if neighbor not in visited and (nx, ny) in self.grid:
                        visited.add(neighbor)
                        queue.append((neighbor, path + [neighbor]))

        print("❌ No path was found to solve the labyrinth.")
        return []

    def write_output_file_mod(self, best_path: list[tuple[int, int]]) -> None:
        """
        Exports the entire maze configuration and its solution to the output
        file.

        This method acts as the final pipeline for the maze data, writing
        information in a sequential format fully compatible with automated
        testing scripts (Moulinette). The export process follows a strict
        structural schema:
        1. Grid Layout: Iterates row-by-row, column-by-column, converting each
           cell's wall bitmask into a single-digit, uppercase hexadecimal
           value (0-F).
        2. Structural Break: Places an explicit empty line separator right
           after the matrix block.
        3. Coordinates Block: Appends the entry and exit points on separate
           lines, formatted cleanly as comma-separated values (X,Y).
        4. Solution String: Translates the sequence of absolute coordinate
           steps (`best_path`) into relative cardinal movements
           ('N', 'E', 'S', 'W') by calculating index differentials, appending
           the final string with a trailing newline character.

        Args:
            best_path (list[tuple[int, int]]):
                A chronological list of grid coordinates representing the
                calculated solution route.

        Raises:
            IOError: Captured and handled internally if a system-level
                     file-writing error occurs (e.g., permission restriction).
            Exception: Captured and handled internally as a fallback mechanism
                       for unexpected execution failures.
        """
        self.path = best_path
        solution_path = ""
        for i in range(len(best_path) - 1):
            x, y = best_path[i]
            x_next, y_next = best_path[i + 1]

            dx = x_next - x
            dy = y_next - y

            if dx == 1:
                solution_path += "E"
            elif dx == -1:
                solution_path += "W"
            elif dy == 1:
                solution_path += "S"
            elif dy == -1:
                solution_path += "N"
        try:
            # Opens the file in write mode ("w"). The 'with'
            # block ensures that it closes automatically upon completion.
            with open(self.output_file, "w") as f:
                for y in range(self.height):
                    for x in range(self.width):
                        # Converts the format :X to uppercase hex without "0x"
                        f.write(f"{self.grid[(x, y)].walls:X}")
                    f.write("\n")

                f.write("\n")
                f.write(f"{self.start[0]},{self.start[1]}")
                f.write("\n")
                f.write(f"{self.exit[0]},{self.exit[1]}")
                f.write("\n")
                f.write(f"{solution_path}")
                f.write("\n")

        except IOError as e:
            print(f"❌ Error writing output file: {e}")
        except Exception as e:
            print(f"General error in write_output_file_mod: {e}")

    # Getters
    def get_width(self) -> int:
        """
        Retrieves the total width (number of columns) of the maze grid.

        Returns:
            int: The width dimension of the maze.
        """
        return self.width

    def get_height(self) -> int:
        """
        Retrieves the total height (number of rows) of the maze grid.

        Returns:
            int: The height dimension of the maze.
        """
        return self.height

    def get_maze_cells(self) -> dict[tuple[int, int], Cell]:
        """
        Retrieves the internal grid dictionary containing all coordinate-cell
        pairs.

        Returns:
            dict[tuple[int, int], Cell]: The full maze grid structure mapped
            by (x, y) coordinates.
        """
        return self.grid

    @classmethod
    def generate_maze_output(cls, filepath: str) -> Maze:
        """
        Orchestrates the entire setup, generation, execution, and export of a
        maze instance.

        This static factory method reads user configuration parameters
        (dimensions, coordinates, output targets, and reproducibility options)
        through an external configuration pipeline. It builds the base maze
        structure, handles potential seed type casting failures by falling
        back gracefully to non-reproducible randomness, and instantiates the
        generation logic.

        Depending on configuration settings, it conditionally degrades the
        perfect grid topology to add loops/cycles, executes the pathfinding
        solver to track down the optimal route, and triggers a comprehensive
        export write to disk.

        Returns:
            MazeGenerator: A fully generated, solved, and exported instance of
            the maze class.

        Raises:
            SystemExit (1): Triggered if config extraction encounters critical
            definition or validation errors (`ConfigError`), or if grid
            instantiation yields structural violations (e.g., entrance/exit
            positions overlapping a protected layout).
        """
        try:
            conf = get_config(filepath)
        except ConfigError:
            sys.exit(1)

        width = conf["WIDTH"]
        height = conf["HEIGHT"]
        entry = conf["ENTRY"]
        exit = conf["EXIT"]
        output_file = conf["OUTPUT_FILE"]
        is_perfect = conf["PERFECT"]
        try:
            raw_seed = conf["SEED"]
            seed = int(raw_seed)
        except KeyError:
            print(r"🎲 No fixed seed. Generating a 100% random maze.")
            seed = None
        except ValueError:
            seed = None
        try:
            maze = Maze(width, height, entry, exit, output_file, seed)
        except (ValueError, KeyError) as e:
            print(e)
            sys.exit(1)

        # If the user does NOT want a perfect maze (the PERFECT flag is False)
        if not is_perfect:
            print("🎲 Adding alternate paths and loops...")
            maze.make_imperfect()
            # It breaks approximately 7% of internal walls

        # We solve the maze
        best_path = maze.solve()

        # We write to the output
        maze.write_output_file_mod(best_path)
        return maze
