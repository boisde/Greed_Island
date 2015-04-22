#coding=utf-8
"""
Given a string, determine if it is a palindrome, considering only alphanumeric characters and
ignoring cases.

For example,
"A man, a plan, a canal: Panama" is a palindrome.
"race a car" is not a palindrome.

Note:
Have you consider that the string might be empty? This is a good question to ask during an interview.

For the purpose of this problem, we define empty string as valid palindrome.
"""


class Solution(object):
    # @param s, a string
    # @return a boolean
    @staticmethod
    def is_palindrome(s):  # linear in length of string, two pointers
        if not s:
            return True  # None case covered
        p, q = 0, len(s)-1
        while p < q:
            if not ('0' <= s[p] <= '9' or 'a' <= s[p].lower() <= 'z'):
                p += 1
            elif not ('0' <= s[q] <= '9' or 'a' <= s[q].lower() <= 'z'):  # isalnum()?
                q -= 1
            else:
                if s[p].lower() != s[q].lower():
                    return False
                else:
                    p += 1
                    q -= 1
        return True  # empty case covered


if __name__ == "__main__":
    s = "A man, a plan, a canal: Panama"
    print "%s ==> %s" % (s, Solution.is_palindrome(s))
    s = "race a car"
    print "%s ==> %s" % (s, Solution.is_palindrome(s))
    s = ""
    print "%s ==> %s" % (s, Solution.is_palindrome(s))