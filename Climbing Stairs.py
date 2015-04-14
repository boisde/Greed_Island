#coding=utf-8
"""
You are climbing a stair case. It takes n steps to reach to the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?
"""

ways = {1:1, 2:2}
class Solution:
    # @param n, an integer
    # @return an integer
    @staticmethod
    def climbStairs(n):
        if n in ways:
            return ways[n]
        # 爬n级楼梯的不同方法=最后一次2级爬上去/1级爬上去，剩下的级数不同爬法之和
        ways[n] = Solution.climbStairs(n-1) + Solution.climbStairs(n-2)
        return ways[n]

    @staticmethod
    def climb_stairs_n(n):
        n1, n2, w = 1, 2, []
        for _ in range(n):
            w.append(n1)
            # 第n级楼梯要么是从第n-1级走上来，要么是从第n-2级走上来的
            n1, n2 = n2, n1+n2
        return w[n-1]

if __name__ == "__main__":
    print "climb_stairs(%d)=[%d]" % (3, Solution.climbStairs(3))
    print "climb_stairs(%d)=[%d]" % (13, Solution.climbStairs(13))
    print "climb_stairs_n(%d)=[%d]" % (3, Solution.climb_stairs_n(3))
    print "climb_stairs_n(%d)=[%d]" % (13, Solution.climb_stairs_n(13))
    print "climb_stairs_n(%d)=[%d]" % (13000, Solution.climb_stairs_n(13000))