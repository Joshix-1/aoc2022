#!/usr/bin/env python3
import sys

def to_ints(x, y) -> tuple[int, int]:
    if isinstance(x, int) and isinstance(y, int):
        return x, y
    if isinstance(x, int):
        x = [x]
    elif isinstance(y, int):
        y = [y]
    assert isinstance(x, list) and isinstance(y, list)
    for i in range(max(len(x), len(y))):
        if i >= len(x):
            return 0, 1
        if i >= len(y):
            return 1, 0
        a, b = to_ints(x[i], y[i])
        if a != b:
            return a, b
    return 1, 1

def solve(input_: str) -> tuple[int | str, int | str]:
    lines: list[str] = list(filter(None, input_.split("\n\n")))

    res1, res2 = 0, 0

    for i, pairs in enumerate(lines, 1):
        one, two = list(filter(None, pairs.split("\n")))
        one, two = eval(one), eval(two)
        a, b = to_ints(one, two)
        print(i if a <= b else 0, one, two)
        res1 += i if a <= b else 0

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
