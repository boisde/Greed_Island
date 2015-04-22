"""
Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

The brackets must close in the correct order, "()" and "()[]{}" are all valid but "(]" and "([)]" are not.
"""


class Solution(object):
    # @param s, a string
    # @return a boolean
    @staticmethod
    def is_valid(s):
        pair = {'(':')', '[':']', '{':'}'}
        stack = []
        for c in s:
            if c == '(' or c == '[' or c == '{':
                stack.append(c)
            elif c == ')' or c == ']' or c == '}':
                # stack empty!!!
                if not stack:
                    return False
                # not empty
                left_bracket = stack.pop()
                if pair[left_bracket] != c:
                    return False
        # check final stack, should be empty!!!
        if not stack:
            return True
        else:
            return False

if __name__ == "__main__":
    print Solution.is_valid("[][][][][][]")
    print Solution.is_valid("[(]{{}}}}}}[)][][][][]")
    print Solution.is_valid("=-=-=[(}][][][][][]")
    # what I did not think of
    print Solution.is_valid("]")  # False
    print Solution.is_valid("[")  # False