import sys

def main() -> None:
    in_ = sys.stdin.read()
    score = [0, 0]
    for row in in_.split("\n"):
        if not row:
            continue
        # A for Rock, B for Paper, and C for Scissors.
        # X for Rock, Y for Paper, and Z for Scissors.
        opponent = "ABC".index(row[0])
        for i in range(2):
            me = row[2]
            if i == 0:
                me = "XYZ".index(me)
            else:
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
            score[i] += 1 + me
            if draw:
                score[i] += 3
            elif won:
               score[i] += 6
    print(f"1: {score[0]}\n2: {score[1]}")

if __name__ == "__main__":
    main()
