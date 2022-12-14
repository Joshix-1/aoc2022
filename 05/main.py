#!/usr/bin/env python3
import sys

def solve(input_: str) -> tuple[str, str]:
    initial, moves = list(filter(None, input_.split("\n\n")))

    crate_lines = list(filter(None, initial.split("\n")))
    crates: dict[int, list[str]] = {}
    for i, char in enumerate(crate_lines[-1]):
        if char == " ":
            continue
        idx = int(char)
        crates.setdefault(idx, [])
        for line in crate_lines[:-1][::-1]:
            if line[i] == " ":
                continue
            crates[idx].append(line[i])
    crates2 = {key: list(value) for key, value in crates.items()}
    print(crates)
    lines = list(filter(None, moves.split("\n")))

    for line in lines:
        _, count, _, from_, _, to_ = line.split(" ")
        count, from_, to_ = int(count), int(from_), int(to_)
        crates2[to_].extend(crates2[from_][-count:])
        for _ in range(count):
            crates2[from_].pop()
            crates[to_].append(crates[from_].pop())

    res1 = "".join(stack[-1] for stack in crates.values())
    res2 = "".join(stack[-1] for stack in crates2.values())
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
