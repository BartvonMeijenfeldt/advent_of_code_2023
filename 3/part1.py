from collections import defaultdict


def sum_first_last_dig(path: str) -> int:
    symbol_locs = get_symbols(path)
    numbers = get_numbers(path)
    _sum = get_sum_numbers(symbol_locs, numbers)

    return _sum


def get_symbols(path: str) -> dict[int, set[int]]:
    with open(path, "r", encoding="utf-8-sig") as f:
        symbol_locs = defaultdict(set)
        for row_nr, row in enumerate(f.readlines()):
            for col_nr, c in enumerate(row):
                if not (c.isdigit() or c == "." or c == "\n"):
                    symbol_locs[row_nr].update([col_nr - 1, col_nr, col_nr + 1])
    return symbol_locs


def get_numbers(path: str) -> list[tuple[int, int, int]]:
    with open(path, "r", encoding="utf-8-sig") as f:
        numbers = []
        for row_nr, row in enumerate(f.readlines()):
            cur_numbers = ""
            for col_nr, c in enumerate(row):
                if c.isdigit():
                    cur_numbers += c
                elif cur_numbers:
                    start_col_nr = col_nr - len(cur_numbers)
                    tuple_to_store = (row_nr, start_col_nr, int(cur_numbers))
                    numbers.append(tuple_to_store)
                    cur_numbers = ""

    return numbers


def get_sum_numbers(symbol_locs: dict[int, set[int]], numbers: list[tuple[int, int, int]]) -> int:
    _sum = 0
    for r, c, v in numbers:
        if is_number_valid_to_add(symbol_locs, r, c, v):
            _sum += v

    return _sum


def is_number_valid_to_add(symbol_locs: dict[int, set[int]], r: int, c: int, v: int) -> bool:
    for r1 in [r - 1, r, r + 1]:
        valid_nr_col_nrs = symbol_locs[r1]
        len_number = len(str(v))
        c_numbers = set(range(c, c + len_number))
        if c_numbers.intersection(valid_nr_col_nrs):
            return True

    return False


path = "3/input.txt"

print(sum_first_last_dig(path))
