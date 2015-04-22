#coding=utf-8
"""
You are given two linked lists representing two non-negative numbers.
The digits are stored in reverse order and each of their nodes contain a single digit.
Add the two numbers and return it as a linked list.

Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
Output: 7 -> 0 -> 8
"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

    def __repr__(self):
        cur = self
        arr = []
        while cur:
            arr.append(cur.val)
            cur = cur.next
        return str(arr)

class Solution(object):
    # @param {ListNode} l1
    # @param {ListNode} l2
    # @return {ListNode}
    @staticmethod
    def add_two_numbers(l1, l2):  # time cost worst case: len(l1)+len(l2), space: max(len(l1), len(l2))
        if not l1:
            return l2
        elif not l2:
            return l1
        adds_up, digit = divmod(l1.val + l2.val, 10)
        head = ListNode(digit)
        pre = head
        while l1.next or l2.next:
            if not l1.next:
                l2 = l2.next
                adds_up, cur = divmod(l2.val+adds_up, 10)
            elif not l2.next:
                l1 = l1.next
                adds_up, cur = divmod(l1.val+adds_up, 10)
            else:
                l1 = l1.next
                l2 = l2.next
                adds_up, cur = divmod(l1.val+l2.val+adds_up, 10)
            cur = ListNode(cur)
            pre.next = cur
            pre = cur
        # 超级超级容易忘记的！最后的进位处理！
        if adds_up > 0:
            pre.next = ListNode(adds_up)
        return head


if __name__ == "__main__":
    l1 = ListNode(2)
    l1.next = ListNode(4)
    l2 = ListNode(5)
    l2.next = ListNode(6)
    l2.next.next = ListNode(4)
    print Solution.add_two_numbers(l1, l2)

    l1 = ListNode(5)
    l2 = ListNode(5)
    print Solution.add_two_numbers(l1, l2)

    l1.next = ListNode(9)
    print Solution.add_two_numbers(l1, l2)