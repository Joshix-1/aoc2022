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
    _distance: "None | int" = None
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

    def distance(self, n_before: "Cell") -> int:
        if self._distance is not None:
            return self._distance
        if self.is_end:
            return 0
        else:
            if n_before.is_end and n_before in self.neighbors:
                self._distance = 1
                return 1
            neighbors = [n for n in self.neighbors if n != n_before]
            if neighbors:
                dist = (
                    0
                    if any(c.is_end for c in neighbors)
                    else min(c.distance(self) for c in neighbors)
                )
            else:
                assert self.neighbors == [n_before]
                self._distance = n_before.distance(self) + 1
                return self._distance
            if self.connection_is_bi(n_before):
                other_dist = n_before.distance(self)
                if dist < other_dist:
                    self._distance = dist
                    n_before._distance = dist + 1
                elif other_dist < dist:
                    self._distance = other_dist + 1
                    other_dist._distance = other_dist
                else:
                    self._distance = dist
            else:
                assert n_before not in self.neighbors
                self._distance = dist
            return dist

    def connection_is_bi(self, other: "Cell") -> bool:
        return other in self.neighbors and self in other.neighbors

    def __eq__(self, other):
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
    print(end_cell, end_cell.distance(None))
    dists = [
        (n, n.distance(end_cell))
        for n in end_cell.neighbors
    ]
    curr_cells: set[Cell] = {end_cell}
    visited: dict[tuple[int, int], int] = {}
    while len(visited) < cell_count and curr_cells:
        cell = curr_cells.pop()
        for n in cell.neighbors:
            if n.pos in visited:
                continue
            if cell in n.neighbors:
                visited[n.pos] = n.distance(cell)
                curr_cells.add(n)

    return start_cell._distance, 0

def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        res1, res2 = solve((Path(__file__).absolute().parent / "input").read_text())
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")


if __name__ == "__main__":
    sys.exit(main())
