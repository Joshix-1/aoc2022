#!/usr/bin/env pypy3
import re
import sys
from typing import Iterable
from itertools import chain


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

    def covered_x(self, y: int) -> "tuple[int, int] | None":
        distance_y = abs(y - self.sensor[1])
        if distance_y > self.distance:
            return None
        max_dist_x = self.distance - distance_y
        # assert max_dist_x >= 0
        x = self.sensor[0]
        return x - max_dist_x, x + max_dist_x

    def covered_x_range(self, y: int, start: int, end: int) -> "tuple[int, int] | None":
        pos = self.covered_x(y)
        if not pos:
            return None
        return max(pos[0], start), min(pos[1], end)

    def is_in_range(self, pos: tuple[int, int]) -> bool:
        return manhattan_dist(self.sensor, pos) <= self.distance

    def just_out_of_range(self, min_: int, max_: int) -> "Iterable[tuple[int, int]]":
        dist = self.distance + 1
        x, y = self.sensor
        for diff_x in range(-dist, dist + 1):
            _x = x + diff_x
            _y = y + dist - diff_x
            if min_ <= _x <= max_ and min_ <= _y <= max_:
                yield _x, _y
            if dist - diff_x:
                _y = (y - dist - diff_x)
                if min_ <= _x <= max_ and min_ <= _y <= max_:
                    yield _x, _y
        return


def start_end_to_iter(start_end: "None | tuple[int, int]") -> "Iterable[int]":
    if not start_end:
        return ()
    return range(start_end[0], start_end[1] + 1)


def solve(input_: str) -> "tuple[int | str, int | str]":
    sensors = [
        Sensor(line) for line in input_.strip().split("\n")
    ]
    y = 10 if "test" in sys.argv else 200_0000

    covered_pos: "set[int]" = set(
        chain.from_iterable(
            start_end_to_iter(sensor.covered_x(y))
            for sensor in sensors
        )
    )

    for sensor in sensors:
        if sensor.beacon[1] == y and sensor.beacon[0] in covered_pos:
            covered_pos.remove(sensor.beacon[0])

    print("first done")

    max_pos = 20 if "test" in sys.argv else 4_000_000

    for xy in chain.from_iterable(
        sensor.just_out_of_range(0, max_pos)
        for sensor in sensors
    ):
        for sensor in sensors:
            if sensor.is_in_range(xy):
                break
        else:
            return len(covered_pos), xy[0] * 4000000 + xy[1]

    return len(covered_pos), -1

def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        res1, res2 = solve(sys.stdin.read())
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")


if __name__ == "__main__":
    sys.exit(main())
