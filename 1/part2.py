str_digits = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def sum_first_last_dig(path: str) -> int:
    with open(path, "r", encoding="utf-8-sig") as f:
        _sum = 0
        for row in f.readlines():
            first = find_first(row)
            last = find_last(row)
            firstlast = first + last
            _sum += int(firstlast)

    return _sum


def find_first(row: str) -> str:
    for i, c in enumerate(row):
        if c.isdigit():
            return c

        for nr_chars in [3, 4, 5]:  # Digits 1-9 fully written out have length varying from 3 to 5
            str_nr_chars = row[i : i + nr_chars]
            if str_nr_chars in str_digits:
                return str_digits[str_nr_chars]


def find_last(row: str) -> str:
    row = row[::-1]

    for i, c in enumerate(row):
        if c.isdigit():
            return c

        for nr_chars in [3, 4, 5]:  # Digits 1-9 fully written out have length varying from 3 to 5
            str_nr_chars = row[i : i + nr_chars][::-1]
            if str_nr_chars in str_digits:
                return str_digits[str_nr_chars]


path = "1/input.txt"

print(sum_first_last_dig(path))
