def get_answer() -> int:
    initialization_sequence = get_data()
    values = get_values(initialization_sequence)
    return sum(values)


def get_data() -> list[str]:
    with open("15/input.txt", "r") as f:
        line = f.read()

    return line.split(",")


def get_values(initialization_sequence: list[str]) -> list[int]:
    return [get_value(command) for command in initialization_sequence]


def get_value(command: str) -> int:
    value = 0
    for c in command:
        value += ord(c)
        value *= 17
        value %= 256

    return value


print(get_answer())
