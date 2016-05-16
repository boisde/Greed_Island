if __name__ == "__main__":
    # N = int(input())
    # S = str(raw_input())
    # M = int(input())
    # for _ in range(M):
    #     l, r, k_times = map(int, raw_input().split())
    #     left_s = S[:l - 1]
    #     right_s = S[r:]
    #
    #     part = S[l - 1:r]
    #     k_times %= len(part)
    #     if k_times != 0:
    #         left_part = part[0:len(part) - k_times]
    #         right_part = part[-k_times:]
    #         part = right_part + left_part
    #
    #     S = left_s + part + right_s
    #
    # print S
    import pickle
    import json
    a = "(dp0\nVmsg\np1\nV\\u5f88\\u9057\\u61be\\uff0c\\u60a8\\u63d0\\u4ea4\\u7684\\u8d44\\u6599\\u672a\\u901a\\u8fc7\\u8ba4\\u8bc1, \\u7406\\u7531: \\u8eab\\u4efd\\u8bc1\\u53f7\\u6709\\u8bef\\u3002\\u60a8\\u53ef\\u4ee5\\u4fee\\u6539\\u8d44\\u6599\\u5e76\\u91cd\\u65b0\\u63d0\\u4ea4\\uff0c\\u611f\\u8c22\\u60a8\\u7684\\u914d\\u5408\\u3002\np2\nsVtype\np3\nI1\nsVtel\np4\nV13245678901\np5\ns."
    b = pickle.loads(a)
    print b
    print json.dumps(b, ensure_ascii=False, indent=4)
