"""
Given a singly linked list L: L0->L1...->Ln-1->Ln.
reorder it to: L0->Ln->L1->Ln-1->L2->Ln-2...

You must do this in-place without altering the nodes' values.

For example,
Given {1,2,3,4}, reorder it to {1,4,2,3}.
"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution(object):
    # @param head, a ListNode
    # @return nothing
    @staticmethod
    def reorder_list(head):
        if not head:
            return
        import collections
        stack = collections.deque([])
        one, two = head, head
        while two:
            if two.next:
                two = two.next.next
                one = one.next
            else:
                break
        while one:
            stack.append(one)
            one = one.next
        pre = head
        while stack:
            cur = stack.pop()
            cur.next = pre.next
            pre.next = cur
            pre = cur.next
        cur.next = None