
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
