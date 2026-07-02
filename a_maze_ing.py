import sys
from mazegen import mazegen_main


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(0)
    try:
        mazegen_main(sys.argv[1])
    except (OSError, ValueError) as error:
        print(f"Error: {error}")
