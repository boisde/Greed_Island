#coding=utf-8
"""
Given an array of integers, every element appears twice except for one. Find that single one.

Note:
Your algorithm should have a linear runtime complexity.
Could you implement it without using extra memory?
"""


class Solution(object):
    # @param {integer[]} nums
    # @return {integer}
    @staticmethod
    # 利用这两个逻辑：x^x=0; x^0=x
    def single_number_linear(nums):
        single = 0
        for i in range(len(nums)):
            single ^= nums[i]
        return single