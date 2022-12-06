#!/usr/bin/env python3
import sys

def solve(input_: str) -> tuple[int | str, int | str]:
    chars: list[str] = list(filter(None, input_.strip()))

    res1, res2 = 0, 0

    for i in range(len(chars) - 4):
        ch = chars[i]
        _4 = chars[i:i+4]
        print(f"{res1=}, {res2=}, {ch=}, {_4=}")
        if len(set(_4)) == 4:
            res1 = i+4
            break

    for i in range(len(chars) - 14):
        ch = chars[i]
        _14 = chars[i:i+14]
        print(f"{res1=}, {res2=}, {ch=}, {_14=}")
        if len(set(_14)) == 14:
            res2 = i+14
            break

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
