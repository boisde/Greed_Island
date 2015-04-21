"""
Given a binary tree, determine if it is a valid binary search tree (BST).

Assume a BST is defined as follows:

The left subtree of a node contains only nodes with keys less than the node's key.
The right subtree of a node contains only nodes with keys greater than the node's key.
Both the left and right subtrees must also be binary search trees.


confused what "{1,#,2,3}" means? > read more on how binary tree is serialized on OJ.

OJ's Binary Tree Serialization:
The serialization of a binary tree follows a level order traversal,
where '#' signifies a path terminator where no node exists below.

Here's an example:
   1
  / \
 2   3
    /
   4
    \
     5
The above binary tree is serialized as "{1,2,3,#,#,4,#,#,5}".
"""


# Definition for a binary tree node
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution(object):
    # @param root, a tree node
    # @return a boolean
    @staticmethod
    def is_valid_bst(root):  # time cost is logN, where N is num of tree elements
        if not root:
            return True


if __name__ == "__main__":
    r = TreeNode(1)
    r.left = TreeNode(2)
    r.right = TreeNode(3)
    r.right.left = TreeNode(4)
    r.right.left.right = TreeNode(5)
    print Solution.is_valid_bst(r)

    r1 = TreeNode(10)
    r1.left = TreeNode(5)
    r1.right = TreeNode(15)
    r1.right.left = TreeNode(6)
    r1.right.right = TreeNode(20)
    print Solution.is_valid_bst(r1)