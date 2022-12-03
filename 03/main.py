#!/usr/bin/env python3

import sys

PRIO="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def main() -> None:
    in_ = sys.stdin.read()
    rucksacks = list(filter(None, in_.split("\n")))
    sum1 = 0
    sum2 = 0
    for r in rucksacks:
        assert len(r) % 2 == 0
        middle = len(r) // 2
        first, second = r[:middle], r[middle:]
        assert len(first) == len(second)
        union = set(first) & set(second)
        assert len(union) == 1
        letter = union.pop()
        sum1 += 1 + PRIO.index(letter)
    for i in range(len(rucksacks) // 3):
        first, second, third = rucksacks[3 * i:3*i+3]
        union = set(first) & set(second)
        union &= set(third) & set(first)
        assert len(union) == 1
        letter = union.pop()
        sum2 += 1 + PRIO.index(letter)
    print(f"1: {sum1}\n2: {sum2}")

if __name__ == "__main__":
    main()
