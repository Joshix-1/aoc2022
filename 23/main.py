#!/usr/bin/env pypy3
import sys

def check_north(elves, x, y):
    # If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north one step.
    if (x, y - 1) not in elves and (x + 1, y - 1) not in elves and (x - 1, y - 1) not in elves:
        return x, y - 1

def check_south(elves, x, y):
    # If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south one step.
    if (x, y + 1) not in elves and (x + 1, y + 1) not in elves and (x - 1, y + 1) not in elves:
        return x, y + 1

def check_west(elves, x, y):
    # If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west one step.
    if (x - 1, y) not in elves and (x - 1, y + 1) not in elves and (x - 1, y - 1) not in elves:
        return x - 1, y

def check_east(elves, x, y):
    # If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east one step.
    if (x + 1, y) not in elves and (x + 1, y + 1) not in elves and (x + 1, y - 1) not in elves:
        return x + 1, y


def print_elves(elves):
    min_x = min(x for x, _ in elves)
    max_x = max(x for x, _ in elves)
    min_y = min(y for _, y in elves)
    max_y = max(y for _, y in elves)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print("#" if (x, y) in elves else ".", end="")
        print()


def solve(input_: str) -> "tuple[int | str, int | str]":
    lines: list[list[str]] = list(map(list, filter(None, input_.split("\n"))))
    elves: set[tuple[int, int]] = set()
    for y, line in enumerate(lines):
        for x, field in enumerate(line):
            if field == "#":
                elves.add((x, y))
    res2 = -1
    elves_count = len(elves)
    moves = [check_north, check_south, check_west, check_east]
    for _ in range(10):
        moves_proposed: dict[tuple[int, int], tuple[int, int]] = {}
        for x, y in elves:
            # If no other Elves are in one of those eight positions, the Elf does not do anything during this round.
            if all(bool(check(elves, x=x, y=y)) for check in moves):
                continue
            for check in moves:
                if pos := check(elves, x=x, y=y):
                    assert pos not in elves
                    moves_proposed[(x, y)] = pos
                    break
        moves.append(moves.pop(0))
        destinations = list(moves_proposed.values())
        if not moves_proposed:
            res2 = _ + 1
        for from_, to in moves_proposed.items():
            print(from_, to)
            if destinations.count(to) == 1:
                elves.add(to)
                elves.remove(from_)
        print("---- " + str(_))
        print_elves(elves)
        assert elves_count == len(elves)
    min_x = min([x for x, _ in elves])
    max_x = max([x for x, _ in elves])
    min_y = min([y for _, y in elves])
    max_y = max([y for _, y in elves])
    print(min_x, max_x, min_y, max_y)
    print("rect", (max_x - min_x + 1) * (max_y - min_y + 1))
    print("elves", len(elves))
    empty_ground_tiles = (max_x - min_x + 1) * (max_y - min_y + 1) - len(elves)

    return empty_ground_tiles, res2


def main() -> None:
    stdout, sys.stdout = sys.stdout, sys.stderr
    try:
        res1, res2 = solve(sys.stdin.read())
    finally:
        sys.stdout = stdout
    print(f"1: {res1}\n2: {res2}")


if __name__ == "__main__":
    sys.exit(main())
