#!/usr/bin/env pypy3
import re
import sys


class Monkey:

    def __init__(self, line: str, monkeys: "dict[str, Monkey]") -> None:
        self.monkeys = monkeys
        self.name, self.calculation = line.split(": ")
        if re.fullmatch(r"[0-9]+", self.calculation):
            self._number = int(self.calculation)
            self.var_names = ()
            return
        match = re.match(r"([^ ]+) ([^ ]) ([^ ]+)", self.calculation)
        self.var_names = (match.group(1), match.group(3))
        self.op = match.group(2)

    @property
    def vars(self):
        return {
            name: self.monkeys[name].number
            for name in self.var_names
        }

    @property
    def direct_monkey_deps(self) -> "list[Monkey]":
        return [self.monkeys[name] for name in self.var_names]

    @property
    def all_deps(self):
        if not hasattr(self, "_all_deps"):
            deps = [*self.var_names]
            for name in self.var_names:
                deps.extend(self.monkeys[name].all_deps)
            self._all_deps = tuple(deps)

        return self._all_deps

    @property
    def number(self) -> int:
        if hasattr(self, "_number"):
            return self._number
        number = eval(self.calculation, self.vars)
        if "humn" not in self.all_deps:
            self._number = number
        return number

    def __str__(self):
        return self.name + ": " + self.calculation


def solve(input_: str) -> "tuple[int | str, int | str]":
    lines: list[str] = list(filter(None, input_.split("\n")))
    monkeys: "dict[str, Monkey]" = {}
    root = None
    humn = None
    for line in lines:
        monkey = Monkey(line, monkeys)
        monkeys[monkey.name] = monkey
        if monkey.name == "root":
            root = monkey
        elif monkey.name == "humn":
            humn = monkey
    res1 = root.number

    root.calculation = " == ".join(root.var_names)
    target_num = None
    monkey = None
    for m in root.direct_monkey_deps:
        if "humn" in m.all_deps:
            assert monkey is None
            monkey = m
        else:
            assert target_num is None
            target_num = m.number
    while monkey.number != target_num:
        magnitude = abs(monkey.number - target_num) // 10 + 1
        if monkey.number < target_num:
            humn._number = int(humn._number - magnitude)
        else:
            humn._number = int(humn._number + magnitude)
    return res1, humn.number


def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        res1, res2 = solve(sys.stdin.read())
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")


if __name__ == "__main__":
    sys.exit(main())
