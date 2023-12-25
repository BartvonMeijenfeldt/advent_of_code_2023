from __future__ import annotations

import heapq
import itertools
from collections import defaultdict
from copy import copy
from typing import Any


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


def get_answer() -> int:
    components = get_data()
    group_a, group_b = get_groups_after_three_cuts(components)
    len_group_a, len_group_b = len(group_a), len(group_b)
    answer = len_group_a * len_group_b

    return answer


def get_data() -> dict[str, list[str]]:
    components: dict[str, list[str]] = defaultdict(list)
    with open("25/input.txt", "r") as f:
        for row in f.read().splitlines():
            source_component, connected_components = row.split(": ")
            for component in connected_components.split(" "):
                components[source_component].append(component)
                components[component].append(source_component)

    return components


def get_groups_after_three_cuts(components: dict[str, list[str]]) -> tuple[set[str], set[str]]:
    paths_three_cuts = get_three_distinct_shortest_paths(components)
    for cut_paths in paths_three_cuts:
        try:
            critical_connections = get_critical_components(components, cut_paths)
        except ValueError:
            continue

        group_a, group_b = get_two_groups_after_connections_cut(components, critical_connections)
        if len(group_b) > 0:
            return group_a, group_b

    raise ValueError("No solution found")


def get_three_distinct_shortest_paths(components: dict[str, list[str]]) -> list[tuple[list[str], list[str], list[str]]]:
    seen: set[tuple[str, str]] = set()
    get_paths_three_cuts: list[tuple[str, str]] = []
    for component, neighbours in components.items():
        for neighbour in neighbours:
            if (component, neighbour) in seen or (neighbour, component) in seen:
                continue

            seen.add((component, neighbour))
            shortest_paths = find_up_to_four_distinct_shortest_paths(components, component, neighbour)
            if len(shortest_paths) <= 3:
                get_paths_three_cuts.append(shortest_paths)

    return get_paths_three_cuts


def find_up_to_four_distinct_shortest_paths(
    components: dict[str, list[str]], source: str, goal: str, forbidden_edges: set[tuple[str, str]] | None = None
) -> list[list[str]]:
    if forbidden_edges is None:
        forbidden_edges: set[tuple[str, str]] = set()
    else:
        forbidden_edges = copy(forbidden_edges)

    distinct_shortest_paths: list[list[str]] = []
    for _ in range(4):
        try:
            shortest_path = find_shortest_path(components, source, goal, forbidden_edges)
        except ValueError:
            break

        for node_a, node_b in itertools.pairwise(shortest_path):
            forbidden_edges.add((node_a, node_b))

        distinct_shortest_paths.append(shortest_path)

    return distinct_shortest_paths


def find_shortest_path(
    components: dict[str, list[str]], source: str, goal: str, forbidden_edges: set[tuple[str, str]]
) -> list[str]:
    queue = PriorityQueue()
    queue.put(source, 0)
    costs = {source: 0}
    from_: dict[str, str] = {}

    while queue:
        current = queue.pop()

        if current == goal:
            reversed_solution = [current]
            while current in from_:
                current = from_[current]
                reversed_solution.append(current)

            solution = reversed_solution[::-1]

            return solution

        neighbour_costs = costs[source] + 1

        for neighbour in components[current]:
            if (current, neighbour) in forbidden_edges or (neighbour, current) in forbidden_edges:
                continue

            if neighbour in costs:
                continue

            costs[neighbour] = neighbour_costs
            from_[neighbour] = current
            queue.put(neighbour, neighbour_costs)

    raise ValueError("No solution found")


def get_critical_components(
    components: dict[str, list[str]], paths: tuple[list[str], ...]
) -> tuple[tuple[str, str], ...]:
    critical_connections: list[tuple[str, str]] = []
    source, goal = paths[0]

    forbidden_edges: set[tuple[str, str]] = set()

    for path in paths:
        critical_connection = get_critical_connection(components, path, source, goal, forbidden_edges)
        critical_connections.append(critical_connection)
        forbidden_edges.add(critical_connection)

    return tuple(critical_connections)


def get_critical_connection(
    components: dict[str, list[str]], path: list[str], source: str, goal: str, forbidden_edges: set[tuple[str, str]]
) -> tuple[str, str]:
    distinct_paths = find_up_to_four_distinct_shortest_paths(components, source, goal, forbidden_edges)
    for node_a, node_b in itertools.pairwise(path):
        forbidden_edges_with_ab = forbidden_edges | {(node_a, node_b)}

        distinct_paths_without_ab = find_up_to_four_distinct_shortest_paths(
            components, source, goal, forbidden_edges_with_ab
        )
        if len(distinct_paths_without_ab) < len(distinct_paths):
            critical_connection = (node_a, node_b)
            return critical_connection

    raise ValueError("No critical connection found")


def get_two_groups_after_connections_cut(
    components: dict[str, list[str]], cut_connections: tuple[tuple[str, str], ...]
) -> tuple[set[str], set[str]]:
    set_cut_connections = set(cut_connections)

    member_group_a = cut_connections[0][0]
    to_parse = [member_group_a]
    members_a = {member_group_a}

    while to_parse:
        member_group_a = to_parse.pop()
        neighbours = components[member_group_a]
        for neighbour in neighbours:
            if (
                (member_group_a, neighbour) in set_cut_connections
                or (neighbour, member_group_a) in set_cut_connections
                or neighbour in members_a
            ):
                continue

            members_a.add(neighbour)
            to_parse.append(neighbour)

    members_b = components.keys() - members_a
    return members_a, members_b


print(get_answer())
