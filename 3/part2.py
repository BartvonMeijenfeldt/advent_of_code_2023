from collections import defaultdict


def sum_first_last_dig(path: str) -> int:
    symbol_locs = get_symbols(path)
    numbers = get_numbers(path)
    _sum = get_sum_numbers(symbol_locs, numbers)

    return _sum


def get_symbols(path: str) -> list[tuple[int, int]]:
    with open(path, "r", encoding="utf-8-sig") as f:
        symbol_locs = []
        for row_nr, row in enumerate(f.readlines()):
            for col_nr, c in enumerate(row):
                if c == "*":
                    symbol_locs.append((row_nr, col_nr))
    return symbol_locs


def get_numbers(path: str) -> dict[int, dict[int, int]]:
    with open(path, "r", encoding="utf-8-sig") as f:
        numbers = defaultdict(dict)
        for row_nr, row in enumerate(f.readlines()):
            cur_numbers = ""
            for col_nr, c in enumerate(row):
                if c.isdigit():
                    cur_numbers += c
                elif cur_numbers:
                    for col_nr2 in range(col_nr - len(cur_numbers), col_nr):
                        numbers[row_nr][col_nr2] = int(cur_numbers)
                    cur_numbers = ""

    return numbers


def get_sum_numbers(symbol_locs: list[tuple[int, int]], numbers: dict[int, dict[int, int]]) -> int:
    _sum = 0
    for r, c in symbol_locs:
        numbers_neighboring = get_numbers_neighboring(r, c, numbers)
        if len(numbers_neighboring) == 2:
            _sum += numbers_neighboring[0] * numbers_neighboring[1]

    return _sum


def get_numbers_neighboring(r: int, c: int, numbers: dict[int, dict[int, int]]) -> bool:
    numbers_neighboring = []
    for r1 in [r - 1, r, r + 1]:
        row_neighbours = {numbers[r1][c1] for c1 in [c - 1, c, c + 1] if c1 in numbers[r1]}
        numbers_neighboring.extend(row_neighbours)

    return numbers_neighboring


path = "3/input.txt"

print(sum_first_last_dig(path))
