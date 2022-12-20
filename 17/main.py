#!/usr/bin/env pypy3
import sys
from dataclasses import dataclass

class Shape:

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
        pieces: list[tuple[int, int]] = []
        for y in range(self.y, self.top_most_y + 1):
            for x in range(self.x, self.right_most_x + 1):
                if self.has_piece_at(x, y):
                    pieces.append((x, y))
        return tuple(pieces)

    @property
    def top_most_y(self) -> int:
        return self.y + self.shape.height - 1

    @property
    def right_most_x(self) -> int:
        return self.x + self.shape.width - 1

    def move_x(self, dx: int, pieces: set[tuple[int, int]]) -> None:
        if dx > 0 and self.right_most_x + 1 == CAVE_WIDTH:
            return
        if dx < 0 and self.x == 0:
            return
        if not self.can_move((dx, 0), pieces):
            return
        self.x += dx
        assert 0 <= self.x <= self.right_most_x

    def can_move_down(self, pieces: set[tuple[int, int]]) -> bool:
        if self.y == 0:
            return False
        return self.can_move((0, -1), pieces)

    def can_move(self, delta: tuple[int, int], pieces: set[tuple[int, int]]) -> bool:
        if not pieces:
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


def solve(jet_pattern: str) -> "tuple[int, int]":
    jet_idx = 0
    top_y = 0
    pieces: set[tuple[int, int]] = set()
    # jet_pattern = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>" * 11
    top_y_values = []
    count = lcm(len(SHAPES), len(jet_pattern))
    for s in range(count * 6 + (1000000000000 % count) + 1):  # 0_000_000
        shape = SHAPES[s % len(SHAPES)]
        x, y = 2, top_y + 3
        rock = Rock(shape=shape, x=x, y=y)

        while True:
            assert jet_pattern[jet_idx] in "<>" or print(jet_pattern[jet_idx])
            rock.move_x(-1 if jet_pattern[jet_idx] == "<" else 1, pieces)
            jet_idx = (jet_idx + 1) % len(jet_pattern)
            if rock.can_move_down(pieces):
                rock.y -= 1
            else:
                if rock.top_most_y >= top_y:
                    top_y = rock.top_most_y + 1
                pieces.update(rock.pieces)
                break

        top_y_values.append(top_y)

    seq = [
        v - top_y_values[i - 1]
        for i, v in enumerate(top_y_values[1:], 1)
    ]
    seq_str = "".join(map(str, seq))
    sub_seq = []
    for _ in range(5, len(seq) // 2):
        sub_str = seq_str[-_:]
        div, mod = divmod(len(seq_str), len(sub_str))
        if seq_str[mod:].count(sub_str) == div:
            sub_seq = list(map(int, sub_str))
            break
    div, mod = divmod((1000000000000 - s - 1), len(sub_seq))
    res2 = top_y + sum(sub_seq) * div + sum(sub_seq[:mod])
    return top_y_values[2021], res2


def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        res1, res2 = solve(sys.stdin.read().strip())
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")


if __name__ == "__main__":
    sys.exit(main())
