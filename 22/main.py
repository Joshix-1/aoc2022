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

def move(pos: "tuple[int, int]", facing: int) -> "tuple[int, int]":
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
    lines: "list[list[str]]" = list(map(list, filter(None, input_.split("\n"))))
    path = re.split(r"(?<=\d)(?=\D)|(?=\d)(?<=\D)", "".join(lines[-1]))
    lines = lines[:-1]
    width = max(map(len, lines))
    for line in lines:
        if len(line) < width:
            line.extend([" "] * (width - len(line)))
    # print("\n".join(["".join(line) for line in lines]))
    height = len(lines)
    res2 = 0

    facing = 0
    pos: "tuple[int, int]" = (lines[0].index("."), 0)

    for instruction in path:
        print(f"{pos}, {facing}, {instruction}")
        if instruction in {"L", "R"}:
            facing = rotate(facing, instruction)
            continue
        for _ in range(int(instruction)):
            x, y = move(pos, facing)
            # print(x, y)
            c = 0
            if FACING[facing] in {"^", "v"}:
                while y < 0 or y >= len(lines) or lines[y][x] == " ":
                    x, y = move((x, y), facing)
                    y = (y + len(lines)) % len(lines)
                    # print(f"  y={y}")
                    assert x == pos[0]
                    c +=1
                    if c > len(lines):
                        raise AssertionError(pos, FACING[facing], x, y)
            elif FACING[facing] in {">", "<"}:
                while x < 0 or x >= len(lines[y]) or lines[y][x] == " ":
                    x, y = move((x, y), facing)
                    x = (x + len(lines[y])) % len(lines[y])
                    # print(f"  x={x}")
                    assert y == pos[1]
                    c += 1
                    if c > len(lines[y]):
                        raise AssertionError(f'{pos} {facing}={FACING[facing]}, {x}, {y}, {"".join(lines[y])}')
            else:
                raise AssertionError()
            if lines[y][x] in {".", "<", ">", "v", "^"}:
                lines[pos[1]][pos[0]] = FACING[facing]
                pos = x, y
            elif lines[y][x] == "#":
                break
            else:
                raise AssertionError()
    print("\n".join(["".join(line) for line in lines]))
    print(pos, facing, FACING[facing])
    res1 = 1000 * (pos[1] + 1) + 4 * (pos[0] + 1) + facing
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
