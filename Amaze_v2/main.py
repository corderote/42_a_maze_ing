from maze import Maze
from solver import MazeSolver
import sys


def main() -> None:

    if len(sys.argv) != 4:
        print("Argument error.")
        print("Correct usage: python main.py <width> <height> <output_file>")
        sys.exit(1)

    try:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        output_file = sys.argv[3]
    except ValueError:
        print("Error: Width and height must be whole numbers.")
        sys.exit(1)

    start_pos = (0, 0)
    exit_pos = (width - 1, height - 1)

    maze = Maze(width, height, start_pos, exit_pos, output_file)
    maze.generate()
    maze.show_maze()
    maze.write_output_file()

    solver = MazeSolver(output_file)
    best_path = solver.solve()
    solver.append_solution_path(best_path)
    # solver.write_hex_path(best_path)
    # solver.rewrite_output_file_coord(best_path)

    # Command test: python3 main.py 7 8 maze.txt


def test() -> None:
    maze = Maze(9, 9, (0, 0), (7, 6), "maze.txt")
    # Tests para ver el grid
    # print(maze.grid)
    maze.grid[(2, 3)].fixed = True
    maze.grid[(3, 3)].fixed = True
    maze.grid[(4, 3)].fixed = True
    maze.grid[(5, 3)].fixed = True
    print(maze.grid[2, 3].fixed)
    # Tests end, delete
    maze.generate()
    maze.show_maze_hex()

    maze.show_maze()
    # Escribimos al output
    maze.write_output_file()


if __name__ == "__main__":
    main()
