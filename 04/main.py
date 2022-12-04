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
        elve1, elve2 = line.split(",")
        r1, r2 = elve_to_range(elve1), elve_to_range(elve2)
        if len(r2) < len(r1):
            r1, r2 = r2, r1
        for el in r1:
            if el in r2:
                count2 += 1
                break
        if len(r1) == len(r2):
            count += r1 == r2
            continue
        assert len(r1) < len(r2)
        if r1[0] in r2 and r1[-1] in r2:
            count += 1
    print(f"1: {count}\n2: {count2}")

if __name__ == "__main__":
    main()
