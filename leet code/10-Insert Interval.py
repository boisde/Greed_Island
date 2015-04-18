#coding=utf-8
"""
Given a set of non-overlapping intervals, insert a new interval into the intervals (merge if necessary).

You may assume that the intervals were initially sorted according to their start times.

Example 1:
Given intervals [1,3],[6,9], insert and merge [2,5] in as [1,5],[6,9].

Example 2:
Given [1,2],[3,5],[6,7],[8,10],[12,16], insert and merge [4,9] in as [1,2],[3,10],[12,16].

This is because the new interval [4,9] overlaps with [3,5],[6,7],[8,10].
"""


# Definition for an interval.
class Interval:
    def __init__(self, s=0, e=0):
        self.start = s
        self.end = e


class Solution(object):
    # 我写的这个实现简直就是渣渣中的战斗渣！！！
    # @param intervals, a list of Intervals
    # @param newInterval, a Interval
    # @return a list of Interval
    @staticmethod
    def insert(intervals, new_interval):  # linear
        if not intervals:
            return [new_interval]

        # 新增的interval的end比最小的start还要小，添加在最前面 O(n+1)
        if new_interval.end < intervals[0].start:
            # intervals[0:0] = new_interval  OJ 不支持slicing方式的insert
            intervals.insert(0, new_interval)
            return intervals
        # 新增的interval的start比最大的end还要大 O(1)
        elif new_interval.start > intervals[-1].end:
            intervals.append(new_interval)
            return intervals

        N = len(intervals)
        s, e = new_interval.start, new_interval.end
        fin = []
        # 第一段是特殊的，因为没有pre_ei来比较。
        s0, e0 = intervals[0].start, intervals[0].end
        if e0 < s:  # 不可能是e < s0,因为前面排除过新的interval在所有intervals前面的情况。
            fin.append(intervals[0])
        else:
            new_start = min(s0, s)
            # 判断end
            if e <= e0:
                fin.append(Interval(new_start, e0))
                fin.extend(intervals[1:])
                return fin
            elif N == 1:
                fin.append(Interval(new_start, e))

        for i in range(1, N):
            si, ei = intervals[i].start, intervals[i].end
            pre_ei = intervals[i - 1].end
            if pre_ei < s <= si:  # interval的start在这条线段start点的外部（不包含上一个end,因为否则就要与上一个merge），更新新的start。
                new_start = s
            elif si <= s <= ei:  # interval的start在某个interval线段上，包含头尾。更新新的start。
                new_start = si
            elif s < si and e > ei and i != N - 1:  # 该interval包含的内部线段，都无视。
                continue
            elif s > ei:
                fin.append(intervals[i])

            if pre_ei < e < si:
                new_end = e
                fin.append(Interval(new_start, new_end))
                fin.append(intervals[i])
            elif si <= e <= ei:  # 找ending.和找start其实是一样的.
                new_end = ei
                fin.append(Interval(new_start, new_end))
            elif e < si:
                fin.append(intervals[i])

            if i == N - 1 and e > ei:
                fin.append(Interval(new_start, e))
        return fin

    # 这个实现好！先append,然后sort,然后就可以用merge intervals同样的算法。
    @staticmethod
    def insert_nlogn(intervals, new_interval):
        intervals.append(new_interval)

        def interval_cmp(x, y):
            if x.start < y.start:
                return -1
            elif x.start > y.start:
                return 1
            else:
                return 0

        intervals = sorted(intervals, cmp=interval_cmp)
        if not intervals:
            return []

        N = len(intervals)
        cur = intervals[0]
        fin = []
        for i in range(1, N):
            nxt = intervals[i]
            # 只有这种情况没有交集，cur应该被放入结果集
            if cur.end < nxt.start:
                fin.append(cur)
                cur = nxt
            # 有交集，更新cur的尾巴
            else:
                cur.end = max(cur.end, nxt.end)
        fin.append(cur)
        return fin


