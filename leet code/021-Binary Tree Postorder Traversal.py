"""
Given a binary tree, return the postorder traversal of its nodes' values.

For example:
Given binary tree {1,#,2,3},
   1
    \
     2
    /
   3
return [3,2,1].

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
    def post_trav(self, root, fin):
        if not root:
            return fin
        self.post_trav(root.left, fin)
        self.post_trav(root.right, fin)
        fin.append(root.val)
    # @param root, a tree node
    # @return a list of integers
    def postorderTraversal(self, root):
        fin = []
        self.post_trav(root, fin)
        return fin