#!/usr/bin/env pypy3
import sys
from dataclasses import dataclass

class Shape:
    # data: "tuple[str, ...]"
    # height: int
    # width: int

    def __init__(self, data: "list[str]") -> None:
        self.data = tuple(data)
        self.height = len(self.data)
        self.width = len(self.data[0])


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
    def pieces(self) -> "tuple[tuple[int, int], ...]":
        if hasattr(self, "_pieces"):
            return self._pieces
        pieces: list[tuple[int, int]] = []
        for y in range(self.y, self.top_most_y + 1):
            for x in range(self.x, self.right_most_x + 1):
                if self.has_piece_at(x, y):
                    pieces.append((x, y))
        return tuple(pieces)

    def fix(self):
        self._pieces = self.pieces

    @property
    def top_most_y(self) -> int:
        return self.y + self.shape.height - 1

    @property
    def right_most_x(self) -> int:
        return self.x + self.shape.width - 1

    def move_x(self, dx: int, others: "list[Rock]", pieces: set[tuple[int, int]]) -> None:
        if dx > 0 and self.right_most_x + 1 == CAVE_WIDTH:
            return
        if dx < 0 and self.x == 0:
            return
        if not self.can_move(others, (dx, 0), pieces):
            return
        self.x += dx
        assert 0 <= self.x <= self.right_most_x

    def can_move_down(self, others: "list[Rock]", pieces: set[tuple[int, int]]) -> bool:
        if self.y == 0:
            return False
        return self.can_move(others, (0, -1), pieces)

    def can_move(self, others: "list[Rock]", delta: tuple[int, int], pieces: set[tuple[int, int]]) -> bool:
        if not others:
            return True
        self.x += delta[0]
        self.y += delta[1]
        can_move_down = True
        for xy in self.pieces:
            if xy in pieces:
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
        for op in other.pieces:
            if self.has_piece_at(*op):
                return True
        return False


def gcd(a: int, b: int) -> int:
    """greatest common divisor"""
    if b == 0:
        return a
    return gcd(b, a % b)


def lcm(x: int, y: int) -> int:
    """least common multiple"""
    return x * y // gcd(x, y)


def solve(jet_pattern: str) -> "tuple[int | str, int | str]":
    rocks: list[Rock] = []
    jet_idx = 0
    top_y = 0
    jet_pattern = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
    pieces: set[tuple[int, int]] = set()
    big_num = 1_000_000_000_000
    min_repetition_num = lcm(len(jet_pattern), len(SHAPES))
    top_y_list = []
    for s in range(big_num):
        if s == 2022:
            res1 = top_y
            print(2022, res1)
        shape = SHAPES[s % len(SHAPES)]
        x, y = 2, top_y + 3
        rock = Rock(shape=shape, x=x, y=y)

        while True:
            assert jet_pattern[jet_idx] in "<>" or print(jet_pattern[jet_idx])
            rock.move_x(-1 if jet_pattern[jet_idx] == "<" else 1, rocks, pieces)
            jet_idx = (jet_idx + 1) % len(jet_pattern)
            if rock.can_move_down(rocks, pieces):
                rock.y -= 1
            else:
                if rock.top_most_y >= top_y:
                    top_y = rock.top_most_y + 1
                #print(rock.x, rock.y, "s", rock.shape.width, rock.shape.height, rock.shape.data)
                rock.fix()
                pieces.update(rock.pieces)
                rocks.insert(0, rock)
                top_y_list.append(top_y)
                break
        if s > max(3000, 4 * min_repetition_num):
            diff1 = top_y_list[s] - top_y_list[s - min_repetition_num]
            diff2 = top_y_list[s - min_repetition_num] - top_y_list[s - 2 * min_repetition_num]
            diff3 = top_y_list[s - 3 * min_repetition_num] - top_y_list[s - 4 * min_repetition_num]
            if any((diff1 == diff2, diff3 == diff2, diff1 == diff3)):
                print(s, diff1, diff2, diff3)
            if diff1 == diff2 == diff3:
                count, rest = divmod(big_num - s, min_repetition_num)
                if rest:
                    continue
                res2 = top_y + count * (diff2 + 1)
                # + (top_y_list[s - min_repetition_num + rest] - top_y_list[s - min_repetition_num])
                return res1, res2

    #for y in reversed(range(top_y)):
    #    print("".join(("#" if any(rock.has_piece_at(x, y) for rock in rocks) else ".") for x in range(CAVE_WIDTH)))
    return res1, -1


def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        res1, res2 = solve(sys.stdin.read().strip())
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")


if __name__ == "__main__":
    sys.exit(main())
