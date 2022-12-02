#!/usr/bin/env python3

import sys
from functools import reduce

def main() -> None:
    _ = tuple(sorted(
        reduce(lambda x, y: x + y, map(int, filter(None, _.split("\n"))))
        for _ in sys.stdin.read().split("\n\n") if _
    ))[-3:]
    print(f"1: {_[-1]}\n2: {sum(_)}")

if __name__ == "__main__":
    sys.exit(main())
