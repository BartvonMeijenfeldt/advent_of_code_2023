def get_answer() -> int:
    image = get_data()
    nr_rows_image = len(image)
    image = transpose_image(image)
    rounded_rocks_final_positions = get_rounded_rocks_final_positions(image)
    sum_ = sum(nr_rows_image - pos for col in rounded_rocks_final_positions for pos in col)
    return sum_


def get_data() -> list[list[str]]:
    with open("14/input.txt", "r") as f:
        image = [row for row in f.read().splitlines()]

    return image


def transpose_image(image: list[list[str]]) -> list[list[str]]:
    return [[image[j][i] for j in range(len(image))] for i in range(len(image[0]))]


def get_rounded_rocks_final_positions(image: list[list[str]]) -> list[list[int]]:
    return [get_rounded_rocks_final_positions_for_col(col) for col in image]


def get_rounded_rocks_final_positions_for_col(col: list[str]) -> list[int]:
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

    return final_positions


print(get_answer())
