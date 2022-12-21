#!/usr/bin/env pypy3
import re
import sys


class Monkey:

    def __init__(self, line: str, monkeys: "dict[str, Monkey]") -> None:
        self.monkeys = monkeys
        self.name, self.calculation = line.split(": ")
        if re.fullmatch(r"[0-9]+", self.calculation):
            self._number = int(self.calculation)
            self.vars = []
            return
        match = re.match(r"([^ ]+) ([^ ]) ([^ ]+)", self.calculation)
        self.vars = [match.group(1), match.group(3)]
        self.op = match.group(2)

    @property
    def number(self) -> int:
        if not hasattr(self, "_number"):
            self._number = eval(
                self.calculation,
                {
                    name: self.monkeys[name].number
                    for name in self.vars
                }
            )
        return self._number

    def __str__(self):
        return self.name + ": " + self.calculation


def solve(input_: str) -> "tuple[int | str, int | str]":
    lines: list[str] = list(filter(None, input_.split("\n")))
    monkeys: "dict[str, Monkey]" = {}
    root = None
    for line in lines:
        monkey = Monkey(line, monkeys)
        monkeys[monkey.name] = monkey
        if monkey.name == "root":
            root = monkey

    return root.number, -1


def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        res1, res2 = solve(sys.stdin.read())
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")


if __name__ == "__main__":
    sys.exit(main())
