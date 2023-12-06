from functools import reduce


def get_multiplied_value():
    race = read_race()
    return get_nr_ways(race)


def read_race() -> tuple[int, int]:
    with open("6/input.txt", "r") as f:
        times_line = next(f)
        records_line = next(f)

    times = times_line.split(":")[1].strip().split()
    records = records_line.split(":")[1].strip().split()

    time = reduce(lambda a, b: a + b, times)
    record = reduce(lambda a, b: a + b, records)

    return int(time), int(record)


def get_nr_ways(race: tuple[int, int]) -> list[int]:
    time, record = race
    a = 0
    b = time

    first_beat_record = _find_first_beats_record(a, b, time, record)
    last_beat_record = _find_last_beats_record(a, b, time, record)

    return last_beat_record - first_beat_record + 1


def _find_first_beats_record(a, b, time, record) -> int:
    m = (a + b) // 2
    m_beats_record = beats_record(m, time, record)
    prev_beats_record = beats_record(m - 1, time, record)
    if m_beats_record and not prev_beats_record:
        return m

    if not m_beats_record:
        a = m + 1
    else:
        b = m - 1

    return _find_first_beats_record(a, b, time, record)


def _find_last_beats_record(a, b, time, record) -> int:
    m = (a + b) // 2
    m_beats_record = beats_record(m, time, record)
    next_beats_record = beats_record(m + 1, time, record)
    if m_beats_record and not next_beats_record:
        return m

    if m_beats_record:
        a = m + 1
    else:
        b = m - 1

    return _find_last_beats_record(a, b, time, record)


def beats_record(i, time, record) -> bool:
    return i * (time - i) > record


print(get_multiplied_value())
