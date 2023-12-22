from __future__ import annotations

import re
from copy import deepcopy
from dataclasses import dataclass


@dataclass
class Block:
    x_start: int
    y_start: int
    z_start: int
    x_end: int
    y_end: int
    z_end: int

    @property
    def pos_taken(self) -> list[tuple[int, int, int]]:
        return [
            (x, y, z)
            for x in range(self.x_start, self.x_end + 1)
            for y in range(self.y_start, self.y_end + 1)
            for z in range(self.z_start, self.z_end + 1)
        ]

    def get_nr_positions_can_drop(self, all_spots_taken: set[tuple[int, int, int]]) -> int:
        if self.z_start == 1:
            return 0

        nr_positions_can_drop = 0

        while not (set(self.get_new_pos_taken_n_down(nr_positions_can_drop + 1)) & all_spots_taken):
            nr_positions_can_drop += 1
            if self.z_start - nr_positions_can_drop == 1:
                break

        return nr_positions_can_drop

    def drop_n_positions(self, n: int) -> None:
        self.z_start -= n
        self.z_end -= n

    def get_new_pos_taken_n_down(self, n: int) -> list[tuple[int, int, int]]:
        return [
            (x, y, self.z_start - n)
            for x in range(self.x_start, self.x_end + 1)
            for y in range(self.y_start, self.y_end + 1)
        ]


def get_answer() -> int:
    blocks = get_data()
    blocks = drop_blocks(blocks)
    disintegratable_blocks = get_disintegratable_blocks(blocks)
    nr_disintegratable_blocks = len(disintegratable_blocks)
    return nr_disintegratable_blocks


def get_data() -> list[Block]:
    with open("22/input.txt", "r") as f:
        blocks = [parse_block(row) for row in f.read().splitlines()]

    return blocks


def parse_block(row: str):
    return Block(*[int(c) for c in re.split(",|~", row)])


def drop_blocks(blocks: list[Block]) -> list[Block]:
    blocks = deepcopy(blocks)
    all_taken_pos: set[tuple[int, int, int]] = {pos for block in blocks for pos in block.pos_taken}
    while True:
        any_block_moved = False
        for block in blocks:
            nr_positions_can_drop = block.get_nr_positions_can_drop(all_taken_pos)
            if nr_positions_can_drop:
                all_taken_pos -= set(block.pos_taken)
                block.drop_n_positions(nr_positions_can_drop)
                all_taken_pos |= set(block.pos_taken)
                any_block_moved = True

        if not any_block_moved:
            break

    return blocks


def get_disintegratable_blocks(blocks: list[Block]) -> list[int]:
    spot_to_block_nr = {pos: i for i, block in enumerate(blocks) for pos in block.pos_taken}
    supported_by_blocks = {
        i: {spot_to_block_nr[pos] for pos in block.get_new_pos_taken_n_down(1) if pos in spot_to_block_nr}
        for i, block in enumerate(blocks)
    }
    crucially_supporting_blocks = {
        list(support_blocks)[0] for support_blocks in supported_by_blocks.values() if len(support_blocks) == 1
    }

    disintegrable_blocks: set[int] = {i for i in range(len(blocks))} - crucially_supporting_blocks

    return list(disintegrable_blocks)


print(get_answer())
