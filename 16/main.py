#!/usr/bin/env pypy3
import re
import sys

names = {}


class Valve:
    name: str
    flow_rate: int
    _next_valves: "list[str]"
    valves: "dict[str, Valve]"
    score_cache: "dict"
    opened: bool

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

    @property
    def next_valves(self) -> "list[Valve]":
        return [self.valves[v] for v in self._next_valves]

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
    el_valve = my_valve = valves["AA"]
    score = 0
    for minute in range(26):
        for el_new in el_valve.next_valves:
            ...
        for my_new in my_valve.next_valves:
            ...
    return score

def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        text = sys.stdin.read()
        res1 = solve(text)
        res2 = solve2(text)
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")


if __name__ == "__main__":
    sys.exit(main())
