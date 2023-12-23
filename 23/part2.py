from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import count


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

    @property
    def neighbours(self) -> list[Coordinate]:
        return [self + direction for direction in DIRECTIONS]


U = Direction(0, -1)
R = Direction(1, 0)
D = Direction(0, 1)
L = Direction(-1, 0)
DIRECTIONS = [U, R, D, L]


def get_data() -> tuple[tuple[str, ...], ...]:
    with open("23/input.txt", "r") as f:
        map_ = tuple(tuple(c for c in row) for row in f.read().splitlines())

    return map_


MAP = get_data()


def get_answer() -> int:
    nr_steps_longest_hike = find_nr_steps_longest_hike()

    return nr_steps_longest_hike


def find_nr_steps_longest_hike() -> int:
    start = Coordinate(1, 0)
    predecessors: set[Coordinate] = set()
    goal = Coordinate(len(MAP) - 2, len(MAP) - 1)
    return _find_nr_steps_longest_hike(start, predecessors, goal)


def _find_nr_steps_longest_hike(start: Coordinate, predecessors: set[Coordinate], goal: Coordinate) -> int:
    if start == goal:
        return 0

    nr_steps_per_path: list[int] = []
    neighbour_predecessors = predecessors | {start}

    for neighbour in start.neighbours:
        if not is_valid_coordinate(neighbour, predecessors):
            continue

        try:
            crossing, nr_steps = find_next_crossing(neighbour, start, goal)
            if crossing in predecessors:
                continue

            nr_steps_after_crossing = _find_nr_steps_longest_hike(
                crossing,
                neighbour_predecessors,
                goal,
            )
        except ValueError:
            continue

        nr_steps_longest_hike_neighbour = nr_steps + 1 + nr_steps_after_crossing
        nr_steps_per_path.append(nr_steps_longest_hike_neighbour)

    if len(nr_steps_per_path) == 0:
        raise ValueError("Invalid path")

    return max(nr_steps_per_path)


@lru_cache(maxsize=10_000)
def find_next_crossing(start: Coordinate, predecessor: Coordinate, goal: Coordinate) -> tuple[Coordinate, int]:
    current = start
    for nr_steps in count(start=0):
        if current == goal:
            break

        valid_neighbours = [
            neighbour for neighbour in current.neighbours if is_valid_coordinate(neighbour, set([predecessor]))
        ]
        if len(valid_neighbours) == 0:
            raise ValueError("Invalid Path")

        if len(valid_neighbours) == 1:
            predecessor = current
            current = valid_neighbours[0]
            continue

        break

    return current, nr_steps


def is_valid_coordinate(c: Coordinate, predecessors: set[Coordinate]) -> bool:
    if c in predecessors:
        return False

    if not is_on_map(c):
        return False

    return not is_forest(c)


def get_symbol_at_c(c: Coordinate) -> str:
    return MAP[c.y][c.x]


def is_forest(c: Coordinate) -> bool:
    symbol = get_symbol_at_c(c)
    return symbol == "#"


def is_on_map(c: Coordinate) -> bool:
    len_y = len(MAP)
    len_x = len(MAP[0])

    return 0 <= c.x < len_x and 0 <= c.y < len_y


print(get_answer())
