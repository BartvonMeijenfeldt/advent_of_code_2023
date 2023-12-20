from __future__ import annotations

from abc import abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from itertools import count
from math import lcm


@dataclass
class Pulse:
    sender: Module
    high_pulse: bool
    receiver: Module


@dataclass
class Module:
    name: str
    receiver_names: list[str]
    low_pulses_received = 0
    high_pulses_received = 0

    def set_receivers(self, all_receivers: dict[str, Module]) -> None:
        self.receivers = [all_receivers[name] for name in self.receiver_names]

    @abstractmethod
    def parse_pulse(self, sender: Module, high_pulse: bool) -> list[Pulse]:
        """Receives the pulse, adjusts internal state and returns new pulses to parse.

        Args:
            sender (Module): From what module the pulse is received
            high_pulse (bool): Whether the received pulse is high (True) or low (False)

        Returns:
            list[Pulse]: list of pulses to parse
        """
        ...

    def _count_pulse(self, high_pulse: bool) -> None:
        if high_pulse:
            self.high_pulses_received += 1
        else:
            self.low_pulses_received += 1


@dataclass
class BroadcasterModule(Module):
    def parse_pulse(self, sender: Module, high_pulse: bool) -> list[Pulse]:
        return self._parse_pulse(high_pulse)

    def _parse_pulse(self, high_pulse: bool) -> list[Pulse]:
        self._count_pulse(high_pulse)
        return self._send_signal(high_pulse=high_pulse)

    def parse_button_press(self) -> list[Pulse]:
        return self._parse_pulse(high_pulse=False)

    def _send_signal(self, high_pulse: bool) -> list[Pulse]:
        return [Pulse(self, high_pulse, receiver) for receiver in self.receivers]


@dataclass
class FlipFlopModule(Module):
    on = False

    def parse_pulse(self, sender: Module, high_pulse: bool) -> list[Pulse]:
        self._count_pulse(high_pulse)

        if high_pulse:
            return []
        self.on = not self.on
        return [Pulse(self, self.on, receiver) for receiver in self.receivers]


@dataclass
class ConjunctionModule(Module):
    def set_senders(self, senders: list[Module]) -> None:
        self.senders_to_signal = {module.name: False for module in senders}

    def set_receivers(self, all_receivers: dict[str, Module]) -> None:
        super().set_receivers(all_receivers)

    def parse_pulse(self, sender: Module, high_pulse: bool) -> list[Pulse]:
        self._count_pulse(high_pulse)
        self.senders_to_signal[sender.name] = high_pulse

        high_pulse = not all(self.senders_to_signal.values())
        return [Pulse(self, high_pulse, receiver) for receiver in self.receivers]


@dataclass
class TestModule(Module):
    def parse_pulse(self, sender: Module, high_pulse: bool) -> list[Pulse]:
        self._count_pulse(high_pulse)
        return []


def get_answer() -> int:
    modules = get_data()
    cycle_lengths = get_cycle_lengths(modules)
    lcm_ = lcm(*cycle_lengths)
    return lcm_


def get_cycle_lengths(modules: dict[str, Module]) -> list[int]:
    broadcaster: BroadcasterModule = modules["broadcaster"]
    groups = [get_groups(receiver) for receiver in broadcaster.receivers]
    cycle_lengths = [_get_cycle_length_group(broadcaster, *group) for group in groups]
    return cycle_lengths


def get_groups(source: Module) -> tuple[Module, Module]:
    to_parse = [source]
    already_parsed = {source.name}
    while to_parse:
        m = to_parse.pop()
        for r in m.receivers:
            if r.name not in already_parsed:
                already_parsed.add(r.name)
                if r.name == "mf":
                    sink = m
                    return source, sink
                else:
                    to_parse.append(r)

    raise ValueError("Not supposed to reach here")


def _get_cycle_length_group(broadcaster: Module, source: Module, sink: Module) -> int:
    nr_times_activated = 0
    last_press_nr = 0

    for nr_presses in count(start=1):
        pulses = source.parse_pulse(broadcaster, high_pulse=False)
        activated = False

        while pulses:
            pulse = pulses.pop(0)
            if pulse.sender.name == sink.name and pulse.high_pulse:
                activated = True
                if nr_times_activated == 1:
                    cycle_length = nr_presses - last_press_nr
                    start = nr_presses % cycle_length
                    assert start == 0  # make sure cycles started from 0
                    return cycle_length

            new_pulses = pulse.receiver.parse_pulse(pulse.sender, pulse.high_pulse)
            pulses.extend(new_pulses)

        if activated:
            last_press_nr = nr_presses
            nr_times_activated += 1

    raise ValueError("No solution found")


def get_data() -> dict[str, Module]:
    with open("20/input.txt", "r") as f:
        modules = [parse_module(row) for row in f.read().splitlines()]

    modules = {module.name: module for module in modules}
    for module in list(modules.values()):
        for receiver_name in module.receiver_names:
            if receiver_name not in modules:
                test_module = TestModule(receiver_name, [])
                modules[test_module.name] = test_module

    for module in modules.values():
        module.set_receivers(modules)

    module_to_senders = defaultdict(list)
    for module in modules.values():
        for receiver in module.receivers:
            module_to_senders[receiver.name].append(module)

    for module in modules.values():
        if isinstance(module, ConjunctionModule):
            senders = module_to_senders[module.name]
            module.set_senders(senders)

    return modules


def parse_module(row: str) -> Module:
    name, receiver_names = row.split("->")
    module_identifier = name[0]
    name = name[1:].strip()
    receiver_names = receiver_names.strip().split(", ")
    if module_identifier == "b":
        return BroadcasterModule("broadcaster", receiver_names)
    elif module_identifier == "%":
        return FlipFlopModule(name, receiver_names)
    elif module_identifier == "&":
        return ConjunctionModule(name, receiver_names)
    else:
        raise ValueError("Unknown module")


print(get_answer())
