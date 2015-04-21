#coding=utf-8
"""
Given two sorted integer arrays A and B, merge B into A as one sorted array.

Note:
You may assume that A has enough space (size that is greater or equal to m + n) to hold additional
elements from B. The number of elements initialized in A and B are m and n respectively.
"""


class Solution(object):
    # @param A  a list of integers
    # @param m  an integer, length of A
    # @param B  a list of integers
    # @param n  an integer, length of B
    # @return nothing(void)
    @staticmethod
    def merge(A, m, B, n):  # linear time in m+n
        # 因为A的尾巴上有足够的空间。且A,B都sorted了。
        # 用类似merge sort的想法，只是从尾巴上比较谁比较大，谁大谁放A的尾巴上。
        # 注意为空的情况，为空就赋值。
        pa = m-1
        pb = n-1
        end = m+n-1
        while pa > -1 or pb > -1:
            if pa == -1:
                A[end] = B[pb]
                pb -= 1
                end -= 1
                continue  # 为-1了，不需要再去比较，会list out of index
            elif pb == -1:
                A[end] = A[pa]
                pa -= 1
                end -= 1
                continue

            if A[pa] > B[pb]:
                A[end] = A[pa]
                pa -= 1
            else:
                A[end] = B[pb]
                pb -= 1
            end -= 1


if __name__ == "__main__":
    A, B = [5,7,8,0,0,0], [-1,9,10]
    Solution.merge(A,3,B,3)
    print "%s ==> %s" % (A[:3], A)

    A, B = [1,2,3,0,0,0], [2,5,6]
    Solution.merge(A,3,B,3)
    print "%s ==> %s" % (A[:3], A)