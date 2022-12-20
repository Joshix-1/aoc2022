#!/usr/bin/env pypy3
import sys


def solve(input_: str) -> "tuple[int | str, int | str]":
    nums: list[int] = list(map(int, filter(None, input_.split("\n"))))
    nums_with_idx = [(idx, num) for idx, num in enumerate(nums)]
    res2 = 0
    print([num for _, num in nums_with_idx])
    for (idx, num) in tuple(nums_with_idx):
        if num == 0:
            continue
        curr_idx = nums_with_idx.index((idx, num))
        next_idx = (curr_idx + num + len(nums)) % len(nums)
        if num < 0:
            next_idx -= 1
        assert 0 <= curr_idx < len(nums)

        before, after = nums_with_idx[next_idx],  nums_with_idx[(next_idx + 1) % len(nums)]
        if after == nums_with_idx[curr_idx]:
            continue
        val = nums_with_idx.pop(curr_idx)
        print(val[1], (before[1], after[1]))
        nums_with_idx.insert(nums_with_idx.index(after), val)
        if len(nums) == 7:
            print([num for _, num in nums_with_idx])
    assert [num for _, num in nums_with_idx].count(0) == 1
    zero_idx = [num for _, num in nums_with_idx].index(0)
    print(zero_idx, nums_with_idx[zero_idx][1])
    print(
        ((zero_idx + 1000) % len(nums), nums_with_idx[(zero_idx + 1000) % len(nums)][1]),
        ((zero_idx + 2000) % len(nums), nums_with_idx[(zero_idx + 2000) % len(nums)][1]),
        ((zero_idx + 3000) % len(nums), nums_with_idx[(zero_idx + 3000) % len(nums)][1]),
    )
    res1 = (
        nums_with_idx[(zero_idx + 1000) % len(nums)][1]
        + nums_with_idx[(zero_idx + 2000) % len(nums)][1]
        + nums_with_idx[(zero_idx + 3000) % len(nums)][1]
    )
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
