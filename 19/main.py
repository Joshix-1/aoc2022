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
        self.clay_robot = {"clay": int(match.group(3))}
        self.obsidian_robot = {"ore": int(match.group(4)), "clay": int(match.group(5))}
        self.geode_robot = {"ore": int(match.group(6)), "obsidian": int(match.group(7))}

    def __repr__(self):
        return repr({
            "id": self.id,
            "ore_robot": self.ore_robot,
            "clay_robot": self.clay_robot,
            "obsidian_robot": self.obsidian_robot,
            "geode_robot": self.geode_robot,
        })

def solve(input_: str) -> "tuple[int | str, int | str]":
    lines: list[str] = list(filter(None, input_.split("\n")))
    blueprints = list(map(Blueprint, lines))

    res1, res2 = 0, 0

    for bp in blueprints:
        print(f"{res1=}, {res2=}, {bp=}")

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
