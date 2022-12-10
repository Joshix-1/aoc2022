#!/usr/bin/env python3
import sys

def print_crt(crt):
    for l in crt:
        print("".join(l))

def solve(input_: str) -> tuple[int | str, int | str]:
    lines: list[str] = list(filter(None, input_.split("\n")))

    res1, res2 = 0, 0

    x = 1

    crt = [["#"] * 40] * 6

    cycle = 1
    for line in lines:
        print(f"{cycle=}, {x=}, {line=}")
        print_crt(crt)
        if cycle in {20, 60, 100, 140, 180, 220}:
            res1 += cycle * x
        if line == "noop":
            cycle += 1
        else:
            assert line.startswith("addx ")
            cycle += 1
            if cycle in {20, 60, 100, 140, 180, 220}:
                res1 += cycle * x
            cycle += 1
            x += int(line.removeprefix("addx "))

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
