from functools import lru_cache

NR_REPEATS = 5


def get_answer() -> int:
    springs = get_data()
    nr_allowed_permutations = get_number_of_allowed_permutations(springs)
    sum_ = sum(nr_allowed_permutations)
    return sum_


def get_data() -> list[tuple[int, frozenset[int], frozenset[int]], tuple[int]]:
    with open("12/input.txt", "r") as f:
        springs_data = [row.split() for row in f.read().splitlines()]

    return [tuple(e for e in parse_spring(spring) + (parse_groups(groups),)) for spring, groups in springs_data]


def parse_spring(spring: str) -> tuple[int, frozenset[int], frozenset[int]]:
    spring = "?".join([spring] * NR_REPEATS)
    len_ = len(spring)
    broken = frozenset(i for i, s in enumerate(spring) if s == "#")
    working = frozenset(i for i, s in enumerate(spring) if s == ".")

    return len_, broken, working


def parse_groups(groups: str) -> tuple[int]:
    return NR_REPEATS * tuple(int(n) for n in groups.split(","))


def get_number_of_allowed_permutations(
    springs: list[tuple[int, frozenset[int], frozenset[int]], tuple[int]]
) -> list[int]:
    return [
        _get_number_of_allowed_permutations(len_, broken, working, 0, elements)
        for len_, broken, working, elements in springs
    ]


@lru_cache(maxsize=1_000_000)
def _get_number_of_allowed_permutations(
    len_: int,
    broken: frozenset[int],
    working: frozenset[int],
    start: int,
    elements: list[int],
) -> int:
    nr_permutations = 0

    current_element = elements[0]

    for element_pos in range(start, len_ - current_element + 1):
        if is_allowed_place(broken, working, element_pos, current_element):
            if len(elements) == 1:
                if not any_broken_springs_left(len_, broken, element_pos + current_element):
                    nr_permutations += 1
            else:
                nr_permutations += _get_number_of_allowed_permutations(
                    len_,
                    broken,
                    working,
                    element_pos + current_element + 1,
                    elements[1:],
                )

        if current_pos_has_broken_spring(broken, element_pos):
            break

    return nr_permutations


def is_allowed_place(broken: frozenset[int], working: frozenset[int], element_pos: int, element: int) -> bool:
    required_not_working = {i for i in range(element_pos, element_pos + element)}
    if required_not_working.intersection(working):
        return False

    required_not_broken = element_pos + element
    return required_not_broken not in broken


def current_pos_has_broken_spring(broken: frozenset[int], element_pos: int) -> bool:
    return element_pos in broken


def any_broken_springs_left(len_: int, broken: frozenset[int], start_pos: int) -> bool:
    return any(pos in broken for pos in range(start_pos, len_))


print(get_answer())
