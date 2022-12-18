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
    _free_surfaces: tuple[tuple[int, int, int], ...]

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

    def free_surfaces(
        self,
        cubes: "set[tuple[int, int, int]]",
    ) -> tuple[tuple[int, int, int], ...]:
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
                pos_tuple = cast(tuple[int, int, int], tuple(pos))
                if pos_tuple not in cubes:
                    free_surfaces.append(pos_tuple)
            self._free_surfaces = tuple(free_surfaces)

        return self._free_surfaces

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
    free: list[tuple[int, int, int]] = []
    for cube in cubes:
        free_s = cube.free_surfaces(cube_pos)
        res1 += len(free_s)
        free.extend(free_s)
    res2 = res1
    for pos in set(free):
        cub_sides = free.count(pos)
        if cub_sides == 6:
            res2 -= 6
            continue
        free_sides = Cube(pos).free_surfaces(cube_pos)
        if cub_sides == 5 and len(free_sides) == 1:
            if 5 == free.count(free_sides[0]):
                res2 -= 10
                continue


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
