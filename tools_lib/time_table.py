#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-10-14 15:08:32
# @Author  : Jim Zhang (jim.zoumo@gmail.com)
# @Github  : https://github.com/zoumo

# from compiler.ast import flatten
import unittest2


def flatten(seq):
    l = []
    for elt in seq:
        if isinstance(elt, (tuple, list)):
            for elt2 in flatten(elt):
                l.append(elt2)
        else:
            l.append(elt)
    return l


def real_index(mid):
    id1 = mid / 2
    id2 = 1 if mid & 1 else 0
    return id1, id2


def binary_search(array, m):
    """
    二分查找
    array是二维数组: [(1,3), (4,6), (7,8)]
    m是需要搜索的数: 5
    """

    array.sort()
    item_num = len(array)
    flatten_array = flatten(array)
    length = len(flatten_array)

    assert(item_num * 2 == length)

    low = 0
    high = length - 1
    left = -1
    right = high + 1
    index = -1

    while low <= high:
        mid = (low + high) / 2
        midval = flatten_array[mid]
        # id1, id2 = real_index(mid)
        # midval = array[id1][id2]

        if midval < m:
            left = mid
            low = mid + 1
        elif midval > m:
            right = mid
            high = mid - 1
        else:
            index = mid
            left = mid
            right = left + 1
            break

    return index, left, right


def is_conflict(array, target):
    """
    时间表合并, 检查冲突
    array是二维数组: [(1,3), (4,6), (7,8)]
    targe是需要合并的新的时间: (5, 6)
    ====================================================
    [ . (1,3) , (4,6) , (7,8) . ]
      -   0   1   2   3   4   +
    我们发现只有当targe[0]和targe[1]同时落在-, 1, 3, +这几个位置时, 时间表合并才不会冲突
    ====================================================
    将 array 压扁
    [ 1 , 3 , 4 , 6 , 7 , 8 ]
      0   1   2   3   4   5
    我们可以用二分查找来查询targe[0]所在的位置
    如果targe[0]落在(1,3), (4,6), (7,8)中, 即索引为(0,1), (2,3), (4,5), 则说明一定会有冲突发生
    当targe[0]符合要求后, 只要targe[1]与targe[0]落在相同的区间则合并成功
    """
    if len(target) != 2 or target[0] >= target[1]:
        return True

    if len(array) == 0:
        return False

    start = target[0]
    end = target[1]

    index, left, right = binary_search(array, start)
    # print array, target, index, left, right

    if not (left & 1) or not (index & 1):
        return True
    elif left == len(array)*2 - 1:
        # array.append(targe)
        return False
    else:
        id1, id2 = real_index(right)
        if end <= array[id1][id2]:
            # array.append(targe)
            return False
        else:
            return True

if __name__ == '__main__':
    class TestCreateAPI(unittest2.TestCase):

        def test_is_conflict_0(self):
            case = []
            t = [1, 2]
            self.assertFalse(is_conflict(case, t))

        def test_is_conflict_1(self):

            case = [[1, 2]]
            t = [1, 2]
            self.assertTrue(is_conflict(case, t))
            t = [2, 3]
            self.assertFalse(is_conflict(case, t))
            t = [0, 1]
            self.assertFalse(is_conflict(case, t))

        def test_is_conflict_2(self):

            case = [[1, 2], [2, 3]]
            t = [0, 1]
            self.assertFalse(is_conflict(case, t))
            t = [3, 4]
            self.assertFalse(is_conflict(case, t))
            t = [1.5, 2.1]
            self.assertTrue(is_conflict(case, t))
            t = [2, 2.1]
            self.assertTrue(is_conflict(case, t))
            t = [1.6, 2]
            self.assertTrue(is_conflict(case, t))
            t = [2, 2]
            self.assertTrue(is_conflict(case, t))

        def test_is_conflict_3(self):

            case = [[1, 2], [2, 3], [3, 4]]
            t = [2, 2.1]
            self.assertTrue(is_conflict(case, t))
            t = [3, 3.1]
            self.assertTrue(is_conflict(case, t))
            t = [2.8, 3.1]
            self.assertTrue(is_conflict(case, t))

    unittest2.main()
