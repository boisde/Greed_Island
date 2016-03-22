# NodeSet get_successor(Node node);
# Node A, Node B;

#
# def top_sort(W):
#     return W
#
#
# def dag_sp(W, s, t):
#     d = {u:float('inf') for u in W}
#     d[s] = 0
#     for u in top_sort(W):
#         if u == t: break
#         for v in W[u]:
#             d[v] = min(d[v], d[u] + W[u][v])
#     return d[t]
#
#
# W={0:{1:2,5:9},1:{2:1,3:2,5:6},2:{3:7},3:{4:2,5:3},4:{5:4},5:{}}
# s,t=0,5
# print(dag_sp(W,s,t)) #7


class StableSet(object):
    def __init__(self):
        self.h_set = {}  # key=int, val=index
        self.size = 0

    def insert(self, number):
        if number in self.h_set:
            return -1
        else:
            self.size += 1
            self.h_set[number] = self.size
            return self.size

    def delete_elem(self, number):
        return self.h_set.pop(number)

    def has_elem(self, number):
        return number in self.h_set

    def iter_elem(self):
        return self.h_set.keys()


def fact(n):
    return fact_iter(n, 1)


def fact_iter(num, product):
    if num == 1:
        return product
    return fact_iter(num - 1, num * product)


if __name__ == "__main__":
    print fact(100)
