from maze import Maze


class ASCII_Maze():
    maze: Maze | None = None
    wall = '#'
    path = ' '
    start = 'S'
    end = 'E'
    solution = '0'
    _maze_str = ''

    def __init__(self, maze: Maze, chars: str = "# SE0"):
        self.maze = maze
        self.wall = chars[0]
        self.path = chars[1]
        self.start = chars[2]
        self.end = chars[3]
        self.solution = chars[4]
        self._maze_str = self.maze_to_str()

    def maze_to_str(self) -> str:
        maze_str = ''
        for row in range(self.maze.get_height()):
            # Top
            if row == 0:
                for col in range(self.maze.get_width()):
                    cell = self.maze._grid[(col, row)]
                    if cell.get_north() == 0:
                        maze_str += f"{self.wall}{self.path}"
                    else:
                        maze_str += f"{self.wall}{self.wall}"
                maze_str += f"{self.wall}\n"
            # Mid 
            for col in range(self.maze.get_width()):
                cell = self.maze._grid[(col, row)]
                if cell.get_west() == 0:
                    maze_str += f"{self.path}"
                else:
                    maze_str += f"{self.wall}"
                if cell.walls == 15:
                    maze_str += f"{self.wall}"
                else:
                    maze_str += f"{self.path}"
            maze_str += f"{self.wall}\n"
            # Bot
            for col in range(self.maze.get_width()):
                cell = self.maze._grid[(col, row)]
                if cell.get_south() == 0:
                    maze_str += f"{self.wall}{self.path}"
                else:
                    maze_str += f"{self.wall}{self.wall}"
            maze_str += f"{self.wall}\n"
        return maze_str

    def print(self, with_path: bool = False, path_steps: int = -1):
        to_print = self._maze_str
        if with_path:
            # Start
            idx = 1 + (2*(self.maze._start[0]))
            idx += ((self.maze.get_width()+1)*2) * (1 + (2 * self.maze._start[1]))
            to_print = to_print[0:idx] + self.start + to_print[idx+1:]
            # Path
            count = 0
            while (count < path_steps or path_steps < 0) and count < len(self.maze._path):
                idx_p = 1 + (2*(self.maze._path[count][0]))
                idx_p += ((self.maze.get_width()+1)*2) * (1 + (2 * self.maze._path[count][1]))
                to_print = to_print[0:idx_p] + self.solution + to_print[idx_p+1:]
                idx_aux = (idx_p + idx)//2
                to_print = to_print[0:idx_aux] + self.solution + to_print[idx_aux+1:]
                idx = idx_p
                count += 1
            # End
            idx = 1 + (2*(self.maze._end[0]))
            idx += ((self.maze.get_width()+1)*2) * (1 + (2 * self.maze._end[1]))
            to_print = to_print[0:idx] + self.end + to_print[idx+1:]
        print(to_print)


if __name__ == "__main__":
    my_maze = Maze.load_from_file("example_maze.txt")
    ascii = ASCII_Maze(my_maze, "| SE0")
    ascii.print(True)
