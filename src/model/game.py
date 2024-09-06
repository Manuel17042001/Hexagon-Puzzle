import copy
import random
from datetime import datetime

from model import hexagonal_map
from solver import my_solver


class Game:

    def __init__(self, grid_width, grid_height, fixed_tiles):
        self.map = hexagonal_map.HexagonalMap(grid_width, grid_height, fixed_tiles)
        self.fixed_tiles = fixed_tiles
        self.play_ground_initialised = False
        self.time = 0
        self.time_start = None
        self.hint_count = 0
        self.colored_hint_count = 0

    def get_map(self):
        return self.map

    def is_play_ground_initialised(self):
        return self.play_ground_initialised

    def set_play_ground_initialised(self):
        self.play_ground_initialised = True

    def is_fixed_tiles(self):
        return self.fixed_tiles

    def time_run(self):
        if self.time_start is None:
            self.time_start = datetime.now().timestamp()

    def time_stop(self):
        if self.time_start is not None:
            self.time += datetime.now().timestamp() - self.time_start
            self.time_start = None

    def get_time(self):
        if self.time_start is not None:
            return self.time + datetime.now().timestamp() - self.time_start
        return self.time

    def increase_hint_count(self):
        self.hint_count += 1

    def increase_colored_hint_count(self):
        self.colored_hint_count += 1

    def get_hint_count(self):
        return self.hint_count

    def get_colored_hint_count(self):
        return self.colored_hint_count

    def get_hint(self, game):
        grid_width, grid_height = self.get_map().get_grid_size()

        row_tile = copy.deepcopy(self.get_map().get_tiles())
        row_tile.sort(key=lambda tile: len(tile.get_hexagons()), reverse=True)
        init_rows = []
        for i in range(len(row_tile)):
            init_rows = init_rows + my_solver.find_all_placements(grid_width, grid_height, row_tile[i], i, game)
        solution = my_solver.solve(init_rows, game)
        if solution is None or solution == []:
            return None
        index = int(random.random() * len(solution))
        return solution[index]
