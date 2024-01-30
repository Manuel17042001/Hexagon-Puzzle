import hexagonal_map


class Game:

    def __init__(self, grid_width, grid_height):
        self.map = hexagonal_map.HexagonalMap(grid_width, grid_height)

    def get_map(self):
        return self.map
