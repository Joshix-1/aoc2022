#!/usr/bin/env pypy3
import sys
from collections.abc import Callable, Iterable, Sequence
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


class State:
    minute: int
    pos: tuple[int, int]

    def __init__(self, minute: int, pos: tuple[int, int]) -> None:
        self.minute = minute
        self.pos = pos

    @property
    def x(self) -> int:
        return self.pos[0]

    @property
    def y(self) -> int:
        return self.pos[1]

    def get_next_moves(
        self,
        get_blizz_positions: Callable[[int], frozenset[tuple[int, int]]],
        maze: Sequence[Sequence[str]],
    ) -> "Iterable[State]":
        minute = self.minute + 1
        blizz_pos = get_blizz_positions(minute)
        curr_pos = x, y = self.pos
        yield_count = 0
        for pos in (
            (x + 1, y),
            (x, y + 1),
            (x - 1, y),
            (x, y - 1),
            curr_pos,
        ):
            if pos[0] < 0 or pos[0] >= len(maze[0]) or pos[1] < 0 or pos[1] >= len(maze):
                continue
            if pos in blizz_pos or maze[pos[1]][pos[0]] == "#":
                continue
            yield State(minute, pos)
            yield_count += 1
            if yield_count > 1:
                return
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
    pos = (1, 0)
    exi = (width - 2, height - 1)
    blizzards: list[Blizzard] = []
    for y in range(height):
        for x in range(width):
            if maze[y][x] in {"v", "^", ">", "<"}:
                blizzards.append(Blizzard(maze[y][x], x=x, y=y))
                #maze[y][x] = "."

    res1 = -1
    moves: list[State] = [State(0, pos)]

    @cache
    def get_blizz_positions(_min: int) -> frozenset[tuple[int, int]]:
        return frozenset(
            blizz.get_pos_at(_min, width, height)
            for blizz in blizzards
        )

    last_minute = 0
    while moves:
        # moves.sort(key=lambda m: (m.minute, -m.x, -m.y))
        move = moves.pop(0)
        if move.pos == exi:
            res1 = move.minute
            break
        if move.minute > last_minute:
            last_minute = move.minute
            print(move.minute, "moves:", len(moves))
        # print_m_b(maze, blizzards, minute, (x, y))
        moves.extend(move.get_next_moves(get_blizz_positions, maze))

    # for m in range(minute):
    #     print_m_b(maze, blizzards, m, None)

    return res1, -1


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
