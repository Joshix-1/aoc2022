#!/usr/bin/env python3
import sys
from dataclasses import dataclass
sys.setrecursionlimit(16385)
def get_next(i, x, y):
    if i == 0:
        return (x + 1, y)
    if i == 1:
        return (x, y + 1)
    if i == 2:
        return (x - 1, y)
    if i == 3:
        return (x, y - 1)
    assert False

@dataclass
class Cell:
    char: str
    dist: int = None
    new_char: str = None

def solve_maze(maze: "list[list[str]]", x, y, ev: str) -> int:
    if min(x, y) < 0 or x >= len(maze[0]) or y >= len(maze):
        return None
    curr = maze[y][x].char
    if curr == "E":
        maze[y][x].dist = 0
        return 0 if ev in {"z", "y"} else None
    if curr != "S":
        diff = ord(curr) - ord(ev)
        if diff > 1:
            #print(diff, ev, curr)
            return None
    if maze[y][x].new_char:
        return maze[y][x].dist
    # can go to this
    maze[y][x].new_char = "."
    ret = [0, 0, 0, 0]
    for i in reversed(range(4)):
        ret[i] = solve_maze(
            maze,
            *get_next(i,x,y),
            curr if curr != "S" else "a"
        )
    ret_ = list(filter(lambda x: x is not None, ret))
    if ret_:
        maze[y][x].dist = min(ret_) + 1
        maze[y][x].new_char = ">V<^"[ret.index(min(ret_))]
        return min(ret_) + 1
    return maze[y][x].dist

def solve(input_: str) -> "tuple[int | str, int | str]":
    lines: list[str] = list(filter(None, input_.split("\n")))

    res1, res2 = 0, 0
    assert lines[0][0] == "S" or lines[20][0] == "S"
    maze = [[Cell(c) for c in x] for x in lines]
    res1 = solve_maze(
        maze,
        0,
        0 if lines[0][0] == "S" else 20,
        "a"
    )
    res1 = solve_maze(
        maze,
        0,
        0 if lines[0][0] == "S" else 20,
        "a"
    )

    for line in maze:
        print("".join([c.new_char or c.char for c in line]))
        pass # print(f"{res1=}, {res2=}, {line=}")

    return res1, res2

def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        res1, res2 = solve(sys.stdin.read())
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")

if __name__ == "__main__":
    sys.exit(main())
