from collections import defaultdict

U = (-1, 0)
R = (0, 1)
D = (1, 0)
L = (0, -1)

DIRECTIONS = (U, R, D, L)


PIPE_MAPPINGS = {
    "F": {U: R, L: D},
    "-": {R: R, L: L},
    "7": {R: D, U: L},
    "|": {D: D, U: U},
    "J": {D: L, R: U},
    "L": {L: U, D: R},
    ".": {},
}


def get_answer() -> int:
    pipes = get_data()
    start = find_start(pipes)
    main_loop = get_main_loop(start, pipes)
    pipes = convert_start_to_correct_pipe(start, pipes)
    pipes = convert_non_main_loop_pipe_to_dot(main_loop, pipes)
    pipes = add_space_in_between_pipes(pipes)
    islands = find_non_pipe_islands(pipes)
    non_edge_islands = get_non_edge_islands(islands, pipes)
    enclosed_islands = get_enclosed_islands(non_edge_islands, main_loop)
    nr_no_pipes = sum(get_pipe(c, pipes) == "." for island in enclosed_islands for c in island)
    return nr_no_pipes


def convert_non_main_loop_pipe_to_dot(main_loop: set[tuple[int, int]], pipes: list[list[str]]) -> list[list[str]]:
    pipes_return = []

    for y, row in enumerate(pipes):
        row_return = ""
        for x, pipe in enumerate(row):
            if (y, x) in main_loop:
                row_return += pipe
            else:
                row_return += "."

        pipes_return.append(row_return)

    return pipes_return


def get_data() -> list[list[str]]:
    with open("10/input.txt", "r") as f:
        pipes = f.read().splitlines()

    return pipes


def get_main_loop(s: tuple[int, int], pipes: list[list[int]]) -> set[tuple[int, int]]:
    cur_y, cur_x = s
    dir = D  # Saw in input that pipe is connected downwards, could have programatically found this out as well.
    main_loop = set()

    while True:
        cur_y += dir[0]
        cur_x += dir[1]
        main_loop.add((cur_y, cur_x))

        pipe_at_dir = pipes[cur_y][cur_x]
        if pipe_at_dir == "S":
            return main_loop

        dir = PIPE_MAPPINGS[pipe_at_dir][dir]


def convert_start_to_correct_pipe(start: tuple[int, int], pipes: list[list[str]]) -> tuple[int, int]:
    start_pipe = find_start_pipe(start, pipes)
    pipes[start[0]] = pipes[start[0]].replace("S", start_pipe)
    return pipes


def find_start(pipes: list[list[str]]) -> tuple[int, int]:
    for y, row in enumerate(pipes):
        for x, pipe in enumerate(row):
            if pipe == "S":
                return y, x


def find_start_pipe(start: tuple[int, int], pipes: list[list[str]]) -> str:
    valid_dirs = find_valid_dirs(start, pipes)
    return retrieve_matching_pipe(valid_dirs)


def find_valid_dirs(start: tuple[int, int], pipes: list[list[str]]) -> list[tuple[int, int]]:
    valid_dirs = []
    for dir in DIRECTIONS:
        pipe_at_dir = get_pipe_at_dir(start, dir, pipes)
        pipe_mapping = PIPE_MAPPINGS[pipe_at_dir]
        if dir in pipe_mapping:
            valid_dirs.append(dir)

    if len(valid_dirs) != 2:
        raise ValueError("Starting pipe should connect to two directions")

    return valid_dirs


def get_pipe_at_dir(start: tuple[int, int], dir: tuple[int, int], pipes: list[list[str]]) -> str:
    pipe_coordinate = find_next_coordinate(start, dir)
    return get_pipe(pipe_coordinate, pipes)


def find_next_coordinate(start: tuple[int, int], dir: tuple[int, int]) -> tuple[int, int]:
    start_y, start_x = start
    dir_y, dir_x = dir
    pipe_y, pipe_x = start_y + dir_y, start_x + dir_x
    return pipe_y, pipe_x


def retrieve_matching_pipe(valid_dirs: list[tuple[int, int]]) -> str:
    for pipe, pipe_mapping in PIPE_MAPPINGS.items():
        if all(dir in pipe_mapping.values() for dir in valid_dirs):
            return pipe

    raise ValueError("No matching pipe found")


