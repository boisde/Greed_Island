# coding=utf-8

if __name__ == "__main__":

    balls = [i for i in range(8)]
    n_times, k_sets = map(int, raw_input().split())

    handles = []
    for _ in range(n_times):
        ai, bi = map(int, raw_input().split())
        handles.append((ai, bi))

    if k_sets % 15 != 0:
        for i in range(n_times):
            ai, bi = handles[i]
            balls[ai - 1], balls[bi - 1] = balls[bi - 1], balls[ai - 1]
        bd = {}
        for now_at_index, ball in enumerate(balls):
            bd[ball] = now_at_index
        print bd
        for _ in range(k_sets % 15 - 1):
            tmp = {}
            for i in range(8):
                if bd[i] not in tmp:
                    tmp[bd[i]] = balls[bd[i]]  # 原来bd[i]位置上的球
                if i in tmp:
                    balls[bd[i]] = tmp[i]
                else:
                    balls[bd[i]] = balls[i]

    balls = [str(i + 1) for i in balls]
    print " ".join(balls)
