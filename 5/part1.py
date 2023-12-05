def get_answer() -> int:
    seeds, maps = load_data()
    locations = get_locations(seeds, maps)
    return min(locations)


def load_data() -> tuple[list[int], list[list[tuple[int, int, int]]]]:
    maps = []
    with open("input.txt", "r") as f:
        seeds_line = next(f)
        seeds_line = seeds_line.split(":")[1].strip()
        seeds = [int(s) for s in seeds_line.split()]

        next(f)
        next(f)
        map_lines = []

        for row in f.readlines():
            row = row.strip()
            if row.endswith("map:"):
                maps.append(map_lines)
                map_lines = []
                continue

            if row == "":
                continue

            line = [int(n) for n in row.split()]
            map_lines.append(line)

    return seeds, maps


def get_locations(seeds: list[int], maps: list[list[tuple[int, int, int]]]) -> list[int]:
    return [get_location(seed, maps) for seed in seeds]


def get_location(seed: int, maps: list[list[tuple[int, int, int]]]) -> int:
    n = seed
    for map in maps:
        n = get_next_number(n, map)

    return n


def get_next_number(n, map):
    for destination, source, range_ in map:
        if source <= n < source + range_:
            return destination + (n - source)

    return n


print(get_answer())
