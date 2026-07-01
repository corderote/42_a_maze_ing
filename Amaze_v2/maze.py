from cell import Cell
from constants import NORTH, EAST, SOUTH, WEST, OPPOSITE, MOVE
import random


class Maze:
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
        random.seed(seed)
        self.width = width
        self.height = height
        self.start = start
        self.exit = exit
        self.output_file = output_file
        self.grid: dict[tuple[int, int], Cell] = {}
        for y in range(height):
            for x in range(width):
                self.grid[(x, y)] = Cell()
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
        stamp = [
            [1, 0, 1, 0, 1, 1, 1],  # 4   2
            [1, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1]
        ]
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
                        if random.random() < probability:
                            # We break consistently on both sides
                            current_cell.walls &= ~SOUTH

                            neighb_south.walls &= ~NORTH

    def show_maze(self) -> None:
        """
        Prints the maze in the terminal using ASCII characters to
        show the walls visually.
        """
        print("\n--- Visual Maze ---")
        for y in range(self.height):
            top_line = ""
            mid_line = ""

            for x in range(self.width):
                cell = self.grid[(x, y)]

                # --- TOP LINE (Roofs / NORTH) ---
                top_line += "+"  # Corner
                if cell.walls & NORTH:
                    top_line += "---"
                else:
                    top_line += "   "

                # --- MIDDLE LINE (Side walls / WEST) ---
                if cell.walls & WEST:
                    mid_line += "|"
                else:
                    mid_line += " "

                # Start (S) and exit (E) indicators within the cells
                # If cell.fixed ("███")
                if cell.fixed:
                    mid_line += "███"
                elif (x, y) == self.start:
                    mid_line += " S "
                elif (x, y) == self.exit:
                    mid_line += " E "
                else:
                    mid_line += "   "
            top_line += "+"

            # When the row is finished, we close the right ends.
            last_cell = self.grid[(self.width - 1, y)]
            if last_cell.walls & EAST:
                mid_line += "|"
            else:
                mid_line += " "

            print(top_line)
            print(mid_line)
        # Floor at the back of the labyrinth to close the drawing
        bottom_line = ""
        for x in range(self.width):
            bottom_line += "+"
            last_row_cell = self.grid[(x, self.height - 1)]
            if last_row_cell.walls & SOUTH:
                bottom_line += "---"
            else:
                bottom_line += "   "
        bottom_line += "+"
        print(bottom_line)

    def show_maze_hex(self) -> None:
        """
        Prints the maze in the terminal using the exact hexadecimal
        representation that goes into the output file.
        """
        print("--- Maze Grid (Hex) ---")
        for y in range(self.height):
            row_str = ""
            for x in range(self.width):
                cell = self.grid[(x, y)]
                # We use :X to convert it to uppercase hexadecimal
                row_str += f"{cell.walls:X}"
            print(row_str)

        print(f"Start: {self.start[0]}, {self.start[1]}")
        print(f"Exit:  {self.exit[0]}, {self.exit[1]}")

    def write_output_file(self) -> None:
        """
        Writes the maze configuration to the specified output file.
        The format includes the hexadecimal array, input, and output.
        """
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
                f.write(f"{self.start[0]}, {self.start[1]}")
                f.write("\n")
                f.write(f"{self.exit[0]}, {self.exit[1]}")

        except IOError as e:
            print(f"❌ Error writing output file: {e}")
