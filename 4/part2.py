from collections import defaultdict


def sum_lottery_tickets(path: str) -> int:
    with open(path, "r", encoding="utf-8-sig") as f:
        nr_tickets = defaultdict(lambda: 0)

        for i, row in enumerate(f.readlines()):
            nr_tickets[i] += 1

            numbers = row.split(":")[1].strip()
            numbers_left, numbers_right = numbers.split("|")
            numbers_left = {int(n) for n in numbers_left.split()}
            numbers_right = {int(n) for n in numbers_right.split()}
            numbers_intersection = numbers_left.intersection(numbers_right)
            for j in range(1, len(numbers_intersection) + 1):
                nr_tickets[i + j] += nr_tickets[i]

    return sum(nr_tickets.values())


path = "4/input.txt"

print(sum_lottery_tickets(path))
