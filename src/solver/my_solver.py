import copy
from copy import copy as cpy

from z3 import Solver, Bool, AtMost, AtLeast, sat, is_true

from model.tile import Tile


def find_all_placements(width, height, tile, i, game):
    if tile.get_grid_pos() is not None:
        return []
    placement_list = []
    for y in range(1, height + 1):
        for x in range(1, width + 1):
            tmp_tile: Tile = copy.deepcopy(tile)
            for rotations in range(6):
                tmp_rotated_tile = copy.deepcopy(tmp_tile)
                for flip in [True, False]:
                    for _ in range(rotations):
                        tmp_rotated_tile.rotate(True)
                    if flip:
                        tmp_rotated_tile.flip_horizontal()
                    place_tile_at_position(x, y, tmp_rotated_tile)
                    if can_be_placed(width, height, tmp_rotated_tile, game):
                        list_pos_hexagons = []
                        for hexagon in tmp_rotated_tile.get_hexagons():
                            list_pos_hexagons.append(hexagon.get_coordinates())
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


def place_tile_at_position(x, y, tile):
    # todo refactor
    hexagons: list = cpy(tile.get_hexagons())
    hexagon_0 = hexagons[0]
    hexagon_0_x, hexagon_0_y = hexagon_0.get_coordinates()
    if (hexagon_0_x, hexagon_0_y) == (x, y):
        return
    y_dif = y - hexagon_0_y
    x_dif = x - hexagon_0_x
    if hexagon_0_y % 2 == y % 2:
        for hexagon in hexagons:
            hexagon_x, hexagon_y = hexagon.get_x() + x_dif, hexagon.get_y() + y_dif
            hexagon.set_coordinates(hexagon_x, hexagon_y)
    else:
        for hexagon in hexagons:
            new_y = hexagon.get_y() + y_dif
            if new_y % 2 == y % 2:
                hexagon_x, hexagon_y = (hexagon.get_x() + x_dif, new_y)
            elif new_y % 2 == 0:
                hexagon_x, hexagon_y = (hexagon.get_x() + x_dif + 1, new_y)
            else:
                hexagon_x, hexagon_y = (hexagon.get_x() + x_dif - 1, new_y)

            hexagon.set_coordinates(hexagon_x, hexagon_y)


def solve(init_rows):
    s = Solver()

    rows = [Bool('row_%d' % r) for r in range(len(init_rows))]

    # make inverse tables:
    inv_tbl_board = {}
    inv_tbl_poly = {}

    cur_row = 0
    for tile_index, hexagons_coordinates in init_rows:
        if tile_index not in inv_tbl_poly:
            inv_tbl_poly[tile_index] = []
        inv_tbl_poly[tile_index].append(cur_row)
        for hexagon_coordinates in hexagons_coordinates:
            coord = hexagon_coordinates
            if coord not in inv_tbl_board:
                inv_tbl_board[coord] = []
            inv_tbl_board[coord].append(cur_row)
        cur_row = cur_row + 1

    # at this point, inv_tbl_poly is a dict, it has poly type as a key and list of rows as a value
    # these are rows where specific poly type is stored

    # inv_tbl_board is also a dict. key=tuple (coordinates). value=list of rows, which can cover this cell on board.

    # only one row can be selected from inv_tbl_poly, meaning, each tile can be connected to only one row:
    for tile in inv_tbl_poly:
        tmp = [rows[q] for q in inv_tbl_poly[tile]]
        # only one True must be present in tmp.
        # AtMost()/AtLeast() takes list of arguments + k.
        # we pass here a list + 1 as an arguments to functions:
        s.add(AtMost(*(tmp + [1])))
        s.add(AtLeast(*(tmp + [1])))

    # only one row can be selected from inv_tbl_board, meaning, each cell on board can be connected to only one row:
    for tile in inv_tbl_board:
        tmp = [rows[q] for q in inv_tbl_board[tile]]

        # only one True must be present in tmp:
        s.add(AtMost(*(tmp + [1])))
        s.add(AtLeast(*(tmp + [1])))

    if s.check() == sat:
        m = s.model()
        solution = []
        for row in range(len(init_rows)):
            if is_true(m[rows[row]]):
                solution.append(init_rows[row])

        return solution
    else:
        return None
