"""
Find the contiguous sub- array within an array (containing at least one number)
which has the largest sum.

For example, given the array [-2,1,-3,4,-1,2,1,-5,4]
the contiguous sub-array [4,-1,2,1] has the largest sum = 6.

More practice:
If you have figured out the O(n) solution, try coding another solution using
the divide and conquer approach, which is more subtle.
"""


class Solution(object):
    # @param {integer[]} nums
    # @return {integer}
    @staticmethod
    def max_sub_array(nums):
        ending_here_sum, cur_max = nums[0], nums[0]
        for i in range(1, len(nums)):
            ending_here_sum = max(ending_here_sum+nums[i], nums[i])
            cur_max = max(cur_max, ending_here_sum)
        return cur_max