#coding=utf=8
"""
Given an array of integers, every element appears three times except for one. Find that single one.

Note:
Your algorithm should have a linear runtime complexity.
Could you implement it without using extra memory?
"""


class Solution(object):
    # @param {integer[]} nums
    # @return {integer}
    @staticmethod
    # hash<integer_val, times>, linear runtime, N/3+1 space
    def singleNumber(nums):
        single_dict = {}
        for i in range(len(nums)):
            if nums[i] not in single_dict:
                single_dict[nums[i]] = 1
            else:
                single_dict[nums[i]] += 1
        for distinct in single_dict:
            if single_dict[distinct] == 1:
                return distinct


if __name__ == "__main__":
    print Solution.singleNumber([333,1,2,2,2,333,333])