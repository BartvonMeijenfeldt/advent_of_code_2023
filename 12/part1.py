def get_answer() -> int:
    springs = get_data()
    nr_allowed_permutations = get_number_of_allowed_permutations(springs)
    sum_ = sum(nr_allowed_permutations)
    return sum_


def get_data() -> list[tuple[tuple[int, set[int], set[int]], list[int]]]:
    with open("12/input.txt", "r") as f:
        springs_data = [row.split() for row in f.read().splitlines()]

    return [(parse_spring(spring), list(int(n) for n in groups.split(","))) for spring, groups in springs_data]


def parse_spring(spring: str) -> tuple[int, set[int], set[int]]:
    len_ = len(spring)
    broken = {i for i, s in enumerate(spring) if s == "#"}
    working = {i for i, s in enumerate(spring) if s == "."}

    return len_, broken, working


def get_number_of_allowed_permutations(springs: list[tuple[tuple[int, set[int], set[int]], list[int]]]) -> list[int]:
    return [_get_number_of_allowed_permutations(sequence, 0, spring) for sequence, spring in springs]


def _get_number_of_allowed_permutations(
    sequence: tuple[int, set[int], set[int]], start: int, elements: list[int]
) -> int:
    nr_permutations = 0

    current_element = elements[0]
    len_sequence = sequence[0]

    # ??????#??#?? 1,1,5,1
    # #.#..#####.# 1,1,5,1

    for element_pos in range(start, len_sequence - current_element + 1):
        if is_allowed_place(sequence, element_pos, current_element):
            if len(elements) == 1:
                if not any_broken_springs_left(sequence, element_pos + current_element):
                    nr_permutations += 1
            else:
                nr_permutations += _get_number_of_allowed_permutations(
                    sequence, element_pos + current_element + 1, elements[1:]
                )

        if current_pos_has_broken_spring(sequence, element_pos):
            break

    return nr_permutations


def is_allowed_place(sequence: tuple[int, set[int], set[int]], element_pos: int, element: int) -> bool:
    broken = sequence[1]
    working = sequence[2]

    required_not_working = {i for i in range(element_pos, element_pos + element)}
    if required_not_working.intersection(working):
        return False

    required_not_broken = element_pos + element
    return required_not_broken not in broken


def current_pos_has_broken_spring(sequence: tuple[int, set[int], set[int]], element_pos: int) -> bool:
    broken = sequence[1]
    return element_pos in broken


def any_broken_springs_left(sequence: tuple[int, set[int], set[int]], start_pos: int) -> bool:
    len_sequence = sequence[0]
    broken = sequence[1]
    return any(pos in broken for pos in range(start_pos, len_sequence))


print(get_answer())
