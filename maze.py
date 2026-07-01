from __future__ import annotations


class MazeError(Exception):
    def __init__(self, msg: str = "Unknown configuration error."):
        print(f"MAZE ERROR: {msg}")


class Cell():
    def __init__(self, value: int = 0b1111) -> None:
        self.walls = value
        self.fixed = False
        if value == 15:
            self.fixed = True   

    def get_north(self) -> int:
        return (self.walls & 0b0001)

    def get_east(self) -> int:
        return ((self.walls & 0b0010) >> 1)

    def get_south(self) -> int:
        return ((self.walls & 0b0100) >> 2)

    def get_west(self) -> int:
        return ((self.walls & 0b1000) >> 3)


class Maze():
    # Variables
    _width: int = 0
    _height: int = 0
    _grid: dict[tuple[int, int], Cell]

    _start: tuple[int, int] = ()
    _end: tuple[int, int] = ()
    _path: list[tuple[int, int]] = []

    # Constructor.
    def __init__(self, w: int, h: int, cells: dict[tuple[int, int], Cell]) -> None:
        #TODO: Add validation here either using setters or a validate
        if w * h != len(cells):
            return
        self._width = w
        self._height = h
        self._grid = cells

    # Getters
    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def get_maze_cells(self) -> int:
        return self._grid

    # Setters
    def set_path(self, start: tuple[int, int],
                 end: tuple[int, int],
                 new_path: str) -> None:
        #TODO: Include validation
        self._start = start
        self._end = end
        position = start
        for direction in new_path:
            match direction:
                case 'N':
                    position = (position[0], position[1] - 1)
                case 'E':
                    position = (position[0] + 1, position[1])
                case 'S':
                    position = (position[0], position[1] + 1)
                case 'W':
                    position = (position[0] - 1, position[1])
            self._path.append(position)

    # Conversion
    def char_to_cell(char: str) -> Cell:
        if Maze._validate_char(char):
            cell = Cell(Maze._char_to_cell(char))
            return cell

    @staticmethod
    def _char_to_cell(char: str) -> int:
        valid_chars = ['0', '1', '2', '3',
                       '4', '5', '6', '7',
                       '8', '9', 'A', 'B',
                       'C', 'D', 'E', 'F']
        for idx in range(len(valid_chars)):
            if char == valid_chars[idx]:
                return idx
        return -1
    
    # Validations
    @staticmethod
    def _validate_char(char: str) -> bool:
        valid_chars = ['0', '1', '2', '3',
                       '4', '5', '6', '7',
                       '8', '9', 'A', 'B',
                       'C', 'D', 'E', 'F']
        return (char in valid_chars)
    
    # File 
    @staticmethod
    def load_from_file(filepath: str, with_path: bool = True) -> None:
        width = 0
        height = 0
        cells: dict[tuple[int, int], Cell] = {}

        with open(filepath, mode="rt", encoding="utf-8") as file:
            line = file.readline().strip('\n')
            cells_str = ''
            width = len(line)
            height = 0
            while line != '':
                cells_str += line
                height += 1
                line = file.readline().strip('\n')
            for row in range(height):
                for col in range(width):
                    cell_idx = (width * row) + col
                    new_cell = Maze.char_to_cell(cells_str[cell_idx])
                    cells[(col, row)] = new_cell
            new_maze = Maze(width, height, cells)
            if with_path is True:
                line = file.readline().strip('\n')
                start = (int(line.split(',')[0]), int(line.split(',')[1]))
                line = file.readline().strip('\n')
                end = (int(line.split(',')[0]), int(line.split(',')[1]))
                path = file.readline().strip('\n')
                new_maze.set_path(start, end, path)
        return new_maze


if __name__ == "__main__":
    maze = Maze.load_from_file("example_maze.txt")
