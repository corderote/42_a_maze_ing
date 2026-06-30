from cell import Cell
from constants import NORTH, EAST, SOUTH, WEST, OPPOSITE, MOVE


class Maze:
    def __init__(self, width: int, height: int,
                 start: tuple[int, int], exit: tuple[int, int],
                 output_file: str) -> None:
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

    def main_loop(self) -> None:
        while (True):
            choice = input("Select your choice")
            if (choice == "1"):
                ...
            elif (choice == "2"):
                ...
            elif (choice == "6"):
                break
            else:
                print("eres tonto")
                # TO DO: Add proper errors

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

    def generate(self) -> None:
        """
        Generates a perfect maze using DFS with Backtracking.
        """
        import random
        print(f"Empezando DFS en la celda: {self.start}")
        print(f"¿Es válida la celda de inicio?: {self.is_valid_cell(self.start[0], self.start[1])}")
        # Initial config
        visited = set()
        stack = [self.start]
        visited.add(self.start)

        # The main loop: as long as the backpack (stack) is not empty
        while stack:
            # We look at the cell where we are currently standing (the last one in the stack)
            x, y = stack[-1]

            # List to save which neighboring addresses are valid to go to
            unvisited_neighbors = []

            # We explored the four directions around us
            for direction in [NORTH, EAST, SOUTH, WEST]:
                dx, dy = MOVE[direction]
                nx, ny = x + dx, y + dy
                # Is the neighboring cell within the map and has NOT been visited?
                if self.is_valid_cell(nx, ny) and (nx, ny) not in visited:
                    unvisited_neighbors.append((direction, nx, ny))

            # Decision making
            if unvisited_neighbors:
                # There are options! We choose a random direction from the available ones
                direction, nx, ny = random.choice(unvisited_neighbors)

                # We break the walls between the current cell and its neighbor
                self.connect_cells(x, y, direction)

                # We physically move to the new cell: we add it to the stack and the visited cell
                stack.append((nx, ny))
                visited.add((nx, ny))
            else:
                # Dead end! No free neighbors.
                # We remove the current cell from the stack to backtrack.
                stack.pop()

    def solve(self) -> None:
        """
        Solves the maze
        """
        ...

    def _ft_pattern(self) -> None:
        """
        Mark 42 cells as fixed, so they cannot be changed.
        If width < 9 or height < 7 (whatever) no 42 pattern will be created
        """
        ...

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
                if (x, y) == self.start:
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
                # Usamos :X para pasarlo a hexadecimal en mayúsculas
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
            # Opens the file in write mode ("w"). The 'with' block ensures that it closes automatically upon completion.
            with open(self.output_file, "w") as f:
                for y in range(self.height):
                    for x in range(self.width):
                        # El formato :X lo pasa a Hexadecimal en mayúsculas sin "0x"
                        # f.write(hex(self.grid[(x, y)].walls).strip("0x").upper())
                        f.write(f"{self.grid[(x, y)].walls:X}")
                    f.write("\n")

                f.write("\n")
                f.write(f"{self.start[0]}, {self.start[1]}")
                f.write("\n")
                f.write(f"{self.exit[0]}, {self.exit[1]}")
                # TO DO: Add solve path

        except IOError as e:
            print(f"❌ Error writing output file: {e}")
