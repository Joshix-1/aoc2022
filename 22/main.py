#!/usr/bin/env pypy3
import re
import sys

FACING = {
    0: ">",
    1: "v",
    2: "<",
    3: "^",
}


def rotate(facing: int, rot) -> int:
    if rot == "R":
        return (facing + 1) % 4
    elif rot == "L":
        return (facing - 1 + 4) % 4
    raise ValueError("rot is " + str(rot))

def move(pos: tuple[int, int], facing: int) -> tuple[int, int]:
    x, y = pos
    if facing == 0:
        return x + 1, y
    if facing == 1:
        return x, y + 1
    if facing == 2:
        return x - 1, y
    if facing == 3:
        return x, y - 1
    raise ValueError("facing is " + str(facing))

def solve(input_: str) -> "tuple[int | str, int | str]":
    lines: list[list[str]] = list(map(list, filter(None, input_.split("\n"))))
    path = re.split(r"(?<=\d)(?=\D)|(?=\d)(?<=\D)", "".join(lines[-1]))
    lines = lines[:-1]
    res2 = 0

    facing = 0
    pos: tuple[int, int] = (0, lines[0].index("."))

    for instruction in path:
        print(f"{pos=}, {facing=}, {instruction=}")
        if instruction in {"L", "R"}:
            facing = rotate(facing, instruction)
            continue
        for _ in range(int(instruction)):
            x, y = move(pos, facing)
            if FACING[facing] in {"<", ">"}:
                while y < 0 or y >= len(lines) or lines[y][x] == " ":
                    x, y = move(pos, facing)
                    y = (y + len(lines)) % len(lines)
                assert y == pos[1]
            elif FACING[facing] in {"v", "^"}:
                while x < 0 or x >= len(lines[y]) or lines[y][x] == " ":
                    x, y = move(pos, facing)
                    x = (x + len(lines[x])) % len(lines[x])
                assert x == pos[0]
            if lines[y][x] == ".":
                pos = x, y


    res1 = 1000 * (pos[0] + 1) + 8 * (pos[1] + 1) + facing
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
