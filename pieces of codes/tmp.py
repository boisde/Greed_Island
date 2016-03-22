if __name__ == "__main__":

    N = int(input())
    S = str(raw_input())
    M = int(input())
    for _ in range(M):
        l, r, k_times = map(int, raw_input().split())
        left_s = S[:l - 1]
        right_s = S[r:]

        part = S[l - 1:r]
        k_times %= len(part)
        if k_times != 0:
            left_part = part[0:len(part) - k_times]
            right_part = part[-k_times:]
            part = right_part + left_part

        S = left_s + part + right_s

    print S
