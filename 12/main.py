#!/usr/bin/env python3
import sys

def get_next(i, x, y):
    if i == 0:
        return (x + 1, y)
    if i == 1:
        return (x, y + 1)
    if i == 2:
        return (x - 1, y)
    if i == 3:
        return (x, y - 1)
    assert False

def solve_maze(maze: "list[list[str]]", x, y, ev: str) -> int:
    if min(x, y) < 0 or x >= len(maze[0]) or y >= len(maze):
        return 0
    #for line in maze:
    #    print("".join(line))
    curr = maze[y][x]
    if curr == "E":
        return int(ev in {"z", "y"})
    if curr in ".<>^V":
        return 0
    if curr != "S":
        diff = ord(curr) - ord(ev)
        if diff > 1:
            #print(diff, ev, curr)
            return 0
    # can go to this
    maze[y][x] = "."
    ret = [0, 0, 0, 0]
    for i in range(4):
        ret[i] = solve_maze(
            maze,
            *get_next(i,x,y),
            curr if curr != "S" else "a"
        )
    ret_ = list(filter(None, ret))
    if ret_:
        maze[y][x] = ">^<V"[ret.index(min(ret_))]
        return min(ret_) + 1
    maze[y][x] = curr
    return 0

def solve(input_: str) -> tuple[int | str, int | str]:
    lines: list[str] = list(filter(None, input_.split("\n")))

    res1, res2 = 0, 0
    assert lines[0][0] == "S" or lines[20][0] == "S"
    res1 = solve_maze(
        [list(x) for x in lines],
        0,
        0 if lines[0][0] == "S" else 20,
        "a"
    ) - 1
    for line in lines:
        pass # print(f"{res1=}, {res2=}, {line=}")
        

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
