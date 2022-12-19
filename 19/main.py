#!/usr/bin/env pypy3
import sys
import re

class Blueprint:

    def __init__(self, line: str):
        match = re.match(
            r"Blueprint ([0-9]+): Each ore robot costs ([0-9]+) ore. "
            r"Each clay robot costs ([0-9]+) ore. "
            r"Each obsidian robot costs ([0-9]+) ore and ([0-9]+) clay. "
            r"Each geode robot costs ([0-9]+) ore and ([0-9]+) obsidian.",
            line
        )
        self.id = int(match.group(1))
        self.ore_robot = {"ore": int(match.group(2))}
        self.clay_robot = {"ore": int(match.group(3))}
        self.obsidian_robot = {"ore": int(match.group(4)), "clay": int(match.group(5))}
        self.geode_robot = {"ore": int(match.group(6)), "obsidian": int(match.group(7))}
        self.cache = {}

    def __repr__(self):
        return repr({
            "id": self.id,
            "ore_robot": self.ore_robot,
            "clay_robot": self.clay_robot,
            "obsidian_robot": self.obsidian_robot,
            "geode_robot": self.geode_robot,
        })

    def count_geodes(self, time, ore_robots, clay_robots, obsidian_robots, geode_robots, ore, clay, obsidian) -> int:
        if time == 0:
            raise AssertionError()
        if time == 1:
            return geode_robots
        key = hash((time, ore_robots, clay_robots, obsidian_robots, geode_robots, ore, clay, obsidian))
        if key in self.cache:
            return self.cache[key]
        ore += ore_robots
        clay += clay_robots
        obsidian += obsidian_robots
        time -= 1
        poss_counts = []
        poss_counts.append(
            self.count_geodes(time, ore_robots, clay_robots, obsidian_robots, geode_robots, ore, clay, obsidian)
        )
        if time > 2 and self.ore_robot["ore"] <= ore - ore_robots:
            poss_counts.append(self.count_geodes(time, ore_robots + 1, clay_robots, obsidian_robots, geode_robots, ore - self.ore_robot["ore"], clay, obsidian))
        if time > 2 and self.clay_robot["ore"] <= ore - ore_robots:
            poss_counts.append(self.count_geodes(time, ore_robots, clay_robots + 1, obsidian_robots, geode_robots, ore - self.clay_robot["ore"], clay, obsidian))
        if time > 2 and self.obsidian_robot["ore"] <= ore - ore_robots and self.obsidian_robot["clay"] <= clay - clay_robots:
            poss_counts.append(self.count_geodes(time, ore_robots, clay_robots, obsidian_robots + 1, geode_robots, ore - self.obsidian_robot["ore"], clay - self.obsidian_robot["clay"], obsidian))
        if self.geode_robot["ore"] <= ore - ore_robots and self.geode_robot["obsidian"] <= obsidian - obsidian_robots:
            poss_counts.append(self.count_geodes(time, ore_robots, clay_robots, obsidian_robots, geode_robots + 1, ore - self.geode_robot["ore"], clay, obsidian - self.geode_robot["obsidian"]))
        res = max(poss_counts) + geode_robots
        self.cache[key] = res
        if time > 20:
            print(time, res, repr(self))
        return res


def solve(input_: str) -> "tuple[int | str, int | str]":
    lines: list[str] = list(filter(None, input_.split("\n")))
    blueprints = list(map(Blueprint, lines))

    res1, res2 = 0, 0

    for bp in blueprints:
        print(f"{res1}, {res2}, {bp}")
        res1 += bp.id * bp.count_geodes(24, 1, 0, 0, 0, 0, 0, 0)
        bp.cache.clear()
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
