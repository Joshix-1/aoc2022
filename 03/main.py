#!/usr/bin/env python3

import sys

def main() -> None:
    in_ = sys.stdin.read()
    rucksacks = list(filter(None, in_.split("\n")))
    sum1 = 0
    for r in rucksacks:
        assert len(r) % 2 == 0
        middle = len(r) // 2
        first, second = r[:middle], r[middle:]
        assert len(first) == len(second)
        union = set(first) & set(second)
        assert len(union) == 1
        letter = union.pop()
        sum1 += 1 + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".index(letter)

    print(f"1: {sum1}\n2: ")

if __name__ == "__main__":
    main()
