from __future__ import annotations

import re
from dataclasses import dataclass
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


MIN_X_Y = 200000000000000
MAX_X_Y = 400000000000000


def get_answer() -> int:
    hails = get_data()
    future_intersections = get_future_intersections(hails)
    intersections_within_borders = {
        (hail_a, hail_b): intersection
        for (hail_a, hail_b), intersection in future_intersections.items()
        if MIN_X_Y <= intersection[0] <= MAX_X_Y and MIN_X_Y <= intersection[1] <= MAX_X_Y
    }
    nr_intersections_within_border = len(intersections_within_borders)

    return nr_intersections_within_border


def get_data() -> list[Hail]:
    with open("24/input.txt", "r") as f:
        hails = [parse_hail(row) for row in f.read().splitlines()]

    return hails


def parse_hail(row: str) -> Hail:
    x, y, z, dx, dy, dz = [int(number) for number in re.split(", | @ ", row)]
    return Hail(x, y, z, dx, dy, dz)


def get_future_intersections(hails: list[Hail]) -> dict[tuple[Hail, Hail], tuple[float, float]]:
    future_intersections = {
        (hail_a, hail_b): get_intersection(hail_a, hail_b) for hail_a, hail_b in combinations(hails, r=2)
    }
    return {
        (hail_a, hail_b): intersection
        for (hail_a, hail_b), intersection in future_intersections.items()
        if intersection is not None
    }


def get_intersection(hail_a: Hail, hail_b: Hail) -> tuple[float, float] | None:
    # Solve following system of equations with na and na signifying the number of nanoseconds passsed for hail_a and
    # hail_b respectively:
    #
    # hail_a.x + na * hail_a.dx = hail_b.x + nb * hail_b.dx
    # hail_a.y + nb * hail_a.dy = hail_b.y + nb * hail_b.dy
    #
    # <=>
    #
    # na * hail_a.dx - nb * hail_b.dx = hail_b.x - hail_a.x
    # na * hail_a.dy - nb * hail_b.dy = hail_b.y - hail_a.y

    a = np.array([[hail_a.dx, -hail_b.dx], [hail_a.dy, -hail_b.dy]])
    b = np.array([hail_b.x - hail_a.x, hail_b.y - hail_a.y])
    try:
        nano_seconds_passed_a, nano_seconds_passed_b = np.linalg.solve(a, b)
    except Exception:
        return None

    if nano_seconds_passed_a < 0 or nano_seconds_passed_b < 0:
        return None

    intersection_x = hail_a.x + nano_seconds_passed_a * hail_a.dx
    intersection_y = hail_a.y + nano_seconds_passed_a * hail_a.dy
    return intersection_x, intersection_y


print(get_answer())
