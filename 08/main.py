#!/usr/bin/env python3
import sys

def solve(input_: str) -> tuple[int | str, int | str]:
    lines: list[str] = list(filter(None, input_.split("\n")))

    res1, res2 = 0, 0


    tree_grid = [list(map(int, line)) for line in lines]
    print(tree_grid)
    visibility = [[False] * len(lines[0])] * len(lines)

    for y, line in enumerate(tree_grid):
        for x, tree in enumerate(line):
            vis = False
            if y in {0, len(tree_grid) - 1}:
                vis = True
            elif x in {0, len(line) - 1}:
                vis = True
            elif max(line[:x]) < tree:
                vis = True
            elif max(line[x + 1:]) < tree:
                vis = True
            else:
                cols = [row[x] for row in tree_grid]
                vis = max(cols[:y]) < tree or max(cols[y + 1:]) < tree
            res1 += vis
            print(f"{x=}, {y=}, {vis=}, {tree=!r}, {res1=}")

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
