#!/usr/bin/env pypy3
import sys
from typing import Literal, cast
from enum import Enum


class Direction(Enum):
    NEG_Y = 0
    POS_Y = 1
    NEG_X = 2
    POS_X = 3
    NEG_Z = 4
    POS_Z = 5


class Cube:
    pos: tuple[int, int, int]
    touches_cache: "dict[tuple[int, int, int], Literal[False] | Direction]"
    _free_surfaces: tuple[Direction, ...]

    def __init__(self, pos: tuple[int, int, int]) -> None:
        self.pos = pos
        self.touches_cache = {}
        assert len(pos) == 3

    @property
    def x(self) -> int:
        return self.pos[0]

    @property
    def y(self) -> int:
        return self.pos[1]

    @property
    def z(self) -> int:
        return self.pos[2]

    def free_surfaces(self, cubes: "tuple[int, int, int]") -> int:
        if not hasattr(self, "_free_surfaces"):
            free_surfaces = []
            for dir_ in Direction:
                pos = list(self.pos)
                coord = "XYZ".index(dir_.name[-1])
                pos[coord] = pos[coord] + (
                    -1
                    if dir_.name[:3] == "NEG"
                    else 1
                )
                if tuple(pos) not in cubes:
                    free_surfaces.append(dir_)
            self._free_surfaces = tuple(free_surfaces)

        return len(self._free_surfaces)

    def touches(self, other: "Cube") -> "Literal[False] | Direction":
        if other.pos in self.touches_cache:
            return self.touches_cache[other.pos]
        dist_x = abs(other.x - self.x)
        dist_y = abs(other.y - self.y)
        dist_z = abs(other.z - self.z)
        if dist_x + dist_y + dist_z > 1:
            return False
        direction: "None | Direction" = None
        if dist_x == 1:
            if other.x > self.x:
                direction = Direction.POS_X
            elif other.x < self.x:
                direction = Direction.NEG_X
        if dist_y == 1:
            if other.y > self.y:
                return Direction.POS_Y
            elif other.y < self.y:
                direction = Direction.NEG_Y
        if dist_z == 1:
            if other.z > self.z:
                return Direction.POS_Z
            elif other.z < self.z:
                direction = Direction.NEG_Z
        if direction is None:
            raise AssertionError()
        self.touches_cache[other.pos] = direction
        return direction

    def __repr__(self) -> str:
        return f"Cube({self.pos!r})"

    def __str__(self) -> str:
        return str(self.pos)


def solve(input_: str) -> "tuple[int | str, int | str]":
    cubes: list[Cube] = [
        Cube(cast(tuple[int, int, int], tuple(map(int, line.split(",")))))
        for line in filter(None, input_.split("\n"))
    ]
    res1, res2 = 0, 0
    cube_pos: set[tuple[int, int, int]] = {c.pos for c in cubes}
    for cube in cubes:
        res1 += cube.free_surfaces(cube_pos)

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
