"""
Given a collection of intervals, merge all overlapping intervals.

For example,
Given [1,3],[2,6],[8,10],[15,18],
return [1,6],[8,10],[15,18].
"""


# Definition for an interval.
class Interval(object):
    def __init__(self, s=0, e=0):
        self.start = s
        self.end = e


class Solution(object):
    # @param intervals, a list of Interval
    # @return a list of Interval
    @staticmethod
    def merge(intervals):  # sorted should cause NlogN runtime.
        if not intervals:
            return []

        def interval_cmp(x, y):
            if x.start < y.start:
                return -1
            elif x.start > y.start:
                return 1
            else:
                return 0
        intervals = sorted(intervals, cmp=interval_cmp)
        for inter in intervals:
            print "[%d,%d]" % (inter.start, inter.end),
        N = len(intervals)
        cur = intervals[0]
        fin = []
        for i in range(1, N):
            nxt = intervals[i]
            # cur should be inside the final
            if cur.end < nxt.start:
                fin.append(cur)
                cur = nxt
            # merge overlapping intervals
            else:
                cur.end = nxt.end if nxt.end > cur.end else cur.end
        # remember to add the last cur into final
        fin.append(cur)
        return fin


if __name__ == "__main__":
    interval_list = [Interval(1,3), Interval(2,6), Interval(8,10), Interval(15,18)]
    final = Solution.merge(interval_list)
    print "==>",
    for interval in final:
        print "[%d,%d]" % (interval.start, interval.end),
    print

    interval_list = [Interval(1,4), Interval(0,4)]
    final = Solution.merge(interval_list)
    print "==>",
    for interval in final:
        print "[%d,%d]" % (interval.start, interval.end),
    print