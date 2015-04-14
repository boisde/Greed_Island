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
        N = len(numbers)
        for i in range(N):
            for j in range(N):
                if numbers[i]+numbers[j] == target and i != j:
                    smaller, bigger = i+1, j+1 if i+1 < j+1 else j+1, i+1
                    return smaller, bigger