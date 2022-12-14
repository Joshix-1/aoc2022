#!/usr/bin/env python3
import sys


def parse_tiles(line: str) -> set[tuple[int, int]]:
    corners: list[tuple[int, int]] = []
    for pair in line.split("->"):
        x, y = list(map(int, pair.strip().split(",")))
        corners.append((x, y))
    tiles = {corners[0]}
    if len(corners) <= 1:
        return tiles
    for i in range(1, len(corners)):
        corner = corners[i]
        tiles.add(corner)
        prev = corners[i - 1]
        dist_x = corner[0] - prev[0]
        dist_y = corner[1] - prev[1]
        distance = max(abs(dist_x), abs(dist_y))
        for j in range(1, distance):
            x = j * dist_x // distance
            y = j * dist_y // distance
            tiles.add((prev[0] + x, prev[1] + y))
    return tiles


def solve(input_: str) -> "tuple[int | str, int | str]":
    lines: list[str] = list(filter(None, input_.split("\n")))

    tiles: set[tuple[int, int]] = set()
    for line in lines:
        tiles |= parse_tiles(line)

    res1 = 0
    bottom_most = max(xy[1] for xy in tiles)
    sand_tiles = 0
    sand_origin = 500, 0
    while True:
        sand_pos = sand_origin
        while True:
            if sand_pos[1] == bottom_most + 1:
                if not res1:
                    res1 = sand_tiles
                sand_tiles += 1
                tiles.add(sand_pos)
                break
            elif (sand_pos[0], sand_pos[1] + 1) not in tiles:  # down
                sand_pos = (sand_pos[0], sand_pos[1] + 1)
            elif (sand_pos[0] - 1, sand_pos[1] + 1) not in tiles:  # left
                sand_pos = (sand_pos[0] - 1, sand_pos[1] + 1)
            elif (sand_pos[0] + 1, sand_pos[1] + 1) not in tiles:  # right
                sand_pos = (sand_pos[0] + 1, sand_pos[1] + 1)
            else:  # rests
                sand_tiles += 1
                tiles.add(sand_pos)
                if sand_pos == sand_origin:
                    return res1, sand_tiles
                break


def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        res1, res2 = solve(sys.stdin.read())
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")


if __name__ == "__main__":
    sys.exit(main())
