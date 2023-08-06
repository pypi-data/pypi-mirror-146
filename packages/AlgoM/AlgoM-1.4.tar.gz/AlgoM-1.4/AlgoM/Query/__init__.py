#Segment tree for sum; 0-indexed; all intervals are inclusive
import math
class SegmentTreeSum:
    def __init__(self, n, arr):
        self.t = [0 for _ in range(4*n)]
        self.n = n
        self.arr = arr
        self.build(arr, 1, 0, n-1)

    def build(self, a, v, tl, tr):
        if (tl == tr):
            self.t[v] = a[tl]
        else:
            tm = (tl + tr) // 2
            self.build(a, v*2, tl, tm)
            self.build(a, v*2+1, tm+1, tr)
            self.t[v] = self.t[v*2] + self.t[v*2+1]

    def query(self, v, tl, tr, l, r):
        if l > r:
            return 0
        if l == tl and r == tr:
            return self.t[v]
        tm = (tl + tr) // 2
        return self.query(v*2, tl, tm, l, min(r, tm)) + self.query(v*2+1, tm+1, tr, max(l, tm+1), r)


    def update(self, v, tl, tr, pos, new_val):
        if tl == tr:
            self.t[v] = new_val
        else:
            tm = (tl + tr) // 2
            if pos <= tm:
                self.update(v*2, tl, tm, pos, new_val)
            else:
                self.update(v*2+1, tm+1, tr, pos, new_val)
                self.t[v] = self.t[v*2] + self.t[v*2+1]
    
    
#Segment tree for max; also has find first element greater than x query; inclusive and 0-indexed
class SegmentTreeMax:
    def __init__(self, n, arr):
        self.t = [0 for _ in range(4*n)]
        self.n = n
        self.arr = arr
        self.build(arr, 1, 0, n-1)
    def build(self, a, v, tl, tr):
        if (tl == tr):
            self.t[v] = a[tl]
        else:
            tm = (tl + tr) // 2
            self.build(a, v*2, tl, tm)
            self.build(a, v*2+1, tm+1, tr)
            self.t[v] = max(self.t[v*2], self.t[v*2+1])

    def query(self, v, tl, tr, l, r):
        if l > r:
            return 0
        if l == tl and r == tr:
            return self.t[v]
        tm = (tl + tr) // 2
        return max(self.query(v*2, tl, tm, l, min(r, tm)), self.query(v*2+1, tm+1, tr, max(l, tm+1), r))


    def update(self, v, tl, tr, pos, new_val):
        if tl == tr:
            self.t[v] = new_val
        else:
            tm = (tl + tr) // 2
            if pos <= tm:
                self.update(v*2, tl, tm, pos, new_val)
            else:
                self.update(v*2+1, tm+1, tr, pos, new_val)
                self.t[v] = max(self.t[v*2], self.t[v*2+1])
                
    def first_greater(self,v, lv, rv, l, r, x): 
        if lv > r or rv < l:
            return -1
        if l <= lv and rv <= r:
            if self.t[v] <= x:
                return -1
            while lv != rv:
                mid = lv + (rv-lv) // 2
                if self.t[2*v] > x:
                    v = 2*v
                    rv = mid
                else:
                    v = 2*v+1
                    lv = mid +1
            return lv
        mid = lv +(rv-lv) // 2
        rs = self.first_greater(2*v, lv, mid, l, r, x)
        if rs != -1:
            return rs
        return self.first_greater(2*v+1, mid+1, rv, l, r, x)


#same as above but min 
class SegmentTreeMin:
    def __init__(self, n, arr):
        self.t = [0 for _ in range(4*n)]
        self.n = n
        self.arr = arr
        self.build(arr, 1, 0, n-1)

    def build(self, a, v, tl, tr):
        if (tl == tr):
            self.t[v] = a[tl]
        else:
            tm = (tl + tr) // 2
            self.build(a, v*2, tl, tm)
            self.build(a, v*2+1, tm+1, tr)
            self.t[v] = max(self.t[v*2], self.t[v*2+1])

    def query(self, v, tl, tr, l, r):
        if l > r:
            return 0
        if l == tl and r == tr:
            return self.t[v]
        tm = (tl + tr) // 2
        return max(self.query(v*2, tl, tm, l, min(r, tm)), self.query(v*2+1, tm+1, tr, max(l, tm+1), r))


    def update(self, v, tl, tr, pos, new_val):
        if tl == tr:
            self.t[v] = new_val
        else:
            tm = (tl + tr) // 2
            if pos <= tm:
                self.update(v*2, tl, tm, pos, new_val)
            else:
                self.update(v*2+1, tm+1, tr, pos, new_val)
                self.t[v] = max(self.t[v*2], self.t[v*2+1])

    

#Sparse table for minimum on a segment (without updates, O(1) queries O(nlog(n)) build; inclusive intervals
class SparseTableMin:
    def __init__(self, arr, n):
        self.lookup = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(0, n):
            self.lookup[i][0] = arr[i]
        j = 1
        while (1 << j) <= n:
            i = 0
            while (i + (1 << j) - 1) < n:
                if (self.lookup[i][j - 1] <
                    self.lookup[i + (1 << (j - 1))][j - 1]):
                    self.lookup[i][j] = self.lookup[i][j - 1]
                else:
                    self.lookup[i][j] = self.lookup[i + (1 << (j - 1))][j - 1]
                i += 1
            j += 1       
    #Returns minimum of arr[L..R] in constant time 
    def query(self, L, R):
        j = int(math.log2(R - L + 1))
        if self.lookup[L][j] <= self.lookup[R - (1 << j) + 1][j]:
            return self.lookup[L][j]
        else:
            return self.lookup[R - (1 << j) + 1][j]




import sys
sys.setrecursionlimit(10**5)
class Sat:
    def __init__(self, no_vars):
        self.size = no_vars*2
        self.no_vars = no_vars
        self.adj = [[] for _ in range(self.size)]
        self.back = [[] for _ in range(self.size)]
    def add_imply(self, i, j):
        self.adj[i].append(j)
        self.back[j].append(i)
    def add_or(self, i, j):
        self.add_imply(i^1, j)
        self.add_imply(j^1, i)
    def add_xor(self, i, j):
        self.add_or(i, j)
        self.add_or(i^1, j^1)
    def add_eq(self, i, j):
        self.add_xor(i, j^1)
    
    def dfs1(self, i):
        if i in self.marked: return
        self.marked.add(i)
        for j in self.adj[i]:
            self.dfs1(j)
        self.stack.append(i)

    def dfs2(self, i):
        if i in self.marked: return
        self.marked.add(i)
        for j in self.back[i]:
            self.dfs2(j)
        self.comp[i] = self.no_c

    def is_sat(self):
        self.marked = set()
        self.stack = []
        for i in range(self.size):
            self.dfs1(i)
        self.marked = set()
        self.no_c = 0
        self.comp = [0]*self.size
        while self.stack:
            i = self.stack.pop()
            if i not in self.marked:
                self.no_c += 1
                self.dfs2(i)
        for i in range(self.no_vars):
            if self.comp[i*2] == self.comp[i*2+1]:
                return False
        return True

    # assumes is_sat. 
    # If ¬xi is after xi in topological sort,
    # xi should be FALSE. It should be TRUE otherwise.
    # https://codeforces.com/blog/entry/16205
    def solution(self):
        V = []
        for i in range(self.no_vars):
            V.append(self.comp[i*2] > self.comp[i*2^1])
        return V

"""
if __name__ == '__main__':
    S = Sat(1)
    S.add_or(0, 0)
    print(S.is_sat())
    print(S.solution())
"""