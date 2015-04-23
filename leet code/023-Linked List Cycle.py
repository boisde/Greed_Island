"""
Given a linked list, determine if it has a cycle in it.

Follow up:
Can you solve it without using extra space?
"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution(object):
    # @param head, a ListNode
    # @return a boolean
    @staticmethod
    def has_cycle(head):
        if not head:
            return False
        two, one = head, head
        while one:
            one = one.next
            if two and two.next:
                two = two.next.next
                if two == one:
                    return True
            else:
                return False