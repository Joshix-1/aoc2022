#!/usr/bin/env python3
import re
import sys


def manhattan_dist(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class Sensor:
    sensor: tuple[int, int]
    beacon: tuple[int, int]
    distance: int

    def __init__(self, line: str) -> None:
        """Example: """
        match = re.match(
            r"Sensor at x=(-?[0-9]+), y=(-?[0-9]+): closest beacon is at x=(-?[0-9]+), y=(-?[0-9]+)",
            line,
        )
        self.sensor = (int(match.group(1)), int(match.group(2)))
        self.beacon = (int(match.group(3)), int(match.group(4)))
        self.distance = manhattan_dist(self.sensor, self.beacon)

    def __str__(self):
        return f"S{self.sensor}, dist={self.distance}"

    def covered_pos(self, y: int) -> set[tuple[int, int]]:
        covered = set()
        x = self.sensor[0]
        while True:
            pos = (x, y)
            distance = manhattan_dist(pos, self.sensor)
            if distance <= self.distance:
                covered.add(pos)
                x += 1
            else:
                break
        x = self.sensor[0]
        while True:
            pos = (x, y)
            distance = manhattan_dist(pos, self.sensor)
            if distance <= self.distance:
                covered.add(pos)
                x -= 1
            else:
                break

        return covered


def solve(input_: str) -> "tuple[int | str, int | str]":
    lines: list[str] = list(filter(None, input_.split("\n")))

    res1, res2 = 0, 0

    sensors = [
        Sensor(line)
        for line in lines
    ]
    covered_pos: set[tuple[int, int]] = set()
    y = 200_0000
    for sensor in sensors:
        print(f"{res1=}, {res2=}, {sensor=!s}")
        covered_pos |= sensor.covered_pos(y)

    for sensor in sensors:
        if sensor.beacon in covered_pos:
            covered_pos.remove(sensor.beacon)

    return len(covered_pos), res2


def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        res1, res2 = solve(sys.stdin.read())
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")


if __name__ == "__main__":
    sys.exit(main())
