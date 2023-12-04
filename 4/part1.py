def sum_lottery_tickets(path: str) -> int:
    with open(path, "r", encoding="utf-8-sig") as f:
        _sum = 0
        for row in f.readlines():
            numbers = row.split(":")[1].strip()
            numbers_left, numbers_right = numbers.split("|")
            numbers_left = {int(n) for n in numbers_left.split()}
            numbers_right = {int(n) for n in numbers_right.split()}
            numbers_intersection = numbers_left.intersection(numbers_right)
            if len(numbers_intersection):
                points = 2 ** (len(numbers_intersection) - 1)
                _sum += points

    return _sum


path = "4/input.txt"

print(sum_lottery_tickets(path))
