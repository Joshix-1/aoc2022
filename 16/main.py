#!/usr/bin/env python3
import re
import sys

#sys.setrecursionlimit(2**10)

class Valve:
    name: str
    flow_rate: int
    _next_valves: "list[str]"
    valves: "dict[str, Valve]"
    score_cache: "dict"

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

    @property
    def next_valves(self) -> "list[Valve]":
        return [self.valves[v] for v in self._next_valves]

    def get_best_score(self, time: int, already_opened: "tuple[str, ...]") -> int:
        if time <= 1:
            return 0
        if not self.flow_rate and self.name not in already_opened:
            # doesn't make sense to open this
            already_opened = (*already_opened, self.name)
        already_opened = tuple(sorted(set(already_opened)))
        key = time, already_opened
        if key in self.score_cache:
            return self.score_cache[key]
        score = 0
        for open_ in range(1 if self.name in already_opened else 2):
            _ao = (*already_opened, self.name) if open_ else already_opened
            t = (time - 1) if open_ else time
            s = (t * self.flow_rate) if open_ else 0
            if not t:
                if s > score:
                    score = s
                continue
            s += max(
                valve.get_best_score(t - 1, _ao)
                for valve in self.next_valves
            )
            if s > score:
                score = s
        #print(self.name, time, score, self.flow_rate, s, already_opened)
        self.score_cache[key] = score
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
