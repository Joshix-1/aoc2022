#!/usr/bin/env python3
import sys
import time

def print_crt(crt):
    for l in crt:
        print("".join(l))

FANCY_DRAWING = __debug__ and sys.stderr.isatty()
SLEEP = 0.1
ON_CHAR = "#"
OFF_CHAR = " "
DEFAULT_CHAR = "."

def draw(crt, x, cycle):
    crt_x = (cycle - 1) % 40
    lit = crt_x in (x - 1, x, x + 1)
    cycle = (cycle - 1) % 240
    # print((cycle) // 40, crt_x)
    crt[(cycle) // 40][crt_x] = ON_CHAR if lit else OFF_CHAR

def solve(input_: str) -> tuple[int | str, int | str]:
    lines: list[str] = list(filter(None, input_.split("\n")))

    res1, res2 = 0, 0

    x = 1

    crt = [[DEFAULT_CHAR] * 40] * 6
    for i in range(len(crt)):
        crt[i] = list(crt[i])

    cycle = 1
    for line in lines:
        if FANCY_DRAWING:
            time.sleep(SLEEP)
            print("\033c", end="")
        print(f"{cycle=}, {x=}, {line=}")
        draw(crt, x, cycle)
        print_crt(crt)
        if cycle in {20, 60, 100, 140, 180, 220}:
            res1 += cycle * x
        if line == "noop":
            cycle += 1
        else:
            assert line.startswith("addx ")
            cycle += 1
            if FANCY_DRAWING:
                time.sleep(SLEEP)
                print("\033c", end="")
            draw(crt, x, cycle)
            if cycle in {20, 60, 100, 140, 180, 220}:
                res1 += cycle * x
            cycle += 1
            x += int(line.removeprefix("addx "))

    return res1, crt

def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        res1, res2 = solve(sys.stdin.read())
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2:")
    print_crt(res2)

if __name__ == "__main__":
    sys.exit(main())
