#!/usr/bin/env pypy3
import sys
from dataclasses import dataclass

class Shape:
    data: "tuple[str, ...]"

    def __init__(self, data: "list[str]") -> None:
        self.data = tuple(data)

    @property
    def height(self) -> int:
        return len(self.data)

    @property
    def width(self) -> int:
        return len(self.data[0])


SHAPES = [
    Shape(["####"]),
    Shape([".#.", "###", ".#."]),
    Shape(["###", "..#", "..#"]),
    Shape(["#", "#", "#", "#"]),
    Shape(["##", "##"]),
]
CAVE_WIDTH = 7


@dataclass
class Rock:
    shape: Shape
    x: int  # left
    y: int  # bottom

    @property
    def top_most_y(self) -> int:
        return self.y + self.shape.height - 1

    @property
    def right_most_x(self) -> int:
        return self.x + self.shape.width - 1

    def move_x(self, dx: int, others: "list[Rock]") -> None:
        if dx > 0 and self.right_most_x + 1 == CAVE_WIDTH:
            return
        if dx < 0 and self.x == 0:
            return
        if not self.can_move(others, (dx, 0)):
            return
        self.x += dx
        assert 0 <= self.x <= self.right_most_x

    def can_move_down(self, others: "list[Rock]") -> bool:
        if self.y == 0:
            return False
        return self.can_move(others, (0, -1))

    def can_move(self, others: "list[Rock]", delta: tuple[int, int]) -> bool:
        if not others:
            return True
        self.x += delta[0]
        self.y += delta[1]
        can_move_down = True
        for rock in reversed(others):
            assert self is not rock
            if self.collides(rock):
                can_move_down = False
                break
        self.x -= delta[0]
        self.y -= delta[1]
        return can_move_down

    def has_piece_at(self, px: int, py: int) -> bool:
        if px > self.right_most_x or py > self.top_most_y:
            return False
        if px < self.x or py < self.y:
            return False
        x, y = px - self.x, py - self.y
        assert x >= 0 and y >= 0
        if self.shape.data[y][x] == "#":
            return True
        assert self.shape.data[y][x] == "."
        return False

    def collides(self, other: "Rock") -> bool:
        if self.y > other.top_most_y:
            return False
        if other.y > self.top_most_y:
            return False
        for y in range(self.y, self.top_most_y + 1):
            for x in range(self.x, self.right_most_x + 1):
                if self.has_piece_at(x, y) and other.has_piece_at(x, y):
                    return True
        return False


def top(rocks: list[Rock]) -> int:
    return 1 + max(rock.top_most_y for rock in rocks)

def solve(jet_pattern: str) -> "tuple[int | str, int | str]":
    res2 = 0
    rocks: list[Rock] = []
    jet_idx = 0
    # jet_pattern = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
    for s in range(2022):
        shape = SHAPES[s % len(SHAPES)]
        x, y = 2, (top(rocks) + 3) if rocks else 3
        rock = Rock(shape=shape, x=x, y=y)

        # if s == 10:
        #     rocks.append(rock)
        #     break

        while True:
            assert jet_pattern[jet_idx] in "<>" or print(jet_pattern[jet_idx])
            rock.move_x(-1 if jet_pattern[jet_idx] == "<" else 1, rocks)
            jet_idx = (jet_idx + 1) % len(jet_pattern)
            if rock.can_move_down(rocks):
                rock.y -= 1
            else:
                print(rock.x, rock.y, "s", rock.shape.width, rock.shape.height, rock.shape.data)
                rocks.append(rock)
                break
    res1 = top(rocks)
    for y in reversed(range(res1)):
        print("".join(("#" if any(rock.has_piece_at(x, y) for rock in rocks) else ".") for x in range(CAVE_WIDTH)))
    return res1, res2


def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        res1, res2 = solve(sys.stdin.read().strip())
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")


if __name__ == "__main__":
    sys.exit(main())
