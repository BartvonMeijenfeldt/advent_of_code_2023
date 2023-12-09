from math import lcm


def get_answer() -> int:
    instructions, nodes = get_data()
    nodes = convert_nodes_to_graph(nodes)
    start_nodes = get_start_nodes(nodes)
    cycle_lengths = find_first_end_z(instructions, start_nodes, nodes)
    lowest_common_multiple = lcm(*cycle_lengths)
    return lowest_common_multiple


def get_data() -> tuple[str, list[tuple[str, str, str]]]:
    with open("8/input.txt", "r") as f:
        instructions = next(f).strip()
        next(f)
        nodes = [get_node(node_line) for node_line in f.readlines()]

    return instructions, nodes


def get_node(node_line: str) -> list[tuple[str, str, str]]:
    node_line = node_line.strip()
    source, left_right = node_line.split(" = ")
    left, right = left_right[1:-1].split(", ")
    return source, left, right


def convert_nodes_to_graph(nodes: list[tuple[str, str, str]]) -> dict[str, dict[str, str]]:
    return {source: {"L": l, "R": r} for source, l, r in nodes}


def get_start_nodes(nodes: dict[str, dict[str, str]]) -> list[str]:
    return [node for node in nodes.keys() if node.endswith("A")]


def find_first_end_z(instructions: str, start_nodes: list[str], nodes: dict[str, dict[str, str]]) -> list[int]:
    return [get_next_nr_steps(0, current, nodes, instructions) for current in start_nodes]


def get_next_nr_steps(
    start_nr_steps: int,
    start: str,
    nodes: dict[str, dict[str, str]],
    instructions: str,
) -> int:
    nr_extra_steps = 0
    current = start

    while True:
        total_nr_steps = start_nr_steps + nr_extra_steps
        current = iter_step(instructions, total_nr_steps, current, nodes)
        nr_extra_steps += 1
        if current.endswith("Z"):
            return nr_extra_steps


def iter_step(instructions: str, nr_steps: int, current: str, nodes: dict[str, dict[str, str]]) -> str:
    instruction_index = get_index(instructions, nr_steps)
    next_step = instructions[instruction_index]
    node = nodes[current][next_step]
    return node


def get_index(instructions: str, nr_steps: int) -> int:
    return nr_steps % len(instructions)


print(get_answer())
