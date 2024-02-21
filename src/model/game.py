import copy
import random

from model import hexagonal_map
from solver import my_solver


class Game:

    def __init__(self, grid_width, grid_height):
        self.map = hexagonal_map.HexagonalMap(grid_width, grid_height)

    def get_map(self):
        return self.map

    def get_hint(self, game):
        # TODO implement function

        grid_width, grid_height = self.get_map().get_grid_size()

        row_tile = copy.deepcopy(self.get_map().get_tiles())
        init_rows = []
        for i in range(len(row_tile)):
            init_rows = init_rows + my_solver.find_all_placements(grid_width, grid_height, row_tile[i], i, game)
        solution = my_solver.solve(init_rows)
        if solution is None or solution == []:
            return None
        index = int(random.random() * len(solution))
        return solution[index]
