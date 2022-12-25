#!/usr/bin/env pypy3
import sys

"""
Starting from the right, you have a ones place, a fives place,
a twenty-fives place, a one-hundred-and-twenty-fives place, and so on.

the digits are 2, 1, 0, minus (written -), and double-minus (written =).
Minus is worth -1, and double-minus is worth -2."
"""
VALUES = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}
DIGITS = {val: key for key, val in VALUES.items()}

TEST_DATA_SNAFU_TO_DECIMAL = {
    "1=-0-2": 1747,
    "12111": 906,
    "2=0=": 198,
    "21": 11,
    "2=01": 201,
    "111": 31,
    "20012": 1257,
    "112": 32,
    "1=-1=": 353,
    "1-12": 107,
    "12": 7,
    "1=": 3,
    "122": 37,
    "2=-1=0": 4890,
    "1121-1110-1=0": 314159265,
    "1-0---0": 12345,
    "1=11-2": 2022,
}

def decimal_to_snafu(decimal: int) ->  str:
    res = []
    while decimal:
        rest = decimal % 5
        if 0 <= rest <= 2:
            res.insert(0, DIGITS[rest])
            decimal //= 5
            continue
        if rest > 0:
            rest -= 5
        assert rest in {-1, -2}
        res.insert(0, DIGITS[rest])
        decimal -= rest
        decimal //= 5

    return "".join(res)


def snafu_to_decimal(snafu: str) -> int:
    return sum(VALUES[digit] * 5**i for i, digit in enumerate(reversed(snafu)))

def test():
    for snafu, dec in TEST_DATA_SNAFU_TO_DECIMAL.items():
        assert snafu_to_decimal(snafu) == dec
        assert decimal_to_snafu(dec) == snafu
    for i in range(100):
        assert i == snafu_to_decimal(decimal_to_snafu(i))
        num = 117 * i
        assert num == snafu_to_decimal(decimal_to_snafu(num))


def solve(input_: str) -> "tuple[int | str, int | str]":
    lines: list[str] = list(filter(None, input_.split("\n")))

    res1 = decimal_to_snafu(sum(map(snafu_to_decimal, lines)))
    res2 = 0

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
