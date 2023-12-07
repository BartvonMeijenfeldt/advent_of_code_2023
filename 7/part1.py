from collections import Counter

CARDS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
CARDS_MAP = {card: value for value, card in enumerate(CARDS)}


def get_answer() -> int:
    hands = get_hands()
    hand_strengths = get_hand_strengths(hands)
    hand_strengths.sort(key=lambda x: [x[2]] + x[0], reverse=True)
    mp_valued = sum(bid * rank for rank, (_, bid, _) in enumerate(hand_strengths, start=1))
    return mp_valued


def get_hands() -> list[tuple[list[int], int]]:
    with open("7/input.txt", "r") as f:
        hands = [hand_bid.split() for hand_bid in f.readlines()]

    hands = [(get_hand_int(hand), int(bid)) for hand, bid in hands]
    return hands


def get_hand_int(hand: str) -> tuple[int]:
    return [CARDS_MAP[card] for card in hand]


def get_hand_strengths(hands: list[tuple[list[int], int]]) -> list[tuple[list[int], int, int]]:
    return [(hand, bid, get_hand_strength(hand)) for hand, bid in hands]


def get_hand_strength(hand: dict) -> int:
    values = Counter(hand).values()

    if len(values) == 1:
        return 0
    if len(values) == 2:
        if max(values) == 4:
            return 1
        else:
            return 2

    if max(values) == 3:
        return 3

    if max(values) == 2:
        if sum(value == 2 for value in values) == 2:
            return 4
        else:
            return 5

    return 6


print(get_answer())
