from __future__ import annotations

from abc import abstractmethod
from collections import defaultdict
from dataclasses import dataclass


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
    press_button(modules, 1000)

    nr_low_pulses = sum(module.low_pulses_received for module in modules.values())
    nr_high_pulses = sum(module.high_pulses_received for module in modules.values())

    answer = nr_low_pulses * nr_high_pulses
    return answer


def press_button(modules: dict[str, Module], n: int) -> None:
    broadcaster: BroadcasterModule = modules["broadcaster"]

    for _ in range(n):
        pulses = broadcaster.parse_button_press()
        while pulses:
            pulse = pulses.pop()
            new_pulses = pulse.receiver.parse_pulse(pulse.sender, pulse.high_pulse)
            pulses.extend(new_pulses)


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
