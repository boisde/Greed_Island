#coding=utf-8
"""
Given a m x n matrix, if an element is 0, set its entire row and column to 0. Do it in place.

Follow up:
Did you use extra space?
A straight forward solution using O(mn) space is probably a bad idea.
A simple improvement uses O(m + n) space, but still not the best solution.
Could you devise a constant space solution?
"""


class Solution(object):
    # @param matrix, a list of lists of integers
    # @return nothing (void), do not return anything, MODIFY matrix IN PLACE.
    @staticmethod
    def set_zeros_constant_space(matrix):
        # 解法1：暴力,拷贝这个m*n矩阵，依次检视原矩阵的每个格子，如果为0，则将目标矩阵行列全部设为0.
        # time: O(m*n), space(O(m*n)
        # 解法2：用两个数组zero_row[m], zero_col[n]来记录这个m*n矩阵该行该列是否存在(a.k.a该设为)0，
        # 依次检视原矩阵的每个格子，如果该行或者该列有0，则将该格设为0.
        # time: O(m*n), space(O(m+n)
        # 解法3：把这个m*n矩阵的第0行第0列当作解法2中的两个数组zero_row[m], zero_col[n]。
        # time: O(m*n), space(O(1)
        if not matrix:
            return
        m = len(matrix)
        n = len(matrix[0])
        first_row_zero, first_col_zero = False, False
        # 检查第0行，第0列自己;只要有一个0,这行/列最后就应该全是0；性能优化：记得break
        for i in range(0, m):
            if matrix[i][0] == 0:
                first_col_zero = True
                break
        for j in range(0, n):
            if matrix[0][j] == 0:
                first_row_zero = True
                break
        # 然后检查1~m-1行，和1~n-1列
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0
                    matrix[0][j] = 0
        # 先处理1~m-1行，和1~n-1列
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0
        # 最后处理第0行，第0列自己.一定要用开始记住的，因为后面处理1:行1:列的时候原来的一些值可能会被置为0.
        if first_row_zero:
            for j in range(0, n):
                matrix[0][j] = 0
        if first_col_zero:
            for i in range(0, m):
                matrix[i][0] = 0


if __name__ == "__main__":
    matrix = [[0,0,0], [1,1,1]]
    print matrix,
    Solution.set_zeros_constant_space(matrix)
    print "==> %s" % matrix

    matrix = [[0,0,0,2,3,33,333,3333]]
    print matrix,
    Solution.set_zeros_constant_space(matrix)
    print "==> %s" % matrix

    # [[1, 0, 3, 0], [0, 0, 0, 0], [0, 0, 0, 0], [5, 0, 2, 0]]
    matrix = [[1,2,3,4],[5,0,5,2],[8,9,2,0],[5,7,2,1]]
    print matrix,
    Solution.set_zeros_constant_space(matrix)
    print "==> %s" % matrix