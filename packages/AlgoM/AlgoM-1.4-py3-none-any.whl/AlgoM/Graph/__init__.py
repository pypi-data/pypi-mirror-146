#Adjacency list, undirected, weighted
from heapq import heappop as pop, heappush as push
class Graph:
    def __init__(self, n, adj):
        self.n = n 
        self.adj = adj


    #Djikstra
    def distance(self, s, e):
        self.vis = set()
        self.dist = [10**18]*self.n
        q = []
        self.dist[s] = 0
        push(q, (0, 0))
        while len(q) > 0:
            d, u = pop(q)
            if u in self.vis:
                continue
            self.vis.add(u)
            for v, w in self.adj[u]:
                new_dist = self.dist[u] + w
                if new_dist < self.dist[v]:
                    self.dist[v] = new_dist
                    push(q, (self.dist[v], v))
        return self.dist[e]


#----------------------------------------


#Adjacency list, directed, unweighted
class Graph2:
    def __init__(self, n, adj):
        self.n = n 
        self.adj = adj
        

    #Strongly connected components
    def scc(self):
      self.vis = [False] * self.n
      self.stack = []
      self.visited = [False] * self.n
      self.connected = []
      for i in range(self.n):
        if not self.visited[i]:
          self.fillOrder(i)
      
      curr = -1
      while self.stack:
        i = self.stack.pop()
        if not self.vis[i]:
          self.connected.append([])
          curr += 1
          self.DFS(i, curr)

      return self.connected

    def dfss(self, v, curr):
      self.vis[v] = True
      self.connected[curr].append(v)
      for i in self.adj[v]:
        if not self.vis[i]:
          self.dfss(i,curr)

    def fillOrder(self, v):
      self.visited[v] = True
      for i in self.adj[v]:
        if not self.visited[i]:
          self.fillOrder(i)
      self.stack.append(v)


    #Topological sort
    def topological_sort(self):
      self.vis = [False for _ in range(self.n)]
      self.ans = []
      for node in range(self.n):
        if not self.vis[node]:
          self.dfst(node)
      self.ans.reverse()
      return self.ans
      
    def dfst(self, node):
      self.vis[node] = True
      for neigh in self.adj[node]:
        if self.vis[neigh] == False:
          self.dfst(neigh)
      self.ans.append(node)


    #Detect cycle 
    def cyclic(self):
      self.vis = [False for _ in range(self.n)]
      self.stack = [False for _ in range(self.n)]
      for node in range(self.n):
        if self.vis[node] == False:
          if self.cycle(node):
            return True
      return False

    def cycle(self, v):
      self.visited[v] = True
      self.recStack[v] = True
      for neighbour in self.adj[v]:
        if self.vis[neighbour] == False:
          if self.cycle(neighbour):
            return True
          elif self.stack[neighbour] == True:
            return True

      self.stack[v] = False
      return False

    #Articulation points (returns two lists, first of articulation points and second of bridges)
    def articulation(self, argument):
      self.low = [0 for _ in range(self.n)]
      self.num = [-1 for _ in range(self.n)]
      self.c = 0
      self.root = 0
      self.root_children = 0
      self.ans = [0 for _ in range(self.n)]
      self.parent = [0] * self.n
      self.bridges = []
      for u in range(self.n):
        if self.num[u] == -1:
          self.root = u
          self.root_children = 0
          self.find(self.root)
          self.ans[self.root] = (self.root_children > 1)
      if argument == "bridges":
        return self.bridges
      else:
        points = []
        for i in range(self.n):
          if self.ans[i]:
            points.append(i)
        return points


    def find(self, node):
        self.num[node] = self.c
        self.c += 1
        self.low[node] = self.num[node]
        for neigh in self.adj[node]:
          if self.num[neigh] == -1:
            self.parent[neigh] = node
            if node == self.root:
              self.root_children += 1
            self.find(neigh)
            if self.low[neigh] >= self.low[node]:
              self.ans[node] = 1
          #for bridges
            if self.low[neigh] > self.low[node]:
              self.bridges.append([node, neigh])
            self.low[node] = min(self.low[node], self.low[neigh])
          elif neigh != self.parent[node]:
            self.low[node] = min(self.low[self.u], self.num[neigh])




#----------------------------------------

#Adjacency list, undirected, unweighted
#class Graph3:
class Graph3:
    def __init__(self, n, adj):
        self.n = n 
        self.adj = adj



#----------------------------------------


#Adjacency list, directed, weighted
#class Graph4:
class Graph4:
    def __init__(self, n, adj):
        self.n = n 
        self.adj = adj



#----------------------------------------

#Adjacency matri, undirected, weighted
class Graph5:
    def __init__(self, n, adj):   
        self.adj = adj
        self.ans = [[float("inf") for _ in range(n)] for _ in range(n)]

    #Floyd Warshall
    def floyd_warshall(self):
        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                  self.ans[i][j] = min(self.ans[i][j], self.adj[i][k] + self.adj[k][j])
    def dist(self, x, y):
      return self.ans[x][y]



#----------------------------------------
from collections import defaultdict
from copy import deepcopy as copy
class Dinitz:
    def __init__(self, sz, INF=10**10):
        self.G = [defaultdict(int) for _ in range(sz)]
        self.sz = sz
        self.INF = INF
        self.paths = []

    def add_edge(self, i, j, w):
        self.G[i][j] += w

    def bfs(self, s, t):
        level = [0]*self.sz
        q = [s]
        level[s] = 1
        while q:
            q2 = []
            for u in q:
                for v, w in self.G[u].items():
                    if w and level[v] == 0:
                        level[v] = level[u] + 1
                        q2.append(v)
            q = q2
        self.level = level
        return level[t] != 0

    def dfs(self, s, t, FLOW, path):
        if s in self.V: return 0
        if s == t: 
          self.path = path
          return FLOW
        self.V.add(s)
        L = self.level[s]
        for u, w in self.G[s].items():
            if u in self.dead: continue
            if w and L+1==self.level[u]:
                new_path = copy(path)
                new_path.append(u)
                F = self.dfs(u, t, min(FLOW, w), new_path)
                if F:
                    self.G[s][u] -= F
                    self.G[u][s] += F
                    return F
        self.dead.add(s)
        return 0
    

    def max_flow(self, s, t):
        flow = 0
        while self.bfs(s, t):
            self.dead = set()
            while True:
                self.V = set()
                self.path = []    
                pushed = self.dfs(s, t, self.INF, [])
                if not pushed: break
                self.paths.append(self.path)
                flow += pushed
        return self.paths, flow

