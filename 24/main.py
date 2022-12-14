#!/usr/bin/env pypy3
import sys
from collections.abc import Callable, Iterable, Sequence
from itertools import count
from typing import NamedTuple
from functools import cache

class Blizzard:
    def __init__(self, char: str, x: int, y: int) -> None:
        self.pos = x, y
        self.char = char
        self.cache = {}  # type: dict[int, tuple[int, int]]
        assert char in {"v", "^", ">", "<"}

    def get_pos_at(
        self, minute: int, width: int, height: int
    ) -> tuple[int, int]:
        if minute == 0:
            return self.pos
        assert minute > 0
        if minute in self.cache:
            return self.cache[minute]
        x, y = self.get_pos_at(minute - 1, width, height)
        if self.char in {"v", "^"}:
            y += -1 if self.char == "^" else 1
            if y < 1:
                y = height - 2
            elif y >= height - 1:
                y = 1
        else:
            x += -1 if self.char == "<" else 1
            if x < 1:
                x = width - 2
            elif x >= width - 1:
                x = 1
        self.cache[minute] = x, y
        return x, y

def get_next_moves(
    curr_pos: tuple[int, int],
    blizz_positions: frozenset[tuple[int, int]],
    maze: Sequence[Sequence[str]],
) -> "Iterable[tuple[int, int]]":
    x, y = curr_pos
    for pos in (
        (x + 1, y),
        (x, y + 1),
        (x, y - 1),
        (x - 1, y),
        curr_pos,
    ):
        if (
            pos[0] < 0 or pos[0] >= len(maze[0])
            or pos[1] < 0 or pos[1] >= len(maze)
            or pos in blizz_positions or maze[pos[1]][pos[0]] == "#"
        ):
            continue
        yield pos
    return


def print_m_b(
    maze: tuple[list[str], ...],
    blizzards: list[Blizzard],
    minute: int,
    pos: "tuple[int, int] | None"
) -> None:
    width, height = len(maze[0]), len(maze)
    maze = tuple(
        [cell for cell in row]
        for row in maze
    )
    blizz_pos = {
        blizz.get_pos_at(minute, width, height): blizz
        for blizz in blizzards
    }
    blizz_pos_list = [
        blizz.get_pos_at(minute, width, height)
        for blizz in blizzards
    ]
    print(f"--- Minute {minute} ---")
    for y in range(height):
        for x in range(width):
            if (x, y) in blizz_pos:
                count = blizz_pos_list.count((x, y))
                print(
                    blizz_pos[(x, y)].char
                    if count == 1
                    else (count if count < 10 else "x"),
                    end="",
                    flush=False
                )
            elif maze[y][x] == "#":
                print("#", end="", flush=False)
            else:
                print(" " if pos != (x, y) else "E", end="", flush=False)
        print()


def solve(input_: str) -> "tuple[int | str, int | str]":
    maze: tuple[list[str], ...] = tuple(map(list, filter(None, input_.split("\n"))))
    width, height = len(maze[0]), len(maze)
    print(width, "x", height)
    pos = (1, 0)
    exi = (width - 2, height - 1)
    blizzards: list[Blizzard] = []
    for y in range(height):
        for x in range(width):
            if maze[y][x] in {"v", "^", ">", "<"}:
                blizzards.append(Blizzard(maze[y][x], x=x, y=y))
                #maze[y][x] = "."

    res1 = -1

    @cache
    def get_blizz_positions(_min: int) -> frozenset[tuple[int, int]]:
        return frozenset(
            blizz.get_pos_at(_min, width, height)
            for blizz in blizzards
        )

    positions: set[tuple[int, int]] = {pos}
    for minute in count(1, 1):
        print(minute, len(positions))
        next_pos: set[tuple[int, int]] = set()
        for _pos in positions:
            next_pos.update(get_next_moves(_pos, get_blizz_positions(minute), maze))
        if exi in next_pos:
            res1 = minute
            break
        positions = next_pos
    positions = {exi}
    for minute in count(res1, 1):
        print(minute, len(positions))
        next_pos: set[tuple[int, int]] = set()
        for _pos in positions:
            next_pos.update(get_next_moves(_pos, get_blizz_positions(minute), maze))
        if pos in next_pos:
            res2 = minute
            break
        positions = next_pos
    positions = {pos}
    for minute in count(res2, 1):
        print(minute, len(positions))
        next_pos: set[tuple[int, int]] = set()
        for _pos in positions:
            next_pos.update(get_next_moves(_pos, get_blizz_positions(minute), maze))
        if exi in next_pos:
            res2 = minute
            break
        positions = next_pos

    # for m in range(minute):
    #     print_m_b(maze, blizzards, m, None)

    return res1, res2


def main() -> "None | int":
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        res1, res2 = solve(sys.stdin.read())
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")
    return None


if __name__ == "__main__":
    sys.exit(main())
