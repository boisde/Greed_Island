# coding=utf-8
"""
There are two sorted arrays nums1 and nums2 of size m and n respectively.
Find the median of the two sorted arrays.

The overall run time complexity should be O(log (m+n)).
"""


class Solution:
    # @param {integer[]} nums1
    # @param {integer[]} nums2
    # @return {float}
    @staticmethod
    def findMedianSortedArrays(A, B):
        pa, pb = 0, 0
        N, M = len(A), len(B)

        is_even = False
        if (N + M) % 2 == 0:
            is_even = True

        prev, cur = None, None
        while pa + pb < ((N + M) // 2) + 1:  # 多走一步，让指针当前停止的位置的值也被put掉
            if pa > N - 1:
                put = B[pb]
                pb += 1
            elif pb > M - 1:
                put = A[pa]
                pa += 1
            else:
                if A[pa] < B[pb]:
                    put = A[pa]
                    pa += 1
                else:
                    put = B[pb]
                    pb += 1
            if not prev:
                prev = put
            elif not cur:
                cur = put
            else:
                prev = cur
                cur = put

        if is_even:
            return (prev + cur) / 2.0
        else:
            return cur if cur else prev  # 两个列表，但总共只有一个值


if __name__ == "__main__":
    print Solution.findMedianSortedArrays([], [2, 3])
