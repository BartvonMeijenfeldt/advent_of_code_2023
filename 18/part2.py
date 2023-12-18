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
DIRECTIONS_MAP = {"0": R, "1": D, "2": L, "3": U}


def get_answer() -> int:
    directions = get_data()
    coordinates_index_x, coordinates_index_y = get_coordinates_index_mapping(directions)
    trench_grid = get_trench_grid(directions, coordinates_index_x, coordinates_index_y)
    enclosed_coordinates = get_enclosed_coordinates(trench_grid)

    nr_meters_trench = get_nr_meters_trench(trench_grid, coordinates_index_x, coordinates_index_y)
    nr_meters_enclosed = get_nr_meters_coordinates(enclosed_coordinates, coordinates_index_x, coordinates_index_y)
    nr_meters = nr_meters_trench + nr_meters_enclosed

    return nr_meters


def get_data() -> list[Direction]:
    with open("18/input.txt", "r") as f:
        instructions = [row.split() for row in f.readlines()]

    instructions = [convert_to_directions(row[2]) for row in instructions]

    return instructions


def convert_to_directions(direction_str: str) -> Direction:
    nr_steps = int(direction_str[2:-2], 16)
    direction = DIRECTIONS_MAP[direction_str[-2]]
    return direction * nr_steps


def get_instructions_end_coordinates(directions: list[Direction]) -> list[Coordinate]:
    current = Coordinate(0, 0)
    coordinates: list[Coordinate] = []

    for direction in directions:
        current = current + direction
        coordinates.append(current)

    return coordinates


def get_coordinates_index_mapping(
    directions: list[Direction],
) -> tuple[dict[int, int], dict[int, int]]:
    end_coordinates = get_instructions_end_coordinates(directions)
    return _get_coordinates_index_mapping(end_coordinates)


def _get_coordinates_index_mapping(
    coordinates: list[Coordinate],
) -> tuple[dict[int, int], dict[int, int]]:
    coordinates_x = {coordinate_x: 2 * i for i, coordinate_x in enumerate(sorted({c.x for c in coordinates}))}
    coordinates_y = {coordinate_y: 2 * i for i, coordinate_y in enumerate(sorted({c.y for c in coordinates}))}
    return coordinates_x, coordinates_y


def get_trench_grid(
    directions: list[Direction],
    coordinates_index_x: dict[int, int],
    coordinates_index_y: dict[int, int],
) -> list[list[bool]]:
    grid = [
        [False for _ in range(max(coordinates_index_x.values()) + 1)]
        for _ in range(max(coordinates_index_y.values()) + 1)
    ]
    current = Coordinate(0, 0)
    prev_index_x = None
    prev_index_y = None

    for direction in directions + directions[:1]:
        current += direction
        index_x = coordinates_index_x[current.x]
        index_y = coordinates_index_y[current.y]

        if prev_index_x is not None and prev_index_y is not None:
            indexes_x = [index_x, prev_index_x]
            indexes_y = [index_y, prev_index_y]

            for x in range(min(indexes_x), max(indexes_x) + 1):
                for y in range(min(indexes_y), max(indexes_y) + 1):
                    grid[y][x] = True

        prev_index_x = index_x
        prev_index_y = index_y

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


def get_nr_meters_trench(
    trench_grid: list[list[bool]],
    coordinates_index_x: dict[int, int],
    coordinates_index_y: dict[int, int],
) -> int:
    trench_coordinates = [
        Coordinate(x, y) for y, row in enumerate(trench_grid) for x, trench in enumerate(row) if trench
    ]
    return get_nr_meters_coordinates(trench_coordinates, coordinates_index_x, coordinates_index_y)


def get_nr_meters_coordinates(
    coordinates: list[Coordinate],
    coordinates_index_x: dict[int, int],
    coordinates_index_y: dict[int, int],
) -> int:
    index_coordinates_x = {v: k for k, v in coordinates_index_x.items()}
    index_coordinates_y = {v: k for k, v in coordinates_index_y.items()}

    index_nr_meters_x = {
        i: get_number_of_meters(i, index_coordinates_x) for i in range(max(index_coordinates_x.keys()) + 1)
    }
    index_nr_meters_y = {
        i: get_number_of_meters(i, index_coordinates_y) for i in range(max(index_coordinates_y.keys()) + 1)
    }

    sum_ = 0
    for c in coordinates:
        width = index_nr_meters_x[c.x]
        length = index_nr_meters_y[c.y]
        sum_ += width * length

    return sum_


def get_number_of_meters(index: int, index_coordinates: dict[int, int]) -> int:
    if index in index_coordinates:
        return 1

    return index_coordinates[index + 1] - index_coordinates[index - 1] - 1


print(get_answer())
