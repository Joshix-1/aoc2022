#!/usr/bin/env pypy3
import sys
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

    def neighboring_voids(self, filter_: "Void | None" = None) -> tuple[tuple[int, int, int], ...]:
        if not hasattr(self, "_neighboring_voids"):
            self._neighboring_voids = tuple(
                neighbor
                for neighbor in self.neighbors
                if neighbor not in self.cube_pos
            )
        if filter_ is None:
            return self._neighboring_voids
        return tuple(
            void
            for void in self._neighboring_voids
            if filter_.pos != void
        )

    def neighboring_cubes(self) -> tuple[tuple[int, int, int], ...]:
        if not hasattr(self, "_neighboring_cubes"):
            self._neighboring_cubes = tuple(
                neighbor
                for neighbor in self.neighbors
                if neighbor in self.cube_pos
            )
        return self._neighboring_cubes

    def __repr__(self) -> str:
        return f"Cube({self.pos!r})"

    def __str__(self) -> str:
        return str(self.pos)

    def __hash__(self) -> int:
        return hash(self.pos)


class Void(Cube):
    def is_enclosed_by_cubes(self) -> "Literal[False] | list[Cube]":
        neighboring_voids = self.neighboring_voids()
        if not neighboring_voids:
            return [Cube(n, self.cube_pos) for n in self.neighboring_cubes()]

        if len(neighboring_voids) > 1:
            return False

        cubes = list(self.neighboring_cubes())
        prev = self
        current = Void(neighboring_voids[0], self.cube_pos)
        cubes.extend(current.neighboring_cubes())
        while len(current.neighboring_voids()) == 2:
            a, b = current.neighboring_voids()
            next_ = Void(b if a == prev else a, self.cube_pos)
            cubes.extend(next_.neighboring_cubes())

        return [
            Cube(n, self.cube_pos) for n in cubes
        ] if len(current.neighboring_voids()) == 0 else False


def solve(input_: str) -> "tuple[int | str, int | str]":
    cube_pos: dict[tuple[int, int, int], Cube] = {}
    for line in filter(None, input_.split("\n")):
        cube = Cube(cast(tuple[int, int, int], tuple(map(int, line.split(",")))), cube_pos)
        cube_pos[cube.pos] = cube
    cubes = list(cube_pos.values())
    res1, res2 = 0, 0
    free: list[tuple[int, int, int]] = []
    for cube in cubes:
        free_s = cube.neighboring_voids()
        res1 += len(free_s)
        free.extend(free_s)
    res2 = res1
    for pos in set(free):
        void = Void(pos, cube_pos)
        enclosed = void.is_enclosed_by_cubes()
        if enclosed:
            res2 -= len(enclosed)
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
