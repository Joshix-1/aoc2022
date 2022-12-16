#!/usr/bin/env python3
import re
import sys


sys.setrecursionlimit(2**10)

class Valve:
    name: str
    flow_rate: int
    _next_valves: list[str]
    valves: "dict[str, Valve]"

    def __init__(self, line: str, valves: "dict[str, Valve]") -> None:
        match = re.match(
            r"Valve ([A-Z][A-Z]) has flow rate=([0-9]+); tunnels? leads? to valves? (.+)",
            line
        )
        if match is None:
            print(line)
        self.name = match.group(1)
        self.flow_rate = int(match.group(2))
        self._next_valves = [valve.strip() for valve in match.group(3).split(",")]
        self.valves = valves

    @property
    def next_valves(self) -> "list[Valve]":
        return [self.valves[v] for v in self._next_valves]

    def get_best_score(self, time: int, already_visited: tuple[str, ...]) -> int:
        if not time:
            return self.flow_rate * time
        already_visited = (*already_visited, self.name)
        score = self.flow_rate * time
        score = max(
            (score if t == time - 1 else 0) + max(
                (valve.get_best_score(t - 1, already_visited)
                 for valve in self.next_valves
                 if valve.name not in already_visited),
                default=0
            )
            for t in (time, time - 1)
        )
        return score


def solve(input_: str) -> "tuple[int | str, int | str]":
    lines: list[str] = list(filter(None, input_.split("\n")))
    valves: dict[str, Valve] = {}
    for line in lines:
        valve = Valve(line, valves)
        valves[valve.name] = valve

    res2 = 0
    current_valve = valves["AA"]
    res1 = current_valve.get_best_score(30, ())

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
