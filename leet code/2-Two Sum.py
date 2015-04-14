#coding= utf-8

"""
Given an array of integers, find two numbers such that they add up to a specific target number.

The function twoSum should return indices of the two numbers such that they add up to the target,
where index1 must be less than index2.
Please note that your returned answers (both index1 and index2) are not zero-based.

You may assume that each input would have exactly one solution.

Input: numbers={2, 7, 11, 15}, target=9
Output: index1=1, index2=2
"""


class Solution(object):
    @staticmethod
    def two_sum_n_squared(numbers, target):
        # brute force method
        N = len(numbers)
        for i in range(N):
            for j in range(N):
                if numbers[i]+numbers[j] == target and i != j:
                    # don't forget the parenthesis, or will report compile error with
                    # "too many values to unpack"
                    smaller, bigger = (i+1, j+1) if i+1 < j+1 else (j+1, i+1)
                    return smaller, bigger

    @staticmethod
    def two_sum_n(numbers, target):
        N = len(numbers)
        num_dict = {}
        for i in range(N):
            num_dict[numbers[i]] = i
        for i in range(N):
            to_find = target - numbers[i]
            # remember to rule self out
            if to_find in num_dict and num_dict[to_find] != i:
                smaller, bigger = i+1, num_dict[to_find] + 1
                smaller, bigger = (smaller, bigger) if smaller<bigger else (bigger, smaller)
                return smaller, bigger
        return -1, -1

    @staticmethod
    def two_sum_n_refined(num, target):
        num_dict = {}
        for i in range(len(num)):
            partner = target - num[i]
            # no need to rule self out here, cause you won't encounter yourself again
            if partner in num_dict:
                # by the time find your partner, you are already in dictionary,
                # and you are always the prior one
                return num_dict[partner]+1, i+1
            else:
                num_dict[num[i]] = i
        return -1, -1


if __name__ == "__main__":
    print Solution.two_sum_n_refined([3,2,4], 6)
    print Solution.two_sum_n_refined([3,2,2], 4)
    print Solution.two_sum_n_refined([3,2,2,2,2,2,2,2,2,2,2,2,2,2], 4)