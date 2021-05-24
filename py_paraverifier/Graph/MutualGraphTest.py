#Author:Hongjian Jiang

from Graph import Vertex,Graph

g = Graph()
g.addVertex("root", "a[2] = C & a[1] = T& x = true")
g.addVertex("first", "a[2] = C & x = true")
g.addVertex("second", "a[2] = C & a[1] = T")
g.addVertex("third", "a[1] = T & x= true")
g.addVertex("fourth", "a[2] = C")
g.addVertex("fifth", "x = true")
g.addVertex("sixth", "a[1] = T")

g.addEdge("root", "first", 0)
g.addEdge("root", "second", 0)
g.addEdge("root", "third", 0)
g.addEdge("first", "fourth", 0)
g.addEdge("first", "fifth", 0)
g.addEdge("second", "fourth", 0)
g.addEdge("second", "sixth", 0)
g.addEdge("third", "fifth", 0)
g.addEdge("third", "sixth", 0)

for v in g:
    for w in v.getConnections():
        print("( %s -> %s , %s )" % (v.getId(), w.getId(),v.getInfo()))