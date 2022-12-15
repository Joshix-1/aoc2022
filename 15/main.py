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

    def is_in_range(self, x, y) -> bool:
        return manhattan_dist(self.sensor, (x, y)) <= self.distance

    def just_out_of_range(self, min_: int, max_: int) -> "set[tuple[int, int]]":
        dist = self.distance + 1
        x, y = self.sensor
        positions = set()
        for diff_x in range(-dist, dist + 1):
            _x, _y = x + diff_x, y + dist - diff_x
            if min_ <= _x <= max_ and min_ <= _y <= max_:
                positions.add((_x, _y))
        return positions

def start_end_to_set(start_end: "None | tuple[int, int]") -> "set[int]":
    if not start_end:
        return set()
    return set(range(start_end[0], start_end[1] + 1))

#def pos_in_range(pos: "tuple[int, int]", start, end) -> bool:
#    return start <= pos[0] <= end and start <= pos[1] <= end

def solve(input_: str) -> "tuple[int | str, int | str]":
    lines: list[str] = list(filter(None, input_.split("\n")))

    res2 = []

    sensors = [
        Sensor(line)
        for line in lines
    ]
    covered_pos: "set[int]" = set()
    y = 10 if "test" in sys.argv else 200_0000
    for sensor in sensors:
        print(f"{sensor!s}: {sensor.covered_x(y)}")
        covered_pos |= start_end_to_set(sensor.covered_x(y))

    for sensor in sensors:
        if sensor.beacon[1] == y and sensor.beacon[0] in covered_pos:
            covered_pos.remove(sensor.beacon[0])

    print("1:", len(covered_pos))
    max_pos = 20 if "test" in sys.argv else 4_000_000
    try:
        just_out_of_range = set()
        for sensor in sensors:
            just_out_of_range |= sensor.just_out_of_range(0, max_pos)
        print("len just_out_of_range", len(just_out_of_range))
        for x, y in just_out_of_range:
            in_range = False
            for sensor in sensors:
                if sensor.is_in_range(x, y):
                    in_range = True
                    break
            if not in_range:
                res2.append((x, y))
    except:
        print("y=",y)
        raise

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
