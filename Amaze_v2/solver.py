import sys
from constants import NORTH, EAST, SOUTH, WEST, MOVE


class MazeSolver:
    def __init__(self, maze_file: str):
        self.maze_file = maze_file
        self.grid = {}        # Matrix in memory: {(x, y): wall_value}
        self.width = 0
        self.height = 0
        self.start = (0, 0)
        self.exit = (0, 0)

        self.load_maze_from_file()

    def load_maze_from_file(self) -> None:
        """
        Read the text file of the pure maze and load it into memory.
        """
        try:
            with open(self.maze_file, 'r') as f:
                # We read all lines, removing whitespace and empty line breaks
                lines = [lin.strip() for lin in f.readlines() if lin.strip()]

            # The last two lines are the input and the output
            matrix_lines = lines[:-2]
            start_line = lines[-2]
            exit_line = lines[-1]

            # We calculate the dimensions directly from the maze text.
            self.height = len(matrix_lines)
            self.width = len(matrix_lines[0]) if self.height > 0 else 0

            # We reconstruct the grid by loading the hexadecimal values
            for y, line in enumerate(matrix_lines):
                for x, char in enumerate(line):
                    # int(char, 16) converts the character 'A'-'F' or '0'-'9'
                    # to its decimal integer (0-15)
                    self.grid[(x, y)] = int(char, 16)

            # We parse the input and output (cleaning up any commas or spaces)
            start_clean = start_line.replace(',', ' ').split()
            exit_clean = exit_line.replace(',', ' ').split()

            self.start = (int(start_clean[0]), int(start_clean[1]))
            self.exit = (int(exit_clean[0]), int(exit_clean[1]))

            print(f"Maze successfully loaded with '{self.maze_file}'")
            print(f"Dimensions detected: {self.width}x{self.height}")
            print(f"Entry Point: {self.start} | Exit Point: {self.exit}")

        except Exception as e:
            print(f"❌ Error reading the maze file: {e}")
            sys.exit(1)

    def solve(self) -> list:
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
            walls = self.grid[(x, y)]

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

    def rewrite_output_file_coord(self, best_path: list) -> None:
        """
        Add the coordinates of the best path (best_path)
        to the end of the maze text file.
        """
        if not best_path:
            print("No path to print")
            return
        try:
            with open(self.maze_file, "a") as f:
                f.write("\n")
                for x, y in best_path:
                    f.write(f"({x}, {y})")
        except IOError as e:
            print(f"Error writing output file: {e}")
        except Exception as e:
            print(f"General error in rewrite_output_file_coord: {e}")

    def write_hex_path(self, best_path: list) -> None:
        """
        Add the hexadecimal values ​​of the optimal path on a single line
        to the end of the maze file.
        """
        if not best_path:
            print("No path to print")
            return
        try:
            hex_chars = []
            for pos in best_path:
                wall_value = self.grid[pos]
                hex_c = f"{wall_value:X}"
                hex_chars.append(hex_c)
            solution = "".join(hex_chars)
            with open(self.maze_file, "a") as f:
                f.write("\n")
                f.write(solution)
        except IOError as e:
            print(f"Error writing the solution to the file:{e}")
        except Exception as e:
            print(f"General error in write_hex_path: {e}")

    def converter_coord_to_path(self, best_path: list) -> None:
        '''
        Convert the path coordinates to the sequence of steps
        '''
        if not best_path:
            print("No path to print")
            return
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
        return solution_path

    def append_solution_path(self, best_path: list) -> None:
        """
        Add to the end of the file the sequence of steps
        (N, E, S, W) that form the shortest path.
        """
        if not best_path:
            print("No path to print")
            return
        try:
            with open(self.maze_file, "a") as f:
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
                f.write("\n")
                f.write(solution_path)
        except IOError as e:
            print(f"❌ Error writing the solution to the file:{e}")
        except Exception as e:
            print(f"General error in write_hex_path: {e}")

    def show_solve_maze(self, path: list) -> None:
        """
        Prints the maze in the terminal using ASCII characters to
        show the walls visually, and the path to solve the maze.
        If no path available, just print the maze.
        """
        path_set = set(path)
        print("+" + "---+" * self.width)
        for y in range(self.height):
            row_str = "|"
            floor_str = "+"
            for x in range(self.width):
                current_pos = (x, y)
                walls = self.grid[current_pos]
                # --- Determine the center of the cell ---
                if current_pos == self.start:
                    cell_center = " S "  # S for Start (Input)
                elif current_pos == self.exit:
                    cell_center = " E "  # E for Exit
                elif current_pos in path_set:
                    cell_center = " * "  # Asterisk for the resolved path
                elif walls == 15:
                    cell_center = "███"
                else:
                    cell_center = "   "  # Empty space

                # --- Right Wall (EAST) ---
                if walls & EAST:
                    row_str += cell_center + "|"
                else:
                    row_str += cell_center + " "  # Open Road to the East

                # --- Bottom Wall (SOUTH) ---
                if walls & SOUTH:
                    floor_str += "---+"
                else:
                    floor_str += "   +"  # Open road to the South

            # We print the cell line and then its corresponding floor
            print(row_str)
            print(floor_str)


if __name__ == "__main__":
    # Can use only if in maze.txt don´t have the path
    if len(sys.argv) != 2:
        print("Usage: python solver.py <archivo_laberinto.txt>")
        sys.exit(1)

    solver = MazeSolver(sys.argv[1])

    # We calculated the solution!
    optimal_path = solver.solve()

    if optimal_path:
        print(f"🎉 Maze solved in {len(optimal_path)} steps!")
        print("The path is:", optimal_path)

        solver.append_solution_path(optimal_path)
        print("\n📍 SOLUTION MAP:")
        solver.show_solve_maze(optimal_path)
