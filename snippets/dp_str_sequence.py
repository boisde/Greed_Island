class Solution:
    def __init__(self, seq):
        # self.seq = [4, 3, 1, 2, 3, 3, 3]
        self.seq = seq
        self.memo_dp_up = {0: 1}
        self.prev = [-1] * len(self.seq)
        self.memo_dp_down = {0: 1}
        self.calls_exp = 0
        self.calls_dp = 0

    def up_exp(self, i):
        self.calls_exp += 1
        # if has computed, just return
        # if i in self.memo:
        #     return self.memo[i]
        # compute the prefix
        if i == 0:
            return 1
        guesses = []
        for j in range(i):
            if self.seq[j] < self.seq[i]:  # strictly increment
                length = self.up_exp(j) + 1
            else:
                length = 1
            guesses.append(length)
        return max(guesses)

    def up_dp(self, N):
        # self.calls_dp += 1
        # # return result if computed
        # if i in self.memo_dp_up:
        #     return self.memo_dp_up[i]
        # # compute using prefix[:i] as sub-problem, which should be already computed
        # # guess all possibilities from 0 to i-1.
        # for j in range(i):
        #     length = self.up_dp(j) + 1 if self.seq[j] < self.seq[i] else self.up_dp(j)
        # # memorize solution at index i
        # self.memo_dp_up[i] = length
        # return self.memo_dp_up[i]
        maxlen = 1
        dp = {0: 1}
        for i in range(1, N):
            dp[i] = 1
            for j in range(i):
                if dp[j] + 1 > dp[i] and self.seq[j] < self.seq[i]:
                    dp[i] = dp[j] + 1
            if dp[i] > maxlen:
                maxlen = dp[i]
        return maxlen

    def up(self, i):
        if i in self.memo_dp_up:
            return self.memo_dp_up[i]
        guesses = []
        for j in range(i):
            if self.seq[j] < self.seq[i]:
                max_len = self.up(j) + 1
                self.prev[i] = j
            else:
                max_len = 1
            guesses.append(max_len)
        self.memo_dp_up[i] = max(guesses)
        return self.memo_dp_up[i]

    def zigzag(self, n):
        up, down = {0: 1}, {0: 1}
        best_len = 0
        for i in range(n):
            up[i], down[i] = 1, 1
            print "i=[%d], up=%s, down=%s" % (i, up, down)
            for j in range(i):
                up[i] = max(down[j] + 1, up[i]) if self.seq[i] > self.seq[j] else 1
                down[i] = max(up[j] + 1, down[i]) if self.seq[i] < self.seq[j] else 1
            best_len = max(best_len, max(up[i], down[i]))
        return best_len


if __name__ == "__main__":
    sol1 = Solution([6, 7, 8, 1, 2, 3])
    print "up_exp%s=[%d], func calls=[%d]" % (sol1.seq, sol1.up_exp(len(sol1.seq) - 1), sol1.calls_exp)

    print "up_dp%s=[%d], func calls=[%d], memo=%s" % (
    sol1.seq, sol1.up_dp(len(sol1.seq) - 1), sol1.calls_dp, sol1.memo_dp_up)

    # sol2 = Solution([1, 7, 4, 9, 2, 5])
    sol2 = Solution([1, 2, 12, 10, 11])
    # sol2 = Solution([1, 17, 5, 10, 13, 15, 10, 5, 16, 8])
    print "zigzag%s=[%d]" % (sol2.seq, sol2.zigzag(len(sol2.seq)))
