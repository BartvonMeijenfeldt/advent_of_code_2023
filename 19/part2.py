from copy import deepcopy
from dataclasses import dataclass
from typing import Optional

MIN_VALUE = 1
MAX_VALUE = 4000


@dataclass
class Rule:
    destination: str


@dataclass
class MainRule(Rule):
    attribute: str
    greater_than: bool
    cutoff: int


@dataclass
class ExceptionRule(Rule):
    pass


def get_answer() -> int:
    rules = get_data()
    accepted_part_ranges = get_accepted_part_ranges(rules)
    nr_parts_per_range = [get_nr_parts(part_range) for part_range in accepted_part_ranges]
    nr_parts = sum(nr_parts_per_range)
    return nr_parts


def get_data() -> dict[str, list[Rule]]:
    with open("19/input.txt", "r") as f:
        rules: dict[str, list[Rule]] = {}
        for row in f.read().splitlines():
            if row == "":
                break

            rule_str, rule = parse_rule_and_str(row)
            rules[rule_str] = rule

    return rules


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


def get_accepted_part_ranges(rules: dict[str, list[Rule]]) -> list[dict[str, tuple[int, int]]]:
    part_range = dict(
        x=(MIN_VALUE, MAX_VALUE), m=(MIN_VALUE, MAX_VALUE), a=(MIN_VALUE, MAX_VALUE), s=(MIN_VALUE, MAX_VALUE)
    )
    current_destination = "in"

    return _get_accepted_part_ranges(rules, part_range, current_destination)


def _get_accepted_part_ranges(
    rules: dict[str, list[Rule]], part_range: dict[str, tuple[int, int]], current_destination: str
) -> list[dict[str, tuple[int, int]]]:
    if current_destination == "A":
        return [part_range]
    elif current_destination == "R":
        return []

    current_part_range = part_range

    accepted_ranges: list[dict[str, tuple[int, int]]] = []
    rule_set = rules[current_destination]
    for rule in rule_set:
        if isinstance(rule, MainRule):
            attribute_range = current_part_range[rule.attribute]
            if rule.greater_than:
                destination_range = (rule.cutoff + 1, attribute_range[1])
                new_part_range = (attribute_range[0], rule.cutoff)
            else:
                destination_range = (attribute_range[0], rule.cutoff - 1)
                new_part_range = (rule.cutoff, attribute_range[1])

            destination_part_range = get_new_part_range(current_part_range, rule.attribute, destination_range)
            current_part_range = get_new_part_range(current_part_range, rule.attribute, new_part_range)

        else:
            destination_part_range = current_part_range
            current_part_range = None

        if destination_part_range:
            added_ranges = _get_accepted_part_ranges(rules, destination_part_range, rule.destination)
            accepted_ranges.extend(added_ranges)

        if current_part_range is None:
            break

    return accepted_ranges


def get_new_part_range(
    part_range: dict[str, tuple[int, int]], attribute: str, new_range: tuple[int, int]
) -> Optional[dict[str, tuple[int, int]]]:
    if new_range[0] > new_range[1]:
        return None

    part_range = deepcopy(part_range)
    part_range[attribute] = new_range
    return part_range


def get_nr_parts(part_range: dict[str, tuple[int, int]]) -> int:
    nr_parts = 1
    for attribute_range in part_range.values():
        range_size = attribute_range[1] - attribute_range[0] + 1
        nr_parts *= range_size

    return nr_parts


print(get_answer())
