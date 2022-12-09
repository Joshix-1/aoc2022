#!/usr/bin/env python3
import sys
from dataclasses import dataclass

@dataclass
class Position:
    x: int
    y: int

    visited_pos: set[tuple[int, int]]

    def move(self, dir_: str, dist: int) -> int:
        assert dist == 1
        if dir_ == "U":
            self.y += (dist)
        elif dir_ == "D":
            self.y -= (dist)
        elif dir_ == "R":
            self.x += (dist)
        elif dir_ == "L":
            self.x -= (dist)
        else:
            assert False
        self.visited_pos.add((self.x, self.y))

    def move_to(self, head: "Position") -> None:
        if abs(self.x - head.x) <= 1 and abs(self.y - head.y) <= 1:
            return
        diff_x = head.x - self.x
        diff_y = head.y - self.y
        assert min(abs(diff_x), abs(diff_y)) <= 1
        if abs(diff_x) == 2:
            self.x += diff_x // 2
            if abs(diff_y) == 1:
                self.y += diff_y
            else:
                assert not diff_y
        elif abs(diff_y) == 2:
            self.y += diff_y // 2
            if abs(diff_x) == 1:
                self.x += diff_x
            else:
                assert not diff_x
        else:
            assert False
        assert abs(self.x - head.x) + abs(self.y - head.y) <= 1
        self.visited_pos.add((self.x, self.y))

    def __str__(self):
        return f"{self.x}, {self.y}"

def solve(input_: str) -> tuple[int | str, int | str]:
    lines: list[str] = list(filter(None, input_.split("\n")))

    res1, res2 = 0, 0

    head = Position(0, 0, set())
    tail = Position(0, 0, set())

    for line in lines:
        dir, num = line[0], int(line[2])
        for i in range(num):
            head.move(dir, 1)
            tail.move_to(head)
        print(f"{dir, num}, {head=!s}, {tail=!s}")


    return len(tail.visited_pos), res2

def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        res1, res2 = solve(sys.stdin.read())
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")

if __name__ == "__main__":
    sys.exit(main())
