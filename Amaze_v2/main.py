from maze import Maze
from solver import MazeSolver
import sys
from settings_maze import get_config, ConfigError


def main_with_args() -> None:

    try:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        output_file = sys.argv[3]
    except ValueError:
        print("Error: Width and height must be whole numbers.")
        sys.exit(1)

    start_pos = (0, 0)
    exit_pos = (width - 1, height - 1)

    try:
        maze = Maze(width, height, start_pos, exit_pos, output_file)
    except ValueError as e:
        print(f"ValueError creating maze: {e}")
        sys.exit(1)
    maze.generate()
    maze.show_maze()
    maze.write_output_file()

    solver = MazeSolver(output_file)
    best_path = solver.solve()
    solver.append_solution_path(best_path)
    # solver.write_hex_path(best_path)
    # solver.rewrite_output_file_coord(best_path)

    # Command test: python3 main.py 7 8 maze.txt


def main_default() -> None:  # ESTE
    try:
        conf = get_config()
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
        print("⚠️ Seed is only valid in INT format. Generating random maze.")
        seed = None
    try:
        maze = Maze(width, height, entry, exit, output_file, seed)
    except (ValueError, KeyError) as e:
        print(e)
        sys.exit(1)

    # If the user does NOT want a perfect maze (the PERFECT flag is False)
    if not is_perfect:
        print("🎲 Adding alternate paths and loops...")
        maze.make_imperfect()
        # It breaks approximately 7% of internal walls

    '''
    # maze.show_maze_hex()
    # maze.show_maze()
    '''
    # We write to the output
    maze.write_output_file()

    solver = MazeSolver(output_file)
    best_path = solver.solve()
    best_path_converted = solver.converter_coord_to_path(best_path)
    if best_path:
        print(f"Best path: {best_path_converted}")
    solver.append_solution_path(best_path)
    # main_loop_default(maze, solver, main_default)


def main_loop_default(maze: Maze, solver: MazeSolver, main_function) -> None:
    #  in progress...
    while (True):
        choice = input("Select your choice:"
                       "\n1-Rebuild"
                       "\n2-Put path"
                       "\n3-Hide path"
                       "\n6-Exit"
                       "\n")
        if (choice == "1"):
            print("")
            main_function()
        elif (choice == "2"):
            print("Put path")
            best_path = solver.solve()
            solver.show_solve_maze(best_path)
        elif (choice == "3"):
            print("Hide path")
            maze.show_maze()
        elif (choice == "6"):
            sys.exit(0)
        else:
            print("Wrong choice!")
            # TO DO: Add proper errors


if __name__ == "__main__":

    if len(sys.argv) == 1:
        main_default()
        sys.exit(0)

    if len(sys.argv) != 4:
        print("Argument error.")
        print("Correct usage: python main.py <width> <height> <output_file>")
        print("Or just: python3 a_maze_ing.py config.txt")
        sys.exit(1)
    main_with_args()
