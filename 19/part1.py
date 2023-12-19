from abc import abstractmethod
from dataclasses import dataclass


@dataclass
class Rule:
    destination: str

    @abstractmethod
    def applies(self, part: dict[str, int]) -> bool:
        ...


@dataclass
class MainRule(Rule):
    attribute: str
    greater_than: bool
    cutoff: int

    def applies(self, part: dict[str, int]) -> bool:
        value_part = part[self.attribute]
        if self.greater_than:
            return value_part > self.cutoff
        else:
            return value_part < self.cutoff


@dataclass
class ExceptionRule(Rule):
    def applies(self, part: dict[str, int]) -> bool:
        return True


def get_answer() -> int:
    rules, parts = get_data()
    accepted_parts = get_accepted_parts(parts, rules)
    sum_ = sum(sum(part.values()) for part in accepted_parts)
    return sum_


def get_data() -> tuple[dict[str, list[Rule]], list[dict[str, int]]]:
    with open("19/input.txt", "r") as f:
        rules: dict[str, list[Rule]] = {}
        parts: list[dict[str, int]] = []
        is_part = False
        for row in f.read().splitlines():
            if is_part:
                part = parse_part(row)
                parts.append(part)
            elif row != "":
                rule_str, rule = parse_rule_and_str(row)
                rules[rule_str] = rule
            else:
                is_part = True

    return rules, parts


def parse_rule_and_str(row: str) -> tuple[str, list[Rule]]:
    rule_str, rules_specs = row.split("{")

    rules_specs = rules_specs.split(",")
    main_rules_specs = rules_specs[:-1]
    main_rules = [parse_rule(rule_spec) for rule_spec in main_rules_specs]
    exception_rule = ExceptionRule(rules_specs[-1][:-1])
    rules = main_rules + [exception_rule]

    return rule_str, rules


def parse_rule(rule_str: str) -> MainRule:
    rule_str, destination = rule_str.split(":")
    attribute = rule_str[0]
    greater_than = rule_str[1] == ">"
    cutoff = int(rule_str[2:])
    rule = MainRule(destination, attribute, greater_than, cutoff)
    return rule


def parse_part(row: str) -> dict[str, int]:
    return {pair[0]: int(pair[2:]) for pair in row[1:-1].split(",")}


def get_accepted_parts(parts: list[dict[str, int]], rules: dict[str, list[Rule]]) -> list[dict[str, int]]:
    return [part for part in parts if is_accepted_part(part, rules)]


def is_accepted_part(part: dict[str, int], rules: dict[str, list[Rule]]) -> bool:
    current_destination = "in"

    while True:
        rule_set = rules[current_destination]
        current_destination = find_next_destination(part, rule_set)
        if current_destination == "A":
            return True
        elif current_destination == "R":
            return False


def find_next_destination(part: dict[str, int], rule_set: list[Rule]) -> str:
    for rule in rule_set:
        if rule.applies(part):
            return rule.destination

    raise ValueError("At least exception rule is supposed to apply")


print(get_answer())
