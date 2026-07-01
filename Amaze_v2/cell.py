class Cell:
    """
    Represents an individual cell within the maze using bitwise masks.

    Attributes:
        walls (int): Binary representation of the wall states (N, E, S, W).
                     A bit set to 1 means the wall is closed, 0 means open.
        fixed (bool): Indicates if the cell belongs to a protected structure
                      (such as the "42" pattern) and should not be modified.
    """

    def __init__(self, value: int = 0b1111) -> None:
        """
        Initializes a new cell with all its walls closed by default.

        Args:
            value (int, optional):
                Initial state of the walls.
                Defaults to 0b1111 (15 in decimal: all walls closed).
        """
        self.walls = value
        self.fixed = False

    def get_north(self) -> int:
        """
        Checks if the North wall is active using a bitwise mask.

        Returns:
            int: 1 if the North wall is closed, 0 if it is open.
        """
        return (self.walls & 0b0001)

    def get_east(self) -> int:
        """
        Checks the state of the East wall by applying a mask and shifting
        the bit to the units position.

        Returns:
            int: 1 if the East wall is closed, 0 if it is open.
        """
        return ((self.walls & 0b0010) >> 1)

    def get_south(self) -> int:
        """
        Checks the state of the South wall by applying a mask and shifting
        the bit to the units position.

        Returns:
            int: 1 if the South wall is closed, 0 if it is open.
        """
        return ((self.walls & 0b0100) >> 2)

    def get_west(self) -> int:
        """
        Checks the state of the West wall by applying a mask and shifting
        the bit to the units position.

        Returns:
            int: 1 if the West wall is closed, 0 if it is open.
        """
        return ((self.walls & 0b1000) >> 3)
