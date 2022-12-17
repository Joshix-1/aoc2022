#!/usr/bin/env pypy3
import re
import sys
import gc

#sys.setrecursionlimit(2**10)

names = {}

def parse_name(name):
    if name in names:
        return names[name]
    assert len(name) == 2
    a = ord("A")
    n1, n2 = ord(name[0]) - a, ord(name[1]) - a
    names[name] = n1 * 100 + n2
    return names[name]

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
        self.name = parse_name(match.group(1))
        self.flow_rate = int(match.group(2))
        self._next_valves = [parse_name(valve.strip()) for valve in match.group(3).split(",")]
        self.valves = valves
        self.score_cache = {}
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
        #if not self.flow_rate and self.name not in already_opened:
        #    # doesn't make sense to open this
        #    already_opened = (*already_opened, self.name)
        # already_opened = tuple(sorted(set(already_opened)))
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
        # print(self.name, time, score, self.flow_rate, s, already_opened)
        self.score_cache[key] = score
        del already_opened, key
        # gc.collect_step() #gc.collect()
        return score


def solve(input_: str) -> "tuple[int | str, int | str]":
    lines: list[str] = list(filter(None, input_.split("\n")))
    valves: dict[str, Valve] = {}
    for line in lines:
        valve = Valve(line, valves)
        valves[valve.name] = valve
    res2 = 0
    current_valve = valves[parse_name("AA")]
    res1 = current_valve.get_best_score(30, ())
    del valves, current_valve
    print("- - - - -", res1)
    valves: dict[str, Valve] = {}
    for line in lines:
        valve = Valve(line, valves)
        valves[valve.name] = valve
    me = valves[parse_name("AA")]
    el = valves[parse_name("AA")]

    not_opened = {v.name for v in valves.values() if v.flow_rate}
    visited = set()
    print(not_opened)
    time = 26
    score = 0
    while time > 0 and not_opened:
        s = 0
        if me.name in not_opened:
            print("opening", me.name)
            s += (time - 1) * me.flow_rate
            not_opened.remove(me.name)
        else:
            print(me.name, "not in", not_opened)
            for v in me.next_valves:
                if me.name not in visited:
                    me = v
                    visited.add(v)
                    break

        if el.name in not_opened:
            print("opening", el.name)
            s += (time - 1) * el.flow_rate
            not_opened.remove(el.name)
        else:
            print(el.name, "not in", not_opened)
            for v in el.next_valves:
                if el.name not in visited:
                    el = v
                    visited.add(v)
                    break

        time -= 1
        score += s

    print(time, not_opened)

    return res1, score


def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        res1, res2 = solve(sys.stdin.read())
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")


if __name__ == "__main__":
    sys.exit(main())
