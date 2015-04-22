"""
Given two words (beginWord and endWord), and a dictionary, find the length of shortest
transformation sequence from beginWord to endWord, such that:

Only one letter can be changed at a time
Each intermediate word must exist in the dictionary
For example,

Given:
start = "hit"
end = "cog"
dict = ["hot","dot","dog","lot","log"]
As one shortest transformation is "hit" -> "hot" -> "dot" -> "dog" -> "cog",
return its length 5.

Note:
Return 0 if there is no such transformation sequence.
All words have the same length.
All words contain only lowercase alphabetic characters.
"""


class Solution(object):
    # @param beginWord, a string
    # @param endWord, a string
    # @param wordDict, a set<string>
    # @return an integer
    @staticmethod
    def ladder_length(begin_word, end_word, word_dict):  # 暴力：26*要查找的词长度*dict所含有的词数量
        import collections
        que = collections.deque([(begin_word, 1)])  # intermediate words and its distance to end_word
        alpha = [chr(i) for i in range(ord('a'), ord('z')+1)]
        # 对每个中间词的每个char进行从a到z的替换，
        # 看下新的词是否在dict里面，是的话，就从dict里面去掉，防止重复计算，如果找到，就返回，不然，就继续从中间词queue中pop来处理。
        while que:
            wt = que.popleft()
            w, w_distance = wt[0], wt[1]
            for i in range(len(w)):
                s1 = w[:i]
                s2 = w[i+1:]
                for c in alpha:
                    m = s1 + c + s2
                    if m == end_word:
                        return w_distance+1
                    elif m in word_dict and c != w[i]:
                        word_dict.remove(m)
                        que.append((m, w_distance+1))
        return 0


if __name__ == "__main__":
    start = "hit"
    end = "cog"
    word_dict = ["hot","dot","dog","lot","log"]
    print Solution.ladder_length(start, end, word_dict)