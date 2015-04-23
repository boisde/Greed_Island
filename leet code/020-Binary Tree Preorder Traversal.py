"""
Given a binary tree, return the preorder traversal of its nodes' values.

For example:
Given binary tree {1,#,2,3},
   1
    \
     2
    /
   3
return [1,2,3].

Note: Recursive solution is trivial, could you do it iteratively?
"""


# Definition for a  binary tree node
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

    def __repr__(self):
        return str(self.val)


class Solution(object):
    # @param root, a tree node
    # @return a list of integers
    @staticmethod
    def preorder_traversal(root, arr):
        if not root:
            return
        arr.append(root.val)
        Solution.preorder_traversal(root.left, arr)
        Solution.preorder_traversal(root.right, arr)

    @staticmethod
    def preorder_traversal_iter(root):
        import collections
        pre_que, result = collections.deque([]), []
        if not root:
            return result
        pre_que.append(root)
        while pre_que:
            cur = pre_que.popleft()
            result.append(cur.val)
            if cur.left:
                pre_que.append(cur.left)
            if cur.right:
                pre_que.append(cur.right)
        return result


if __name__ == "__main__":
    r = TreeNode(1)
    r.left = TreeNode(-2)
    r.right = TreeNode(3)
    r.right.left = TreeNode(2)
    r.right.left.right = TreeNode(2.5)
    arr = []
    Solution.preorder_traversal(r, arr)
    print arr

    print Solution.preorder_traversal_iter(r)