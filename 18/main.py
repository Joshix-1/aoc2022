#!/usr/bin/env pypy3
import sys
from collections import defaultdict
from typing import Iterable, Literal, cast
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
    _neighboring_voids: tuple[tuple[int, int, int], ...]
    _neighboring_cubes: tuple[tuple[int, int, int], ...]
    neighbors: tuple[tuple[int, int, int], ...]
    cube_pos: "dict[tuple[int, int, int], Cube]"

    def __init__(self, pos: tuple[int, int, int], cube_pos: "dict[tuple[int, int, int], Cube]") -> None:
        self.pos = pos
        self.touches_cache = {}
        self.cube_pos = cube_pos
        self.neighbors = tuple(self._neighbors())
        assert len(pos) == 3

    @property
    def is_cube(self) -> bool:
        return self.pos in self.cube_pos

    @property
    def x(self) -> int:
        return self.pos[0]

    @property
    def y(self) -> int:
        return self.pos[1]

    @property
    def z(self) -> int:
        return self.pos[2]

    def _neighbors(self) -> Iterable[tuple[int, int, int]]:
        for dir_ in Direction:
            pos = list(self.pos)
            coord = "XYZ".index(dir_.name[-1])
            pos[coord] = pos[coord] + (
                -1
                if dir_.name[:3] == "NEG"
                else 1
            )
            yield cast(tuple[int, int, int], tuple(pos))

    def neighboring_voids(self) -> tuple[tuple[int, int, int], ...]:
        if not hasattr(self, "_neighboring_voids"):
            self._neighboring_voids = tuple(
                neighbor
                for neighbor in self.neighbors
                if neighbor not in self.cube_pos
            )
        return self._neighboring_voids

    def __repr__(self) -> str:
        return f"Cube({self.pos!r})"

    def __str__(self) -> str:
        return str(self.pos)

    def __hash__(self) -> int:
        return hash(self.pos)


class Void(Cube):
    def neighboring_cubes(self) -> tuple[tuple[int, int, int], ...]:
        if not hasattr(self, "_neighboring_cubes"):
            self._neighboring_cubes = tuple(
                neighbor
                for neighbor in self.neighbors
                if neighbor in self.cube_pos
            )
        return self._neighboring_cubes


def solve(input_: str) -> "tuple[int | str, int | str]":
    cube_pos: dict[tuple[int, int, int], Cube] = {}
    for line in filter(None, input_.split("\n")):
        cube = Cube(cast(tuple[int, int, int], tuple(map(int, line.split(",")))), cube_pos)
        cube_pos[cube.pos] = cube
    cubes = list(cube_pos.values())
    res1, res2 = 0, 0
    for cube in cubes:
        free_s = cube.neighboring_voids()
        res1 += len(free_s)
    res2 = res1
    min_x = min(c.x for c in cubes) - 1
    min_y = min(c.y for c in cubes) - 1
    min_z = min(c.z for c in cubes) - 1
    max_x = max(c.x for c in cubes) + 1
    max_y = max(c.y for c in cubes) + 1
    max_z = max(c.z for c in cubes) + 1

    start = (min_x, min_y, min_z)  # 100% outside
    checked: set[tuple[int, int, int]] = set()
    free_to_check: list[tuple[int, int, int]] = [start]
    exposed_faces: dict[tuple[int, int, int], int] = defaultdict(int)
    while free_to_check:
        x, y, z = curr_pos = free_to_check.pop(0)
        if curr_pos in checked:
            continue
        checked.add(curr_pos)
        if x < min_x or y < min_y or z < min_z:
            continue
        if x > max_x or y > max_y or z > max_z:
            continue
        assert curr_pos not in cube_pos
        current = Void(curr_pos, cube_pos)
        for cube in current.neighboring_cubes():
            exposed_faces[cube] += 1
        free_to_check.extend(current.neighboring_voids())

    return res1, sum(exposed_faces.values())


def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        res1, res2 = solve(sys.stdin.read())
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")


if __name__ == "__main__":
    sys.exit(main())
