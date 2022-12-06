#!/usr/bin/env python3
import sys

def solve(input_: str) -> tuple[int | str, int | str]:
    res1, res2 = 0, 0

    for i in range(len(input_) - 4):
        _4 = input_[i:i+4]
        if len(set(_4)) == 4:
            res1 = i+4
            break

    for i in range(len(input_) - 14):
        _14 = input_[i:i+14]
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
