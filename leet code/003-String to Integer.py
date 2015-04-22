"""
Implement atoi to convert a string to an integer.

Hint: Carefully consider all possible input cases.
If you want a challenge, please do not see below and ask yourself what are the possible input cases.

Notes: It is intended for this problem to be specified vaguely
(ie, no given input specs). You are responsible to gather all the input requirements up front.

constraints:
- should strip string with white spaces
- string is allowed to have -/+ in the beginning
- string can contain additional characters after the first sequence of integer number
- if the first sequence of non-whitespace chars is not a valid number,
or either str empty or it contains only whitespaces, no conversion is performed.
- if no valid conversion can be performed, return 0.
- if the correct value is out of the range of representable values, INT_32_MAX or INT_32_MIN is returned.
"""


class Solution:
    @staticmethod
    def atoi(token):
        # import sys
        sys_max_int = 2147483647
        sys_max_int_neg_abs = sys_max_int+1
        # invalid token; strip whitespaces
        if not token:
            return 0
        token = token.strip()

        # token if there is a -/+ symbol
        is_negative = False
        if token[0] == '-':
            is_negative = True
            token = token[1:]
        elif token[0] == '+':
            token = token[1:]

        # strip precedent '0's
        token = token.lstrip('0')

        quotient, divisor, zeros = sys_max_int_neg_abs, 10, -1
        sysmax_arr = []
        while quotient != 0:
            remainder = quotient%divisor
            quotient /= divisor
            zeros += 1
            sysmax_arr.append(remainder)
        sysmax_arr = sysmax_arr[::-1]
        # print "zeros=[%d], sysmax_arr=%s" % (zeros, sysmax_arr)

        ctoi_arr = []
        for c in token:
            if '0' <= c <= '9':
                ctoi = ord(c) - ord('0')
                ctoi_arr.append(ctoi)
                # too large/small, out of range
                if len(ctoi_arr) > zeros+1:
                    return -sys_max_int_neg_abs if is_negative else sys_max_int
            # invalid char
            else:
                break

        # check if out of range
        is_out_of_range, all_digits_equal_sysmaxint_neg_abs = False, False
        if len(ctoi_arr) == len(sysmax_arr):
            for i in range(len(ctoi_arr)):
                if ctoi_arr[i] < sysmax_arr[i]:
                    all_digits_equal_sysmaxint_neg_abs = False
                    break
                elif ctoi_arr[i] > sysmax_arr[i]:
                    is_out_of_range = True
                    all_digits_equal_sysmaxint_neg_abs = False
                    break
                all_digits_equal_sysmaxint_neg_abs = True
        if all_digits_equal_sysmaxint_neg_abs and is_negative:
            return -sys_max_int_neg_abs
        elif all_digits_equal_sysmaxint_neg_abs:
            return sys_max_int
        elif is_out_of_range:
            return -sys_max_int_neg_abs if is_negative else sys_max_int

        # do conversion
        N = len(ctoi_arr)
        final = 0
        for i in range(N):
            final += ctoi_arr[i]*(10**(N-1-i))
        return -final if is_negative else final

if __name__ == "__main__":
    print "token=[%s], output=[%s]" % ("", Solution.atoi(""))  # 0
    print "token=[%s], output=[%s]" % ("-1", Solution.atoi("-1"))  # -1
    print "token=[%s], output=[%s]" % ("2147483648", Solution.atoi("2147483648"))  # 2147483647
    print "token=[%s], output=[%s]" % ("-2147483647", Solution.atoi("-2147483647"))  # -2147483647
    print "token=[%s], output=[%s]" % ("-2147483648", Solution.atoi("-2147483648"))  # -2147483648
    print "token=[%s], output=[%s]" % ("      -11919730356x", Solution.atoi("      -11919730356x"))  # -2147483648
    print "token=[%s], output=[%s]" % ("    +11191657170", Solution.atoi("    +11191657170"))  # 2147483647
