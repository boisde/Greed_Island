#coding=utf-8
"""
A linked list is given such that each node contains an additional random pointer
which could point to any node in the list or null.

Return a deep copy of the list.
"""


# Definition for singly-linked list with a random pointer.
class RandomListNode:
    def __init__(self, x):
        self.label = x
        self.next = None
        self.random = None

    def __repr__(self):
        return str(self.label)


class Solution(object):
    # @param head, a RandomListNode
    # @return a RandomListNode
    @staticmethod
    def copy_random_list(head):  # time cost 2N, space 2N
        if not head:
            return head
        # 存放<旧链表elem>:<复制后的elem>
        list_dict = {}
        cur = head
        while cur:
            list_dict[cur] = RandomListNode(cur.label)
            cur = cur.next
        cur = head
        while cur:
            # 即使没有next了，也有可能有random，所以要全部链表elem处理，不能漏掉最后一个
            if cur.next:
                list_dict[cur].next = list_dict[cur.next]
            if cur.random:
                list_dict[cur].random = list_dict[cur.random]
            cur = cur.next
        new_head = list_dict[head]
        return new_head