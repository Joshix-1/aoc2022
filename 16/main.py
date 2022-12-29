#!/usr/bin/env pypy3
import random
import re
import sys
from itertools import count

names = {}


class Valve:
    name: str
    flow_rate: int
    _next_valves: "list[str]"
    valves: "dict[str, Valve]"
    score_cache: "dict"
    opened: bool
    _next_valve_with_dist: "tuple[tuple[int, Valve], ...]"

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
        self.score_cache = {}
        self.opened = False
        del match
        del line

    def __repr__(self) -> str:
        return f"Valve({self.name!r}, {self.flow_rate!r}, {self._next_valves!r})"

    @property
    def next_valves(self) -> "list[Valve]":
        return [self.valves[v] for v in self._next_valves]

    def next_valve_with_dist(self) -> "tuple[tuple[int, Valve], ...]":
        if not hasattr(self, "_next_valve_with_dist"):
            next_valves = self.next_valves
            next_valve_with_dist: "list[tuple[int, Valve]]" = []
            checked_valves: set[str] = {self.name}
            for dist in count(1, 1):
                valves = list(next_valves)
                next_valves = []
                for valve in valves:
                    if valve.name in checked_valves:
                        continue
                    checked_valves.add(valve.name)
                    next_valves.extend(
                        v for v in valve.next_valves if v.name not in checked_valves
                    )
                    if valve.flow_rate:
                        # assert valve.name not in tuple(vv.name for _, vv in next_valve_with_dist)
                        next_valve_with_dist.append((dist, valve))
                if not next_valves:
                    break
            self._next_valve_with_dist = tuple(next_valve_with_dist)

        return self._next_valve_with_dist

    def get_best_next(self, minutes_left: int, exclude_names: set[str]) -> "None | tuple[int, Valve]":
        next_valve_with_dist = [
            (valve.flow_rate * (minutes_left - dist - 1), dist, valve)
            for dist, valve in self.next_valve_with_dist()
            if dist < minutes_left and valve.name not in exclude_names
        ]
        if not next_valve_with_dist:
            return None
        next_valve_with_dist.sort(key=lambda x: x[0])
        return next_valve_with_dist.pop()[1:]

    def get_best_score(self, time: int, already_opened: "tuple[str, ...]") -> int:
        if time <= 1:
            # print(self.name, already_opened)
            return 0
        if not self.flow_rate and len(self._next_valves) == 1 and time < 30:
            return 0
        key = hash((time, already_opened))
        if key in self.score_cache:
            return self.score_cache[key]
        score = 0
        for open_ in range(1 if not self.flow_rate or self.name in already_opened else 2):
            _ao = (*already_opened, self.name) if open_ else already_opened
            t = time - 1 if open_ else time
            s = t * self.flow_rate if open_ else 0
            if not t:
                if time == 30:
                    print(s)
                if s > score:
                    score = s
                continue
            s += max(
                valve.get_best_score(t - 1, _ao)
                for valve in self.next_valves
            )
            if time == 30:
                print(s)
            if s > score:
                score = s
        self.score_cache[key] = score
        del already_opened, key
        return score


def solve(input_: str) -> int:
    lines: list[str] = list(filter(None, input_.split("\n")))
    valves: dict[str, Valve] = {}
    for line in lines:
        valve = Valve(line, valves)
        valves[valve.name] = valve
    current_valve = valves["AA"]
    return current_valve.get_best_score(30, ())


def solve2(input_: str) -> int:
    lines: list[str] = list(filter(None, input_.split("\n")))
    valves: dict[str, Valve] = {}
    for line in lines:
        valve = Valve(line, valves)
        valves[valve.name] = valve
    # print("\n".join(map(repr, valves["AA"].next_valve_with_dist())))
    opened: set[str] = set()
    valves = {"el": valves["AA"], "my": valves["AA"]}
    minutes = {"el": 26, "my": 26}
    score = 0
    while minutes["el"] > 0 and minutes["my"] > 0:
        if minutes["el"] == minutes["my"]:
            curr = random.choice(("my", "el"))
        else:
            curr = "my" if minutes["el"] < minutes["my"] else "el"
        valve = valves[curr]
        res = valve.get_best_next(minutes[curr], opened)
        if res is None:
            minutes[curr] = 0
            continue
        time, valves[curr] = res
        minutes[curr] -= time + 1
        opened.add(valves[curr].name)
        score += valves[curr].flow_rate * minutes[curr]
        print(curr, 26 - minutes[curr], valves[curr], opened)

    return score


def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        text = sys.stdin.read()
        res1 = -1  # solve(text)
        res2 = solve2(text)
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")


if __name__ == "__main__":
    sys.exit(main())
