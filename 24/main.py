#!/usr/bin/env pypy3
import sys
from typing import NamedTuple

class Blizzard:
    def __init__(self, char: str, x: int, y: int) -> None:
        self.pos = x, y
        self.char = char
        self.cache = {}  # type: dict[int, tuple[int, int]]
        assert char in {"v", "^", ">", "<"}

    def get_pos_at(
        self, minute: int, width: int, height: int
    ) -> tuple[int, int]:
        # if minute in self.cache:
        #     return self.cache[minute]
        x, y = self.pos
        if self.char in {"v", "^"}:
            y += minute * (-1 if self.char == "^" else 1)
            if y < 1:
                y = height - 2
            elif y >= height - 1:
                y = 1
        if self.char in {"<", ">"}:
            x += minute * (-1 if self.char == "<" else 1)
            if x < 1:
                x = width - 2
            elif x >= width - 1:
                x = 1
        self.cache[minute] = x, y
        return x, y


class State(NamedTuple):
    minute: int
    x: int
    y: int
    visited: list[tuple[int, int]]

    def get_next_moves(self) -> "list[State]":
        minute = self.minute + 1
        visited = self.visited + [(self.x, self.y)]
        states: "list[State]" = []
        for pos in [
            (self.x + 1, self.y),
            (self.x, self.y + 1),
            (self.x - 1, self.y),
            (self.x, self.y - 1),
            (self.x, self.y),
        ]:
            if pos in visited and visited.count(pos) > 100:
                continue
            if min(pos) < 0:
                continue
            states.append(State(minute, *pos, visited=list(visited)))
        return states

def test():
    pass

def print_m_b(
    maze: list[list[str]],
    blizzards: list[Blizzard],
    minute: int,
    pos: "tuple[int, int] | None"
):
    width, height = len(maze[0]), len(maze)
    maze: list[list[str]] = [
        [cell for cell in row]
        for row in maze
    ]
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
    maze: list[list[str]] = list(map(list, filter(None, input_.split("\n"))))
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
    moves: list[State] = [State(0, pos[0], pos[1], [])]
    blizz_pos_lists: dict[int, tuple[tuple[int, int], ...]] = {}
    while moves:
        moves.sort(key=lambda m: (m.minute, -m.x, -m.y))
        move = moves.pop(0)
        minute, x, y, visited = move
        if (x, y) == exi:
            res1 = minute
            break
        if maze[y][x] == "#":
            continue
        blizz_pos_tpl = blizz_pos_lists[minute] if minute in blizz_pos_lists else tuple(
            blizz.get_pos_at(minute, width, height)
            for blizz in blizzards
        )
        if (x, y) in blizz_pos_tpl:
            continue
        # print_m_b(maze, blizzards, minute, (x, y))
        moves.extend(move.get_next_moves())

    for m in range(minute):
        print_m_b(maze, blizzards, m, None)

    return res1, -1


def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        res1, res2 = solve(sys.stdin.read())
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")


if __name__ == "__main__":
    sys.exit(main())
