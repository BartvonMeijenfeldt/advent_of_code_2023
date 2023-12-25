from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from itertools import combinations

import numpy as np


@dataclass(frozen=True)
class Hail:
    x: int
    y: int
    z: int

    dx: int
    dy: int
    dz: int


def get_answer() -> int:
    hails = get_data()
    x, y, z = find_stone_xyz(hails)
    sum_xyz = x + y + z

    return sum_xyz


def get_data() -> list[Hail]:
    with open("24/input.txt", "r") as f:
        hails = [parse_hail(row) for row in f.read().splitlines()]

    return hails


def parse_hail(row: str) -> Hail:
    x, y, z, dx, dy, dz = [int(number) for number in re.split(", | @ ", row)]
    return Hail(x, y, z, dx, dy, dz)


def find_stone_xyz(hails: list[Hail]) -> tuple[int, int, int]:
    dx = find_only_speed_possible(hails, "x")
    dy = find_only_speed_possible(hails, "y")
    dz = find_only_speed_possible(hails, "z")
    x, y, z = _find_xyz(hails=hails, dx=dx, dy=dy, dz=dz)
    return x, y, z


def find_only_speed_possible(hails: list[Hail], dimension: str) -> int:
    speed_distances = get_distances_equal_speeds(hails, dimension)
    all_potential_speeds = get_potential_speeds(speed_distances)

    # Remove all speeds not feasible with the other equal speed, distance combinations
    for speed, distances in speed_distances.items():
        for distance in distances:
            for potential_speed in list(all_potential_speeds):
                if potential_speed == speed:
                    all_potential_speeds.remove(potential_speed)
                    continue

                if distance % (potential_speed - speed) != 0:
                    all_potential_speeds.remove(potential_speed)

    assert len(all_potential_speeds) == 1
    return list(all_potential_speeds)[0]


def get_distances_equal_speeds(hails: list[Hail], dimension: str) -> dict[int, list[int]]:
    counts_ddimension_to_dimension: dict[int, list[int]] = defaultdict(list)
    for hail in hails:
        key = getattr(hail, f"d{dimension}")
        value = getattr(hail, dimension)
        counts_ddimension_to_dimension[key].append(value)

    speed_to_distances: dict[int, list[int]] = defaultdict(list)
    for speed, x_list in counts_ddimension_to_dimension.items():
        for a, b in combinations(x_list, r=2):
            speed_to_distances[speed].append(abs(a - b))

    return speed_to_distances


def get_potential_speeds(speed_distances: dict[int, list[int]]) -> set[int]:
    """For one random speed, distance combination. Calculate all potential speeds that are possible
    for this case.
    """
    random_speed, random_distances = list(speed_distances.items())[0]
    random_distance = random_distances[0]
    all_factors = get_factors(random_distance)
    all_potential_speeds = {mp * f + random_speed for f in all_factors for mp in [-1, 1]}
    return all_potential_speeds


def get_factors(n: int) -> set[int]:
    return set(reduce(list.__add__, ([i, n // i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))


def _find_xyz(hails: list[Hail], dx: int, dy: int, dz: int) -> tuple[int, int, int]:
    """Use two hails to define a small set of linear equations to find the unique x, y, z.

    Equations:
    x_0 + n_0 * dx_0 = x + n_0 * dx
    y_0 + n_0 * dy_0 = y + n_0 * dy
    z_0 + n_0 * dz_0 = z + n_0 * dz
    x_1 + n_0 * dx_1 = x + n_0 * dx
    y_1 + n_0 * dy_1 = y + n_0 * dy

    n_i = number of timesteps until the stone hits hail i

    x_i = start position x of hail i
    y_i = start position y of hail i
    z_i = start position z of hail i

    dx_i = x speed of hail i
    dy_i = y speed of hail i
    dz_i = z speed of hail i

    x = start position x of stone
    y = start position y of stone
    z = start position z of stone

    dx = x speed of stone
    dy = y speed of stone
    dz = z speed of stone

    """
    hail_0, hail_1 = hails[:2]

    # Array columns, n_0, n_1, x, y, z
    a = np.array(
        [
            [hail_0.dx - dx, 0, -1, 0, 0],
            [hail_0.dy - dy, 0, 0, -1, 0],
            [hail_0.dz - dz, 0, 0, 0, -1],
            [0, hail_1.dx - dx, -1, 0, 0],
            [0, hail_1.dy - dy, 0, -1, 0],
        ]
    )

    b = np.array([-hail_0.x, -hail_0.y, -hail_0.z, -hail_1.x, -hail_1.y])
    n0, n1, x, y, z = np.linalg.solve(a, b)
    return x, y, z


print(get_answer())
