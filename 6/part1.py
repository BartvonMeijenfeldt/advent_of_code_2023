from functools import reduce


def get_multiplied_value():
    races = read_races()
    nr_ways = get_nr_ways(races)
    return reduce(lambda a, b: a * b, nr_ways)


def read_races() -> list[tuple[int, int]]:
    with open("6/input.txt", "r") as f:
        times_line = next(f)
        records_line = next(f)

    times = times_line.split(":")[1].strip().split()
    records = records_line.split(":")[1].strip().split()

    return [(int(time), int(record)) for time, record in zip(times, records)]


def get_nr_ways(races: list[tuple[int, int]]) -> list[int]:
    return [get_nr_ways_race(race) for race in races]


def get_nr_ways_race(race: tuple[int, int]) -> int:
    time, record = race

    return sum(True for i in range(time) if i * (time - i) > record)


print(get_multiplied_value())
