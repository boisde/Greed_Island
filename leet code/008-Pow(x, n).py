"""
Implement pow(x, n).
"""


class Solution(object):
    # @param x, a float
    # @param n, a integer
    # @return a float
    @staticmethod
    def pow(x, n):
        if n > 1:
            half = Solution.pow(x, n//2)
            if n%2 == 0:
                return half*half
            else:
                return half*half*x
        elif n < 0:
            return 1.0/Solution.pow(x, -n)
        elif n == 1:
            return x
        # n == 0
        else:
            return 1


if __name__ == "__main__":
    print Solution.pow(0.00001, 2147483647)