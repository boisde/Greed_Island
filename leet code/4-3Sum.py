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
    def three_sum_n_square(num):
        num = sorted(num)
        N = len(num)
        triplets = []
        for i in range(N-2):
            a = num[i]
            # if processed, skip. The first element does not have former.
            if i > 0 and a == num[i-1]:
                continue
            bi = i+1
            ci = N-1
            # use two pointers to find b,c in elements after a.
            while bi < ci:
                ans = a + num[bi] + num[ci]
                if ans == 0:
                    triplets.append([a, num[bi], num[ci]])
                    # if already in answer, skip.
                    while bi < ci:
                        bi += 1
                        ci -= 1
                        if num[bi]!=num[bi-1] or num[ci]!=num[ci+1]:
                            break
                elif ans < 0:
                    # if already in answer, skip
                    while bi < ci:
                        bi += 1
                        if num[bi]!=num[bi-1]:
                            break
                else:
                    # if already in answer, skip
                    while bi < ci:
                        ci -= 1
                        if num[ci]!=num[ci+1]:
                            break
        return triplets


if __name__ == "__main__":
    S = [-1, 0, 1, 2, -1, -4]
    print "three_sum(%s)=%s" %(S, Solution.three_sum_n_square(S))
    S = [1,2,-2,-1]
    print "three_sum(%s)=%s" %(S, Solution.three_sum_n_square(S))  # []
    S = [3,-2,1,0]
    print "three_sum(%s)=%s" %(S, Solution.three_sum_n_square(S))  # []
    S = [-2,0,1,1,2]
    print "three_sum(%s)=%s" %(S, Solution.three_sum_n_square(S))  # [[-2,0,2],[-2,1,1]]
    S = [0,0,0,0]
    print "three_sum(%s)=%s" %(S, Solution.three_sum_n_square(S))  # [[0,0,0]]
    S = [0,4,-1,0,3,1,1,0,-3,2,-5,-4,-3,0,0,-3]
    print "three_sum(%s)=%s" %(S, Solution.three_sum_n_square(S))  #
    S = [7,-1,14,-12,-8,7,2,-15,8,8,-8,-14,-4,-5,7,9,11,-4,-15,-6,1,-14,4,3,10,-5,2,1,6,11,2,-2,-5,-7,-6,2,-15,11,-6,8,-4,2,1,-1,4,-6,-15,1,5,-15,10,14,9,-8,-6,4,-6,11,12,-15,7,-1,-9,9,-1,0,-4,-1,-12,-2,14,-9,7,0,-3,-4,1,-2,12,14,-10,0,5,14,-1,14,3,8,10,-8,8,-5,-2,6,-11,12,13,-7,-12,8,6,-13,14,-2,-5,-11,1,3,-6]
    print "three_sum(%s)=%s" %(S, Solution.three_sum_n_square(S))  #