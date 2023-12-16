U = (-1, 0)
R = (0, 1)
D = (1, 0)
L = (0, -1)
DIRECTIONS = (U, R, D, L)


SPLITTER_DIRECTIONS_TO_NEXT_DIRECTION = {
    (U, "."): [U],
    (R, "."): [R],
    (D, "."): [D],
    (L, "."): [L],
    (U, "|"): [U],
    (R, "-"): [R],
    (D, "|"): [D],
    (L, "-"): [L],
    (U, "-"): [L, R],
    (R, "|"): [U, D],
    (D, "-"): [L, R],
    (L, "|"): [U, D],
    (U, "\\"): [L],
    (R, "\\"): [D],
    (D, "\\"): [R],
    (L, "\\"): [U],
    (U, "/"): [R],
    (R, "/"): [U],
    (D, "/"): [L],
    (L, "/"): [D],
}


def get_answer() -> int:
    image = get_data()
    energized_positions = get_energized_positions(image)
    nr_energized_positions = len(energized_positions)
    return nr_energized_positions


def get_data() -> list[list[str]]:
    with open("16/input.txt", "r") as f:
        image = [row for row in f.read().splitlines()]

    return image


def get_energized_positions(image: list[list[str]]) -> set[tuple[int, int]]:
    energized_positions = set()
    beam_positions_seen = set()

    beam_positions_to_parse = [(R, (0, 0))]

    while len(beam_positions_to_parse):
        direction, position = beam_positions_to_parse.pop()
        energized_positions.add(position)

        next_beam_directions = get_next_beam_directions(image, direction, position)
        for next_direction in next_beam_directions:
            next_position = get_next_position(position, next_direction)
            if not is_on_image(image, next_position):
                continue

            beam_position = (next_direction, next_position)
            if beam_position not in beam_positions_seen:
                beam_positions_to_parse.append(beam_position)
                beam_positions_seen.add(beam_position)

    return energized_positions


def get_next_beam_directions(
    image: list[list[str]], direction: tuple[int, int], position: tuple[int, int]
) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    object_as_pos = image[position[0]][position[1]]
    next_beam_directions = SPLITTER_DIRECTIONS_TO_NEXT_DIRECTION[(direction, object_as_pos)]
    return next_beam_directions


def get_next_position(position: tuple[int, int], direction: tuple[int, int]) -> tuple[int, int]:
    return position[0] + direction[0], position[1] + direction[1]


def is_on_image(image: list[list[str]], position: tuple[int, int]) -> bool:
    r, c = position
    return 0 <= r < len(image) and 0 <= c < len(image[0])


print(get_answer())
