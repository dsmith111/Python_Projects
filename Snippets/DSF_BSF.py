# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
from collections import defaultdict

class Graph:
    
    def __init__(self):
        self.graph = defaultdict(list)
        
    def addEdge(self, n, e):
        self.graph[n].append(e)
        
        
    def DSF(self, n, visited):
        visited[n] = True
        print(n)
        
        for child in self.graph[n]:
            if visited[child]:
                continue
            
            self.DSF(child,visited)
        
    def DSF_Init(self, n):
        
        visited = dict.fromkeys(self.graph.keys(), False)
        self.DSF(n, visited)
            

        
    def BSF(self, n):
        
        queue = []
        visited = dict.fromkeys(self.graph.keys(), False)
        queue.append(n)
        visited[n] = True
        
        while queue:
            n = queue.pop(0)
            print(n)
            for child in self.graph[n]:
                if(visited[child]):
                    continue
                queue.append(child)
                visited[child] = True
                
            
            
g = Graph()
g.addEdge(0, 1)
g.addEdge(1, 2)
g.addEdge(1, 3)
g.addEdge(2, 4)
g.addEdge(3, 5)
g.addEdge(4, 6)
g.addEdge(5, 6)
g.addEdge(5, 7)
g.addEdge(6, 8)
g.addEdge(7, 8)
g.addEdge(8, 8)

print("DSF SEARCH")
g.DSF_Init(0)

print("\nBSF Search\n")
g.BSF(0)

