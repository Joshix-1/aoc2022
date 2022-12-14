#!/usr/bin/env python3
import sys


class Wall:
    tiles: set[tuple[int, int]]
    def __init__(self, line: str) -> None:
        corners: list[tuple[int, int]] = []
        for pair in line.split("->"):
            x, y = list(map(int, pair.strip().split(",")))
            corners.append((x, y))
        self.tiles = {corners[0]}
        if len(corners) <= 1:
            return
        for i in range(1, len(corners)):
            corner = corners[i]
            self.tiles.add(corner)
            prev = corners[i - 1]
            assert (corner[0] == prev[0]) + (corner[1] == prev[1]) == 1
            dist_x = corner[0]  - prev[0]
            dist_y = corner[1] - prev[1]
            distance = max(abs(dist_x), abs(dist_y))
            for i in range(1, distance):
                x = i * dist_x // distance
                y = i * dist_y // distance
                self.tiles.add((prev[0] + x, prev[1] + y))


def solve(input_: str) -> tuple[int | str, int | str]:
    lines: list[str] = list(filter(None, input_.split("\n")))

    tiles: set[tuple[int, int]] = set()
    for line in lines:
        tiles |= Wall(line).tiles
    tiles2 = set(tuple(tiles))

    bottom_most = max(xy[1] for xy in tiles)
    print(bottom_most, tiles)
    sand_tiles: set[tuple[int, int]] = set()
    sand_origin = 500, 0
    while True:
        sand_pos = sand_origin
        while sand_pos[1] < bottom_most + 1:
            if (sand_pos[0], sand_pos[1] + 1) not in tiles:  # down
                sand_pos = (sand_pos[0], sand_pos[1] + 1)
            elif (sand_pos[0] - 1, sand_pos[1] + 1) not in tiles:  # left
                sand_pos = (sand_pos[0] - 1, sand_pos[1] + 1)
            elif (sand_pos[0] + 1, sand_pos[1] + 1) not in tiles:  # right
                sand_pos = (sand_pos[0] + 1, sand_pos[1] + 1)
            else:  # rests
                sand_tiles.add(sand_pos)
                tiles.add(sand_pos)
                break
        else:
            break

    sand_tiles2: set[tuple[int, int]] = set()
    while True:
        sand_pos = sand_origin
        while True:
            if sand_pos[1] == bottom_most + 1:
                sand_tiles2.add(sand_pos)
                tiles2.add(sand_pos)
                if sand_pos == sand_origin:
                    return len(sand_tiles), len(sand_tiles2)
                break
            elif (sand_pos[0], sand_pos[1] + 1) not in tiles2:  # down
                sand_pos = (sand_pos[0], sand_pos[1] + 1)
            elif (sand_pos[0] - 1, sand_pos[1] + 1) not in tiles2:  # left
                sand_pos = (sand_pos[0] - 1, sand_pos[1] + 1)
            elif (sand_pos[0] + 1, sand_pos[1] + 1) not in tiles2:  # right
                sand_pos = (sand_pos[0] + 1, sand_pos[1] + 1)
            else:  # rests
                sand_tiles2.add(sand_pos)
                tiles2.add(sand_pos)
                if sand_pos == sand_origin:
                    return len(sand_tiles), len(sand_tiles2)
                break

    return len(sand_tiles), len(sand_tiles2)


def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        res1, res2 = solve(sys.stdin.read())
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")


if __name__ == "__main__":
    sys.exit(main())
