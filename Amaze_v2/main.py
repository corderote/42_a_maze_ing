from maze import Maze
import sys

if __name__ == "__main__":

    if len(sys.argv) == 1:
        maze2 = Maze.generate_maze_output()
        sys.exit(0)
    else:
        print("Argument error.")
        print("Correct usage: python3 a_maze_ing.py")
        sys.exit(1)
