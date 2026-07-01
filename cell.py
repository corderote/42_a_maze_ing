class Cell():
    def __init__(self, value: int = 0b1111) -> None:
        self.walls = value
        self.fixed = False 

    def get_north(self) -> int:
        return (self.walls & 0b0001)

    def get_east(self) -> int:
        return ((self.walls & 0b0010) >> 1)

    def get_south(self) -> int:
        return ((self.walls & 0b0100) >> 2)

    def get_west(self) -> int:
        return ((self.walls & 0b1000) >> 3)