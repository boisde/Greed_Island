# coding=utf-8

"""
Given an array S of n integers, are there elements a, b, c in S such that a + b + c = 0?
Find all unique triplets in the array which gives the sum of zero.

Note:
- Elements in a triplet (a,b,c) must be in non-descending order. (ie, a ≤ b ≤ c)
- The solution set must not contain duplicate triplets.

    A solution set is:
    (-1, 0, 1)
    (-1, -1, 2)
"""


class Solution(object):
    @staticmethod
    # @return a list of lists of length 3, [[val1,val2,val3]]
    def three_sum_n_cubed(num):
        # todo: remove duplicated triplet
        N = len(num)
        triplets = []
        for i in range(N):
            target = 0 - num[i]
            for j in range(i+1, N):
                partner = target - num[j]
                for k in range(j+1, N):
                    if partner == num[k]:
                        triplets.append(sorted([num[i], num[j], num[k]]))
        return triplets


if __name__ == "__main__":
    S = [-1, 0, 1, 2, -1, -4]
    print "three_sum(%s)=%s" %(S, Solution.three_sum_n_cubed(S))