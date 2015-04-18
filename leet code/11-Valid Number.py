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
- allow scientific format as 2r10, 2e+10, 2e-10
"""


class Solution(object):
    # @param s, a string
    # @return a boolean
    @staticmethod
    def is_number(s):
        pass