from __future__ import annotations

from dataclasses import dataclass, field


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


U = Direction(0, -1)
R = Direction(1, 0)
D = Direction(0, 1)
L = Direction(-1, 0)
DIRECTIONS_MAP = {"U": U, "R": R, "D": D, "L": L}


def get_answer() -> int:
    instructions = get_data()
    directions = convert_to_directions(instructions)
    min_x, min_y, len_x, len_y = get_min_x_y_len_x_y(directions)
    trench_grid = get_trench_grid(directions, min_x, min_y, len_x, len_y)
    enclosed_coordinates = get_enclosed_coordinates(trench_grid)

    nr_meters_trench = sum(trench for trench_row in trench_grid for trench in trench_row)
    nr_meters_enclosed = len(enclosed_coordinates)
    nr_meters = nr_meters_trench + nr_meters_enclosed

    return nr_meters


def get_data() -> list[tuple[str, int, str]]:
    with open("18/input.txt", "r") as f:
        instructions = [row.split() for row in f.readlines()]

    instructions = [(row[0], int(row[1]), row[2]) for row in instructions]

    return instructions


def convert_to_directions(instructions: list[tuple[str, int, str]]) -> list[Direction]:
    return [DIRECTIONS_MAP[direction_str] * nr_steps for direction_str, nr_steps, _ in instructions]


def get_min_x_y_len_x_y(directions: list[Direction]) -> tuple[int, int, int, int]:
    end_coordinates = get_instructions_end_coordinates(directions)
    return _get_min_x_y_len_x_len_y(end_coordinates)


def get_instructions_end_coordinates(directions: list[Direction]) -> list[Coordinate]:
    current = Coordinate(0, 0)
    coordinates: list[Coordinate] = []

    for direction in directions:
        current = current + direction
        coordinates.append(current)

    return coordinates


def _get_min_x_y_len_x_len_y(
    coordinates: list[Coordinate],
) -> tuple[int, int, int, int]:
    min_x = min(c.x for c in coordinates)
    min_y = min(c.y for c in coordinates)
    max_x = max(c.x for c in coordinates)
    max_y = max(c.y for c in coordinates)
    len_x = max_x - min_x + 1
    len_y = max_y - min_y + 1
    return min_x, min_y, len_x, len_y


def get_trench_grid(directions: list[Direction], min_x: int, min_y: int, len_x: int, len_y: int) -> list[list[bool]]:
    grid = [[False for _ in range(len_x)] for _ in range(len_y)]
    current = Coordinate(-min_x, -min_y)

    for direction in directions:
        cardinal_direction = Direction(direction.x, direction.y)
        for _ in range(direction.n):
            current += cardinal_direction
            grid[current.y][current.x] = True

    return grid


def get_enclosed_coordinates(trench_grid: list[list[bool]]) -> list[Coordinate]:
    coordinates_seen: set[Coordinate] = set()
    islands: list[Coordinate] = []

    for y, row in enumerate(trench_grid):
        for x, trench in enumerate(row):
            coordinate = Coordinate(x, y)
            if trench or coordinate in coordinates_seen:
                continue

            island = [coordinate]
            check_neighbours_coordinates = [coordinate]
            coordinates_seen.add(coordinate)

            while check_neighbours_coordinates:
                coordinate = check_neighbours_coordinates.pop()
                for direction in DIRECTIONS_MAP.values():
                    neighbour = coordinate + direction
                    if neighbour in coordinates_seen:
                        continue

                    coordinates_seen.add(neighbour)

                    if not is_on_grid(neighbour, trench_grid):
                        continue

                    neighbour_fence = trench_grid[neighbour.y][neighbour.x]
                    if neighbour_fence:
                        continue

                    island.append(neighbour)
                    check_neighbours_coordinates.append(neighbour)

            if is_island_not_connected_to_edge(island, trench_grid):
                islands.extend(island)

    return islands


def is_on_grid(coordinate: Coordinate, trench_grid: list[list[bool]]) -> bool:
    max_y = len(trench_grid)
    max_x = len(trench_grid[0])

    return (0 <= coordinate.x < max_x) and (0 <= coordinate.y < max_y)


def is_island_not_connected_to_edge(island: list[Coordinate], trench_grid: list[list[bool]]) -> bool:
    min_x = min(c.x for c in island)
    max_x = max(c.x for c in island)
    min_y = min(c.y for c in island)
    max_y = max(c.y for c in island)

    return 0 < min_x and max_x < len(trench_grid[0]) - 1 and 0 < min_y and max_y < len(trench_grid) - 1


print(get_answer())
