U = (-1, 0)
R = (0, 1)
D = (1, 0)
L = (0, -1)


PIPE_MAPPINGS = {
    "F": {U: R, L: D},
    "-": {R: R, L: L},
    "7": {R: D, U: L},
    "|": {D: D, U: U},
    "J": {D: L, R: U},
    "L": {L: U, D: R},
}


def get_answer() -> int:
    pipes = get_data()
    start = find_start(pipes)
    loop_length = get_main_loop_length(start, pipes)
    farthest_step = loop_length / 2
    return farthest_step


def get_data() -> list[list[str]]:
    with open("10/input.txt", "r") as f:
        pipes = f.read().splitlines()

    return pipes


def find_start(pipes: list[list[str]]) -> tuple[int, int]:
    for y, row in enumerate(pipes):
        for x, pipe in enumerate(row):
            if pipe == "S":
                return y, x


def get_main_loop_length(s: tuple[int, int], pipes: list[list[int]]) -> int:
    cur_y, cur_x = s
    dir = D  # Saw in input that pipe is connected downwards, could have programatically found this out as well.
    nr_steps = 0

    while True:
        cur_y += dir[0]
        cur_x += dir[1]
        nr_steps += 1

        pipe_at_dir = pipes[cur_y][cur_x]
        if pipe_at_dir == "S":
            return nr_steps

        dir = PIPE_MAPPINGS[pipe_at_dir][dir]


print(get_answer())
