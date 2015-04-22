#coding=utf-8
"""
Validate if a given string is numeric.

Some examples:
"0" => true
" 0.1 " => true
"abc" => false
"1 a" => false
"2e10" => true

Note: It is intended for the problem statement to be ambiguous.
You should gather all requirements up front before implementing one.

constraints:
- should strip string with whitespaces
- can contain . as float number
- float number can begin with only .<digits>, i.e. 0 is allowed to be skipped
- allow +/- as precedent sign
- allow scientific format as 2e10, 2e+10, 2e-10
"""


class Solution(object):
    # @param s, a string
    # @return a boolean
    @staticmethod
    def is_number(s):
        import re
        s = s.strip()
        # +/-可选；整数/带整数部分的小数/不带整数部分的纯小数；可选的科学表示法
        result = re.match(r"^[\+\-]?((\d+(\.\d*)?)|(\.\d+))(e[\+\-]?\d+)?$", s)
        return True if result is not None else False


if __name__ == "__main__":
    s = " 0"
    print "is_number(%s)=[%s]" % (s, Solution.is_number(s))
    s = " 0.1"
    print "is_number(%s)=[%s]" % (s, Solution.is_number(s))
    s = "abc"
    print "is_number(%s)=[%s]" % (s, Solution.is_number(s))
    s = "1 "
    print "is_number(%s)=[%s]" % (s, Solution.is_number(s))
    s = "2e10"
    print "is_number(%s)=[%s]" % (s, Solution.is_number(s))
    s = "e9"
    print "is_number(%s)=[%s]" % (s, Solution.is_number(s))  #应该是false
    s = "3."
    print "is_number(%s)=[%s]" % (s, Solution.is_number(s))  #应该是true