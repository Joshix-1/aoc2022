#!/usr/bin/env python3
import sys

def solve(input_: str) -> tuple[int | str, int | str]:
    lines: list[str] = list(filter(None, input_.split("\n")))

    res1 = 0


    tree_grid = [list(map(int, line)) for line in lines]
    print(tree_grid)
    visibility = [[False] * len(lines[0])] * len(lines)

    senic_scores = []

    for y, line in enumerate(tree_grid):
        for x, tree in enumerate(line):
            vis = False
            cols = [row[x] for row in tree_grid]
            if y in {0, len(tree_grid) - 1}:
                vis = True
            elif x in {0, len(line) - 1}:
                vis = True
            elif max(line[:x]) < tree:
                vis = True
            elif max(line[x + 1:]) < tree:
                vis = True
            else:
                vis = max(cols[:y]) < tree or max(cols[y + 1:]) < tree
            res1 += vis
            print(f"{x=}, {y=}, {vis=}, {tree=!r}, {res1=}")

            x1 = 0
            for x_ in range(x + 1, len(line)):
                assert x_ != x
                if line[x_] >= tree:
                    break
                x1 += 1
            
            x2 = 0
            for x_ in reversed(list(range(x))):
                assert x_ != x
                x2 += 1
                if line[x_] >= tree:
                    break
                
            y1 = 0
            for y_ in range(y + 1, len(cols)):
                assert y_ != y
                y1 += 1
                if cols[y_] >= tree:
                    break
                
            y2 = 0
            for y_ in reversed(list(range(y))):
                assert y_ != y
                y2 += 1
                if cols[y_] >= tree:
                    break
                
            senic_scores.append(x1 * x2 * y1 * y2)

    return res1, max(senic_scores)

def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        res1, res2 = solve(sys.stdin.read())
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")

if __name__ == "__main__":
    sys.exit(main())
