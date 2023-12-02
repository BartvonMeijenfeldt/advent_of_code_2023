from functools import reduce


def sum_first_last_dig(path: str) -> int:
    with open(path, "r", encoding="utf-8-sig") as f:
        _sum = 0
        for row in f.readlines():
            game_str, info_str = row.strip().split(":")
            min_cubes_required = get_min_cubes_required(info_str)
            power = reduce(lambda x, y: x * y, min_cubes_required)
            _sum += power

    return _sum


def get_min_cubes_required(info_str: str) -> list[int]:
    min_cubes = {"red": 0, "green": 0, "blue": 0}

    draws = info_str.split(";")

    for draw in draws:
        for color_draw in draw.strip().split(","):
            nr, color = color_draw.split()
            nr = int(nr)
            min_cubes[color] = max(min_cubes[color], nr)

    return [v for v in min_cubes.values()]


path = "2/input.txt"

print(sum_first_last_dig(path))
