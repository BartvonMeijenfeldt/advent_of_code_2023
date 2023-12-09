from itertools import pairwise


def get_answer() -> int:
    sequences = get_data()
    extrapolations = get_extrapolated_values(sequences)
    sum_ = sum(extrapolations)
    return sum_


def get_data() -> list[list[int]]:
    with open("9/input.txt", "r") as f:
        sequences = f.read().splitlines()

    return [[int(c) for c in seq.split()] for seq in sequences]


def get_extrapolated_values(sequences: list[list[int]]) -> list[int]:
    return [get_extrapolated_value(seq) for seq in sequences]


def get_extrapolated_value(seq: list[int]) -> int:
    last_numbers = [seq[-1]]
    cur_seq = seq
    while not all(n == 0 for n in cur_seq):
        cur_seq = [b - a for a, b in pairwise(cur_seq)]
        last_numbers.append(cur_seq[-1])

    return sum(last_numbers)


print(get_answer())
