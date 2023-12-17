from __future__ import annotations

import heapq
import itertools
from dataclasses import dataclass
from typing import Any

MIN_REPEATS = 4
MAX_REPEATS = 10


class PriorityQueue:
    def __init__(self):
        self.elements: list[tuple[float, int, Any]] = []
        self._counter = itertools.count()

    def is_empty(self) -> bool:
        return not self.elements

    def put(self, item: Any, priority: float):
        item = (priority, -next(self._counter), item)
        heapq.heappush(self.elements, item)

    def __getitem__(self, index: int) -> Any:
        return self.elements[index][2]

    def pop(self) -> Any:
        return heapq.heappop(self.elements)[2]

    def __len__(self) -> int:
        return len(self.elements)


@dataclass(frozen=True)
class Direction:
    x: int
    y: int


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def __eq__(self, other: Coordinate) -> bool:
        return self.x == other.x and self.y == other.y


U = Direction(0, -1)
R = Direction(1, 0)
D = Direction(0, 1)
L = Direction(-1, 0)
DIRECTIONS = [U, R, D, L]
NEIGHBOUR_DIRECTIONS = {U: [L, R], R: [U, D], D: [R, L], L: [D, U]}


@dataclass(frozen=True)
class DirectionCoordinate(Coordinate):
    x: int
    y: int
    direction: Direction
    repeats: int

    @property
    def neighbours(self) -> list[DirectionCoordinate]:
        neighbours: list[DirectionCoordinate] = []

        if self.repeats >= MIN_REPEATS:
            neighbours.extend(self + direction for direction in NEIGHBOUR_DIRECTIONS[self.direction])

        if self.repeats < MAX_REPEATS:
            neighbours.append(self + self.direction)

        return neighbours

    def __lt__(self, other: DirectionCoordinate) -> bool:
        return self.x < other.y or self.y < other.y

    def is_valid(self, map: list[list[int]]) -> bool:
        len_y = len(map)
        len_x = len(map[0])
        return 0 <= self.x < len_x and 0 <= self.y < len_y

    def __add__(self, other: Direction) -> DirectionCoordinate:
        x = self.x + other.x
        y = self.y + other.y
        if self.direction == other:
            repeats = self.repeats + 1
        else:
            repeats = 1

        return DirectionCoordinate(x, y, other, repeats)

    def get_shortest_cost_to_goal(self, goal: Coordinate) -> int:
        return self.get_distance_to_coordinate(goal)

    def get_distance_to_coordinate(self, coordinate: Coordinate) -> int:
        dis_x = abs(self.x - coordinate.x)
        dis_y = abs(self.y - coordinate.y)
        return dis_x + dis_y

    def step_onto_cost(self, map: list[list[int]]) -> int:
        return map[self.y][self.x]


def get_answer() -> int:
    map = get_data()
    cost = get_shortest_path_cost(map)
    return cost


def get_data() -> list[list[int]]:
    with open("17/input.txt", "r") as f:
        map = [[int(d) for d in row] for row in f.read().splitlines()]

    return map


def get_shortest_path_cost(map: list[list[int]]) -> int:
    start_coordinates = [DirectionCoordinate(x=0, y=0, direction=d, repeats=0) for d in [D, R]]
    goal = Coordinate(x=len(map[1]) - 1, y=len(map) - 1)

    queue = PriorityQueue()
    costs: dict[DirectionCoordinate, int] = {}
    for start_coordinate in start_coordinates:
        queue.put(start_coordinate, 0)
        costs[start_coordinate] = 0

    while queue:
        coordinate: DirectionCoordinate = queue.pop()
        coordinate_cost = costs[coordinate]

        if goal == coordinate:
            return coordinate_cost

        for neighbour in coordinate.neighbours:
            if not neighbour.is_valid(map):
                continue

            neighbour_cost = coordinate_cost + neighbour.step_onto_cost(map)

            if neighbour in costs and neighbour_cost > costs[neighbour]:
                continue

            costs[neighbour] = neighbour_cost
            shortest_future_cost = neighbour.get_shortest_cost_to_goal(goal)
            heuristic_cost = neighbour_cost + shortest_future_cost
            queue.put(neighbour, heuristic_cost)

    raise ValueError("No solution was found")


print(get_answer())
