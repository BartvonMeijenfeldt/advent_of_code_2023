from __future__ import annotations

import re
from collections import defaultdict
from copy import copy, deepcopy
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
    supporting_block_to_falling_blocks = get_crucially_supporting_blocks_to_falling_blocks(blocks)
    nr_falling_blocks = sum(len(falling_blocks) for falling_blocks in supporting_block_to_falling_blocks.values())
    return nr_falling_blocks


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


def get_crucially_supporting_blocks_to_falling_blocks(blocks: list[Block]) -> dict[int, set[int]]:
    spot_to_block_nr = {pos: i for i, block in enumerate(blocks) for pos in block.pos_taken}
    blocks_to_supported_by_blocks = {
        i: {spot_to_block_nr[pos] for pos in block.get_new_pos_taken_n_down(1) if pos in spot_to_block_nr}
        for i, block in enumerate(blocks)
    }

    blocks_to_supporting_blocks: dict[int, set[int]] = defaultdict(set)
    for supported_block, supported_by_blocks in blocks_to_supported_by_blocks.items():
        for supported_by_block in supported_by_blocks:
            blocks_to_supporting_blocks[supported_by_block].add(supported_block)

    supporting_block_to_falling_blocks = get_blocks_fall_if_supporting_block_falls(
        blocks_to_supporting_blocks, blocks_to_supported_by_blocks
    )

    return supporting_block_to_falling_blocks


def get_blocks_fall_if_supporting_block_falls(
    blocks_to_supporting_blocks: dict[int, set[int]],
    blocks_to_supported_by_blocks: dict[int, set[int]],
) -> dict[int, set[int]]:
    return {
        block: _get_blocks_that_fall_if_block_falls(block, blocks_to_supporting_blocks, blocks_to_supported_by_blocks)
        for block in blocks_to_supporting_blocks
    }


def _get_blocks_that_fall_if_block_falls(
    support_block: int,
    blocks_to_supporting_blocks: dict[int, set[int]],
    blocks_to_supported_by_blocks: dict[int, set[int]],
):
    blocks_that_might_fall = copy(blocks_to_supporting_blocks[support_block])
    blocks_that_fall: set[int] = {support_block}

    while True:
        any_block_fell = False
        for block in list(blocks_that_might_fall):
            supported_by_blocks = blocks_to_supported_by_blocks[block]
            if supported_by_blocks.issubset(blocks_that_fall):
                blocks_that_fall.add(block)
                any_block_fell = True

                blocks_that_might_fall.remove(block)
                if block in blocks_to_supporting_blocks:
                    new_blocks_that_might_fall = blocks_to_supporting_blocks[block]
                    blocks_that_might_fall.update(new_blocks_that_might_fall)

        if not any_block_fell:
            break

    new_blocks_that_fall = blocks_that_fall - {support_block}
    return new_blocks_that_fall


print(get_answer())
