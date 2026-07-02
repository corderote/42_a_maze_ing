# CONFIG FILE EXPECTED VALUES:
CONFIG_FIELDS = {
    "WIDTH":        int,
    "HEIGHT":       int,
    "ENTRY":        tuple,
    "EXIT":         tuple,
    "OUTPUT_FILE":  str,
    "PERFECT":      bool
}

# DIRECTION CONSTANTS (Values from the subject)
NORTH = 1  # Bit 0 (0b0001)
EAST = 2   # Bit 1 (0b0010)
SOUTH = 4  # Bit 2 (0b0100)
WEST = 8   # Bit 3 (0b1000)

# OPPOSITE DIRECTIONS MAP
OPPOSITE = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST
}

# MOVEMENT DELTAS MAP
MOVE = {
    NORTH: (0, -1),
    SOUTH: (0, 1),
    EAST: (1, 0),
    WEST: (-1, 0)
}
# 42 stamp
STAMP = [
            [1, 0, 1, 0, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1]
]

# MLX_MAZE GLOBALS:
MLX_BUTTON_IMGS = [
    "mazegen/Resources/Images/new_button.png",
    "mazegen/Resources/Images/path_button.png",
    "mazegen/Resources/Images/color_button.png",
    "mazegen/Resources/Images/exit_button.png",
]

MLX_MAZE_SPRITES = {
    0: [
        "./mazegen/Resources/Images/wall_0.png",
        "./mazegen/Resources/Images/path_0.png",
        "./mazegen/Resources/Images/fixed_0.png",
        "./mazegen/Resources/Images/start_0.png",
        "./mazegen/Resources/Images/end_0.png",
        "./mazegen/Resources/Images/solution_0.png",
    ],
    1: [
        "./mazegen/Resources/Images/wall_1.png",
        "./mazegen/Resources/Images/path_1.png",
        "./mazegen/Resources/Images/fixed_1.png",
        "./mazegen/Resources/Images/start_1.png",
        "./mazegen/Resources/Images/end_1.png",
        "./mazegen/Resources/Images/solution_1.png",
    ],
}
