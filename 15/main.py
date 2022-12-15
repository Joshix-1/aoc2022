#!/usr/bin/env python3
import re
import sys


def manhattan_dist(a: "tuple[int, int]", b: "tuple[int, int]") -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class Sensor:
    sensor: "tuple[int, int]"
    beacon: "tuple[int, int]"
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

    def covered_pos(self, y: int) -> "set[tuple[int, int]]":
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
        x = self.sensor[0] - 1
        while True:
            pos = (x, y)
            distance = manhattan_dist(pos, self.sensor)
            if distance <= self.distance:
                covered.add(pos)
                x -= 1
            else:
                break

        return covered

    def covered_pos_range(self, y: int, start: int, end: int) -> "set[tuple[int, int]]":
        covered = set()
        x = self.sensor[0]
        while x <= end:
            pos = (x, y)
            distance = manhattan_dist(pos, self.sensor)
            if distance <= self.distance:
                covered.add(pos)
                x += 1
            else:
                break
        x = self.sensor[0] - 1
        while start <= x:
            pos = (x, y)
            distance = manhattan_dist(pos, self.sensor)
            if distance <= self.distance:
                covered.add(pos)
                x -= 1
            else:
                break

        return covered

def pos_in_range(pos: "tuple[int, int]", start, end) -> bool:
    return start <= pos[0] <= end and start <= pos[1] <= end

def solve(input_: str) -> "tuple[int | str, int | str]":
    lines: list[str] = list(filter(None, input_.split("\n")))

    res2 = []

    sensors = [
        Sensor(line)
        for line in lines
    ]
    covered_pos: "set[tuple[int, int]]" = set()
    y = 10 if "test" in sys.argv else 200_0000
    for sensor in sensors:
        print(f"{sensor!s}")
        covered_pos |= sensor.covered_pos(y)
    max_pos = 20 if "test" in sys.argv else 4_000_000
    for y in range(0, max_pos + 1):
        if not y % 100_000:
            print(y)
        covered = set()
        for sensor in sensors:
            covered |= sensor.covered_pos_range(y, 0, max_pos)
        if len(covered) != max_pos + 1:
            print(f"{y}, {len(covered)}")
            break
    for x in range(max_pos + 1):
        if (x, y) not in covered:
            res2.append((x, y))
            break
    for sensor in sensors:
        if sensor.beacon in covered_pos:
            covered_pos.remove(sensor.beacon)

    print(f"{res2}")
    return len(covered_pos), res2[0][0] * 4000000 + res2[0][1]


def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        res1, res2 = solve(sys.stdin.read())
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")


if __name__ == "__main__":
    sys.exit(main())
