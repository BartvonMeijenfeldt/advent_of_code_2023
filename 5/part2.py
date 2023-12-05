def get_answer() -> int:
    seeds, maps = load_data()
    maps = fill_intermediate_ranges(maps)
    locations = get_locations_ranges(seeds, maps)
    return min(locations)


def load_data() -> tuple[list[int, int], list[list[tuple[int, int, int]]]]:
    maps = []
    with open("5/input.txt", "r") as f:
        seeds_line = next(f)
        seeds_line = seeds_line.split(":")[1].strip()
        seeds = [int(s) for s in seeds_line.split()]
        seeds = [(seed, range_) for seed, range_ in zip(seeds[::2], seeds[1::2])]

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
            line[2] = line[1] + line[2]
            map_lines.append(line)

    return seeds, maps


def fill_intermediate_ranges(maps: list[list[tuple[int, int, int]]]):
    return [fill_intermediate_range(map_) for map_ in maps]


def fill_intermediate_range(map: list[tuple[int, int, int]]):
    intermediate_ranges = []

    map = sorted(map, key=lambda x: x[1])

    _, source_prev, source_final_prev = map[0]
    if source_prev > 0:
        intermediate_range_1 = [0, 0, source_prev]
        intermediate_ranges.append(intermediate_range_1)

    for _, source, source_final in map[1:]:
        if source_final_prev < source:
            intermediate_range = [source_final_prev, source_final_prev, source]
            intermediate_ranges.append(intermediate_range)

        source_prev, source_final_prev = source, source_final

    map.extend(intermediate_ranges)
    return sorted(map, key=lambda x: x[1])


def get_locations_ranges(seeds: list[int, int], maps: list[list[tuple[int, int, int]]]) -> list[int]:
    return [loc for seed in seeds for loc in get_location_range(seed[0], seed[1], 0, maps)]


def get_location_range(
    src_start: int,
    range_len: int,
    map_nr: int,
    maps: list[list[tuple[int, int, int]]],
) -> list[int]:
    map = maps[map_nr]
    next_map_nr = map_nr + 1

    for destination, source, source_final in map:
        if source <= src_start < source_final:
            start_destination = destination + src_start - source

            if next_map_nr >= len(maps):
                return [start_destination]

            first_range_len = min(range_len, source_final - src_start)
            location_range = get_location_range(start_destination, first_range_len, next_map_nr, maps)

            if first_range_len < range_len:
                surplus_range_len = range_len - first_range_len
                surplus_range = get_location_range(src_start + first_range_len, surplus_range_len, map_nr, maps)
                location_range.extend(surplus_range)

            return location_range

    if next_map_nr >= len(maps):
        return [src_start]

    return get_location_range(src_start, range_len, next_map_nr, maps)


print(get_answer())
