#!/usr/bin/env pypy3
import random
import re
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from itertools import count
from typing import Literal

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

    def get_possible_next(self, minutes_left: int, exclude_names: Iterable[str]) -> "Iterable[tuple[int, Valve]]":
        return (
            (dist, valve)
            for dist, valve in self.next_valve_with_dist()
            if dist < minutes_left and valve.name not in exclude_names
        )

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


@dataclass
class TwoState:
    valves: dict[str, Valve]
    opened_names: frozenset[str]
    el_minutes_left: int
    my_minutes_left: int
    el_valve: Valve
    my_valve: Valve

    def create_copy_with(
        self, el_my: "Literal['my', 'el']", valve: Valve, minutes_left: int
    ) -> "TwoState":
        return TwoState(
            valves=self.valves,
            opened_names=self.opened_names | {valve.name},
            el_minutes_left=self.el_minutes_left if el_my == "my" else minutes_left,
            my_minutes_left=self.my_minutes_left if el_my == "el" else minutes_left,
            el_valve=self.el_valve if el_my == "my" else valve,
            my_valve=self.my_valve if el_my == "el" else valve,
        )

    def get_valve(self, el_my: "Literal['my', 'el']") -> Valve:
        return getattr(self, el_my + "_valve")

    def get_minutes_left(self, el_my: "Literal['my', 'el']") -> int:
        return getattr(self, el_my + "_minutes_left")

    def iter_next(self) -> "Iterable[tuple[int, TwoState]]":
        curr: Literal['my', 'el']
        if self.my_minutes_left <= 1 and self.el_minutes_left <= 1:
            return ()
        poss = ("el", "my")
        if self.my_minutes_left == self.el_minutes_left and self.el_valve == self.my_valve:
            poss = ("my",)
        for curr in poss:
            valve = self.get_valve(curr)
            minutes_left = self.get_minutes_left(curr)
            # assert (valve.flow_rate and valve.name in self.opened_names) or valve.name == "AA"
            for dist, next_valve in valve.get_possible_next(minutes_left, self.opened_names):
                new_minutes_left = minutes_left - dist - 1
                if not new_minutes_left:
                    continue
                assert new_minutes_left > 0
                yield next_valve.flow_rate * new_minutes_left, self.create_copy_with(
                    curr,
                    next_valve,
                    new_minutes_left,
                )
        return

    def get_max_score(self) -> int:
        return max(
            [
                score + ts.get_max_score()
                for score, ts in self.iter_next()
            ],
            default=0,
        )


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

    return TwoState(
        valves=valves,
        opened_names=frozenset(),
        el_minutes_left=26,
        my_minutes_left=26,
        el_valve=valves["AA"],
        my_valve=valves["AA"],
    ).get_max_score()


def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        text = sys.stdin.read()
        res1 = solve(text)
        print("finished part 1, please wait :(")
        res2 = solve2(text)  # bit slow :(
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")


if __name__ == "__main__":
    sys.exit(main())
