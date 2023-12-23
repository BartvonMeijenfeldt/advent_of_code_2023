from __future__ import annotations

import sys
from dataclasses import dataclass

sys.setrecursionlimit(2_500)


@dataclass(frozen=True)
class Direction:
    x: int
    y: int


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def __add__(self, other: Direction) -> Coordinate:
        return Coordinate(self.x + other.x, self.y + other.y)


U = Direction(0, -1)
R = Direction(1, 0)
D = Direction(0, 1)
L = Direction(-1, 0)
DIRECTIONS = [U, R, D, L]


SLOPES_MAPPING = {"^": U, ">": R, "v": D, "<": L}


def get_answer() -> int:
    map_ = get_data()
    nr_steps_longest_hike = find_nr_steps_longest_hike(map_)

    return nr_steps_longest_hike


def get_data() -> tuple[tuple[str, ...], ...]:
    with open("23/input.txt", "r") as f:
        map_ = tuple(tuple(c for c in row) for row in f.read().splitlines())

    return map_


def find_nr_steps_longest_hike(map_: tuple[tuple[str, ...], ...]) -> int:
    start = Coordinate(1, 0)
    predecessor = start
    goal = Coordinate(len(map_) - 2, len(map_) - 1)
    return _find_nr_steps_longest_hike(start, predecessor, goal, map_)


def _find_nr_steps_longest_hike(
    start: Coordinate, predecessor: Coordinate, goal: Coordinate, map_: tuple[tuple[str, ...], ...]
) -> int:
    nr_steps_per_path: list[int] = []

    directions = DIRECTIONS if not is_slope(start, map_) else [SLOPES_MAPPING[get_symbol_at_c(start, map_)]]
    for direction in directions:
        neighbour = start + direction
        if neighbour == goal:
            return 1

        if not is_valid_coordinate(neighbour, direction, predecessor, map_):
            continue

        nr_steps_longest_hike_neighbour = 1 + _find_nr_steps_longest_hike(neighbour, start, goal, map_)
        nr_steps_per_path.append(nr_steps_longest_hike_neighbour)

    return max(nr_steps_per_path)


def is_valid_coordinate(
    c: Coordinate, direction: Direction, prepredecessor: Coordinate, map_: tuple[tuple[str, ...], ...]
) -> bool:
    if c == prepredecessor:
        return False

    if not is_on_map(c, map_):
        return False

    if is_slope(c, map_):
        required_direction = SLOPES_MAPPING[get_symbol_at_c(c, map_)]
        return direction == required_direction

    return not is_forest(c, map_)


def get_symbol_at_c(c: Coordinate, map_: tuple[tuple[str, ...], ...]) -> str:
    return map_[c.y][c.x]


def is_forest(c: Coordinate, map_: tuple[tuple[str, ...], ...]) -> bool:
    symbol = get_symbol_at_c(c, map_)
    return symbol == "#"


def is_slope(c: Coordinate, map_: tuple[tuple[str, ...], ...]) -> bool:
    symbol = get_symbol_at_c(c, map_)
    return symbol in SLOPES_MAPPING


def is_on_map(c: Coordinate, map_: tuple[tuple[str, ...], ...]) -> bool:
    len_y = len(map_)
    len_x = len(map_[0])

    return 0 <= c.x < len_x and 0 <= c.y < len_y


print(get_answer())
