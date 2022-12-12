#!/usr/bin/env python3
import sys
from dataclasses import dataclass
from pathlib import Path
from string import ascii_lowercase

sys.setrecursionlimit(16385)

def get_next(i, x, y):
    if i == 0:
        return x + 1, y
    if i == 1:
        return x, y + 1
    if i == 2:
        return x - 1, y
    if i == 3:
        return x, y - 1
    assert False

@dataclass
class Cell:
    maze: "list[list[Cell]]"
    char: str
    x: int
    y: int
    dist: "None | int" = None
    _neighbors: "None | list[Cell]" = None
    _height: "None | int" = None

    @property
    def is_start(self) -> bool:
        return self.char == "S"

    @property
    def is_end(self) -> bool:
        return self.char == "E"

    @property
    def pos(self) -> tuple[int, int]:
        return self.x, self.y

    @property
    def height(self) -> int:
        if self._height is None:
            if self.is_end:
                char = "z"
            elif self.is_start:
                char = "a"
            elif self.char in ascii_lowercase:
                char = self.char
            else:
                raise ValueError(f"{self.char=}")
            self._height = ord(char) - ord("a")
        return self._height

    @property
    def neighbors(self) -> "list[Cell]":
        if not self._neighbors:
            def is_valid(x, y) -> "Literal[False] | Cell":
                if min(x, y) < 0:
                    return False
                if y >= len(self.maze) or x >= len(self.maze[0]):
                    return False
                cell_ = self.maze[y][x]
                if self.height - cell_.height > 1:
                    return False
                return cell_
            self._neighbors = [
                cell
                for i in range(4)
                if (cell := is_valid(*get_next(i, self.x, self.y)))
            ]
        return list(self._neighbors)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Cell):
            return False
        return self.pos == other.pos

    def __hash__(self) -> int:
        return hash(self.pos)

    def __repr__(self):
        return str(self)
    def __str__(self) -> int:
        return f"{self.char}({self.x}, {self.y})"


def solve(input_: str) -> "tuple[int | str, int | str]":
    lines: list[str] = list(filter(None, input_.split("\n")))
    maze: list[list[Cell]] = []
    for y, line in enumerate(lines):
        maze.append([Cell(maze, ch, x, y) for x, ch in enumerate(line)])

    start_cell = None
    end_cell = None
    cell_count = 0
    for line in maze:
        for cell in line:
            if cell.is_start:
                start_cell = cell
            elif cell.is_end:
                end_cell = cell
            cell_count += 1

    assert start_cell and end_cell

    stack: "list[tuple[int, Cell, Cell | None]]" = [(0, end_cell, None)]
    while stack:
        dist, cell, prev = stack.pop(0)
        print(dist, cell)
        if cell.dist is None:
            cell.dist = dist
        else:
            continue
        dist += 1
        stack.extend(
            [
                (dist, n, cell) for n in cell.neighbors
                if n.dist is None and n != prev
            ]
        )

    return start_cell.dist, 0

def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        res1, res2 = solve((Path(__file__).absolute().parent / "input").read_text())
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")


if __name__ == "__main__":
    sys.exit(main())
