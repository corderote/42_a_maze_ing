from cell import Cell


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
        self.generate()

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
                # TODO: Add proper errors

    def generate(self) -> None:
        """
        Algorithm to open walls, ...
        """
        ...

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
        Prints in terminal the maze.
        """
        ...

    def write_output_file(self) -> None:
        with open(self.output_file, "w") as f:
            for y in range(self.height):
                for x in range(self.width):
                    f.write(hex(self.grid[(x, y)].walls).strip("0x").upper())
                f.write("\n")
            f.write("\n")
            f.write(f"{self.start[0]}, {self.start[1]}")
            f.write("\n")
            f.write(f"{self.exit[0]}, {self.exit[1]}")
            # TODO: Add solve path
            ...
