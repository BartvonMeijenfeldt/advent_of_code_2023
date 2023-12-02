from collections import defaultdict

max_cubes = {"red": 12, "green": 13, "blue": 14}


def sum_first_last_dig(path: str) -> int:
    with open(path, "r", encoding="utf-8-sig") as f:
        _sum = 0
        for row in f.readlines():
            game_str, info_str = row.strip().split(":")
            if is_game_possible(info_str):
                game_nr = int(game_str.split()[-1])
                _sum += game_nr

    return _sum


def is_game_possible(info_str: str) -> bool:
    max_color = defaultdict(lambda: 0)

    draws = info_str.split(";")

    for draw in draws:
        for color_draw in draw.strip().split(","):
            nr, color = color_draw.split()
            nr = int(nr)
            max_color[color] = max(max_color[color], nr)
            if max_color[color] > max_cubes[color]:
                return False

    return True


path = "2/input.txt"

print(sum_first_last_dig(path))
