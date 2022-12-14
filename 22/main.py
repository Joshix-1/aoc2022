#!/usr/bin/env pypy3
import os
import re
import sys

FACING = {
    0: ">",
    1: "v",
    2: "<",
    3: "^",
}
FACING_REVERSE = {value: key for key, value in FACING.items()}
FACING_REVERSED = FACING_REVERSE


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


def print_cube(lines, bounds_mapping_only_coords, width):
    os.system("clear")
    print(" ", flush=False, end="")
    for x in range(width + 1):
        if (x, -1) in bounds_mapping_only_coords:
            print("o", flush=False, end="")
        else:
            print(" ", flush=False, end="")
    print()
    for y, line in enumerate(lines + [[" "] * width]):
        if (-1, y) in bounds_mapping_only_coords:
            print("o", flush=False, end="")
        else:
            print(" ", flush=False, end="")
        for x, ch in enumerate(line + [" "]):
            if (x, y) in bounds_mapping_only_coords:
                assert ch == " "
                print("o", flush=False, end="")
            else:
                print(ch, flush=False, end="")
        print()

def solve2(input_: str) -> "int":
    lines: "list[list[str]]" = list(map(list, filter(None, input_.split("\n"))))
    path = re.split(r"(?<=\d)(?=\D)|(?=\d)(?<=\D)", "".join(lines[-1]))
    lines = lines[:-1]
    cube_size = min(len("".join(line).strip()) for line in lines)
    assert cube_size in {50, 4}
    width = max(map(len, lines))
    for line in lines:
        if len(line) < width:
            line.extend([" "] * (width - len(line)))

    facing = 0
    pos: "tuple[int, int]" = (lines[0].index("."), 0)

    cube_grid = []
    for y in range(len(lines), step=cube_size):
        line = []
        cube_grid.append(line)
        for x in range(len(lines[y]), step=cube_size):
            line.append(lines[y][x] != " ")
    cube_net = "\n".join(
        ("".join([("#" if l else ".") for l in line])) for line in cube_grid
    )
    print("net:")
    print(cube_net)
    assert cube_net == ".##\n.#.\n##.\n#..", "sorry, I can't help you today"
    assert cube_size == 50, "test input doesn't work :("
    bounds_mapping: "dict[tuple[str, tuple[int, int]], tuple[str, tuple[int, int]]]" = (
        {}
    )
    for i in range(50):
        """.v#
           .#.
           ##.
           <.."""
        bounds_mapping[("<", (-1, 150 + i))] = ("v", (50 + i, 0))
        """.^#
           .#.
           ##.
           >.."""
        bounds_mapping[("^", (50 + i, -1))] = (">", (0, 150 + i))
        """.#v
           .#.
           ##.
           v.."""
        bounds_mapping[("v", (i, 200))] = ("v", (100 + i, 0))
        """.#^
           .#.
           ##.
           ^.."""
        bounds_mapping[("^", (100 + i, -1))] = ("^", (i, 199))
        """.##
           .>.
           ^#.
           #.."""
        bounds_mapping[("^", (i, 99))] = (">", (50, 50 + i))
        """.##
           .<.
           v#.
           #.."""
        bounds_mapping[("<", (49, 50 + i))] = ("v", (i, 100))
        """.>#
           .#.
           <#.
           #.."""
        bounds_mapping[("<", (-1, 100 + i))] = (">", (50, 49 - i))
        """.<#
           .#.
           >#.
           #.."""
        bounds_mapping[("<", (49, i))] = (">", (0, 149 - i))
        """.#>
           .#.
           #<.
           #.."""
        bounds_mapping[(">", (150, i))] = ("<", (99, 149 - i))
        """.#<
           .#.
           #>.
           #.."""
        bounds_mapping[(">", (100, 100 + i))] = ("<", (149, 49 - i))
        """.#v
           .<.
           ##.
           #.."""
        bounds_mapping[("v", (100 + i, 50))] = ("<", (99, 50 + i))
        """.#^
           .>.
           ##.
           #.."""
        bounds_mapping[(">", (100, 50 + i))] = ("^", (100 + i, 49))
        """.##
           .#.
           #v.
           <.."""
        bounds_mapping[("v", (50 + i, 150))] = ("<", (49, 150 + i))
        """.##
           .#.
           #^.
           >.."""
        bounds_mapping[(">", (50, 150 + i))] = ("^", (50 + i, 149))

    bounds_mapping_only_coords: "dict[tuple[int, int], tuple[int, int]]" = {
        key[1]: value[1] for key, value in bounds_mapping.items()
    }
    print_cube(lines, bounds_mapping_only_coords, width)
    # print(sorted([key[1] for key in bounds_mapping]))
    assert len(set(bounds_mapping.values())) == len(bounds_mapping)
    for i, instruction in enumerate(path):
        #print(f"{pos}, {facing}, {instruction}")
        if instruction in {"L", "R"}:
            facing = rotate(facing, instruction)
            continue
        for _ in range(int(instruction)):
            x, y = move(pos, facing)
            #print(x, y, FACING[facing])
            new_facing = facing
            if (
                (y < 0 or y >= len(lines))
                or (x < 0 or x >= len(lines[y]))
                or lines[y][x] == " "
            ):
                dir_, (x, y) = bounds_mapping[(FACING[facing], (x, y))]
                new_facing = FACING_REVERSE[dir_]
            assert (x, y) not in bounds_mapping_only_coords, f"{(x, y)} {bounds_mapping_only_coords.get((x, y))}"
            assert move((x, y), facing) != (x, y) and bounds_mapping.get(
                (FACING[facing], move((x, y), facing))
            ) != (x, y)
            if lines[y][x] in {".", "<", ">", "v", "^"}:
                lines[pos[1]][pos[0]] = FACING[facing]
                pos = x, y
                facing = new_facing
            elif lines[y][x] == "#":
                pass # print("###", x, y)
            else:
                raise AssertionError()
    lines[pos[1]][pos[0]] = "x"
    #print("\n".join(["".join(line) for line in lines]))
    #print(pos, facing, FACING[facing])
    print_cube(lines, bounds_mapping_only_coords, width)

    print(144361 == 1000 * (pos[1] + 1) + 4 * (pos[0] + 1) + facing)
    return 1000 * (pos[1] + 1) + 4 * (pos[0] + 1) + facing


def solve1(input_: str) -> "int":
    lines: "list[list[str]]" = list(map(list, filter(None, input_.split("\n"))))
    path = re.split(r"(?<=\d)(?=\D)|(?=\d)(?<=\D)", "".join(lines[-1]))
    lines = lines[:-1]
    width = max(map(len, lines))
    for line in lines:
        if len(line) < width:
            line.extend([" "] * (width - len(line)))

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
                    c += 1
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
                        raise AssertionError(
                            f'{pos} {facing}={FACING[facing]}, {x}, {y}, {"".join(lines[y])}'
                        )
            else:
                raise AssertionError()
            if lines[y][x] in {".", "<", ">", "v", "^"}:
                lines[pos[1]][pos[0]] = FACING[facing]
                pos = x, y
            elif lines[y][x] == "#":
                break
            else:
                raise AssertionError()
    lines[pos[1]][pos[0]] = "o"
    print("\n".join(["".join(line) for line in lines]))
    print(pos, facing, FACING[facing])
    return 1000 * (pos[1] + 1) + 4 * (pos[0] + 1) + facing


def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        in_ = sys.stdin.read()
        res1 = solve1(in_)
        print("----")
        res2 = solve2(in_)
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")


if __name__ == "__main__":
    sys.exit(main())
