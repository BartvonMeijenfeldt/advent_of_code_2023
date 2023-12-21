from __future__ import annotations

from dataclasses import dataclass, field

NR_STEPS = 64


@dataclass(frozen=True)
class Direction:
    x: int
    y: int
    n: int = field(default=1)

    def __mul__(self, n: int) -> Direction:
        return Direction(self.x, self.y, n * self.n)


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def __add__(self, other: Direction) -> Coordinate:
        return Coordinate(self.x + other.n * other.x, self.y + other.n * other.y)

    def __sub__(self, other: Direction) -> Coordinate:
        return Coordinate(self.x - other.n * other.x, self.y - other.n * other.y)

    @property
    def neighbours(self) -> list[Coordinate]:
        return [self + direction for direction in DIRECTIONS]


U = Direction(0, -1)
R = Direction(1, 0)
D = Direction(0, 1)
L = Direction(-1, 0)
DIRECTIONS = [U, R, D, L]


def get_answer() -> int:
    start, is_walkable_map = get_data()
    walkable_coordinates = find_walkable_coordinates(start, is_walkable_map, NR_STEPS)
    nr_coordinates = len(walkable_coordinates)

    return nr_coordinates


def get_data() -> tuple[Coordinate, list[list[bool]]]:
    is_walkable_map: list[list[bool]] = []
    with open("21/input.txt", "r") as f:
        for y, row in enumerate(f.read().splitlines()):
            new_row: list[bool] = []
            for x, c in enumerate(row):
                if c == ".":
                    new_row.append(True)
                elif c == "S":
                    new_row.append(True)
                    start = Coordinate(x, y)
                else:
                    new_row.append(False)

            is_walkable_map.append(new_row)

    return start, is_walkable_map


def find_walkable_coordinates(start: Coordinate, is_walkable_map: list[list[bool]], n_steps: int) -> list[Coordinate]:
    to_parse: list[tuple[Coordinate, int]] = [(start, 0)]
    coordinate_time_steps_seen: set[tuple[Coordinate, int]] = set()
    walkable_coordinates: list[Coordinate] = []

    while to_parse:
        coordinate, coordinate_n_steps = to_parse.pop()
        neighbour_n_steps = coordinate_n_steps + 1
        for neighbour in coordinate.neighbours:
            neighbour_steps_tuple = (neighbour, neighbour_n_steps)
            if neighbour_steps_tuple in coordinate_time_steps_seen:
                continue

            coordinate_time_steps_seen.add(neighbour_steps_tuple)

            if not is_valid_coordinate(neighbour, is_walkable_map):
                continue

            if neighbour_n_steps == n_steps:
                walkable_coordinates.append(neighbour)
            else:
                to_parse.append(neighbour_steps_tuple)

    return walkable_coordinates


def is_valid_coordinate(c: Coordinate, is_walkable_map: list[list[bool]]) -> bool:
    len_y = len(is_walkable_map)
    len_x = len(is_walkable_map[0])

    if 0 <= c.x < len_x and 0 <= c.y < len_y:
        return is_walkable_map[c.y][c.x]

    return False


print(get_answer())
