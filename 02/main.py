import sys

def main():
    in_ = sys.stdin.read()
    score = 0
    for row in in_.split("\n"):
        if not row:
            continue
        # A for Rock, B for Paper, and C for Scissors.
        # X for Rock, Y for Paper, and Z for Scissors.
        opponent = "ABC".index(row[0])
        me = row[2]
        if me == "X":
            me = (opponent - 1 + 3) % 3
        elif me == "Y":
            me = opponent
        elif me == "Z":
            me = (opponent + 1) % 3
        won = False
        draw = False
        if me == opponent:
            draw = True
        elif opponent == 0:
            won = me == 1
        elif opponent == 1:
           won = me == 2
        else:
           assert opponent == 2
           won = me == 0
        score += 1 + me
        if draw:
            score += 3
        elif won:
           score += 6
    print(score)

main()
