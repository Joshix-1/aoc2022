#!/usr/bin/env pypy3
import sys


class CycleList:

    def __init__(self, list_):
        self._list = list_

    def __len__(self):
        return len(self._list)

    def __getitem__(self, idx: int):
        while idx < 0:
            idx += len(self._list)
        idx %= len(self._list)
        return self._list[idx]

    def __setitem__(self, idx, value):
        while idx < 0:
            idx += len(self._list)
        idx %= len(self._list)
        self._list[idx] = value

    def index(self, item):
        return self._list.index(item)

    def swap(self, idx1, idx2):
        x, y = self[idx1], self[idx2]
        self[idx1], self[idx2] = y, x

def solve(input_: str) -> "tuple[int | str, int | str]":
    nums: list[int] = list(map(int, filter(None, input_.split("\n"))))
    nums_with_idx = CycleList([(idx, num) for idx, num in enumerate(nums)])
    assert len(set(nums_with_idx._list)) == len(nums)
    res2 = 0
    if len(nums) == 7:
        print([num for _, num in nums_with_idx._list])
    for _, (_i, num) in enumerate(tuple(nums_with_idx._list)):
        assert _i == _
        if num == 0:
            print("0 does not move:")
            if len(nums) == 7:
                print([num for _, num in nums_with_idx._list])
            continue
        index = nums_with_idx.index((_i, num))
        for i in range(abs(num)):
            sign = num // abs(num)
            diff = i * sign
            nums_with_idx.swap(index + diff, index + diff + sign)

        #print(f"{val[1]} moves between x and {after[1]}")
        if len(nums) == 7:
            print([num for _, num in nums_with_idx._list])
    assert [num for _, num in nums_with_idx._list].count(0) == 1
    zero_idx = [num for _, num in nums_with_idx._list].index(0)
    print(zero_idx, nums_with_idx[zero_idx][1])
    print(
        ((zero_idx + 1000) % len(nums), nums_with_idx[(zero_idx + 1000)][1]),
        ((zero_idx + 2000) % len(nums), nums_with_idx[(zero_idx + 2000)][1]),
        ((zero_idx + 3000) % len(nums), nums_with_idx[(zero_idx + 3000)][1]),
    )
    res1 = (
        nums_with_idx[(zero_idx + 1000)][1]
        + nums_with_idx[(zero_idx + 2000)][1]
        + nums_with_idx[(zero_idx + 3000)][1]
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
