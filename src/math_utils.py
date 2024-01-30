import math

sin60 = math.sin(math.radians(60))
cos60 = 0.5


def cube_to_axial(q: int, r: int, _) -> (int, int):
    return q, r


def axial_to_cube(x: int, y: int) -> (int, int, int):
    return x, y, -x - y


def axial_to_oddr(x: int, y: int) -> (int, int):
    return x + int((y - (y & 1)) / 2), y


def oddr_to_axial(x: int, y: int) -> (int, int):
    return x - int((y - (y & 1)) / 2), y
