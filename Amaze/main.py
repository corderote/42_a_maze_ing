from maze import Maze

maze = Maze(4, 4, (0, 0), (3, 3), "maze.txt")
print(maze.grid)
maze.write_output_file()
