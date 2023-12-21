from __future__ import annotations

from dataclasses import dataclass, field

NR_STEPS_ELF = 26501365


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


@dataclass
class NrCoordinatesCopies:
    even_middle: int
    odd_middle: int
    cardinal_outers: list[int]
    side_outers: list[int]
    below_side_outers: list[int]


def get_answer() -> int:
    start, is_walkable_map = get_data()
    assert_start_in_middle(start, is_walkable_map)
    cycle_length = len(is_walkable_map)
    nr_complete_cycles, remainder_cycle = divmod(NR_STEPS_ELF, cycle_length)

    # Solution is based on the following finding: we start in the middle, with a clear path to left, right, upper and
    # down. Also the number of steps to walk is exactly some amount of cycles (length of garden) and the number of steps
    # to reach the edge on each side. This means after each cycle the following relevant copies of the original map are
    # relevant:

    #  ...SCS...
    #  ..SBOBS..
    #  .SBOEOBS.
    #  SBOEOEOBS
    #  COEOEOEOC
    #  SBOEOEOBS
    #  .SBOEOBS.
    #  ..SBOBS..
    #  ...SCS...

    # E: Even copies close enough to the middle to have either all even or odd spots reached (~half full)
    # O: Even copies close enough to the middle to have either all even or odd spots reached (~half full)
    # C: Cardinal directions on the very outside which are less full to barely being reached (quite empty)
    # S: Sides which are on the very outside which are less full to barely being reached (quite empty)
    # B: The side below the side, which are almost fully reached (almost half full)

    # Now all that needs to be done is calculating the number locations reached in each type of copy (calculated
    # separately for each quadrant, as the C/S/B copies will have different values), and counting the number of copies
    # in total for each type after the nr cycles required and appropriately multipling them to get to the final count.

    nr_coordinates_copies = get_nr_coordinates_per_copy(
        start, is_walkable_map, cycle_length, nr_complete_cycles, remainder_cycle
    )
    total_nr_coordinates = get_total_nr_coordinates(nr_coordinates_copies, nr_complete_cycles)

    return total_nr_coordinates


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


def assert_start_in_middle(start: Coordinate, is_walkable_map: list[list[bool]]):
    assert (
        start.x == start.y
        and len(is_walkable_map[0]) == len(is_walkable_map)
        and len(is_walkable_map[0]) - 1 == 2 * start.x
    )


def get_nr_coordinates_per_copy(
    start: Coordinate,
    is_walkable_map: list[list[bool]],
    cycle_length: int,
    nr_complete_cycles: int,
    remainder_cycle: int,
) -> NrCoordinatesCopies:
    min_nr_cycles_for_each_copy_type = 2
    steps_cycles_plus_remainder = min_nr_cycles_for_each_copy_type * cycle_length + remainder_cycle
    walkable_coordinates = find_walkable_coordinates(start, is_walkable_map, steps_cycles_plus_remainder)

    nr_even_middle = count_nr_coordinates_in_copy(walkable_coordinates, 0, 0, cycle_length)
    nr_odd_middle = count_nr_coordinates_in_copy(walkable_coordinates, 1, 0, cycle_length)
    nr_outers = get_nr_coordinates_outers(walkable_coordinates, min_nr_cycles_for_each_copy_type, cycle_length)
    nr_side_outers = get_nr_coordinates_sides(walkable_coordinates, min_nr_cycles_for_each_copy_type, cycle_length)
    nr_below_sides = get_nr_coordinates_below_sides(
        walkable_coordinates, min_nr_cycles_for_each_copy_type, cycle_length
    )

    if nr_complete_cycles % 2 == 1:
        nr_even_middle, nr_odd_middle = nr_odd_middle, nr_even_middle

    return NrCoordinatesCopies(
        even_middle=nr_even_middle,
        odd_middle=nr_odd_middle,
        cardinal_outers=nr_outers,
        side_outers=nr_side_outers,
        below_side_outers=nr_below_sides,
    )


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

    y = c.y % len_y
    x = c.x % len_x

    return is_walkable_map[y][x]


def get_total_nr_coordinates(nr_coordinates_copies: NrCoordinatesCopies, nr_complete_cycles: int) -> int:
    nr_copies_per_side = nr_complete_cycles
    nr_copies_even = sum(4 * i if i else 1 for i in range(nr_complete_cycles) if i % 2 == 0)
    nr_copies_odd = sum(4 * i if i else 1 for i in range(nr_complete_cycles) if i % 2 == 1)

    nr_coordinates_outer_edge = sum(
        nr_outer + nr_copies_per_side * nr_side + (nr_copies_per_side - 1) * nr_below_side
        for nr_outer, nr_side, nr_below_side in zip(
            nr_coordinates_copies.cardinal_outers,
            nr_coordinates_copies.side_outers,
            nr_coordinates_copies.below_side_outers,
        )
    )
    nr_coordinates_even = nr_copies_even * nr_coordinates_copies.even_middle
    nr_coordinates_odd = nr_copies_odd * nr_coordinates_copies.odd_middle

    total_nr_coordinates = nr_coordinates_outer_edge + nr_coordinates_even + nr_coordinates_odd
    return total_nr_coordinates


def get_nr_coordinates_outers(coordinates: list[Coordinate], nr_cycles: int, cycle_length: int) -> list[int]:
    return [
        count_nr_coordinates_in_copy(coordinates, mp_x * nr_cycles, mp_y * nr_cycles, cycle_length)
        for mp_x, mp_y in [(1, 0), (0, 1), (-1, 0), (0, -1)]
    ]


def get_nr_coordinates_sides(coordinates: list[Coordinate], nr_cycles: int, cycle_length: int) -> list[int]:
    return [
        count_nr_coordinates_in_copy(coordinates, mp_x, mp_y * nr_cycles, cycle_length)
        for mp_x in [-1, 1]
        for mp_y in [-1, 1]
    ]


def get_nr_coordinates_below_sides(coordinates: list[Coordinate], nr_cycles: int, cycle_length: int) -> list[int]:
    return [
        count_nr_coordinates_in_copy(coordinates, mp_x, mp_y * (nr_cycles - 1), cycle_length)
        for mp_x in [-1, 1]
        for mp_y in [-1, 1]
    ]


def count_nr_coordinates_in_copy(
    coordinates: list[Coordinate], steps_down: int, steps_right: int, cycle_length: int
) -> int:
    min_x = cycle_length * steps_right
    max_x = min_x + cycle_length

    min_y = cycle_length * steps_down
    max_y = min_y + cycle_length

    coordinates = [c for c in coordinates if min_x <= c.x < max_x and min_y <= c.y < max_y]
    return len(coordinates)


print(get_answer())
