from __future__ import annotations
from mazegen.cell import Cell
from mazegen.constants import NORTH, EAST, SOUTH, WEST, OPPOSITE, MOVE, STAMP
import random
import sys
from mazegen.config import get_config, ConfigError


class MazeGenerator:
    def __init__(self, width: int, height: int,
                 start: tuple[int, int], exit: tuple[int, int],
                 output_file: str, seed: int | None = None) -> None:
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
        Breaks the wall of the current cell (x, y) and the opposite wall
        of its neighbor in the given direction.
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
        Checks if the coordinates (x, y) are inside the maze boundaries.
        Returns True if they are valid, False otherwise.
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        current_cell = self.grid[(x, y)]
        if current_cell.fixed:
            return False
        return True

    def _ft_pattern(self) -> None:
        """
        Calculate the center of the maze and stamp the logo '42'
        by marking the corresponding cells as fixed (solid walls).
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
        Generates a perfect maze using DFS with Backtracking.
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
        Navigate the maze and break down internal walls randomly
        to create loops (multiple paths), making it IMPERFECT.
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
                        if (bin(current_cell.walls).count('1') >= 3 and
                           bin(neighbor_east.walls).count('1') >= 3):
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
                        if (bin(current_cell.walls).count('1') >= 3 and
                           bin(neighb_south.walls).count('1') >= 3):
                            if random.random() < probability:
                                # We break consistently on both sides
                                current_cell.walls &= ~SOUTH

                                neighb_south.walls &= ~NORTH

    def solve(self) -> list[tuple[int, int]]:
        """
        Find the shortest path from the entrance to the exit using BFS.
        Returns a list of tuples with the path coordinates.
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
        Writes the maze configuration to the specified output file.
        The format includes the hexadecimal array, input, output and path.
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
        return self.width

    def get_height(self) -> int:
        return self.height

    def get_maze_cells(self) -> dict[tuple[int, int], Cell]:
        return self.grid

    @classmethod
    def generate_maze_output(cls, filepath: str) -> MazeGenerator:
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
            print("Seed is only valid in INT format. Generating random maze.")
            seed = None
        try:
            maze = MazeGenerator(width, height, entry, exit, output_file, seed)
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
