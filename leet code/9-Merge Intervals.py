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
    def merge(intervals):
        pass


if __name__ == "__main__":
    interval_list = [Interval(1,3), Interval(2,6), Interval(8,10), Interval(15,18)]
    print Solution.merge(interval_list)