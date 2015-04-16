"""
Merge two sorted linked lists and return it as a new list.
The new list should be made by splicing together the nodes of the first two lists.
"""


# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

    def __repr__(self):
        ll = []
        cur = self
        while cur:
            ll.append(cur.val)
            cur = cur.next
        return str(ll)


class Solution(object):
    # @param two ListNodes
    # @return a ListNode
    @staticmethod
    def merge_two_lists(m, n):  # linear in sum of length of two lists
        # TODO improve performance when some list empty
        head, put_away = None, None
        while m or n:
            # find the elem to put away
            if not m:
                to_put_away = n
                n = n.next
            elif not n:
                to_put_away = m
                m = m.next
            else:
                if m.val <= n.val:
                    to_put_away = m
                    m = m.next
                else:
                    to_put_away = n
                    n = n.next
            # add link if not the first put_away
            # always put_away
            if put_away:
                put_away.next = to_put_away  # add link
                put_away = to_put_away
            # init
            else:
                put_away = to_put_away
                head = put_away
        return head

    @staticmethod
    def merge_two_lists_recursive(m, n):
        if not m:
            return n
        if not n:
            return m
        if m.val <= n.val:
            m.next = Solution.merge_two_lists_recursive(m.next, n)
            return m
        else:
            n.next = Solution.merge_two_lists_recursive(m, n.next)
            return n

if __name__ == "__main__":
    m = ListNode(0)
    m.next = ListNode(4)
    n = ListNode(1)
    n.next = ListNode(2)
    print Solution.merge_two_lists(ListNode(0), ListNode(1))
    print Solution.merge_two_lists(m, n)