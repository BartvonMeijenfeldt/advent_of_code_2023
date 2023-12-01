def sum_first_last_dig(path: str) -> int:
    with open(path, "r", encoding="utf-8-sig") as f:
        _sum = 0
        for row in f.readlines():
            numbers = [i for i in row if i.isdigit()]
            firstlast = numbers[0] + numbers[-1]
            _sum += int(firstlast)

    return _sum


path = "1/input.txt"

print(sum_first_last_dig(path))
