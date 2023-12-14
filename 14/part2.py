NR_STEPS = 1_000_000_000
NR_ORIENTATIONS = 4


def get_answer() -> int:
    image = get_data()
    image = transpose_image(image)

    step, cycle_length, image = find_start_step_and_cycle_length(image)
    nr_cycles_forward = (NR_STEPS - step) // cycle_length

    step += nr_cycles_forward * cycle_length

    for _ in range(step, NR_STEPS):
        for _ in range(NR_ORIENTATIONS):
            image = step_forward(image)

    sum_ = _get_sum_rounded_rock_current_positions(image)
    return sum_


def _get_sum_rounded_rock_current_positions(image: list[list[str]]) -> int:
    nr_rows_image = len(image[0])
    rounded_rocks_current_positions = get_rounded_rock_current_positions(image)
    sum_ = sum(nr_rows_image - pos for col in rounded_rocks_current_positions for pos in col)
    return sum_


def get_data() -> list[list[str]]:
    with open("14/input.txt", "r") as f:
        image = [row for row in f.read().splitlines()]

    return image


def transpose_image(image: list[list[str]]) -> list[list[str]]:
    return [[image[j][i] for j in range(len(image))] for i in range(len(image[0]))]


def rotate_image(image: list[list[str]]) -> list[list[str]]:
    return [[image[j][i] for j in range(len(image))] for i in reversed(range(len(image[0])))]


def get_rounded_rocks_final_positions(image: list[list[str]]) -> tuple[tuple[int]]:
    return tuple(get_rounded_rocks_final_positions_for_col(col) for col in image)


def get_rounded_rocks_final_positions_for_col(col: list[str]) -> tuple[int]:
    final_positions = []

    start_rounded_rocks = 0
    nr_rounded_rocks = 0

    for i, c in enumerate(col):
        if c == "O":
            final_positions.append(start_rounded_rocks + nr_rounded_rocks)
            nr_rounded_rocks += 1
        elif c == "#":
            start_rounded_rocks = i + 1
            nr_rounded_rocks = 0

    return tuple(final_positions)


def get_rounded_rock_current_positions(image: list[list[str]]) -> tuple[tuple[int]]:
    return tuple(tuple(r for r, c in enumerate(col) if c == "O") for col in image)


def set_rounded_rocks(image: list[list[str]], rounded_rock_positions: tuple[tuple[int]]) -> list[list[str]]:
    image = unset_current_rounded_rocks(image)
    image = overwrite_new_rounded_rocks(image, rounded_rock_positions)
    return image


def unset_current_rounded_rocks(image: list[list[str]]) -> list[str]:
    return [[(c if c != "O" else ".") for c in row] for row in image]


def overwrite_new_rounded_rocks(image: list[list[str]], rounded_rock_positions: tuple[tuple[int]]) -> list[list[str]]:
    for r, row in enumerate(rounded_rock_positions):
        for c in row:
            image[r][c] = "O"

    return image


def find_start_step_and_cycle_length(
    image: list[list[str]],
) -> tuple[int, int, list[list[str]]]:
    positions_to_step = {}

    for step in range(NR_STEPS):
        rounded_rock_positions = get_rounded_rock_current_positions(image)

        if rounded_rock_positions in positions_to_step:
            cycle_length = step - positions_to_step[rounded_rock_positions]
            return step, cycle_length, image
        else:
            positions_to_step[rounded_rock_positions] = step

        for _ in range(NR_ORIENTATIONS):
            image = step_forward(image)


def step_forward(image: list[list[str]]) -> list[list[str]]:
    rounded_rocks_final_positions = get_rounded_rocks_final_positions(image)
    image = set_rounded_rocks(image, rounded_rocks_final_positions)
    image = rotate_image(image)
    return image


print(get_answer())