def add_space_in_between_pipes(pipes: list[list[str]]) -> list[list[str]]:
    space_in_between_pipes = []

    len_y = len(pipes)
    len_x = len(pipes[0])

    for y in range(len_y):
        row_current = []
        row_below = []
        for x in range(len_x):
            coordinate = (y, x)
            pipe = get_pipe(coordinate, pipes)
            row_current.append(pipe)

            pipe_outputs = PIPE_MAPPINGS[pipe].values()
            if y + 1 < len_y:
                pipe_down = get_pipe_at_dir(coordinate, D, pipes)
                pipe_down_outputs = PIPE_MAPPINGS[pipe_down].values()
                if D in pipe_outputs and U in pipe_down_outputs:
                    row_below.append("|")
                else:
                    row_below.append("o")

                if x + 1 < len_x:
                    row_below.append("o")

            if x + 1 < len_x:
                pipe_right = get_pipe_at_dir(coordinate, R, pipes)
                pipe_right_outputs = PIPE_MAPPINGS[pipe_right].values()
                if R in pipe_outputs and L in pipe_right_outputs:
                    row_current.append("-")
                else:
                    row_current.append("o")

        space_in_between_pipes.append(row_current)
        if y + 1 < len_y:
            space_in_between_pipes.append(row_below)

    return space_in_between_pipes


def find_non_pipe_islands(pipes: list[list[str]]) -> list[list[tuple[int, int]]]:
    coordinates_seen = set()
    islands = []
    max_y = len(pipes)
    max_x = len(pipes[0])

    for y, row in enumerate(pipes):
        for x, pipe in enumerate(row):
            if (y, x) in coordinates_seen or is_pipe(pipe):
                continue

            coordinate = (y, x)
            island = [coordinate]
            check_neighbours_coordinates = [coordinate]
            coordinates_seen.add(coordinate)

            while check_neighbours_coordinates:
                coordinate = check_neighbours_coordinates.pop()
                for dir in DIRECTIONS:
                    neighbour_coordinate = find_next_coordinate(coordinate, dir)
                    if neighbour_coordinate in coordinates_seen:
                        continue

                    coordinates_seen.add(neighbour_coordinate)

                    if not ((0 <= neighbour_coordinate[0] < max_y) and (0 <= neighbour_coordinate[1] < max_x)):
                        continue

                    neighbour_pipe = get_pipe(neighbour_coordinate, pipes)
                    if is_pipe(neighbour_pipe):
                        continue

                    island.append(neighbour_coordinate)
                    check_neighbours_coordinates.append(neighbour_coordinate)

            islands.append(island)

    return islands


def get_pipe(coordinate: tuple[int, int], pipes: list[list[str]]) -> str:
    y, x = coordinate
    return pipes[y][x]


def is_pipe(pipe: str) -> bool:
    return pipe not in [".", "o"]


def get_non_edge_islands(islands: list[list[tuple[int, int]]], pipes: list[list[str]]) -> list[list[tuple[int, int]]]:
    non_edge_islands = []

    edge_y = 0, len(pipes) - 1
    edge_x = 0, len(pipes[0]) - 1

    for island in islands:
        if not any(c_y in edge_y or c_x in edge_x for c_y, c_x in island):
            non_edge_islands.append(island)
        else:
            pass

    return non_edge_islands


def get_enclosed_islands(
    islands: list[list[tuple[int, int]]], main_loop: set[tuple[int, int]]
) -> list[list[tuple[int, int]]]:
    main_loop_x = defaultdict(list)
    for (y, x) in main_loop:
        main_loop_x[x].append(y)

    main_loop_y = defaultdict(list)
    for (y, x) in main_loop:
        main_loop_y[y].append(x)

    enclosed_islands = []

    for island in islands:
        if is_enclosed_island(island, main_loop_y, main_loop_x):
            enclosed_islands.append(island)

    return enclosed_islands


def is_enclosed_island(
    island: list[tuple[int, int]], main_loop_y: dict[int, list[int]], main_loop_x: dict[int, list[int]]
) -> bool:
    for c_y, c_x in island:
        if c_y % 2 == 1 or c_x % 2 == 1:
            continue

        c_y, c_x = c_y // 2, c_x // 2

        if not is_enclosed_vertical(c_y, c_x, main_loop_x):
            return False

        if not is_enclosed_horizontal(c_y, c_x, main_loop_y):
            return False

    return True


def is_enclosed_vertical(c_y: int, c_x: int, main_loop_x: dict[int, list[int]]) -> bool:
    values_y = main_loop_x[c_x]
    if not values_y:
        return False

    return min(values_y) < c_y < max(values_y)


def is_enclosed_horizontal(c_y: int, c_x: int, main_loop_y: dict[int, list[int]]) -> bool:
    values_x = main_loop_y[c_y]
    if not values_x:
        return False

    return min(values_x) < c_x < max(values_x)


print(get_answer())
