def get_answer() -> int:
    instructions, nodes = get_data()
    nodes = convert_nodes_to_graph(nodes)
    nr_steps = find_nr_steps_zzz(instructions, nodes)
    return nr_steps


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


def find_nr_steps_zzz(instructions: str, nodes: dict[str, dict[str, str]]) -> int:
    nr_steps = 0
    current = "AAA"

    while current != "ZZZ":
        next_step = instructions[nr_steps % len(instructions)]
        current = nodes[current][next_step]
        nr_steps += 1

    return nr_steps


print(get_answer())
