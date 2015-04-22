"""
Implement strStr().

Returns the index of the first occurrence of needle in haystack,
or -1 if needle is not part of haystack.
"""


class Solution(object):
    # @param haystack, a string
    # @param needle, a string
    # @return an integer
    @staticmethod
    def str_str(haystack, needle):  # run time: (M-N)*N
        found_at = -1
        h_len = len(haystack)
        n_len = len(needle)
        if n_len == 0:
            return 0
        elif h_len < n_len or n_len == 0 or h_len == 0:
            return -1

        for hi in range(h_len-n_len+1):
            found_at = hi
            for nj in range(n_len):
                if haystack[hi+nj] != needle[nj]:
                    found_at = -1
            if found_at != -1:
                return found_at
        return -1


if __name__ == "__main__":
    print Solution.str_str("", "")  # 0
    print Solution.str_str("nnn", "")
    print Solution.str_str("", "nnn")
    print Solution.str_str("n", "nnn")
    print Solution.str_str("nnn", "nnn")  # 0
    print Solution.str_str("nnmn", "nnn")  # -1
    print Solution.str_str("nnmnnn", "nnn")  # 3