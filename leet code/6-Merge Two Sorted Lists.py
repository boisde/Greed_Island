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
        ll = [self.val]
        while self.next:
            ll.append(self.next.val)
        return str(ll)


class Solution(object):
    # @param two ListNodes
    # @return a ListNode
    @staticmethod
    def merge_two_lists(m, n):  # linear in sum of length of two lists
        head, put_away = None, None
        while m or n:
            # find the elem to put away
            if not m:
                to_put_away = n
            elif not n:
                to_put_away = m
            else:
                if m.val <= n.val:
                    to_put_away = m
                    m = m.next
                else:
                    to_put_away = n
                    n = n.next
            # add link if not the first put_away
            if not put_away:
                put_away = to_put_away
                head = put_away
            else:
                put_away.next = to_put_away
                put_away = to_put_away
                # either list is empty, Done!
                if not m or not n:
                    break
        return head

if __name__ == "__main__":
    print Solution.merge_two_lists(ListNode(0), ListNode(1))
    # m = ListNode(0)
    # m.next = ListNode(4)
    # n = ListNode(1)
    # n.next = ListNode(2)
    # print Solution.merge_two_lists(m, n)
