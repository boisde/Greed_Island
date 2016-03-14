# encoding=utf-8
s, e = 16, 18
fin = [s]


def n(x):
    ret = [x + 1, x - 1, x + 3, x - 3]
    return [v for v in ret if 1 <= v <= 18]


def move(x):
    moves = n(x)
    mov = None
    for m in moves:
        if m not in fin:
            mov = m
            fin.append(mov)
            move(mov)
        # else:
        #     return fin
    # Ending: no neighbors.
    if not mov:
        if len(fin) == 18 and fin[17] == e:
            print "SUCCESS: ", fin
        else:
            print "FAILED: ", fin
            global fin
            fin = [s]


if __name__ == "__main__":
    move(s)
