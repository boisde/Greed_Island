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
    # @param intervals, a list of Intervals
    # @param newInterval, a Interval
    # @return a list of Interval
    @staticmethod
    def insert(intervals, new_interval):
        if not intervals:
            return [new_interval]

        # 新增的interval的end比最小的start还要小，添加在最前面 O(n+1)
        if new_interval.end < intervals[0].start:
            intervals[0:0] = new_interval
            return intervals
        # 新增的interval的start比最大的end还要大 O(1)
        elif new_interval.start > intervals[-1].end:
            intervals.append(new_interval)
            return new_interval

        N = len(intervals)
        s, e = new_interval.start, new_interval.end
        for i in range(N):
            si, ei = intervals[i].start, intervals[i].end
            pre_ei = intervals[i-1] if i > 0 else None
            if si <= s <= ei:
                intervals.remove(intervals[i])
                new_start = si
            elif pre_ei < s <= si:
                intervals.remove(intervals[i])
                new_start = s
            elif s <= si and e >= ei:
                intervals.remove(intervals[i])
            elif pre_ei < e <= si or si <= e <= ei:
                new_end = ei if ei>e else e
                intervals[i] = Interval(new_start, new_end)
                return intervals


if __name__ == "__main__":
    interval_list = [Interval(1,6), Interval(8,10), Interval(15,18)]
    final = Solution.insert(interval_list, Interval(6,8))
    for inte in final:
        print "[%d,%d]" % (inte.start, inte.end),
    print