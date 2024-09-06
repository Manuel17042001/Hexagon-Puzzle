import copy
from copy import copy as cpy

from z3 import Solver, Bool, AtMost, AtLeast, sat, is_true, Or, Z3Exception, Z3_UNINTERPRETED_SORT, is_array

from model.tile import Tile
from utils.math_utils import get_neighbour_coordinates


def find_all_placements(width, height, tile, i, game):
    if tile.get_grid_pos() is not None or not tile.is_moveable():
        return []
    placement_list = []
    for flip in [False, True]:
        tmp_tile: Tile = copy.deepcopy(tile)
        if flip:
            tmp_tile.flip_vertical()
        for _ in range(6):
            tmp_tile.rotate(False)
            tmp_rotated_tile = copy.deepcopy(tmp_tile)
            for y in range(1, height + 1):
                for x in range(1, width + 1):
                    place_tile_at_position(x, y, tmp_rotated_tile)
                    if can_be_placed(width, height, tmp_rotated_tile, game):
                        list_pos_hexagons = []
                        for hexagon in tmp_rotated_tile.get_hexagons():
                            list_pos_hexagons.append((hexagon.get_coordinates(), hexagon.get_color()))
                        placement_list.append((i, list_pos_hexagons))
    distinct_list = deep_distinct(placement_list)
    return distinct_list


def deep_distinct(lst):
    seen = set()

    def deep_hash(obj):
        return hash(tuple([hash(x) for x in obj[1]]))

    def _check_seen(obj):
        obj_hash = deep_hash(obj)
        if obj_hash not in seen:
            seen.add(obj_hash)
            return True
        return False

    return [item for item in lst if _check_seen(item)]


def can_be_placed(width, height, tile, game):
    for hexagon in tile.get_hexagons():
        x, y = hexagon.get_coordinates()
        if x < 1 or x > width or y < 1 or y > height:
            return False
        if game.get_map().get_actual_map()[y][x] is not None:
            return False
    return True


def place_tile_at_position(grid_x: int, grid_y: int, tile: Tile) -> None:
    hexagons: list = cpy(tile.get_hexagons())
    hexagon_0_x, hexagon_0_y = hexagons[0].get_coordinates()
    if (hexagon_0_x, hexagon_0_y) == (grid_x, grid_y):
        return
    y_dif = grid_y - hexagon_0_y
    x_dif = grid_x - hexagon_0_x

    for hexagon in hexagons:
        hexagon_y = hexagon.get_y() + y_dif
        hexagon_x = hexagon.get_x() + x_dif
        if hexagon_0_y % 2 != grid_y % 2 != hexagon_y % 2:
            hexagon_x += 1 if hexagon_y % 2 == 0 else -1
        hexagon.set_coordinates(hexagon_x, hexagon_y)


def is_solution_correctly(solution, game) -> bool:
    def set_value_to_island(map, x, y, value):
        map[x][y] = value
        for y_n, x_n in [get_neighbour_coordinates(y, x, k) for k in [0, 1, 2, 3, 4, 5]]:
            if map[x_n][y_n] == 1:
                set_value_to_island(map, x_n, y_n, value)

    width, height = game.get_map().get_grid_size()
    width, height = width + 2, height + 2
    solution_map = copy.deepcopy(game.get_map().get_actual_map())
    for tiles in solution:
        for hexagon in tiles[1]:
            coord, color = hexagon
            x, y = coord
            solution_map[y][x] = color

    num_islands = 1

    for j in range(1, width - 1):
        for i in range(1, height - 1):
            if solution_map[i][j] is None:
                return False
            elif solution_map[i][j] == 0:
                continue
            elif solution_map[i][j] == 1 and num_islands == 1:
                set_value_to_island(solution_map, i, j, 0)
                num_islands += 1
            else:
                return False
    return True


def solve(init_rows, game):
    s = Solver()

    rows = [Bool('row_%d' % r) for r in range(len(init_rows))]

    # make inverse tables:
    inv_tbl_grid = {}
    inv_tbl_tile = {}

    cur_row = 0
    for tile_index, hexagons_coordinates in init_rows:
        if tile_index not in inv_tbl_tile:
            inv_tbl_tile[tile_index] = []
        inv_tbl_tile[tile_index].append(cur_row)
        for hexagon_coordinates in hexagons_coordinates:
            coord, color = hexagon_coordinates
            if coord not in inv_tbl_grid:
                inv_tbl_grid[coord] = []
            inv_tbl_grid[coord].append(cur_row)
        cur_row = cur_row + 1

    for tile in inv_tbl_tile:
        tmp = [rows[i] for i in inv_tbl_tile[tile]]
        s.add(AtMost(*(tmp + [1])))
        s.add(AtLeast(*(tmp + [1])))

    for tile in inv_tbl_grid:
        tmp = [rows[i] for i in inv_tbl_grid[tile]]
        s.add(AtMost(*(tmp + [1])))
        s.add(AtLeast(*(tmp + [1])))

    results = []
    solutions = []

    while s.check() == sat:
        m = s.model()
        results.append(m)
        solutions.append([])
        for row in range(len(init_rows)):
            if is_true(m[rows[row]]):
                solutions[-1].append(init_rows[row])

        if is_solution_correctly(solutions[-1], game):
            return solutions[-1]

        block = []
        for d in m:
            block.append(d() != m[d])
        s.add(Or(block))

    return None