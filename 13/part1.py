from typing import Optional


def get_answer() -> int:
    images = get_data()
    nr_columns_left = get_nr_columns_left_vertical_reflection(images)
    nr_columns_above = get_nr_columns_above_horizontal_reflection(images)
    sum_ = sum(nr_columns_left) + 100 * sum(nr_columns_above)
    return sum_


def get_data() -> list[list[str]]:
    images = []
    with open("13/input.txt", "r") as f:
        image = []
        for row in f.readlines():
            if row == "\n":
                images.append(image)
                image = []
                continue

            row = row.strip()
            image.append(row)

        images.append(image)

    return images


def get_nr_columns_left_vertical_reflection(images: list[list[str]]) -> list[int]:
    return [get_nr_columns_left_vertical_reflection_for_image(image) for image in images]


def get_nr_columns_left_vertical_reflection_for_image(
    image: list[list[str]],
) -> list[int]:
    transposed_image = transpose_image(image)
    return get_nr_columns_above_horizontal_reflection_for_image(transposed_image)


def transpose_image(image: list[list[str]]) -> list[list[str]]:
    return [[image[j][i] for j in range(len(image))] for i in range(len(image[0]))]


def get_nr_columns_above_horizontal_reflection(images: list[list[str]]) -> list[int]:
    return [get_nr_columns_above_horizontal_reflection_for_image(image) for image in images]


def get_nr_columns_above_horizontal_reflection_for_image(image: list[str]) -> int:
    vertical_reflection_below_column = get_horizontal_reflection_below_column(image)
    if vertical_reflection_below_column is None:
        return 0

    return vertical_reflection_below_column + 1


def get_horizontal_reflection_below_column(image: list[str]) -> Optional[int]:
    for reflection_index in range(len(image) - 1):
        if is_horizontal_reflection(image, reflection_index):
            return reflection_index

    return None


def is_horizontal_reflection(image: list[str], reflection_index: int):
    i = 0
    while reflection_index - i >= 0 and reflection_index + i + 1 < len(image):
        top_index = reflection_index - i
        bottom_index = reflection_index + i + 1
        if image[top_index] != image[bottom_index]:
            return False

        i += 1

    return True


print(get_answer())
