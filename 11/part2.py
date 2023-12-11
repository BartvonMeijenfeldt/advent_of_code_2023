from itertools import combinations

import numpy as np


def get_answer() -> np.longlong:
    galaxies = get_data()
    galaxy_indexes = get_galaxy_indexes(galaxies)
    empty_rows, empty_columns = find_empty_rows_and_columns(galaxies, galaxy_indexes)
    shortest_paths = find_shortest_paths(galaxy_indexes, empty_rows, empty_columns)
    sum_ = get_long_sum(shortest_paths)
    return sum_


def get_data() -> list[list[str]]:
    with open("11/input.txt", "r") as f:
        galaxies = f.read().splitlines()

    return galaxies


def get_galaxy_indexes(galaxies: list[list[str]]) -> list[tuple[int, int]]:
    return [(r, c) for r, row in enumerate(galaxies) for c, element in enumerate(row) if element == "#"]


def find_empty_rows_and_columns(
    galaxies: list[list[str]], galaxy_indexes: list[tuple[int, int]]
) -> tuple[np.ndarray, np.ndarray]:
    nr_rows = len(galaxies)
    nr_cols = len(galaxies[0])

    galaxy_rows = {r for r, _ in galaxy_indexes}
    galaxy_columns = {c for _, c in galaxy_indexes}

    empty_rows = [r not in galaxy_rows for r in range(nr_rows)]
    empty_columns = [c not in galaxy_columns for c in range(nr_cols)]

    nr_empty_rows = np.cumsum(empty_rows)
    nr_empty_columns = np.cumsum(empty_columns)

    return nr_empty_rows, nr_empty_columns


def find_shortest_paths(
    galaxy_indexes: list[tuple[int, int]],
    empty_rows: np.ndarray,
    empty_columns: np.ndarray,
) -> dict[tuple[tuple[int, int], tuple[int, int]], int]:
    shortest_paths = {}
    empty_space_distance = 1_000_000

    for (r1, c1), (r2, c2) in combinations(galaxy_indexes, 2):
        row_distance = get_distance(r1, r2, empty_rows, empty_space_distance)
        col_distance = get_distance(c1, c2, empty_columns, empty_space_distance)
        distance = row_distance + col_distance
        shortest_paths[((r1, c1), (r2, c2))] = distance

    return shortest_paths


def get_distance(i1: int, i2: int, empty_space: np.ndarray, empty_distance: int) -> int:
    normal_distance = abs(i1 - i2)
    nr_empty_spaces = abs(empty_space[i1] - empty_space[i2])
    extra_empty_distance = nr_empty_spaces * (empty_distance - 1)
    return normal_distance + extra_empty_distance


def get_long_sum(shortest_paths: dict[tuple[tuple[int, int], tuple[int, int]], int]) -> np.longlong:
    sum_ = np.longlong(0)
    for v in shortest_paths.values():
        sum_ += v

    return sum_


print(get_answer())
