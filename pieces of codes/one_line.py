# encoding=utf-8
s, e = (6, 1), (6, 3)


def n(x, been):
    i, j = x[0], x[1]
    ret = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
    ret = [v for v in ret if 1 <= v[0] <= 6 and 1 <= v[1] <= 3]
    for elem in ret:
        if elem in been:
            ret.remove(elem)
    return ret


def move(x, been):
    if x == e:
        been.append(x)
        return been
    elif x in been:
        print "x in been", been
        return been
    else:
        been.append(x)

    moves = n(x, been)
    if not moves:
        return been

    for m in moves:
        move(m, been)


if __name__ == "__main__":
    # for mi in xrange(1, 7):
    #     for mj in xrange(1, 4):
    #         print "(%s%s):" % (mi, mj), n((mi, mj))
    move(s, [])
