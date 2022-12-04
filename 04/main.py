#!/usr/bin/env python3

import sys

def elve_to_range(elve: str) -> list[int]:
    start, end = elve.split("-")
    return list(range(int(start), int(end) + 1))

def main() -> None:
    in_ = filter(None, sys.stdin.read().split("\n"))

    count = 0
    count2 = 0
    for line in in_:
        r1, r2 = [elve_to_range(elve) for elve in line.split(",")]
        if len(r2) < len(r1):
            r1, r2 = r2, r1
        bools = [el in r2 for el in r1]
        count += all(bools)
        count2 += any(bools)

    print(f"1: {count}\n2: {count2}")

if __name__ == "__main__":
    main()
