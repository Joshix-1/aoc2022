#!/usr/bin/env python3
import sys

sys.set_int_max_str_digits(99999999)
class Monkey:
    def __init__(self, spec: str) -> None:
        lines = list(filter(None, spec.split("\n")))
        self.index = int(lines[0].removeprefix("Monkey ").removesuffix(":"))
        self.items = [int(x.strip()) for x in lines[1].removeprefix("  Starting items:").split(",")]
        code = compile(
            lines[2].removeprefix("  Operation: new = "),
            "str",
            "eval")
        self.operation = lambda old: eval(code, dict(old=old))
        self.test = [int(line.strip().split(" ")[-1]) for line in lines[3:]]
        self.count = 0

    def __str__(self):
        return f"M{self.index} {self.items} {self.test} {self.count}"

def solve2(input_: str) -> tuple[int | str, int | str]:
    monkeys: list[Monkey] = list(map(Monkey, filter(None, input_.split("\n\n"))))

    for i, m in enumerate(monkeys):
        assert i == m.index

    mod = 1
    for m in monkeys:
        mod *= m.test[0]

    print(f"{mod=}")

    for round in range(10000):
        #print(f"{round=}")
        for m in monkeys:
            #print(f"{m=!s}")
            while m.items:
                m.count += 1
                m.items[0] = m.operation(m.items[0]) % mod
                # m.items[0] = m.items[0] // 3
                recip = m.test[2] if m.items[0] % m.test[0] else m.test[1]
                monkeys[recip].items.append(m.items.pop(0))

    for m in monkeys:
        print(str(m))

    activity = list(sorted([m.count for m in monkeys]))
    print(f"{activity=}")
    return 0, activity[-1] * activity[-2]

def solve1(input_: str) -> tuple[int | str, int | str]:
    monkeys: list[Monkey] = list(map(Monkey, filter(None, input_.split("\n\n"))))

    for i, m in enumerate(monkeys):
        assert i == m.index

    for round in range(20):
        for m in monkeys:
            #print(f"{m=!s}")
            while m.items:
                m.count += 1
                m.items[0] = m.operation(m.items[0])
                m.items[0] = m.items[0] // 3
                recip = m.test[2] if m.items[0] % m.test[0] else m.test[1]
                monkeys[recip].items.append(m.items.pop(0))

    for m in monkeys:
        print(str(m))

    activity = list(sorted([m.count for m in monkeys]))
    print(f"{activity=}")
    return activity[-1] * activity[-2], 0

def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        input_ = sys.stdin.read()
        res1, _ = solve1(input_)
        _, res2 = solve2(input_)
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")

if __name__ == "__main__":
    sys.exit(main())