if __name__ == "__main__":
    # ==> [1,10] [15,18]
    interval_list = [Interval(1, 6), Interval(8, 10), Interval(15, 18)]
    final = Solution.insert(interval_list, Interval(6, 8))
    for inte in final:
        print "[%d,%d]" % (inte.start, inte.end),
    print "<==>",
    final = Solution.insert_nlogn(interval_list, Interval(6, 8))
    for inte in final:
        print "[%d,%d]" % (inte.start, inte.end),
    print

    # [1,2],[3,5],[6,7],[8,10],[12,16] ==> [1,2] [3,10] [12,16]
    interval_list = [Interval(1, 2), Interval(3, 5), Interval(6, 7), Interval(8, 10), Interval(12, 16)]
    final = Solution.insert(interval_list, Interval(4, 9))
    for inte in final:
        print "[%d,%d]" % (inte.start, inte.end),
    print "<==>",
    final = Solution.insert_nlogn(interval_list, Interval(4, 9))
    for inte in final:
        print "[%d,%d]" % (inte.start, inte.end),
    print

    # [[1,5]], [2,3] ==> [[1,5]]
    interval_list = [Interval(1, 5)]
    final = Solution.insert(interval_list, Interval(2, 3))
    for inte in final:
        print "[%d,%d]" % (inte.start, inte.end),
    print "<==>",
    final = Solution.insert_nlogn(interval_list, Interval(2, 3))
    for inte in final:
        print "[%d,%d]" % (inte.start, inte.end),
    print

    # [[1,5], [6,8]], [0,9] ==> [[0,9]]
    interval_list = [Interval(1, 5), Interval(6, 8)]
    final = Solution.insert(interval_list, Interval(0, 9))
    for inte in final:
        print "[%d,%d]" % (inte.start, inte.end),
    print "<==>",
    final = Solution.insert_nlogn(interval_list, Interval(0, 9))
    for inte in final:
        print "[%d,%d]" % (inte.start, inte.end),
    print

    # [[0,5],[8,9]], [3,4] ==> [[0,5],[8,9]]
    interval_list = [Interval(0, 5), Interval(8, 9)]
    final = Solution.insert(interval_list, Interval(3, 4))
    for inte in final:
        print "[%d,%d]" % (inte.start, inte.end),
    print "<==>",
    final = Solution.insert_nlogn(interval_list, Interval(3, 4))
    for inte in final:
        print "[%d,%d]" % (inte.start, inte.end),
    print

    # [[0,2],[3,3],[6,11]], [9,15] ==> [[0,2],[3,3],[6,15]]
    interval_list = [Interval(0, 2), Interval(3, 3), Interval(6, 11)]
    final = Solution.insert(interval_list, Interval(9, 15))
    for inte in final:
        print "[%d,%d]" % (inte.start, inte.end),
    print "<==>",
    final = Solution.insert_nlogn(interval_list, Interval(9, 15))
    for inte in final:
        print "[%d,%d]" % (inte.start, inte.end),
    print

    # [[0,0],[1,3],[5,11]], [0,3] ==> [[0,3],[5,11]]
    interval_list = [Interval(0, 0), Interval(1, 3), Interval(5, 11)]
    final = Solution.insert(interval_list, Interval(0, 3))
    for inte in final:
        print "[%d,%d]" % (inte.start, inte.end),
    print "<==>",
    final = Solution.insert_nlogn(interval_list, Interval(0, 3))
    for inte in final:
        print "[%d,%d]" % (inte.start, inte.end),
    print

    # [[0,4],[7,12]], [0,5] ==> [[0,5],[7,12]]
    interval_list = [Interval(0, 4), Interval(7, 12)]
    final = Solution.insert(interval_list, Interval(0, 5))
    for inte in final:
        print "[%d,%d]" % (inte.start, inte.end),
    print "<==>",
    final = Solution.insert_nlogn(interval_list, Interval(0, 5))
    for inte in final:
        print "[%d,%d]" % (inte.start, inte.end),
    print